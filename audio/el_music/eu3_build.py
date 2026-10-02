"""Round 3: (1) for the lines the user approved, pick the round-2 take whose sung pitch curve matches the
original best (Whisper must hear the key word) and write a draft with only those lines changed;
(2) audition set for the re-generated lines (round-3 takes U01-U10) with the metric pick marked."""
import json, pathlib, subprocess, sys
import numpy as np, librosa, scipy.signal as ss

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_select import SR, XF, HERE, ROOT, orig, vocals, f0, performance, hear, flat

OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v3"
L = json.loads((ROOT / "data/lyrics.json").read_text())["lines"]
bounds = lambda n: (L[n - 1]["start"], {34: 109.90}.get(n, L[n]["start"]))

# line: (text, key spellings Whisper must produce)
APPROVED = {9: ("Trapped in the Brussels room", ["brussel"]), 10: ("Where the faxes zoom", ["fax"]),
            20: ("A-S-M-L to the moon", ["asml"]), 22: ("One E thirty forms a second", ["forms"]),
            27: ("Without a single GDPR", ["gdpr"]), 28: ("NATO, please don't let me go", ["nato"]),
            40: ("The AI Act goes askew", ["aiact", "aact", "eyeact", "askew"])}
HOOK = {"A": "I'm upping my EU doom", "B": "I'm upping my U-doom"}
REDO = {7: HOOK, 18: HOOK, 29: HOOK, 41: HOOK,
        19: {"A": "I hear the bazooka boom", "B": "I hear the basic income boom"},
        22: {"A": "One E thirty forms a second", "B": "One E thirty forms a second"},
        31: {"A": "Brussels guy's on PTO", "B": "Whole EU's on PTO"},
        45: {"A": "What did Draghi (DRAH-gee) see? We'll never know", "B": "What did Draghi see? We'll never know"}}
R2 = {f"T{i:02d}": n for i, n in enumerate(
    [f"eu2_{s}{k}" for s, r in (("high", 4), ("medium", 4), ("low", 15)) for k in range(1, r + 1)], 1)}
R3 = {f"U{i:02d}": f"eu3_{v}{k}" for i, (v, k) in enumerate([(v, k) for v in "AB" for k in range(1, 6)], 1)}

cache_f = HERE / "eu3_cache.json"
cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
refs = {}


def load(name):
    y = librosa.load(HERE / f"{name}.mp3", sr=SR, mono=False)[0]
    y = np.pad(y, ((0, 0), (0, max(0, orig.shape[1] - y.shape[1]))))[:, : orig.shape[1]]
    a, b = int(40 * SR), int(52 * SR)
    return y * orig[:, a:b].std() / y[:, a:b].std()


def local(y, a, b, m=int(0.06 * SR)):
    x = orig.mean(0)[int((a - 1.5) * SR):int((b + 1.5) * SR)]
    seg = y.mean(0)[int((a - 1.5) * SR) - m:int((b + 1.5) * SR) + m]
    return np.roll(y, -(int(np.argmax(ss.correlate(seg, x, "valid"))) - m), axis=1)


def splice_into(base, new, a, b):
    w = np.zeros(base.shape[1])
    i0, i1, h = int(a * SR), int(b * SR), XF // 2
    w[i0:i1] = 1
    w[i0 - h:i0 - h + XF] = np.linspace(0, 1, XF)
    w[i1 - h:i1 - h + XF] = np.linspace(1, 0, XF)
    j0, j1 = i0 - h, i1 - h + XF
    out = base.copy()
    out[:, j0:j1] = base[:, j0:j1] * np.cos(w[j0:j1] * np.pi / 2) + new[:, j0:j1] * np.sin(w[j0:j1] * np.pi / 2)
    return out


def score(tid, name, y, n, text, keys):
    a, b = bounds(n)
    key = f"{name}|L{n}|{text}"
    if key not in cache:
        if n not in refs:
            refs[n] = f0(vocals(orig, a, b)[0])
        yl = local(y, a, b)
        err, iou = performance(yl, a, b, refs[n])
        heard = hear(splice_into(orig, yl, a, b), a - 0.3, b + 0.3)
        cache[key] = dict(err=round(err), iou=round(iou, 2), heard=heard,
                          keys=any(k in flat(heard) for k in keys))
        cache_f.write_text(json.dumps(cache, indent=1))
    return dict(tid=tid, name=name, **cache[key])


def pick(rows):
    held = [r for r in rows if r["err"] <= 60 and r["iou"] >= 0.7] or rows
    return max(held, key=lambda r: (r["keys"], r["iou"] - r["err"] / 300))


def mp3(y, path, br="224k"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-b:a", br, str(path)], input=np.ascontiguousarray(y.T, dtype=np.float32).tobytes(), check=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    lines_out = []

    # (1) approved lines -> draft
    rows = {n: [] for n in APPROVED}
    for tid, name in R2.items():
        y = load(name)
        for n, (text, keys) in APPROVED.items():
            rows[n].append(score(tid, name, y, n, text, keys))
    draft, picks = orig.copy(), {}
    for n, (text, _) in APPROVED.items():
        best = pick(rows[n])
        a, b = bounds(n)
        draft = splice_into(draft, local(load(best["name"]), a, b), a, b)
        picks[n] = best
        lines_out.append(f"L{n:02d} {text!r:34s} -> {best['tid']} ({best['name']}): pitch {best['err']}c, "
                         f"IoU {best['iou']}, heard {best['heard']!r}")
    mp3(draft, OUT / "draft_approved_lines_only.mp3", "320k")
    print("\n".join(lines_out), flush=True)

    # (2) audition set for re-generated lines
    index = ["Round 3 takes: U01-U05 = variant A, U06-U10 = variant B. <Lnn>_all.mp3 = original, then U01..U10.", ""]
    gap = np.zeros((2, int(0.6 * SR)), dtype=np.float32)
    takes3 = {tid: load(name) for tid, name in R3.items()}
    for n, variants in REDO.items():
        a, b = bounds(n)
        d = OUT / f"L{n:02d}"
        d.mkdir(exist_ok=True)
        c0, c1 = int((a - 1) * SR), int((b + 1) * SR)
        reel, t, marks, rs = [orig[:, c0:c1], gap], (c1 - c0) / SR + 0.6, ["orig@0:00.0"], []
        for tid, y in takes3.items():
            v = "A" if tid <= "U05" else "B"
            text = variants[v]
            keys = [flat(w) for w in text.split("(")[0].split() if len(flat(w)) > 3][:2]
            rs.append(score(tid, R3[tid], y, n, text, keys))
            c = splice_into(orig, local(y, a, b), a, b)[:, c0:c1]
            mp3(c, d / f"L{n:02d}_{tid}.mp3")
            marks.append(f"{tid}@{int(t // 60)}:{t % 60:04.1f}")
            reel += [c, gap]
            t += c.shape[1] / SR + 0.6
        mp3(np.concatenate(reel, 1), d / f"L{n:02d}_all.mp3")
        best = pick(rs)
        index.append(f"L{n:02d}  A: {variants['A']!r}  B: {variants['B']!r}")
        index.append(f"      metric pick {best['tid']} (pitch {best['err']}c, IoU {best['iou']}, heard {best['heard']!r})")
        index.append("      " + " ".join(marks))
        print(index[-3], "\n", index[-2], flush=True)
    (OUT / "index.txt").write_text("Draft (approved lines only):\n" + "\n".join(lines_out) + "\n\n" + "\n".join(index) + "\n")
    (HERE / "eu3_picks.json").write_text(json.dumps({f"L{n}": p for n, p in picks.items()}, indent=1))
