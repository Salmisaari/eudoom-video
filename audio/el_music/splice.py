"""Splice [t_in, t_out] of an ElevenLabs inpainted take into the original song, everything else untouched.

usage: splice.py <take> <t_in> <t_out>     (seconds on the original timeline)
Writes audio/el_music/<take>_spliced.wav, full mp3 + a 58.4-66.2 s preview clip to the Desktop,
and prints what Whisper hears in 60.5-64.2 s.
"""
import pathlib, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf, scipy.signal as ss

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))
import common  # noqa: F401
import mlx_whisper

SR = 44100
XF = int(0.03 * SR)
DESK = pathlib.Path.home() / "Desktop/suno_test/elevenlabs_music"
take, t_in, t_out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])

orig, _ = librosa.load(ROOT / "audio/pdoom.mp3", sr=SR, mono=False)
new, _ = librosa.load(ROOT / f"audio/el_music/{take}.mp3", sr=SR, mono=False)

# sample-accurate offset and gain, measured outside the edit (40-58 s)
a, b = int(40 * SR), int(58 * SR)
m = 4410
lag = int(np.argmax(ss.correlate(new.mean(0)[a - m:b + m], orig.mean(0)[a:b], "valid"))) - m
new = np.roll(new, -lag, axis=1)
gain = orig[:, a:b].std() / new[:, a:b].std()
new = new[:, : orig.shape[1]] * gain
new = np.pad(new, ((0, 0), (0, orig.shape[1] - new.shape[1])))

w = np.zeros(orig.shape[1])  # 0 = original, 1 = take (equal-power crossfades)
i0, i1 = int(t_in * SR), int(t_out * SR)
w[i0:i1] = 1
h = XF // 2
w[i0 - h:i0 - h + XF] = np.linspace(0, 1, XF)
w[i1 - h:i1 - h + XF] = np.linspace(1, 0, XF)
out = orig * np.cos(w * np.pi / 2) + new * np.sin(w * np.pi / 2)

tag = f"{take}_{t_in:.2f}-{t_out:.2f}"
wav = ROOT / f"audio/el_music/{tag}_spliced.wav"
sf.write(wav, out.T, SR)
DESK.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "320k", DESK / f"pdoom_ASML_{tag}.mp3"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "58.4", "-to", "66.2", "-i", wav, "-b:a", "256k",
                DESK / f"preview_{tag}.mp3"], check=True)

with tempfile.NamedTemporaryFile(suffix=".wav") as f:
    sf.write(f.name, librosa.resample(out.mean(0)[int(60.5 * SR):int(64.2 * SR)], orig_sr=SR, target_sr=16000), 16000)
    txt = mlx_whisper.transcribe(f.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                 temperature=0.0, condition_on_previous_text=False)["text"].strip()
d = np.abs(out - orig).max(0)
nz = np.flatnonzero(d > 1e-5)
print(f"{tag}: lag {lag / SR * 1000:+.1f} ms, gain {20 * np.log10(gain):+.2f} dB, "
      f"changed {nz[0] / SR:.2f}-{nz[-1] / SR:.2f} s | heard: {txt}")
