"""L20 "Nokia to the moon" clips for the user's ear. Whisper's gate only accepted the spelling "nokia", but a sung
No-ki-a is mostly heard as "No key", so these near-hits were never listened to. Each take is spliced untouched
(local alignment only, no warp, no tune) into v7 and cut from L18 to L21.
usage: l20_audition.py [take:ins|whl ...]   default: the near-hits of rounds 14-17
writes ~/Desktop/suno_test/eu_v8_L20/L20_<take>_<ins|whl>.mp3 (+ 00_original, 00_v7_ASML)"""
import pathlib, subprocess, sys
import librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V
from final10 import bounds

NEAR = ["eu14_6:ins", "eu14_6:whl", "eu14_18:ins", "eu14_18:whl", "eu14_13:ins", "eu14_3:whl", "eu15_9:ins",
        "eu14_19:whl", "eu14_11:whl"]
PLAN = {"ins": ([0], "EN VEE DEE AY", "NOKIA", "Nokia"),
        "whl": (V.ALL_WORDS(20), "EN VEE DEE AY TO THE MOON", "NOKIA TO THE MOON", "Nokia to the moon")}
OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v8_L20"
T0, T1 = 58.9, 66.4  # L18 "I'm upping my EU doom" to the end of L21


def write(y, name):
    with open(OUT / f"{name}.wav", "wb") as f:
        sf.write(f, y[:, int(T0 * V.SR):int(T1 * V.SR)].T, V.SR, format="WAV")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT / f"{name}.wav", "-b:a", "256k", OUT / f"{name}.mp3"], check=True)
    (OUT / f"{name}.wav").unlink()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    v7 = librosa.load(HERE / "pdoom_EU_v7.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    write(V.mix, "00_original")
    write(v7, "00_v7_ASML")
    for arg in sys.argv[1:] or NEAR:
        take, mode = arg.split(":")
        V.PLAN[20] = PLAN[mode]
        Y = V.apply(V.mix, V.VO, V.build(V.load_take(take), 20, warp_on=False))[0]
        write(paste(v7, Y, *bounds(20))[0], f"L20_{take}_{mode}")
        print(f"L20_{take}_{mode}", flush=True)
