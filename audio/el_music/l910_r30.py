"""Round 30, L9-10 "Trapped in the Brussels room, where the faxes zoom" on the path that made L11/L12 smooth (final15.py):
each take's whole span untouched (no tune, no warp) on the BS-RoFormer split, its centre and sides levelled to the
original singer's, spliced into v11. The eu30 takes plus eu2_low4 (v11's take, there mid-tuned on Demucs) and eu2_low3
on the same path, for comparison.
  build    clips "L9-10 <take> - ..." in analysis/work/l910_r30, with the original and v11's current line cut the same
  measure  every clip against the original, on the BS-RoFormer vocal of each clip (compare.py):
             timing  each syllable's vowel onset (CTC, sylfit.vowels) against the original's syllable for syllable
                     (Chi|nese = Brus|sels, with a bag of shrooms = where the fax|es zoom), ms
             pitch   per word, cents against the original (Praat), compare.table
             clarity Praat harmonicity (HNR) over the line against the original's, dB: smear and phasiness read low
             m       "zoom" closing on its m: 1-4 kHz against 100-600 Hz over the last 80 ms of the note against its
                     vowel, dB (the original's "shroo-m" darkens as the lips shut)
             words   Whisper large-v3-turbo on the vocal; CTC margin of the new words over the old
             seams   level at both splice points against v11 and the original, dB
           ranks them and files the clips best first in Desktop/suno_test/"eu_v11_L9-10 - all versions" with a README.
Round 30b (the user: "a couple more runs of the same verse"): eu30_10-18, the same chunk and spellings, added to the
same folder; the clips already filed keep their names (the user may have heard them), the new ones continue the numbers.
Run from audio/el_music with the analysis venv: l910_r30.py build|measure [take ...] | file"""
import json, pathlib, shutil, subprocess, sys, tempfile
import numpy as np, librosa, soundfile as sf

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
WORK = HERE.parents[1] / "analysis/work/l910_r30"
WORK.mkdir(parents=True, exist_ok=True)
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_v11_L9-10 - all versions"
TEXT = "Trapped in the Brussels room, where the faxes zoom"
ORIG = "Trapped in the Chinese room, with a bag of shrooms"
TAKES = [f"eu30_{k}" for k in range(1, 10)] + ["eu2_low4", "eu2_low3"] + [f"eu30_{k}" for k in range(10, 19)]
SPELL = {1: "plain", 2: "Brus-sels / fax-es hyphenated", 0: "BRUS-sels / FAX-es / ZOOM stressed"}


def mp3(y, sr, path):
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/x.wav", y.T, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/x.wav", "-af",
                        "afade=t=in:d=0.05,areverse,afade=t=in:d=0.1,areverse", "-b:a", "256k", str(path)], check=True)


def build(*only):
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    import final12, l910
    a, b = bounds(l910.N)
    cut = lambda y: y[:, int((a - 0.8) * V.SR):int((b + 0.5) * V.SR)]
    v11 = librosa.load(HERE / "pdoom_EU_v11.wav", sr=V.SR, mono=False)[0][:, : V.mix.shape[1]]
    mp3(cut(V.mix), V.SR, WORK / f"L9-10 original - {ORIG}.mp3")
    mp3(cut(v11), V.SR, WORK / f"L9-10 current - {TEXT}.mp3")
    f = WORK / "seams.json"
    seams = json.loads(f.read_text()) if f.exists() else {}
    for take in only or TAKES:
        Y = hooked(ms(None, l910.N), l910.N, take, l910.PLAN, "bsroformer", VO_R)
        out, span = paste(v11, Y, a, b)
        mp3(cut(out), V.SR, WORK / f"L9-10 {take} - {TEXT}.mp3")
        seams[take] = [[round(float(t), 3), round(float(final12.seam_db(out, v11, t)), 1), round(float(final12.seam_db(out, V.mix, t)), 1)] for t in span]
        print(take, "span", [round(t, 3) for t in span], "seams (t, vs v11, vs original)", seams[take], flush=True)
    (WORK / "seams.json").write_text(json.dumps(seams, indent=1))


def vowel_grid(voc, t0, text):
    """vowel onset (s, song time) of each syllable of text sung in the clip's vocal, inside the line only"""
    import sylfit
    a, b = 26.32 - 0.12, 29.907 + 0.15
    m = voc.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]
    return sylfit.vowels(m, a, text)


def hnr(voc, t0):
    import parselmouth
    a, b = 26.32, 29.907
    m = voc.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)].astype(np.float64)
    h = parselmouth.Sound(m, 44100).to_harmonicity_cc(time_step=0.01, minimum_pitch=90)
    v = h.values[0]
    return float(np.mean(v[v > 0]))


def m_drop(voc, t0):
    """'zoom' / 'shrooms': 1-4 kHz against 100-600 Hz where the lips close (0.17-0.07 s before the note ends), minus over
    its vowel (dB); negative = darkens onto the m"""
    m = voc.mean(0)
    P = np.abs(librosa.stft(m, n_fft=2048, hop_length=441)) ** 2
    f = librosa.fft_frequencies(sr=44100, n_fft=2048)
    t = t0 + np.arange(P.shape[1]) * 0.01
    lvl = 10 * np.log10(P[(f > 100) & (f < 8000)].sum(0) + 1e-10)
    ratio = 10 * np.log10(P[(f > 1000) & (f < 4000)].sum(0) + 1e-10) - 10 * np.log10(P[(f > 100) & (f < 600)].sum(0) + 1e-10)
    w = (t > 29.25) & (t < 29.88)  # L11's "See" starts at 29.91
    on = w & (lvl > lvl[w].max() - 15)
    end = t[on].max()
    close = (t > end - 0.17) & (t <= end - 0.07)  # the original: lips shut 29.56-29.64, released by 29.74
    vowel = (t > end - 0.45) & (t <= end - 0.27)
    return float(np.mean(ratio[close]) - np.mean(ratio[vowel])), float(end)


def heard(voc, t0):
    import mlx_whisper
    a, b = 26.32 - 0.1, 29.907 + 0.1
    m = voc.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]
    with tempfile.NamedTemporaryFile(suffix=".wav") as tf:
        sf.write(tf.name, librosa.resample(m, orig_sr=44100, target_sr=16000), 16000)
        return mlx_whisper.transcribe(tf.name, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                      temperature=0.0, condition_on_previous_text=False)["text"].strip()


def ctc_fit(voc, t0):
    """CTC loss of the new words on the vocal: lower = the words come through clearer (the original singing its own
    words scores ~76)"""
    import lyricfit as F
    a, b = 26.32 - 0.12, 29.907 + 0.15
    m = voc.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]
    em = F.emissions(librosa.resample(m, orig_sr=44100, target_sr=22050), 22050)
    return float(F.loss(em, "TRAPPED IN THE BRUSSELS ROOM WHERE THE FAXES ZOOM"))


def ctc_margin(voc, t0):
    import lyricfit as F
    a, b = 26.32 - 0.12, 29.907 + 0.15
    m = voc.mean(0)[int((a - t0) * 44100):int((b - t0) * 44100)]
    em = F.emissions(librosa.resample(m, orig_sr=44100, target_sr=22050), 22050)
    return float(F.margin(em, "TRAPPED IN THE CHINESE ROOM WITH A BAG OF SHROOMS", "TRAPPED IN THE BRUSSELS ROOM WHERE THE FAXES ZOOM"))


def measure(*only):
    import compare as C
    C.LINES, C.WORK = WORK, WORK / "cmp"
    C.WORK.mkdir(exist_ok=True)
    C.plot = lambda *a, **k: None
    keys = [f" {t}" for t in only] if only else [" current"] + [f" {t}" for t in TAKES]
    O, rows = C.table("L9-10", keys)
    t0 = C.words("L9-10")[0]
    _, vo = C.split(C.clip("L9-10", " original"))
    g_o = vowel_grid(vo, t0, "Trapped in the Chinese room with a bag of shrooms")
    h_o, (m_o, end_o) = hnr(vo, t0), m_drop(vo, t0)
    print(f"\noriginal: vowels {[(s, round(t, 3)) for s, t in g_o]}  HNR {h_o:.1f} dB  m {m_o:+.1f} dB (end {end_o:.2f})", flush=True)
    seams = json.loads((WORK / "seams.json").read_text())
    f = WORK / "measure.json"
    res = json.loads(f.read_text()) if f.exists() else {}
    for key in keys:
        k = key.strip()
        _, vc = C.split(C.clip("L9-10", key))
        g = vowel_grid(vc, t0, "Trapped in the Brussels room where the faxes zoom")
        d = [(s, None if (tc is None or to is None) else round((tc - to) * 1000)) for (s, tc), (_, to) in zip(g, g_o)]
        dd = np.array([x for i, (_, x) in enumerate(d) if x is not None and i != 1])  # "-ped" has no vowel of its own
        cents = np.array([r["cents"] for r in rows[key]["words"]])
        cents = (cents + 600) % 1200 - 600  # Praat's octave jumps folded out
        width = np.array([r["width"] for r in rows[key]["words"]])
        lvl = np.array([r["lvl"] for r in rows[key]["words"]])
        m, end = m_drop(vc, t0)
        r = dict(timing_ms=float(np.mean(np.abs(dd))), timing_max=int(np.max(np.abs(dd))), syl=d,
                 cents=float(np.nanmedian(np.abs(cents))), cents_words={w["w"]: round(w["cents"]) if np.isfinite(w["cents"]) else None for w in rows[key]["words"]},
                 width=float(np.mean(np.abs(width))), level=float(np.mean(np.abs(lvl))),
                 hnr=hnr(vc, t0) - h_o, m=m, m_orig=m_o, end=end, end_orig=end_o,
                 heard=heard(vc, t0), ctc=ctc_margin(vc, t0), ctc_loss=ctc_fit(vc, t0), seams=seams.get(k))
        res[k] = r
        print(f"{k:10s} timing {r['timing_ms']:4.0f} ms (max {r['timing_max']})  pitch {r['cents']:4.0f} c  HNR {r['hnr']:+.1f} dB  "
              f"m {r['m']:+.1f} (orig {m_o:+.1f})  width {r['width']:.1f}  lvl {r['level']:.1f}  ctc {r['ctc']:+.2f}  heard: {r['heard']}",
              flush=True)
        print(f"           syllables (ms vs original): {d}", flush=True)
    (WORK / "measure.json").write_text(json.dumps(res, indent=1))


def rank(res):
    """rank-sum over the measures (lower is better); a take whose words don't win over the original's (CTC margin
    under 10) goes last. Weights: rhythm 2, roughness 1.5, pitch 1, the m 1, words (absolute CTC fit) 1, width/level 0.5"""
    keys = [k for k in res if k != "current"]
    score = {k: 0.0 for k in keys}
    crit = {"timing_ms": (2, lambda r: r["timing_ms"]), "hnr": (1.5, lambda r: -r["hnr"]), "cents": (1, lambda r: r["cents"]),
            "m": (1, lambda r: max(0.0, r["m"] - r["m_orig"])), "words": (1, lambda r: r["ctc_loss"]),
            "mix": (0.5, lambda r: r["width"] + r["level"])}
    for w, f in crit.values():
        order = sorted(keys, key=lambda k: f(res[k]))
        for i, k in enumerate(order):
            score[k] += w * i
    return sorted(keys, key=lambda k: (res[k]["ctc"] < 10, score[k]))


# the names the first round was filed under (the user may have heard them; they stay)
FILED = {"eu30_4": 1, "eu30_8": 2, "eu30_7": 3, "eu30_9": 4, "eu30_3": 5, "eu30_6": 6, "eu30_1": 7, "eu30_5": 8,
         "eu2_low4": 9, "eu30_2": 10, "eu2_low3": 11}


def file():
    res = json.loads((WORK / "measure.json").read_text())
    order = rank(res)
    nf = WORK / "names.json"
    names = json.loads(nf.read_text()) if nf.exists() else dict(FILED)
    for k in order:  # takes not filed yet: the next numbers, best first
        if k not in names:
            names[k] = max(names.values()) + 1
    nf.write_text(json.dumps(names, indent=1))
    DESK.mkdir(parents=True, exist_ok=True)
    src = lambda k: next(WORK.glob(f"L9-10 {k} - *.mp3"))
    put = lambda k, name: (DESK / name).exists() or shutil.copy(src(k), DESK / name)
    put("original", f"L9-10 original - {ORIG}.mp3")
    put("current", f"L9-10 current (v11, in the video) - {TEXT}.mp3")
    new = []
    for k in order:
        if not (DESK / f"L9-10v{names[k]} - {TEXT}.mp3").exists():
            new.append(k)
        put(k, f"L9-10v{names[k]} - {TEXT}.mp3")
    how = lambda k: (SPELL[int(k.split("_")[1]) % 3] if k.startswith("eu30") else "v11's take" if k == "eu2_low4" else "round-2 take")
    hdr = f"{'rank':>4}  {'clip':9}  {'take':9}  {'rhythm ms':>9}  {'worst':>5}  {'pitch c':>7}  {'clarity dB':>10}  {'zoom m dB':>9}  {'words':>5}  spelling"
    row = lambda i, k, r: (f"{i:>4}  {'L9-10v' + str(names[k]) if k in names else 'current':9}  {k:9}  {r['timing_ms']:9.0f}  {r['timing_max']:5d}  "
                           f"{r['cents']:7.0f}  {r['hnr']:+10.1f}  {r['m']:+9.1f}  {r['ctc_loss']:5.0f}  {how(k) if k in names else 'eu2_low4 mid-tuned on Demucs'}"
                           + ("   NEW" if k in new else ""))
    table = [hdr, "-" * len(hdr)] + [row(i, k, res[k]) for i, k in enumerate(order, 1)] + [row(0, "current", res["current"]).replace("   0", "   -", 1)]
    r0 = res[order[0]]
    why = lambda k: (f"rhythm {res[k]['timing_ms']:.0f} ms off, pitch {res[k]['cents']:.0f} c, clarity {res[k]['hnr']:+.1f} dB, "
                     f"zoom m {res[k]['m']:+.1f} dB, words {res[k]['ctc_loss']:.0f}")
    top = "\n".join(f"  {i}. L9-10v{names[k]} ({k}): {why(k)}" for i, k in enumerate(order[:3], 1))
    (DESK / "README.txt").write_text(
        "L9-10 \"Trapped in the Brussels room, where the faxes zoom\": round 30, 1 Oct 2026\n\n"
        "Takes eu30_1-18 (one chunk over both lines, conditioned low on the original; spellings by take) and the old ones,\n"
        "each spliced the way L11/L12 were (whole span untouched: no tuning, no warp; BS-RoFormer split; centre and sides\n"
        "levelled) and measured against the original singer. Clip numbers are only names: v1-v11 are the first round's\n"
        "(kept as they were), v12 on the second round's. The table is the ranking, closest to the original first.\n\n"
        f"TOP 3\n{top}\n\n"
        "ALL, CLOSEST TO THE ORIGINAL FIRST\n" + "\n".join(table) + "\n\n"
        "rhythm   mean distance of each syllable's vowel onset from the original's, syllable for syllable (Chi|nese =\n"
        "         Brus|sels, with a bag of shrooms = where the fax|es zoom), ms; worst = the furthest syllable\n"
        "pitch    median distance from the original's notes per word, cents (100 = a semitone)\n"
        "clarity  Praat harmonicity against the original's, dB; below 0 reads rough or smeared\n"
        f"zoom m   how much 'zoom' darkens as the lips close, dB; the original's 'shrooms' {r0['m_orig']:+.1f}; above 0 = no m\n"
        "words    CTC fit of the new words, lower = clearer; the original singing its own words scores 76\n"
        "Ranking: rank-sum, rhythm x2, clarity x1.5, pitch, zoom m and words x1, width/level x0.5. Seams at 26.24 s and\n"
        "29.914 s are 0.0 dB against v11 for every take. Whisper mishears these short isolated vocals, so it isn't used.\n")
    print("\n".join(table)); print("top 3:\n" + top); print("new:", new)
    subprocess.run(["open", str(DESK)])


if __name__ == "__main__":
    {"build": build, "measure": measure, "file": file}[sys.argv[1]](*sys.argv[2:])
