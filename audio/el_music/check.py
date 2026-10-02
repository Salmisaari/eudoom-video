"""For each inpainted take: where does it differ from the original, and what does Whisper hear there?"""
import sys, pathlib, tempfile
import numpy as np, librosa, soundfile as sf, scipy.signal as ss
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "analysis"))
import common  # noqa: F401
import mlx_whisper

SR = 44100
orig, _ = librosa.load("audio/pdoom.mp3", sr=SR, mono=True)


def heard(y):
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        sf.write(t.name, librosa.resample(y, orig_sr=SR, target_sr=16000), 16000)
        return mlx_whisper.transcribe(t.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


for p in sys.argv[1:]:
    y, _ = librosa.load(p, sr=SR, mono=True)
    # global offset vs original (first 20 s)
    seg = orig[int(10 * SR):int(20 * SR)]
    lag = int(np.argmax(ss.correlate(y[int(10 * SR) - 4410:int(20 * SR) + 4410], seg, "valid"))) - 4410
    y = np.roll(y, -lag)[: len(orig)] if lag >= 0 else np.pad(y, (-lag, 0))[: len(orig)]
    y = np.pad(y, (0, max(0, len(orig) - len(y))))
    fr = int(0.05 * SR)
    d = [20 * np.log10(np.std(y[i:i + fr] - orig[i:i + fr]) / (np.std(orig[i:i + fr]) + 1e-9) + 1e-9)
         for i in range(0, len(orig) - fr, fr)]
    changed = [i * 0.05 for i, v in enumerate(d) if v > -20]
    span = f"{changed[0]:.2f}-{changed[-1]:.2f} s ({len(changed) * 0.05:.1f} s differ)" if changed else "none"
    print(f"{pathlib.Path(p).name}: len {len(y) / SR:.2f}s offset {lag / SR * 1000:+.1f} ms, changed {span}")
    print("   heard:", heard(y[int(58.4 * SR):int(66.2 * SR)]))
