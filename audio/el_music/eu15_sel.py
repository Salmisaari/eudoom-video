"""Score one round of L20 takes. A hit has to sing Nokia and moon.
usage: eu15_sel.py [prefix] [count] [first]   default eu15 10 1, writes sel_<prefix>_20.json (sel_<prefix>_<first>_20.json)"""
import json, sys
# sel14 clears sys.argv on import, so read the round name first.
prefix = sys.argv[1] if len(sys.argv) > 1 else "eu15"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
import sel14 as S

S.TAKES = [f"{prefix}_{k}" for k in range(first, count + 1)]
target = "20"
rows = []
for k, take in enumerate(S.TAKES, 1):
    y = S.V.load_take(take)
    for n, lines, plan, disp in S.plans(target, k):
        S.V.PLAN[n] = plan
        b = S.V.build(y, n, warp_on=False)
        Y = S.V.apply(S.V.mix, S.V.VO, b)[0]
        _, margin = S.V.score(n, b)
        per = {}
        for ln in lines:
            m = S.R.line_metrics(Y, S.V.mix, ln)
            heard = S.hear(Y, ln)
            h = S.flat(heard)
            per[ln] = dict(cost=round(S.cost(m), 2), ok=S.words_ok(ln, heard) and "moon" in h, heard=heard, **m)
        row = dict(take=take, plan=plan[:3], insert=len(plan[0]) < len(S.V.LYR[n - 1]["words"]),
                   margin=round(margin, 1), cost=round(sum(p["cost"] for p in per.values()), 2),
                   ok=all(p["ok"] for p in per.values()) and margin > 0, display=disp, lines=per)
        rows.append(row)
        print(f"{target:5s} {take:8s} {'insert' if row['insert'] else 'whole ':6s} fit {margin:+6.1f} cost {row['cost']:5.2f} "
              + " | ".join(f"L{ln} in50 {p['pitch_in50']} ghost {p['ghost']:.2f} band {p['band_db']} {'OK' if p['ok'] else 'no'} '{p['heard'][:70]}'"
                           for ln, p in per.items()), flush=True)
good = sorted([r for r in rows if r["ok"]], key=lambda r: r["cost"])
res = {target: dict(best=good[0] if good else None, top=good[:5], rows=rows)}
(S.HERE / f"sel_{prefix}{f'_{first}' if first > 1 else ''}_20.json").write_text(json.dumps(res, indent=1, default=str))
print(f"20 -> {(good[0]['take'] + (' insert' if good[0]['insert'] else ' whole') + ' cost ' + str(good[0]['cost'])) if good else 'NONE verified'}", flush=True)
