"""L10 "where the faxes zoom": v3's take (eu2_low3, the one the user liked) was pasted as a full mix, so its own band played
under the line -- up to 12.6 dB off the original at 28.05-28.35 s, in the gap before "where the" (the "audio bug before").
Rebuild it as a vocal-only swap (the band stays the original) and compare with the v3 line. -> l10_fix.json"""
import json, pathlib, sys
import librosa, numpy as np, soundfile as sf
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "analysis"))
import vsplice as V, review as R
from select10 import cost
from final_select import hear

V.PLAN[10] = (V.ALL_WORDS(10), "WITH A BAG OF SHROOMS", "WHERE THE FAXES ZOOM", "where the faxes zoom")
y = V.load_take("eu2_low3")
v3 = librosa.load(HERE / "pdoom_EU_v3.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
rows = [dict(kind="v3 full mix", **R.line_metrics(v3, V.mix, 10), heard=hear(v3, 10))]
for sep in ("htdemucs", "htdemucs_ft"):
    for warp in (False, True):
        for tune in (False, True):
            Y, _ = V.apply(V.mix, V.VO, V.build(y, 10, sep=sep, warp_on=warp, tune=tune))
            kind = f"{'warp' if warp else 'nowarp'}{'+tune' if tune else ''} ({sep})"
            rows.append(dict(kind=kind, **R.line_metrics(Y, V.mix, 10), heard=hear(Y, 10)))
            sf.write(HERE / f"l10_{kind.replace(' ', '_').replace('(', '').replace(')', '').replace('+', '_')}.wav", Y[:, int(26 * V.SR):int(31 * V.SR)].T, V.SR)
for r in rows:
    r["cost"] = round(cost(r), 2)
    print(f"{r['kind']:28s} cost {r['cost']:5.2f} in50 {r['pitch_in50']:3d} ghost {r['ghost']:.2f} band {r['band_db']:.1f} onset {r['onset_ms']} | {r['heard']}")
(HERE / "l10_fix.json").write_text(json.dumps(rows, indent=1, default=float))
