"""L18 "I'm upping my EU doom" (59.13 s), the user, 1 Oct 2026: "0.59 EU doom had some flaw". L18 has been v5's since
v5, like L7 (22.76 s). measure: what is off in L18 against the original and against L7's hook, and whether the
original's two hooks are the same melody, rhythm and backing (L18 sits exactly 80 beats after L7 at 132.007 BPM).
Found (measure): the original's two hooks sing the same notes on the same beats for "I'm upping my" (63, 63-70, 70);
"P(doom)" differs (L7: P on 63, doom on 63 falling to 60; L18: P on 70, doom scooping 68->63 and held) and so does the
backing (correlation 0.57). In v12, L7 and L18 are the original singer up to "my", then v5's "EU doom". L18's flaw: v5
cut in at the old word start, 59.96 s; L18's "my" is held legato into the next word (L7's ends 70 ms earlier, in
silence), so the cut lands in the note: "my" drops to -45 dB 20 ms early, then the "E" starts 8-13 dB under the
original's "P" for 60 ms with left and right anti-phase (correlation -0.4..-0.2, original +0.8): a swallowed, hollow
E right at 1:00.
fix(base, kind) swaps the vocal over L18's own backing (out = base - V18 w + V7 w, BS-RoFormer estimates, equal-power
fades), L7's vocal taken from exactly 80 beats earlier:
  A  the original singer's "my" to its end (59.975), then L7's "EU doom" to 60.70 (out where the vocal dips before
     L19's "I")
  B  L7's whole hook (from the breath before "I'm" to 60.70); its "my" ends early, as L7's does
  C  the original's "my" to its end, L7's E onset, then L18's own E from 60.065 (same note) and its own "doom"
Run from audio/el_music with the analysis venv: l18_fix.py measure | build"""
import json, pathlib, sys
import numpy as np, librosa, scipy.signal as ss

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import V
import rof

SR = V.SR
L7, L18 = V.LYR[6], V.LYR[17]
BEAT = 60 / 132.007
D = 80 * BEAT  # L7 -> L18, 20 bars


def seg(y, a, b):
    return y[:, int(a * SR):int(b * SR)]


def f0(v):
    import parselmouth
    p = parselmouth.Sound(v.mean(0).astype(np.float64), SR).to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
    return p.xs(), p.selected_array["frequency"]


def env(x, w=0.01):
    n = int(w * SR)
    return 10 * np.log10(np.convolve(x ** 2, np.ones(n) / n, "same") + 1e-12)


def clicks(y, a, b):
    """times of sample-domain transients above 6 kHz that stand 15 dB over their 50 ms surroundings"""
    sos = ss.butter(4, 6000, "hp", fs=SR, output="sos")
    h = ss.sosfilt(sos, y.mean(0))
    e, bg = env(h, 0.002), env(h, 0.05)
    t = a + np.arange(len(h)) / SR
    hit = (e - bg > 15) & (e > e.max() - 30)
    return sorted({round(float(x), 3) for x in t[hit]})


def measure():
    mix, VO = V.mix, rof.original(V.mix)
    v12 = librosa.load(HERE / "pdoom_EU_v12.wav", sr=SR, mono=False)[0][:, : mix.shape[1]]
    a7, b7 = L7["start"] - 0.6, L7["end"] + 0.4
    a18, b18 = a7 + D, b7 + D
    print(f"L7 {L7['start']:.2f}-{L7['end']:.2f}, L18 {L18['start']:.2f}-{L18['end']:.2f}; L18 - L7 = {L18['start'] - L7['start']:.3f} s, 80 beats = {D:.3f} s")
    # the original's two hooks: backing, vocal, melody
    bk = mix - VO
    for name, y in (("mix", mix), ("vocal", VO), ("backing", bk)):
        x7, x18 = seg(y, a7, b7).mean(0), seg(y, a18 - 0.06, b18 + 0.06).mean(0)
        k = int(np.argmax(ss.correlate(x18, x7, "valid")))
        x18a = x18[k:k + len(x7)]
        r = np.corrcoef(x7, x18a)[0, 1]
        res = 20 * np.log10(np.std(x18a - x7 * np.dot(x7, x18a) / np.dot(x7, x7)) / np.std(x18a))
        print(f"original L7 vs L18 {name:8s}: best offset {(k / SR - 0.06) * 1000:+.1f} ms from 80 beats, correlation {r:.3f}, residual {res:+.1f} dB")
    t7, f7 = f0(seg(VO, a7, b7)); t18, f18 = f0(seg(VO, a18, b18))
    n = min(len(f7), len(f18)); both = (f7[:n] > 0) & (f18[:n] > 0)
    c = 1200 * np.log2(f18[:n][both] / f7[:n][both])
    print(f"original L18 melody vs L7 (same beat position): median {np.median(c):+.0f} cents, |c| > 50 on {np.mean(np.abs(c) > 50):.0%} of voiced frames, "
          f"voiced {np.mean(f7 > 0):.0%} / {np.mean(f18 > 0):.0%}")
    on = lambda v, a: a + librosa.onset.onset_detect(y=v.mean(0), sr=SR, hop_length=256, units="time", backtrack=False)
    print("  vocal onsets L7 (rel. to L7 start):", np.round(on(seg(VO, a7, b7), a7) - L7["start"], 2))
    print("  vocal onsets L18 (rel. to L18 start):", np.round(on(seg(VO, a18, b18), a18) - L18["start"], 2))
    # v12's hooks: vocals by RoFormer, against the original's and against each other
    E7, E18 = rof.separate(v12, a7, b7), rof.separate(v12, a18, b18)
    np.save(HERE.parents[1] / "analysis/work/l18_E.npy", np.stack([E7, E18[:, : E7.shape[1]]]))
    for name, E, O, a in (("L7", E7, seg(VO, a7, b7), a7), ("L18", E18, seg(VO, a18, b18), a18)):
        te, fe = f0(E); to, fo = f0(O)
        n = min(len(fe), len(fo)); both = (fe[:n] > 0) & (fo[:n] > 0)
        c = 1200 * np.log2(fe[:n][both] / fo[:n][both]); c = (c + 600) % 1200 - 600
        print(f"\nv12 {name} vs original: pitch median |{np.median(np.abs(c)):.0f}| cents; voiced {np.mean(fe > 0):.0%} vs {np.mean(fo > 0):.0%}")
        for w in V.LYR[6 if name == "L7" else 17]["words"]:
            s = slice(int((w["start"] - a) * 100), int((w["end"] - a) * 100))
            fw, ow = fe[s], fo[s]; b2 = (fw > 0) & (ow > 0)
            cw = (1200 * np.log2(fw[b2] / ow[b2]) + 600) % 1200 - 600 if b2.sum() > 2 else np.array([np.nan])
            le = lambda X: 10 * np.log10(np.mean(seg(X, w["start"] - a, w["end"] - a) ** 2) + 1e-12)
            mid = lambda X: X.mean(0); side = lambda X: (X[0] - X[1]) / 2
            wid = lambda X: 10 * np.log10(np.mean(side(seg(X, w["start"] - a, w["end"] - a)) ** 2 + 1e-12) / (np.mean(mid(seg(X, w["start"] - a, w["end"] - a)) ** 2) + 1e-12))
            print(f"  {w['w']:8s} cents {np.nanmedian(cw):+5.0f}  level {le(E) - le(O):+5.1f} dB  width {wid(E) - wid(O):+5.1f} dB  "
                  f"pitch-wobble {np.nanstd(cw):4.0f}")
    # v12's L18 against its own L7, aligned on 80 beats: where do the EU hooks differ?
    n = min(E7.shape[1], E18.shape[1])
    k = int(np.argmax(ss.correlate(E18[:, :n].mean(0), E7.mean(0)[int(0.05 * SR):n - int(0.05 * SR)], "valid"))) - int(0.05 * SR)
    print(f"\nv12 hook L18 vs L7 vocal: offset {k / SR * 1000:+.1f} ms from 80 beats")
    t7_, g7 = f0(E7); t18_, g18 = f0(E18)
    m = min(len(g7), len(g18)); b2 = (g7[:m] > 0) & (g18[:m] > 0)
    cc = np.full(m, np.nan); cc[b2] = 1200 * np.log2(g18[:m][b2] / g7[:m][b2])
    lv = env(E18.mean(0)[:n]) - env(E7.mean(0)[:n])
    for i in range(0, m, 5):
        t = a18 + i * 0.01
        li = lv[int(i * 0.01 * SR)] if int(i * 0.01 * SR) < len(lv) else np.nan
        if (np.isfinite(cc[i]) and abs(cc[i]) > 40) or abs(li) > 4:
            print(f"  {t:6.2f}s  L18-L7 pitch {cc[i]:+6.0f} c  level {li:+5.1f} dB")
    # seams, clicks, the old vocal under it
    for t in json.loads((HERE / "v12_sources.json").read_text())["L18"]["span"]:
        s = slice(int((t - 0.02) * SR), int((t + 0.02) * SR))
        print(f"seam {t:.3f}: {20 * np.log10(np.std(v12[:, s]) / np.std(mix[:, s])):+.1f} dB vs original")
    print("clicks in v12 L18:", clicks(seg(v12, a18, b18), a18, b18), " in the original:", clicks(seg(mix, a18, b18), a18, b18))
    print("clicks in v12 L7: ", clicks(seg(v12, a7, b7), a7, b7), " in the original:", clicks(seg(mix, a7, b7), a7, b7))
    for name, E, a, b in (("L7", E7, a7, b7), ("L18", E18, a18, b18)):
        rest_v, rest_o = seg(v12, a, b) - E, seg(mix, a, b) - seg(VO, a, b)
        d = 10 * np.log10(np.mean((rest_v - rest_o) ** 2) / np.mean(rest_o ** 2))
        print(f"v12 {name} backing (mix - vocal) vs the original's: difference {d:+.1f} dB (old vocal left under the new one, holes)")


W = (58.60, 61.20)  # L18 window the vocals are separated over
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_v12_L18 - EU doom fix"
NAMES = {"A": "fix A - L7's EU doom sung in L18", "B": "fix B - L7's whole hook sung in L18",
         "C": "fix C - L18's own EU doom, its E onset from L7"}


def quiet(v1, v2, lo, hi):
    """time in [lo, hi] where the two vocals (L18 window) are quietest together, 10 ms RMS"""
    e = env((v1 + v2).mean(0)); t = W[0] + np.arange(len(e)) / SR
    w = (t >= lo) & (t <= hi)
    return float(t[w][np.argmin(e[w])])


def fix(base, kind, verbose=True):
    E18 = rof.separate(base, *W)
    # fine offset of L7's hook against 80 beats, on the EU (A, C) or the whole hook (B)
    a, b = (59.98, 60.40) if kind in "AC" else (59.10, 60.40)
    pad = int(0.04 * SR)
    E7w = rof.separate(base, W[0] - D - 0.05, W[1] - D + 0.05)
    x = E18.mean(0)[int((a - W[0]) * SR):int((b - W[0]) * SR)]
    y = E7w.mean(0)[int((a - W[0] + 0.05) * SR) - pad:int((b - W[0] + 0.05) * SR) + pad]
    kx = int(np.argmax(ss.correlate(y, x, "valid"))) - pad  # cross-correlation's offset: it locks onto "doom", whose notes
    k = 0  # differ between the hooks, and puts L7's E 40 ms late; the original's hook onsets sit on the 80-beat grid within
    #        10-20 ms ("I'm", "up", "my", "doom"), so L7's vocal goes in exactly 80 beats later
    E7 = E7w[:, int(0.05 * SR) + k:int(0.05 * SR) + k + E18.shape[1]]
    t_in = {"A": quiet(E18, E7, 59.94, 59.99), "C": quiet(E18, E7, 59.94, 59.99), "B": quiet(E18, E7, 59.00, 59.09)}[kind]
    t_out = {"A": 60.69, "B": 60.69, "C": 60.065}[kind]
    if kind in "AB":
        t_out = quiet(E18, E7, 60.64, 60.71)
    fade = 0.03
    t = W[0] + np.arange(E18.shape[1]) / SR
    out = base.copy()
    i0 = int(W[0] * SR)
    if kind == "B":
        w = np.clip(np.minimum((t - t_in) / fade + 0.5, (t_out - t) / fade + 0.5), 0, 1)
        out[:, i0:i0 + E18.shape[1]] = base[:, i0:i0 + E18.shape[1]] - E18 + E18 * np.cos(w * np.pi / 2) + E7 * np.sin(w * np.pi / 2)
    else:
        # A, C: "my" is the original singer's, but v5's cut faded it 20 ms early (-45 dB at 59.97): the original's own
        # "my" back from 59.90 (inside the held note, where v12 is the original singer) to 59.975, the instant before its
        # P; L7's E comes in there on the same note (12 ms crossfade), and out at t_out
        t_in, tc = 59.90, 59.975
        VOw = seg(rof.original(V.mix), *W)[:, : E18.shape[1]]
        wa = np.clip((t - t_in) / fade + 0.5, 0, 1)
        x = np.clip((t - tc) / 0.012 + 0.5, 0, 1)
        wb = np.clip((t_out - t) / fade + 0.5, 0, 1)
        # v12's vocal there is the original singer's, so the join into it is linear (equal power would lift two equal
        # signals by up to 3 dB mid-fade); the joins to L7's take, a different recording, are equal power
        g_e = np.where(t < tc, 1 - wa, np.cos(wb * np.pi / 2))
        g_vo = wa * np.cos(x * np.pi / 2)
        g_7 = np.sin(x * np.pi / 2) * np.sin(wb * np.pi / 2)
        out[:, i0:i0 + E18.shape[1]] = base[:, i0:i0 + E18.shape[1]] - E18 + E18 * g_e + VOw * g_vo + E7 * g_7
    if verbose:
        print(f"fix {kind}: L7's vocal 80 beats later (cross-correlation would say {kx / SR * 1000:+.1f} ms), swapped {t_in:.3f}-{t_out:.3f} s", flush=True)
    return out, (t_in, t_out)


def assess(y, mix, VO, spans=()):
    """L18 in y against the original: the E onset, the dip before it, pitch, clarity, seams, the backing"""
    import parselmouth
    E = rof.separate(y, *W)
    O = seg(VO, *W)
    at = lambda v, a, b: v[:, int((a - W[0]) * SR):int((b - W[0]) * SR)]
    lv = lambda v, a, b: 10 * np.log10(np.mean(at(v, a, b).mean(0) ** 2) + 1e-12)
    lr = lambda v, a, b: float(np.corrcoef(*at(v, a, b))[0, 1])
    def hnr(v, a, b):
        h = parselmouth.Sound(at(v, a, b).mean(0).astype(np.float64), SR).to_harmonicity_cc(time_step=0.01, minimum_pitch=90).values[0]
        return float(np.mean(h[h > 0]))
    def cents(a, b):
        _, fe = f0(at(E, a, b)); _, fo = f0(at(O, a, b)); n = min(len(fe), len(fo)); bt = (fe[:n] > 0) & (fo[:n] > 0)
        c = (1200 * np.log2(fe[:n][bt] / fo[:n][bt]) + 600) % 1200 - 600
        return float(np.median(np.abs(c))) if bt.sum() > 3 else float("nan")
    rest = lambda v, Vv: at(v, 59.9, 60.7) - at(Vv, 59.9, 60.7)
    r = dict(onset_lr=lr(E, 59.98, 60.05), onset_db=lv(E, 59.98, 60.04) - lv(O, 59.98, 60.04),
             dip_db=lv(E, 59.94, 59.98) - lv(O, 59.94, 59.98), hnr=hnr(E, 59.98, 60.62) - hnr(O, 59.98, 60.62),
             cents_hook=cents(59.10, 59.96), cents_eu=cents(59.98, 60.62),
             backing_db=float(10 * np.log10(np.mean((rest(seg(y, *W), E) - rest(seg(mix, *W), O)) ** 2) / np.mean(rest(seg(mix, *W), O) ** 2))),
             clicks=clicks(seg(y, 58.9, 60.9), 58.9, 60.9),
             seams=[(round(t, 3), round(float(20 * np.log10(np.std(y[:, int((t - .02) * SR):int((t + .02) * SR)]) /
                                                         np.std(mix[:, int((t - .02) * SR):int((t + .02) * SR)]))), 1)) for t in spans])
    return r


def build():
    import tempfile, subprocess, shutil
    import soundfile as sf
    mix, VO = V.mix, rof.original(V.mix)
    v12 = librosa.load(HERE / "pdoom_EU_v12.wav", sr=SR, mono=False)[0][:, : mix.shape[1]]
    src = json.loads((HERE / "v12_sources.json").read_text())["L18"]["span"]
    DESK.mkdir(parents=True, exist_ok=True)
    a, b = L18["start"] - 2.0, L18["end"] + 1.5

    def clip(y, name):
        with tempfile.TemporaryDirectory() as d:
            sf.write(f"{d}/x.wav", y[:, int(a * SR):int(b * SR)].T, SR)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/x.wav", "-af", "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse",
                            "-b:a", "256k", str(DESK / f"L18 {name}.mp3")], check=True)
    clip(mix, "original - I'm upping my P(doom)")
    clip(v12, "current (v12, in the video) - I'm upping my EU doom")
    res = {"current": assess(v12, mix, VO, src)}
    for kind in "ABC":
        out, sp = fix(v12, kind)
        clip(out, NAMES[kind])
        res[kind] = assess(out, mix, VO, sp) | {"span": [round(x, 3) for x in sp]}
    res["original"] = assess(mix, mix, VO)
    (HERE.parents[1] / "analysis/work/l18_fix.json").write_text(json.dumps(res, indent=1, default=float))
    hdr = f"{'clip':10s} {'E onset L/R':>11s} {'E onset dB':>10s} {'dip dB':>7s} {'clarity dB':>10s} {'pitch hook c':>12s} {'pitch EU c':>10s} {'backing dB':>10s}  clicks / seams"
    print(hdr)
    for k, r in res.items():
        print(f"{k:10s} {r['onset_lr']:11.2f} {r['onset_db']:+10.1f} {r['dip_db']:+7.1f} {r['hnr']:+10.1f} {r['cents_hook']:12.0f} {r['cents_eu']:10.0f} "
              f"{r['backing_db']:+10.1f}  {r['clicks']} {r['seams']}")


if __name__ == "__main__":
    {"measure": measure, "build": build}[sys.argv[1]]()
