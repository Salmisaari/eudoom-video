"""L9-10W: V ("ok quality, maybe good enough, but noise blended in; the original has more clarity and the song's
power"), with the two things measured against the original (lead vocal, BS-RoFormer split, 26.1-30.1 s):
  - in the gaps between syllables (the original singer's quietest quarter) V's vocal carries +4.8 dB at 100-1k Hz,
    +2.4 dB at 1-4 kHz, +1.3 dB at 4-8 kHz: reverb tails and bleed that smear the syllables together. A downward
    expander per band (ratio 1:2 below the take's own 35th-percentile level) takes out at most that much; notes above
    the threshold are untouched.
  - micro-dynamics: V's vocal is peakier than the original's (10 ms level p95-p50: 5.7 vs 4.8 dB; mix crest +0.7 dB),
    i.e. less dense: gentle compression (2:1 above its 60th percentile, 5 ms attack, 80 ms release, same loudness).
Everything else as V."""
import sys, pathlib
import numpy as np, librosa
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from l910_v import hook_v
from v8_refine import write, V

BANDS = [(100, 1000, 5.0), (1000, 4000, 3.0), (4000, 8000, 2.0), (8000, 16000, 0.0)]  # (lo, hi, max cut dB)


def expand(x, t0, a=26.1, b=30.1, pct=35):
    n_fft, hop = 2048, 441
    X = [librosa.stft(ch, n_fft=n_fft, hop_length=hop) for ch in x]
    P = (np.abs(X[0]) ** 2 + np.abs(X[1]) ** 2) / 2
    f = librosa.fft_frequencies(sr=V.SR, n_fft=n_fft)
    t = t0 + np.arange(P.shape[1]) * hop / V.SR
    act = (t >= a) & (t <= b)
    G = np.zeros_like(P)
    for lo, hi, cap in BANDS:
        sel = (f >= lo) & (f < hi)
        L = 10 * np.log10(P[sel].sum(0) + 1e-12)
        L = np.convolve(L, np.ones(3) / 3, "same")
        T = np.percentile(L[act], pct)
        g = -np.clip(T - L, 0, cap) * act  # 1:2 expansion below T, capped
        g = np.minimum.accumulate(np.stack([np.roll(g, k) for k in range(3)]), axis=0)[-1]  # hold 20 ms (no chatter)
        g = np.convolve(g, np.ones(5) / 5, "same")
        G[sel] = g[None]
    Y = [librosa.istft(Xc * 10 ** (G / 20), hop_length=hop, length=x.shape[1]) for Xc in X]
    return np.stack(Y).astype(np.float32)


def compress(x, ratio=2.0, pct=60, attack=0.005, release=0.08):
    m = x.mean(0)
    env = 10 * np.log10(np.convolve(m ** 2, np.ones(441) / 441, "same") + 1e-12)
    act = env > env.max() - 30
    T = np.percentile(env[act], pct)
    gr = -np.clip(env - T, 0, None) * (1 - 1 / ratio)
    sm = np.empty_like(gr); cur = 0.0
    ka, kr = np.exp(-1 / (attack * V.SR)), np.exp(-1 / (release * V.SR))
    for i, g in enumerate(gr):  # attack when reducing, release when recovering
        k = ka if g < cur else kr
        cur = k * cur + (1 - k) * g; sm[i] = cur
    y = x * 10 ** (sm / 20)
    return (y * np.sqrt(np.mean(x[:, act] ** 2) / (np.mean(y[:, act] ** 2) + 1e-12))).astype(np.float32)


def hook_w():
    v = hook_v()
    def f(vt, vo):
        v.a = f.a
        return compress(expand(v(vt, vo), f.a))
    return f


if __name__ == "__main__":
    import rof_clips
    write(l910.N, "eu2_low4", l910.PLAN, "bsroformer", False, rof_clips.ms(hook_w(), l910.N),
          "V with the gaps between syllables cleaned (expander) and the voice as dense as the original's (compression)",
          "Trapped in the Brussels room, where the faxes zoom", label="L9-10", letter="W")
