"""The user's L11 "See through Pinocchio's lies" and L12 "with your Eurovision eyes" (eu27_*, one chunk over both
lines), each line spliced alone into v9 like l25_new.py. Clips L11v1.. / L12v1.. in "eu_v10_L11 …" / "eu_v10_L12 …"."""
import sys, pathlib, subprocess
import librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rof_clips  # RoFormer split of the original as V.VO
from rof_clips import ms
import v8_refine
from v8_refine import write, V

v8_refine._v7 = librosa.load(HERE / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
DESK = pathlib.Path.home() / "Desktop/suno_test"
L11 = ["See through Pinocchio's lies", "See through Pinocchio's lies", "See through the Pinocchio's lies"]
L12 = ["with your Eurovision eyes", "with your Eurovision eyes", "with Eurovision eyes"]
ORIG = {11: "See through the shoggoth's lies", 12: "with your shinigami eyes"}
if __name__ == "__main__":
    for n, texts, old in ((11, L11, "SEE THROUGH THE SHOGGOTHS LIES"), (12, L12, "WITH YOUR SHINIGAMI EYES")):
        out = DESK / f"eu_v10_L{n} - all versions"; out.mkdir(exist_ok=True)
        v8_refine.OUT = out
        a, b = v8_refine.bounds(n)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a - 0.8), "-to", str(b + 0.5), "-i", str(HERE.parents[0] / "pdoom.mp3"),
                        "-af", "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k",
                        str(out / f"L{n} original (current, in the video) - {ORIG[n]}.mp3")], check=True)
        for k in range(1, 10):
            text = texts[(k - 1) % 3]
            plan = (V.ALL_WORDS(n), old, text.upper().replace("'", ""), text)
            write(n, f"eu27_{k}", plan, "bsroformer", False, ms(None, n), f"eu27_{k} line {n}, RoFormer split, levelled",
                  text, letter=str(k), label=f"L{n}v")
