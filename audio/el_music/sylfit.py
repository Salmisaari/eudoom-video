"""Fit a take's syllables onto the original's rhythm, as a vocal editor would (2026-10-01, L25: the takes sang "plastic"
as one word on the original's "von", where the original sings von | Neu | mann's on three notes; the user: "study the
rhythm and how each part of the sounds is combined").
  1. the take's syllables: CTC forced alignment (wav2vec2 LV60K) of the new words on the take's separated vocal; each
     syllable is anchored at its vowel (where the note starts in singing)
  2. the target grid: the original's vowel onsets, measured on the original vocal (Praat notes + voiced runs)
  3. a piecewise time map from the take's vowels to the targets, applied with Praat PSOLA (a DurationTier; pitch and
     formants kept) on centre and sides, then the notes tuned onto the original's (v8_refine.TUNE, mid channel)
fit(text, targets) returns a hook f(vt, vo) for v8_refine.write (f.a = the segment's start, set by write)."""
import sys, pathlib
import numpy as np, librosa, parselmouth, torch, torchaudio
from parselmouth.praat import call

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis"))
import lyricfit as F
from v8_refine import V, TUNE
from timing_eu import syllables, pron

FRAME = 320 / 16000

# the original's vowel onsets per line (s), measured on the BS-RoFormer original vocal (2026-10-01)
GRID = {25: {7: [77.74, 78.22, 78.89, 79.30, 80.03, 80.46, 81.06],          # Now von Neu mann's ob so lete
             8: [77.74, 78.22, 78.89, 79.30, 79.72, 80.03, 80.46, 81.06]},  # + "are" in the breath before "ob"
        # See through the shog goth's lies (notes 67 30.24, 65 30.75, 63 30.92, 60 31.15); one more syllable sits
        # between goth's and lies, two more also split "the"
        11: {6: [30.05, 30.24, 30.48, 30.75, 30.92, 31.15], 7: [30.05, 30.24, 30.48, 30.75, 30.92, 31.04, 31.15],
             8: [30.05, 30.24, 30.40, 30.56, 30.75, 30.92, 31.04, 31.15]},
        # with your shi ni ga mi eyes (voiced 33.42 33.57 33.91 34.11 34.41 34.55 34.82)
        12: {7: [33.44, 33.57, 33.90, 34.11, 34.41, 34.55, 34.82], 6: [33.44, 33.90, 34.11, 34.41, 34.55, 34.82]}}


def vowels(v, t0, text):
    """vowel onset (s) of each syllable of `text` sung in v (mono, starts at t0): [(syllable, t)]"""
    em = F.emissions(v, V.SR)
    toks, owner = [], []
    words = [pron(w) for w in text.split()]
    for wi, subs in enumerate(words):
        for si, sub in enumerate(subs):
            if toks:
                toks.append(F._IDX["|"]); owner.append(None)
            for ci, ch in enumerate(sub.upper()):
                if ch in F._IDX and ch not in "-|":
                    toks.append(F._IDX[ch]); owner.append((wi, si, ci))
    ali, sc = torchaudio.functional.forced_align(em[None], torch.tensor([toks]), blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
    at = {owner[k]: t0 + s.start * FRAME for k, s in enumerate(spans) if owner[k]}
    out = []
    for wi, subs in enumerate(words):
        for si, sub in enumerate(subs):
            for a0, a1 in syllables(sub):
                vi = next((c for c in range(a0, a1) if sub[c] in "aeiouy"), a0)
                t = at.get((wi, si, vi)) or at.get((wi, si, a0))
                out.append((sub[a0:a1], t))
    return out


def retime(x, t0, src, dst):
    """x (stereo, starts at t0) time-mapped so src[i] lands on dst[i] (piecewise linear between anchors, the ends kept
    where they are); Praat PSOLA on centre and sides"""
    dur = x.shape[1] / V.SR
    s = [0.0] + [a - t0 for a in src] + [dur]
    d = [0.0] + [b - t0 for b in dst] + [dur + (dst[-1] - src[-1])]
    mid, side = x.mean(0), (x[0] - x[1]) / 2
    outs = []
    for ch in (mid, side):
        snd = parselmouth.Sound(ch.astype(np.float64), V.SR)
        man = call(snd, "To Manipulation", 0.01, 75, 900)
        dt = call("Create DurationTier", "d", 0, dur)
        for i in range(len(s) - 1):
            f = float(np.clip((d[i + 1] - d[i]) / max(1e-3, s[i + 1] - s[i]), 0.35, 3.0))
            call(dt, "Add point", s[i] + 0.002, f)
            call(dt, "Add point", s[i + 1] - 0.002, f)
        call([man, dt], "Replace duration tier")
        y = call(man, "Get resynthesis (overlap-add)").values[0]
        outs.append(np.pad(y, (0, max(0, len(ch) - len(y))))[: len(ch)])
    m, sd = outs
    return np.stack([m + sd, m - sd]).astype(np.float32)


def fit(text, line, tune=True, report=None):
    a, b = V.LYR[line - 1]["start"] - 0.12, V.LYR[line - 1]["end"] + 0.15  # align inside the line only

    def f(vt, vo):
        i0, i1 = int((a - f.a) * V.SR), int((b - f.a) * V.SR)
        syl = vowels(vt.mean(0)[i0:i1], f.a + i0 / V.SR, text)
        grid = GRID[line][len(syl)]
        src = [t for _, t in syl]
        ok = [i for i in range(len(src)) if src[i] is not None and (i == 0 or src[i] > max(x for x in src[:i] if x is not None))]
        src2, dst2 = [src[i] for i in ok], [grid[i] for i in ok]
        if report is not None:
            report.append(" ".join(f"{s}:{a:.2f}->{b:.2f}" for (s, _), a, b in zip([syl[i] for i in ok], src2, dst2)))
        y = retime(vt, f.a, src2, dst2)
        return TUNE(y, vo, max_cents=300, fold=True, half=2) if tune else y
    return f
