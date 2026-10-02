"""Score round 20 (eu20_inpaint.py) with round 14's untouched-splice selection (sel14.py): no warp, no tune, whole lines
(L9-L10 as one span). Odd takes sang L16 without "my" and L40 "Ee-You Ink", even takes with "my" and "E. U. Inc.".
Round 22 (eu22_inpaint.py, L24 and L40): L24 must be heard as S-A-P, not only without the old MLP.
usage: sel20.py [prefix] <count> <target> ...   prefix eu20 (default) or eu22; targets: 9-10 16 24 40
  -> sel20_<targets>.json (eu20) or sel_<prefix>_<targets>.json"""
import json, sys
prefix = sys.argv.pop(1) if not sys.argv[1].isdigit() else "eu20"
count, targets = int(sys.argv[1]), sys.argv[2:]
import sel14 as S  # clears sys.argv on import

S.TAKES = [f"{prefix}_{k}" for k in range(1, count + 1)]
S.A = lambda k: k % 2 == 1
_ok = S.words_ok
S.words_ok = lambda n, heard: _ok(n, heard) and (n != 24 or prefix == "eu20" or "sap" in S.flat(heard))
out_f = S.HERE / (f"sel20_{'_'.join(targets)}.json" if prefix == "eu20" else f"sel_{prefix}_{'_'.join(targets)}.json")
res = json.loads(out_f.read_text()) if out_f.exists() else {}
for target in targets:
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
                per[ln] = dict(cost=round(S.cost(m), 2), ok=S.words_ok(ln, heard), heard=heard, **m)
            row = dict(take=take, plan=plan[:3], insert=len(plan[0]) < len(S.V.LYR[n - 1]["words"]), margin=round(margin, 1),
                       cost=round(sum(p["cost"] for p in per.values()), 2), ok=all(p["ok"] for p in per.values()) and margin > 0,
                       display=disp, lines=per)
            rows.append(row)
            print(f"{target:5s} {take:8s} fit {margin:+6.1f} cost {row['cost']:5.2f} "
                  + " | ".join(f"L{ln} in50 {p['pitch_in50']} ghost {p['ghost']:.2f} band {p['band_db']} {'OK' if p['ok'] else 'no'} '{p['heard'][:60]}'" for ln, p in per.items()),
                  flush=True)
    good = sorted([r for r in rows if r["ok"]], key=lambda r: r["cost"])
    res[target] = dict(best=good[0] if good else None, top=good[:5], rows=rows)
    out_f.write_text(json.dumps(res, indent=1, default=str))
    print(f"{target} -> {(good[0]['take'] + ' cost ' + str(good[0]['cost'])) if good else 'NONE verified'}", flush=True)
