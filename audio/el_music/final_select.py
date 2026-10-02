"""Final pick per line: cheapest by the calibrated cost (select10.cost) among renditions whose new words Whisper
actually hears (keys), with pitch correction to the original melody available for every take. Updates select10.json."""
import json, pathlib, sys, tempfile
import librosa, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "analysis"))
import vsplice as V, review as R
import mlx_whisper
from select10 import PLANS, fullmix, cost

flat = lambda s: "".join(c for c in s.lower() if c.isalnum())
KEYS = {16: (["temperat"], 1), 19: (["gloom", "glum", "gloo"], 1), 23: (["fast"], 1), 24: (None, 0), 25: (["privac", "chat"], 2),
        26: (["overseas", "oversea", "west"], 1), 34: (["open", "europe", "border"], 2), 35: (["unicorn"], 1),
        37: (["build", "post", "trend"], 2), 40: (["inc", "fix", "thing", "soon"], 2), 41: (None, 0)}
HOOK_TAKES = {"eu6_4", "eu6_2"}  # the hooks the user approved in animatic_v5


def hear(Y, n):
    L = V.LYR[n - 1]
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, librosa.resample(Y.mean(0)[int((L["start"] - 0.2) * V.SR):int((L["end"] + 0.2) * V.SR)], orig_sr=V.SR, target_sr=16000), 16000)
        return mlx_whisper.transcribe(f.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


def words_ok(n, heard):
    keys, need = KEYS[n]
    h = flat(heard)
    if n == 24:
        return "mlp" not in h and "forward" in h  # SAP sounds like letters; the old MLP must be gone
    if n == 41:
        return "pdoom" not in h and "mypee" not in h
    if n == 40 and len(heard.split()) > 7:  # the held "soon" must stay one held note (no words sung into it)
        return False
    return sum(k in h for k in keys) >= need


def render(n, row):
    plan = next(p for t, p in PLANS[n] if row["take"] in t)
    V.PLAN[n] = plan
    y = V.load_take(row["take"])
    if row["kind"] == "full":
        return fullmix(y, n), None
    b = V.build(y, n, warp_on=row["kind"].startswith("warp"), tune="tune" in row["kind"])
    return V.apply(V.mix, V.VO, b)[0], b


sel_f = HERE / "select10.json"
sel = json.loads(sel_f.read_text())
for n in map(int, sys.argv[1:]):
    rows = sel[str(n)]["rows"]
    # tuned variants for the takes that sing the new words best
    have = {(r["take"], r["kind"]) for r in rows}
    tops = [t for t in dict.fromkeys(r["take"] for r in sorted(rows, key=lambda r: -r["margin"]) if r["margin"] > 0)][:6]
    if n == 41:
        tops = list(dict.fromkeys(list(HOOK_TAKES) + tops))[:6]
    for take in tops:
        for kind in ("warp+tune", "nowarp+tune"):
            if (take, kind) in have:
                continue
            Y, b = render(n, dict(take=take, kind=kind))
            m = R.line_metrics(Y, V.mix, n)
            rows.append(dict(take=take, kind=kind, text=PLANS[n][0][1][3], margin=round(V.score(n, b)[1], 1), cost=round(cost(m), 2), **m))
    pool = sorted([r for r in rows if r["margin"] > 0 or n == 41], key=lambda r: (0 if (n == 41 and r["take"] in HOOK_TAKES) else 1, r["cost"]))
    best = None
    for r in pool[:20 if n == 40 else 10]:
        Y, _ = render(n, r)
        r["heard"] = hear(Y, n)
        ok = words_ok(n, r["heard"])
        print(f"L{n:02d} {r['take']:8s} {r['kind']:12s} cost {r['cost']:5.2f} in50 {r['pitch_in50']:3d} ghost {r['ghost']:.2f} words {'OK ' if ok else 'no '} | {r['heard']}", flush=True)
        if ok and r["cost"] <= 6:
            best = r
            break
    sel[str(n)]["rows"] = rows
    sel[str(n)]["best"] = best or sel[str(n)]["best"]
    sel[str(n)]["verified"] = bool(best)
    sel_f.write_text(json.dumps(sel, indent=1))
    print(f"L{n:02d} -> {'VERIFIED ' if best else 'UNVERIFIED '}{sel[str(n)]['best']['take']} {sel[str(n)]['best']['kind']}", flush=True)
