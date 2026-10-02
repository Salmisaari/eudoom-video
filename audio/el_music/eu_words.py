"""Word timings and mouth shapes for the re-sung EU lines, from the final song (usage: eu_words.py <song.wav> <sources.json>):
CTC forced alignment (wav2vec2 LV60K) of each line's sung words on its separated vocal.
Writes data/eu_words.json {line: [[word, start, end], ...]} and data/visemes_eu.json (data/visemes.json
with the changed lines' keys replaced)."""
import json, pathlib, sys
import numpy as np, soundfile as sf, torch, torchaudio

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis"))
from eu2_select import vocals
from eu3_build import bounds
import lyricfit as F
from visemes import letters_to_visemes, REST_GAP

SR = 44100
SPOKEN = {"EU": "EE YOU", "ASML": "AY ESS EM EL", "GDPR": "GEE DEE PEE AR", "GDP": "GEE DEE PEE", "SAP": "ESS AY PEE", "AC": "AY SEE", "PTO": "PEE TEE OH",
          "EU's": "EE YOU'S", "Euro-banality": "EURO BANALITY", "AI": "AY EYE", "E": "EE",
          "Post-AI-bubble": "POST AY EYE BUBBLE", "super-dense": "SUPER DENSE"}
# what the screen shows for each chosen take text (hooks show "EU" whichever way it was sung)
# sung word timings where the word count changed (v8, untouched takes: CTC word onsets on the separated vocal of
# pdoom_EU_v8.wav, checked against Whisper's word stamps): L10 and L16 sing on their own timing; L25 "private chats
# get" fills "von Neumann's"; L40 sings E-U-Inc-fix-es-things on R-L-H-F-goes-a and holds "soon" where the original
# holds "askew"
TIMED = {17: [["Cookies,", 52.825, 54.37], ["please,", 54.37, 55.98], ["please", 55.98, 56.58], ["let", 56.58, 57.14],
              ["me", 57.14, 57.769], ["free", 57.769, 59.13]],  # v13: both pleases sung (analysis/timing_eu.py FIXED)
         10: [["where", 27.94, 28.19], ["the", 28.19, 28.28], ["faxes", 28.28, 29.28], ["zoom", 29.28, 29.907]],  # v12, eu30_17
         # v10 (analysis/timing_eu.py FIXED, measured on the v10 vocal)
         11: [["See", 29.907, 30.18], ["through", 30.18, 30.47], ["Pinocchio's", 30.47, 31.12], ["lies,", 31.12, 33.4]],
         12: [["with", 33.58, 33.94], ["Eurovision", 33.94, 34.82], ["eyes", 34.82, 37.31]],
         16: [["I", 49.562, 49.72], ["feel", 49.72, 50.0], ["my", 50.0, 50.38], ["AC", 50.38, 50.94], ["temperatures", 50.94, 51.62],
              ["rearranging", 51.62, 52.825]],
         25: [["Now", 77.72, 78.14], ["privacy", 78.14, 78.86], ["in", 78.86, 79.3], ["chats", 79.3, 80.02], ["obsolete", 80.02, 81.21]],
         40: [["EU", 120.76, 121.09], ["Inc", 121.09, 121.3], ["fixes", 121.3, 121.88], ["things", 121.88, 122.1], ["soon", 122.1, 124.52]]}
DISPLAY = {"I'm upping my EU doom": "I'm upping my EU doom", "I'm upping my U-doom": "I'm upping my EU doom",
           "A-S-M-L to the moon": "ASML to the moon", "Trapped in the Brussels room": "Trapped in the Brussels room,",
           "Where the faxes zoom": "where the faxes zoom", "Whole EU's on PTO": "Whole EU's on PTO",
           "Brussels guy's on PTO": "Brussels guy's on PTO"}
FRAME = 320 / 16000


def spoken(display, sung_as):
    """[(display word, spoken form)]; the U-doom take sings 'EU' as 'you'."""
    out = []
    for w in display.split():
        bare = w.strip(",.?!")
        sp = SPOKEN.get(bare, bare.upper())
        if bare == "EU" and "U-doom" in sung_as:
            sp = "YOU"
        out.append((w, sp))
    return out


def align(voc, t0, pairs):
    em = F.emissions(voc, 22050)
    toks, owner = [], []
    for wi, (_, sp) in enumerate(pairs):
        for sub in sp.split():
            if toks:
                toks.append(F._IDX["|"]); owner.append(None)
            for c in sub:
                if c in F._IDX:
                    toks.append(F._IDX[c]); owner.append((wi, sub, c))
    ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
    letters = [(owner[i], t0 + s.start * FRAME) for i, s in enumerate(spans) if owner[i]]
    return letters


def relyric_windows(ow, nw):
    """Python port of animatic.ts relyric(): matching prefix/suffix words keep their timings, the new words in
    between share the replaced words' span by length."""
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


def align_in_windows(voc, t0, pairs, windows):
    """Same word count as the original line (the takes keep its timing): each word's letters are aligned
    inside that word's verified window from data/lyrics.json, like analysis/visemes.py does."""
    em = F.emissions(voc, 22050)
    letters = []
    for wi, ((_, sp), (ws, we)) in enumerate(zip(pairs, windows)):
        toks, owner = [], []
        for sub in sp.split():
            if toks:
                toks.append(F._IDX["|"]); owner.append(None)
            for c in sub:
                if c in F._IDX:
                    toks.append(F._IDX[c]); owner.append((wi, sub, c))
        f0, f1 = int((ws - t0) / FRAME), int((we - t0) / FRAME)
        if f1 - f0 > 2 * len(toks):
            ali, sc = torchaudio.functional.forced_align(em[f0:f1][None], torch.tensor([toks]), blank=0)
            spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
            times = [t0 + (f0 + s.start) * FRAME for s in spans]
        else:
            times = list(np.linspace(ws, we, len(toks), endpoint=False))
        times[0] = ws  # the word onset is the verified one
        letters += [(o, t) for o, t in zip(owner, times) if o]
    return letters


def main(song_path=HERE / "pdoom_EU_v3.wav", report_path=HERE / "eu_final_report.json"):
    """report: {"L<n>": {"text": sung line or display text}}; lines absent or null keep the original words."""
    song = sf.read(song_path, dtype="float32")[0].T
    report = json.loads(pathlib.Path(report_path).read_text())
    lyr = json.loads((ROOT / "data/lyrics.json").read_text())["lines"]
    vis = json.loads((ROOT / "data/visemes.json").read_text())
    keys = [tuple(k) for k in vis["keys"]]
    words_out = {}
    for ln, pick in report.items():
        if not pick:
            continue
        n = int(ln[1:])
        a, b = bounds(n)
        display = DISPLAY.get(pick["text"], pick["text"])
        pairs = spoken(display, pick["text"])
        voc, t0 = vocals(song, a, b)
        cut = int(0.7 * 22050)  # align on [a-0.3, b+0.3]
        seg, s0 = voc[cut:len(voc) - cut], t0 + cut / 22050
        ow = lyr[n - 1]["words"]
        if len(ow) == len(pairs):  # keep the verified word timings; the animatic re-sets these 1:1
            letters = align_in_windows(seg, s0, pairs, [(w["start"], w["end"]) for w in ow])
            ws = [[w, o["start"], o["end"]] for (w, _), o in zip(pairs, ow)]
        else:  # word count changed: measured timings, else the animatic's relyric() mapping (CTC drifts on held notes)
            windows = [(x, y) for _, x, y in TIMED[n]] if n in TIMED else relyric_windows(ow, [w for w, _ in pairs])
            if n in TIMED:
                words_out[str(n)] = TIMED[n]
            letters = align_in_windows(seg, s0, pairs, windows)
            ws = [[w, round(x, 3), round(y, 3)] for (w, _), (x, y) in zip(pairs, windows)]
        # mouth keys: letter onsets -> shapes, per spoken sub-word; rest where the singer breathes
        new, per_sub = [], {}
        for (wi, sub, c), t in letters:
            per_sub.setdefault((wi, sub), []).append(t)
        for (wi, sub), ts in per_sub.items():
            for v, i in letters_to_visemes(sub.lower()):
                new.append((round(max(a, ts[min(i, len(ts) - 1)]), 3), v))
        new.sort()
        merged = [k for i, k in enumerate(new) if i == 0 or k[1] != new[i - 1][1]]
        after = [k for k in keys if k[0] >= b]
        resume = next((k[1] for k in reversed(keys) if k[0] <= b), "X")
        keys = [k for k in keys if k[0] < a] + merged + ([(b, resume)] if not after or after[0][0] > b else []) + after
        print(f"L{n:02d} {display!r}: " + " ".join(f"{w}@{s:.2f}" for w, s, _ in ws), flush=True)
    (ROOT / "data/eu_words.json").write_text(json.dumps(words_out, indent=1))
    vis["keys"] = [[t, v] for t, v in keys]
    vis["note"] += " EU edition: re-sung lines replaced from audio/el_music/eu_words.py."
    (ROOT / "data/visemes_eu.json").write_text(json.dumps(vis, separators=(",", ":")))


if __name__ == "__main__":
    main(*sys.argv[1:3]) if len(sys.argv) > 2 else main()
