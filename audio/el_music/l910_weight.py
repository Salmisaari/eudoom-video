"""L9-10E (eu2_low4 for both lines, mid-tuned) was "ok, but still some small drift", and flat where the original puts
the weight (CHI-nese, SHROOMS). Measured against the original vocal: word onsets within 20-40 ms (the drift is pitch,
not timing): "where the" sits ~4 semitones under "with" and "-es" ~8 over "of", both beyond the 300-cent reach of the
line tune; and the stressed words start soft (B-, Z-) where the original hits a ch / sh, weakened again by the
separation, a few dB under the original's contour. Variants of E: the two notes lifted into place (L16M's recipe),
and "weight": the take's loudness contour pulled toward the original's (+-3 dB, 100 ms) and its own sibilant
onsets lifted (L24K's recipe). Clips "L9-10<letter>" in eu_v8_lines."""
import sys, pathlib
import numpy as np, librosa, scipy.signal as ss
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from v8_refine import write, V, TUNE

WHERE_THE, ES = (27.95, 28.22), (28.88, 29.14)
SIBILANTS = [(26.9, 27.35), (29.1, 29.4)]  # "Brus-sels", "z-oom"


def mask(n, t0, spans, ramp=0.02):
    t = t0 + np.arange(n) / V.SR
    return np.clip(np.max([np.minimum((t - a) / ramp, (b - t) / ramp) for a, b in spans], axis=0), 0, 1)


def weight(x, vo, t0, db=3):
    """x's loudness contour pulled toward vo's (+-db, 100 ms), plus x's own sibilant frames +6 dB above 3.5 kHz."""
    env = lambda v: 20 * np.log10(np.convolve(librosa.to_mono(v) ** 2, np.ones(4410) / 4410, "same") ** 0.5 + 1e-7)
    ex, eo = env(x), env(vo)
    active = (eo > -40) & (ex > -40)
    g = np.where(active, eo - ex, 0.0)
    g = np.clip(g - np.median(g[active]), -db, db) * active
    g = np.convolve(g, np.ones(4410) / 4410, "same")
    x = x * 10 ** (g / 20)
    m = librosa.to_mono(x); hop = 441
    S = np.abs(librosa.stft(m, n_fft=1024, hop_length=hop)); fr = librosa.fft_frequencies(sr=V.SR, n_fft=1024)
    d = 20 * np.log10(S[fr > 4000].sum(0) + 1e-9) - 20 * np.log10(S[(fr > 100) & (fr < 1500)].sum(0) + 1e-9)
    tf = t0 + np.arange(len(d)) * hop / V.SR
    on = (d > 6) & np.any([(tf >= a) & (tf <= b) for a, b in SIBILANTS], axis=0)
    w = np.convolve(np.interp(np.arange(x.shape[1]), np.arange(len(d)) * hop, on.astype(float)), np.ones(441) / 441, "same")
    b_, a_ = ss.butter(2, 3500 / (V.SR / 2), "high")
    return x + ss.lfilter(b_, a_, x, axis=1) * (10 ** (6 / 20) - 1) * w


def proc(lift=(), heavy=False):
    def f(vt, vo):
        x = TUNE(vt, vo)  # E's line tune
        for (a, b), mc in lift:  # to the original's actual note (no octave fold: "-es" is 8 semitones over "of")
            m = mask(x.shape[1], f.a, [(a, b)])
            x = x * (1 - m) + TUNE(x, vo, max_cents=mc, fold=False) * m
        return (weight(x, vo, f.a) if heavy else x).astype(np.float32)
    return f


if __name__ == "__main__":
    text = "Trapped in the Brussels room, where the faxes zoom"
    only = sys.argv[1:]  # letters to rebuild in place, e.g. G J
    for letter, (lift, heavy, desc) in zip("FGHIJ", (([(WHERE_THE, 600)], False, "E with 'where the' lifted to the original"),
                              ([(WHERE_THE, 600), (ES, 1000)], False, "E with 'where the' and '-es' on the original notes"),
                              ([], True, "E with the original's weight (loudness contour, stronger B-/Z- onsets)"),
                              ([(WHERE_THE, 600)], True, "E, 'where the' lifted, with the weight"),
                              ([(WHERE_THE, 600), (ES, 1000)], True, "E, both notes on the original, with the weight"))):
        if not only or letter in only:
            write(l910.N, "eu2_low4", l910.PLAN, "htdemucs_ft", False, proc(lift, heavy), desc, text, label="L9-10", letter=letter)
