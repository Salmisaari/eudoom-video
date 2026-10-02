"""v9 = v8 (final13.py) with only L25 replaced: the user heard v7's "Now privacy in chats obsolete" as chopped.
Measured (l25_scan.py, BS-RoFormer split, Praat f0): the original sings "von Neumann's" legato (voiced 89 % of
78.15-80.05 s, one gap: the s before "obsolete"); v7's eu12_3 insert is voiced 69 % with four gaps of 90-180 ms and
two joins inside continuous singing. eu12_8 whole line (L25I in eu_v8_lines): voiced 89 %, its only gap the "ts" of
"chats" where the original has its s; within 20 ms, 10 cents and 1 dB of the original on every word.
RoFormer split, centre/sides levelled (round 6). Writes pdoom_EU_v9.wav, audio/pdoom_eu.mp3, the Desktop copy,
v9_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
from final13 import hooked, VO_R, ms
import final12
from l25_fix import P25

if __name__ == "__main__":
    v8 = librosa.load(HERE / "pdoom_EU_v8.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    Y = hooked(ms(None, 25), 25, "eu12_8", P25, "bsroformer", VO_R)
    out, span = paste(v8, Y, *bounds(25))
    src = json.loads((HERE / "v8_sources.json").read_text())
    src["L25"] = dict(source="eu12_8 whole line (bsroformer, centre/sides levelled): L25I", span=list(span),
                      text="Now privacy in chats obsolete")
    sf.write(HERE / "pdoom_EU_v9.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v9.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v9"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v9.wav", "-b:a", "320k", d / "pdoom_EU_edition_v9.mp3"], check=True)
    (HERE / "v9_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool); mask[int((span[0] - 0.03) * V.SR):int((span[1] + 0.03) * V.SR)] = False
    print(f"outside L25 vs v8: max |diff| {np.abs(out - v8)[:, mask].max():.1e}")
    for t in span:
        print(f"  seam {t:.3f}: {final12.seam_db(out, v8, t):+.1f} dB vs v8, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
    a, b = span
    sf.write(d / "L25 v9.wav", out[:, int((a - 1.5) * V.SR):int((b + 1.0) * V.SR)].T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", d / "L25 v9.wav", "-b:a", "256k", d / "L25 v9 - Now privacy in chats obsolete.mp3"], check=True)
    (d / "L25 v9.wav").unlink()
