"""Assemble v8 on v7 (whose seams are flat). Only the lines the user heard as broken in animatic_v7, plus the new
wordings, change, and every new line is an untouched take: local alignment only, no time-warp, no pitch-tune, vocal
only over the original band. The user heard exactly the tuned or warped lines as broken (L10, L16, L24, L40).
  L10  eu2_low3, the v3 take the user liked, untouched instead of v7's warp+tune
  L16  eu14_10 whole "I feel my AC temperatures rearranging"
  L20  eu18_38 "Nokia" inserted (round 21): Whisper hears "No key out to the moon", the "a" running into "to" like
       eu18_12; 89 % on the melody, no ghost, "to the moon" stays the original singer's
  L24  eu14_10 whole "Forward SAP, backward, repeat", 90 % on the melody
  L25  eu14_16 "private chats get" inserted, "Now ... obsolete" stays the original singer's
  L40  eu20_1 whole "EU Inc fixes things soon", "soon" held like "askew"
Each candidate in CANDS is also written as a clip spliced alone into v7 (Desktop/suno_test/eu_v8/Lnn_<take>_<ins|whl>),
next to the v7 and original lines, so the user can swap any pick by take.
usage: final12.py [--clips]   writes pdoom_EU_v8.wav, audio/pdoom_eu.mp3, the Desktop copy and v8_sources.json"""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, best_sep, V, R, cost, ROOT
from final10 import bounds

ALL = V.ALL_WORDS
P = {10: (ALL(10), "WITH A BAG OF SHROOMS", "WHERE THE FAXES ZOOM", "where the faxes zoom"),
     16: (ALL(16), "I FEEL MY ATOMS REARRANGING", "I FEEL MY AY SEE TEMPERATURES REARRANGING", "I feel my AC temperatures rearranging"),
     "16a": (ALL(16), "I FEEL MY ATOMS REARRANGING", "I FEEL AY SEE TEMPERATURES REARRANGING", "I feel AC temperatures rearranging"),
     20: (ALL(20), "EN VEE DEE AY TO THE MOON", "NOKIA TO THE MOON", "Nokia to the moon"),
     "20i": ([0], "EN VEE DEE AY", "NOKIA", "Nokia"),
     24: (ALL(24), "FORWARD EM EL PEE BACKWARD REPEAT", "FORWARD ESS AY PEE BACKWARD REPEAT", "Forward SAP, backward, repeat"),
     25: (ALL(25), "NOW VON NEUMANN'S OBSOLETE", "NOW PRIVATE CHATS GET OBSOLETE", "Now private chats get obsolete"),
     "25i": ([1, 2], "VON NEUMANN'S", "PRIVATE CHATS GET", "private chats get"),
     40: (ALL(40), "AR EL AITCH EF GOES ASKEW", "EE YOU INC FIXES THINGS SOON", "EU Inc fixes things soon")}
PICKS = {10: ("eu2_low3", 10), 16: ("eu14_10", 16), 20: ("eu18_38", "20i"), 24: ("eu14_10", 24), 25: ("eu14_16", "25i"),
         40: ("eu20_1", 40)}
CANDS = {10: [("eu2_low3", 10)],
         16: [("eu14_10", 16), ("eu14_20", 16), ("eu14_18", 16), ("eu14_15", "16a")],
         20: [("eu18_38", "20i"), ("eu18_3", 20), ("eu18_12", 20), ("eu18_3", "20i"), ("eu18_12", "20i"), ("eu14_6", "20i"), ("eu14_18", "20i"),
              ("eu14_13", "20i"), ("eu15_9", "20i"), ("eu18_22", "20i")],
         24: [("eu14_10", 24), ("eu14_16", 24), ("eu14_1", 24)],
         25: [("eu14_16", "25i"), ("eu14_16", 25), ("eu14_19", "25i"), ("eu14_4", "25i")],
         40: [("eu20_1", 40), ("eu20_11", 40), ("eu20_3", 40), ("eu14_15", 40)]}
OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v8"


def line(take, key):
    """The take's line spliced untouched into the original, the cleaner of the two separations."""
    n = int(str(key).rstrip("ai"))
    V.PLAN[n] = P[key]
    return best_sep(take, P[key], n, "nowarp")


def clip(y, n, name):
    a, b = bounds(n)
    t0, t1 = max(0, a - 2.5), b + 1.0
    OUT.mkdir(parents=True, exist_ok=True)
    sf.write(OUT / f"{name}.wav", y[:, int(t0 * V.SR):int(t1 * V.SR)].T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT / f"{name}.wav", "-b:a", "256k", OUT / f"{name}.mp3"], check=True)
    (OUT / f"{name}.wav").unlink()


def seam_db(out, ref, t):
    s = slice(int((t - 0.02) * V.SR), int((t + 0.02) * V.SR))
    return 20 * np.log10(np.sqrt(np.mean(out[:, s] ** 2)) / (np.sqrt(np.mean(ref[:, s] ** 2)) + 1e-12))


if __name__ == "__main__":
    v7 = librosa.load(HERE / "pdoom_EU_v7.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    srcs = json.loads((HERE / "v7_sources.json").read_text())
    if "--clips" in sys.argv:
        for n, cands in CANDS.items():
            clip(V.mix, n, f"L{n}_00_original")
            clip(v7, n, f"L{n}_00_v7")
            for take, key in cands:
                Y, src = line(take, key)
                m = R.line_metrics(Y, V.mix, n)
                name = f"L{n}_{take}_{'ins' if str(key).endswith('i') else 'whl'}"
                clip(paste(v7, Y, *bounds(n))[0], n, name)
                print(f"{name:22s} {src:36s} in50 {m['pitch_in50']:3d} ghost {m['ghost']:.2f} band {m['band_db']} cost {cost(m):.1f}", flush=True)
    out, sources = v7.copy(), {k: v for k, v in srcs.items()}
    for n, (take, key) in PICKS.items():
        Y, src = line(take, key)
        out, span = paste(out, Y, *bounds(n))
        words = [w["w"] for w in V.LYR[n - 1]["words"]]
        p = P[key]
        sources[f"L{n}"] = dict(source=f"{src}, untouched", span=span, text=" ".join(words[: p[0][0]] + [p[3]] + words[p[0][-1] + 1:]))
        m = R.line_metrics(out, V.mix, n)
        print(f"L{n:02d} {src}: {sources[f'L{n}']['text']} | in50 {m['pitch_in50']} ghost {m['ghost']:.2f} band {m['band_db']} "
              f"seams {seam_db(out, v7, span[0]):+.1f} {seam_db(out, v7, span[1]):+.1f} dB", flush=True)
    sf.write(HERE / "pdoom_EU_v8.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v8.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v8.wav", "-b:a", "320k", OUT / "pdoom_EU_edition_v8.mp3"], check=True)
    (HERE / "v8_sources.json").write_text(json.dumps(dict(sorted(sources.items(), key=lambda kv: int(kv[0][1:]))), indent=1))
    mask = np.ones(out.shape[1], bool)
    for n in PICKS:
        s = sources[f"L{n}"]["span"]
        mask[int((s[0] - 0.03) * V.SR):int((s[1] + 0.03) * V.SR)] = False
    print(f"outside the changed lines vs v7: max |diff| {np.abs(out - v7)[:, mask].max():.1e}")
