"""Variants of the options the user picked from eu_v8_lines, aimed at what they heard:
  L10C  "close but a bit rough" (eu2_low3, tune only): C was tuned L and R apart (rough, phasey); tuned on the mid
        channel, with the cleaner separation, and a gentler tune (only notes within 150 cents are moved)
  L16F  "minimal corruption between A and C" (eu9_7 "AC temperatures" inserted untouched): the take's "s" of "A-C" is
        ~5 dB weaker than the original's there (the separation smears it). htdemucs_ft, the insert starting at "my",
        and the take's whole line
  L16K  "great, but the -ing of rearranging should be higher": the original singer's "rearranging", or "-ranging"
        tuned up (4-5 semitones) to the original melody
  L25D  "parts slightly higher, pronunciation closer to the original" (eu14_16 whole line): its "Now" sits ~2
        semitones under the original. The original singer's "Now" + the take's "private chats get obsolete", and D with
        only "Now" tuned up to the original
Each clip is the line alone spliced into v7 (0.8 s before, 0.5 s after), named Lnn<letter> - <lyric>.mp3 in
Desktop/suno_test/eu_v8_lines; the key goes into v8_options.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, swap, L10, V
from final10 import bounds
from select10 import PLANS

OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v8_lines"
PSOLA = V.tune_to


def TUNE(vt, vo, max_cents=300, fold=True, half=4):
    """V.tune_to on the mid channel only, the side (the take's stereo spread) kept as it was: tuning L and R apart
    finds different pitch marks in each and halves their correlation (0.33 -> 0.16 on L10), heard as rough/phasey."""
    mid, side = vt.mean(0), (vt[0] - vt[1]) / 2
    m = PSOLA(mid[None], vo, max_cents=max_cents, fold=fold, half=half)[0]
    return np.stack([m + side, m - side]).astype(np.float32)


def gentle(vt, vo):
    return TUNE(vt, vo, max_cents=150)


def region(t0, t1, max_cents=300):
    """tune only inside [t0, t1] s of the song (20 ms ramps); vt starts at the line start - 0.8 s"""
    def f(vt, vo, a=None):
        tuned = TUNE(vt, vo, max_cents=max_cents)
        s = np.arange(vt.shape[1]) / V.SR + f.a
        m = np.clip(np.minimum((s - t0) / 0.02, (t1 - s) / 0.02), 0, 1)
        return (vt * (1 - m) + tuned * m).astype(np.float32)
    return f


P16 = PLANS[16][0][1]
P16_MY = ([2, 3], "MY ATOMS", "MY AY SEE TEMPERATURES", "my AC temperatures")
P16_ALL = (V.ALL_WORDS(16), "I FEEL MY ATOMS REARRANGING", "I FEEL MY AY SEE TEMPERATURES REARRANGING", "I feel my AC temperatures rearranging")
P16_KEEP_REARRANGING = ([0, 1, 2, 3], "I FEEL MY ATOMS", "I FEEL MY AY SEE TEMPERATURES", "I feel my AC temperatures")
P25_ALL = (V.ALL_WORDS(25), "NOW VON NEUMANN'S OBSOLETE", "NOW PRIVATE CHATS GET OBSOLETE", "Now private chats get obsolete")
P25_KEEP_NOW = ([1, 2, 3], "VON NEUMANN'S OBSOLETE", "PRIVATE CHATS GET OBSOLETE", "private chats get obsolete")
TEXT = {10: "where the faxes zoom", 16: "I feel my AC temperatures rearranging", 25: "Now private chats get obsolete"}
# line: [(take, plan, sep, warp, tune function or None, description)]
VARIANTS = {10: [("eu2_low3", L10[1], "htdemucs", False, TUNE, "L10C tuned on the mid channel (C tuned L and R apart)"),
                 ("eu2_low3", L10[1], "htdemucs_ft", False, TUNE, "L10C mid-tuned, cleaner separation"),
                 ("eu2_low3", L10[1], "htdemucs_ft", False, gentle, "L10C mid-tuned gently, cleaner separation")],
            16: [("eu9_7", P16, "htdemucs_ft", False, None, "L16F with the cleaner separation"),
                 ("eu9_7", P16_MY, "htdemucs", False, None, "L16F, insert from 'my'"),
                 ("eu9_7", P16_MY, "htdemucs_ft", False, None, "L16F, insert from 'my', cleaner separation"),
                 ("eu9_7", P16_ALL, "htdemucs_ft", False, None, "L16F's take, whole line"),
                 # L16K "great, but the -ing of rearranging should be higher": K is on the original melody up to
                 # 52.05 s, then "-ranging" sits 4-5 semitones under it (take ~310 Hz, original 390-466 Hz)
                 ("eu9_7", P16_KEEP_REARRANGING, "htdemucs_ft", False, None, "L16K with the original singer's 'rearranging'"),
                 ("eu9_7", P16_ALL, "htdemucs_ft", False, region(52.05, 52.85, 600), "L16K, '-ranging' lifted to the original")],
            25: [("eu14_16", P25_KEEP_NOW, "htdemucs", False, None, "L25D with the original singer's 'Now'"),
                 ("eu14_16", P25_KEEP_NOW, "htdemucs_ft", False, None, "L25D with the original 'Now', cleaner separation"),
                 ("eu14_16", P25_ALL, "htdemucs", False, region(77.6, 78.2), "L25D, only 'Now' tuned up to the original"),
                 ("eu14_16", P25_ALL, "htdemucs_ft", False, region(77.6, 78.2), "L25D, only 'Now' tuned, cleaner separation")]}


_v7 = None


def write(n, take, plan, sep, warp, tune, desc, text, letter=None, label=None):
    """The take's line spliced alone into v7 -> the next free letter for line n (or letter); returns that name.
    label names the clip when n is a joined span (e.g. "L9-10")."""
    label = label or f"L{n}"
    global _v7
    if _v7 is None:
        _v7 = librosa.load(HERE / "pdoom_EU_v7.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    keys_f = HERE / "v8_options.json"
    keys = json.loads(keys_f.read_text())
    a, b = bounds(n)
    letter = letter or chr(65 + sum(1 for k in keys if k[:len(label)] == label and len(k) == len(label) + 1))
    if tune is not None:
        tune.a = V.LYR[n - 1]["start"] - 0.8  # where build()'s vocal segment starts
        V.tune_to = tune
    out = paste(_v7, swap(take, plan, n, sep=sep, warp_on=warp, tune=tune is not None), a, b)[0]
    V.tune_to = PSOLA
    name = f"{label}{letter} - {text}"
    sf.write(OUT / f"{name}.wav", out[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)].T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT / f"{name}.wav", "-af",
                    "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k", OUT / f"{name}.mp3"], check=True)
    (OUT / f"{name}.wav").unlink()
    keys[f"{label}{letter}"] = f"{take} ({sep}): {desc}"
    keys_f.write_text(json.dumps(keys, indent=1))
    print(f"{label}{letter}", keys[f"{label}{letter}"], flush=True)
    return f"{label}{letter}"


if __name__ == "__main__":
    only = sys.argv[1:]  # e.g. L10D L25G: rebuild those letters in place
    for n, vs in VARIANTS.items():
        first = {10: "D", 16: "H", 25: "E"}[n]
        for i, v in enumerate(vs):
            letter = chr(ord(first) + i)
            if not only or f"L{n}{letter}" in only:
                write(n, *v, TEXT[n], letter=letter)
