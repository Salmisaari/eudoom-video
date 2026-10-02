"""One line re-sung in a new inpainting round, the way round 30 did L9-10 (l910_r30.py), for rounds 31 and 32:
  L16  "I feel my AC temperatures rearranging"   eu31_1-9 (the user: "AC temperatures need similar work")
  L37  "Post-AI-bubble, super-dense" (eu32a_1-8, the last spelling literally "Post AI bubble") and
       "Post-bubble, all makes sense" (eu32b_1-9)
  build    each take's line untouched (no tune, no warp) on the BS-RoFormer split, its centre and sides levelled to the
           original singer's, spliced into song v12; clips "<label> <take> - <lyric>" in analysis/work/<round>, with
           the original and v12's current line cut the same
  measure  every clip against the original, on the BS-RoFormer vocal of each clip (compare.py):
             rhythm   the syllable counts differ from the original's, so: for each of the original's vowel onsets (CTC,
                      sylfit.vowels), the distance to the nearest vowel onset the take sings, ms (does it land on the
                      original's beats); worst = the furthest
             pitch    per original word, cents against the original (Praat, octave jumps folded), median
             clarity  Praat harmonicity over the line against the original's, dB; below 0 reads rough or smeared
             hold     the held last word ("-ranging": the original's 70 67 67 at 52.13-52.71; "dense": its last note),
                      cents against the original, median
             words    CTC loss of the take's own words (lower = clearer; the original singing its own words gives the
                      reference) and its margin over the original's words; L37A: also how clearly "A-I" is two letters
                      (CTC of "ay eye" against "ay", "eye" or neither)
             seams    level at both splice points against v12, dB
  file     ranks them (rank-sum: rhythm x2, clarity x1.5, pitch, hold and words x1, width/level x0.5; a take whose
           words don't beat the original's goes last), files the clips best first in Desktop/suno_test/<folder> with a
           README (one table, top 3 per lyric), opens the folder
Run from audio/el_music with the analysis venv: line_round.py L16|L37 build|measure|file"""
import json, pathlib, shutil, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DESK = pathlib.Path.home() / "Desktop/suno_test"

ROUNDS = {
    "L16": dict(n=16, work="l16_r31", folder="eu_v12_L16 - all versions",
                orig="I feel my atoms rearranging", orig_sp="i feel my atoms rearranging",
                cur_desc="eu9_7 whole line, '-ranging' lifted (RoFormer, levelled)",
                hold=(52.10, 52.75), hold_name="'-ranging'", hold_rule=200,
                lyrics={"AC": dict(text="I feel my AC temperatures rearranging", sp="i feel my ay see temperatures rearranging",
                                   takes=[f"eu31_{k}" for k in range(1, 10)],
                                   spell=["plain", "A-C tem-pra-tures re-ar-rang-ing", "AY-SEE TEM-pra-tures re-ar-RANG-ing"])}),
    # round 35: "The UBI point's coming soon" (U-B-I on O-me-ga); L21 in v13 is the original singer
    "L21": dict(n=21, work="l21_r35", folder="eu_v13_L21 - all versions", base="pdoom_EU_v13.wav", no_current=True,
                orig="The Omega Point's coming soon", orig_sp="the omega points coming soon",
                cur_desc="the original singer, \"The Omega Point's coming soon\"", hold=(65.60, 66.20), hold_name="'soon'",
                letters=True, top_per_lyric=1,
                # letters: the letter-words in the sung text, their spellings to try, the glide checked (from one
                # letter-word to the next one's onset), the I (take syllable "on") against the original's syllable
                # "on_orig", and the letters before it against the original's syllables ("map": take -> original)
                lyrics={"UBI": dict(text="The UBI point's coming soon", sp="the you bee eye points coming soon",
                                    takes=[f"eu35_{k}" for k in range(1, 10)], spell=["U-B-I", "you-bee-eye", "UBI Point"],
                                    letters=dict(word="you bee eye", variants=["you bee eye", "u b i", "yu bee i"], glide=(0, 1),
                                                 on=3, on_orig=3, on_name="ga", map={1: 1, 2: 2})),
                        # round 36: the stressed I on the strong beat where "Point's" was, the letters before it on O-me-ga
                        "YOUR": dict(text="Your U-B-I's coming soon", sp="your you bee eyes coming soon",
                                     takes=[f"eu36a_{k}" for k in range(1, 5)], spell=["you-bee-eye's", "U-B-I's"],
                                     letters=dict(word="you bee eyes", variants=["you bee eyes", "yu bee eyes", "you b eyes"],
                                                  glide=(0, 1), on=3, on_orig=4, on_name="Point's", map={1: 1, 2: 2})),
                        "THE": dict(text="The U-B-I's coming soon", sp="the you bee eyes coming soon",
                                    takes=[f"eu36b_{k}" for k in range(1, 5)], spell=["you-bee-eye's", "U-B-I's"],
                                    letters=dict(word="you bee eyes", variants=["you bee eyes", "yu bee eyes", "you b eyes"],
                                                 glide=(0, 1), on=3, on_orig=4, on_name="Point's", map={1: 1, 2: 2})),
                        "EUBI": dict(text="The E-U-B-I's coming soon", sp="the ee you bee eyes coming soon",
                                     takes=[f"eu36c_{k}" for k in range(1, 5)], spell=["ee-you-bee-eye's", "E-U-B-I's"],
                                     letters=dict(word="ee you bee eyes", variants=["ee you bee eyes", "e yu bee eyes", "e u b eyes"],
                                                  glide=(0, 2), on=4, on_orig=4, on_name="Point's", map={1: 1, 2: 2, 3: 3}))}),
    # round 37: "I hear the basic income's soon" ("income's" = "income is", the UBI reference). Each take twice: the whole
    # line, and (keys ending in "m") only "-come's soon" from the k of "in-come" on, after the current singer's
    # "I hear the basic in-" (the cut in the k's closure, a silence)
    "L19": dict(n=19, work="l19_r37", folder="eu_v13_L19 - all versions", base="pdoom_EU_v13.wav", top_per_lyric=1, overall=3,
                orig="I hear the basilisk boom", orig_sp="i hear the basilisk boom",
                cur_desc="eu9_9, \"I hear the basic income gloom\"", cur_text="I hear the basic income gloom", hold=(62.10, 62.54), hold_name="'soon'", soon=True,
                lyrics={"WHOLE": dict(text="I hear the basic income's soon (whole line new)", sp="i hear the basic incomes soon",
                                      takes=[f"eu37_{k}" for k in range(1, 10)],
                                      spell=["income's", "in-come's", "no 'the'"],
                                      literal={2: ("I hear basic income's soon (whole line new)", "i hear basic incomes soon")},
                                      literal_note="Sung without \"the\" (\"{txt}\"): {clips}"),
                        "MIN": dict(text="I hear the basic income's soon (only -come's soon new)", sp="i hear the basic incomes soon",
                                    takes=[f"eu37_{k}m" for k in range(1, 10)], from_k=(61.70, 61.92),
                                    spell=["income's", "in-come's", "no 'the'"]),
                        # round 39: the user heard "income", not "income's": spellings that give the s its own sound
                        "SWHOLE": dict(text="I hear the basic income's soon (whole line new)", sp="i hear the basic incomes soon",
                                       takes=[f"eu39_{k}" for k in range(1, 9)],
                                       spell=["in-come-ZOON", "income-s-soon", "incomes soon", "in-comes SOON"]),
                        "SMIN": dict(text="I hear the basic income's soon (only -come's soon new)", sp="i hear the basic incomes soon",
                                     takes=[f"eu39_{k}m" for k in range(1, 9)], from_k=(61.70, 61.92),
                                     spell=["in-come-ZOON", "income-s-soon", "incomes soon", "in-comes SOON"])}),
    # round 38: L16's A-C as two letters (the user: "the new AC doesn't even say AC but AAH"); gated in pick_gate.py
    "L16b": dict(n=16, work="l16_r38", folder="eu_v13_L16 - round 38", base="pdoom_EU_v13.wav", clip="L16",
                 orig="I feel my atoms rearranging", orig_sp="i feel my atoms rearranging", cur_text="I feel my AC temperatures rearranging",
                 cur_desc="eu9_7 whole line, '-ranging' lifted (RoFormer, levelled)", hold=(52.10, 52.75), hold_name="'-ranging'",
                 lyrics={"AC": dict(text="I feel my AC temperatures rearranging", sp="i feel my ay see temperatures rearranging",
                                    takes=[f"eu38_{k}" for k in range(1, 10)], spell=["ay-see", "A.C.", "Ay-Cee"])}),
    "L37": dict(n=37, work="l37_r32", folder="eu_v12_L37 - all versions",
                orig="Post-Chinchilla, super-dense", orig_sp="post chinchilla super dense",
                cur_desc="the original singer: Post-Chinchilla, super-dense",
                hold=(116.60, 117.00), hold_name="'dense' / 'sense'",
                lyrics={"A": dict(text="Post-AI-bubble, super-dense", sp="post ay eye bubble super dense",
                                  takes=[f"eu32a_{k}" for k in range(1, 9)],
                                  spell=["Post-AI-bubble", "Post A.I. bubble", "Post-AI bubble", "Post AI bubble (stretched)"],
                                  literal={3: ("Post AI bubble", "post ay eye bubble")}),
                        "B": dict(text="Post-bubble, all makes sense", sp="post bubble all makes sense",
                                  takes=[f"eu32b_{k}" for k in range(1, 10)],
                                  spell=["plain", "Post-bub-ble", "POST-bubble, ALL makes SENSE"]),
                        # round 33: v17 (eu32a_3) with the glide the user asked for ("AIJAI", ay-YAI)
                        "Y": dict(text="Post-AI-bubble, super-dense", sp="post ay eye bubble super dense",
                                  takes=[f"eu33_{k}" for k in range(1, 10)], ref="eu32a_3",
                                  spell=["Post-ay-yai bubble", "Post-A-yai bubble", "Post-Ay-Eye bubble", "Post-AY-YAI bubble"])}),
}


def cfg(label):
    R = ROUNDS[label]
    W = pathlib.Path(__file__).resolve().parents[2] / "analysis/work" / R["work"]
    W.mkdir(parents=True, exist_ok=True)
    return R, W


def takes(R):
    """[(take, lyric key, display text, spoken text, spelling)]"""
    out = []
    for key, L in R["lyrics"].items():
        for take in L["takes"]:
            k = int(take.split("_")[1].rstrip("m"))
            i = (k - 1) % len(L["spell"])
            text, sp = L.get("literal", {}).get(i, (L["text"], L["sp"]))
            out.append((take, key, text, sp, L["spell"][i]))
    return out


def mp3(y, sr, path):
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/x.wav", y.T, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/x.wav", "-af",
                        "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k", str(path)], check=True)


def build(label, *only):
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    import final12
    R, W = cfg(label)
    n = R["n"]
    a, b = bounds(n)
    cut = lambda y: y[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)]
    v12 = librosa.load(HERE / R.get("base", "pdoom_EU_v12.wav"), sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]  # the song spliced into
    mp3(cut(V.mix), V.SR, W / f"{R.get('clip', label)} original - {R['orig']}.mp3")
    mp3(cut(v12), V.SR, W / f"{R.get('clip', label)} current - current.mp3")
    f = W / "seams.json"
    seams = json.loads(f.read_text()) if f.exists() else {}
    old = " ".join(w["w"] for w in V.LYR[n - 1]["words"]).upper()
    for take, key, text, sp, _ in takes(R):
        if only and take not in only:
            continue
        plan = (V.ALL_WORDS(n), old, sp.upper(), text)
        Y = hooked(ms(None, n), n, take.rstrip("m"), plan, "bsroformer", VO_R)
        out, span = paste(v12, Y, a, b)
        fk = R["lyrics"][key].get("from_k")
        if fk:  # only from the k of "in-come" on: the vocal swapped between the two songs' quietest points
            out, span = swap_vocal(v12, out, fk, (span[1] - 0.05, span[1] + 0.05))
        mp3(cut(out), V.SR, W / f"{R.get('clip', label)} {take} - {text}.mp3")
        seams[take] = [[round(float(t), 3), round(float(final12.seam_db(out, v12, t)), 1)] for t in span]
        print(take, text, f"seams (t, dB vs {R.get('base', 'pdoom_EU_v12.wav')[9:12]})", seams[take], flush=True)
    f.write_text(json.dumps(seams, indent=1))


def swap_vocal(song, other, lo, hi, W=None):
    """song with other's vocal (BS-RoFormer estimates of both) from the quietest point of the two vocals together in lo
    to the quietest in hi, 20 ms equal-power fades (the two are different takes)"""
    import rof
    W = W or (lo[0] - 0.4, hi[1] + 0.4)
    E1, E2 = rof.separate(song, *W), rof.separate(other, *W)
    t = W[0] + np.arange(E1.shape[1]) / 44100
    e = 10 * np.log10(np.convolve((E1 + E2).mean(0) ** 2, np.ones(441) / 441, "same") + 1e-12)
    qp = lambda a, b: float(t[(t >= a) & (t <= b)][np.argmin(e[(t >= a) & (t <= b)])])
    ti, to = qp(*lo), qp(*hi)
    w = np.clip(np.minimum((t - ti) / 0.02 + 0.5, (to - t) / 0.02 + 0.5), 0, 1)
    out = song.copy(); i0 = int(W[0] * 44100)
    out[:, i0:i0 + E1.shape[1]] = song[:, i0:i0 + E1.shape[1]] - E1 + E1 * np.cos(w * np.pi / 2) + E2 * np.sin(w * np.pi / 2)
    return out, (ti, to)


def measure(label, *only):
    import compare as C
    import parselmouth, sylfit
    import lyricfit as F
    R, W = cfg(label)
    n = R["n"]
    C.LINES, C.WORK = W, W / "cmp"
    C.WORK.mkdir(exist_ok=True)
    C.plot = lambda *a, **k: None
    T = {t[0]: t for t in takes(R)}
    keys = [f" {t}" for t in only] if only else [" current"] + [f" {t}" for t in T]
    _, rows = C.table(R.get('clip', label), keys)
    t0, ws = C.words(R.get('clip', label))
    la, lb = ws[0]["start"], ws[-1]["end"]
    piece = lambda v, a, b: v.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]

    def grid(v, sp):
        return [t for _, t in sylfit.vowels(piece(v, la - 0.12, lb + 0.15), la - 0.12, sp) if t is not None]

    def hnr(v):
        h = parselmouth.Sound(piece(v, la, lb).astype(np.float64), 44100).to_harmonicity_cc(time_step=0.01, minimum_pitch=90).values[0]
        return float(np.mean(h[h > 0]))

    def notes(v, a, b):
        p = parselmouth.Sound(piece(v, a, b).astype(np.float64), 44100).to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
        return p.selected_array["frequency"]

    def ctc(v, sp):
        em = F.emissions(librosa.resample(piece(v, la - 0.12, lb + 0.15), orig_sr=44100, target_sr=22050), 22050)
        return lambda s: float(F.loss(em, s.upper()))

    def ai_letters(v, sp, spell):
        """(weaker of A and I / the other letters, A, I, other letters): CTC confidence of each letter's span"""
        import torch, torchaudio
        em = F.emissions(librosa.resample(piece(v, la - 0.12, lb + 0.15), orig_sr=44100, target_sr=22050), 22050)
        toks, owner = [], []
        for wi, w in enumerate(sp.upper().split()):
            if toks:
                toks.append(F._IDX["|"]); owner.append(None)
            for c in w:
                toks.append(F._IDX[c]); owner.append(wi)
        ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
        spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
        s = [(owner[i], x.score) for i, x in enumerate(spans) if owner[i] is not None]
        ia = sp.split().index(spell.split()[0])
        a = float(np.mean([x for w, x in s if w == ia])); i = float(np.mean([x for w, x in s if w == ia + 1]))
        rest = float(np.mean([x for w, x in s if w not in (ia, ia + 1)]))
        return min(a, i) / rest, a, i, rest

    def letter_at(v, sp, word, letter):
        import torch, torchaudio
        m = piece(v, la - 0.12, lb + 0.15)
        em = F.emissions(librosa.resample(m, orig_sr=44100, target_sr=22050), 22050)
        toks, owner = [], []
        for wi, w in enumerate(sp.upper().split()):
            if toks:
                toks.append(F._IDX["|"]); owner.append(None)
            for c in w:
                toks.append(F._IDX[c]); owner.append((wi, c))
        ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
        spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
        return next(la - 0.12 + x.start * 0.02 for i, x in enumerate(spans) if owner[i] == (word, letter))

    def yai(v):
        """the /j/ glide from the A into the I (glide.py), anchored on CTC's A and I of "post ay i ..." """
        import glide as G
        sp = "post ay i bubble super dense"
        tA, tI = letter_at(v, sp, 1, "A"), letter_at(v, sp, 2, "I")
        return G.glide(piece(v, la - 0.12, lb + 0.15), la - 0.12, tA, tI, "AI")

    def pitch_track(v):
        p = parselmouth.Sound(piece(v, la, lb).astype(np.float64), 44100).to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
        return p.selected_array["frequency"]

    refs = {k: L["ref"] for k, L in R["lyrics"].items() if "ref" in L}
    REF = {}
    for key_, ref in refs.items():
        _, vr = C.split(C.clip(R.get('clip', label), f" {ref}"))
        REF[key_] = dict(take=ref, grid=grid(vr, R["lyrics"][key_]["sp"].replace("ay eye", "ay i")), hnr=hnr(vr), f0=pitch_track(vr))

    def soon_checks(v, vcur):
        """L19: the s of "income's" (unvoiced over 4 kHz between "-come" and "soon": length, and its peak level against
        the s of "basic" in the same clip), the k of "in-come" (the unvoiced gap in 61.6-62.0), and "soon" against the
        current's "gloom" (pitch over its notes, voiced length)"""
        def frames(x, a, b):
            y = piece(x, a, b)
            S = np.abs(librosa.stft(y, n_fft=1024, hop_length=441)) ** 2; fr = librosa.fft_frequencies(sr=44100, n_fft=1024)
            hi = 10 * np.log10(S[fr > 4000].sum(0) + 1e-12); ratio = hi - 10 * np.log10(S[(fr > 100) & (fr < 4000)].sum(0) + 1e-12)
            p = parselmouth.Sound(y.astype(np.float64), 44100).to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
            f0 = np.array([p.get_value_at_time(t) or np.nan for t in np.arange(len(hi)) * 0.01])
            return a + np.arange(len(hi)) * 0.01, hi, ratio, f0
        t, hi, ratio, f0 = frames(v, 61.9, 62.35)
        sib = (ratio > 0) & ~np.isfinite(f0)
        t2, hi2, ratio2, f02 = frames(v, 61.1, 61.55)
        sib2 = (ratio2 > 0) & ~np.isfinite(f02)
        t3, _, _, f03 = frames(v, 61.6, 62.0)
        un = ~np.isfinite(f03); runs, r = [], 0
        for u in un:
            r = r + 1 if u else 0; runs.append(r)
        tc, _, _, fcur = frames(vcur, 62.10, 62.54); _, _, _, fv = frames(v, 62.10, 62.54)
        mm = min(len(fcur), len(fv)); bt = np.isfinite(fcur[:mm]) & np.isfinite(fv[:mm])
        cents = (1200 * np.log2(fv[:mm][bt] / fcur[:mm][bt]) + 600) % 1200 - 600
        _, _, _, fl = frames(v, 62.0, 62.65); _, _, _, flc = frames(vcur, 62.0, 62.65)
        return dict(s_ms=int(sib.sum() * 10), s_vs_basic_db=round(float(hi[sib].max() - hi2[sib2].max()), 1) if sib.any() and sib2.any() else None,
                    k_gap_ms=int(max(runs) * 10), soon_cents=round(float(np.median(np.abs(cents)))) if bt.sum() > 3 else None,
                    soon_ms=int(np.isfinite(fl).sum() * 10), gloom_ms=int(np.isfinite(flc).sum() * 10))

    _, vo = C.split(C.clip(R.get('clip', label), " original"))
    g_o, h_o, f_o = grid(vo, R["orig_sp"]), hnr(vo), notes(vo, *R["hold"])
    vcur = C.split(C.clip(R.get('clip', label), " current"))[1] if R.get("soon") else None
    ref = ctc(vo, R["orig_sp"])(R["orig_sp"])
    print(f"original: vowels {[round(t, 2) for t in g_o]}  HNR {h_o:.1f} dB  CTC of its own words {ref:.0f}", flush=True)
    seams = json.loads((W / "seams.json").read_text())
    f = W / "measure.json"
    res = json.loads(f.read_text()) if f.exists() else {}
    for key in keys:
        k = key.strip()
        sp = T[k][3] if k in T else None
        if k == "current":
            sp = R["lyrics"][next(iter(R["lyrics"]))]["sp"] if label == "L16" else R["orig_sp"]
        _, vc = C.split(C.clip(R.get('clip', label), key))
        g = grid(vc, sp)
        d = np.array([min(abs(t - x) for x in g) for t in g_o]) * 1000 if g else np.array([999.0])
        cents = np.array([r["cents"] for r in rows[key]["words"]]); cents = np.abs((cents + 600) % 1200 - 600)
        fc = notes(vc, *R["hold"]); m = min(len(fc), len(f_o)); bt = (fc[:m] > 0) & (f_o[:m] > 0)
        hold = (1200 * np.log2(fc[:m][bt] / f_o[:m][bt]) + 600) % 1200 - 600 if bt.sum() > 3 else np.array([np.nan])
        L = ctc(vc, sp)
        r = dict(text=T[k][2] if k in T else "current", sp=sp, lyric=T[k][1] if k in T else "current", spell=T[k][4] if k in T else "",
                 rhythm=float(np.mean(d)), rhythm_max=int(np.max(d)), syllables=len(g), syllables_orig=len(g_o),
                 cents=float(np.nanmedian(cents)), hold=float(np.nanmedian(np.abs(hold))), hold_signed=float(np.nanmedian(hold)),
                 hnr=hnr(vc) - h_o, width=float(np.mean(np.abs([r["width"] for r in rows[key]["words"]]))),
                 level=float(np.mean(np.abs([r["lvl"] for r in rows[key]["words"]]))),
                 words=L(sp), words_ref=ref, margin=L(R["orig_sp"]) - L(sp), seams=seams.get(k))
        if label == "L37" and "ay eye" in (sp or ""):
            # "A-I" as two letters: in the CTC alignment of the whole line, the weaker of the A and the I against the
            # other letters (1 = as clear), under whichever spelling fits the sung "I" best; the words are then scored
            # in that spelling too (dropping letters to test them only measures the shorter text)
            best = max((ai_letters(vc, sp.replace("ay eye", s), s) + (s,) for s in ("ay eye", "ay i", "a i")), key=lambda x: x[0])
            r["ai_two_letters"], r["ai_letters"] = best[0], [best[4], round(best[1], 2), round(best[2], 2), round(best[3], 2)]
            r["sp"] = sp = sp.replace("ay eye", best[4])
            r["words"], r["margin"] = L(sp), L(R["orig_sp"]) - L(sp)
        if "letters" in R and k in T:
            Lc = R["lyrics"][T[k][1]]["letters"]
            # each letter clearly sung: CTC confidence of each letter-word against the line's other letters, under the
            # spelling that fits best (as for L37's A-I)
            def conf(spv, v_):
                import torch, torchaudio
                m = piece(vc, la - 0.12, lb + 0.15)
                em_ = F.emissions(librosa.resample(m, orig_sr=44100, target_sr=22050), 22050)
                toks, owner = [], []
                for wi, w in enumerate(spv.upper().split()):
                    if toks:
                        toks.append(F._IDX["|"]); owner.append(None)
                    for c in w:
                        toks.append(F._IDX[c]); owner.append(wi)
                ali, sc = torchaudio.functional.forced_align(em_[None], torch.tensor([toks]), blank=0)
                spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
                s_ = [(owner[i], x.score, x.start) for i, x in enumerate(spans) if owner[i] is not None]
                i0 = spv.split().index(v_.split()[0]); n_ = len(v_.split())
                each = [float(np.mean([x for w, x, _ in s_ if w == i0 + j])) for j in range(n_)]
                rest = float(np.mean([x for w, x, _ in s_ if not (i0 <= w < i0 + n_)]))
                first = {w: la - 0.12 + st * 0.02 for w, _, st in reversed(s_)}
                return min(each) / rest, each, rest, [first[i0 + j] for j in range(n_)]
            best = None
            for v_ in Lc["variants"]:
                c_ = conf(sp.replace(Lc["word"], v_), v_) + (v_,)
                if best is None or c_[0] > best[0]:
                    best = c_
            r["letters"] = dict(spelling=best[4], weakest=round(best[0], 2), each=[round(x, 2) for x in best[1]], rest=round(best[2], 2))
            r["sp"] = sp = sp.replace(Lc["word"], best[4])
            r["words"], r["margin"] = L(sp), L(R["orig_sp"]) - L(sp)
            # the "yoo": the /j/ into the /u/ (glide.py, as for EU), from one letter's onset to the next one's (U to B;
            # for E-U-B-I, E to B: the ee-YOO)
            import glide as G
            firsts = best[3]
            g0, g1 = Lc["glide"]
            r["yoo"] = G.glide(piece(vc, la - 0.12, lb + 0.15), la - 0.12, firsts[g0], firsts[g0] + 0.05, "EU", until=firsts[g1] + 0.02)
            # the I on the original's note ("ga" in round 35, "Point's" in 36): vowel onset and pitch; the letters before
            # it against the original's syllables on O-me-ga
            vow_o = sylfit.vowels(piece(vo, la - 0.12, lb + 0.15), la - 0.12, R["orig_sp"])
            vow_c = sylfit.vowels(piece(vc, la - 0.12, lb + 0.15), la - 0.12, sp)
            vo_, vc_ = vow_o[Lc["on_orig"]][1], vow_c[Lc["on"]][1]
            f_ = lambda v, t: notes(v, t, t + 0.12)
            a_, b_ = f_(vc, vc_), f_(vo, vo_); mm = min(len(a_), len(b_)); bt = (a_[:mm] > 0) & (b_[:mm] > 0)
            r["on_note"] = dict(dt_ms=round((vc_ - vo_) * 1000), name=Lc["on_name"],
                                cents=round(float(np.median(((1200 * np.log2(a_[:mm][bt] / b_[:mm][bt])) + 600) % 1200 - 600))) if bt.sum() > 3 else None)
            r["letters_on"] = {f"{vow_c[ti][0]}->{vow_o[oi][0]}": (round((vow_c[ti][1] - vow_o[oi][1]) * 1000)
                                                                 if vow_c[ti][1] is not None and vow_o[oi][1] is not None else None)
                               for ti, oi in Lc["map"].items()}
        if R.get("soon"):
            r["soon"] = soon_checks(vc, vcur)
        lk = T[k][1] if k in T else None
        if label == "L37" and lk in ("A", "Y"):
            r["yai"] = yai(vc)
        ref_of = next((kk for kk, rf in refs.items() if rf == k), None)
        for key_ in ([lk] if lk in REF else []) + ([ref_of] if ref_of else []):
            Q = REF[key_]
            gk = grid(vc, R["lyrics"][key_]["sp"].replace("ay eye", "ay i"))
            dv = np.array([min(abs(t - x) for x in gk) for t in Q["grid"]]) * 1000 if gk else np.array([999.0])
            fk = pitch_track(vc); mm = min(len(fk), len(Q["f0"])); bt = (fk[:mm] > 0) & (Q["f0"][:mm] > 0)
            cv = np.abs((1200 * np.log2(fk[:mm][bt] / Q["f0"][:mm][bt]) + 600) % 1200 - 600)
            r["vs_ref"] = dict(ref=Q["take"], rhythm=float(np.mean(dv)), cents=float(np.median(cv)), hnr=hnr(vc) - Q["hnr"])
        res[k] = r
        print(f"{k:9s} {r['text'][:30]:30s} rhythm {r['rhythm']:4.0f} ms (worst {r['rhythm_max']})  pitch {r['cents']:4.0f} c  "
              f"hold {r['hold_signed']:+5.0f} c  HNR {r['hnr']:+.1f} dB  words {r['words']:.0f} (orig {ref:.0f}, margin {r['margin']:+.0f})"
              + (f"  A-I {r['ai_two_letters']:.2f} as '{r['ai_letters'][0]}'" if "ai_two_letters" in r else "")
              + (f"  yai {r['yai']}" if "yai" in r else "") + (f"  vs {r['vs_ref']}" if "vs_ref" in r else "")
              + (f"  soon {r['soon']}" if "soon" in r else "")
              + (f"  letters {r['letters']}  yoo {r['yoo']['glide']} (gap {r['yoo']['gap_ms']})  I on ga {r['on_note']}" if "letters" in r else ""),
              flush=True)
    f.write_text(json.dumps(res, indent=1))


def rank(res, keys, R):
    """rank-sum; then two hard rules. Words: a take whose words fit no better than the original's goes last, but only
    where the two texts are about as long (CTC loss grows with the letters: L16's new words have 12 more than "atoms").
    Hold (L16): the user asked for "the -ing of rearranging" to be higher (L16K), so a take more than hold_rule cents
    off the original's held note ranks below every take that holds it."""
    n_old = len(R["orig_sp"].replace(" ", ""))
    score = {k: 0.0 for k in keys}
    crit = [(2, lambda r: r["rhythm"]), (1.5, lambda r: -r["hnr"]), (1, lambda r: r["cents"]), (1, lambda r: r["hold"]),
            (1, lambda r: r["words"]), (0.5, lambda r: r["width"] + r["level"])]
    if "letters" in R:  # L21: the I on the original's note, in time and pitch, and the U's "yoo"
        crit += [(1, lambda r: abs(r["on_note"]["dt_ms"])), (1, lambda r: abs(r["on_note"]["cents"] or 999)),
                 (1, lambda r: not r["yoo"]["glide"]),
                 (1, lambda r: np.mean([abs(x) for x in r.get("letters_on", {}).values() if x is not None] or [999]))]
    if R.get("soon"):  # L19: "soon" on gloom's notes and length, the k as long as the current's
        ck = res["current"]["soon"]["k_gap_ms"]
        crit += [(1, lambda r: r["soon"]["soon_cents"] if r["soon"]["soon_cents"] is not None else 999),
                 (1, lambda r: abs(r["soon"]["soon_ms"] - r["soon"]["gloom_ms"])), (0.5, lambda r: abs(r["soon"]["k_gap_ms"] - ck))]
    for w, f in crit:
        for i, k in enumerate(sorted(keys, key=lambda k: f(res[k]) if np.isfinite(f(res[k])) else 1e9)):
            score[k] += w * i
    same_len = lambda k: abs(len(res[k]["sp"].replace(" ", "")) - n_old) <= 4
    hold_bad = lambda k: R.get("hold_rule") is not None and not (abs(res[k]["hold_signed"]) <= R["hold_rule"])
    ai_bad = lambda k: res[k].get("ai_two_letters", 1.0) < 0.5  # L37A: "A-I" not clearly two letters
    letters_bad = lambda k: res[k].get("letters", {}).get("weakest", 1.0) < 0.5  # L21: a letter swallowed
    # L21: the brief is the stressed I on its note ("ga", round 36 "Point's"); the rhythm against the original's syllables
    # counts the new layout against a take, so the I within 80 ms and 100 cents of that note comes first
    def on_bad(k):
        o = res[k].get("on_note")
        return o is not None and not (abs(o["dt_ms"]) <= 80 and o["cents"] is not None and abs(o["cents"]) <= 100)
    # L19: the s of "income's" missing (under 50 ms) or hissier than the s of "basic" by more than 3 dB
    s_bad = lambda k: "soon" in res[k] and (res[k]["soon"]["s_ms"] < 50 or (res[k]["soon"]["s_vs_basic_db"] or 0) > 3)
    return sorted(keys, key=lambda k: (same_len(k) and res[k]["margin"] <= 0, ai_bad(k), letters_bad(k), on_bad(k), s_bad(k),
                                       hold_bad(k), score[k]))


def file(label):
    R, W = cfg(label)
    res = json.loads((W / "measure.json").read_text())
    takes_ = [k for k in res if k != "current"]
    order = rank(res, takes_, R)
    out = DESK / R["folder"]
    out.mkdir(parents=True, exist_ok=True)
    src = lambda k: next(W.glob(f"{R.get('clip', label)} {k} - *.mp3"))
    refs_ = [("original", f"{label} original (as in v13, in the video) - {R['orig']}.mp3")] if R.get("no_current") else \
            [("original", f"{label} original - {R['orig']}.mp3"),
             ("current", f"{label} current ({R.get('base', 'pdoom_EU_v12.wav')[9:12]}, in the video) - "
                         f"{R.get('cur_text') or (R['orig'] if label == 'L37' else R['lyrics']['AC']['text'])}.mp3")]
    for k, name in refs_:
        if not (out / name).exists():
            shutil.copy(src(k), out / name)
    # names already filed stay (the user may have heard them); new takes continue the numbers, the takes of a round
    # with a reference take ("ref") in their own order (the glide first, then closest to the reference)
    nf = W / "names.json"
    names = json.loads(nf.read_text()) if nf.exists() else {}
    refd = {k: L for k, L in R["lyrics"].items() if "ref" in L}
    def ref_order(key):
        ks = [k for k in takes_ if res[k]["lyric"] == key]
        sc = {k: 0.0 for k in ks}
        for w, f in [(2, lambda r: r["vs_ref"]["rhythm"]), (1, lambda r: r["vs_ref"]["cents"]), (1, lambda r: -r["vs_ref"]["hnr"]),
                     (1, lambda r: r["yai"]["gap_ms"] if r["yai"]["gap_ms"] is not None else 999)]:
            for i, k in enumerate(sorted(ks, key=lambda k: f(res[k]))):
                sc[k] += w * i
        return sorted(ks, key=lambda k: (not res[k]["yai"]["glide"], not res[k]["yai"]["j"], sc[k]))
    new = [k for k in order if k not in names and res[k]["lyric"] not in refd] + [k for key in refd for k in ref_order(key) if k not in names]
    n0 = max((int(v[len(label) + 1:]) for v in names.values()), default=0)
    for i, k in enumerate(new, n0 + 1):
        names[k] = f"{label}v{i}"
    for k in order:
        f = out / f"{names[k]} - {res[k]['text']}.mp3"
        if not f.exists():
            shutil.copy(src(k), f)
    nf.write_text(json.dumps(names, indent=1))
    ai = label == "L37"
    seam_max = max(abs(db) for k in takes_ for _, db in (res[k]["seams"] or [[0, 0]]))
    hdr = (f"{'rank':>4}  {'clip':7}  {'take':8}  {'lyric':30}  {'rhythm ms':>9}  {'worst':>5}  {'pitch c':>7}  {'hold c':>6}  "
           f"{'clarity dB':>10}  {'words':>5}" + (f"  {'A-I':>4}  " if ai else "") + "  spelling")
    def row(i, k):
        r = res[k]
        return (f"{i:>4}  {names.get(k, 'current'):7}  {k:8}  {r['text'][:30]:30}  {r['rhythm']:9.0f}  {r['rhythm_max']:5d}  {r['cents']:7.0f}  "
                f"{r['hold_signed']:+6.0f}  {r['hnr']:+10.1f}  {r['words']:5.0f}"
                + (f"  {r['ai_two_letters']:4.2f}" if ai and "ai_two_letters" in r else ("      " if ai else "")) + f"  {r['spell']}")
    table = [hdr, "-" * len(hdr)] + [row(i, k) for i, k in enumerate(order, 1)] + [row(0, "current").replace("   0", "   -", 1)]
    why = lambda k: (f"rhythm {res[k]['rhythm']:.0f} ms off the original's syllables, pitch {res[k]['cents']:.0f} c, "
                     f"{R['hold_name']} {res[k]['hold_signed']:+.0f} c, clarity {res[k]['hnr']:+.1f} dB, words {res[k]['words']:.0f}"
                     + (f", A-I {res[k]['ai_two_letters']:.2f}" if "ai_two_letters" in res[k] else "")
                     + (f", letters {'/'.join(str(x) for x in res[k]['letters']['each'])} (rest {res[k]['letters']['rest']}), "
                        f"'yoo' {'yes' if res[k]['yoo']['glide'] else 'no'}, the I {res[k]['on_note']['dt_ms']:+d} ms / "
                        f"{'?' if res[k]['on_note']['cents'] is None else format(res[k]['on_note']['cents'], '+d')} c from '{res[k]['on_note'].get('name', 'ga')}'"
                        if "letters" in res[k] else ""))
    tops = []
    for key, L in R["lyrics"].items():
        if "ref" in L:
            ref = L["ref"]; rr = res[ref]["yai"]
            ks = ref_order(key)
            num = lambda x, fmt: "-" if x is None else format(x, fmt)
            yrow = lambda k: (f"  {names[k]:7}  {k:8}  {'yes' if res[k]['yai']['glide'] else 'no':5}  "
                              f"{num(res[k]['yai']['gap_ms'], 'd'):>6}  {num(res[k]['yai']['dip_db'], '+.1f'):>6}  "
                              f"{'yes' if res[k]['yai']['j'] else 'no':4}  {res[k]['vs_ref']['rhythm']:9.0f}  {res[k]['vs_ref']['cents']:7.0f}  "
                              f"{res[k]['vs_ref']['hnr']:+10.1f}  {res[k]['spell']}")
            glided = [k for k in ks if res[k]["yai"]["glide"]]
            tops.append(
                f"CLOSEST TO {names[ref]} ({ref}) BUT WITH THE YAI, round 33 (\"{L['text']}\" sung ay-YAI)\n"
                f"  {names[ref]} itself: the A reaches the /j/ position (F1 {rr['f1_j']} Hz) but the voicing stops for {rr['gap_ms']} ms "
                f"({rr['dip_db']:+.1f} dB) before the I's /a/: no glide.\n"
                + "\n".join(f"  {i}. {names[k]} ({k}): " + ("the glide is there" if res[k]["yai"]["glide"] else
                     ("reaches the /j/ but breaks for " + str(res[k]["yai"]["gap_ms"]) + " ms" if res[k]["yai"]["j"] else "no /j/ (\"ah-ai\")"))
                     + f"; against {names[ref]}: rhythm {res[k]['vs_ref']['rhythm']:.0f} ms, pitch {res[k]['vs_ref']['cents']:.0f} c, "
                     f"clarity {res[k]['vs_ref']['hnr']:+.1f} dB" for i, k in enumerate(ks[:3], 1))
                + (f"\n  Only {len(glided)} of the {len(ks)} new takes {'has' if len(glided) == 1 else 'have'} the glide." if len(glided) < 3 else "")
                + f"\n\n  {'clip':7}  {'take':8}  {'yai':5}  {'gap ms':>6}  {'dip dB':>6}  {'/j/':4}  {'rhythm ms':>9}  {'pitch c':>7}  {'clarity dB':>10}  spelling"
                + f"\n  (against {names[ref]})\n" + "\n".join(yrow(k) for k in [ref] + ks))
            continue
        nt = R.get("top_per_lyric", 3)
        ks = [k for k in order if res[k]["lyric"] == key and res[k]["text"] == L["text"]][:nt]
        tops.append((f"TOP 3, \"{L['text']}\"\n" if nt == 3 else f"TOP PICK, \"{L['text']}\"\n")
                    + "\n".join(f"  {i}. {names[k]} ({k}): {why(k)}" for i, k in enumerate(ks, 1)))
        for i, (txt, _) in L.get("literal", {}).items():
            lit = [names[k] for k in order if res[k]["lyric"] == key and res[k]["text"] == txt]
            tops[-1] += (f"\n  {L['literal_note'].format(txt=txt, clips=', '.join(lit))}" if "literal_note" in L else
                         f"\n  The literal \"{txt}\" stretched over the whole line (no \"super-dense\"): {', '.join(lit)}; its"
                         f" rhythm can't match the original's syllables, so it ranks by ear, not by the table")
    if R.get("overall"):
        tops.insert(0, "OVERALL TOP 3\n" + "\n".join(f"  {i}. {names[k]} ({k}, \"{res[k]['text']}\"): {why(k)}"
                                                        for i, k in enumerate(order[:3], 1)))
    if R.get("soon"):
        num = lambda x, f: "-" if x is None else format(x, f)
        sr = lambda name, k: (f"  {name:8}  {k:8}  {res[k]['soon']['s_ms']:5d}  {num(res[k]['soon']['s_vs_basic_db'], '+.1f'):>7}  "
                              f"{res[k]['soon']['k_gap_ms']:5d}  {num(res[k]['soon']['soon_cents'], 'd'):>6}  {res[k]['soon']['soon_ms']:5d} / "
                              f"{res[k]['soon']['gloom_ms']}  {res[k]['text']}")
        tops.append("THE S OF \"INCOME'S\", THE K, \"SOON\" ON GLOOM'S NOTES\n"
                    f"  {'clip':8}  {'take':8}  {'s ms':>5}  {'s vs basic':>7}  {'k ms':>5}  {'cents':>6}  soon / gloom ms  lyric\n"
                    + "\n".join([sr("current", "current")] + [sr(names[k], k) for k in order]))
    if "letters" in R:
        num = lambda x, f: "-" if x is None else format(x, f)
        if R.get("top_per_lyric", 3) < 3 and len(R["lyrics"]) > 1:
            tops.insert(0, "OVERALL TOP 3\n" + "\n".join(f"  {i}. {names[k]} ({k}, \"{res[k]['text']}\"): {why(k)}"
                                                            for i, k in enumerate(order[:3], 1)))
        for key, L in R["lyrics"].items():
            Lc, ks = L["letters"], [k for k in order if res[k]["lyric"] == key]
            nl = len(Lc["word"].split())
            clear = [k for k in ks if res[k]["letters"]["weakest"] >= 0.5]
            on = [k for k in ks if abs(res[k]["on_note"]["dt_ms"]) <= 60]
            late = [k for k in ks if res[k]["on_note"]["dt_ms"] > 150]
            verdict = (f"  {len(clear)} of {len(ks)} takes sing every letter clearly; {len(on)} put the I on \"{Lc['on_name']}\"'s beat"
                       f" ({', '.join(names[k] for k in on) or 'none'}); {len(late)} 150 ms or more later. "
                       + ("No take does both.\n" if not set(clear) & set(on) else
                          f"Both: {', '.join(names[k] for k in ks if k in set(clear) & set(on))}.\n"))
            heads = [w.upper()[:5] for w in Lc["word"].split()]
            tops.append(f"\"{L['text']}\": LETTERS, THE 'YOO', THE I ON \"{Lc['on_name']}\"\n" + verdict +
                        f"  {'clip':7}  {'take':8}  " + "  ".join(f"{h:>5}" for h in heads) + f"  {'rest':>5}  {'weakest':>7}  {'yoo':4}  "
                        f"{'gap ms':>6}  {'I dt ms':>7}  {'I cents':>7}  letters before the I, ms off their notes  sung as\n"
                        + "\n".join(f"  {names[k]:7}  {k:8}  " + "  ".join(f"{x:5.2f}" for x in res[k]['letters']['each'])
                                     + f"  {res[k]['letters']['rest']:5.2f}  {res[k]['letters']['weakest']:7.2f}  "
                                     f"{'yes' if res[k]['yoo']['glide'] else 'no':4}  {num(res[k]['yoo']['gap_ms'], 'd'):>6}  "
                                     f"{res[k]['on_note']['dt_ms']:+7d}  {num(res[k]['on_note']['cents'], '+d'):>7}  "
                                     + f"{' '.join(f'{a_}{num(v, chr(43) + chr(100))}' for a_, v in res[k].get('letters_on', {}).items()):40}  "
                                     + res[k]['letters']['spelling'] for k in ks))
    ref = res[order[0]]["words_ref"]
    (out / "README.txt").write_text(
        f"{label}: new takes, 1 Oct 2026. Original: \"{R['orig']}\". In the video now: {R['cur_desc']}.\n\n"
        "Each take was generated over the line (conditioned low on the original), spliced the way L9-10 and L11/L12 were\n"
        "(the whole line untouched: no tuning, no warp; BS-RoFormer split; centre and sides levelled) and measured against\n"
        "the original singer. The lyric is in each file name. Clips are numbered best first; names already filed stay as\n"
        "they were, so a later round continues the numbers in its own order (shown in its section).\n\n"
        + "\n\n".join(tops) + "\n\nALL, CLOSEST TO THE ORIGINAL FIRST\n" + "\n".join(table) + "\n\n"
        + ("yai      the /j/ glide from A into I (glide.py, Praat formants): the A must reach the /j/ position (F1 under 480 Hz,\n"
         "         F2 over 1800 Hz) and run into the I's /a/ with at most 20 ms unvoiced (gap) and no deeper dip than -12 dB\n"
         if any("ref" in L for L in R["lyrics"].values()) else "")
        + "rhythm   for each of the original's syllables, how far the take's nearest syllable onset is, ms (mean; worst)\n"
        "pitch    median distance from the original's notes per word, cents (100 = a semitone)\n"
        f"hold c   {R['hold_name']}, the held end: cents against the original's note (+ = higher)\n"
        "clarity  Praat harmonicity against the original's, dB; below 0 reads rough or smeared\n"
        f"words    CTC fit of the take's own words, lower = clearer; the original singing its own words scores {ref:.0f}\n"
        + ("s / k    the s of \"income's\" (unvoiced, over 4 kHz, between -come and soon): its length and peak level against the\n"
           "         s of \"basic\" in the same clip (audible, not hissier: within +3 dB); k = the closure of \"in-come\" (current 60 ms)\n"
           "soon     its pitch against the current \"gloom\" over gloom's notes (62.10-62.54 s), and its voiced length\n"
           "Whole line new: the take from \"I hear\" on. Only -come's soon new: the current singer to the k of \"in-come\", the take\n"
           "from there (the cut in the k's silence).\n" if R.get("soon") else "")
        + ("letters  each of U, B, I: CTC confidence of its letters in the alignment of the whole line (spelled \"you bee eye\",\n"
           "         \"u b i\" or \"yu bee i\", whichever fits best); rest = the line's other letters; a weakest under half the\n"
           "         rest's = a letter swallowed (those rank below)\n"
           "yoo      the U's /j/ glide into its /u/ (glide.py, as for EU: F2 from over 1900 Hz to under 1700 Hz, <= 20 ms gap)\n"
           "I dt/c   the I's vowel onset (ms) and pitch (cents) against the original's syllable it should replace (round 35:\n"
           "         \"ga\"; round 36: \"Point's\", the strong beat); the letters before it against O-me-ga the same way\n"
           if "letters" in R else "")
        + ("A-I      how clearly \"A-I\" comes out as two letters: in the CTC alignment of the whole line, the weaker of the A\n"
           "         and the I against the line's other letters (spelled \"ay i\", \"ay eye\" or \"a i\", whichever fits best);\n"
           "         1 = as clear as the rest, under 0.5 = one letter swallowed (those rank below the takes that sing both)\n" if ai else "")
        + ("Ranking: first the takes that sing every letter clearly with the I within 80 ms and 100 cents of its note; then\n"
           "rank-sum, rhythm x2, clarity x1.5, pitch, hold and words x1, width/level x0.5 (the rhythm is against the original's\n"
           "syllables, so the new layout of round 36 counts against it)" if "letters" in R else
           "Ranking: rank-sum, rhythm x2, clarity x1.5, pitch, hold and words x1, width/level x0.5")
        + (f"; takes more than {R['hold_rule']} cents off the\noriginal's {R['hold_name']} rank below those that hold it (you asked for the -ing higher before)"
           if R.get("hold_rule") else "") + ". Whisper mishears these short\n"
        f"isolated vocals, so it isn't used. Seams: at both splice points every take is within {seam_max:.1f} dB of {R.get('base', 'pdoom_EU_v12.wav')[9:12]}.\n")
    print("\n".join(table)); print("\n\n".join(tops))
    subprocess.run(["open", str(out)])


if __name__ == "__main__":
    label, step = sys.argv[1], sys.argv[2]
    {"build": build, "measure": measure, "file": file}[step](label, *sys.argv[3:])
