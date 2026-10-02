"""L16 "I feel my AC temperatures rearranging", the user (1 Oct 2026): "like 95% close but there's something little off".
The line in v13 is eu9_7 whole, untouched, with "-ranging" (52.05-52.85 s) PSOLA-tuned onto the original's notes (up to
600 cents, 20 ms ramps): L16O, final13.py.
  diagnose  the current line, the same take unlifted and the original ("I feel my atoms rearranging"), syllable by
            syllable on their BS-RoFormer vocals: vowel onsets (CTC), pitch against the original's notes, vowel length,
            level, brightness over 4 kHz (consonants), width; across "-ranging" the pitch track, its steps, harmonicity
            and formants; the seams; clicks
  build     the fixes, one per variant (see FIXES), into song v13; clips in analysis/work/l16_tune
  file      Desktop/suno_test/"eu_v13_L16 - fine-tune": the original, the current, "L16 F1 - <fix>" ..., README; opens it
Run from audio/el_music with the analysis venv: l16_tune.py diagnose|build|file"""
import json, pathlib, shutil, subprocess, sys
import numpy as np, librosa, parselmouth

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import line_round as LR

WORK = HERE.parents[1] / "analysis/work/l16_tune"
WORK.mkdir(parents=True, exist_ok=True)
DESK = pathlib.Path.home() / "Desktop/suno_test/eu_v13_L16 - fine-tune"
SR = 44100
SP_NEW = "i feel my ay see temperatures rearranging"
SP_OLD = "i feel my atoms rearranging"
LIFT = (52.05, 52.85)


def clip_build(Y, out_name, base):
    from final11 import paste, V
    from final10 import bounds
    import final12
    a, b = bounds(16)
    out, span = paste(base, Y, a, b)
    LR.mp3(out[:, int((a - 0.8) * SR):int((b + 0.5) * SR)], SR, WORK / f"L16 {out_name}.mp3")
    return out, [[round(float(t), 3), round(float(final12.seam_db(out, base, t)), 1)] for t in span]


def base_clips():
    from final11 import V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    from v8_refine import P16_ALL
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=SR, mono=False)[0][:, : V.mix.shape[1]]
    a, b = bounds(16)
    cut = lambda y: y[:, int((a - 0.8) * SR):int((b + 0.5) * SR)]
    LR.mp3(cut(V.mix), SR, WORK / "L16 original - I feel my atoms rearranging.mp3")
    LR.mp3(cut(v13), SR, WORK / "L16 current - I feel my AC temperatures rearranging.mp3")
    Y = hooked(ms(None, 16), 16, "eu9_7", P16_ALL, "bsroformer", VO_R)
    _, seams = clip_build(Y, "unlifted - I feel my AC temperatures rearranging", v13)
    print("unlifted seams", seams)


def split(name):
    import compare as C
    C.WORK = WORK / "cmp"; C.WORK.mkdir(exist_ok=True)
    return C.split(next(WORK.glob(f"L16 {name} - *.mp3")))


T0 = 49.562 - 0.8  # clip start (song time)


def piece(v, a, b):
    return v[:, int((a - T0) * SR):int((b - T0) * SR)]


def syllables(v, sp):
    import sylfit
    return [(s, t) for s, t in sylfit.vowels(piece(v, 49.45, 52.95).mean(0), 49.45, sp)]


def f0(v, a, b, step=0.01):
    p = parselmouth.Sound(piece(v, a, b).mean(0).astype(np.float64), SR).to_pitch(time_step=step, pitch_floor=90, pitch_ceiling=1000)
    ts = np.arange(0, b - a, step)
    return a + ts, np.array([p.get_value_at_time(t) or np.nan for t in ts])


def midi(f):
    return 69 + 12 * np.log2(f / 440)


def level(v, a, b):
    return 10 * np.log10(np.mean(piece(v, a, b).mean(0) ** 2) + 1e-12)


def bright(v, a, b):
    x = piece(v, a, b).mean(0)
    S = np.abs(librosa.stft(x, n_fft=1024, hop_length=256)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=1024)
    return 10 * np.log10(S[f > 4000].sum() / (S[(f > 100) & (f < 4000)].sum() + 1e-12) + 1e-12)


def width(v, a, b):
    x = piece(v, a, b)
    m, s = x.mean(0), (x[0] - x[1]) / 2
    return 10 * np.log10(np.mean(s ** 2) / (np.mean(m ** 2) + 1e-12) + 1e-12)


def hnr(v, a, b):
    h = parselmouth.Sound(piece(v, a, b).mean(0).astype(np.float64), SR).to_harmonicity_cc(time_step=0.01, minimum_pitch=90).values[0]
    return float(np.mean(h[h > 0])) if (h > 0).any() else float("nan")


def formants(v, a, b):
    snd = parselmouth.Sound(piece(v, a, b).mean(0).astype(np.float64), SR)
    fm = snd.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500)
    ts = np.arange(0.02, b - a - 0.02, 0.01)
    return [float(np.nanmedian([fm.get_value_at_time(i, t) for t in ts])) for i in (1, 2, 3)]


def diagnose():
    _, vo = split("original")
    res = {}
    for name in ("current", "unlifted"):
        _, vc = split(name)
        so, sc = syllables(vo, SP_OLD), syllables(vc, SP_NEW)
        print(f"\n== {name}: vowel onsets (CTC) ==")
        print("  original:", [(s, round(t, 2) if t else None) for s, t in so])
        print("  take    :", [(s, round(t, 2) if t else None) for s, t in sc])
        # shared syllables: I, feel, my and re-ar-ran-ging
        shared = list(zip(so[:3], sc[:3])) + list(zip(so[-3:], sc[-3:]))  # I feel my ... rear-ran-ging
        print("  shared syllables, onset ms off the original:", [(o[0], round((c[1] - o[1]) * 1000) if c[1] and o[1] else None) for o, c in shared])
        # pitch per syllable window (from its vowel onset to the next one), against the original over the same time
        to_, fo = f0(vo, 49.45, 52.95); tc_, fc = f0(vc, 49.45, 52.95)
        on = [t for _, t in sc if t] + [52.85]
        rows = []
        for (s, t), t1 in zip([x for x in sc if x[1]], on[1:]):
            w = (tc_ >= t) & (tc_ < t1)
            c = np.nanmedian(midi(fc[w])) if np.isfinite(fc[w]).any() else np.nan
            o = np.nanmedian(midi(fo[w])) if np.isfinite(fo[w]).any() else np.nan
            rows.append(dict(syl=s, t=round(t, 2), len_ms=round((t1 - t) * 1000), note=round(float(c), 2), orig_note=round(float(o), 2),
                             cents=round(float((c - o) * 100)) if np.isfinite(c - o) else 0, lvl=round(level(vc, t, t1) - level(vo, t, t1), 1),
                             bright=round(bright(vc, t, t1) - bright(vo, t, t1), 1), width=round(width(vc, t, t1) - width(vo, t, t1), 1),
                             hnr=round(hnr(vc, t, t1) - hnr(vo, t, t1), 1)))
        print(f"  {'syl':8} {'t':>6} {'len':>5} {'note':>6} {'orig':>6} {'cents':>6} {'lvl dB':>6} {'>4k dB':>6} {'width':>6} {'HNR':>6}")
        for r in rows:
            print(f"  {r['syl']:8} {r['t']:6.2f} {r['len_ms']:5d} {r['note']:6.2f} {r['orig_note']:6.2f} {r['cents']:+6d} {r['lvl']:+6.1f} "
                  f"{r['bright']:+6.1f} {r['width']:+6.1f} {r['hnr']:+6.1f}")
        # across the lift: pitch steps (cents per 10 ms) and the lift's edges
        t_, f_ = f0(vc, 51.9, 52.95, 0.005)
        m_ = midi(f_)
        d = np.abs(np.diff(m_)) * 100
        big = [(round(float(t_[i]), 3), round(float(d[i]))) for i in np.where(d > 60)[0]]
        print("  pitch jumps > 60 cents in 5 ms over 51.90-52.95:", big)
        print(f"  '-ranging' ({LIFT[0]}-{LIFT[1]}): HNR {hnr(vc, *LIFT):.1f} dB (original {hnr(vo, *LIFT):.1f}), "
              f"formants F1-F3 {[round(x) for x in formants(vc, *LIFT)]} (original {[round(x) for x in formants(vo, *LIFT)]})")
        res[name] = dict(rows=rows, jumps=big, hnr_lift=hnr(vc, *LIFT), hnr_lift_orig=hnr(vo, *LIFT))
    # the lift itself: the current against the unlifted take over "-ranging"
    _, vc = split("current"); _, vu = split("unlifted")
    tt, fc = f0(vc, 51.9, 52.95); _, fu = f0(vu, 51.9, 52.95); _, fo = f0(vo, 51.9, 52.95)
    print("\n== '-ranging', notes every 50 ms: original / unlifted / current ==")
    for i in range(0, len(tt), 5):
        print(f"  {tt[i]:.2f}  {midi(fo[i]):6.2f}  {midi(fu[i]):6.2f}  {midi(fc[i]):6.2f}")
    print(f"  HNR over the lift: current {hnr(vc, *LIFT):.1f}, unlifted {hnr(vu, *LIFT):.1f}, original {hnr(vo, *LIFT):.1f} dB")
    import l18_fix
    print("  clicks: current", l18_fix.clicks(piece(vc, 49.4, 52.95), 49.4, 52.95), " original", l18_fix.clicks(piece(vo, 49.4, 52.95), 49.4, 52.95))
    (WORK / "diagnose.json").write_text(json.dumps(res, indent=1, default=float))


DELAY = 0.11  # the take sings "ran" 100-120 ms after the original (vowel onsets 52.27/52.29 against 52.17)
AC = "eu31_7"  # round 31's L16v2: its "A" holds 65 for 260 ms at 17.3 dB harmonicity (the original 240 ms, 19.4 dB)
FIXES = {"F1": "ran on its high note - the lift moved 110 ms later, onto the take's own ran",
         "F2": "a clean A - A-C from round 31's L16v2 (eu31_7)",
         "F3": "both - ran on its high note and a clean A"}


def lift_on_take(t0=LIFT[0], t1=LIFT[1], d=DELAY, until=52.45):
    """the current lift (TUNE inside [t0, t1], 20 ms ramps, up to 600 cents) aimed at the original's notes moved d later,
    up to `until` ('ran'), then at the original's own (the two agree on 67 there: 40 ms crossfade)"""
    from v8_refine import TUNE
    def f(vt, vo):
        n = int(d * SR)
        vo_d = np.concatenate([np.repeat(vo[:, :1], n, 1), vo[:, :-n]], 1)
        # one pass on one target (blending two tuned signals phase-cancels: -6.5 dB at the blend), aimed at the original's
        # own octave: the moved 70 meets the take's 63 (+700 cents), which "nearest octave" folds to -500 (58)
        s_ = np.arange(vt.shape[1]) / SR + f.a
        x = np.clip((s_ - (until - 0.02)) / 0.04, 0, 1)
        tuned = TUNE(vt, (vo_d * (1 - x) + vo * x).astype(np.float32), max_cents=800, fold=False)
        m = np.clip(np.minimum((s_ - t0) / 0.02, (t1 - s_) / 0.02), 0, 1)
        return (vt * (1 - m) + tuned * m).astype(np.float32)
    return f


def swap_ac(song, take_song, lo=(50.15, 50.27), hi=(50.56, 50.74)):
    """the vocal of take_song over A-C into song: BS-RoFormer estimates of both, in at the quietest point of the two
    vocals together in lo, out at the quietest in hi (both in dips: after "my", the t of "tem"), 20 ms equal-power fades"""
    import rof
    W = (49.9, 51.0)
    E1, E2 = rof.separate(song, *W), rof.separate(take_song, *W)
    t = W[0] + np.arange(E1.shape[1]) / SR
    e = 10 * np.log10(np.convolve((E1 + E2).mean(0) ** 2, np.ones(441) / 441, "same") + 1e-12)
    qp = lambda a, b: float(t[(t >= a) & (t <= b)][np.argmin(e[(t >= a) & (t <= b)])])
    ti, to = qp(*lo), qp(*hi)
    w = np.clip(np.minimum((t - ti) / 0.02 + 0.5, (to - t) / 0.02 + 0.5), 0, 1)
    out = song.copy(); i0 = int(W[0] * SR)
    out[:, i0:i0 + E1.shape[1]] = song[:, i0:i0 + E1.shape[1]] - E1 + E1 * np.cos(w * np.pi / 2) + E2 * np.sin(w * np.pi / 2)
    return out, (ti, to)


def build():
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    from v8_refine import P16_ALL
    import final12
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=SR, mono=False)[0][:, : V.mix.shape[1]]
    a, b = bounds(16)
    cut = lambda y: y[:, int((a - 0.8) * SR):int((b + 0.5) * SR)]
    seam = lambda out, ts: [[round(float(x), 3), round(float(final12.seam_db(out, v13, x)), 1)] for x in ts]
    # F1: the take with the lift on its own "ran", spliced over the line as the current is
    Y1 = hooked(ms(lift_on_take(), 16), 16, "eu9_7", P16_ALL, "bsroformer", VO_R)
    f1, sp1 = paste(v13, Y1, a, b)
    # F2: the current with eu31_7's A-C; the take's line levelled and spliced the same way first
    Y7 = hooked(ms(None, 16), 16, AC, P16_ALL, "bsroformer", VO_R)
    s7, _ = paste(v13, Y7, a, b)
    f2, sp2 = swap_ac(v13, s7)
    f3, sp3 = swap_ac(f1, s7)
    info = {}
    for k, y, sp in (("F1", f1, list(sp1)), ("F2", f2, list(sp2)), ("F3", f3, list(sp1) + list(sp2))):
        LR.mp3(cut(y), SR, WORK / f"L16 {k} - {FIXES[k]}.mp3")
        info[k] = dict(seams=seam(y, sp))
        print(k, FIXES[k], info[k], flush=True)
    (WORK / "build.json").write_text(json.dumps(info, indent=1))


def assess(name):
    """the two things found off, plus the line's overall numbers, for one clip"""
    _, vo = split("original"); _, vc = split(name)
    sc = dict(syllables(vc, SP_OLD if name == "original" else SP_NEW))
    t_ran = sc.get("ran")
    tt, fc = f0(vc, 51.9, 52.95)
    w = (tt >= t_ran) & (tt < t_ran + 0.15)
    ran_note = float(np.nanmedian(midi(fc[w]))) if np.isfinite(fc[w]).any() else float("nan")
    tt_o, fo = f0(vo, 51.9, 52.95); wo = (tt_o >= 52.17) & (tt_o < 52.32)
    ran_orig = float(np.nanmedian(midi(fo[wo])))
    # the A: voiced frames on 64.4-65.6 in 50.2-50.5, their harmonicity; the s: unvoiced hissy frames after it
    t2, f2 = f0(vc, 50.12, 50.8)
    on65 = (t2 >= 50.2) & (t2 <= 50.5) & (midi(f2) >= 64.4) & (midi(f2) <= 65.6)
    a_ms = int(on65.sum() * 10)
    a_hnr = hnr(vc, float(t2[on65][0]), float(t2[on65][-1]) + 0.01) if on65.any() else float("nan")
    x = piece(vc, 50.3, 50.55).mean(0)
    S = np.abs(librosa.stft(x, n_fft=1024, hop_length=441)) ** 2; fr = librosa.fft_frequencies(sr=SR, n_fft=1024)
    hi = 10 * np.log10(S[fr > 4000].sum(0) / (S[(fr > 100) & (fr < 4000)].sum(0) + 1e-12) + 1e-12)
    s_ms = int((hi > 0).sum() * 10)
    import l18_fix
    return dict(ran_vowel=round(t_ran, 2), ran_note=round(ran_note, 2), ran_cents=round((ran_note - ran_orig) * 100),
                A_ms=a_ms, A_hnr=round(a_hnr, 1), s_ms=s_ms, line_hnr=round(hnr(vc, 49.56, 52.82) - hnr(vo, 49.56, 52.82), 1),
                clicks=l18_fix.clicks(piece(vc, 49.4, 52.95), 49.4, 52.95))


def measure():
    out = {k: assess(k) for k in ("original", "current", "F1", "F2", "F3")}
    for k, r in out.items():
        print(k, r, flush=True)
    (WORK / "measure.json").write_text(json.dumps(out, indent=1, default=float))


ORIG_SYL = [(49.50, "I"), (49.66, "feel"), (50.00, "my"), (50.25, "a-"), (50.50, "-toms"), (51.30, "re-"), (51.85, "-ar-"),
            (52.10, "-ran-"), (52.50, "-ging")]  # the original's syllables by its word timings and notes


def vib_glide(m, i, j):
    """vibrato (cents, sd around a quadratic fit of the note) and the glide into it (its first 50 ms against its median)"""
    seg = m[i:j + 1]; ok = np.isfinite(seg)
    if ok.sum() < 5:
        return 0.0, 0.0
    x = np.arange(len(seg))[ok]; y = seg[ok]
    vib = float(np.std(y - np.polyval(np.polyfit(x, y, 2), x)) * 100)
    head = seg[:5][np.isfinite(seg[:5])]
    return vib, float((np.mean(head) - np.median(y)) * 100) if len(head) else 0.0


def notes_of(v, a, b):
    """the sung notes of v in [a, b]: runs of voiced 10 ms frames whose pitch stays within 60 cents of the run's median,
    40 ms or longer -> [(start, end, median MIDI, start index, end index)], with the 10 ms track"""
    t, f = f0(v, a, b)
    m = midi(f)
    out, i = [], 0
    while i < len(m):
        if not np.isfinite(m[i]):
            i += 1; continue
        j = i
        while j + 1 < len(m) and np.isfinite(m[j + 1]) and abs(m[j + 1] - np.median(m[i:j + 1])) < 0.6:
            j += 1
        if j - i >= 3:
            out.append((float(t[i]), float(t[j] + 0.01), float(np.median(m[i:j + 1])), i, j))
        i = j + 1
    return out, t, m


def intonation(name="current", save=True):
    """the original's notes against OLD (the v13 line), note by note: the note, what OLD sings over the same time (octave
    slips of the pitch tracker folded), when OLD reaches it (ms against the original), the glide into it and the vibrato
    (each over its steady part); which syllable each sings there"""
    _, vo = split("original"); _, vc = split(name)
    sc = [(s_, t) for s_, t in syllables(vc, SP_NEW) if t]
    syl_o = lambda t: next(x for tt, x in reversed(ORIG_SYL) if tt <= t + 0.02)
    syl_c = lambda t: next((x for x, tt in reversed(sc) if tt <= t + 0.06), sc[0][0])
    notes, t, mo = notes_of(vo, 49.45, 52.95)
    _, fc = f0(vc, 49.45, 52.95); mc = midi(fc)
    rows = []
    for (a, b, med, i, j) in notes:
        cm = mc[max(0, i - 15):j + 1].copy()
        cm = np.where(np.isfinite(cm), cm - 12 * np.round((cm - med) / 12), np.nan)  # octave slips folded
        body = cm[min(15, i):]
        if np.isfinite(body).sum() < 3:
            continue
        c = float(np.nanmedian(body))
        hit = np.where(np.abs(cm - med) < 0.4)[0]
        land = int((hit[0] - min(15, i)) * 10) if len(hit) else None
        steady = body[np.abs(body - c) < 0.6]
        vib_c = float(np.std(steady - np.polyval(np.polyfit(np.arange(len(steady)), steady, 2), np.arange(len(steady)))) * 100) if len(steady) > 4 else 0.0
        vo_, go = vib_glide(mo, i, j)
        head = body[:5][np.isfinite(body[:5])]
        gc = float((np.mean(head) - c) * 100) if len(head) else 0.0
        rows.append(dict(t=round(a, 2), end=round(b, 2), orig_syl=syl_o(a), note=round(med, 2), old_syl=syl_c(a), old=round(c, 2),
                         cents=round(float((c - med) * 100)), land_ms=land, glide_orig=round(go), glide_old=round(gc),
                         vib_orig=round(vo_), vib_old=round(vib_c)))
    hdr = (f"{'time':>11}  {'original':8} {'note':>6}  {'OLD sings':9} {'note':>6}  {'cents':>6}  {'lands':>6}  "
           f"{'glide in orig/OLD':>17}  {'vibrato orig/OLD':>16}")
    lines = [hdr] + [f"{r['t']:5.2f}-{r['end']:5.2f}  {r['orig_syl']:8} {r['note']:6.2f}  {r['old_syl']:9} {r['old']:6.2f}  {r['cents']:+6d}  "
                     f"{('-' if r['land_ms'] is None else format(r['land_ms'], '+d') + ' ms'):>6}  "
                     f"{r['glide_orig']:+8d} / {r['glide_old']:<+6d}  {r['vib_orig']:7d} / {r['vib_old']:<6d}" for r in rows]
    print("\n".join(lines))
    if save:
        (WORK / "intonation.json").write_text(json.dumps(dict(rows=rows, table=lines), indent=1))
    return rows, lines


def note_shift(vt, t0, shifts, ramp=0.025):
    """PSOLA (Praat, formants kept) of vt's mid channel (window starting at song time t0): over each (a, b, cents) the
    take's own pitch times a constant ratio, 25 ms ramps in and out: its vibrato and timing stay, only the note moves"""
    import parselmouth
    from parselmouth.praat import call
    if not shifts:
        return vt
    # the mid channel only, the side kept (as v8_refine.TUNE: tuning L and R apart reads rough and phasey)
    mid, side = vt.mean(0), (vt[0] - vt[1]) / 2
    out = []
    for ch in (mid,):
        snd = parselmouth.Sound(ch.astype(np.float64), SR)
        man = call(snd, "To Manipulation", 0.01, 90, 1000)
        p = snd.to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
        tier = call("Create PitchTier", "shifted", 0, snd.duration)
        for t, f in zip(p.xs(), p.selected_array["frequency"]):
            if f > 0:
                st = t0 + t
                c = sum(cents * np.clip(min((st - a) / ramp, (b - st) / ramp) + 0.5, 0, 1) for a, b, cents in shifts)
                call(tier, "Add point", t, f * 2 ** (c / 1200))
        call([man, tier], "Replace pitch tier")
        y = call(man, "Get resynthesis (overlap-add)").values[0]
        out.append(np.pad(y, (0, max(0, len(ch) - len(y))))[: len(ch)])
    shifted = np.stack([out[0] + side, out[0] - side]).astype(np.float32)
    # only inside the shifted notes (+ ramps): the rest of the take untouched (resynthesis is not bit-exact)
    s_ = t0 + np.arange(vt.shape[1]) / SR
    m = np.zeros(vt.shape[1])
    for a, b, _ in shifts:
        m = np.maximum(m, np.clip(np.minimum((s_ - (a - 2 * ramp)) / ramp, ((b + 2 * ramp) - s_) / ramp), 0, 1))
    return (vt * (1 - m) + shifted * m).astype(np.float32)


def lift_segments(segs, t0=51.80, t1=LIFT[1], half=1):
    """TUNED c: the lift region from the glide into -ar- on, aimed at the original's contour moved by a delay per
    stretch (segs: [(until, delay)], 40 ms blends of the target), following its glide shapes closely (half=1: 30 ms)"""
    from v8_refine import TUNE
    def f(vt, vo):
        s_ = np.arange(vt.shape[1]) / SR + f.a
        tgt, prev = None, None
        for until, d in segs:
            n = int(d * SR)
            vd = np.concatenate([np.repeat(vo[:, :1], n, 1), vo[:, :-n]], 1) if n else vo
            if tgt is None:
                tgt = vd
            else:
                x = np.clip((s_ - (prev - 0.02)) / 0.04, 0, 1)
                tgt = tgt * (1 - x) + vd * x
            prev = until
        tuned = TUNE(vt, tgt.astype(np.float32), max_cents=800, fold=False, half=half)
        m = np.clip(np.minimum((s_ - t0) / 0.02, (t1 - s_) / 0.02), 0, 1)
        return (vt * (1 - m) + tuned * m).astype(np.float32)
    return f


def lift_dtw(t0=51.80, t1=LIFT[1], half=1):
    """TUNED c: from the glide into -ar- to the end of -ging, aimed at the original's contour time-warped (DTW,
    vsplice.warp) onto the take's own timing, so each glide comes where the take sings its syllable, followed closely
    (half=1: 30 ms)"""
    from v8_refine import TUNE
    import vsplice
    def f(vt, vo):
        i0, i1 = int((t0 - 0.3 - f.a) * SR), int((t1 + 0.2 - f.a) * SR)
        wo, _ = vsplice.warp(vo[:, i0:i1], vt[:, i0:i1])  # the original onto the take's timeline
        tgt = vo.copy(); tgt[:, i0:i1] = wo
        tuned = TUNE(vt, tgt.astype(np.float32), max_cents=800, fold=False, half=half)
        s_ = np.arange(vt.shape[1]) / SR + f.a
        m = np.clip(np.minimum((s_ - t0) / 0.02, (t1 - s_) / 0.02), 0, 1)
        return (vt * (1 - m) + tuned * m).astype(np.float32)
    f.warp = True
    return f


def contour_clock(name, a=51.80, b=52.85):
    """cents between the clip's pitch and the original's on the same clock over [a, b] (the take's syllables sit where the
    original's do): median, and over the transitions (where the original moves more than 50 cents in 30 ms)"""
    _, vo = split("original"); _, vc = split(name)
    _, fo = f0(vo, a, b); _, fc = f0(vc, a, b)
    mo, mc = midi(fo), midi(fc)
    ok = np.isfinite(mo) & np.isfinite(mc)
    c = np.abs(((mc - mo) * 100 + 600) % 1200 - 600)
    mv = np.abs(np.concatenate([[0, 0, 0], mo[3:] - mo[:-3]])) > 0.5
    return dict(all=round(float(np.median(c[ok]))), transitions=round(float(np.median(c[ok & mv]))) if (ok & mv).sum() > 2 else None)


def contour_fit(name, a=51.80, b=52.85):
    """cents between the clip's pitch and the original's contour warped onto the clip's timing (DTW), over [a, b]: median
    and over the transitions (frames where the warped original moves more than 50 cents in 30 ms)"""
    import vsplice
    _, vo = split("original"); _, vc = split(name)
    po, pc = piece(vo, a - 0.3, b + 0.2), piece(vc, a - 0.3, b + 0.2)
    n = min(po.shape[1], pc.shape[1])
    wo, _ = vsplice.warp(po[:, :n], pc[:, :n])
    T_ = lambda x: np.array([0.0])
    import parselmouth
    tr = lambda x: parselmouth.Sound(x.mean(0).astype(np.float64), SR).to_pitch(time_step=0.01, pitch_floor=90, pitch_ceiling=1000)
    p1, p2 = tr(wo), tr(pc[:, :n])
    ts = np.arange(0.3, 0.3 + b - a, 0.01)
    f1 = np.array([p1.get_value_at_time(t) or np.nan for t in ts]); f2 = np.array([p2.get_value_at_time(t) or np.nan for t in ts])
    ok = np.isfinite(f1) & np.isfinite(f2)
    c = np.abs((1200 * np.log2(f2 / f1) + 600) % 1200 - 600)
    m1 = midi(f1); mv = np.abs(np.concatenate([[0, 0, 0], m1[3:] - m1[:-3]])) > 0.5
    return dict(all=round(float(np.median(c[ok]))), transitions=round(float(np.median(c[ok & mv]))) if (ok & mv).sum() > 2 else None)


# Corrected (formants, 1 Oct 2026): the take sings "ran" when the original does (the r at 52.07, the open a of "ran" from
# 52.10 in both); CTC's vowel onset (52.27) was late, so F1's premise was wrong and OLD's lift is on the right syllable.
TUNED = {"a": "the one note far off - -toms on 60, not 63",
         "b": "a and the original's glide shapes into -ar-, -ran- and -ging",
         "c": "F1 alone - the earlier ran fix, which moves the high note later, off ran"}


def tuned_build():
    """TUNED a/b/c of OLD (the v13 line: eu9_7 whole line, untouched, BS-RoFormer, levelled), into song v13"""
    from final11 import paste, V
    from final10 import bounds
    from final13 import hooked, VO_R, ms
    from v8_refine import P16_ALL
    import final12
    rows = json.loads((WORK / "intonation.json").read_text())["rows"]
    # every note more than 40 cents off, 60 ms or longer, outside the lift (52.05-52.85): moved onto the original's
    shifts = [(r["t"], r["end"], -r["cents"]) for r in rows if abs(r["cents"]) > 40 and r["end"] - r["t"] >= 0.06 and r["end"] <= LIFT[0]]
    print("notes moved:", shifts)
    v13 = librosa.load(HERE / "pdoom_EU_v13.wav", sr=SR, mono=False)[0][:, : V.mix.shape[1]]
    a, b = bounds(16)
    cut = lambda y: y[:, int((a - 0.8) * SR):int((b + 0.5) * SR)]

    def chain(*fs):
        def g(vt, vo):
            for h in fs:
                h.a = g.a
                vt = h(vt, vo)
            return vt
        return g

    def shift_hook(vt, vo):
        return note_shift(vt, shift_hook.a, shifts)
    from v8_refine import region
    def glides(t0=51.80, t1=LIFT[1]):
        """OLD's lift extended back to the glide into -ar-, following the original's contour closely (half=1), on the
        same clock (the take's syllables sit where the original's do)"""
        from v8_refine import TUNE
        def f(vt, vo):
            tuned = TUNE(vt, vo, max_cents=600, half=1)
            s_ = np.arange(vt.shape[1]) / SR + f.a
            m = np.clip(np.minimum((s_ - t0) / 0.02, (t1 - s_) / 0.02), 0, 1)
            return (vt * (1 - m) + tuned * m).astype(np.float32)
        return f
    hooks = {"a": chain(region(*LIFT, 600), shift_hook),
             "b": chain(glides(), shift_hook),
             "c": lift_on_take()}
    info = {}
    for k, h in hooks.items():
        Y = hooked(ms(h, 16), 16, "eu9_7", P16_ALL, "bsroformer", VO_R)
        out, sp = paste(v13, Y, a, b)
        LR.mp3(cut(out), SR, WORK / f"L16 TUNED {k} - {TUNED[k]}.mp3")
        info[k] = [[round(float(x), 3), round(float(final12.seam_db(out, v13, x)), 1)] for x in sp]
        print(k, TUNED[k], info[k], flush=True)
    (WORK / "tuned.json").write_text(json.dumps(dict(shifts=shifts, seams=info), indent=1))


def file():
    m = json.loads((WORK / "measure.json").read_text())
    b = json.loads((WORK / "build.json").read_text())
    DESK.mkdir(parents=True, exist_ok=True)
    src = lambda k: next(WORK.glob(f"L16 {k} - *.mp3"))
    shutil.copy(src("original"), DESK / "L16 original - I feel my atoms rearranging.mp3")
    shutil.copy(src("current"), DESK / "L16 current (v13, in the video) - I feel my AC temperatures rearranging.mp3")
    for k, what in FIXES.items():
        shutil.copy(src(k), DESK / f"L16 {k} - {what}.mp3")
    row = lambda k: (f"  {k:9}  {m[k]['ran_note']:6.2f} ({m[k]['ran_cents']:+5d} c)  {m[k]['A_ms']:5d} ms  {m[k]['A_hnr']:5.1f} dB  "
                     f"{m[k]['s_ms']:4d} ms  {m[k]['line_hnr']:+5.1f} dB  " + (", ".join(f"{t:.3f} {d:+.1f} dB" for t, d in b[k]['seams']) if k in b else ""))
    (DESK / "README.txt").write_text(
        "L16 \"I feel my AC temperatures rearranging\": fine-tune, 1 Oct 2026 (\"like 95% close but there's something little off\")\n\n"
        "DIAGNOSIS (the current line against the original, syllable by syllable, on the vocals)\n"
        "In time the line is close: I, feel, my and -ging within 20 ms of the original, re-ar 40 ms; \"A-C tem-pe-ra-tures\" fills the\n"
        "original's \"a-toms\". No clicks; the seams are flat. Two things stand out:\n"
        "  1. \"ran\" is on the wrong note. The take sings \"ran\" 100 ms after the original (vowel 52.27 against 52.17). The\n"
        "     -ranging lift moved the take onto the original's notes by the clock, so the high note (70) sits on the end of\n"
        "     \"re-ar\" (52.10-52.25) and \"ran\" itself is back on 67: 3 semitones (-301 cents) under the original's \"ran\".\n"
        "  2. The \"A\" of \"A-C\" is short and breathy. The original holds the \"a\" of \"atoms\" on 65 for 240 ms (harmonicity\n"
        "     20 dB); the take's \"A\" lasts 80 ms (9 dB, breathy), then a 110 ms \"s\" fills the rest of that note, 5-6 dB under\n"
        "     the original's vowel: the \"corruption between A and C\" you heard in this take before.\n\n"
        "THE FIXES (one per clip; everything else is the current line)\n"
        "  F1  the lift aimed 110 ms later, onto the take's own \"ran\" (one PSOLA pass, at the note's own octave), back on\n"
        "      the original's timing from \"-ging\" (both on 67 there)\n"
        "  F2  \"A-C\" from round 31's L16v2 (eu31_7, whose A holds 65 for 260 ms), swapped in on the vocal between two dips\n"
        "      (after \"my\", and the t of \"tem\")\n"
        "  F3  both\n\n"
        f"  {'clip':9}  {'ran note':16}  {'A on 65':>8}  {'A clarity':>9}  {'s hiss':>7}  {'line':>8}  seams (against v13)\n"
        + "\n".join(row(k) for k in ("original", "current", "F1", "F2", "F3")) + "\n\n"
        "  ran note: the take's \"ran\" (150 ms from its vowel), MIDI and cents against the original's \"ran\"; A: voiced time on\n"
        "  the original's 65 and its harmonicity; s hiss: the \"s\" of \"C\" over 4 kHz; line: harmonicity of the whole line\n"
        "  against the original's. No clicks in any clip.\n\n"
        "TOP PICK: F3. It fixes both: \"ran\" on its high note (-5 cents), the A held clean (250 ms, 18 dB), the line\n"
        "1 dB clearer. If the A-C from the other take sounds like a different voice to you, F1 alone fixes the note.\n"
        "Nothing is in the song yet.\n")
    subprocess.run(["open", str(DESK)])


def tuned_check():
    """each TUNED clip note by note against the original, its ran note, and its clarity against OLD's"""
    out = {}
    _, vold = split("current")
    for k in ("a", "b", "c"):
        name = f"TUNED {k}"
        print(f"\n== TUNED {k}: {TUNED[k]} ==")
        rows, lines = intonation(name, save=False)
        r = assess(name)
        _, vk = split(name)
        out[k] = dict(rows=rows, table=lines, line_hnr=r["line_hnr"],
                      hnr_vs_old=round(hnr(vk, 49.56, 52.82) - hnr(vold, 49.56, 52.82), 1),
                      hnr_toms=round(hnr(vk, 50.85, 51.10) - hnr(vold, 50.85, 51.10), 1), clicks=r["clicks"])
        out[k]["contour"] = contour_clock(name)
        print(f"  clarity {out[k]['hnr_vs_old']:+.1f} dB against OLD (-toms note {out[k]['hnr_toms']:+.1f}); "
              f"against the original's contour, 51.80-52.85: {out[k]['contour']}; clicks {r['clicks']}")
    out["OLD"] = dict(contour=contour_clock("current"))
    print("OLD against the original's contour:", out["OLD"]["contour"])
    (WORK / "tuned_check.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    {"base": base_clips, "diagnose": diagnose, "build": build, "measure": measure, "file": file,
     "intonation": intonation, "tuned": tuned_build, "tuned_check": tuned_check}[sys.argv[1]]()
