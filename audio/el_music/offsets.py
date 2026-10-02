"""How far each clip's vocal is from the original's, frame by frame, measured on the harmonics (no pitch tracker):
  timing  DTW between the two vocals on octave-folded pitch (chroma) + loudness + onset strength, which the
          words don't change much: ms the clip is late (+) or early (-) against the original at each moment
  pitch   on the time-aligned frames, the transposition (cents) that best lines up the clip's harmonic pattern with
          the original's (constant-Q, 25-cent bins, formants flattened out): immune to the octave jumps a tracker
          makes when the 2nd harmonic is the loud one; frames where the patterns don't match well are left out
  level   dB the clip's vocal is louder (+) than the original's at the same moment (aligned)
Per original word: median of each. Plot analysis/qa/offsets_<label>.png.
Run: cd analysis && uv run python ../audio/el_music/offsets.py L9-10 E J"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compare as C
import numpy as np, librosa, scipy.ndimage as nd

BPO, FMIN = 48, librosa.note_to_hz("C3")
SHIFT = 28  # bins searched each way (7 semitones)


def features(v):
    m = v.mean(0)
    Q = np.abs(librosa.cqt(m, sr=C.SR, hop_length=C.HOP, fmin=FMIN, n_bins=BPO * 5, bins_per_octave=BPO))
    L = np.log(Q + 1e-6)
    flat = L - nd.uniform_filter1d(L, BPO, axis=0)  # formants out, harmonic peaks left
    flat = np.maximum(flat, 0)
    lvl = 20 * np.log10(np.sqrt((Q ** 2).sum(0)) + 1e-6)
    chroma = flat.reshape(5, BPO, -1).sum(0)
    chroma = chroma.reshape(12, 4, -1).sum(1)
    chroma /= np.linalg.norm(chroma, axis=0, keepdims=True) + 1e-6
    on = librosa.onset.onset_strength(y=m, sr=C.SR, hop_length=C.HOP)[: Q.shape[1]]
    return dict(flat=flat, lvl=lvl, chroma=chroma, on=on / (on.max() + 1e-6))


def align(O, K):
    """clip frame for each original frame (DTW, +-150 ms band, smoothed)"""
    z = lambda x: (x - x.mean()) / (x.std() + 1e-6)
    act = lambda F: np.clip((F["lvl"] - F["lvl"].max() + 40) / 40, 0, 1)
    fo = np.vstack([O["chroma"] * act(O), z(O["lvl"])[None] * 0.7, O["on"][None] * 1.5])
    fk = np.vstack([K["chroma"] * act(K), z(K["lvl"])[None] * 0.7, K["on"][None] * 1.5])
    n = min(fo.shape[1], fk.shape[1])
    D = ((fo[:, :n, None] - fk[:, None, :n]) ** 2).sum(0)
    i, j = np.indices(D.shape)
    D[np.abs(i - j) > 15] = np.inf
    _, wp = librosa.sequence.dtw(C=D, step_sizes_sigma=np.array([[1, 1], [1, 2], [2, 1]]))
    wp = wp[::-1]
    m = np.interp(np.arange(n), wp[:, 0], wp[:, 1])  # the diagonal steps skip frames
    return np.clip(nd.uniform_filter1d(m, 9), 0, n - 1)


def pitch_shift(O, K, m):
    """cents the clip sits above the original at each original frame (nan where the harmonics don't line up)"""
    n = len(m)
    out, conf = np.full(n, np.nan), np.zeros(n)
    for k in range(n):
        o, c = O["flat"][:, k], K["flat"][:, int(round(m[k]))]
        if o.sum() < 1 or c.sum() < 1:
            continue
        sc = [np.dot(o[max(0, -s):len(o) - max(0, s)], c[max(0, s):len(c) - max(0, -s)]) for s in range(-SHIFT, SHIFT + 1)]
        sc = np.array(sc) / (np.linalg.norm(o) * np.linalg.norm(c) + 1e-9)
        b = int(np.argmax(sc))
        if 0 < b < 2 * SHIFT:  # parabolic peak
            d = (sc[b - 1] - sc[b + 1]) / (2 * (sc[b - 1] - 2 * sc[b] + sc[b + 1]) + 1e-9)
        else:
            d = 0
        out[k], conf[k] = (b - SHIFT + d) * 1200 / BPO, sc[b]
    return out, conf


def measure(label, key):
    t0, ws = C.words(label)
    O = features(C.split(C.clip(label, " original"))[1])
    K = features(C.split(C.clip(label, key))[1])
    m = align(O, K)
    n = len(m)
    dt = (m - np.arange(n)) * C.HOP / C.SR * 1000
    cents, conf = pitch_shift(O, K, m)
    voiced = (O["lvl"][:n] > O["lvl"].max() - 30) & (conf > 0.45)
    cents[~voiced] = np.nan
    dl = K["lvl"][np.round(m).astype(int)] - O["lvl"][:n]
    dl[O["lvl"][:n] < O["lvl"].max() - 35] = np.nan
    return t0, ws, dt, cents, dl, O


if __name__ == "__main__":
    label, keys = sys.argv[1], sys.argv[2:]
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(4, 1, figsize=(16, 11), sharex=True)
    for i, key in enumerate(keys):
        t0, ws, dt, cents, dl, O = measure(label, key)
        t = t0 + np.arange(len(dt)) * C.HOP / C.SR
        print(f"\n{label}{key}: per original word   timing ms (+ = late) | pitch cents | level dB")
        for w in ws:
            s = (t >= w["start"]) & (t < w["end"])
            med = lambda x: np.nanmedian(x[s]) if np.isfinite(x[s]).sum() > 3 else np.nan
            print(f"  {w['w']:12s} {med(dt):5.0f} | {med(cents):5.0f} ({np.isfinite(cents[s]).mean():.0%} frames) | {med(dl):5.1f}")
        ax[0].plot(t, dt, f"C{i}", label=key); ax[1].plot(t, cents, f"C{i}.", ms=3); ax[2].plot(t, dl, f"C{i}", lw=1)
        if i == 0:
            ax[3].plot(t, O["lvl"][:len(t)], "k")
    for a, name in zip(ax, ("clip late by ms", "clip pitch vs original, cents", "clip level vs original, dB", "original level dB")):
        a.set_ylabel(name); a.grid(alpha=.3)
        for w in ws:
            a.axvline(w["start"], color="gray", lw=.5)
    for w in ws:
        ax[0].text(w["start"], 130, w["w"], fontsize=9)
    ax[0].set_ylim(-150, 150); ax[1].set_ylim(-800, 800); ax[2].set_ylim(-20, 20); ax[0].legend()
    ax[0].set_xlim(ws[0]["start"] - 0.2, ws[-1]["end"] + 0.2)
    fig.tight_layout(); fig.savefig(C.common.QA / f"offsets_{label}.png", dpi=80)
