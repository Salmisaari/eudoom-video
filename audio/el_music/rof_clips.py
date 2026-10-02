"""The final lines rebuilt on the BS-RoFormer vocal split (rof.py) instead of Demucs, everything else as the approved
clip. Measured with that split (compare.py, offsets.py), the Demucs builds are off where the Demucs estimate of the
ORIGINAL vocal is off, because the swap subtracts it (out = mix - V_orig + V_take) and matches the take's level and
tone (1/3-octave) to it: L24K sits 1.5-3 dB under the original singer, L16M's voice is 9 dB thin at 125-250 Hz.
With RoFormer both the subtraction and the reference are the better estimate (vocal SDR ~13 dB vs ~9).
Measured the same way, the takes' vocals are wider than the original singer's: their side (stereo reverb, doubles) is
3-8 dB louder against the centre, so at the same total level the centre voice is quieter (L24: 2 dB). ms() levels the
take's centre and sides separately to the original singer's over the line (plain gains, +-6 dB), as a mix engineer
would set width.
Clips in eu_v8_lines under the next letters; the approved ones stay as they are."""
import sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v8_refine import write, V, region, P16_ALL
from l24_s import s_boost
from r22_clips import P24
from final12 import P
import l910, l910_hold, rof

V.VO = rof.original(V.mix)


def ms(hook, n, limit=6):
    """hook's result (or the take) with its mid and side each at the original vocal's level over line n"""
    t_a, t_b = V.LYR[n - 1]["start"], V.LYR[n - 1]["end"]

    def f(vt, vo):
        if hook is not None:
            hook.a = f.a
            vt = hook(vt, vo)
        s = slice(int((t_a - f.a) * V.SR), int((t_b - f.a) * V.SR))
        MS = lambda x: (x.mean(0), (x[0] - x[1]) / 2)
        (mt, st), (mo, so) = MS(vt), MS(vo)
        db = lambda x: 10 * np.log10(np.mean(x[s] ** 2) + 1e-12)
        gm, gs = (np.clip(db(o) - db(t), -limit, limit) for o, t in ((mo, mt), (so, st)))
        print(f"  L{n}: centre {gm:+.1f} dB, sides {gs:+.1f} dB", flush=True)
        mt, st = mt * 10 ** (gm / 20), st * 10 ** (gs / 20)
        return np.stack([mt + st, mt - st]).astype(np.float32)
    return f
SEP = "bsroformer"
CLIPS = {"L16N": (16, "eu9_7", P16_ALL, region(52.05, 52.85, 600), "L16M on the RoFormer split", "I feel my AC temperatures rearranging"),
         "L20K": (20, "eu18_3", P["20i"], None, "L20I on the RoFormer split", "Nokia to the moon"),
         "L24O": (24, "eu22_3", P24, s_boost(8), "L24K on the RoFormer split", "Forward SAP, backward, repeat"),
         "L24P": (24, "eu22_3", P24, None, "L24K on the RoFormer split, without the S lift", "Forward SAP, backward, repeat"),
         "L9-10N": (l910.N, "eu2_low4", l910.PLAN, l910_hold.hold(False, 28.74), "L9-10K on the RoFormer split",
                    "Trapped in the Brussels room, where the faxes zoom")}
# the same with the centre and sides levelled to the original singer's
for key, new in (("L16N", "L16O"), ("L20K", "L20L"), ("L24O", "L24Q"), ("L9-10N", "L9-10O")):
    n, take, plan, hook, desc, text = CLIPS[key]
    CLIPS[new] = (n, take, plan, ms(hook, n), desc.replace("on the RoFormer split", "on the RoFormer split, centre/sides levelled"), text)
# L9-10: + the original's word weight (loudness contour, +-5 dB; "where" sat +4 dB, "fa-xes" -4 dB)
# and (measured on P's first build) "the" 3 semitones over the original's "a", "where" still +6 dB over the soft "with"
CLIPS["L9-10P"] = (l910.N, "eu2_low4", l910.PLAN,
                   ms(l910_hold.hold(True, 28.74, db=5, lifts=(((27.95, 28.38), 600), (l910_hold.ES, 1000)),
                                     rides=(((27.98, 28.2), -4),)), l910.N),
                   "L9-10K on the RoFormer split, centre/sides levelled, the original's word weight (+-5 dB), "
                   "'the' on the original's note, 'where' -4 dB",
                   "Trapped in the Brussels room, where the faxes zoom")
# and "where the" in the original's time: the take sings it ~0.12 s early and then hisses a 0.15 s "f" where the original
# sings "a"; "where the" (28.02-28.24) lengthened x1.55 to end at 28.36, the f from there (60 ms, like the original's b)
CLIPS["L9-10Q"] = (l910.N, "eu2_low4", l910.PLAN,
                   ms(l910_hold.hold(True, 28.74, db=5, lifts=(((27.95, 28.40), 600), (l910_hold.ES, 1000)),
                                     rides=(((27.98, 28.2), -4),), retimes=((28.02, 28.24, 28.36),),
                                     trans=0.11), l910.N),  # + the first 30 ms of the s, so it starts as sung
                   "L9-10P with 'where the' in the original's time (lengthened x1.55, the f after it shortened)",
                   "Trapped in the Brussels room, where the faxes zoom")
if __name__ == "__main__":
    for key, (n, take, plan, hook, desc, text) in CLIPS.items():
        if len(sys.argv) > 1 and key not in sys.argv[1:]:
            continue
        label = key[:-1]
        write(n, take, plan, SEP, False, hook, desc, text, letter=key[-1], label=label)
