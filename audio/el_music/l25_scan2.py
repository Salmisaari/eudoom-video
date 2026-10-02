"""l25_scan.py for the user's new L25 lines: eu26_* "Now vegan steak's obsolete" (clips L25v14-22) and eu25_* "Now plastic
straws obsolete" (L25v23-31): legato over the original's "von Neumann's" phrase, on the melody, new words (CTC margin)."""
import json, sys, pathlib
import numpy as np, librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V
import rof
import lyricfit as F
from l25_scan import A, B, PHRASE, LINE, f0, longest_gap

if __name__ == "__main__":
    vo = rof.original(V.mix)[:, int(A * V.SR):int(B * V.SR)]
    t, fo = f0(vo)
    ph = (t >= PHRASE[0]) & (t < PHRASE[1]); ln = (t >= LINE[0]) & (t < LINE[1])
    rows, n = {}, 14
    for pre, new in (("eu26", "NOW VEGAN STEAKS OBSOLETE"), ("eu25", "NOW PLASTIC STRAWS OBSOLETE")):
        for k in range(1, 10):
            name = f"{pre}_{k}"
            vt = rof.separate(V.coarse(V.load_take(name), *LINE), A, B)
            _, ft = f0(vt)
            ov = ph & np.isfinite(fo)
            legato = float(np.mean(np.isfinite(ft[ov]))); gap = longest_gap(np.isfinite(ft[ph]))
            both = ln & np.isfinite(fo) & np.isfinite(ft)
            in50 = float(np.mean(np.abs(1200 * np.log2(ft[both] / fo[both])) < 50))
            seg = vt.mean(0)[int((LINE[0] - 0.2 - A) * V.SR):int((LINE[1] + 0.2 - A) * V.SR)]
            em = F.emissions(librosa.resample(seg, orig_sr=V.SR, target_sr=22050), 22050)
            margin = F.margin(em, "NOW VON NEUMANN'S OBSOLETE", new)
            rows[f"L25v{n}"] = dict(take=name, legato=round(legato, 2), gap_ms=gap, in50=round(in50, 2), margin=round(float(margin), 1))
            print(f"L25v{n} {name:8s} legato {legato:4.0%}  gap {gap:4d} ms  melody {in50:4.0%}  new words {margin:+6.1f}", flush=True)
            n += 1
    (HERE / "l25_scan2.json").write_text(json.dumps(rows, indent=1))
