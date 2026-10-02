"""Constant-Q spectrograms (a piano-roll of the harmonics) of the original's lead vocal and each clip's, over a time
range, so the sung note can be read off the harmonics instead of trusting a pitch tracker (Praat jumps octaves on
soft notes). Uses compare.py's BS-RoFormer vocals. Writes analysis/qa/zoom_<label>.png.
Run: cd analysis && uv run python ../audio/el_music/zoom.py L9-10 27.8 29.8 E J"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compare as C
import numpy as np, librosa

if __name__ == "__main__":
    label, t_a, t_b, keys = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4:]
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    t0, ws = C.words(label)
    rows = [(" original", "original")] + [(k, k.strip()) for k in keys]
    fig, ax = plt.subplots(len(rows), 1, figsize=(16, 3.2 * len(rows)), sharex=True)
    for a, (k, name) in zip(ax, rows):
        _, v = C.split(C.clip(label, k))
        m = v.mean(0)[int((t_a - t0) * C.SR):int((t_b - t0) * C.SR)]
        Q = librosa.amplitude_to_db(np.abs(librosa.cqt(m, sr=C.SR, hop_length=C.HOP, fmin=librosa.note_to_hz("C3"),
                                                       n_bins=48 * 4, bins_per_octave=48)), ref=np.max)
        a.imshow(Q, origin="lower", aspect="auto", cmap="magma", vmin=-60, vmax=0,
                 extent=[t_a, t_b, 48 - 0.125, 48 + 48 - 0.125])  # MIDI 48 = C3, 4 octaves
        a.set_ylim(48, 84); a.set_yticks(range(48, 85, 2)); a.grid(alpha=.25, color="w")
        a.set_ylabel(f"{name}\nMIDI")
        for w in ws:
            if t_a <= w["start"] <= t_b:
                a.axvline(w["start"], color="c", lw=.6)
                a.text(w["start"], 82, w["w"], color="c", fontsize=9)
    fig.tight_layout(); fig.savefig(C.common.QA / f"zoom_{label}.png", dpi=80)
