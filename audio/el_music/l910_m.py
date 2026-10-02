"""L9-10E "works if zooe -> zoom": its last word never closes on the m. Measured on the vocals (BS-RoFormer split):
the original's "shroo-m" darkens as the lips shut, 29.56-29.64 s: energy 1-4 kHz against 100-600 Hz falls from
-17..-22 dB to -24..-30 dB and the level 3-5 dB, then its s. E's "zoo" stays bright (-10..-14 dB) to 29.66 and then
opens into a breath (+5 dB at 29.70): "zoo-e". None of the 15 other eu2 takes has a clearer m to borrow.
m_close() gives E's own vowel the original's closure: above ~1 kHz it fades by up to 16 dB over 29.56-29.64 (a
lowpass closing like lips), the level drops 4 dB, and the release after 29.68 fades out (zoom has no s).
E is otherwise as heard (eu2_low4, htdemucs_ft, mid-channel tune)."""
import sys, pathlib
import numpy as np, librosa
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from v8_refine import write, V, TUNE

CLOSE = (29.56, 29.64)  # the original's lips closing
END = (29.68, 29.74)    # release faded out


def m_close(x, t0, db_hi=16, db_all=4):
    n_fft, hop = 1024, 256
    X = [librosa.stft(ch, n_fft=n_fft, hop_length=hop) for ch in x]
    t = t0 + np.arange(X[0].shape[1]) * hop / V.SR
    f = librosa.fft_frequencies(sr=V.SR, n_fft=n_fft)
    ramp = np.clip((t - CLOSE[0]) / (CLOSE[1] - CLOSE[0]), 0, 1)                   # 0 -> 1 over the closure
    hi = np.clip((f - 700) / 600, 0, 1)                                            # 0 below 700 Hz, 1 above 1.3 kHz
    fade = np.clip((END[1] - t) / (END[1] - END[0]), 0, 1)                          # 1 -> 0 over the release
    g_db = -(db_hi * hi[:, None] * ramp[None]) - db_all * ramp[None]
    G = 10 ** (g_db / 20) * fade[None]
    y = np.stack([librosa.istft(Xc * G, hop_length=hop, length=x.shape[1]) for Xc in X])
    # only touch the tail: before the closure the original signal, untouched
    s = np.clip((np.arange(x.shape[1]) / V.SR + t0 - (CLOSE[0] - 0.02)) / 0.02, 0, 1)
    return (x * (1 - s) + y * s).astype(np.float32)


def e_with_m(vt, vo):
    return m_close(TUNE(vt, vo), e_with_m.a)


def with_expression(loud=False):
    """R, but tuned to the original's pitch curve in detail (30 ms instead of 90 ms smoothing): its scoops and
    flicks come along (measured: "Trapped" 330 cents of glide in the original, 195 in R; "with" 330 vs 160), and with
    loud, its loudness contour too (l910_weight.weight, +-4 dB)."""
    from l910_weight import weight
    def f(vt, vo):
        x = TUNE(vt, vo, half=1)
        x = weight(x, vo, f.a, 4) if loud else x
        return m_close(x, f.a)
    return f


if __name__ == "__main__":
    text = "Trapped in the Brussels room, where the faxes zoom"
    only = sys.argv[1:]
    for letter, hook, desc in (("R", e_with_m, "E with its zoom closed on an m like the original's"),
                               ("S", with_expression(), "R following the original's pitch curve in detail (its scoops and flicks)"),
                               ("T", with_expression(True), "S with the original's loudness contour too")):
        if (not only and letter == "R") or letter in only:
            write(l910.N, "eu2_low4", l910.PLAN, "htdemucs_ft", False, hook, desc, text, label="L9-10", letter=letter)


def rof_u():
    """L9-10T on the BS-RoFormer split with centre/sides levelled (round 6; the user called those lines great):
    T was "a bit mushy and less clear" on the Demucs split, which leaves more of the original singer under the take
    (~2 dB more band residue measured on L16/L24) and smears consonants."""
    import rof_clips
    return rof_clips.ms(with_expression(True), l910.N)


if __name__ == "__main__" and "U" in sys.argv[1:]:
    import rof_clips  # sets V.VO to the RoFormer split of the original
    write(l910.N, "eu2_low4", l910.PLAN, "bsroformer", False, rof_u(), "T on the RoFormer split, centre/sides levelled",
          "Trapped in the Brussels room, where the faxes zoom", label="L9-10", letter="U")
