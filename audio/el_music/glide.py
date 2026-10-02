"""The /j/ glide between two sung vowels: "AI" as ay-YAI (L37, the user: "AI should be almost like AIJAI") and "EU" as
ee-YOO (the user: "same with EU that's EJU"). Measured on a vocal (mono, 44.1 kHz) with Praat, 5 ms steps, between
the first vowel's onset t1 and the second's t2 (CTC letter onsets):
  join     from the first vowel's last frame on the /j/ position (AI: F1 < 480 Hz, F2 > 1800 Hz) or on /i/ (EU: F2 >
           1900 Hz) to the second vowel's first frame of /a/ (AI: F1 > 650 Hz) or /u/ (EU: F2 < 1700 Hz, the sung /u/ is fronted); move_ms
  gap_ms   unvoiced time inside the join (0 = sung through)
  dip_db   lowest level across the join against the two vowels' mean level (a /j/ is narrower and a few dB quieter
           than the open vowel after it; a hard restart dips further and stops the voicing)
  j        the first vowel reaches the /j/ position (the join is only measured from there; for EU the /i/ is it)
  f2_jump  F2 at the second vowel's start minus F2 at the end of the /j/, Hz
  glide    a /j/, then gap <= 20 ms and dip >= -12 dB: sung through into the second vowel (which must hold its
           formants for 20 ms, so a one-frame formant blip isn't taken for it)
In v17 (eu32a_3) the A ends on the /j/ position, then voicing stops for ~40 ms (-12 dB) and the I restarts on its /a/:
no glide, which is what the user heard."""
import numpy as np, parselmouth

SR = 44100
STEP = 0.005


def tracks(m, a):
    """times (song), F1, F2, f0 (nan unvoiced), level dB of mono m starting at song time a"""
    snd = parselmouth.Sound(m.astype(np.float64), SR)
    fm = snd.to_formant_burg(time_step=STEP, max_number_of_formants=5, maximum_formant=5500, window_length=0.025)
    p = snd.to_pitch(time_step=STEP, pitch_floor=90, pitch_ceiling=1000)
    ts = np.arange(0.015, len(m) / SR - 0.015, STEP)
    f1 = np.array([fm.get_value_at_time(1, t) for t in ts]); f2 = np.array([fm.get_value_at_time(2, t) for t in ts])
    f0 = np.array([p.get_value_at_time(t) or np.nan for t in ts])
    lv = 10 * np.log10(np.convolve(m ** 2, np.ones(441) / 441, "same")[(ts * SR).astype(int)] + 1e-12)
    f0[lv < lv.max() - 30] = np.nan
    return a + ts, f1, f2, f0, lv


TESTS = {"AI": (lambda f1, f2: (f2 > 1800) & (f1 < 480), lambda f1, f2: f1 > 650),   # /j/ position, then the /a/ of /aI/
         "EU": (lambda f1, f2: f2 > 1900, lambda f1, f2: f2 < 1700)}                  # /i/ (/j/-like), then /u/ (sung
#                                                                    fronted here: F2 ~1500 against the /i/'s 2400-2800)


def glide(m, a, t1, t2, kind="AI", until=None):
    """t1, t2: CTC onsets of the two letters (only to bound the search). The join runs from the first vowel's last
    frame on the /j/ position (AI) or /i/ (EU) to the second vowel's first frame of /a/ (AI) or /u/ (EU)."""
    t, f1, f2, f0, lv = tracks(m, a)
    v = np.isfinite(f0) & np.isfinite(f1) & np.isfinite(f2)
    first, second = TESTS[kind]
    # the first vowel sits in the first 60 % of the word when its end is known, and (below) is its first held /i/ run,
    # starting in the first 35 % (L40: the /i/ at the end of its "EU" is the I of "Inc" coming early, not the E)
    win = (t >= t1 - 0.03) & (t <= (t1 + 0.6 * (until - t1) if until else t2 + 0.25))
    ok1 = v & first(f1, f2)
    run1 = np.convolve(ok1.astype(int), np.ones(4, int), "same") >= 4  # inside a run of >= 4 frames: no formant spikes
    jt = np.where(win & ok1 & run1)[0]
    if until and len(jt):  # EU: the E is the first held /i/ run, starting in the word's first 35 %
        if t[jt[0]] > t1 + 0.35 * (until - t1):
            jt = jt[:0]
        else:
            brk = np.where(np.diff(jt) > 1)[0]
            jt = jt[: brk[0] + 1] if len(brk) else jt
    if not len(jt):
        return dict(gap_ms=None, dip_db=None, j=False, f1_j=None, f2_jump=None, glide=False, join=None, move_ms=None)
    # the second vowel: its first frame after the /j/ run; the /j/ run ends at its last frame before that
    ok2 = v & second(f1, f2)
    held = np.convolve(ok2.astype(int), np.ones(4, int), "full")[3:] == 4  # starts a run of >= 4 frames (20 ms)
    after = np.where(held & (t > t[jt[0]]) & (t <= (until if until else t2 + 0.3)))[0]
    if not len(after):
        return dict(gap_ms=None, dip_db=None, j=True, f1_j=None, f2_jump=None, glide=False, join=None, move_ms=None)
    s2 = after[0]
    j_end = jt[jt < s2].max()
    gap = float((~v[j_end:s2 + 1]).sum() * STEP * 1000)
    side = (lv[max(0, j_end - 6):j_end + 1].mean() + lv[s2:s2 + 8].mean()) / 2
    dip = float(lv[j_end:s2 + 1].min() - side)
    jr = jt[(jt <= j_end) & (jt >= j_end - 12)]
    f1j = float(f1[jr].min())
    f2_jump = float(f2[s2] - f2[j_end])
    return dict(gap_ms=round(gap), dip_db=round(dip, 1), j=bool(kind == "EU" or f1j < 480), f1_j=round(f1j),
                f2_jump=round(f2_jump), move_ms=round(float(t[s2] - t[j_end]) * 1000),
                glide=bool(gap <= 20 and dip >= -12), join=round(float(t[j_end]), 3))
