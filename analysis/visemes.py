"""Mouth chart timings for the idol's lip-sync -> data/visemes.json.

Each lyric word is re-aligned letter by letter inside its verified window
(data/lyrics.json) on the same fused CTC emissions as the timing map, so the
mouth follows what was actually sung. CTC letter spikes are short; a letter
holds until the next one starts, so sung vowels get their held length.
Letters (pronunciation spelling, pron.py) map to a 9-shape chart:
  X rest · M lips pressed (m b p) · F lip under teeth (f v) · A open (ah, I)
  E wide (ee, eh) · O round (oh, aw) · U pucker (oo, w) · L tongue (l t d n th)
  S teeth (s z k g ch sh r h y ...)
"""
import json
import re

import common
import numpy as np
from ctcalign import AIDX, FRAME, _viterbi, emissions
from pron import pron

DIGRAPHS = {"oo": "U", "ew": "U", "ue": "U", "ou": "O", "ow": "O", "oy": "O", "aw": "O", "au": "O",
            "ee": "E", "ea": "E", "ay": "E", "ai": "E", "ey": "E", "th": "L", "sh": "S", "ch": "S",
            "ng": "S", "ck": "S", "ph": "F", "wh": "U", "qu": "U"}
SINGLE = {"a": "A", "e": "E", "i": "E", "o": "O", "u": "A", "y": "E",
          "m": "M", "b": "M", "p": "M", "f": "F", "v": "F", "w": "U",
          "l": "L", "t": "L", "d": "L", "n": "L"}
REST_GAP = 0.12  # s of silence between words before the mouth closes


MAGIC_E = re.compile(r"[aiou][bcdfgklmnprstvz]e[sd]?$")  # safe, alive, fuse: the vowel says its name


def letters_to_visemes(sub):
    """[(viseme, first letter index)] for one pronunciation sub-word."""
    bare = sub.replace("'", "")
    out, i = [], 0
    while i < len(sub):
        if sub[i] == "'":
            i += 1
            continue
        c = sub[i]
        if bare in ("eye", "eyes") and i == 0:
            out.append(("A", 0)); out.append(("S", len(sub) - 1)) if bare == "eyes" else None
            break
        if sub[i:i + 3] == "igh":
            out.append(("A", i)); i += 3; continue
        two = sub[i:i + 2]
        if two == "ie" and i + 2 >= len(sub) - 1:  # lies, die
            out.append(("A", i)); i += 2; continue
        if two in DIGRAPHS:
            out.append((DIGRAPHS[two], i)); i += 2; continue
        v = SINGLE.get(c, "S")
        m = MAGIC_E.search(sub)
        if m and i == m.start():
            v = {"a": "E", "i": "A", "o": "O", "u": "U"}[c]
        if c == "i" and bare in ("i", "im", "ive", "ill", "id"):
            v = "A"  # the diphthong in "I" opens wide
        if c == "y" and i == len(sub) - 1 and not re.search(r"[aeiou]", sub[:-1]):
            v = "A"  # my, by, why
        if c == "e" and i == len(sub) - 1 and len(sub) > 2:
            i += 1; continue  # silent final e
        out.append((v, i)); i += 1
    return out


def word_keys(E, w):
    """Viseme keys [(t, v)] inside one word."""
    subs = pron(w["w"])
    chars = [c for s in subs for c in s]
    f0 = max(0, int(round(w["start"] / FRAME)))
    f1 = min(len(E), int(round(w["end"] / FRAME)))
    tgt = np.array([AIDX[c] for c in chars], np.int64)
    need = len(tgt) + int(np.sum(tgt[1:] == tgt[:-1]))
    starts = None
    if f1 - f0 >= need:
        seg = E[f0:f1]
        path, _ = _viterbi(seg, tgt, np.zeros(len(tgt), np.int64), np.full(len(tgt), len(seg) - 1, np.int64))
        tok = np.where(path % 2 == 1, (path - 1) // 2, -1)
        starts = []
        for j in range(len(tgt)):
            fr = np.where(tok == j)[0]
            starts.append((f0 + fr.min()) * FRAME if len(fr) else None)
        # a letter the path skipped (can't happen with CTC, but be safe): interpolate
        for j, s in enumerate(starts):
            if s is None:
                starts[j] = starts[j - 1] if j else w["start"]
    else:  # window shorter than the letters: spread them evenly
        starts = list(np.linspace(w["start"], w["end"], len(chars), endpoint=False))
    starts[0] = w["start"]  # the word onset is the verified one
    keys, base = [], 0
    for s in subs:
        for v, i in letters_to_visemes(s):
            keys.append((round(float(starts[base + i]), 3), v))
        base += len(s)
    # merge repeats
    merged = []
    for t, v in keys:
        if not merged or merged[-1][1] != v:
            merged.append((t, v))
    return merged


def main():
    E = emissions("fused6")
    lyr = json.loads((common.DATA / "lyrics.json").read_text())
    words = [w for l in lyr["lines"] for w in l["words"]]
    keys = [(0.0, "X")]
    for i, w in enumerate(words):
        keys += word_keys(E, w)
        nxt = words[i + 1]["start"] if i + 1 < len(words) else None
        if nxt is None or nxt - w["end"] > REST_GAP:
            keys.append((round(w["end"], 3), "X"))
    out = {
        "note": "Mouth chart keys [t, viseme] from per-word CTC letter alignment (analysis/visemes.py). "
                "X rest, M m/b/p, F f/v, A ah, E ee, O oh, U oo/w, L l/t/d/n/th, S other consonants.",
        "keys": keys,
    }
    (common.DATA / "visemes.json").write_text(json.dumps(out, separators=(",", ":")))
    from collections import Counter
    print(len(keys), "keys", Counter(v for _, v in keys))


if __name__ == "__main__":
    main()
