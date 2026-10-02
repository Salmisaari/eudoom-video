"""Assemble the EU song line by line from the original: every changed line comes from its chosen source -- a
version the user approved by ear (copied exactly), or round 10's pick (select10.json, rebuilt with htdemucs_ft).
Seams sit at the quietest point of the original vocal near each line edge (40 ms equal-power).
Writes audio/el_music/pdoom_EU_v6.wav, audio/pdoom_eu.mp3, the Desktop copy, and v6_sources.json."""
import json, os, pathlib, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import vsplice as V
from select10 import PLANS, fullmix, cost
import review as R

SR = V.SR
O = V.mix
ver = lambda p: librosa.load(p, sr=SR, mono=False)[0][:, : O.shape[1]]
SRC = {"v5": ver(HERE / "pdoom_EU_v5.wav"), "v4": ver("/tmp/pdoom_eu_v4.mp3"), "v3": ver(HERE / "pdoom_EU_v3.wav")}
# the user's verdicts on animatic_v5 (and earlier): keep what they called good, restore what was better before
KEEP = {7: "v5", 9: "v5", 17: "v5", 18: "v5", 22: "v5", 29: "v5", 31: "v5",  # good in v5
        10: "v3", 27: "v3", 45: "v3",  # "before it was good": where the faxes zoom, GDPR, Draghi
        20: "v4"}                       # "ASML to the moon was before good"
TEXT = {7: "I'm upping my EU doom", 9: "Trapped in the Brussels room,", 10: "where the faxes zoom",
        17: "Cookies, please let me free", 18: "I'm upping my EU doom", 20: "ASML to the moon",
        22: "One E thirty faxes a second", 27: "Without a single GDPR", 29: "I'm upping my EU doom,",
        31: "Brussels guy's on PTO", 45: "What did Draghi see? We'll never know"}


def bounds(n):
    return V.LYR[n - 1]["start"], (V.LYR[n]["start"] if n < len(V.LYR) else V.LYR[n - 1]["end"])


def quiet(t, lo=-0.08, hi=0.04):
    """Quietest 10 ms of the original vocal near t."""
    v = librosa.to_mono(V.VO[:, int((t + lo) * SR):int((t + hi) * SR)])
    e = np.convolve(v ** 2, np.ones(441) / 441, "same")
    return t + lo + np.argmin(e) / SR


def paste(out, src, a, b, xf=0.04):
    a, b = quiet(a), quiet(b)
    w = np.zeros(out.shape[1]); i0, i1, k = int(a * SR), int(b * SR), int(xf * SR)
    w[i0:i1] = 1; w[i0 - k // 2:i0 - k // 2 + k] = np.linspace(0, 1, k); w[i1 - k // 2:i1 - k // 2 + k] = np.linspace(1, 0, k)
    return out * np.cos(w * np.pi / 2) + src * np.sin(w * np.pi / 2), (round(a, 3), round(b, 3))


if __name__ == "__main__":
    sel = json.loads((HERE / "select10.json").read_text())
    out, sources = O.copy(), {}
    for n, v in KEEP.items():
        out, span = paste(out, SRC[v], *bounds(n))
        sources[n] = dict(source=v, span=span, text=TEXT[n])
    for n in sorted(map(int, sel)):
        best = sel[str(n)]["best"]
        plan = next(p for takes, p in PLANS[n] if best["take"] in takes)
        V.PLAN[n] = plan
        y = V.load_take(best["take"])
        if best["kind"] == "full":
            line = fullmix(y, n)
        else:  # the separation model changes how much of the take's own backing (old melody) comes along: keep the cleaner
            builds = {sep: V.apply(V.mix, V.VO, V.build(y, n, sep=sep, warp_on=best["kind"].startswith("warp"),
                                                        tune="tune" in best["kind"]))[0] for sep in ("htdemucs", "htdemucs_ft")}
            scores = {sep: cost(R.line_metrics(Y, V.mix, n)) for sep, Y in builds.items()}
            sep = min(scores, key=scores.get)
            line = builds[sep]
            best = dict(best, kind=f"{best['kind']} ({sep})")
        out, span = paste(out, line, *bounds(n))
        words = [w["w"] for w in V.LYR[n - 1]["words"]]
        text = " ".join(words[: plan[0][0]] + [plan[3]] + words[plan[0][-1] + 1:])
        sources[n] = dict(source=f"{best['take']} {best['kind']}", span=span, text=text)
        print(f"L{n:02d} {best['take']} {best['kind']}: {text}", flush=True)
    sf.write(HERE / "pdoom_EU_v6.wav", out.T, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v6.wav", "-b:a", "320k", ROOT / "audio/pdoom_eu.mp3"], check=True)
    d = pathlib.Path.home() / "Desktop/suno_test/eu_v6"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "pdoom_EU_v6.wav", "-b:a", "320k", d / "pdoom_EU_edition_v6.mp3"], check=True)
    (HERE / "v6_sources.json").write_text(json.dumps({f"L{n}": s for n, s in sorted(sources.items())}, indent=1))
    mask = np.ones(O.shape[1], bool)
    for s in sources.values():
        mask[int((s["span"][0] - 0.03) * SR):int((s["span"][1] + 0.03) * SR)] = False
    print(f"outside the changed lines: max |diff| {np.abs(out - O)[:, mask].max():.1e}")
