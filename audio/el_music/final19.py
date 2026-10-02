"""v14 = v13 (final18.py) with the user's pick of 1 Oct 2026 from the PICK folder:
  L7  L7 EUv1 (eu34_L7_5, round 34, spelled "ee-YOO"): only "EU doom" from the take, "I'm upping my" the original
      singer's as before, untouched on the BS-RoFormer split, centre/sides levelled (eu_glide.py, exactly as the clip)
L29 and L40 stay as in v13; L16 and L19 too, until the user picks among TUNED / M.
Writes pdoom_EU_v14.wav, audio/pdoom_eu.mp3 (v13 kept as pdoom_EU_v13.wav), the Desktop copy, v14_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
from final13 import hooked, VO_R, ms
import final12

TAKE, N = "eu34_L7_5", 7

if __name__ == "__main__":
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    src = json.loads((HERE / "v13_sources.json").read_text())
    old = " ".join(w["w"] for w in V.LYR[N - 1]["words"]).upper()
    plan = ([3], old, "I'M UPPING MY EE YOU DOOM", "I'm upping my EU doom")
    Y = hooked(ms(None, N), N, TAKE, plan, "bsroformer", VO_R)
    out, span = paste(v13, Y, *bounds(N))
    src["L7"] = dict(source=f"{TAKE} 'EU doom' only, sung ee-YOO (bsroformer, centre/sides levelled): L7 EUv1",
                     span=[round(float(t), 3) for t in span], text="I'm upping my EU doom")
    src["L17"]["text"] = "Cookies, please, please let me free"
    sf.write(HERE / "pdoom_EU_v14.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v14.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v14"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v14.wav", "-b:a", "320k", d / "pdoom_EU_edition_v14.mp3"], check=True)
    (HERE / "v14_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool); mask[int((span[0] - 0.03) * V.SR):int((span[1] + 0.03) * V.SR)] = False
    print(f"outside L7 vs v13: max |diff| {np.abs(out - v13)[:, mask].max():.1e}")
    for t in span:
        print(f"  L7 seam {t:.3f}: {final12.seam_db(out, v13, t):+.1f} dB vs v13, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
