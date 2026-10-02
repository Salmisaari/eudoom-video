"""L9-10 "where the FAXES zoom": the held note. Measured on the vocals (BS-RoFormer split, Praat f0, compare.py /
offsets.py / l10_scan.py): the original rises into "baaag" at 28.42 s and holds MIDI 70 until 28.80, level steady;
round 5's take (eu2_low4, G/J) holds its "fa" at 70 only to 28.60, falls, closes on the k at ~28.65 and then hisses
the s for 0.2 s (28.68-28.88) where the original still sings: the held note loses its length and its weight, and the
syllables after it feel early/late ("drift"). None of the 23 eu2 takes that sing "faxes" holds it (best 40 % of the
note; the four that hold it sing the old "bag of shoes").
So the note length is edited, as a vocal editor would: the clean, full part of the take's own vowel (28.575-28.605) is
lengthened (x5.5, or x3.5 for M) by PSOLA (repeats pitch periods, formants kept; mid channel, the side by phase vocoder), the take's own
vowel end and k follow, the s hiss is shortened by as much as the vowel grew (a cut in noise), so "-es"
stays where it was (28.90). The lengthened part keeps the level the vowel starts at. Then the held note is tuned onto the original's (mid channel).
Clips "L9-10<letter>" in eu_v8_lines (the next free letters)."""
import sys, pathlib
import numpy as np, librosa, parselmouth
from parselmouth.praat import call
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from l910_weight import proc, mask, WHERE_THE, ES, weight
from v8_refine import write, V, TUNE

V0, V1 = 28.575, 28.605  # the clean, full part of the vowel (HNR 8-20 dB, level steady; before it the take is breathy
#                          and splits into a lower octave at 28.50-28.57, after it it fades 12-16 dB into the k)
TRANS = 0.08  # the take's own vowel end + k closure, kept whole
HOLD = (28.42, 28.84)
XF = 0.01


def psola_stretch(x, factor):
    """x (mono) lengthened by factor, pitch kept (Praat PSOLA; it lengthens at most x3 per pass, so in equal passes)"""
    passes = int(np.ceil(np.log(factor) / np.log(2.5)))
    for _ in range(passes):
        s = parselmouth.Sound(x.astype(np.float64), V.SR)
        man = call(s, "To Manipulation", 0.01, 150, 900)
        dt = call("Create DurationTier", "d", 0, s.duration)
        call(dt, "Add point", 0, factor ** (1 / passes))
        call([man, dt], "Replace duration tier")
        x = call(man, "Get resynthesis (overlap-add)").values[0]
    return x


def lengthen(x, t0, NEW_END, TRANS=TRANS):
    """x (stereo vocal starting at t0 s): the vowel [V0, V1] lengthened to end at NEW_END, then [V1, V1 + TRANS] of
    the take, then the take again from NEW_END + TRANS on (the hiss between is dropped)."""
    i = lambda t: int(round((t - t0) * V.SR))
    factor = (NEW_END - V0) / (V1 - V0)
    pad = int(0.03 * V.SR)  # context so PSOLA finds the pitch marks at the edges: the clean vowel mirrored, since the
    #                          take's own neighbours (the split octave before, the fall after) read as other notes and
    #                          the stretch spreads that glide over 80 ms
    mirror = lambda c: np.concatenate([c[:pad][::-1], c, c[-pad:][::-1]])
    mid, side = x.mean(0), (x[0] - x[1]) / 2
    seg_m = psola_stretch(mirror(mid[i(V0):i(V1)]), factor)[int(pad * factor):]
    seg_s = librosa.effects.time_stretch(mirror(side[i(V0):i(V1)]), rate=1 / factor)[int(pad * factor):]
    n_new = i(NEW_END) - i(V0)
    seg_m, seg_s = seg_m[:n_new + int(XF * V.SR)], seg_s[:n_new + int(XF * V.SR)]
    # the clean slice was already fading into the take's fall, and the stretch draws that fade out over 80 ms; the
    # original holds its level through the note, so the copy is levelled to the slice's start (20 ms RMS, <= +9 dB)
    env = np.sqrt(np.convolve(seg_m ** 2, np.ones(882) / 882, "same")) + 1e-9
    g = np.clip(np.median(env[441:1764]) / env, 1, 10 ** (9 / 20))
    g = np.convolve(np.pad(g, 441, mode="edge"), np.ones(883) / 883, "valid")
    seg_m, seg_s = seg_m * g, seg_s * g
    tail_from = i(V1)  # vowel end + k: the take's own, moved to NEW_END
    out_m, out_s = mid.copy(), side.copy()
    k = int(XF * V.SR)
    ramp = np.linspace(0, 1, k)
    # 1. lengthened vowel from V0 (crossfade in over 10 ms)
    out_m[i(V0):i(V0) + k] = mid[i(V0):i(V0) + k] * (1 - ramp) + seg_m[:k] * ramp
    out_s[i(V0):i(V0) + k] = side[i(V0):i(V0) + k] * (1 - ramp) + seg_s[:k] * ramp
    out_m[i(V0) + k:i(NEW_END)] = seg_m[k:n_new]
    out_s[i(V0) + k:i(NEW_END)] = seg_s[k:n_new]
    # 2. the take's vowel end + k closure + the start of its s at NEW_END (crossfade from the lengthened vowel)
    n_tr = int(TRANS * V.SR)
    tr_m, tr_s = mid[tail_from:tail_from + n_tr + k], side[tail_from:tail_from + n_tr + k]
    out_m[i(NEW_END):i(NEW_END) + k] = seg_m[n_new:n_new + k] * (1 - ramp) + tr_m[:k] * ramp
    out_s[i(NEW_END):i(NEW_END) + k] = seg_s[n_new:n_new + k] * (1 - ramp) + tr_s[:k] * ramp
    out_m[i(NEW_END) + k:i(NEW_END) + n_tr] = tr_m[k:n_tr]
    out_s[i(NEW_END) + k:i(NEW_END) + n_tr] = tr_s[k:n_tr]
    # 3. back on the take's own timeline inside the s hiss (the hiss in between is dropped)
    j = i(NEW_END) + n_tr
    out_m[j:j + k] = tr_m[n_tr:n_tr + k] * (1 - ramp) + mid[j:j + k] * ramp
    out_s[j:j + k] = tr_s[n_tr:n_tr + k] * (1 - ramp) + side[j:j + k] * ramp
    return np.stack([out_m + out_s, out_m - out_s]).astype(np.float32)


def retime(x, t0, a0, a1, new_end, onset=0.03):
    """x's [a0, a1] lengthened (PSOLA, mid; phase vocoder, side) to end at new_end, then x's [a1, a1 + onset] (the
    natural start of the consonant after it), then x's own timeline again from new_end + onset: what x had in between
    is dropped inside the consonant's steady hiss (jumping straight into mid-hiss gave a click: 2.4x the song's usual
    >6 kHz flux). 10 ms crossfades."""
    i = lambda t: int(round((t - t0) * V.SR))
    factor = (new_end - a0) / (a1 - a0)
    k = int(XF * V.SR)
    mid, side = x.mean(0), (x[0] - x[1]) / 2
    n_new = i(new_end) - i(a0)
    n_on = int(onset * V.SR)
    seg_m = psola_stretch(mid[i(a0):i(a1) + k], factor)
    seg_s = librosa.effects.time_stretch(side[i(a0):i(a1) + k], rate=1 / factor)
    seg_m = np.pad(seg_m, (0, max(0, n_new + k - len(seg_m))))[:n_new + k]
    seg_s = np.pad(seg_s, (0, max(0, n_new + k - len(seg_s))))[:n_new + k]
    ramp = np.linspace(0, 1, k)
    out = []
    for ch, seg in ((mid, seg_m), (side, seg_s)):
        o = ch.copy()
        o[i(a0):i(a0) + k] = ch[i(a0):i(a0) + k] * (1 - ramp) + seg[:k] * ramp
        o[i(a0) + k:i(new_end)] = seg[k:n_new]
        on = ch[i(a1):i(a1) + n_on + k]
        o[i(new_end):i(new_end) + k] = seg[n_new:n_new + k] * (1 - ramp) + on[:k] * ramp
        o[i(new_end) + k:i(new_end) + n_on] = on[k:n_on]
        j = i(new_end) + n_on
        o[j:j + k] = on[n_on:n_on + k] * (1 - ramp) + ch[j:j + k] * ramp
        out.append(o)
    return np.stack([out[0] + out[1], out[0] - out[1]]).astype(np.float32)


def hold(heavy=False, new_end=28.74, db=3, lifts=((WHERE_THE, 600), (ES, 1000)), rides=(), retimes=(), trans=TRANS):
    """G (lifts: its notes put on the original's), the held note lengthened, optionally J's weight (+-db) and
    rides: [((t0, t1), dB)] extra gain on single words (20 ms ramps); retimes: [(a0, a1, new_end)] (retime(), before
    the lifts)"""
    base = proc(list(lifts), False)

    def f(vt, vo):
        base.a = f.a
        for a0, a1, e in retimes:
            vt = retime(vt, f.a, a0, a1, e)
        x = lengthen(base(vt, vo), f.a, new_end, trans)
        m = mask(x.shape[1], f.a, [HOLD])
        x = x * (1 - m) + TUNE(x, vo, max_cents=300, fold=False) * m
        x = weight(x, vo, f.a, db) if heavy else x
        for span, gain in rides:
            x = x * 10 ** (gain * mask(x.shape[1], f.a, [span]) / 20)
        return x.astype(np.float32)
    return f


if __name__ == "__main__":
    text = "Trapped in the Brussels room, where the faxes zoom"
    only = sys.argv[1:]
    for letter, heavy, end, desc in (("K", False, 28.74, "G with the held note (fa-) as long as the original's"),
                                     ("L", True, 28.74, "J (G + weight) with the held note as long as the original's"),
                                     ("M", False, 28.68, "G with the held note lengthened less (to 28.68 s; the original's to 28.78)")):
        if not only or letter in only:
            write(l910.N, "eu2_low4", l910.PLAN, "htdemucs_ft", False, hold(heavy, end), desc, text, label="L9-10", letter=letter)
