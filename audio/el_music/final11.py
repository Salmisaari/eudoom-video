"""Assemble v7 from the original, line by line (after the user's review of animatic_v6):
- the lines they approved stay exactly as heard: copied from v5 / v4 / v3 / v6 on the same quiet-point seams;
- L10 "where the faxes zoom": v3's take re-spliced vocal-only (v3 had pasted the take's own band, whose drums
  jumped at the seam before "where"); warped and tuned onto the original melody;
- L23 "That was fast enough, we reckoned" (new), L25 "Now privacy in chats obsolete", L40 "EU Inc fixes things soon"
  (the v6 take sang extra words into the held note): round 12-13 picks, see PICKS;
- L26 and L37 are the original again (the user moved them back).
Seams: v6's paste() used an equal-power crossfade between signals that share the band, so every seam swelled +2..+6 dB
for ~40 ms (v4/v5, built vocal-only, were flat). Here the crossfade is power-preserving for the measured correlation
of the two sides (amplitude-complementary when they share the band), and v6's lines are rebuilt from their takes rather
than copied with v6's bumps in them.
Writes pdoom_EU_v7.wav, audio/pdoom_eu.mp3, the Desktop copy and v7_sources.json."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from final10 import SRC, O, V, R, PLANS, cost, bounds, quiet, ver, ROOT

v6 = json.loads((HERE / "v6_sources.json").read_text())
KEEP = {7: "v5", 9: "v5", 17: "v5", 18: "v5", 22: "v5", 29: "v5", 31: "v5", 27: "v3", 45: "v3", 20: "v4"}
V6 = (16, 19, 24, 34, 35, 41)  # rebuilt exactly as v6 built them (take, rendition, separation from v6_sources.json)


def paste(out, src, a, b, xf=0.04):
    """src over out on [a, b] (moved to the quietest vocal point), crossfaded power-neutrally for the two sides'
    correlation r: gains cos, sin scaled by 1/sqrt(1 + 2 r cos sin) (r = 1: amplitude-complementary; r = 0: equal-power)."""
    a, b = quiet(a), quiet(b)
    w = np.zeros(out.shape[1]); i0, i1, k = int(a * V.SR), int(b * V.SR), int(xf * V.SR)
    w[i0:i1] = 1
    res = out.copy()
    for i, up in ((i0, True), (i1, False)):
        s0 = i - k // 2
        x, y = out[:, s0:s0 + k].mean(0), src[:, s0:s0 + k].mean(0)
        r = float(np.clip(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12), 0, 1))
        w[s0:s0 + k] = np.linspace(0, 1, k) if up else np.linspace(1, 0, k)
        c, s = np.cos(w[s0:s0 + k] * np.pi / 2), np.sin(w[s0:s0 + k] * np.pi / 2)
        g = 1 / np.sqrt(1 + 2 * r * c * s)
        res[:, s0:s0 + k] = out[:, s0:s0 + k] * c * g + src[:, s0:s0 + k] * s * g
    res[:, i0 + k // 2:i1 - k // 2] = src[:, i0 + k // 2:i1 - k // 2]
    return res, (round(a, 3), round(b, 3))
# line: (take, rendition, separation or None = the cleaner of the two), picked in select10/final_select/l40_eval
PICKS = {23: ("eu12_9", "warp", None),          # Whisper: "That was fast enough we reckoned", 100 % on the melody
         25: ("eu12_3", "nowarp", None),        # best of 20 "privacy in chats" takes: 94 %, no ghost; Whisper hears "...seeing chats"
         40: ("eu13_7", "nowarp+tune", "htdemucs_ft")}  # holds "soon" like the original holds "askew"; no words sung into it
L10 = ("eu2_low3", (V.ALL_WORDS(10), "WITH A BAG OF SHROOMS", "WHERE THE FAXES ZOOM", "where the faxes zoom"), dict(sep="htdemucs", warp_on=True, tune=True))


def swap(take, plan, n, **kw):
    V.PLAN[n] = plan
    return V.apply(V.mix, V.VO, V.build(V.load_take(take), n, **kw))[0]


def best_sep(take, plan, n, kind):
    builds = {sep: swap(take, plan, n, sep=sep, warp_on=kind.startswith("warp"), tune="tune" in kind) for sep in ("htdemucs", "htdemucs_ft")}
    scores = {sep: cost(R.line_metrics(Y, V.mix, n)) for sep, Y in builds.items()}
    sep = min(scores, key=scores.get)
    return builds[sep], f"{take} {kind} ({sep})"


if __name__ == "__main__":
    sel = json.loads((HERE / "select10.json").read_text())
    out, sources = O.copy(), {}
    for n, v in KEEP.items():
        out, span = paste(out, SRC[v], *bounds(n))
        sources[n] = dict(source=v, span=span, text="")
    for n in V6:
        take, kind, sep = v6[f"L{n}"]["source"].replace("(", "").replace(")", "").split()
        plan = next(p for takes, p in PLANS[n] if take in takes)
        out, span = paste(out, swap(take, plan, n, sep=sep, warp_on=kind.startswith("warp"), tune="tune" in kind), *bounds(n))
        sources[n] = dict(source=f"{take} {kind} ({sep}), as v6", span=span, text=v6[f"L{n}"]["text"])
    take, plan, kw = L10
    out, span = paste(out, swap(take, plan, 10, **kw), *bounds(10))
    sources[10] = dict(source=f"{take} warp+tune (htdemucs), vocal only", span=span, text=plan[3])
    for n, (take, kind, sep) in PICKS.items():
        plan = next(p for takes, p in PLANS[n] if take in takes)
        if sep:
            V.PLAN[n] = plan
            line, src = swap(take, plan, n, sep=sep, warp_on=kind.startswith("warp"), tune="tune" in kind), f"{take} {kind} ({sep})"
        else:
            line, src = best_sep(take, plan, n, kind)
        out, span = paste(out, line, *bounds(n))
        words = [w["w"] for w in V.LYR[n - 1]["words"]]
        sources[n] = dict(source=src, span=span, text=" ".join(words[: plan[0][0]] + [plan[3]] + words[plan[0][-1] + 1:]))
        print(f"L{n:02d} {src}: {sources[n]['text']}", flush=True)
    for n, s in sources.items():  # texts of the lines copied from v3-v5
        if not s["text"]:
            s["text"] = v6.get(f"L{n}", {}).get("text", "")
    sf.write(HERE / "pdoom_EU_v7.wav", out.T, V.SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v7.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v7"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v7.wav", "-b:a", "320k", d / "pdoom_EU_edition_v7.mp3"], check=True)
    (HERE / "v7_sources.json").write_text(json.dumps({f"L{n}": s for n, s in sorted(sources.items())}, indent=1))
    mask = np.ones(O.shape[1], bool)
    for s in sources.values():
        mask[int((s["span"][0] - 0.03) * V.SR):int((s["span"][1] + 0.03) * V.SR)] = False
    print(f"outside the changed lines: max |diff| {np.abs(out - O)[:, mask].max():.1e}")
