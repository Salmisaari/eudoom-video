"""Which "where the faxes zoom" take sings L10's notes like the original, read from the vocal itself (BS-RoFormer
split, Praat f0 with a high octave-jump cost), not from Whisper. The original's notes (measured):
  with 62 (28.0-28.2)  a 55.5 (28.2-28.38)  baaag rises 66->70 at 28.42, holds 70 to 28.80  of 62 (28.88-29.1)
  shrooms 62->60 (29.3-29.7)
Per take and region: share of the original's voiced frames where the take is voiced within 50 cents (no octave
folding), and the take's level against the original's (dB). The held note is where round 5's take (eu2_low4) fails:
its "fa" holds 70 only to 28.62, then 0.2 s of "ks" where the original still sings.
Run: cd audio/el_music && ../../analysis/.venv/bin/python -u l10_scan.py"""
import json, pathlib, sys
import numpy as np, parselmouth

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V
import rof

A, B = 25.5, 30.5
REGIONS = {"room": (27.52, 27.98), "with": (28.0, 28.2), "a": (28.22, 28.38), "hold": (28.45, 28.80), "of": (28.88, 29.1),
           "shrooms": (29.3, 29.7), "L9": (26.32, 27.5)}


def f0(v):
    p = parselmouth.Sound(v.mean(0).astype(np.float64), V.SR).to_pitch_ac(
        time_step=0.01, pitch_floor=150, pitch_ceiling=900, octave_jump_cost=0.8, voicing_threshold=0.3)
    t = A + np.arange(int((B - A) * 100)) / 100
    f = np.array([p.get_value_at_time(x - A) or np.nan for x in t])
    lvl = 20 * np.log10(np.sqrt(np.convolve(v.mean(0) ** 2, np.ones(1764) / 1764, "same"))[(np.arange(len(t)) * 441)] + 1e-9)
    return t, f, lvl


def score(fo, lo, ft, lt, t):
    out = {}
    for k, (a, b) in REGIONS.items():
        s = (t >= a) & (t < b) & np.isfinite(fo)
        c = 1200 * np.log2(ft[s] / fo[s])
        out[k] = (float(np.mean(np.abs(np.nan_to_num(c, nan=9999)) < 50)), float(np.median(lt[s] - lo[s])))
    return out


if __name__ == "__main__":
    names = sorted(p.stem for p in HERE.glob("eu2_*.mp3"))
    vo = rof.original(V.mix)[:, int(A * V.SR):int(B * V.SR)]
    t, fo, lo = f0(vo)
    rows = {}
    for name in names:
        y = V.coarse(V.load_take(name), 27.94, 29.91)
        vt = rof.separate(y, A, B)
        _, ft, lt = f0(vt)
        rows[name] = score(fo, lo, ft, lt, t)
        r = rows[name]
        print(f"{name:14s} " + "  ".join(f"{k} {r[k][0]:4.0%} {r[k][1]:+5.1f}" for k in REGIONS), flush=True)
    (HERE / "l10_scan.json").write_text(json.dumps(rows, indent=1))
