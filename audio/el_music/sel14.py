"""Round 14 selection, with the lessons of animatic_v7 (the user's ear): every line they heard as broken or not smooth
had been processed -- pitch-tuned (L10, L16, L40) or a multi-syllable insert time-warped into the original phrase (L16,
L24) -- while untouched splices passed. So: no pitch-tune; whole lines (or the two lines L9-L10 as one span, so the
transition is the singer's own) spliced untouched (local alignment only); word inserts only where the take matches the
original around them. Score = select10.cost on each original line in the mix + Whisper words + CTC fit.
usage: sel14.py <target> ...   targets: 9-10 10 16 20 24 25 40   -> sel14_<targets>.json"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "analysis"))
import vsplice as V, review as R
from select10 import cost
ARGS, sys.argv = sys.argv[1:], sys.argv[:1]  # final_select reads its own argv on import
from final_select import hear, flat

TAKES = [f"eu14_{k}" for k in range(1, 21)]
A = lambda k: (k - 1) // 5 % 2 == 0  # text variant A (takes 1-5, 11-15)
L9, L10 = V.LYR[8], V.LYR[9]
V.LYR.append(dict(start=L9["start"], end=L10["end"], words=L9["words"] + L10["words"]))  # L9+L10 as one span
N910 = len(V.LYR)
ALL = V.ALL_WORDS


def plans(target, k):
    """[(line n for build, lines to score, plan, display texts per scored line)]"""
    if target == "10":  # round 24: words that keep the original's vowels; A(k) -> "that zooms", else "of doom"
        new, disp = ("WITH A FAX THAT ZOOMS", "with a fax that zooms") if A(k) else ("WITH A FAX OF DOOM", "with a fax of doom")
        return [(10, (10,), (ALL(10), "WITH A BAG OF SHROOMS", new, disp), {10: disp})]
    if target == "9-10":
        return [(N910, (9, 10), (ALL(N910), "TRAPPED IN THE CHINESE ROOM WITH A BAG OF SHROOMS", "TRAPPED IN THE BRUSSELS ROOM WHERE THE FAXES ZOOM", ""),
                 {9: "Trapped in the Brussels room,", 10: "where the faxes zoom"})]
    if target == "16":
        new, disp = ("I FEEL AY SEE TEMPERATURES REARRANGING", "I feel AC temperatures rearranging") if A(k) else \
                    ("I FEEL MY AY SEE TEMPERATURES REARRANGING", "I feel my AC temperatures rearranging")
        return [(16, (16,), (ALL(16), "I FEEL MY ATOMS REARRANGING", new, disp), {16: disp})]
    if target == "20":
        return [(20, (20,), ([0], "EN VEE DEE AY", "NOKIA", "Nokia"), {20: "Nokia to the moon"}),
                (20, (20,), (ALL(20), "EN VEE DEE AY TO THE MOON", "NOKIA TO THE MOON", "Nokia to the moon"), {20: "Nokia to the moon"})]
    if target == "24":
        return [(24, (24,), (ALL(24), "FORWARD EM EL PEE BACKWARD REPEAT", "FORWARD ESS AY PEE BACKWARD REPEAT", "Forward SAP, backward, repeat"),
                 {24: "Forward SAP, backward, repeat"})]
    if target == "25":
        return [(25, (25,), (ALL(25), "NOW VON NEUMANN'S OBSOLETE", "NOW PRIVATE CHATS GET OBSOLETE", "Now private chats get obsolete"), {25: "Now private chats get obsolete"}),
                (25, (25,), ([1, 2], "VON NEUMANN'S", "PRIVATE CHATS GET", "private chats get"), {25: "Now private chats get obsolete"})]
    if target == "40":
        return [(40, (40,), (ALL(40), "AR EL AITCH EF GOES ASKEW", "EE YOU INC FIXES THINGS SOON", "EU Inc fixes things soon"), {40: "EU Inc fixes things soon"})]


KEYS = {9: (["brussel"], 1), 10: (["fax"], 1), 16: (["temperat"], 1), 20: (["nokia", "nokya", "nokiya", "nokie"], 1),
        25: (["private", "chat"], 2), 40: (["fix", "thing", "soon"], 2)}


def words_ok(n, heard):
    h = flat(heard)
    if n == 24:
        return "mlp" not in h and "forward" in h
    if n == 40 and len(heard.split()) > 7:
        return False
    keys, need = KEYS[n]
    return sum(k in h for k in keys) >= need


if __name__ == "__main__":
    out_f = HERE / f"sel14_{'_'.join(ARGS)}.json"
    res = json.loads(out_f.read_text()) if out_f.exists() else {}
    for target in ARGS:
        rows = []
        for k, take in enumerate(TAKES, 1):
            y = V.load_take(take)
            for n, lines, plan, disp in plans(target, k):
                V.PLAN[n] = plan
                b = V.build(y, n, warp_on=False)
                Y = V.apply(V.mix, V.VO, b)[0]
                _, margin = V.score(n, b)
                per = {}
                for ln in lines:
                    m = R.line_metrics(Y, V.mix, ln)
                    heard = hear(Y, ln)
                    per[ln] = dict(cost=round(cost(m), 2), ok=words_ok(ln, heard), heard=heard, **m)
                row = dict(take=take, plan=plan[:3], insert=len(plan[0]) < len(V.LYR[n - 1]["words"]), margin=round(margin, 1),
                           cost=round(sum(p["cost"] for p in per.values()), 2), ok=all(p["ok"] for p in per.values()) and margin > 0,
                           display=disp, lines=per)
                rows.append(row)
                print(f"{target:5s} {take:8s} {'insert' if row['insert'] else 'whole ':6s} fit {margin:+6.1f} cost {row['cost']:5.2f} "
                      + " | ".join(f"L{ln} in50 {p['pitch_in50']} ghost {p['ghost']:.2f} band {p['band_db']} {'OK' if p['ok'] else 'no'} '{p['heard'][:60]}'" for ln, p in per.items()),
                      flush=True)
        good = sorted([r for r in rows if r["ok"]], key=lambda r: r["cost"])
        res[target] = dict(best=good[0] if good else None, top=good[:5], rows=rows)
        out_f.write_text(json.dumps(res, indent=1, default=str))
        print(f"{target} -> {(good[0]['take'] + (' insert' if good[0]['insert'] else ' whole') + ' cost ' + str(good[0]['cost'])) if good else 'NONE verified'}", flush=True)
