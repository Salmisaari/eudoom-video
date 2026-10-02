"""Compare review clips with the original by measurement, not by ear or Whisper.

Every clip in eu_v8_lines is cut from the song at the same place (line start - 0.8 s), so a clip and its
"original" share one timeline. Each is split with the BS-RoFormer vocal model (SDR 12.97; htdemucs_ft ~9) (not the Demucs models the
swaps were built with, so the builder's own separation errors don't cancel out), and on the lead vocal, per 10 ms:
  pitch   Praat f0 of the mid channel, in cents against the original
  level   RMS of the mid channel 100 Hz-8 kHz, dB
  bright  energy above 4.5 kHz (s, sh, ch, t, breath), dB
  width   side / mid, dB (how wide the vocal sits)
  bands   long-term spectrum per octave (125 Hz-8 kHz) over the voiced frames, relative to the vocal's total
and on the rest (mix - lead): the difference to the original's rest, dB against it (old vocal leaking, holes in
the band). Summed per original word. Writes a table and a plot per line to analysis/qa/compare_<line>.png.
Run: cd analysis && uv run python ../audio/el_music/compare.py L9-10 E J"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "analysis"))
import common
import numpy as np, librosa, soundfile as sf, scipy.signal as ss

SR, HOP = 44100, 441
LINES = pathlib.Path.home() / "Desktop/suno_test/eu_v8_lines"
WORK = common.WORK / "cmp"; WORK.mkdir(exist_ok=True)
LYR = json.loads((common.DATA / "lyrics.json").read_text())["lines"]
MODEL = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
_sep = None


def words(label):
    ns = [int(x) for x in label[1:].split("-")]
    ws = [w for n in range(ns[0], ns[-1] + 1) for w in LYR[n - 1]["words"]]
    return LYR[ns[0] - 1]["start"] - 0.8, ws


def clip(label, key):
    return next(p for p in LINES.glob(f"{label}{key} - *.mp3"))


def split(path):
    """(mix, lead vocal) of a clip, stereo float32 at 44.1 kHz; cached in analysis/work/cmp."""
    global _sep
    stem = WORK / path.stem.replace(" ", "_")
    vf = stem.with_name(stem.name + "_voc.wav")
    y = librosa.load(path, sr=SR, mono=False)[0]
    if not vf.exists():
        if _sep is None:
            import beartype  # its checks fail on this Python for the RoFormer's type hints; they only check types
            beartype.beartype = lambda f=None, **k: f if f is not None else (lambda g: g)
            from audio_separator.separator import Separator
            _sep = Separator(model_file_dir=str(common.ROOT / ".cache/audio-separator"), output_dir=str(WORK),
                             normalization_threshold=1.0, log_level=40)
            _sep.load_model(model_filename=MODEL)
        wav = stem.with_suffix(".in.wav")
        sf.write(wav, y.T, SR)
        _sep.separate(str(wav), custom_output_names={"Vocals": vf.stem, "Instrumental": vf.stem.replace("_voc", "_inst")})
        wav.unlink()
    v = sf.read(vf, dtype="float32", always_2d=True)[0].T
    n = min(y.shape[1], v.shape[1])
    return y[:, :n], v[:, :n]


def feats(y, v):
    import parselmouth
    mid, side = v.mean(0), (v[0] - v[1]) / 2
    S = lambda x: np.abs(librosa.stft(x, n_fft=2048, hop_length=HOP)) ** 2
    Pm, Ps = S(mid), S(side)
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    db = lambda p: 10 * np.log10(p + 1e-10)
    body = (f > 100) & (f < 8000)
    p = parselmouth.Sound(mid.astype(np.float64), SR).to_pitch(time_step=HOP / SR, pitch_floor=90, pitch_ceiling=1000)
    f0 = np.interp(np.arange(Pm.shape[1]) * HOP / SR, p.xs(), p.selected_array["frequency"], left=0, right=0)
    rest = S((y - v).mean(0))
    edges = 125 * 2 ** np.arange(0, 7)  # 125 ... 8k
    return dict(level=db(Pm[body].sum(0)), bright=db(Pm[f > 4500].sum(0)), width=db(Ps[body].sum(0)) - db(Pm[body].sum(0)),
                f0=f0, Pm=Pm, f=f, rest=rest, bands=[(f >= a) & (f < 2 * a) for a in edges[:-1]], edges=edges[:-1])


def lag(a, b, max_ms=60):
    """ms by which b trails a (cross-correlation of the two level curves)"""
    a, b = a - a.mean(), b - b.mean()
    k = max_ms // 10
    c = [np.dot(a[k:-k], np.roll(b, -s)[k:-k]) for s in range(-k, k + 1)]
    return (int(np.argmax(c)) - k) * 10


def table(label, keys):
    t0, ws = words(label)
    O = feats(*split(clip(label, " original")))
    rows = {}
    for key in keys:
        C = feats(*split(clip(label, key)))
        n = min(len(O["f0"]), len(C["f0"]))
        per = []
        for w in ws:
            s = slice(int((w["start"] - t0) * 100), min(n, int((w["end"] - t0) * 100)))
            vo, vc = O["f0"][s] > 0, C["f0"][s] > 0
            both = vo & vc
            cents = 1200 * np.log2(C["f0"][s][both] / O["f0"][s][both]) if both.sum() > 3 else np.array([np.nan])
            lvl = lambda F: 10 * np.log10(np.mean(10 ** (F["level"][s] / 10)))
            brt = lambda F: 10 * np.log10(np.mean(10 ** (F["bright"][s] / 10)))
            rest_d = 10 * np.log10(np.abs(C["rest"][:, s] - O["rest"][:, s]).sum() / O["rest"][:, s].sum() + 1e-9)
            per.append(dict(w=w["w"], cents=float(np.nanmedian(cents)), lvl=lvl(C) - lvl(O), bright=brt(C) - brt(O),
                            width=float(np.median(C["width"][s]) - np.median(O["width"][s])),
                            lag=lag(O["level"][s], C["level"][s]) if s.stop - s.start > 15 else 0, rest=rest_d,
                            voiced=f"{vc.mean():.0%}/{vo.mean():.0%}"))
        s = slice(int((ws[0]["start"] - t0) * 100), min(n, int((ws[-1]["end"] - t0) * 100)))
        vv = (O["f0"][s] > 0) & (C["f0"][s] > 0)
        LT = lambda F: np.array([10 * np.log10(F["Pm"][b][:, s][:, vv].sum() + 1e-10) for b in F["bands"]])
        lo, lc = LT(O), LT(C)
        bands = (lc - lc.mean()) - (lo - lo.mean())
        rows[key] = dict(words=per, bands=dict(zip(map(int, O["edges"]), np.round(bands, 1).tolist())), C=C)
        print(f"\n{label}{key} vs original   (cents: pitch; lvl/bright/width/rest: dB; lag: ms, + = later)")
        print(f"  {'word':12s} {'cents':>6s} {'lvl':>5s} {'bright':>6s} {'width':>6s} {'lag':>4s} {'rest':>5s}  voiced")
        for r in per:
            print(f"  {r['w']:12s} {r['cents']:6.0f} {r['lvl']:5.1f} {r['bright']:6.1f} {r['width']:6.1f} {r['lag']:4d} {r['rest']:5.1f}  {r['voiced']}")
        print("  tone (octave bands, dB vs original):", rows[key]["bands"])
    plot(label, t0, ws, O, rows)
    return O, rows


def plot(label, t0, ws, O, rows):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(4, 1, figsize=(16, 12), sharex=True)
    t = lambda F: t0 + np.arange(len(F["f0"])) * HOP / SR
    st = lambda f0: np.where(f0 > 0, 12 * np.log2(np.maximum(f0, 1) / 440) + 69, np.nan)
    ax[0].plot(t(O), st(O["f0"]), "k", lw=3, label="original")
    for i, (k, r) in enumerate(rows.items()):
        C = r["C"]; c = f"C{i}"
        ax[0].plot(t(C), st(C["f0"]), c, lw=1.2, label=k)
        ax[1].plot(t(C), C["level"], c, lw=1)
        ax[2].plot(t(C), C["bright"], c, lw=1)
        ax[3].plot(t(C), C["width"], c, lw=1)
    ax[1].plot(t(O), O["level"], "k", lw=2); ax[2].plot(t(O), O["bright"], "k", lw=2); ax[3].plot(t(O), O["width"], "k", lw=2)
    for a, name in zip(ax, ("pitch (MIDI)", "level dB", ">4.5 kHz dB", "side/mid dB")):
        a.set_ylabel(name); a.grid(alpha=.3)
        for w in ws:
            a.axvline(w["start"], color="gray", lw=.5)
    for w in ws:
        ax[0].text(w["start"], ax[0].get_ylim()[1] - 1, w["w"], fontsize=9)
    ax[0].legend(loc="lower right", ncol=len(rows) + 1)
    ax[1].set_ylim(np.nanmax(O["level"]) - 45, np.nanmax(O["level"]) + 5)
    ax[3].set_ylim(-30, 5)
    ax[0].set_xlim(ws[0]["start"] - 0.2, ws[-1]["end"] + 0.2)
    fig.tight_layout(); fig.savefig(common.QA / f"compare_{label}.png", dpi=80); plt.close(fig)


if __name__ == "__main__":
    label, keys = sys.argv[1], sys.argv[2:]
    table(label, keys)
