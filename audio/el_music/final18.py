"""v13 = v12 (final17.py) with the user's pick of 1 Oct 2026 from "eu_v12_L37 - all versions":
  L37v24 "Post-AI-bubble, super-dense"  eu33_3 (round 33, spelled "Post-Ay-Eye bubble"), the whole line untouched on
         the BS-RoFormer split, centre/sides levelled (line_round.py, exactly as the clip was built)
and L17's text as sung since v5: "Cookies, please, please let me free".
Writes pdoom_EU_v13.wav, audio/pdoom_eu.mp3 (v12 kept as pdoom_EU_v12.wav), the Desktop copy, v13_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
from final13 import hooked, VO_R, ms
import final12

TAKE, N = "eu33_3", 37

if __name__ == "__main__":
    v12 = librosa.load(HERE / "pdoom_EU_v12.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    src = json.loads((HERE / "v12_sources.json").read_text())
    old = " ".join(w["w"] for w in V.LYR[N - 1]["words"]).upper()
    plan = (V.ALL_WORDS(N), old, "POST AY EYE BUBBLE SUPER DENSE", "Post-AI-bubble, super-dense")
    Y = hooked(ms(None, N), N, TAKE, plan, "bsroformer", VO_R)
    out, span = paste(v12, Y, *bounds(N))
    src["L37"] = dict(source=f"{TAKE} whole line, spelled 'Post-Ay-Eye bubble' (bsroformer, centre/sides levelled): L37v24",
                      span=[round(float(t), 3) for t in span], text="Post-AI-bubble, super-dense")
    src["L17"]["text"] = "Cookies, please, please let me free"
    sf.write(HERE / "pdoom_EU_v13.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v13.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v13"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v13.wav", "-b:a", "320k", d / "pdoom_EU_edition_v13.mp3"], check=True)
    (HERE / "v13_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool); mask[int((span[0] - 0.03) * V.SR):int((span[1] + 0.03) * V.SR)] = False
    print(f"outside L37 vs v12: max |diff| {np.abs(out - v12)[:, mask].max():.1e}")
    for t in span:
        print(f"  L37 seam {t:.3f}: {final12.seam_db(out, v12, t):+.1f} dB vs v12, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
