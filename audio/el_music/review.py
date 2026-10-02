"""Objective review of every swapped line against the original song, per version (v3, v4, v5, ...).

For each line window, both mixes are separated the same way (htdemucs) and compared:
  pitch   median |cents| of the vocal f0 vs the original (octave-safe) and % of frames within 50 c
  onset   median |ms| between each original vocal onset and the nearest new one (timing / groove)
  vocal   vocal level difference (dB) and brightness (spectral centroid ratio)
  ghost   how much of the ORIGINAL vocal's pitch track is still sounding under the new vocal where
          the two melodies differ (old words bleeding through: doubled, "broken background voice")
  band    mel difference of the accompaniment (mix minus vocal) vs the original's (the band should not change)
  seam    worst spectral-flux spike near the line edges relative to the original's (clicks, cuts)
usage: review.py v3=path.wav v4=path.mp3 ...   -> review_<version>.json + a table"""
import json, pathlib, sys
import numpy as np, librosa, soundfile as sf, torch

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import common  # noqa: F401
from demucs.pretrained import get_model
from demucs.apply import apply_model

SR, HOP = 44100, 512
LYR = json.loads((ROOT / "data/lyrics.json").read_text())["lines"]
LINES = [7, 9, 10, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 31, 34, 35, 37, 40, 41, 45]
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
M = get_model("htdemucs").eval()
VI = M.sources.index("vocals")


def load(p):
    y = librosa.load(p, sr=SR, mono=False)[0]
    return y


def sep(y, a, b):
    seg = torch.tensor(y[:, int(a * SR):int(b * SR)], dtype=torch.float32)
    with torch.no_grad():
        v = apply_model(M, seg[None], device=DEV, split=True, overlap=0.25, progress=False)[0, VI].cpu().numpy()
    return v, y[:, int(a * SR):int(a * SR) + v.shape[1]] - v


def f0(v):
    f, vo, _ = librosa.pyin(librosa.to_mono(v), fmin=100, fmax=1000, sr=SR, frame_length=4096, hop_length=HOP)
    return f, vo


def onsets(v):
    return librosa.onset.onset_detect(y=librosa.to_mono(v), sr=SR, hop_length=HOP, units="time", backtrack=False)


def melspec(x):
    return librosa.power_to_db(librosa.feature.melspectrogram(y=librosa.to_mono(x), sr=SR, n_fft=2048, hop_length=HOP, n_mels=64))


def flux(x):
    return librosa.onset.onset_strength(y=librosa.to_mono(x), sr=SR, hop_length=HOP)


def harmonic_energy(S, freqs, f0s, nh=6):
    """Per frame: summed magnitude at the first nh harmonics of f0 (nan -> 0)."""
    out = np.zeros(S.shape[1])
    for k in range(S.shape[1]):
        if not np.isfinite(f0s[k]):
            continue
        for h in range(1, nh + 1):
            i = np.argmin(np.abs(freqs - f0s[k] * h))
            out[k] += S[max(0, i - 1):i + 2, k].max()
    return out


_orig_cache = {}


def line_metrics(Y, O, n):
    a, b = LYR[n - 1]["start"], (LYR[n]["start"] if n < len(LYR) else LYR[n - 1]["end"])
    w0, w1 = a - 0.5, b + 0.5
    if n not in _orig_cache:
        _orig_cache[n] = sep(O, w0, w1)
    vo, ao = _orig_cache[n]
    vy, ay = sep(Y, w0, w1)
    k = min(vo.shape[1], vy.shape[1]); vo, ao, vy, ay = vo[:, :k], ao[:, :k], vy[:, :k], ay[:, :k]
    inner = slice(int(0.5 * SR), k - int(0.5 * SR))
    fo, voo = f0(vo[:, inner]); fy, voy = f0(vy[:, inner])
    m = min(len(fo), len(fy)); fo, fy, voo, voy = fo[:m], fy[:m], voo[:m], voy[:m]
    both = voo & voy
    c = 1200 * np.log2(fy[both] / fo[both]) if both.any() else np.array([0.0])
    c = np.abs((c + 600) % 1200 - 600)
    # onset timing: each original onset -> nearest new onset
    oo, oy = onsets(vo[:, inner]), onsets(vy[:, inner])
    dt = [np.min(np.abs(oy - t)) * 1000 for t in oo] if len(oy) and len(oo) else [999]
    rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    cen = lambda x: np.median(librosa.feature.spectral_centroid(y=librosa.to_mono(x), sr=SR, hop_length=HOP))
    # ghost: where the melodies differ by > 1 semitone, energy at the ORIGINAL f0's harmonics in the new vocal,
    # relative to the energy at the new vocal's own harmonics (1.0 = old voice as loud as the new one)
    S = np.abs(librosa.stft(librosa.to_mono(vy[:, inner]), n_fft=4096, hop_length=HOP))[:, :m]
    fr = librosa.fft_frequencies(sr=SR, n_fft=4096)
    diff = both & (np.abs(1200 * np.log2(np.where(both, fy, 1) / np.where(both, fo, 1))) > 100)
    ghost_frames = int(diff.sum())
    if diff.sum() >= 15:  # fewer differing frames than ~0.2 s is too little to judge
        ghost = float(np.median(harmonic_energy(S[:, diff], fr, fo[diff]) / (harmonic_energy(S[:, diff], fr, fy[diff]) + 1e-9)))
    else:
        ghost = 0.0
    band = float(np.mean(np.abs(melspec(ay[:, inner]) - melspec(ao[:, inner]))))
    fo_, fy_ = flux(O[:, int(w0 * SR):int(w1 * SR)]), flux(Y[:, int(w0 * SR):int(w1 * SR)])
    edges = [int((t - w0) * SR / HOP) for t in (a, b)]
    seam = max(float(fy_[max(0, e - 8):e + 8].max() / (fo_[max(0, e - 8):e + 8].max() + 1e-9)) for e in edges)
    return dict(pitch_med=round(float(np.median(c))), pitch_in50=round(float(np.mean(c < 50)) * 100),
                onset_ms=round(float(np.median(dt))), vocal_db=round(float(rms(vy[:, inner]) - rms(vo[:, inner])), 1),
                bright=round(float(cen(vy[:, inner]) / (cen(vo[:, inner]) + 1e-9)), 2), ghost=round(ghost, 2), ghost_frames=ghost_frames,
                band_db=round(band, 1), seam=round(seam, 2))


if __name__ == "__main__":
    O = load(ROOT / "audio/pdoom.mp3")
    for arg in sys.argv[1:]:
        name, path = arg.split("=")
        Y = load(path)
        n = min(O.shape[1], Y.shape[1]); Y = Y[:, :n]
        res = {}
        for ln in LINES:
            res[ln] = line_metrics(Y, O[:, :n], ln)
            print(name, f"L{ln:02d}", res[ln], flush=True)
        (HERE / f"review_{name}.json").write_text(json.dumps(res, indent=1))
