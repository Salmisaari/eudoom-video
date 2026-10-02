"""L9-10V: U ("much better": T on the RoFormer split, levelled), pushed further on what still measures off against the
original (compare.py / offsets.py / the clarity check):
  - the pitch correction only where the take is off: U runs the whole line through PSOLA, which smears a little even
    where it changes nothing; here the corrected signal is used only where the take is >25 cents from the original's
    curve (dilated 30 ms, 20 ms ramps), the take untouched elsewhere
  - "-es" of faxes onto the original's "of" (E sings it ~4 semitones under; round 5's G/J lift)
  - width: the take sits 4-6 dB narrower than the original on "the", "room", "with": its side follows the original's
    side/mid contour (+-4 dB, 100 ms)
  - loudness contour +-5 dB (U: +-4), then the m of "zoom" and the centre/sides levelling as U."""
import sys, pathlib
import numpy as np, librosa, parselmouth
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import l910
from l910_m import m_close
from l910_weight import weight, mask, ES
from v8_refine import write, V, TUNE


def off_mask(x, vo, t0, cents=25):
    """1 where the take's pitch is more than cents from the original's (both voiced), dilated 30 ms, 20 ms ramps"""
    pt = lambda y: parselmouth.Sound(y.mean(0).astype(np.float64), V.SR).to_pitch_ac(
        time_step=0.01, pitch_floor=100, pitch_ceiling=1000)
    px, po = pt(x), pt(vo)
    ts = np.arange(0, x.shape[1] / V.SR, 0.01)
    fx = np.array([px.get_value_at_time(t) for t in ts]); fo = np.array([po.get_value_at_time(t) for t in ts])
    c = np.abs(1200 * np.log2(fo / fx))
    off = np.isfinite(c) & (c > cents) & (c < 1250)
    off = np.convolve(off.astype(float), np.ones(7), "same") > 0  # +-30 ms
    m = np.interp(np.arange(x.shape[1]) / V.SR, ts, off.astype(float))
    return np.clip(np.convolve(m, np.ones(882) / 882, "same"), 0, 1)  # 20 ms ramps


def width_ride(x, vo, db=4):
    """x's side gain following the original's side/mid contour (100 ms), +-db, where both sing"""
    env = lambda s: 10 * np.log10(np.convolve(s ** 2, np.ones(4410) / 4410, "same") + 1e-12)
    mx, sx = x.mean(0), (x[0] - x[1]) / 2
    mo, so = vo.mean(0), (vo[0] - vo[1]) / 2
    act = (env(mo) > env(mo).max() - 35) & (env(mx) > env(mx).max() - 35)
    g = np.where(act, (env(so) - env(mo)) - (env(sx) - env(mx)), 0.0)
    g = np.convolve(np.clip(g, -db, db), np.ones(4410) / 4410, "same")
    sx = sx * 10 ** (g / 20)
    return np.stack([mx + sx, mx - sx]).astype(np.float32)


def hook_v():
    def f(vt, vo):
        tuned = TUNE(vt, vo, half=1)
        # "where the": the take's "the" is too short for the pitch check to see it (it came out +108 cents); corrected
        # there regardless, like U
        m = np.maximum(off_mask(vt, vo, f.a), mask(vt.shape[1], f.a, [(27.95, 28.40)]))
        x = vt * (1 - m) + tuned * m
        e = mask(x.shape[1], f.a, [ES])
        x = x * (1 - e) + TUNE(x, vo, max_cents=1000, fold=False) * e
        x = weight(x, vo, f.a, 5)
        x = width_ride(x, vo)
        return m_close(x, f.a)
    return f


if __name__ == "__main__":
    import rof_clips  # the RoFormer split of the original as V.VO
    h = rof_clips.ms(hook_v(), l910.N)
    write(l910.N, "eu2_low4", l910.PLAN, "bsroformer", False, h,
          "U with the pitch fixed only where it's off, -es on the original's note, width and loudness like the original",
          "Trapped in the Brussels room, where the faxes zoom", label="L9-10", letter="V")
