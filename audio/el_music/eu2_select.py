"""EU lyrics, round 2 selection: per changed stretch, pick the take whose SUNG PERFORMANCE matches the
original (pitch curve and voicing timing of the separated vocal), provided Whisper hears the new words.
Splices only those stretches into the original. Also scores round 1 (pdoom_EU.wav) for comparison."""
import difflib, json, pathlib, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf, scipy.signal as ss, torch

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "audio/el_music"
sys.path.insert(0, str(ROOT / "analysis"))
import common  # noqa: F401
import mlx_whisper
from demucs.pretrained import get_model
from demucs.apply import apply_model

SR = 44100
XF = int(0.03 * SR)
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_lyrics_v2"
RUNS = [
    (22.76, 24.32, "I'm upping EU doom", ["pdoom", "mypee"]),
    (26.32, 29.91, "Trapped in the Brussels room where the faxes zoom", ["chinese", "shrooms"]),
    (59.13, 64.10, "I'm upping EU doom I hear the basic income boom ASML to the moon", ["basilisk", "nvda"]),
    (66.22, 69.76, "One E thirty forms a second", ["flops"]),
    (85.00, 96.84, "Without a single GDPR NATO please don't let me go I'm upping EU doom", ["cdr", "gato"]),
    (98.82, 100.72, "EU guy's on PTO", ["killswitch"]),
    (105.96, 109.90, "Euro banality thesis blues", ["orthogonality"]),
    (120.76, 126.12, "The AI Act goes askew I'm upping EU doom", ["rlhf"]),
    (132.02, 136.94, "What did Draghi see We'll never know", ["ilya"]),
]

# the new words themselves must be heard (any listed spelling of each group, in Whisper's flattened text)
EUDOOM = ["eudoom", "udoom", "youdoom", "eudom"]
KEYS = [
    [EUDOOM],
    [["brussel"], ["fax"]],
    [EUDOOM, ["basicincome"], ["asml"]],
    [["forms"], ["thirty", "30"]],
    [["gdpr"], ["nato"], EUDOOM],
    [["euguy", "youguy"], ["pto"]],
    [["eurobanality", "europanality", "yourobanality", "yurobanality"]],
    [["aiact", "aact", "eyeact"], ["askew"], EUDOOM],
    [["draghi", "dragi", "draggy", "drahgi"]],
]

orig = librosa.load(ROOT / "audio/pdoom.mp3", sr=SR, mono=False)[0]


def aligned(p):
    y = librosa.load(p, sr=SR, mono=False)[0]
    a, b, m = int(40 * SR), int(52 * SR), 4410
    lag = int(np.argmax(ss.correlate(y.mean(0)[a - m:b + m], orig.mean(0)[a:b], "valid"))) - m
    y = np.roll(y, -lag, axis=1)[:, : orig.shape[1]]
    y = np.pad(y, ((0, 0), (0, orig.shape[1] - y.shape[1])))
    return y * orig[:, a:b].std() / y[:, a:b].std()



dev = "mps" if torch.backends.mps.is_available() else "cpu"
model = get_model("htdemucs").eval()
VOC = model.sources.index("vocals")


def vocals(y, a, b):
    """Separated vocal (mono, 22.05 kHz) of y over [a-1, b+1] s; returns (signal, t0)."""
    seg = torch.tensor(y[:, int((a - 1) * SR):int((b + 1) * SR)], dtype=torch.float32)
    with torch.no_grad():
        out = apply_model(model, seg[None], device=dev, split=True, overlap=0.25, progress=False)[0, VOC]
    return librosa.resample(out.mean(0).cpu().numpy(), orig_sr=SR, target_sr=22050), a - 1


def f0(v):
    f, voiced, _ = librosa.pyin(v, fmin=100, fmax=1000, sr=22050, frame_length=2048, hop_length=256)
    return f, voiced


def performance(y, a, b, ref):
    """Pitch error (cents, octave-safe median) and voicing IoU of y's vocal vs the reference contour."""
    v, t0 = vocals(y, a, b)
    f, vo = f0(v)
    rf, rvo = ref
    n = min(len(f), len(rf))
    t = t0 + np.arange(n) * 256 / 22050
    w = (t >= a) & (t < b)
    both, either = w & vo[:n] & rvo[:n], w & (vo[:n] | rvo[:n])
    c = 1200 * np.log2(f[:n][both] / rf[:n][both])
    err = float(np.median(np.abs((c + 600) % 1200 - 600))) if both.any() else 999.0
    return err, float(both.sum() / max(either.sum(), 1))


def splice(base, new, a, b):
    w = np.zeros(base.shape[1])
    i0, i1, h = int(a * SR), int(b * SR), XF // 2
    w[i0:i1] = 1
    w[i0 - h:i0 - h + XF] = np.linspace(0, 1, XF)
    w[i1 - h:i1 - h + XF] = np.linspace(1, 0, XF)
    j0, j1 = i0 - h, i1 - h + XF
    out = base.copy()
    out[:, j0:j1] = base[:, j0:j1] * np.cos(w[j0:j1] * np.pi / 2) + new[:, j0:j1] * np.sin(w[j0:j1] * np.pi / 2)
    return out


def hear(y, a, b):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, librosa.resample(y.mean(0)[int(a * SR):int(b * SR)], orig_sr=SR, target_sr=16000), 16000)
        return mlx_whisper.transcribe(f.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


flat = lambda s: "".join(c for c in s.lower() if c.isalnum())


def words(txt, want, gone):
    return difflib.SequenceMatcher(None, flat(txt), flat(want)).ratio() - 0.3 * sum(g in flat(txt) for g in gone)


if __name__ == "__main__":
    takes = {p.stem: aligned(p) for p in sorted(HERE.glob("eu2_*.mp3"))}
    round1 = librosa.load(HERE / "pdoom_EU.wav", sr=SR, mono=False)[0]
    # scale: codec-only take vs original on an untouched stretch
    v, t0 = vocals(orig, 44.0, 48.0)
    ctl = performance(next(iter(takes.values())), 44.0, 48.0, f0(v))
    print(f"control (untouched 44-48 s, codec only): pitch err {ctl[0]:.0f}c, voicing IoU {ctl[1]:.2f}", flush=True)

    cache_f = HERE / "eu2_cache.json"
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    out, report = orig.copy(), []
    for (s, e, want, gone), keys in zip(RUNS, KEYS):
        ref = f0(vocals(orig, s, e)[0])
        r1 = performance(round1, s, e, ref)
        rows = []
        for name, y in takes.items():
            key = f"{name}@{s}-{e}|{want}"
            if key not in cache:
                cand = splice(orig, y, s, e)
                err, iou = performance(y, s, e, ref)
                txt = hear(cand, s - 0.3, e + 0.3)
                cache[key] = dict(take=name, err=round(err), iou=round(iou, 2), words=round(words(txt, want, gone), 2), heard=txt)
                cache_f.write_text(json.dumps(cache, indent=1))
            rows.append(cache[key])
        # the melody must hold (pitch within 60 cents, voicing overlap >= 0.7); then the clearest words win
        for r in rows:
            r["keys"] = round(sum(any(k in flat(r["heard"]) for k in g) for g in keys) / len(keys), 2)
        held = [r for r in rows if r["err"] <= 60 and r["iou"] >= 0.7]
        best = max(held or rows, key=lambda r: (r["keys"], r["words"]) if held else (r["keys"] - r["err"] / 300, r["words"]))
        best = dict(best, melody_ok=bool(held), words_ok=best["keys"] == 1)
        out = splice(out, takes[best["take"]], s, e)
        report.append(dict(start=s, end=e, want=want, round1_err=round(r1[0]), round1_iou=round(r1[1], 2), **best,
                           all=rows))
        flag = "OK  " if best["melody_ok"] and best["words_ok"] else "MISS"
        print(f"{flag} {s:6.2f}-{e:6.2f} {best['take']:12s} pitch err {best['err']:4d}c IoU {best['iou']:.2f} "
              f"(round 1: {r1[0]:.0f}c {r1[1]:.2f}) keys {best['keys']:.2f} words {best['words']:.2f} | {best['heard']}", flush=True)

    DESK.mkdir(parents=True, exist_ok=True)
    wav = HERE / "pdoom_EU_v2.wav"
    sf.write(wav, out.T, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "320k", DESK / "pdoom_EU_edition_v2.mp3"], check=True)
    (HERE / "eu2_report.json").write_text(json.dumps(report, indent=1))

    gap, reel, idx, t = np.zeros((2, int(0.8 * SR)), dtype="float32"), [], [], 0.0
    for r in report:
        a, b = r["start"] - 1.0, r["end"] + 1.5
        for lab, y in (("original", orig), ("EU v2", out)):
            c = y[:, int(a * SR):int(b * SR)]
            idx.append(f"{int(t // 60)}:{t % 60:04.1f}  {lab:8s} {r['want'] if lab != 'original' else ''}")
            reel += [c, gap]
            t += c.shape[1] / SR + 0.8
        reel.append(gap)
        t += 0.8
    sf.write(HERE / "eu2_reel.wav", np.concatenate(reel, 1).T, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE / "eu2_reel.wav", "-b:a", "256k",
                    DESK / "changes_before_after.mp3"], check=True)
    (DESK / "changes_before_after.txt").write_text("\n".join(idx) + "\n")
    print("wrote", DESK)
