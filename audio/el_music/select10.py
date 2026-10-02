"""Round 10 selection, judged on the finished line in the mix (review.py's metrics, calibrated on the user's verdicts
of v3-v5: the lines they called good sit at >=86% of frames within 50 c of the original melody, ghost <= 0.35,
band change <= 2.6 dB). For every candidate take three renditions are built -- vocal-only swap warped onto the
original timing, vocal-only unwarped, and the take's full mix on the line bounds -- and scored; the new words must
be sung (CTC lyric-fit margin > 0). usage: select10.py <line> ...  -> select10.json"""
import json, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V
import review as R

T = lambda p: [f"{p}_{k}" for k in range(1, 11)]
ALL = V.ALL_WORDS
# line: [(takes, (word indices, old as sung, new as sung, display))]
PLANS = {
    16: [(T("eu9"), ([3], "ATOMS", "AY SEE TEMPERATURES", "AC temperatures"))],
    19: [(T("eu9"), ([3, 4], "BASILISK BOOM", "BASIC INCOME GLOOM", "basic income gloom"))],
    23: [(T("eu12"), ([2], "SAFE", "FAST", "fast"))],
    24: [(T("eu10"), ([1], "EM EL PEE", "ESS AY PEE", "SAP,"))],
    25: [(T("eu12") + T("eu13"), ([1, 2], "VON NEUMANN'S", "PRIVACY IN CHATS", "privacy in chats"))],
    26: [(T("eu9"), (ALL(26), "SHARP LEFT TURN AND THERE YOU ARE", "SHARP LEFT TO THE WEST AND THERE YOU ARE",
                     "Sharp left to the west and there you are")),
         (T("eu6"), (ALL(26), "SHARP LEFT TURN AND THERE YOU ARE", "SHARP LEFT OVERSEAS AND THERE YOU ARE",
                     "Sharp left overseas and there you are"))],
    34: [(T("eu9"), ([0, 1], "ORTHOGONALITY THESIS", "OPEN EUROPE BORDERS", "Open Europe borders"))],
    35: [(T("eu9") + T("eu11"), ([0, 1], "JUST TRANSFORMERS", "BUILD UNICORNS", "Build unicorns"))],
    37: [(T("eu6"), ([0, 1], "POST CHINCHILLA SUPER DENSE", "BUILD POST AY EYE TRENDS", "Build post AI trends"))],
    40: [(T("eu9") + T("eu11") + T("eu13"), (ALL(40), "AR EL AITCH EF GOES ASKEW", "EE YOU INC FIXES THINGS SOON", "EU Inc fixes things soon"))],
    41: [(T("eu6"), ([3], ["PEE DOOM", "EE YOU DOOM"], "YOU DOOM", "EU doom"))],
}


def fullmix(y, n):
    """The take's own mix on the line bounds (locally aligned), crossfaded 30 ms into the original."""
    a, b = V.LYR[n - 1]["start"], V.LYR[n]["start"]
    yl = V.coarse(y, a, b)
    w = np.zeros(V.mix.shape[1]); i0, i1, xf = int(a * V.SR), int(b * V.SR), int(0.03 * V.SR)
    w[i0:i1] = 1; w[i0 - xf // 2:i0 - xf // 2 + xf] = np.linspace(0, 1, xf); w[i1 - xf // 2:i1 - xf // 2 + xf] = np.linspace(1, 0, xf)
    return V.mix * np.cos(w * np.pi / 2) + yl * np.sin(w * np.pi / 2)


def cost(m):
    return ((100 - m["pitch_in50"]) / 10 + 10 * max(0, m["ghost"] - 0.2) + 2 * max(0, m["band_db"] - 2.2)
            + max(0, m["onset_ms"] - 12) / 6 + 10 * max(0, m["seam"] - 1.1))


if __name__ == "__main__":
    out_f = HERE / "select10.json"
    res = json.loads(out_f.read_text()) if out_f.exists() else {}
    for n in map(int, sys.argv[1:]):
        rows = []
        for takes, plan in PLANS[n]:
            V.PLAN[n] = plan
            whole = len(plan[0]) == len(V.LYR[n - 1]["words"])
            for name in takes:
                if not (HERE / f"{name}.mp3").exists():
                    continue
                y = V.load_take(name)
                for kind in (("nowarp", "full") if whole else ("warp", "nowarp", "full")):
                    if kind == "full":
                        Y = fullmix(y, n)
                        r = V.build(y, n, warp_on=False)  # words are checked on the take's vocal either way
                    else:
                        r = V.build(y, n, warp_on=kind == "warp")
                        Y, _ = V.apply(V.mix, V.VO, r)
                    _, margin = V.score(n, r)
                    m = R.line_metrics(Y, V.mix, n)
                    row = dict(take=name, kind=kind, text=plan[3], margin=round(margin, 1), cost=round(cost(m), 2), **m)
                    rows.append(row)
                    print(f"L{n:02d} {name:9s} {kind:6s} fit {margin:+6.1f} cost {row['cost']:5.2f} "
                          f"in50 {m['pitch_in50']:3d} ghost {m['ghost']:.2f} band {m['band_db']:.1f} onset {m['onset_ms']} seam {m['seam']}",
                          flush=True)
        ok = [r for r in rows if r["margin"] > 0] or rows
        best = min(ok, key=lambda r: r["cost"])
        res[str(n)] = dict(best=best, rows=rows)
        out_f.write_text(json.dumps(res, indent=1))
        print(f"L{n:02d} -> {best['take']} {best['kind']} ({best['text']}) cost {best['cost']}", flush=True)
