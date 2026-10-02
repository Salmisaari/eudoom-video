"""Does an L20 take sing "Nokia" or "No key"? Whisper hears a sung No-ki-a as "No key" and the rounds 14-19 gate threw
those takes away. CTC loss (lyricfit's wav2vec2 letters) on the spliced line's vocal, per reading; kia = loss("NO KEY
TO THE MOON") - loss("NOKIA TO THE MOON") > 0 means the final "a" is there.
usage: l20_kia.py sel_json ...   prints one row per take and rendition, writes l20_kia.json"""
import json, pathlib, sys
import librosa

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vsplice as V, lyricfit as F

READ = ["NOKIA TO THE MOON", "NO KEY TO THE MOON", "EN VEE DEE AY TO THE MOON", "NO KAIYA TO THE MOON"]
PLAN = {True: ([0], "EN VEE DEE AY", "NOKIA", "Nokia"),
        False: (V.ALL_WORDS(20), "EN VEE DEE AY TO THE MOON", "NOKIA TO THE MOON", "Nokia to the moon")}


def losses(voc):
    L = V.LYR[19]
    v = librosa.to_mono(voc[:, int((L["start"] - 0.2) * V.SR):int((L["end"] + 0.2) * V.SR)])
    em = F.emissions(v, V.SR)
    return {r: round(F.loss(em, r), 1) for r in READ}


if __name__ == "__main__":
    rows = [dict(take="original", insert=None, **losses(V.VO))]
    for f in sys.argv[1:]:
        for r in json.loads((HERE / f).read_text())["20"]["rows"]:
            p = list(r["lines"].values())[0]
            if r["margin"] < 25 or p["ghost"] > 0.7:
                continue
            V.PLAN[20] = PLAN[r["insert"]]
            voc = V.apply(V.mix, V.VO, V.build(V.load_take(r["take"]), 20, warp_on=False))[1]
            rows.append(dict(take=r["take"], insert=r["insert"], fit=r["margin"], in50=p["pitch_in50"], ghost=p["ghost"],
                             heard=p["heard"], **losses(voc)))
    for r in rows:
        r["kia"] = round(r["NO KEY TO THE MOON"] - r["NOKIA TO THE MOON"], 1)
        print(f"{r['take']:9s} {'ins' if r['insert'] else 'whl'} kia {r['kia']:+5.1f} nokia {r['NOKIA TO THE MOON']:5.1f} "
              f"nvda {r['EN VEE DEE AY TO THE MOON']:5.1f} in50 {r.get('in50', '')} ghost {r.get('ghost', '')} '{r.get('heard', '')[:40]}'", flush=True)
    (HERE / "l20_kia.json").write_text(json.dumps(rows, indent=1))
