"""v12 = v11 (final16.py) with the user's pick of 1 Oct 2026 from "eu_v11_L9-10 - all versions":
  L9-10v16 "Trapped in the Brussels room, where the faxes zoom"  eu30_17, both lines as one span, untouched on the
           BS-RoFormer split, centre/sides levelled (l910_r30.py, exactly as the clip was built)
  L18      fix C from "eu_v12_L18 - EU doom fix" (l18_fix.py): v5's cut into the held "my" (59.96 s) left "my" fading
           20 ms early and the E of "EU" weak and phasey; the original's "my" held to its end, the E's first 90 ms
           from L7's hook (80 beats earlier), then L18's own "EU doom"
Writes pdoom_EU_v12.wav, audio/pdoom_eu.mp3 (v11 kept as pdoom_EU_v11.wav), the Desktop copy, v12_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
from final13 import hooked, VO_R, ms
import final12, l910, l18_fix

TAKE = "eu30_17"

if __name__ == "__main__":
    v11 = librosa.load(HERE / "pdoom_EU_v11.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    src = json.loads((HERE / "v11_sources.json").read_text())
    Y = hooked(ms(None, l910.N), l910.N, TAKE, l910.PLAN, "bsroformer", VO_R)
    out, span = paste(v11, Y, *bounds(l910.N))
    desc = f"{TAKE} both lines as one span, untouched (bsroformer, centre/sides levelled): L9-10v16"
    src["L9"] = dict(source=desc, span=[round(float(t), 3) for t in span], text="Trapped in the Brussels room,")
    src["L10"] = dict(source=desc, span=[round(float(t), 3) for t in span], text="where the faxes zoom")
    spans = [("L9-10", span)]
    out, span18 = l18_fix.fix(out, "C")
    src["L18"] = dict(source="v7: v5, with 'my' held to its end and the E onset from L7 (l18_fix C)",
                      span=src["L18"]["span"], text=src["L18"]["text"], repair=[round(float(t), 3) for t in span18])
    spans.append(("L18", span18))
    sf.write(HERE / "pdoom_EU_v12.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v12.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v12"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v12.wav", "-b:a", "320k", d / "pdoom_EU_edition_v12.mp3"], check=True)
    (HERE / "v12_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool)
    for _, (a, b) in spans:
        mask[int((a - 0.03) * V.SR):int((b + 0.03) * V.SR)] = False
    print(f"outside the changed spans vs v11: max |diff| {np.abs(out - v11)[:, mask].max():.1e}")
    for name, sp in spans:
        for t in sp:
            print(f"  {name} seam {t:.3f}: {final12.seam_db(out, v11, t):+.1f} dB vs v11, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
