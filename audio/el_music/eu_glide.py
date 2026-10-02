"""Round 34: "EU" sung ee-YOO (eu34_inpaint.py) in the lines whose EU lacks the glide in v13 (glide.py):
  L7   "I'm upping my EU doom"    holds "ee" straight into "doom" (no U)
  L29  "I'm upping my EU doom,"   no "ee" ("you doom")
  L40  "EU Inc fixes things soon" an open "eh-oo" into "Inc"
  build    each take's "EU doom" (hooks; "I'm upping my" stays the original singer's, as built since v5) or "EU" (L40,
           up to the join at 121.09 s, so the user's "Inc fixes things soon" stays) swapped into song v13, untouched on
           the BS-RoFormer split, centre/sides levelled; clips "L<n> EU <take>" in analysis/work/eu_glide/L<n>
  measure  on the BS-RoFormer vocal of each clip (and of v13's current line), against the original singer:
             glide    glide.py on the E and U (CTC letters of "ee you"): the E must reach /i/ (F2 > 1900 Hz, held) in the
                      word's first 35 % and run into the U (F2 < 1700 Hz, held) with <= 20 ms unvoiced, dip >= -12 dB
             my->E    the level of the last 40 ms before the E against the original's (L18's flaw was -45 dB there)
             rhythm, pitch, clarity, words (CTC of the sung line), seams (against v13)
  file     Desktop/suno_test/"eu_v12_EU glide - all versions": per line its current clip and "L<n> EUv1 ..." best first
           (the glide first, then the original's rhythm, clarity, pitch, words), README with the glide of each clip and a
           top pick per line; opens the folder
Run from audio/el_music with the analysis venv: eu_glide.py build|measure|file [line ...]"""
import json, pathlib, shutil, subprocess, sys
import numpy as np, librosa

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import line_round as LR

WORK = HERE.parents[1] / "analysis/work/eu_glide"
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_v12_EU glide - all versions"
SPELL = ["ee-YOO", "E-yu", "Ee-you", "E.U. (ee-yoo)"]
LINES = {7: dict(text="I'm upping my EU doom", sp="i'm upping my ee you doom", orig_sp="i'm upping my p doom", idx=[3],
                 next_word="doom", paste=None),
         29: dict(text="I'm upping my EU doom,", sp="i'm upping my ee you doom", orig_sp="i'm upping my p doom", idx=[3],
                  next_word="doom", paste=None),
         40: dict(text="EU Inc fixes things soon", sp="ee you inc fixes things soon", orig_sp="ar el aitch eff goes askew", idx=[0],
                  next_word="inc", paste=(120.76, 121.09))}
TAKES = {n: [f"eu34_L{n}_{k}" for k in range(1, 9)] for n in LINES}


def wdir(n):
    d = WORK / f"L{n}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def build(*lines):
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    import final12
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    for n in [int(x) for x in lines] or LINES:
        C, W = LINES[n], wdir(n)
        a, b = bounds(n)
        cut = lambda y: y[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)]
        LR.mp3(cut(V.mix), V.SR, W / f"L{n} original - original.mp3")
        LR.mp3(cut(v13), V.SR, W / f"L{n} current - {C['text']}.mp3")
        f = W / "seams.json"
        seams = json.loads(f.read_text()) if f.exists() else {}
        old = " ".join(w["w"] for w in V.LYR[n - 1]["words"]).upper()
        for take in TAKES[n]:
            plan = (C["idx"], old, C["sp"].upper(), C["text"])
            Y = hooked(ms(None, n), n, take, plan, "bsroformer", VO_R)
            if C["paste"]:  # L40: from the quiet point before the line to exactly the takes' join at 121.09
                from final10 import quiet
                from final13 import paste_at
                out, span = paste_at(v13, Y, quiet(C["paste"][0]), C["paste"][1])
            else:
                out, span = paste(v13, Y, a, b)
            LR.mp3(cut(out), V.SR, W / f"L{n} {take} - {C['text']}.mp3")
            seams[take] = [[round(float(t), 3), round(float(final12.seam_db(out, v13, t)), 1)] for t in span]
            print(f"L{n} {take} seams (t, dB vs v13)", seams[take], flush=True)
        f.write_text(json.dumps(seams, indent=1))


def measure(*lines):
    import compare as C
    import parselmouth, sylfit, glide as G
    import lyricfit as F
    import torch, torchaudio
    T = json.loads((HERE.parents[1] / "data/timing_eu.json").read_text())["lines"]
    for n in [int(x) for x in lines] or LINES:
        cfg, W = LINES[n], wdir(n)
        C.LINES, C.WORK = W, W / "cmp"
        C.WORK.mkdir(exist_ok=True)
        if C._sep is not None:  # compare.py's separator keeps the folder it was made with
            C._sep.output_dir = C._sep.model_instance.output_dir = str(C.WORK)
        C.plot = lambda *a, **k: None
        keys = [" current"] + [f" {t}" for t in TAKES[n]]
        _, rows = C.table(f"L{n}", keys)
        t0, ws = C.words(f"L{n}")
        la, lb = ws[0]["start"], ws[-1]["end"]
        piece = lambda v, a, b: v.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]
        tE0 = ws[cfg["idx"][0]]["start"]  # the original's word the EU replaces

        def letters(v, sp):
            m = piece(v, la - 0.12, lb + 0.15)
            em = F.emissions(librosa.resample(m, orig_sr=44100, target_sr=22050), 22050)
            toks, owner = [], []
            for wi, w in enumerate(sp.upper().split()):
                if toks:
                    toks.append(F._IDX["|"]); owner.append(None)
                for c in w.replace("'", ""):
                    toks.append(F._IDX[c]); owner.append((wi, c))
            ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
            spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
            first = {}
            for i, s in enumerate(spans):
                if owner[i] and owner[i] not in first:
                    first[owner[i]] = la - 0.12 + s.start * 0.02
            return first, em

        def hnr(v):
            h = parselmouth.Sound(piece(v, la, lb).astype(np.float64), 44100).to_harmonicity_cc(time_step=0.01, minimum_pitch=90).values[0]
            return float(np.mean(h[h > 0]))

        _, vo = C.split(C.clip(f"L{n}", " original"))
        g_o, h_o = [t for _, t in sylfit.vowels(piece(vo, la - 0.12, lb + 0.15), la - 0.12, cfg["orig_sp"]) if t is not None], hnr(vo)
        lvl = lambda v, a, b: 10 * np.log10(np.mean(piece(v, a, b) ** 2) + 1e-12)
        pre_o = lvl(vo, tE0 - 0.04, tE0)
        seams = json.loads((W / "seams.json").read_text())
        res = {}
        words = cfg["sp"].split()
        iE = words.index("ee")
        for key in keys:
            k = key.strip()
            _, vc = C.split(C.clip(f"L{n}", key))
            first, em = letters(vc, cfg["sp"])
            tE, tY = first[(iE, "E")], first[(iE + 1, "Y")]
            nxt = first[(iE + 2, cfg["next_word"][0].upper())]
            gl = G.glide(piece(vc, la - 0.12, lb + 0.15), la - 0.12, tE, tY, "EU", until=nxt + 0.02)
            g = [t for _, t in sylfit.vowels(piece(vc, la - 0.12, lb + 0.15), la - 0.12, cfg["sp"]) if t is not None]
            d = np.array([min(abs(t - x) for x in g) for t in g_o]) * 1000 if g else np.array([999.0])
            cents = np.array([r["cents"] for r in rows[key]["words"]]); cents = np.abs((cents + 600) % 1200 - 600)
            L = lambda s: float(F.loss(em, s.upper().replace("'", "")))
            # my->E only where "my" leads into the E (the hooks); L40's EU starts the line
            res[k] = dict(glide=gl, E=round(tE, 3), next=round(nxt, 3), pre_E_db=lvl(vc, tE0 - 0.04, tE0) - pre_o if cfg["idx"][0] else None,
                          rhythm=float(np.mean(d)), rhythm_max=int(np.max(d)), cents=float(np.nanmedian(cents)), hnr=hnr(vc) - h_o,
                          words=L(cfg["sp"]), seams=seams.get(k))
            r = res[k]
            print(f"L{n} {k:12s} glide {gl['glide']!s:5} (gap {gl['gap_ms']}, dip {gl['dip_db']}, move {gl['move_ms']} ms)  "
                  f"my->E {r['pre_E_db'] if r['pre_E_db'] is None else round(r['pre_E_db'], 1)} dB  rhythm {r['rhythm']:.0f} ms  pitch {r['cents']:.0f} c  clarity {r['hnr']:+.1f} dB  "
                  f"words {r['words']:.0f}  seams {r['seams']}", flush=True)
        (W / "measure.json").write_text(json.dumps(res, indent=1, default=float))


def rank(res, keys):
    sc = {k: 0.0 for k in keys}
    for w, f in [(2, lambda r: r["rhythm"]), (1.5, lambda r: -r["hnr"]), (1, lambda r: r["cents"]), (1, lambda r: r["words"]),
                 (1, lambda r: abs(min(0.0, r["pre_E_db"] or 0.0))), (1, lambda r: max(abs(db) for _, db in (r["seams"] or [[0, 0]])))]:
        for i, k in enumerate(sorted(keys, key=lambda k: f(res[k]))):
            sc[k] += w * i
    return sorted(keys, key=lambda k: (not res[k]["glide"]["glide"], sc[k]))


def file():
    DESK.mkdir(parents=True, exist_ok=True)
    parts = []
    for n, cfg in LINES.items():
        W = wdir(n)
        res = json.loads((W / "measure.json").read_text())
        order = rank(res, [k for k in res if k != "current"])
        src = lambda k: next(W.glob(f"L{n} {k} - *.mp3"))
        shutil.copy(src("current"), DESK / f"L{n} EU current (v13, in the video) - {cfg['text']}.mp3")
        names = {}
        for i, k in enumerate(order, 1):
            names[k] = f"L{n} EUv{i}"
            shutil.copy(src(k), DESK / f"L{n} EUv{i} - {cfg['text']}.mp3")
        (W / "names.json").write_text(json.dumps(names, indent=1))
        def row(name, k):
            r, g = res[k], res[k]["glide"]
            sp = SPELL[(int(k.split("_")[-1]) - 1) % 4] if k != "current" else ""
            gap = "-" if g["gap_ms"] is None else g["gap_ms"]
            dip = "-" if g["dip_db"] is None else f"{g['dip_db']:+.1f}"
            mv = "-" if g["move_ms"] is None else g["move_ms"]
            return (f"  {name:14}  {k:12}  {'yes' if g['glide'] else 'no':5}  {gap!s:>6}  {dip:>6}  {mv!s:>7}  "
                    f"{('-' if r['pre_E_db'] is None else format(r['pre_E_db'], '+.1f')):>7}  "
                    f"{r['rhythm']:9.0f}  {r['cents']:7.0f}  {r['hnr']:+10.1f}  {r['words']:5.0f}  {sp}")
        glided = [k for k in order if res[k]["glide"]["glide"]]
        top = order[0] if glided else None
        parts.append(f"L{n} \"{cfg['text']}\"\n"
                     + (f"  TOP PICK: {names[top]} ({top}): the glide, rhythm {res[top]['rhythm']:.0f} ms off the original, clarity "
                        f"{res[top]['hnr']:+.1f} dB, pitch {res[top]['cents']:.0f} c\n" if top else "  No take has the glide.\n")
                     + f"  {len(glided)} of {len(order)} takes have the glide; the current one "
                     + ("does" if res["current"]["glide"]["glide"] else "doesn't") + ".\n"
                     + f"  {'clip':14}  {'take':12}  {'glide':5}  {'gap ms':>6}  {'dip dB':>6}  {'move ms':>7}  {'my->E':>7}  "
                       f"{'rhythm ms':>9}  {'pitch c':>7}  {'clarity dB':>10}  {'words':>5}  spelling\n"
                     + "\n".join([row("current", "current")] + [row(names[k], k) for k in order]))
    (DESK / "README.txt").write_text(
        "\"EU\" sung ee-YOO, with the /j/ glide into the U: round 34, 1 Oct 2026.\n\n"
        "In song v13 L18 and L41 already glide (measured the same way); L7 holds \"ee\" straight into \"doom\", L29 sings\n"
        "\"you doom\" (no \"ee\"), L40 an open \"eh-oo\" into \"Inc\". For those three, new takes (one chunk per line, conditioned\n"
        "low on the original, spelled ee-YOO / E-yu / Ee-you / E.U. (ee-yoo)); only \"EU doom\" (L7, L29: \"I'm upping my\" stays the\n"
        "original singer's) or \"EU\" (L40, to 121.09 s: \"Inc fixes things soon\" stays) is swapped, untouched on the RoFormer\n"
        "split, centre/sides levelled. Per line its current clip and the takes, best first.\n\n"
        + "\n\n".join(parts) + "\n\n"
        "glide    glide.py on the vocal: the E must reach /i/ (F2 over 1900 Hz, held 20 ms) in the word's first 35 % and run into\n"
        "         the U (F2 under 1700 Hz, held) with at most 20 ms unvoiced (gap) and no deeper dip than -12 dB; move = /i/ to /u/\n"
        "my->E    level of the 40 ms before the E against the original's (L18's old flaw: \"my\" faded early, -45 dB)\n"
        "rhythm   for each of the original's syllables, how far the take's nearest syllable onset is, ms\n"
        "pitch    median distance from the original's notes per word, cents; clarity: Praat harmonicity against the\n"
        "         original's, dB; words: CTC fit of the sung line, lower = clearer\n"
        "Ranking: the glide first, then rank-sum: rhythm x2, clarity x1.5, pitch, words, my->E and the end seam's level x1.\n"
        "Caveat: the same check said your L37 pick (v24, eu33_3) never reaches the /j/ at all, while it had the clearest\n"
        "A and I by CTC, so the glide check isn't yet proven against your ear; the top picks are where to start listening.\n"
        "Nothing is in the song yet.\n")
    print("\n\n".join(parts))
    subprocess.run(["open", str(DESK)])


if __name__ == "__main__":
    {"build": build, "measure": measure, "file": file}[sys.argv[1]](*sys.argv[2:])
