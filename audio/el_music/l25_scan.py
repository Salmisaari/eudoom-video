"""L25 "Now privacy in chats obsolete" sounds chopped in v8 (= v7: eu12_3's "privacy in chats" inserted between the
original singer's "Now" and "obsolete"). Measured on the vocals (BS-RoFormer, Praat f0): the original sings "von
Neumann's" as one legato phrase (voiced 78.22-79.72 s but for a 20 ms dip); eu12_3 breaks it with four hisses
(160, 80, 100, 140 ms) and the insert adds two joins inside continuous singing.
Every round 12/13 take (they all sing "privacy in chats"), whole line: how legato (share of the original's voiced
frames the take also voices, longest unvoiced gap inside the phrase), on the melody (within 50 cents), and whether
it sings the new words (CTC margin old -> new, lyricfit). Run with analysis/.venv/bin/python."""
import json, pathlib, sys
import numpy as np, parselmouth, librosa

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V
import rof
import lyricfit as F

A, B = 77.0, 81.9
PHRASE = (78.22, 79.72)  # the original's legato "von Neumann's"
LINE = (77.72, 81.21)


def f0(v):
    p = parselmouth.Sound(v.mean(0).astype(np.float64), V.SR).to_pitch_ac(
        time_step=0.01, pitch_floor=150, pitch_ceiling=900, octave_jump_cost=0.8, voicing_threshold=0.3)
    t = A + np.arange(int((B - A) * 100)) / 100
    return t, np.array([p.get_value_at_time(x - A) or np.nan for x in t])


def longest_gap(voiced):
    best = cur = 0
    for x in voiced:
        cur = 0 if x else cur + 1
        best = max(best, cur)
    return best * 10


if __name__ == "__main__":
    vo = rof.original(V.mix)[:, int(A * V.SR):int(B * V.SR)]
    t, fo = f0(vo)
    ph = (t >= PHRASE[0]) & (t < PHRASE[1])
    ln = (t >= LINE[0]) & (t < LINE[1])
    rows = {}
    for name in sorted({p.stem for p in HERE.glob("eu12_*.mp3")} | {p.stem for p in HERE.glob("eu13_*.mp3")},
                       key=lambda s: (s.split("_")[0], int(s.split("_")[1]))):
        y = V.coarse(V.load_take(name), *LINE)
        vt = rof.separate(y, A, B)
        _, ft = f0(vt)
        ov = ph & np.isfinite(fo)
        legato = float(np.mean(np.isfinite(ft[ov])))
        gap = longest_gap(np.isfinite(ft[ph]))
        both = ln & np.isfinite(fo) & np.isfinite(ft)
        in50 = float(np.mean(np.abs(1200 * np.log2(ft[both] / fo[both])) < 50))
        seg = vt.mean(0)[int((LINE[0] - 0.2 - A) * V.SR):int((LINE[1] + 0.2 - A) * V.SR)]
        em = F.emissions(librosa.resample(seg, orig_sr=V.SR, target_sr=22050), 22050)
        margin = F.margin(em, "NOW VON NEUMANN'S OBSOLETE", "NOW PRIVACY IN CHATS OBSOLETE")
        rows[name] = dict(legato=round(legato, 2), gap_ms=gap, in50=round(in50, 2), margin=round(float(margin), 1))
        print(f"{name:9s} legato {legato:4.0%}  longest gap {gap:4d} ms  melody {in50:4.0%}  new words {margin:+6.1f}", flush=True)
    (HERE / "l25_scan.json").write_text(json.dumps(rows, indent=1))
