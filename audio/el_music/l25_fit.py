"""L25 takes fitted onto the original's rhythm (sylfit.py: each syllable's vowel moved onto the original's note onset,
PSOLA, then the notes tuned). Clips L25v40.. in "eu_v10_L25 - all versions". usage: l25_fit.py <take> <text> <number>..."""
import sys, pathlib
import librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rof_clips
from rof_clips import ms
import v8_refine
from v8_refine import write, V
import sylfit

v8_refine._v7 = librosa.load(HERE / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
v8_refine.OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v10_L25 - all versions"
if __name__ == "__main__":
    args = sys.argv[1:]
    for take, text, num in zip(args[0::3], args[1::3], args[2::3]):
        rep = []
        plan = (V.ALL_WORDS(25), "NOW VON NEUMANN'S OBSOLETE", text.upper().replace("'", ""), text)
        write(25, take, plan, "bsroformer", False, ms(sylfit.fit(text, 25, report=rep), 25),
              f"{take} fitted onto the original's syllable onsets, tuned", f"{text} (fitted)", letter=num, label="L25v")
        print("  ", take, rep, flush=True)
