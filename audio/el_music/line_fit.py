"""Takes fitted onto the original's rhythm for any line with a grid in sylfit.GRID, spliced into v9.
usage: line_fit.py <line> <take> <text> <number> [<take> <text> <number> ...]  -> L<line>v<number> - <text> (fitted)"""
import sys, pathlib
import librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rof_clips
from rof_clips import ms
import v8_refine
from v8_refine import write, V
import sylfit

OLD = {25: "NOW VON NEUMANN'S OBSOLETE", 11: "SEE THROUGH THE SHOGGOTHS LIES", 12: "WITH YOUR SHINIGAMI EYES"}
v8_refine._v7 = librosa.load(HERE / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
if __name__ == "__main__":
    n, args = int(sys.argv[1]), sys.argv[2:]
    v8_refine.OUT = pathlib.Path.home() / f"Desktop/suno_test/eu_v10_L{n} - all versions"
    for take, text, num in zip(args[0::3], args[1::3], args[2::3]):
        rep = []
        plan = (V.ALL_WORDS(n), OLD[n], text.upper().replace("'", ""), text)
        try:
            write(n, take, plan, "bsroformer", False, ms(sylfit.fit(text, n, report=rep), n),
                  f"{take} fitted onto the original's syllable onsets, tuned", f"{text} (fitted)", letter=num, label=f"L{n}v")
        except Exception as e:
            print("  failed", take, e, flush=True)
        print("  ", take, rep, flush=True)
