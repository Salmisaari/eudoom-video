"""Assemble the EU song from vsplice.py's picks: each winner re-separated with htdemucs_ft and spliced word-level into
the vocal only. Writes audio/pdoom_eu.mp3, data/eu_words.json (lines whose word count changed), data/visemes_eu.json,
and a before/after reel on the Desktop. Checks that everything outside the swapped words is untouched."""
import json, pathlib, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from vsplice import SR, LYR, PLAN, mix, VO, load_take, build, apply
from eu_words import spoken, align
from visemes import letters_to_visemes
import mlx_whisper

VER = __import__("os").environ.get("EU_VERSION", "v5")
DESK = pathlib.Path.home() / f"Desktop/suno_test/eu_{VER}"


def hear(y, a, b):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, librosa.resample(y.mean(0)[int(a * SR):int(b * SR)], orig_sr=SR, target_sr=16000), 16000)
        return mlx_whisper.transcribe(f.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


def mp3(y, path, br="320k"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-b:a", br,
                    str(path)], input=np.ascontiguousarray(y.T, dtype=np.float32).tobytes(), check=True)


report = json.loads((HERE / "vsplice_report.json").read_text())
out, voc, spans = mix.copy(), VO.copy(), {}
for n in sorted(PLAN):
    best = report[str(n)]["best"]
    take = best["take"]
    r = build(load_take(take), n, sep="htdemucs_ft", warp_on=best.get("warp", True))
    out, voc = apply(out, voc, r)
    spans[n] = (take, r["t_in"], r["t_out"], r["ws"], r["we"])
    print(f"L{n:02d} {take:10s} swapped {r['t_in']:.3f}-{r['t_out']:.3f} s", flush=True)

# untouched outside the swapped words (fades are 30 ms)
mask = np.ones(mix.shape[1], bool)
for _, t_in, t_out, _, _ in spans.values():
    mask[int((t_in - 0.02) * SR):int((t_out + 0.02) * SR)] = False
print(f"outside the swaps: max |diff| {np.abs(out - mix)[:, mask].max():.2e}; swapped {(~mask).sum() / SR:.1f} s total")

sf.write(HERE / f"pdoom_EU_{VER}.wav", out.T, SR)
mp3(out, ROOT / "audio/pdoom_eu.mp3")
DESK.mkdir(parents=True, exist_ok=True)
mp3(out, DESK / f"pdoom_EU_edition_{VER}.mp3")

# word timings and mouth keys for the swapped words, aligned on the new vocal inside each original span
vis = json.loads((ROOT / "data/visemes.json").read_text())
keys = [tuple(k) for k in vis["keys"]]
words_out = {}
vm = librosa.resample(librosa.to_mono(voc), orig_sr=SR, target_sr=22050)
for n, (take, t_in, t_out, ws, we) in spans.items():
    idx, _, _, disp = PLAN[n]
    pairs = spoken(disp, "I'm upping my U-doom" if n in (7, 18, 29, 41) else disp)  # hooks sing "you doom"
    seg = vm[int((ws - 0.02) * 22050):int((we + 0.02) * 22050)]
    letters = align(seg, ws - 0.02, pairs)
    starts = {}
    for (wi, _, _), t in letters:
        starts.setdefault(wi, t)
    st = [min(max(ws, starts.get(i, ws)), we) for i in range(len(pairs))]
    st = list(np.maximum.accumulate(st))
    new_words = [[w, round(st[i], 3), round(st[i + 1] if i + 1 < len(st) else we, 3)] for i, (w, _) in enumerate(pairs)]
    ow = LYR[n - 1]["words"]
    line = [[w["w"], w["start"], w["end"]] for w in ow[: idx[0]]] + new_words + \
           [[w["w"], w["start"], w["end"]] for w in ow[idx[-1] + 1:]]
    if len(line) != len(ow):
        words_out[str(n)] = line
    new, per_sub = [], {}
    for (wi, sub, _), t in letters:
        per_sub.setdefault((wi, sub), []).append(t)
    for (wi, sub), ts in per_sub.items():
        for v, i in letters_to_visemes(sub.lower()):
            new.append((round(float(np.clip(ts[min(i, len(ts) - 1)], ws, we)), 3), v))
    new.sort()
    new = [k for i, k in enumerate(new) if i == 0 or k[1] != new[i - 1][1]]
    resume = next((k[1] for k in reversed(keys) if k[0] <= we), "X")
    keys = [k for k in keys if k[0] < ws] + new + [(round(we, 3), resume)] + [k for k in keys if k[0] > we]
    print(f"L{n:02d} " + " ".join(f"{w}@{s:.2f}" for w, s, _ in line) + f" | heard: {hear(out, ow[0]['start'] - 0.2, LYR[n - 1]['end'] + 0.2)}",
          flush=True)
(ROOT / "data/eu_words.json").write_text(json.dumps(words_out, indent=1))
vis["keys"] = [[t, v] for t, v in keys]
vis["note"] = vis["note"].split(" EU edition")[0] + " EU edition: swapped words re-aligned by audio/el_music/vassemble.py."
(ROOT / "data/visemes_eu.json").write_text(json.dumps(vis, separators=(",", ":")))

gap, reel, idx_txt, t = np.zeros((2, int(0.6 * SR)), dtype=np.float32), [], [], 0.0
for n, (take, t_in, t_out, ws, we) in spans.items():
    a, b = LYR[n - 1]["start"] - 1.0, LYR[n - 1]["end"] + 1.0
    for lab, y in (("original", mix), (f"EU {VER}", out)):
        c = y[:, int(a * SR):int(b * SR)]
        idx_txt.append(f"{int(t // 60)}:{t % 60:04.1f}  L{n:02d} {lab}")
        reel += [c, gap]
        t += c.shape[1] / SR + 0.6
mp3(np.concatenate(reel, 1), DESK / f"{VER}_changes_before_after.mp3", "256k")
(DESK / f"{VER}_changes_before_after.txt").write_text("\n".join(idx_txt) + "\n")
