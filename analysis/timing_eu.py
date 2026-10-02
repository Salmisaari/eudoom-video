"""Timing map of everything in the EU edition (the song in audio/pdoom_eu.mp3, built as pdoom_EU_v9.wav)
-> data/timing_eu.json, for the kinetic-type cut (app/src/scenes/typo.ts). Stages, each cached in work/eu/:
  vocal    BS-RoFormer split of the whole song (stems/bsroformer/pdoom_eu_v9_vocals.wav)
  whisper  mlx-whisper large-v3-turbo and large-v3 word stamps on the vocal: an independent cross-check
  ctc      wav2vec2 LV60K CTC log-probs of the vocal (20 ms frames, 20 s chunks with 3 s context)
  words    the display words of every line (the EU lyric where re-sung) on their verified windows
           (data/lyrics.json; data/eu_words.json where the re-sung line has its own timing; else CTC on this vocal),
           letters by forced alignment inside each word, syllables from the letters (onsets snapped to the vocal's
           own onsets within 40 ms), sung notes (Praat f0, 10 ms), loudness
  music    beats, downbeats, sections, kick/snare/hat onsets (data/audio.json: the band is the original's), plus
           bass and synth onsets from the Demucs stems and the EU vocal's envelope
Run: cd analysis && uv run python timing_eu.py [stage ...]"""
import common
import json, re, sys
import numpy as np, soundfile as sf

EU = common.PROJECT / "audio" / "el_music"
# v14 (1 Oct 2026: v13 + L7 EUv1 eu34_L7_5, "EU doom" sung ee-YOO); earlier caches stay in work/eu, work/eu_v10..v13
SONG = EU / "pdoom_EU_v14.wav"
VOC = common.ROOT / "stems" / "bsroformer" / "pdoom_eu_v14_vocals.wav"
OUT = common.WORK / "eu_v14"
OUT.mkdir(exist_ok=True)
SR = 44100
FRAME = 0.02


def vocal():
    if not VOC.exists():
        sys.path.insert(0, str(EU))
        import rof
        y = sf.read(SONG, dtype="float32", always_2d=True)[0].T
        sf.write(VOC, rof._run(y).T, SR)
    return sf.read(VOC, dtype="float32", always_2d=True)[0].T


def vocal16():
    f = OUT / "vocal16k.wav"
    if not f.exists():
        import soxr
        v = vocal().mean(0)
        sf.write(f, soxr.resample(v, SR, 16000), 16000)
    return f


def whisper():
    import mlx_whisper
    prompt = ("Song lyrics: I'm upping my EU doom. Brussels room, faxes zoom, shoggoth, shinigami, AC temperatures, "
              "Cookies, basic income gloom, Nokia to the moon, Omega Point, SAP, privacy in chats, GDPR, NATO, PTO, "
              "unicorns, Chinchilla, GPU, EU Inc, Draghi, Loom.")
    for tag, repo in (("turbo", "mlx-community/whisper-large-v3-turbo"), ("large", "mlx-community/whisper-large-v3-mlx")):
        f = OUT / f"whisper_{tag}.json"
        if f.exists():
            continue
        res = mlx_whisper.transcribe(str(vocal16()), path_or_hf_repo=repo, language="en", word_timestamps=True,
                                     condition_on_previous_text=False, initial_prompt=prompt, temperature=0.0,
                                     no_speech_threshold=None, hallucination_silence_threshold=None)
        f.write_text(json.dumps(res, default=float))
        for s in res["segments"]:
            print(f"{tag} {s['start']:7.2f} {s['end']:7.2f} {s['text']}", flush=True)


def ctc():
    f = OUT / "emission_lv60k.npy"
    if f.exists():
        return np.load(f)
    import torch, torchaudio
    B = torchaudio.pipelines.WAV2VEC2_ASR_LARGE_LV60K_960H
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    model = B.get_model().to(dev).eval()
    y = sf.read(vocal16(), dtype="float32")[0]
    y = y / (np.abs(y).max() + 1e-9)
    hop, chunk, ctx = 320, 20 * 16000, 3 * 16000
    n = len(y) // hop
    out = np.full((n, len(B.get_labels())), np.nan, np.float32)
    for s in range(0, len(y), chunk):
        a, b = max(0, s - ctx), min(len(y), s + chunk + ctx)
        with torch.inference_mode():
            em, _ = model(torch.from_numpy(y[a:b])[None].to(dev))
            em = torch.log_softmax(em, -1)[0].float().cpu().numpy()
        lo, hi = s // hop, min(n, (s + chunk) // hop)
        seg = em[lo - a // hop: hi - a // hop]
        out[lo:lo + len(seg)] = seg
        print("ctc", s / 16000, flush=True)
    last = np.where(~np.isnan(out[:, 0]))[0].max()
    out[last + 1:] = out[last]
    np.save(f, out)
    return out


# ------------------------------------------------------------------ words
SPOKEN = {"EU": "ee you", "GDPR": "gee dee pee are", "SAP": "ess ay pee", "AC": "ay see", "PTO": "pee tee oh",
          "EU's": "ee yous", "AGI": "ay gee i", "ChatGPT": "chat gee pee tee", "GPU": "gee pee you", "NATO": "gato",
          "E": "ee", "Inc": "ink", "Draghi": "dragee", "guy's": "guys"}


def eu_lyrics():
    """line number -> display text of the re-sung lines, read from animatic.ts (one source of truth)"""
    ts = (common.PROJECT / "app/src/scenes/animatic.ts").read_text()
    body = ts[ts.index("const EU_LYRICS"):]
    body = body[:body.index("};")]
    out = {}
    for m in re.finditer(r"(\d+):\s*(['\"])(.*?)\2", body):
        out[int(m.group(1))] = m.group(3).replace("\\'", "'")
    return out


def smart(s):
    return s.replace("’", "'").replace("“", '"').replace("”", '"')


def pron(tok):
    bare = re.sub(r"[^A-Za-z0-9'()\-]", "", smart(tok)).strip("'")
    key = bare.strip("-")
    if key in SPOKEN:
        return SPOKEN[key].split()
    sys.path.insert(0, str(common.ROOT))
    from pron import pron as p0
    return p0(smart(tok))


def relyric(ow, nw):
    """animatic.ts relyric(): matching prefix/suffix words keep their timings, the new words in between share the
    replaced words' span (1:1 when the counts agree, else by length)"""
    key = lambda x: "".join(c for c in x.lower() if c.isalnum())
    a = 0
    while a < len(nw) and a < len(ow) and key(nw[a]) == key(ow[a]["w"]):
        a += 1
    b = 0
    while b < len(nw) - a and b < len(ow) - a and key(nw[-1 - b]) == key(ow[-1 - b]["w"]):
        b += 1
    mid, om = nw[a:len(nw) - b], ow[a:len(ow) - b]
    if len(mid) == len(om):
        spans = [(w["start"], w["end"]) for w in om]
    else:
        t0, t1, tot, acc, spans = om[0]["start"], om[-1]["end"], sum(len(w) for w in mid), 0, []
        for w in mid:
            s0 = t0 + (t1 - t0) * acc / tot; acc += len(w); spans.append((s0, t0 + (t1 - t0) * acc / tot))
    return [(w["start"], w["end"]) for w in ow[:a]] + spans + [(w["start"], w["end"]) for w in ow[len(ow) - b:]]


_LAB = None


def labels():
    global _LAB
    if _LAB is None:
        import torchaudio
        _LAB = {c: i for i, c in enumerate(torchaudio.pipelines.WAV2VEC2_ASR_LARGE_LV60K_960H.get_labels())}
    return _LAB


def force(E, t0, t1, subs_per_word):
    """CTC forced alignment of words (each a list of pronunciation sub-words) over [t0, t1] s:
    [(word index, sub index, letter index, start s, end s, score)]"""
    import torch, torchaudio
    L = labels()
    toks, owner = [], []
    for wi, subs in enumerate(subs_per_word):
        for si, sub in enumerate(subs):
            if toks:
                toks.append(L["|"]); owner.append(None)
            for ci, ch in enumerate(sub.upper()):
                if ch in L and ch not in "-|":
                    toks.append(L[ch]); owner.append((wi, si, ci))
    f0, f1 = max(0, int(t0 / FRAME)), min(len(E), int(t1 / FRAME))
    if f1 - f0 < 2 * len(toks) + 2:
        return None
    em = torch.from_numpy(E[f0:f1]).float()[None]
    ali, sc = torchaudio.functional.forced_align(em, torch.tensor([toks]), blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
    return [(*owner[k], (f0 + s.start) * FRAME, (f0 + s.end) * FRAME, float(s.score)) for k, s in enumerate(spans) if owner[k]]


def whisper_words(tag):
    f = OUT / f"whisper_{tag}.json"
    if not f.exists():
        return []
    res = json.loads(f.read_text())
    return [(re.sub(r"[^a-z0-9]", "", w["word"].lower()), w["start"], w["end"]) for s in res["segments"] for w in s.get("words", [])]


def match_whisper(ws, line_words, a, b):
    """whisper [start, end] for each display word of a line (nearest same-text word inside the line's window)"""
    out = []
    for w in line_words:
        k = re.sub(r"[^a-z0-9]", "", smart(w["w"]).lower())
        cand = [x for x in ws if a - 0.6 <= x[1] <= b + 0.3 and (x[0] == k or (len(k) > 3 and (x[0].startswith(k[:4]) or k.startswith(x[0][:4]))))]
        best = min(cand, key=lambda x: abs(x[1] - w["start"]), default=None)
        out.append([round(best[1], 3), round(best[2], 3)] if best else None)
    return out


# Re-sung words placed from the v9 vocal itself where the relyric split or the stored timing disagreed with it
# (vocal onsets, Praat notes and CTC, checked 2026-10-01): (line, word index) -> start (the end is the next word's start)
FIXED = {
    # the hooks sing E-U where the original sang "P": EU on its syllable, doom on its "doom" syllable
    (7, 3): 23.60, (7, 4): 23.87, (18, 3): None, (18, 4): None, (29, 3): 96.32, (29, 4): 96.56, (41, 3): 125.40, (41, 4): 125.66,
    # "Nokia" starts after the cut at 62.62 (onsets 62.69/62.75, a note at 62.74; CTC 62.72)
    (20, 0): 62.70,
    # v10 (1 Oct 2026): "See through Pi-noc-chio's lies" (eu27_5; voiced 30.03 see, 30.25 through, 30.48 pi-noc, 31.12 lies)
    # and "with Eu-ro-vi-sion eyes" (eu27_3; CTC prefers these words to "with your …"; voiced 33.62 with, 33.96 Eu-ro,
    # 34.56 vi-sion, 34.83 eyes, held to 35.48)
    (11, 1): 30.18, (11, 2): 30.47, (11, 3): 31.12, (12, 0): 33.58, (12, 1): 33.94, (12, 2): 34.82,
    # "O-pen Eu-ro-pe bor-ders blues": notes at 105.95 106.14 106.39 106.69 106.84 107.04 107.26 107.53
    (34, 1): 106.37, (34, 2): 107.04, (34, 3): 107.48,
    # "Cookies, please, please let me free": both pleases are sung (Whisper large/turbo); the vocal dips at 54.3 and rises
    # at 54.37-54.42 for the first, the second is the strong onset at 56.00 (CTC 55.98)
    (17, 1): 54.37,
    # v12 (1 Oct 2026): L9-10 is eu30_17. L9 agrees with CTC within 50 ms. L10 on the v12 vocal: "the" onset 28.19 (CTC
    # 28.20); "faxes" f hiss from 28.29, vowel note 28.42; "zoom" after the unvoiced s/z hiss (29.16-29.34), its vowel
    # 29.35 (CTC 29.28)
    (10, 1): 28.19, (10, 2): 28.28, (10, 3): 29.28,
}


VOW = set("aeiouy")


def syllables(sub):
    """letter-index spans of the syllables of one pronunciation sub-word (vowel groups; silent final e; the
    consonants between two vowel groups go to the next syllable except the first of a cluster)"""
    s = sub.replace("'", "")
    n = len(s)
    isv = [c in VOW and not (c == "y" and i == 0) for i, c in enumerate(s)]
    if n > 2 and s.endswith("e") and not isv[-2] and any(isv[:-2]) and not s.endswith("le"):
        isv[-1] = False  # silent e
    groups, i = [], 0
    while i < n:
        if isv[i]:
            j = i
            while j < n and isv[j]:
                j += 1
            groups.append((i, j)); i = j
        else:
            i += 1
    if len(groups) <= 1:
        return [(0, n)]
    cuts = []
    for (a0, a1), (b0, b1) in zip(groups, groups[1:]):
        k = b0 - a1  # consonants between
        cuts.append(a1 if k <= 1 else a1 + 1)
    edges = [0] + cuts + [n]
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]


def display_split(disp, parts):
    """cut the display word into len(parts) pieces in proportion to the pronunciation's letter counts, at letter
    boundaries (acronyms: one display letter per spoken letter name)"""
    letters = [i for i, c in enumerate(disp) if c.isalnum()]
    n = len(parts)
    if n <= 1 or not letters:
        return [disp]
    tot = sum(parts)
    cuts, acc = [], 0
    for p in parts[:-1]:
        acc += p
        k = int(round(acc / tot * len(letters)))
        k = min(max(k, 1 + len(cuts)), len(letters) - (n - 1 - len(cuts)))
        cuts.append(letters[k])
    edges = [0] + cuts + [len(disp)]
    return [disp[edges[i]:edges[i + 1]] for i in range(n)]


LETTER_NAMES = {"ay", "bee", "see", "dee", "ee", "eff", "gee", "aitch", "i", "jay", "kay", "el", "em", "en", "oh", "pee",
                "cue", "are", "ar", "ess", "tee", "you", "vee", "ex", "why", "zee"}


def split_display(disp, subs, syl):
    """display pieces for the syllables: each spelled letter name takes one display letter (G-P-T), a spoken sub-word
    takes as many display letters as it has; inside a sub-word the syllables share its letters by length"""
    letters = [i for i, c in enumerate(disp) if c.isalnum()]
    spelled = [sub in LETTER_NAMES and len(subs) > 1 for sub in subs]
    need = [1 if sp else len(sub.replace("'", "")) for sub, sp in zip(subs, spelled)]
    tot = sum(need)
    # display letters per sub-word (scaled if the spelling and the display differ in length, e.g. Neumann's/noymans)
    per, acc = [], 0
    for k, nd in enumerate(need):
        a0 = round(acc / tot * len(letters)); acc += nd; a1 = round(acc / tot * len(letters))
        per.append((a0, max(a1, a0 + 1) if k == len(need) - 1 or a1 > a0 else a0 + 1))
    cuts = []
    for si, (a0, a1) in enumerate(per):
        mine = [x for x in syl if x[2] == si]
        n_l = a1 - a0
        acc2, tot2 = 0, sum(x[0] for x in mine) or 1
        for x in mine:
            cuts.append(a0 + min(n_l - 1, round(acc2 / tot2 * n_l)) if n_l else a0)
            acc2 += x[0]
    starts = [letters[min(c, len(letters) - 1)] for c in cuts]
    starts[0] = 0
    for k in range(1, len(starts)):
        if starts[k] <= starts[k - 1]:
            return [disp]
    edges = starts + [len(disp)]
    return [disp[edges[i]:edges[i + 1]] for i in range(len(starts))]


def notes_of(v, t0=0.0):
    """sung notes of a mono vocal: Praat f0 (10 ms, high octave-jump cost), split where the pitch moves by more than
    0.7 semitone from the note's running median or the voice stops; notes >= 60 ms. [(midi, start, end, dB)]"""
    import parselmouth
    p = parselmouth.Sound(v.astype(np.float64), SR).to_pitch_ac(time_step=0.01, pitch_floor=110, pitch_ceiling=1000,
                                                                 octave_jump_cost=0.8, voicing_threshold=0.45)
    f = p.selected_array["frequency"]
    ts = p.xs() + t0
    env = np.sqrt(np.convolve(v ** 2, np.ones(441) / 441, "same"))
    db = 20 * np.log10(env[np.clip((ts - t0) * SR, 0, len(v) - 1).astype(int)] + 1e-9)
    midi = np.where(f > 0, 69 + 12 * np.log2(np.maximum(f, 1) / 440), np.nan)
    notes, cur = [], []
    for k in range(len(midi)):
        m = midi[k]
        if np.isfinite(m) and db[k] > -50 and (not cur or abs(m - np.median([midi[j] for j in cur[-8:]])) < 0.7):
            cur.append(k); continue
        if len(cur) >= 6:
            notes.append(cur)
        cur = [k] if np.isfinite(m) and db[k] > -50 else []
    if len(cur) >= 6:
        notes.append(cur)
    return [(round(float(np.median(midi[c])), 2), round(float(ts[c[0]] - 0.005), 3), round(float(ts[c[-1]] + 0.005), 3),
             round(float(np.max(db[c])), 1)) for c in notes], (ts, midi, db)


def onset_peaks(v):
    import librosa
    o = librosa.onset.onset_strength(y=v, sr=SR, hop_length=220)
    pk = librosa.util.peak_pick(o, pre_max=3, post_max=3, pre_avg=10, post_avg=10, delta=o.std() * 0.3, wait=6)
    return pk * 220 / SR, o[pk] / (o.max() + 1e-9)


def words():
    import librosa
    v = vocal().mean(0)
    E = ctc()
    lyr = json.loads((common.DATA / "lyrics.json").read_text())["lines"]
    eu_timed = json.loads((common.DATA / "eu_words.json").read_text())
    EU_TXT = eu_lyrics()
    W = {tag: whisper_words(tag) for tag in ("turbo", "large")}
    notes, (pts, pmidi, pdb) = notes_of(v)
    pk, pks = onset_peaks(v)
    lines, report = [], []
    for li, L in enumerate(lyr):
        n = li + 1
        disp = EU_TXT.get(n, L["text"]).split()
        ow = L["words"]
        if n in EU_TXT:
            if str(n) in eu_timed:
                spans, src = [(a, b) for _, a, b in eu_timed[str(n)]], "eu_measured"
            else:
                spans, src = relyric(ow, disp), "relyric"
            # CTC of the display words on this vocal over the line: where the EU take sits in time
            subs = [pron(w) for w in disp]
            fa = force(E, L["start"] - 0.25, L["end"] + 0.25, subs)
            if fa:
                ctc_start = {}
                for wi, si, ci, s, e, sc in fa:
                    ctc_start.setdefault(wi, s)
            else:
                ctc_start = {}
        else:
            spans, src = [(w["start"], w["end"]) for w in ow], "verified"
            ctc_start = {}
        spans = [list(x) for x in spans]
        for wi in range(len(spans)):
            k = (n, wi)
            if k in FIXED:
                st = FIXED[k]
                if st is None:  # the hook's own original syllables (P(doom): "pee", "doom")
                    syl = ow[3].get("syl") or [[ow[3]["start"]], [ow[3]["start"] + 0.25]]
                    st = syl[0][0] if wi == 3 else syl[1][0]
                spans[wi][0] = st
                if wi:
                    spans[wi - 1][1] = st
                src = src + "+fixed" if "fixed" not in src else src
        wds = [{"w": d, "start": round(a, 3), "end": round(b, 3), "src": src} for d, (a, b) in zip(disp, spans)]
        for tag in W:
            for w, m in zip(wds, match_whisper(W[tag], wds, L["start"], L["end"])):
                w["whisper_" + tag] = m
        for wi, w in enumerate(wds):
            if wi in ctc_start:
                w["ctc_line"] = round(ctc_start[wi], 3)
        # letters inside each word's window, syllables from them
        for wi, w in enumerate(wds):
            subs = pron(w["w"])
            fa = force(E, w["start"] - 0.04, w["end"] + 0.02, [subs])
            lets = []
            if fa:
                for _, si, ci, s, e, sc in fa:
                    lets.append((si, ci, s))
            if not lets:  # too short to align: spread evenly
                k = sum(len(s) for s in subs)
                lets = [(si, ci, w["start"] + (w["end"] - w["start"]) * j / k)
                        for j, (si, ci) in enumerate((si, ci) for si, s in enumerate(subs) for ci in range(len(s)))]
            first = {}
            for si, ci, s in lets:
                first[(si, ci)] = s
            syl = []
            for si, sub in enumerate(subs):
                for a0, a1 in syllables(sub):
                    ts_ = [first[(si, c)] for c in range(a0, a1) if (si, c) in first]
                    syl.append([a1 - a0, min(ts_) if ts_ else None, si])
            # the word onset is the verified one; later syllables snap to the vocal's own onsets within 40 ms
            st = [w["start"]] + [x[1] for x in syl[1:]]
            for k in range(1, len(st)):
                if st[k] is None or not (w["start"] < st[k] < w["end"]):
                    st[k] = w["start"] + (w["end"] - w["start"]) * k / len(st)
                j = np.argmin(np.abs(pk - st[k]))
                if abs(pk[j] - st[k]) < 0.04 and w["start"] < pk[j] < w["end"]:
                    st[k] = float(pk[j])
            st = list(np.maximum.accumulate(st))
            parts = split_display(w["w"], subs, syl) if len(syl) > 1 else [w["w"]]
            if len(parts) != len(syl):
                parts, st = [w["w"]], st[:1]
            ends = st[1:] + [w["end"]]
            w["syl"] = [[p, round(a, 3), round(b, 3)] for p, a, b in zip(parts, st, ends)]
            w["letters"] = [[si, ci, round(s, 3)] for si, ci, s in sorted(lets, key=lambda x: x[2])]
            # sung notes inside the word; the longest is its hold
            wn = [x for x in notes if x[2] > w["start"] + 0.02 and x[1] < w["end"] - 0.02]
            w["notes"] = [[m, max(a, w["start"]), min(b, w["end"]), d] for m, a, b, d in wn]
            # the held note: the longest syllable, from its first sung note to its last (vibrato and glides split
            # notes; they are one held vowel), if that is at least 0.25 s
            sy = max(w["syl"], key=lambda x: x[2] - x[1])
            inn = [x for x in w["notes"] if x[2] > sy[1] + 0.02 and x[1] < sy[2] - 0.02]
            if inn:
                h0, h1 = max(inn[0][1], sy[1]), min(inn[-1][2], sy[2])
                if h1 - h0 >= 0.25:
                    m = max(inn, key=lambda x: x[2] - x[1])[0]
                    w["hold"] = [round(h0, 3), round(h1, 3), m]
            sel = (pts >= w["start"]) & (pts < w["end"])
            w["peak"] = round(float(np.max(pdb[sel])), 1) if sel.any() else None
        d = [(w["w"], (w.get("whisper_turbo") or [None])[0], w["start"], w.get("ctc_line")) for w in wds]
        report.append((n, src, " ".join(f"{a}@{s:.2f}" + (f"(w{x - s:+.2f})" if x is not None else "(w-)") + (f"(c{c - s:+.2f})" if c is not None else "") for a, x, s, c in d)))
        lines.append({"n": n, "text": " ".join(disp), "orig": L["text"], "eu": n in EU_TXT, "start": wds[0]["start"],
                      "end": wds[-1]["end"], "words": wds})
    for r in report:
        print(f"L{r[0]:02d} {r[1]:12s} {r[2]}")
    json.dump({"lines": lines, "notes": notes}, open(OUT / "words.json", "w"))
    return lines, notes


# ------------------------------------------------------------------ music + output
def stem_onsets(name, delta=0.25, wait=0.09):
    """onsets of a Demucs stem (the band is the original's): [[t, strength 0..1]]"""
    import librosa
    y, sr = common.load_stem(name, sr=22050)
    o = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
    pk = librosa.util.peak_pick(o, pre_max=4, post_max=4, pre_avg=12, post_avg=12, delta=o.std() * delta, wait=int(wait * sr / 256))
    s = o[pk] / (np.percentile(o[pk], 95) + 1e-9)
    return [[round(float(t), 3), round(float(min(1, x)), 3)] for t, x in zip(pk * 256 / sr, s)]


def write():
    lines, notes = (lambda j: (j["lines"], j["notes"]))(json.loads((OUT / "words.json").read_text()))
    A = json.loads((common.DATA / "audio.json").read_text())
    ons = dict(A["onsets"])
    ons["bass"] = stem_onsets("bass")
    ons["synth"] = stem_onsets("other", delta=0.4)
    v = vocal().mean(0)
    env = np.sqrt(np.convolve(v ** 2, np.ones(441) / 441, "same"))[::441]
    db = np.clip(20 * np.log10(env + 1e-9) + 60, 0, 60) / 60
    pk, pks = onset_peaks(v)
    ons["vocal"] = [[round(float(t), 3), round(float(s), 3)] for t, s in zip(pk, pks)]
    out = {"song": "audio/pdoom_eu.mp3 (= audio/el_music/pdoom_EU_v11.wav)",
           "note": "analysis/timing_eu.py: words on their verified windows (data/lyrics.json; data/eu_words.json and CTC "
                   "on the v9 vocal for the re-sung lines), letters by CTC inside each word, syllables snapped to the "
                   "vocal's onsets, notes from Praat f0; beats/sections/drums from data/audio.json (the band is unchanged).",
           "duration": A["duration"], "bpm": A["bpm"], "beats": A["beats"], "downbeats": A["downbeats"],
           "sections": A["sections"], "onsets": ons, "lines": lines, "notes": notes,
           "vocal_env": {"fps": 100, "v": [round(float(x), 3) for x in db]}}
    (common.DATA / "timing_eu.json").write_text(json.dumps(out, separators=(",", ":")))
    print("wrote", common.DATA / "timing_eu.json", {k: len(v) for k, v in ons.items()})


if __name__ == "__main__":
    stages = sys.argv[1:] or ["vocal", "whisper", "ctc"]
    for s in stages:
        {"vocal": vocal, "whisper": whisper, "ctc": ctc, "words": words, "write": write}[s]()
        print("done", s, flush=True)
