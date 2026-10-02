"""L24 "Forward SAP": the user hears the S as silent. The takes do sing it (eu22_3: a sibilant at 75.00-75.22 s,
HF-LF +19 dB; the original singer's "s" in "obsolete" is +26 dB), but pulling the take's vocal out with Demucs
leaves much of the hiss behind, and the original band under it has none. So the take's own "s" is lifted: the
frames in 74.9-75.35 s where >4 kHz outweighs 100-1500 Hz by 6 dB get a +DB high shelf above 3.5 kHz (10 ms
ramps). Nothing pitched is touched. Clips via v8_refine.write (the hook runs where build() would tune)."""
import sys, pathlib
import numpy as np, librosa, scipy.signal as ss
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v8_refine import write, V
from r22_clips import P24, P24_INS


def s_boost(db):
    def f(vt, vo):
        m = librosa.to_mono(vt); hop = 441
        S = np.abs(librosa.stft(m, n_fft=1024, hop_length=hop)); fr = librosa.fft_frequencies(sr=V.SR, n_fft=1024)
        d = 20 * np.log10(S[fr > 4000].sum(0) + 1e-9) - 20 * np.log10(S[(fr > 100) & (fr < 1500)].sum(0) + 1e-9)
        t = f.a + np.arange(len(d)) * hop / V.SR
        on = (d > 6) & (t >= 74.9) & (t <= 75.35)
        w = np.interp(np.arange(vt.shape[1]), np.arange(len(d)) * hop, on.astype(float))
        w = np.convolve(w, np.ones(441) / 441, "same")  # 10 ms ramps
        b, a = ss.butter(2, 3500 / (V.SR / 2), "high")
        hi = ss.lfilter(b, a, vt, axis=1)
        print(f"  s at {t[on].min():.2f}-{t[on].max():.2f} s, +{db} dB above 3.5 kHz", flush=True)
        return (vt + hi * (10 ** (db / 20) - 1) * w).astype(np.float32)
    return f


if __name__ == "__main__":
    for take, plan, kind in (("eu22_3", P24, "whole line"), ("eu22_3", P24_INS, "only the letters"),
                             ("eu24_4", P24, "whole line"), ("eu22_12", P24, "whole line")):
        write(24, take, plan, "htdemucs_ft", False, s_boost(8), f"{kind}, its own S lifted +8 dB", "Forward SAP, backward, repeat")
