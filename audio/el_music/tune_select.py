"""Re-select weak lines with pitch correction to the original melody (vsplice.tune_to) as an option: the takes that
sing the new words best (top by lyric fit in select10.json), each as warp/nowarp x tuned. Updates select10.json."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V, review as R
from select10 import PLANS, cost

sel_f = HERE / "select10.json"
sel = json.loads(sel_f.read_text())
for n in map(int, sys.argv[1:]):
    tops = sorted([r for r in sel[str(n)]["rows"] if r["margin"] > 5 and r["kind"] != "full"], key=lambda r: -r["margin"])
    seen, rows = set(), []
    for r in tops:
        if r["take"] in seen or len(seen) >= 5:
            continue
        seen.add(r["take"])
        plan = next(p for takes, p in PLANS[n] if r["take"] in takes)
        V.PLAN[n] = plan
        y = V.load_take(r["take"])
        for warp_on in (True, False):
            b = V.build(y, n, warp_on=warp_on, tune=True)
            Y, _ = V.apply(V.mix, V.VO, b)
            _, margin = V.score(n, b)
            m = R.line_metrics(Y, V.mix, n)
            row = dict(take=r["take"], kind=("warp" if warp_on else "nowarp") + "+tune", text=plan[3], margin=round(margin, 1), cost=round(cost(m), 2), **m)
            rows.append(row)
            print(f"L{n:02d} {row['take']:8s} {row['kind']:12s} fit {margin:+6.1f} cost {row['cost']:5.2f} in50 {m['pitch_in50']:3d} ghost {m['ghost']:.2f} band {m['band_db']} onset {m['onset_ms']} seam {m['seam']}", flush=True)
    sel[str(n)]["rows"] += rows
    ok = [r for r in sel[str(n)]["rows"] if r["margin"] > 5]
    sel[str(n)]["best"] = min(ok, key=lambda r: r["cost"])
    sel_f.write_text(json.dumps(sel, indent=1))
    b = sel[str(n)]["best"]
    print(f"L{n:02d} -> {b['take']} {b['kind']} cost {b['cost']} in50 {b['pitch_in50']} fit {b['margin']}", flush=True)
