"""BS-RoFormer vocal separation (audio-separator, model_bs_roformer_ep_317_sdr_12.9755: vocal SDR ~13 dB on MUSDB18,
htdemucs_ft ~9). A better split matters twice in a vocal swap (out = mix - V_orig + V_take): what the model misses of
the original singer stays in the band as a ghost, and what it misses of the take (hiss of s/ch/sh, breaths, the
reverb tail) never arrives. Runs in the analysis venv (cd analysis && uv run python ...).
  separate(y, a, b)  stereo vocal of y (song timeline, 44.1 kHz) over [a, b] s
  original()         the original song's vocal, whole song, aligned to vsplice.mix (cached)"""
import pathlib, sys, tempfile
import numpy as np, soundfile as sf

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))
import common

MODEL = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
SR = 44100
_sep = None


def _run(y):
    """vocal stem of the stereo signal y"""
    global _sep
    if _sep is None:
        import beartype  # its checks fail on this Python for the RoFormer's type hints; they only check types
        beartype.beartype = lambda f=None, **k: f if f is not None else (lambda g: g)
        from audio_separator.separator import Separator
        _sep = Separator(model_file_dir=str(common.ROOT / ".cache/audio-separator"), output_dir=tempfile.gettempdir(),
                         normalization_threshold=1.0, log_level=40)
        _sep.load_model(model_filename=MODEL)
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/in.wav", y.T, SR)
        _sep.output_dir = d
        _sep.model_instance.output_dir = d
        _sep.separate(f"{d}/in.wav", custom_output_names={"Vocals": "voc", "Instrumental": "inst"})
        v = sf.read(f"{d}/voc.wav", dtype="float32", always_2d=True)[0].T
    return np.pad(v, ((0, 0), (0, max(0, y.shape[1] - v.shape[1]))))[:, : y.shape[1]]


def separate(y, a, b, pad=1.0):
    """vocal of y over [a, b] s; separated with pad s of context on each side (the model sees the phrase whole)"""
    i0, i1 = int(a * SR), int(b * SR)
    p = int(pad * SR)
    s0 = max(0, i0 - p)
    v = _run(y[:, s0:i1 + p])
    return v[:, i0 - s0:i0 - s0 + (i1 - i0)]


def original(mix):
    f = common.ROOT / "stems/bsroformer/pdoom_vocals.wav"
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        sf.write(f, _run(mix).T, SR)
    v = sf.read(f, dtype="float32", always_2d=True)[0].T
    return np.pad(v, ((0, 0), (0, max(0, mix.shape[1] - v.shape[1]))))[:, : mix.shape[1]]
