"""v8: v7 plus only the lines the user approved in eu_v8_lines (2026-09-30), each rebuilt exactly as the clip they
heard, with their last notes on round 6:
  L9-10  E (eu2_low4 for both lines, mid-tuned, htdemucs_ft) with "zoom" closed on an m (l910_m.py; "L9-10E works if
         zooe -> zoom")
  L16    O (eu9_7, "-ranging" lifted, BS-RoFormer split, centre/sides levelled; "L16O is great")
  L20    L (eu18_3 "Nokia" inserted, RoFormer) from the breath before "N" at 62.62 s on; before it I (Demucs), whose
         end of "gloom" runs as long as v7's ("the mini part before that doesn't match, cut before Nokia starts")
  L24    Q's "SAP" only (eu22_3, its S lifted, RoFormer, levelled), "Forward" and "backward, repeat" the original
         singer's ("SAP great, maybe just cut that into the original")
  L40    J's "EU" (eu22_7, hook-style "you") and A's "Inc fixes things soon" (eu20_1, "closest"), joined in the
         unvoiced gap both have at 121.09 s ("the EU first is good but then the second EU doesn't work")
  L25    stays v7 ("Now privacy in chats obsolete"); every other line is v7.
Seams: correlation-aware crossfades (final11.paste); the two inner joins (62.62, 121.09) sit in unvoiced sound.
Writes pdoom_EU_v8.wav, audio/pdoom_eu.mp3, Desktop/suno_test/eu_v8/pdoom_EU_edition_v8.mp3, v8_sources.json and
one clip per changed line in Desktop/suno_test/eu_v8_final."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, swap, V, ROOT
from final10 import bounds, quiet
import final12, l910, l910_m
from v8_refine import region, P16_ALL, PSOLA
from r22_clips import P24_INS, P40
from l24_s import s_boost
import rof

VO_D = V.VO                      # htdemucs_ft split of the original (the Demucs builds)
VO_R = rof.original(V.mix)       # BS-RoFormer split (round 6 builds)
import rof_clips                  # (sets V.VO to RoFormer on import)
V.VO = VO_D
ms = rof_clips.ms


def paste_at(out, src, a, b, xf=0.04):
    """final11.paste on exactly [a, b] (no snapping to the original's quiet points)"""
    q = quiet.__globals__
    snap = q["quiet"]
    try:
        import final11
        final11.quiet = lambda t, *k: t
        return paste(out, src, a, b, xf)
    finally:
        final11.quiet = snap


def hooked(hook, n, take, plan, sep, vo):
    """swap() with hook as the build's tune step (as v8_refine.write runs it)"""
    V.VO = vo
    hook.a = V.LYR[n - 1]["start"] - 0.8
    V.tune_to = hook
    try:
        return swap(take, plan, n, sep=sep, warp_on=False, tune=True)
    finally:
        V.tune_to = PSOLA
        V.VO = VO_D


if __name__ == "__main__":
    v7 = librosa.load(HERE / "pdoom_EU_v7.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    out, src = v7.copy(), {}
    # L9-10
    Y = hooked(l910_m.e_with_m, l910.N, "eu2_low4", l910.PLAN, "htdemucs_ft", VO_D)
    out, span = paste(out, Y, *bounds(l910.N))
    src["L9"] = dict(source="eu2_low4 mid-tuned (htdemucs_ft), with L10: L9-10E", span=span, text="Trapped in the Brussels room,")
    src["L10"] = dict(source="eu2_low4 mid-tuned (htdemucs_ft), zoom closed on an m: L9-10E + l910_m", span=span, text="where the faxes zoom")
    # L16
    Y = hooked(ms(region(52.05, 52.85, 600), 16), 16, "eu9_7", P16_ALL, "bsroformer", VO_R)
    out, span = paste(out, Y, *bounds(16))
    src["L16"] = dict(source="eu9_7 whole line, -ranging lifted (bsroformer, centre/sides levelled): L16O", span=span,
                      text="I feel my AC temperatures rearranging")
    # L20: I up to the breath before "N", L from there
    YI, desc = final12.line("eu18_3", "20i")
    out, span_i = paste(out, YI, *bounds(20))
    Y = hooked(ms(None, 20), 20, "eu18_3", final12.P["20i"], "bsroformer", VO_R)
    out, span = paste_at(out, Y, 62.62, span_i[1])
    src["L20"] = dict(source=f"{desc} to 62.62 s (L20I), eu18_3 Nokia (bsroformer, levelled) from there (L20L)",
                      span=[span_i[0], span[1]], text="Nokia to the moon")
    # L24: only SAP, into the original line
    Y = hooked(ms(s_boost(8), 24), 24, "eu22_3", P24_INS, "bsroformer", VO_R)
    out, span = paste(out, Y, *bounds(24))
    src["L24"] = dict(source="eu22_3 'SAP' only, S lifted (bsroformer, levelled): L24Q's SAP in the original line", span=span,
                      text="Forward SAP, backward, repeat")
    # L40: J's EU, A's rest
    V.VO = VO_D
    YJ = swap("eu22_7", P40, 40, sep="htdemucs_ft", warp_on=False, tune=False)
    YA, desc_a = final12.line("eu20_1", 40)
    a40, b40 = bounds(40)
    out, span_j = paste_at(out, YJ, quiet(a40), 121.09)
    out, span_a = paste_at(out, YA, 121.09, quiet(b40))
    src["L40"] = dict(source=f"eu22_7 'EU' (htdemucs_ft, L40J) to 121.09 s, {desc_a} from there (L40A)",
                      span=[span_j[0], span_a[1]], text="EU Inc fixes things soon")
    # everything else as v7
    v7src = json.loads((HERE / "v7_sources.json").read_text())
    for k, s in v7src.items():
        src.setdefault(k, dict(s, source=f"v7: {s['source']}"))
    sf.write(HERE / "pdoom_EU_v8.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v8.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v8"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v8.wav", "-b:a", "320k", d / "pdoom_EU_edition_v8.mp3"], check=True)
    (HERE / "v8_sources.json").write_text(json.dumps(dict(sorted(src.items(), key=lambda kv: int(kv[0][1:]))), indent=1))
    # checks: v7 untouched outside the changed spans; seam level vs v7 at every edge
    changed = [src[k]["span"] for k in ("L10", "L16", "L20", "L24", "L40")]
    mask = np.ones(out.shape[1], bool)
    for a, b in changed:
        mask[int((a - 0.03) * V.SR):int((b + 0.03) * V.SR)] = False
    print(f"outside the changed lines vs v7: max |diff| {np.abs(out - v7)[:, mask].max():.1e}")
    for t in [x for ab in changed for x in ab] + [62.62, 121.09]:
        print(f"  seam {t:7.3f}: {final12.seam_db(out, v7, t):+.1f} dB vs v7, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
    # a clip per changed line for the ear
    c = pathlib.Path.home() / "Desktop/suno_test/eu_v8_final"; c.mkdir(parents=True, exist_ok=True)
    for k in ("L10", "L16", "L20", "L24", "L40"):
        a, b = src[k]["span"]
        a = src["L9"]["span"][0] if k == "L10" else a
        name = f"{k if k != 'L10' else 'L9-10'} v8 - {src[k]['text'] if k != 'L10' else 'Trapped in the Brussels room, where the faxes zoom'}"
        sf.write(c / f"{name}.wav", out[:, int((a - 1.0) * V.SR):int((b + 1.0) * V.SR)].T, V.SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", c / f"{name}.wav", "-b:a", "256k", c / f"{name}.mp3"], check=True)
        (c / f"{name}.wav").unlink()
    print("done")
