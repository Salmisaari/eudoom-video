"""The user's pick folder (Desktop/suno_test/"PICK - 5 lines, old vs new", OLD = the song now, NEW = my measured top pick):
"your new ones need more variations, such as the new AC doesn't even say AC but AAH". The measured checks passed takes
the ear doesn't, so every NEW variant now has to pass a gate that includes what a machine hears:
  Whisper  large-v3-turbo on the clip (the mix) and on its vocal (BS-RoFormer), no prompt; the line's words must be in
           either: L16 "AC" / "A.C." / "a c" (not "ah"), the hooks and L40 "EU" / "E.U.", L19 "income's soon" (with the s)
  L16      also the CTC confidence of A and of C each at least half the line's other letters (letters spelled "ay see",
           "a c" or "ay c", whichever fits); the winners get the "ran" fix (l16_tune.lift_on_take on their own timing)
  EU       also an "ee" held before the "yoo" (glide.py: the E's /i/ found); the glide (sung through) ranks first
Passing clips go into the folder as "<n> L<line> NEW b - ...", c, d ...; the existing NEW becomes "NEW a"; LISTEN.txt has
the transcripts of every NEW clip, one line each.
Run from audio/el_music with the analysis venv: pick_gate.py rename | L16 | EU | L19 | listen"""
import json, pathlib, re, shutil, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
PICK = pathlib.Path.home() / "Desktop/suno_test/PICK - 5 lines, old vs new"
CACHE = ROOT / "analysis/work/pick_gate"
CACHE.mkdir(parents=True, exist_ok=True)
SR = 44100
LINES = {16: ("1", "I feel my AC temperatures rearranging"), 7: ("2", "I'm upping my EU doom (0.22)"),
         29: ("3", "I'm upping my EU doom (1.35)"), 40: ("4", "EU Inc fixes things soon"), 19: ("5", "I hear the basic income's soon")}
GATE = {16: r"\ba\.?\s*c\.?(?=\W|$)|\bay[\s-]*see\b|\ba/c\b", 7: r"\be\.?\s*u\.?(?=\W|$)", 29: r"\be\.?\s*u\.?(?=\W|$)",
        40: r"\be\.?\s*u\.?(?=\W|$)", 19: r"\bincome'?s\s+soon\b"}
_model = None


def whisper(path):
    """(mix transcript, vocal transcript) of a clip"""
    import mlx_whisper, compare as C
    out = []
    y = librosa.load(path, sr=16000, mono=True)[0]
    path = pathlib.Path(path)
    C.WORK = path.parent / "cmp" if (path.parent / "cmp").exists() else CACHE / "cmp"  # the clip's own vocal cache
    C.WORK.mkdir(exist_ok=True)
    if C._sep is not None:
        C._sep.output_dir = C._sep.model_instance.output_dir = str(C.WORK)
    v = C.split(pathlib.Path(path))[1].mean(0)
    for x, sr in ((y, 16000), (librosa.resample(v, orig_sr=SR, target_sr=16000), 16000)):
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, x, sr)
            out.append(mlx_whisper.transcribe(t.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                              temperature=0.0, condition_on_previous_text=False)["text"].strip())
    return tuple(out)


def heard(n, texts):
    return any(re.search(GATE[n], t, re.I) for t in texts)


def name(n, letter, text):
    return PICK / f"{LINES[n][0]} L{n} NEW {letter} - {text}.mp3"


def rename():
    for n, (i, text) in LINES.items():
        for f in PICK.glob(f"{i} L{n} NEW - *.mp3"):
            f.rename(f.with_name(f.name.replace(" NEW - ", " NEW a - ")))
    print(sorted(p.name for p in PICK.iterdir()))


def put(n, clips):
    """clips: [(source path, note)] passing, best first -> NEW b, c, ... (existing letters kept)"""
    have = sorted(p.name for p in PICK.glob(f"{LINES[n][0]} L{n} NEW * - *.mp3"))
    used = {re.search(r" NEW (\w) - ", h).group(1) for h in have}
    letters = [c for c in "bcdefg" if c not in used]
    log = json.loads((CACHE / "picks.json").read_text()) if (CACHE / "picks.json").exists() else {}
    for (src, note), letter in zip(clips, letters):
        shutil.copy(src, name(n, letter, LINES[n][1]))
        log[f"L{n} NEW {letter}"] = dict(src=str(src), note=note)
    (CACHE / "picks.json").write_text(json.dumps(log, indent=1))


def gate_eu():
    for n in (7, 29, 40):
        W = ROOT / f"analysis/work/eu_glide/L{n}"
        res = json.loads((W / "measure.json").read_text())
        names = json.loads((W / "names.json").read_text())
        top = min(names, key=lambda k: int(names[k].split("EUv")[1]))  # NEW a (the folder's NEW)
        rows = []
        for k, r in res.items():
            if k in ("current", top):
                continue
            src = next(W.glob(f"L{n} {k} - *.mp3"))
            t = whisper(src)
            ee, gl = r["glide"]["j"], r["glide"]["glide"]
            ok = heard(n, t) and ee
            print(f"L{n} {k} ({names[k]}): Whisper mix {t[0]!r} | vocal {t[1]!r}  ee {ee} glide {gl} -> {'PASS' if ok else 'fail'}", flush=True)
            rows.append((k, ok, gl, src, t, names[k]))
        passing = sorted([r for r in rows if r[1]], key=lambda r: (not r[2], int(r[5].split("EUv")[1])))[:4]
        put(n, [(r[3], f"{r[0]} ({r[5]} in eu_v12_EU glide), glide {'yes' if r[2] else 'no (ee, then a break)'}") for r in passing])
        print(f"L{n}: {len(passing)} more passing", flush=True)


def letter_conf(v, t0, a, b, sp, targets):
    """CTC alignment of sp on the vocal v (stereo, clip starting at song time t0) over [a, b]; for each target (word index,
    letter index or None for the whole word) its letters' mean confidence against all the other letters'"""
    import torch, torchaudio, lyricfit as F
    m = v.mean(0)[int((a - t0) * SR):int((b - t0) * SR)]
    em = F.emissions(librosa.resample(m, orig_sr=SR, target_sr=22050), 22050)
    toks, owner = [], []
    for wi, w in enumerate(sp.upper().split()):
        if toks:
            toks.append(F._IDX["|"]); owner.append(None)
        for ci, c in enumerate(w.replace("'", "")):
            toks.append(F._IDX[c]); owner.append((wi, ci))
    ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
    s_ = [(owner[i], x.score) for i, x in enumerate(spans) if owner[i] is not None]
    hit = lambda o, tg: o[0] == tg[0] and (tg[1] is None or o[1] == (tg[1] if tg[1] >= 0 else len(sp.split()[tg[0]].replace("'", "")) + tg[1]))
    each = [float(np.mean([x for o, x in s_ if hit(o, tg)])) for tg in targets]
    rest = float(np.mean([x for o, x in s_ if not any(hit(o, tg) for tg in targets)]))
    return [e / rest for e in each]


def vocal_of(path):
    import compare as C
    path = pathlib.Path(path)
    C.WORK = path.parent / "cmp"; C.WORK.mkdir(exist_ok=True)
    if C._sep is not None:
        C._sep.output_dir = C._sep.model_instance.output_dir = str(C.WORK)
    return C.split(path)[1]


def gate_l16():
    """round 38: Whisper hears AC, and A and C each at least half as confident as the line's other letters; the
    winners get the ran fix (the lift on their own ran) and are heard again"""
    import l16_tune as T, sylfit
    W = ROOT / "analysis/work/l16_r38"
    res = json.loads((W / "measure.json").read_text())
    T0 = 49.562 - 0.8
    rows = []
    for k in [f"eu38_{i}" for i in range(1, 10)]:
        src = next(W.glob(f"L16 {k} - *.mp3"))
        v = vocal_of(src)
        conf = max((letter_conf(v, T0, 49.45, 52.95, f"i feel my {x} temperatures rearranging", [(3, None), (4, None)]), x)
                   for x in ("ay see", "a c", "ay c"))
        t = whisper(src)
        ok = heard(16, t) and min(conf[0]) >= 0.5
        print(f"L16 {k}: Whisper mix {t[0]!r} | vocal {t[1]!r}  A {conf[0][0]:.2f} C {conf[0][1]:.2f} ('{conf[1]}')  "
              f"-ranging {res[k]['hold_signed']:+.0f} c  seam {res[k]['seams'][0][1]:+.1f} dB -> {'PASS' if ok else 'fail'}", flush=True)
        rows.append(dict(k=k, ok=ok, src=src, conf=min(conf[0]), both=sum(bool(re.search(GATE[16], x, re.I)) for x in t),
                         hold=res[k]["hold_signed"], words=res[k]["words"], seam=res[k]["seams"][0][1]))
    passing = sorted([r for r in rows if r["ok"] and abs(r["seam"]) < 3], key=lambda r: (-r["both"], -r["conf"], r["words"]))[:4]
    out = []
    for r in passing:
        src, note = r["src"], f"{r['k']}: A/C weakest {r['conf']:.2f} of the other letters"
        if abs(r["hold"]) > 100:  # -ranging low: the lift, on this take's own ran
            v = vocal_of(src)
            ran = dict(T.syllables(v, T.SP_NEW)).get("ran")
            d = round(ran - 52.17, 3)
            src = lift_build(r["k"], d)
            note += f"; ran lifted onto its note (the lift {d * 1000:+.0f} ms, onto this take's ran)"
            t = whisper(src)
            print(f"   lifted {r['k']}: Whisper mix {t[0]!r} | vocal {t[1]!r} -> {'still heard' if heard(16, t) else 'NOT heard after the lift'}", flush=True)
            if not heard(16, t):
                continue
        out.append((src, note))
    put(16, out)
    print(f"L16: {len(out)} passing", flush=True)


def lift_build(take, d):
    import l16_tune as T
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    from v8_refine import P16_ALL
    import line_round as LR
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=SR, mono=False)[0][:, : V.mix.shape[1]]
    a, b = bounds(16)
    Y = hooked(ms(T.lift_on_take(d=d, until=52.17 + d + 0.28), 16), 16, take, P16_ALL, "bsroformer", VO_R)
    out, _ = paste(v13, Y, a, b)
    f = ROOT / f"analysis/work/l16_r38/L16 {take} lifted - I feel my AC temperatures rearranging.mp3"
    LR.mp3(out[:, int((a - 0.8) * SR):int((b + 0.5) * SR)], SR, f)
    return f


def gate_l19():
    """the user heard "income", not "income's": the s at least as strong as the s of "basic", 80 ms or more, and
    Whisper hearing "income's"/"incomes" or the CTC confidence of that s at least half the other letters'"""
    W = ROOT / "analysis/work/l19_r37"
    res = json.loads((W / "measure.json").read_text())
    T0 = 60.58 - 0.8
    cands = [f"eu39_{i}" for i in range(1, 9)] + [f"eu39_{i}m" for i in range(1, 9)] + [f"eu37_{i}" for i in range(1, 10)]
    rows = []
    for k in cands:
        s_ = res[k]["soon"]
        if s_["s_ms"] < 80 or (s_["s_vs_basic_db"] or -99) < 0:
            print(f"L19 {k}: s {s_['s_ms']} ms, {s_['s_vs_basic_db']} dB against basic's -> fail (s)", flush=True)
            continue
        src = next(W.glob(f"L19 {k} - *.mp3"))
        v = vocal_of(src)
        c = letter_conf(v, T0, 60.5, 62.7, "i hear the basic incomes soon", [(4, -1)])[0]
        t = whisper(src)
        heard_s = any(re.search(r"\bincome'?s\b", x, re.I) for x in t)
        ok = heard_s or c >= 0.5
        print(f"L19 {k}: s {s_['s_ms']} ms {s_['s_vs_basic_db']:+.1f} dB, CTC s {c:.2f}, Whisper mix {t[0]!r} | vocal {t[1]!r} -> {'PASS' if ok else 'fail'}", flush=True)
        rows.append(dict(k=k, ok=ok, src=src, heard=heard_s, c=c, s=s_))
    passing = sorted([r for r in rows if r["ok"]], key=lambda r: (not r["heard"], -r["s"]["s_vs_basic_db"], -r["c"]))[:4]
    put(19, [(r["src"], f"{r['k']}: s {r['s']['s_ms']} ms, {r['s']['s_vs_basic_db']:+.1f} dB against basic's, CTC s {r['c']:.2f}"
                        + (", Whisper heard income's" if r["heard"] else "")) for r in passing])
    print(f"L19: {len(passing)} passing", flush=True)


def tidy():
    """the user's verdict (1 Oct 2026): L16 OLD is still best, so tune it (TUNED a/b/c, l16_tune.py); L19 OLD "gloom"
    is best but sounds like "glue", so close its m (M a/b/c, l19_m.py). The failed NEW clips and caches go to _rejected"""
    rej = PICK / "_rejected"; rej.mkdir(exist_ok=True)
    for f in list(PICK.glob("1 L16 NEW * - *.mp3")) + list(PICK.glob("5 L19 NEW * - *.mp3")) + [PICK / "cmp", PICK / "LISTEN.txt"]:
        if f.exists():
            shutil.move(str(f), str(rej / f.name))
    import l16_tune as T
    for k, what in T.TUNED.items():
        shutil.copy(next(T.WORK.glob(f"L16 TUNED {k} - *.mp3")), PICK / f"1 L16 TUNED {k} - {what}.mp3")
    names = {"a": "m closed lightly", "b": "m closed like L10's zoom", "c": "m closed fully", "d": "m hum from the original singer"}
    for k, what in names.items():
        shutil.copy(ROOT / f"analysis/work/l19_m/L19 M {k} - I hear the basic income gloom.mp3",
                    PICK / f"5 L19 M {k} - I hear the basic income gloom ({what}).mp3")
    print(sorted(p.name for p in PICK.iterdir()))


def listen():
    """LISTEN.txt: what Whisper hears in OLD and in every variant now in the folder"""
    gate = {16: GATE[16], 7: GATE[7], 29: GATE[29], 40: GATE[40], 19: r"\bgloom\b"}
    word = {16: "AC", 7: "EU", 29: "EU", 40: "EU", 19: "gloom"}
    lines = []
    for f in sorted(p for p in PICK.glob("* - *.mp3")):
        n = int(re.search(r" L(\d+) ", f.name).group(1))
        if n in (7, 29, 40) and " OLD " in f.name:
            continue
        t = whisper(f)
        ok = any(re.search(gate[n], x, re.I) for x in t)
        lines.append(f"{f.name}\n    mix:   {t[0]}\n    vocal: {t[1]}\n    {'heard' if ok else 'did NOT hear'} \"{word[n]}\"")
    (PICK / "LISTEN.txt").write_text(
        "What Whisper (large-v3-turbo, no prompt) heard in each clip: on the mix, and on the vocal alone. For L19 the\n"
        "question is now whether it hears \"gloom\" (with its m) rather than \"glue\". The earlier NEW clips and their\n"
        "transcripts are in _rejected.\n\n" + "\n".join(lines) + "\n")
    print("\n".join(lines))
    import shutil as _s
    if (PICK / "cmp").exists():  # whisper() caches the vocal split next to the clip
        _s.rmtree(PICK / "cmp")


if __name__ == "__main__":
    {"rename": rename, "EU": gate_eu, "L16": gate_l16, "L19": gate_l19, "tidy": tidy, "listen": listen}[sys.argv[1]]()
