"""Word-level VOCAL splicing: only the changed words change, only in the vocal; the band is the original.

For each changed-word span [ws, we] (original timeline):
  1. the take's vocal is separated (Demucs) around the span, after a coarse local alignment;
  2. its timing is warped onto the original vocal's (DTW on chroma + MFCC, rubberband --timemap; pitch kept);
  3. level and tone are matched to the original vocal of the line (RMS, 1/3-octave long-term spectrum);
  4. out = mix - V_orig*w + V_take*w, w = equal-power fades placed at the quietest vocal point near each edge.
Candidates per line are scored on the result: pitch-curve error on the span, and whether the line now fits the new
words better than the old ones (CTC margin, lyricfit.py). Winners are re-separated with htdemucs_ft and spliced.
Writes audio/el_music/pdoom_EU_v4.wav and vsplice_report.json."""
import json, pathlib, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf, scipy.signal as ss, torch

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis"))
import common  # noqa: F401  (model caches)
import lyricfit as F
from demucs.pretrained import get_model
from demucs.apply import apply_model

SR, HOP = 44100, 512
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
LYR = json.loads((ROOT / "data/lyrics.json").read_text())["lines"]

mix = librosa.load(ROOT / "audio/pdoom.mp3", sr=SR, mono=False)[0]
_v = sf.read(ROOT / "analysis/stems/htdemucs_ft/pdoom/vocals.wav", dtype="float32", always_2d=True)[0][1015:].T
VO = np.zeros_like(mix)
VO[:, : min(mix.shape[1], _v.shape[1])] = _v[:, : mix.shape[1]]

# the hooks must sing "you doom" rather than "P-doom" or a pronounced "E-U doom" (the E stays quiet)
HOOK = (["PEE DOOM", "EE YOU DOOM"], "YOU DOOM")
ALL_WORDS = lambda n: list(range(len(LYR[n - 1]["words"])))
# line: (changed word indices, old words as sung (or several to beat), new words as sung, display words replacing them)
PLAN = {
    7: ([3], *HOOK, "EU doom"), 18: ([3], *HOOK, "EU doom"), 29: ([3], *HOOK, "EU doom,"), 41: ([3], *HOOK, "EU doom"),
    9: ([3], "CHINESE", "BRUSSELS", "Brussels"),
    10: (ALL_WORDS(10), "WITH A BAG OF SHROOMS", "WHERE FAXES STILL ZOOM", "where faxes still zoom"),
    16: ([3], "ATOMS", "AY SEE MAX", "AC max"),
    17: ([0], "SYDNEY", "COOKIES", "Cookies,"),
    19: ([3, 4], "BASILISK BOOM", "BASIC INCOME GLOOM", "basic income gloom"),
    20: ([0], "EN VEE DEE AY", "AY ESS EM EL", "ASML"),
    22: ([3], "FLOPS", "FAXES", "faxes"),
    # 24 keeps the original audio ("em-el-pee"); no take sang "GDP" audibly, so only the screen says GDP (like NATO)
    25: ([1, 2], "VON NEUMANN'S", "PRIVATE CHATS", "private chats"),
    26: (ALL_WORDS(26), "SHARP LEFT TURN AND THERE YOU ARE", "SHARP LEFT OVERSEAS AND THERE YOU ARE",
         "Sharp left overseas and there you are"),  # three syllables need the whole line
    27: (ALL_WORDS(27), "WITHOUT A SINGLE SEE DEE AR", "WITHOUT A SINGLE GEE DEE PEE AR", "Without a single GDPR"),
    31: ([0], "KILLSWITCH", "BRUSSELS", "Brussels"),
    34: ([0, 1], "ORTHOGONALITY THESIS", "EUROPE OPEN BORDERS", "Europe open borders"),
    37: ([0, 1], "POST CHINCHILLA SUPER DENSE", "BUILD POST AY EYE TRENDS", "Build post AI trends"),
    40: ([0, 1, 2], "AR EL AITCH EF GOES ASKEW", "EE YOU INC FIXES EE YOU SOON", "EU Inc fixes EU soon"),
    45: (ALL_WORDS(45), "WHAT DID ILYA SEE WE'LL NEVER KNOW", "WHAT DID DRAGHI SEE WE'LL NEVER KNOW",
         "What did Draghi see? We'll never know"),
}
# takes the user already approved by ear (animatic_v3), kept as they were
FORCED = {27: ["eu2_low13"], 45: ["eu2_low14"]}
CANDIDATES_PER_LINE = 6

_models = {}


def separate(y, a, b, name="htdemucs"):
    """Stereo vocal of y over [a, b] s."""
    if name == "bsroformer":
        import rof
        return rof.separate(y, a, b)
    if name not in _models:
        _models[name] = get_model(name).eval()
    m = _models[name]
    seg = torch.tensor(y[:, int(a * SR):int(b * SR)], dtype=torch.float32)
    with torch.no_grad():
        out = apply_model(m, seg[None], device=DEV, split=True, overlap=0.25, progress=False)[0, m.sources.index("vocals")]
    return out.cpu().numpy()


def load_take(name):
    y = librosa.load(HERE / f"{name}.mp3", sr=SR, mono=False)[0]
    y = np.pad(y, ((0, 0), (0, max(0, mix.shape[1] - y.shape[1]))))[:, : mix.shape[1]]
    a, b = int(40 * SR), int(52 * SR)
    return y * mix[:, a:b].std() / y[:, a:b].std()


def coarse(y, a, b, m=int(0.08 * SR)):
    x = mix.mean(0)[int((a - 1.5) * SR):int((b + 1.5) * SR)]
    seg = y.mean(0)[int((a - 1.5) * SR) - m:int((b + 1.5) * SR) + m]
    return np.roll(y, -(int(np.argmax(ss.correlate(seg, x, "valid"))) - m), axis=1)


def feats(v):
    m = librosa.to_mono(v)
    c = librosa.feature.chroma_cqt(y=m, sr=SR, hop_length=HOP)
    mf = librosa.feature.mfcc(y=m, sr=SR, n_mfcc=13, hop_length=HOP)[1:]
    mf = (mf - mf.mean(1, keepdims=True)) / (mf.std(1, keepdims=True) + 1e-6)
    return np.vstack([c * 2, mf * 0.5])


def warp(vt, vo):
    """Time-warp take vocal vt onto original vocal vo (same window length): DTW path, smoothed over ~150 ms and
    limited to 0.7-1.4x local speed, then rubberband --timemap (pitch kept). Returns (vt', mean |shift| in ms)."""
    fo, ft = feats(vo), feats(vt)
    _, wp = librosa.sequence.dtw(X=fo, Y=ft, metric="cosine", global_constraints=True, band_rad=0.12)
    io, it = wp[::-1, 0], wp[::-1, 1]
    m = np.array([it[io == k].mean() for k in range(fo.shape[1])])  # take frame for each original frame
    m = np.convolve(np.pad(m, 6, mode="edge"), np.ones(13) / 13, "valid")
    for k in range(1, len(m)):
        m[k] = np.clip(m[k], m[k - 1] + 0.7, m[k - 1] + 1.4)
    m = np.clip(m, 0, ft.shape[1] - 1)
    n = vt.shape[1]
    step = max(1, int(0.1 * SR / HOP))
    pts, last = [(0, 0)], 0
    for k in range(step, len(m) - step, step):
        s_t = int(m[k] * HOP)
        if s_t > last:
            pts.append((s_t, k * HOP)); last = s_t
    pts.append((n, vo.shape[1]))
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "map.txt").write_text("".join(f"{i} {o}\n" for i, o in pts))
        sf.write(f"{d}/in.wav", vt.T, SR)
        subprocess.run(["rubberband", "-q", "--fine", "-t", f"{vo.shape[1] / n:.6f}", "-M", f"{d}/map.txt",
                        f"{d}/in.wav", f"{d}/out.wav"], check=True, capture_output=True)
        out = sf.read(f"{d}/out.wav", dtype="float32", always_2d=True)[0].T
    out = np.pad(out, ((0, 0), (0, max(0, vo.shape[1] - out.shape[1]))))[:, : vo.shape[1]]
    return out, float(np.mean(np.abs(m - np.arange(len(m)))) * HOP / SR * 1000)


def tone_match(vt, vo):
    f, Po = ss.welch(librosa.to_mono(vo), SR, nperseg=4096)
    _, Pt = ss.welch(librosa.to_mono(vt), SR, nperseg=4096)
    g = 10 * np.log10((Po + 1e-12) / (Pt + 1e-12))
    band = (f > 150) & (f < 9000)
    g -= np.median(g[band])
    lf = np.log2(np.maximum(f, 20))
    g = np.clip([np.median(g[np.abs(lf - x) < 1 / 6]) for x in lf], -4, 4)
    fir = ss.firwin2(1025, f / (SR / 2), 10 ** (np.array(g) / 20))
    return np.stack([ss.fftconvolve(ch, fir, "full")[512:512 + vt.shape[1]] for ch in vt])


def tune_to(vt, vo, max_cents=300, fold=True, half=4):
    """Pitch-correct the take vocal to the original's melody (Praat PSOLA, formants kept): the correction ratio
    orig/take is smoothed over ~80 ms so the take keeps its own vibrato; only notes within max_cents are moved.
    fold: aim for the original's note in the octave nearest the take (keeps the take's register); fold=False aims
    for the original's actual note. half: the correction is a median over 2*half+1 frames (10 ms each); smaller
    follows the original's own scoops and flicks, larger keeps the take's."""
    import parselmouth
    from parselmouth.praat import call
    snd_t, snd_o = parselmouth.Sound(librosa.to_mono(vt), SR), parselmouth.Sound(librosa.to_mono(vo), SR)
    pt = snd_t.to_pitch(time_step=0.01, pitch_floor=100, pitch_ceiling=1000)
    po = snd_o.to_pitch(time_step=0.01, pitch_floor=100, pitch_ceiling=1000)
    ts = pt.xs()
    ft = pt.selected_array["frequency"]
    fo = np.array([po.get_value_at_time(t) or np.nan for t in ts])
    ok = (ft > 0) & np.isfinite(fo) & (fo > 0)
    c = np.full(len(ts), np.nan)
    c[ok] = 1200 * np.log2(fo[ok] / ft[ok])
    if fold:
        c[ok] = (c[ok] + 600) % 1200 - 600  # nearest octave: keep the take's register
    c[np.abs(c) > max_cents] = np.nan
    cs = np.array([np.nanmedian(c[max(0, i - half):i + half + 1]) if np.isfinite(c[max(0, i - half):i + half + 1]).any() else np.nan
                   for i in range(len(c))])
    out = []
    for ch in vt:
        s_ch = parselmouth.Sound(ch, SR)
        man = call(s_ch, "To Manipulation", 0.01, 100, 1000)
        tier = call("Create PitchTier", "tuned", 0, s_ch.duration)
        for t, f, k in zip(ts, ft, cs):
            if f > 0:
                call(tier, "Add point", t, f * 2 ** ((0 if np.isnan(k) else k) / 1200))
        call([man, tier], "Replace pitch tier")
        res = call(man, "Get resynthesis (overlap-add)").values[0]
        out.append(np.pad(res, (0, max(0, len(ch) - len(res))))[: len(ch)])
    return np.array(out, dtype=np.float32)


def quiet_point(vo, vt, t0, lo, hi):
    """Time in [lo, hi] (s) where the two vocals are quietest together (20 ms RMS)."""
    e = librosa.feature.rms(y=librosa.to_mono(vo + vt), frame_length=882, hop_length=220)[0]
    t = t0 + np.arange(len(e)) * 220 / SR
    w = (t >= lo) & (t <= hi)
    return float(t[w][np.argmin(e[w])]) if w.any() else (lo + hi) / 2


def build(y, n, sep="htdemucs", warp_on=True, tune=False):
    """Take y's changed words for line n, fitted into the original vocal. Returns (new vocal track segment info)."""
    idx, old, new, _ = PLAN[n]
    ws, we = LYR[n - 1]["words"][idx[0]]["start"], LYR[n - 1]["words"][idx[-1]]["end"]
    a, b = LYR[n - 1]["start"] - 0.8, max(we, LYR[n - 1]["end"]) + 0.8  # whole line + context for DTW
    yl = coarse(y, ws, we)
    vt = separate(yl, a, b, sep)
    vo = VO[:, int(a * SR):int(a * SR) + vt.shape[1]]
    vt, severity = warp(vt, vo) if warp_on else (vt, 0.0)
    if tune:
        vt = tune_to(vt, vo)
    vt = tone_match(vt, vo)
    span = slice(int((ws - a) * SR), int((we - a) * SR))
    g = np.sqrt(np.mean(vo[:, span] ** 2) / (np.mean(vt[:, span] ** 2) + 1e-12))
    vt *= np.clip(g, 0.5, 2.0)
    t_in = quiet_point(vo, vt, a, ws - 0.08, ws + 0.02)
    t_out = quiet_point(vo, vt, a, we - 0.02, we + 0.08)
    return dict(a=a, vt=vt, vo=vo, t_in=t_in, t_out=t_out, ws=ws, we=we, severity=severity)


def apply(base_mix, base_voc, r, fade=0.03):
    """Swap the vocal between t_in and t_out: out = mix - Vo*w + Vt*w, w with equal-power fades."""
    a0 = int(r["a"] * SR)
    n = r["vt"].shape[1]
    t = r["a"] + np.arange(n) / SR
    w = np.clip(np.minimum((t - r["t_in"]) / fade + 0.5, (r["t_out"] - t) / fade + 0.5), 0, 1)
    g_in, g_out = np.sin(w * np.pi / 2), np.cos(w * np.pi / 2)
    out, voc = base_mix.copy(), base_voc.copy()
    seg_v = base_voc[:, a0:a0 + n] * g_out + r["vt"] * g_in
    out[:, a0:a0 + n] = base_mix[:, a0:a0 + n] - base_voc[:, a0:a0 + n] + seg_v
    voc[:, a0:a0 + n] = seg_v
    return out, voc


def score(n, r):
    """Pitch error on the span (octave-safe median cents) and CTC margin old->new on the spliced line vocal."""
    _, voc = apply(mix, VO, r)
    a, b = LYR[n - 1]["start"] - 0.2, LYR[n - 1]["end"] + 0.2
    line_v = librosa.to_mono(voc[:, int(a * SR):int(b * SR)])
    s0, s1 = int((r["ws"] - r["a"]) * SR), int((r["we"] - r["a"]) * SR)
    pv = [librosa.pyin(librosa.to_mono(x[:, s0:s1]), fmin=100, fmax=1000, sr=SR, frame_length=4096, hop_length=HOP)
          for x in (r["vt"], r["vo"])]
    both = pv[0][1] & pv[1][1]
    c = 1200 * np.log2(pv[0][0][both] / pv[1][0][both]) if both.any() else np.array([999.0])
    err = float(np.median(np.abs((c + 600) % 1200 - 600)))
    idx, old, new, _ = PLAN[n]
    words = [w["w"] for w in LYR[n - 1]["words"]]
    def sung(repl):
        return " ".join(w.upper().strip(",.?!\"“”") for w in words[: idx[0]]) + f" {repl} " + \
            " ".join(w.upper().strip(",.?!\"“”") for w in words[idx[-1] + 1:])
    em = F.emissions(librosa.resample(line_v, orig_sr=SR, target_sr=22050), 22050)
    olds = old if isinstance(old, list) else [old]
    return err, min(F.margin(em, sung(o), sung(new)) for o in olds)


def candidates(n):
    if n in FORCED:
        return FORCED[n]
    if n == 10:
        return [f"eu7_{k}" for k in range(1, 6)]
    if n == 22:
        return [f"eu8_{k}" for k in range(1, 6)]
    if n in (7, 18, 29, 41, 16, 19, 24, 25, 26, 34, 37, 40):
        return [f"eu6_{k}" for k in range(1, 11)]
    if n == 17:
        return [f"eu4_{k}" for k in range(1, 11)]
    cache = json.loads((HERE / "eu_final_cache.json").read_text())
    rows = [r for k, r in cache.items() if f"|L{n}|" in k and r["err"] <= 60 and r["iou"] >= 0.7]
    rows.sort(key=lambda r: -(r["margin"] + 10 * r["key"]))
    return [r["take"] for r in rows[:CANDIDATES_PER_LINE]]

if __name__ == "__main__":
    only = [int(x) for x in sys.argv[1:]] or sorted(PLAN)
    rep_f = HERE / "vsplice_report.json"
    report = json.loads(rep_f.read_text()) if rep_f.exists() else {}
    for n in only:
        rows = []
        whole_line = len(PLAN[n][0]) == len(LYR[n - 1]["words"])
        for name in candidates(n):
            y = load_take(name)
            for warp_on in ((True, False) if whole_line else (True,)):  # a whole-line swap may sound better unwarped
                r = build(y, n, warp_on=warp_on)
                err, margin = score(n, r)
                rows.append(dict(take=name, warp=warp_on, err=round(err), margin=round(margin, 1), shift_ms=round(r["severity"])))
                print(f"L{n:02d} {name:10s} warp={warp_on!s:5s} pitch {err:4.0f}c  fit {margin:+6.1f}  timing shift {r['severity']:4.0f} ms", flush=True)
        ok = [x for x in rows if (x["margin"] > 0 or n in FORCED) and x["err"] <= 80 and x["shift_ms"] <= 120] or rows
        best = min(ok, key=lambda x: x["err"] / 50 - x["margin"] / 10 + x["shift_ms"] / 60)
        report[str(n)] = dict(best=best, rows=rows)
        rep_f.write_text(json.dumps(report, indent=1))
        print(f"L{n:02d} -> {best['take']}", flush=True)
