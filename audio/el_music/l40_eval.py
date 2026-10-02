"""L40 "EU Inc fixes things soon": the takes that hold "soon" as one note like the original "askew" (round 13), in every
rendition (warp/tune/separation), scored on the line in the mix + what Whisper hears. -> l40_eval.json"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "analysis"))
import vsplice as V, review as R
from select10 import PLANS, cost
TAKES, sys.argv = sys.argv[1:], sys.argv[:1]  # final_select reads its own argv on import
from final_select import hear

V.PLAN[40] = PLANS[40][0][1]
rows = []
for take in TAKES:
    y = V.load_take(take)
    for sep in ("htdemucs", "htdemucs_ft"):
        for warp in (False, True):
            for tune in (False, True):
                b = V.build(y, 40, sep=sep, warp_on=warp, tune=tune)
                Y = V.apply(V.mix, V.VO, b)[0]
                m = R.line_metrics(Y, V.mix, 40)
                r = dict(take=take, sep=sep, warp=warp, tune=tune, cost=round(cost(m), 2), margin=round(V.score(40, b)[1], 1), heard=hear(Y, 40), **m)
                rows.append(r)
                print(f"{take} {sep:11s} {'warp' if warp else 'nowarp'}{'+tune' if tune else '':5s} cost {r['cost']:5.2f} in50 {m['pitch_in50']:3d} ghost {m['ghost']:.2f} band {m['band_db']:.1f} fit {r['margin']:+5.1f} | {r['heard'][:90]}", flush=True)
(HERE / "l40_eval.json").write_text(json.dumps(rows, indent=1, default=float))
