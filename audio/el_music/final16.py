"""v11 = v10 (final15.py) with L35 back to the original "Just transformers all the way!" (the user, 1 Oct 2026: the
picture becomes a unicorn factory, transformers making the new companies, so the line goes back to transformers).
Writes pdoom_EU_v11.wav, audio/pdoom_eu.mp3 (v10 kept as pdoom_EU_v10.wav), the Desktop copy, v11_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
import final12

if __name__ == "__main__":
    v10 = librosa.load(HERE / "pdoom_EU_v10.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    out, span = paste(v10, V.mix, *bounds(35))
    src = json.loads((HERE / "v10_sources.json").read_text())
    src.pop("L35", None)
    print(f"L35 original: {span[0]:.3f}-{span[1]:.3f}")
    sf.write(HERE / "pdoom_EU_v11.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v11.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v11"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v11.wav", "-b:a", "320k", d / "pdoom_EU_edition_v11.mp3"], check=True)
    (HERE / "v11_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool); mask[int((span[0] - 0.03) * V.SR):int((span[1] + 0.03) * V.SR)] = False
    print(f"outside L35 vs v10: max |diff| {np.abs(out - v10)[:, mask].max():.1e}")
    for t in span:
        print(f"  seam {t:.3f}: {final12.seam_db(out, v10, t):+.1f} dB vs v10, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
