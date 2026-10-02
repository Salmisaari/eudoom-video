"""v10 = v9 (final14.py) with the user's picks of 1 Oct 2026 (eu_v10_L11 / eu_v10_L12 / eu_v10_L25 folders):
  L11v5 "See through Pinocchio's lies"  eu27_5, whole line ("amazing")
  L12v3 "with Eurovision eyes"          eu27_3, whole line ("amazing")
  L25   back to the original "Now von Neumann's obsolete" (the user: "we could keep it, it's still a European
        reference"); v9's "Now privacy in chats obsolete" had sounded broken. (A take can still be passed:
        final15.py <take> "<text>" [fit], fit = sylfit.py onto the original's note onsets.)
Each line spliced alone on the RoFormer split, centre/sides levelled, as its clip. Writes pdoom_EU_v10.wav,
audio/pdoom_eu.mp3 (v9 kept as pdoom_EU_v9.wav), the Desktop copy, v10_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final11 import paste, V, ROOT
from final10 import bounds
from final13 import hooked, VO_R, ms
import final12
import sylfit

PICKS = {11: ("eu27_5", "SEE THROUGH THE SHOGGOTHS LIES", "See through Pinocchio's lies", False),
         12: ("eu27_3", "WITH YOUR SHINIGAMI EYES", "with Eurovision eyes", False)}

if __name__ == "__main__":
    if len(sys.argv) > 2:
        PICKS[25] = (sys.argv[1], "NOW VON NEUMANN'S OBSOLETE", sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "fit")
    v9 = librosa.load(HERE / "pdoom_EU_v9.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    out, src = v9.copy(), json.loads((HERE / "v9_sources.json").read_text())
    spans = []
    if 25 not in PICKS:  # the original singer again
        out, span = paste(out, V.mix, *bounds(25))
        spans.append(span)
        src.pop("L25", None)
        print(f"L25 original: {span[0]:.3f}-{span[1]:.3f}", flush=True)
    for n, (take, old, text, fit) in sorted(PICKS.items()):
        plan = (V.ALL_WORDS(n), old, text.upper().replace("'", ""), text)
        Y = hooked(ms(sylfit.fit(text, n) if fit else None, n), n, take, plan, "bsroformer", VO_R)
        out, span = paste(out, Y, *bounds(n))
        spans.append(span)
        src[f"L{n}"] = dict(source=f"{take} whole line{' fitted onto the original rhythm' if fit else ''} (bsroformer, centre/sides levelled)",
                            span=list(span), text=text)
        print(f"L{n} {text!r}: {take}, {span[0]:.3f}-{span[1]:.3f}", flush=True)
    sf.write(HERE / "pdoom_EU_v10.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v10.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v10"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v10.wav", "-b:a", "320k", d / "pdoom_EU_edition_v10.mp3"], check=True)
    (HERE / "v10_sources.json").write_text(json.dumps(src, indent=1))
    mask = np.ones(out.shape[1], bool)
    for a, b in spans:
        mask[int((a - 0.03) * V.SR):int((b + 0.03) * V.SR)] = False
    print(f"outside the new lines vs v9: max |diff| {np.abs(out - v9)[:, mask].max():.1e}")
    for a, b in spans:
        for t in (a, b):
            print(f"  seam {t:.3f}: {final12.seam_db(out, v9, t):+.1f} dB vs v9, {final12.seam_db(out, V.mix, t):+.1f} dB vs original")
