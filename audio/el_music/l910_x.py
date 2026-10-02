"""L9-10X: V plus two things measured against the original's lead vocal (26.1-30.1 s) that don't move any timing:
  - air: on sung vowels V has 2 dB less 8-16 kHz (against 1-4 kHz) than the original singer: +2 dB high shelf
    above 7 kHz on voiced frames (20 ms ramps), consonants untouched
  - swell: V's phrase-level loudness moves 5.3 dB (300 ms, p90-p10) against the original's 6.8: its loudness contour
    at 300 ms pulled toward the original's (+-3 dB)
(W, an expander on the gaps plus compression, measured worse: the gap sound is mostly the take singing where the
original pauses, and the compression flattened the swells.)"""
import sys, pathlib
import numpy as np, librosa, parselmouth, scipy.signal as ss
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from l910_v import hook_v
from v8_refine import write, V


def air(x, db=2.0, fc=7000):
    p = parselmouth.Sound(x.mean(0).astype(np.float64), V.SR).to_pitch_ac(time_step=0.01, pitch_floor=150, pitch_ceiling=900)
    ts = np.arange(0, x.shape[1] / V.SR, 0.01)
    vo = np.array([np.isfinite(p.get_value_at_time(t)) for t in ts]).astype(float)
    w = np.clip(np.convolve(np.interp(np.arange(x.shape[1]) / V.SR, ts, vo), np.ones(882) / 882, "same"), 0, 1)
    b, a = ss.butter(2, fc / (V.SR / 2), "high")
    return (x + ss.filtfilt(b, a, x, axis=1) * (10 ** (db / 20) - 1) * w).astype(np.float32)


def swell(x, vo, db=3.0, win=0.3):
    k = int(win * V.SR)
    env = lambda y: 10 * np.log10(np.convolve(y.mean(0) ** 2, np.ones(k) / k, "same") + 1e-12)
    ex, eo = env(x), env(vo)
    act = (eo > eo.max() - 30) & (ex > ex.max() - 30)
    g = np.where(act, eo - ex, 0.0)
    g = np.clip(g - np.median(g[act]), -db, db) * act
    g = np.convolve(g, np.ones(k // 2) / (k // 2), "same")
    return (x * 10 ** (g / 20)).astype(np.float32)


def hook_x():
    v = hook_v()
    def f(vt, vo):
        v.a = f.a
        return air(swell(v(vt, vo), vo))
    return f


if __name__ == "__main__":
    import rof_clips
    write(l910.N, "eu2_low4", l910.PLAN, "bsroformer", False, rof_clips.ms(hook_x(), l910.N),
          "V with the original's air on the vowels and its phrase swells",
          "Trapped in the Brussels room, where the faxes zoom", label="L9-10", letter="X")
