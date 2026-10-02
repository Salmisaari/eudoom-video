"""Does a sung line fit the NEW lyric better than the OLD one? CTC loss of both transcripts under the
wav2vec2 LV60K acoustic model (the one analysis/ uses for alignment) on the separated vocal.
margin = loss(old) - loss(new), in nats: > 0 means the new words are what is being sung."""
import numpy as np, torch, torchaudio, librosa

_B = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_LV60K_960H
_DEV = "mps" if torch.backends.mps.is_available() else "cpu"
_model = None
_IDX = {c: i for i, c in enumerate(_B.get_labels())}  # '-' blank = 0, '|' word separator


def _tokens(text):
    s = "|".join("".join(c for c in w.upper() if c in _IDX and c not in "-|") for w in text.split())
    return torch.tensor([_IDX[c] for c in s if c in _IDX], dtype=torch.long)


def emissions(vocal, sr):
    global _model
    if _model is None:
        _model = _B.get_model().to(_DEV).eval()
    y = librosa.resample(vocal, orig_sr=sr, target_sr=16000)
    y = y / (np.abs(y).max() + 1e-9)
    with torch.inference_mode():
        em, _ = _model(torch.from_numpy(y).float()[None].to(_DEV))
    return torch.log_softmax(em, -1)[0].float().cpu()


def loss(em, text):
    t = _tokens(text)
    return float(torch.nn.functional.ctc_loss(em[:, None], t[None], torch.tensor([em.shape[0]]),
                                              torch.tensor([len(t)]), blank=0, reduction="sum", zero_infinity=True))


def margin(em, old, new):
    return loss(em, old) - loss(em, new)
