"""L28 "NATO, please don't let me go": the song still has the original singer's "Gato" (only the screen says NATO).
The round-2 takes (eu2_*) sang NATO over L27-L28. Per take, whole line, measured like l25_scan.py: legato (share of
the original's voiced frames the take voices), longest unvoiced gap, on the melody (within 50 cents), and N vs G
(CTC margin "GATO ..." -> "NATO ...", lyricfit). Run with analysis/.venv/bin/python."""
import json, pathlib, sys
import numpy as np, librosa
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V
import rof, lyricfit as F
from l25_scan import f0 as _f0, longest_gap
import l25_scan

LINE = (89.28, 95.47)
A, B = 88.6, 96.0
l25_scan.A, l25_scan.B = A, B
if __name__ == "__main__":
    vo = rof.original(V.mix)[:, int(A * V.SR):int(B * V.SR)]
    t, fo = _f0(vo)
    ln = (t >= LINE[0]) & (t < LINE[1])
    rows = {}
    for name in ["eu2_low5", "eu2_low10", "eu2_low11", "eu2_low2", "eu2_low8", "eu2_low1", "eu2_low9", "eu2_low4"]:
        y = V.coarse(V.load_take(name), *LINE)
        vt = rof.separate(y, A, B)
        _, ft = _f0(vt)
        ov = ln & np.isfinite(fo)
        legato = float(np.mean(np.isfinite(ft[ov])))
        gap = longest_gap(np.isfinite(ft[ln]) | ~np.isfinite(fo[ln]))
        both = ln & np.isfinite(fo) & np.isfinite(ft)
        in50 = float(np.mean(np.abs(1200 * np.log2(ft[both] / fo[both])) < 50))
        seg = vt.mean(0)[int((LINE[0] - 0.2 - A) * V.SR):int((LINE[1] + 0.2 - A) * V.SR)]
        em = F.emissions(librosa.resample(seg, orig_sr=V.SR, target_sr=22050), 22050)
        margin = F.margin(em, "GATO PLEASE DON'T LET ME GO", "NATO PLEASE DON'T LET ME GO")
        rows[name] = dict(legato=round(legato, 2), gap_ms=gap, in50=round(in50, 2), n_vs_g=round(float(margin), 1))
        print(f"{name:10s} legato {legato:4.0%}  gap where the original sings {gap:4d} ms  melody {in50:4.0%}  N over G {margin:+5.1f}", flush=True)
    (HERE / "l28_scan.json").write_text(json.dumps(rows, indent=1))
