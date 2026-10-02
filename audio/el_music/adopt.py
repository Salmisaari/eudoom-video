"""Adopt the EU lyrics: for each changed stretch pick the (take, cut-in, cut-out) that Whisper hears closest
to the EU text, splice only those stretches into the original, and write the full song + a report."""
import difflib, json, pathlib, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf, scipy.signal as ss

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "audio/el_music"
sys.path.insert(0, str(ROOT / "analysis"))
import common  # noqa: F401
import mlx_whisper

SR = 44100
XF = int(0.03 * SR)
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_lyrics"
TAKES = sorted(HERE.glob("eu_take*.mp3"))

# changed stretches on the original timeline: (start, end, EU text sung there, words that must be gone)
RUNS = [
    (22.76, 24.32, "I'm upping EU doom", ["pdoom", "mypee"]),
    (26.32, 29.91, "Trapped in the notary's room where the faxes zoom", ["chinese", "shrooms"]),
    (59.13, 64.10, "I'm upping EU doom I hear the basic income boom Nokia to the moon", ["basilisk", "nvda", "pdoom"]),
    (66.22, 69.76, "One to thirty faxes a second", ["flops"]),
    (85.00, 96.84, "Without a single GDPR NATO please don't let me go I'm upping EU doom", ["cdr", "gato", "pdoom"]),
    (98.82, 100.72, "EU switch all on PTO", ["killswitch"]),
    (105.96, 109.90, "Euro originality thesis blues", ["orthogonality"]),  # keep the whole held "blues"
    (120.76, 126.12, "ASML sales through the roof I'm upping EU doom", ["rlhf", "askew", "pdoom"]),
    (132.02, 136.94, "What did Draghi see We'll never know", ["ilya"]),
]
IN = (-0.30, -0.20, -0.10, 0.0)
OUT = (-0.10, 0.0, 0.10)


def load(p):
    y, _ = librosa.load(p, sr=SR, mono=False)
    return y


orig = load(ROOT / "audio/pdoom.mp3")


def aligned(p):
    """Take shifted and gain-matched to the original (measured on 40-58 s, which no edit touches)."""
    y = load(p)
    a, b, m = int(40 * SR), int(52 * SR), 4410
    lag = int(np.argmax(ss.correlate(y.mean(0)[a - m:b + m], orig.mean(0)[a:b], "valid"))) - m
    y = np.roll(y, -lag, axis=1)[:, : orig.shape[1]]
    y = np.pad(y, ((0, 0), (0, orig.shape[1] - y.shape[1])))
    return y * orig[:, a:b].std() / y[:, a:b].std()


takes = {p.stem: aligned(p) for p in TAKES}


def splice(base, new, t_in, t_out):
    w = np.zeros(base.shape[1])
    i0, i1, h = int(t_in * SR), int(t_out * SR), XF // 2
    w[i0:i1] = 1
    w[i0 - h:i0 - h + XF] = np.linspace(0, 1, XF)
    w[i1 - h:i1 - h + XF] = np.linspace(1, 0, XF)
    out = base.copy()
    j0, j1 = i0 - h, i1 - h + XF
    out[:, j0:j1] = base[:, j0:j1] * np.cos(w[j0:j1] * np.pi / 2) + new[:, j0:j1] * np.sin(w[j0:j1] * np.pi / 2)
    return out


def hear(y, a, b):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, librosa.resample(y.mean(0)[int(a * SR):int(b * SR)], orig_sr=SR, target_sr=16000), 16000)
        return mlx_whisper.transcribe(f.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


flat = lambda s: "".join(c for c in s.lower() if c.isalnum())


def score(txt, want, gone):
    s = difflib.SequenceMatcher(None, flat(txt), flat(want)).ratio()
    return s - 0.3 * sum(g in flat(txt) for g in gone)


# REDO=5,7 re-selects only those runs (0-based) and keeps the other choices from the last report
redo = {int(x) for x in __import__("os").environ.get("REDO", "").split(",") if x}
prev = json.loads((HERE / "adopt_report.json").read_text()) if redo else []
out, report = orig.copy(), []
for ri, (s, e, want, gone) in enumerate(RUNS):
    if redo and ri not in redo:
        best = prev[ri]
        out = splice(out, takes[best["take"]], best["t_in"], best["t_out"])
        report.append(best)
        continue
    best = None
    for name, y in takes.items():
        for di in IN:
            for do in OUT:
                cand = splice(orig, y, s + di, e + do)
                txt = hear(cand, s - 0.3, e + 0.3)
                sc = score(txt, want, gone)
                if best is None or sc > best["score"]:
                    best = dict(start=s, end=e, take=name, t_in=round(s + di, 2), t_out=round(e + do, 2),
                                score=round(sc, 3), heard=txt, want=want)
    out = splice(out, takes[best["take"]], best["t_in"], best["t_out"])
    report.append(best)
    print(f"{s:6.2f}-{e:6.2f} {best['take']} cut {best['t_in']}-{best['t_out']} score {best['score']:.2f} | "
          f"heard: {best['heard']}  | want: {want}", flush=True)

DESK.mkdir(parents=True, exist_ok=True)
wav = HERE / "pdoom_EU.wav"
sf.write(wav, out.T, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "320k", DESK / "pdoom_EU_edition.mp3"], check=True)
(HERE / "adopt_report.json").write_text(json.dumps(report, indent=1))
d = np.abs(out - orig).max(0)
changed = np.flatnonzero(d > 1e-5) / SR
print(f"changed audio: {len(changed) / SR:.1f} s in total, everything else sample-identical")
