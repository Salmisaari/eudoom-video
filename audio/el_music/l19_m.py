"""L19 "I hear the basic income gloom" (v13, eu9_9), the user: OLD is best, but "gloom" sounds like "glue": it doesn't
close on its m, the same as L10's "zoom" (l910_m.py). Measured on the vocals: the v13 "gloo-" stays bright on 63
(1-4 kHz against 100-600 Hz +10..+13 dB) and opens again at its end (62.54-62.58, up to +15 dB) into an unvoiced breath
(62.58-62.66) before Nokia's N (62.68); the original's "boom" darkens into a nasal (-5..-18 dB) and runs into the N.
The fix as l910_m.m_close, on the vocal alone (BS-RoFormer estimate; out = song - V + V'): over the closure (the last
80 ms of the note) the band above ~1 kHz fades down like lips shutting and the level dips; the open release and the
breath after it fade out before the N. Three strengths: M a (-10 dB above 1 kHz, -2 dB level), b (-16, -4, L10's), c
(-22, -6); M d = b with the original singer's own m hum laid into the breath gap before the N (Whisper still
heard "glue" in a-c: darkening the vowel's end isn't an m). Clips into Desktop/suno_test/"PICK - 5 lines, old vs new" as "5 L19 M a/b/c - ...".
Run from audio/el_music with the analysis venv: l19_m.py build"""
import json, pathlib, sys
import numpy as np, librosa

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
WORK = HERE.parents[1] / "analysis/work/l19_m"
WORK.mkdir(parents=True, exist_ok=True)
SR = 44100
CLOSE, END = (62.50, 62.58), (62.58, 62.64)  # the lips closing; the release and breath faded out before the N (62.68)
W = (62.20, 62.80)
STRENGTH = {"a": (10, 2), "b": (16, 4), "c": (22, 6)}


def m_close(x, t0, db_hi, db_all):
    """l910_m.m_close with L19's times: above ~1 kHz down by db_hi, the level by db_all, over CLOSE; the release faded
    over END; before CLOSE untouched"""
    n_fft, hop = 1024, 256
    X = [librosa.stft(ch, n_fft=n_fft, hop_length=hop) for ch in x]
    t = t0 + np.arange(X[0].shape[1]) * hop / SR
    f = librosa.fft_frequencies(sr=SR, n_fft=n_fft)
    ramp = np.clip((t - CLOSE[0]) / (CLOSE[1] - CLOSE[0]), 0, 1)
    hi = np.clip((f - 700) / 600, 0, 1)
    fade = np.clip((END[1] - t) / (END[1] - END[0]), 0, 1)
    G = 10 ** ((-(db_hi * hi[:, None] * ramp[None]) - db_all * ramp[None]) / 20) * fade[None]
    y = np.stack([librosa.istft(Xc * G, hop_length=hop, length=x.shape[1]) for Xc in X])
    s = np.clip((np.arange(x.shape[1]) / SR + t0 - (CLOSE[0] - 0.02)) / 0.02, 0, 1)
    # after the release the vocal comes back (Nokia's N from 62.66)
    back = np.clip((np.arange(x.shape[1]) / SR + t0 - (END[1] + 0.01)) / 0.01, 0, 1)
    y = y * (1 - back) + x * back
    return (x * (1 - s) + y * s).astype(np.float32)


def darkening(v, t0):
    """1-4 kHz against 100-600 Hz over the closure minus over the vowel (62.36-62.48), dB; negative = closes darker"""
    m = v.mean(0)
    P = np.abs(librosa.stft(m, n_fft=2048, hop_length=441)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    t = t0 + np.arange(P.shape[1]) * 0.01
    r = 10 * np.log10(P[(f > 1000) & (f < 4000)].sum(0) + 1e-10) - 10 * np.log10(P[(f > 100) & (f < 600)].sum(0) + 1e-10)
    lvl = 10 * np.log10(P[(f > 100) & (f < 8000)].sum(0) + 1e-10)
    seg = lambda a, b: (t >= a) & (t < b)
    return dict(close_vs_vowel=round(float(r[seg(62.52, 62.60)].mean() - r[seg(62.36, 62.48)].mean()), 1),
                release_bright=round(float(r[seg(62.58, 62.66)].mean()), 1), release_lvl=round(float(lvl[seg(62.58, 62.66)].mean() - lvl[seg(62.36, 62.48)].mean()), 1))


def with_hum(E, Eo, t0, src=(62.60, 62.68), at=62.58, fade=0.015):
    """M d: M b's closure, then the original singer's own m hum (src, on the same note, 63) laid into the breath gap
    before Nokia's N (from `at`), its level matched to the take's closing vowel, 15 ms fades"""
    Eb = m_close(E, t0, *STRENGTH["b"])
    i_src0, i_src1, i_at = (int((x - t0) * SR) for x in (*src, at))
    hum = Eo[:, i_src0:i_src1].copy()
    ref = Eb[:, i_at - int(0.04 * SR):i_at]
    hum *= np.sqrt(np.mean(ref ** 2) / (np.mean(hum ** 2) + 1e-12)) * 10 ** (-3 / 20)  # a hum sits a little under its vowel
    n = hum.shape[1]; r = int(fade * SR)
    w = np.ones(n); w[:r] = np.linspace(0, 1, r); w[-r:] = np.linspace(1, 0, r)
    out = Eb.copy()
    out[:, i_at:i_at + n] = Eb[:, i_at:i_at + n] * (1 - w) + hum * w
    return out


def build():
    import rof, final12
    import line_round as LR
    from final11 import V
    from final10 import bounds
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=SR, mono=False)[0][:, : V.mix.shape[1]]
    E = rof.separate(v13, *W)
    i0 = int(W[0] * SR)
    a, b = bounds(19)
    cut = lambda y: y[:, int((a - 0.8) * SR):int((b + 0.5) * SR)]
    res = {"OLD": darkening(E, W[0]), "original": darkening(rof.original(V.mix)[:, i0:i0 + E.shape[1]], W[0])}
    for k, (dh, da) in STRENGTH.items():
        Ek = m_close(E, W[0], dh, da)
        out = v13.copy(); out[:, i0:i0 + E.shape[1]] = v13[:, i0:i0 + E.shape[1]] - E + Ek
        LR.mp3(cut(out), SR, WORK / f"L19 M {k} - I hear the basic income gloom.mp3")
        res[k] = darkening(Ek, W[0]) | dict(db_hi=dh, db_all=da, seam=[round(float(final12.seam_db(out, v13, x)), 1) for x in (CLOSE[0] - 0.02, END[1] + 0.02)])
    Eo = rof.original(V.mix)[:, i0:i0 + E.shape[1]]
    Ed = with_hum(E, Eo, W[0])
    out = v13.copy(); out[:, i0:i0 + E.shape[1]] = v13[:, i0:i0 + E.shape[1]] - E + Ed
    LR.mp3(cut(out), SR, WORK / "L19 M d - I hear the basic income gloom.mp3")
    res["d"] = darkening(Ed, W[0]) | dict(seam=[round(float(final12.seam_db(out, v13, x)), 1) for x in (CLOSE[0] - 0.02, 62.58, 62.68)])
    for k, r in res.items():
        print(k, r, flush=True)
    (WORK / "measure.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"build": build}[sys.argv[1]]()
