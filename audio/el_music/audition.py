"""Per-line audition set: every changed line from every round-2 take, spliced into the original on that
line's own boundaries (locally re-aligned), with 1 s of original context either side.
Writes ~/Desktop/suno_test/eu_lines/<Lnn>/<Lnn>_Tnn.mp3, <Lnn>_all.mp3 (original first) and index.txt."""
import json, pathlib, subprocess
import numpy as np, librosa, scipy.signal as ss

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "audio/el_music"
OUT = pathlib.Path.home() / "Desktop/suno_test/eu_lines"
SR, XF, CTX = 44100, int(0.03 * 44100), 1.0

L = json.loads((ROOT / "data/lyrics.json").read_text())["lines"]
NEW = {7: "I'm upping EU doom", 9: "Trapped in the Brussels room", 10: "Where the faxes zoom",
       18: "I'm upping EU doom", 19: "I hear the basic income boom", 20: "A-S-M-L to the moon",
       22: "One E thirty forms a second", 27: "Without a single GDPR", 28: "NATO, please don't let me go",
       29: "I'm upping EU doom", 31: "EU guy's on PTO", 34: "Euro-banality thesis blues",
       40: "The AI Act goes askew", 41: "I'm upping EU doom", 45: "What did Draghi see? We'll never know"}
END_FIX = {34: 109.90}  # keep the held "blues"
LINES = [(n, L[n - 1]["start"], END_FIX.get(n, L[n]["start"])) for n in NEW]

order = [f"eu2_{s}{k}" for s, r in (("high", 4), ("medium", 4), ("low", 15)) for k in range(1, r + 1)]
TAKES = {f"T{i:02d}": name for i, name in enumerate(order, 1)}

orig = librosa.load(ROOT / "audio/pdoom.mp3", sr=SR, mono=False)[0]


def mp3(y, path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-b:a", "224k", str(path)], input=np.ascontiguousarray(y.T, dtype=np.float32).tobytes(), check=True)


def local_lag(y, a, b, m=int(0.06 * SR)):
    x = orig.mean(0)[int((a - 1.5) * SR):int((b + 1.5) * SR)]
    seg = y.mean(0)[int((a - 1.5) * SR) - m:int((b + 1.5) * SR) + m]
    return int(np.argmax(ss.correlate(seg, x, "valid"))) - m


def clip(new, a, b):
    """Original with [a, b] taken from `new` (equal-power 30 ms crossfades), cut to [a-CTX, b+CTX]."""
    c0, c1 = int((a - CTX) * SR), int((b + CTX) * SR)
    w = np.zeros(c1 - c0)
    i0, i1, h = int(a * SR) - c0, int(b * SR) - c0, XF // 2
    w[i0:i1] = 1
    w[i0 - h:i0 - h + XF] = np.linspace(0, 1, XF)
    w[i1 - h:i1 - h + XF] = np.linspace(1, 0, XF)
    return orig[:, c0:c1] * np.cos(w * np.pi / 2) + new[:, c0:c1] * np.sin(w * np.pi / 2)


clips = {n: {"T00": orig[:, int((a - CTX) * SR):int((b + CTX) * SR)]} for n, a, b in LINES}
lags = {}
for tid, name in TAKES.items():
    y = librosa.load(HERE / f"{name}.mp3", sr=SR, mono=False)[0]
    y = np.pad(y, ((0, 0), (0, max(0, orig.shape[1] - y.shape[1]))))[:, : orig.shape[1]]
    g = orig[:, int(40 * SR):int(52 * SR)].std() / y[:, int(40 * SR):int(52 * SR)].std()
    for n, a, b in LINES:
        lag = local_lag(y, a, b)
        lags[f"L{n:02d}_{tid}"] = round(lag / SR * 1000, 1)
        clips[n][tid] = clip(np.roll(y, -lag, axis=1) * g, a, b)
    print(tid, name, flush=True)

OUT.mkdir(parents=True, exist_ok=True)
gap = np.zeros((2, int(0.6 * SR)), dtype=np.float32)
index = ["Each line: <Lnn>_all.mp3 plays the original (T00) then T01..T23, 0.6 s apart. Single clips: <Lnn>_Tnn.mp3.",
         "Takes: " + ", ".join(f"{t}={n.replace('eu2_', '')}" for t, n in TAKES.items()), ""]
for n, a, b in LINES:
    d = OUT / f"L{n:02d}"
    d.mkdir(exist_ok=True)
    reel, t, marks = [], 0.0, []
    for tid, c in clips[n].items():
        if tid != "T00":
            mp3(c, d / f"L{n:02d}_{tid}.mp3")
        marks.append(f"{tid}@{int(t // 60)}:{t % 60:04.1f}")
        reel += [c, gap]
        t += c.shape[1] / SR + 0.6
    mp3(np.concatenate(reel, 1), d / f"L{n:02d}_all.mp3")
    index.append(f"L{n:02d}  {a:6.2f}-{b:6.2f}  was: {L[n - 1]['text']!r:42s} now: {NEW[n]!r}")
    index.append("      " + " ".join(marks))
(OUT / "index.txt").write_text("\n".join(index) + "\n")
(HERE / "audition_lags.json").write_text(json.dumps(lags, indent=1))
print("\n".join(index))
