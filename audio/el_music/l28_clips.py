"""L28 "NATO, please don't let me go": only "NATO" from a take (the takes sing the rest of the line off the original's
melody: 5-21 % within 50 cents, l28_scan.py), "please don't let me go" stays the original singer's. The three takes
the phonetic model hears most as N rather than G: eu2_low5, eu2_low4, eu2_low8. RoFormer split, levelled (round 6).
Clips L28A-C in eu_v8_lines, with "L28 original" and "L28 now" (v9) cut the same way."""
import sys, pathlib, subprocess
import soundfile as sf, librosa
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rof_clips
from rof_clips import ms
from v8_refine import write, V, OUT
from final10 import bounds

P28_INS = ([0], "GATO", "NATO", "NATO,")
TEXT = "NATO, please don't let me go"
WORD = (89.28, 90.64)  # "Gato," in the original


def word_level(hook, span=WORD, limit=12):
    """hook, then the take's centre over span set to the original's (L28A's NATO sat 7 dB under the original's Gato;
    the build's own gain stops at +6 dB). 20 ms ramps."""
    import numpy as np
    def f(vt, vo):
        hook.a = f.a
        x = hook(vt, vo)
        s = slice(int((span[0] - f.a) * V.SR), int((span[1] - f.a) * V.SR))
        db = lambda y: 10 * np.log10(np.mean(y.mean(0)[s] ** 2) + 1e-12)
        g = float(np.clip(db(vo) - db(x), -limit, limit))
        t = f.a + np.arange(x.shape[1]) / V.SR
        m = np.clip(np.minimum((t - span[0]) / 0.02, (span[1] - t) / 0.02), 0, 1)
        print(f"  NATO {g:+.1f} dB", flush=True)
        return (x * 10 ** (g * m / 20)).astype(np.float32)
    return f
if __name__ == "__main__":
    a, b = bounds(28)
    for name, y in (("L28 original - Gato, please don't let me go", V.mix),
                    (f"L28 now - {TEXT}", librosa.load(pathlib.Path(__file__).parent / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0])):
        sf.write(OUT / f"{name}.wav", y[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)].T, V.SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT / f"{name}.wav", "-af",
                        "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k", OUT / f"{name}.mp3"], check=True)
        (OUT / f"{name}.wav").unlink()
    if sys.argv[1:] == ["E"]:
        # the take's N-A 0.15 s earlier (its vowel came 0.22 s after the original's), at the original's level, and
        # the original singer from the t of "-to" on: the insert ends in the t closure (89.94-90.04)
        import numpy as np
        inner = word_level(ms(None, 28), span=(89.3, 89.92))
        def early(vt, vo):
            inner.a = early.a
            k = int(0.15 * V.SR)
            return inner(np.pad(vt[:, k:], ((0, 0), (0, k))), vo)
        w0 = V.LYR[27]["words"][0]; end = w0["end"]; w0["end"] = 89.96
        try:
            write(28, "eu2_low5", P28_INS, "bsroformer", False, early,
                  "the take's 'Na' 0.15 s earlier at the original's level, the original's '-to, please don't let me go'",
                  TEXT, letter="E")
        finally:
            w0["end"] = end
        sys.exit()
    if sys.argv[1:] == ["D"]:
        write(28, "eu2_low5", P28_INS, "bsroformer", False, word_level(ms(None, 28)),
              "L28A with NATO at the original word's level", TEXT, letter="D")
        sys.exit()
    for letter, take in zip("ABC", ("eu2_low5", "eu2_low4", "eu2_low8")):
        write(28, take, P28_INS, "bsroformer", False, ms(None, 28), "'NATO' only, the original's 'please don't let me go'",
              TEXT, letter=letter)
