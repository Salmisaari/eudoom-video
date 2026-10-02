"""The v7 take of each processed line with some or all of the processing taken off, so a line the user likes in v7 can
keep its performance while the broken bit goes. v7 had L10 eu2_low3 warp+tune, L16 eu9_7 warp+tune ("AC temperatures"
inserted, as v6), L24 eu10_1 warp ("SAP" inserted, as v6), L40 eu13_7 nowarp+tune (htdemucs_ft). Each clip is the line
alone spliced into v7, cut 0.8 s before to 0.5 s after, written as the next free letter in
Desktop/suno_test/eu_v8_lines (L16E ...); the key goes into v8_options.json. Demucs runs on the CPU so a video render
on the GPU isn't stalled."""
import json, pathlib, subprocess, sys
import librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, swap, L10, V
from final10 import bounds
from select10 import PLANS

V.DEV = "cpu"
OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v8_lines"
# line: [(take, plan, sep, warp, tune)]
VARIANTS = {10: [("eu2_low3", L10[1], "htdemucs", True, False), ("eu2_low3", L10[1], "htdemucs", False, True)],
            16: [("eu9_7", PLANS[16][0][1], "htdemucs", True, False), ("eu9_7", PLANS[16][0][1], "htdemucs", False, False),
                 ("eu9_7", PLANS[16][0][1], "htdemucs", False, True)],
            24: [("eu10_1", PLANS[24][0][1], "htdemucs", False, False)],
            40: [("eu13_7", PLANS[40][0][1], "htdemucs_ft", False, False), ("eu13_7", PLANS[40][0][1], "htdemucs", False, False)]}


def kind(warp, tune):
    return ("warp" if warp else "nowarp") + ("+tune" if tune else "")


if __name__ == "__main__":
    v7 = librosa.load(HERE / "pdoom_EU_v7.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    keys_f = HERE / "v8_options.json"
    keys = json.loads(keys_f.read_text())
    for n, vs in VARIANTS.items():
        a, b = bounds(n)
        for take, plan, sep, warp, tune in vs:
            letter = chr(65 + sum(1 for k in keys if k.startswith(f"L{n}") and k[len(f"L{n}"):].isalpha() and len(k) == len(f"L{n}") + 1))
            out = paste(v7, swap(take, plan, n, sep=sep, warp_on=warp, tune=tune), a, b)[0]
            name = f"L{n}{letter}"
            sf.write(OUT / f"{name}.wav", out[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)].T, V.SR)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT / f"{name}.wav", "-af",
                            "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k", OUT / f"{name}.mp3"], check=True)
            (OUT / f"{name}.wav").unlink()
            keys[name] = f"{take} {kind(warp, tune)} ({sep}), the v7 take"
            keys_f.write_text(json.dumps(keys, indent=1))
            print(name, keys[name], flush=True)
