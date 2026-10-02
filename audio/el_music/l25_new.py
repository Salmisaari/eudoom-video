"""The user's new L25 lines (2026-10-01): "Now vegan steak's obsolete" (eu26_*, preferred) and "Now plastic straws
obsolete" (eu25_*), each take's whole line spliced into v9 (the song in the video) like L25I/J/K: RoFormer split,
centre/sides levelled. Clips L25v14.. in "eu_v10_L25 - all versions" (L25v1 = current, L25v2-13 = the earlier takes).
usage: l25_new.py [first_number]"""
import sys, pathlib
import librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rof_clips  # RoFormer split of the original as V.VO
from rof_clips import ms
import v8_refine
from v8_refine import write, V

v8_refine._v7 = librosa.load(HERE / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]  # splice into v9
v8_refine.OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v10_L25 - all versions"
LINES = [("eu26", "NOW VEGAN STEAKS OBSOLETE", "Now vegan steak's obsolete"),
         ("eu25", "NOW PLASTIC STRAWS OBSOLETE", "Now plastic straws obsolete")]
if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    for pre, upper, text in LINES:
        plan = (V.ALL_WORDS(25), "NOW VON NEUMANN'S OBSOLETE", upper, text)
        for k in range(1, 10):
            write(25, f"{pre}_{k}", plan, "bsroformer", False, ms(None, 25), f"{pre}_{k} whole line, RoFormer split, levelled",
                  text, letter=str(n), label="L25v")
            n += 1
