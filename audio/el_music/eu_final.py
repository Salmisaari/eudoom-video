"""Assemble the EU edition song: for every changed line, pick the take (rounds 2-4) that keeps the original
melody (separated-vocal pitch within 60 cents, voicing IoU >= 0.7) and whose words are the new ones
(CTC lyric-fit margin > 0 or Whisper hears the key word); splice winners into the original on line bounds.
A line with no such take stays original. Writes audio/el_music/pdoom_EU_v3.wav and a report."""
import json, pathlib, subprocess, sys
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_select import SR, HERE, orig, vocals, f0, hear, flat
from eu3_build import load, local, bounds, splice_into, mp3
import lyricfit as F

OUT = pathlib.Path.home() / "Desktop/suno_test/eu_v3"
EUD = ["eudoom", "udoom", "youdoom"]
HOOK = ("I'M UPPING MY PEE DOOM", {"A": ("I'm upping my EU doom", "I'M UPPING MY EE YOU DOOM", EUD),
                                    "B": ("I'm upping my U-doom", "I'M UPPING MY YOU DOOM", EUD)})
# line: (old as sung, {variant: (display text, new as sung, whisper keys)}, take pool)
R2 = [f"eu2_{s}{k}" for s, r in (("high", 4), ("medium", 4), ("low", 15)) for k in range(1, r + 1)]
R3 = [f"eu3_{v}{k}" for v in "AB" for k in range(1, 6)]
R4 = [f"eu4_{k}" for k in range(1, 11)]
one = lambda text, sung, keys: {"A": (text, sung, keys), "B": (text, sung, keys)}
LINES = {
    7: (HOOK[0], HOOK[1], R3), 18: (HOOK[0], HOOK[1], R3), 29: (HOOK[0], HOOK[1], R3), 41: (HOOK[0], HOOK[1], R3),
    9: ("TRAPPED IN THE CHINESE ROOM", one("Trapped in the Brussels room", "TRAPPED IN THE BRUSSELS ROOM", ["brussel"]), R2),
    10: ("WITH A BAG OF SHROOMS", one("Where the faxes zoom", "WHERE THE FAXES ZOOM", ["fax"]), R2),
    17: ("SYDNEY PLEASE LET ME FREE", one("Cookies, please let me free", "COOKIES PLEASE LET ME FREE", ["cookie"]), R4),
    19: ("I HEAR THE BASILISK BOOM", {"A": ("I hear the bazooka boom", "I HEAR THE BAZOOKA BOOM", ["bazooka"]),
                                      "B": ("I hear the basic income boom", "I HEAR THE BASIC INCOME BOOM", ["basicincome"])}, R3),
    20: ("EN VEE DEE AY TO THE MOON", one("A-S-M-L to the moon", "AY ESS EM EL TO THE MOON", ["asml"]), R2),
    22: ("ONE EE THIRTY FLOPS A SECOND", one("One E thirty forms a second", "ONE EE THIRTY FORMS A SECOND", ["forms"]), R2 + R3),
    24: ("FORWARD EM EL PEE BACKWARD REPEAT",
         one("Tear down the wall, rebuild it, repeat", "TEAR DOWN THE WALL REBUILD IT REPEAT", ["wall", "rebuild"]), R4),
    27: ("WITHOUT A SINGLE SEE DEE AR", one("Without a single GDPR", "WITHOUT A SINGLE GEE DEE PEE AR", ["gdpr"]), R2),
    28: ("GATO PLEASE DON'T LET ME GO", one("NATO, please don't let me go", "NATO PLEASE DON'T LET ME GO", ["nato"]), R2),
    31: ("KILLSWITCH GUY'S ON PEE TEE OH", {"A": ("Brussels guy's on PTO", "BRUSSELS GUY'S ON PEE TEE OH", ["brussel"]),
                                            "B": ("Whole EU's on PTO", "WHOLE EE YOU'S ON PEE TEE OH", ["wholeeu", "holeeu", "wholeu"])}, R3),
    34: ("ORTHOGONALITY THESIS BLUES", one("Euro-banality thesis blues", "EURO BANALITY THESIS BLUES", ["banality"]), R2),
    40: ("AR EL AITCH EF GOES ASKEW", one("The AI Act goes askew", "THE AY EYE ACT GOES ASKEW", ["aiact", "aact", "eyeact"]), R2),
    45: ("WHAT DID ILYA SEE WE'LL NEVER KNOW",
         one("What did Draghi see? We'll never know", "WHAT DID DRAGHI SEE WE'LL NEVER KNOW", ["draghi", "dragi", "draggy"]), R2 + R3),
}
cache_f = HERE / "eu_final_cache.json"
cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
refs = {}


def contour_match(voc, t0, a, b, ref):
    """performance() on an already separated vocal: octave-safe median pitch error (cents), voicing IoU."""
    f, vo = f0(voc)
    rf, rvo = ref
    k = min(len(f), len(rf))
    t = t0 + np.arange(k) * 256 / 22050
    w = (t >= a) & (t < b)
    both, either = w & vo[:k] & rvo[:k], w & (vo[:k] | rvo[:k])
    c = 1200 * np.log2(f[:k][both] / rf[:k][both])
    return (float(np.median(np.abs((c + 600) % 1200 - 600))) if both.any() else 999.0,
            float(both.sum() / max(either.sum(), 1)))


def evaluate(name, y, n):
    old, variants, _ = LINES[n]
    v = "B" if name.startswith("eu3_B") else "A"
    text, sung, keys = variants[v]
    key = f"{name}|L{n}|{sung}"
    if key not in cache:
        a, b = bounds(n)
        if n not in refs:
            refs[n] = f0(vocals(orig, a, b)[0])
        yl = local(y, a, b)
        voc, t0 = vocals(yl, a, b)  # one separation feeds both the pitch and the lyric check
        err, iou = contour_match(voc, t0, a, b, refs[n])
        em = F.emissions(voc[int(0.8 * 22050):len(voc) - int(0.8 * 22050)], 22050)
        heard = hear(splice_into(orig, yl, a, b), a - 0.3, b + 0.3)
        cache[key] = dict(take=name, text=text, err=round(err), iou=round(iou, 2),
                          margin=round(F.margin(em, old, sung), 1), heard=heard,
                          key=any(k in flat(heard) for k in keys))
        cache_f.write_text(json.dumps(cache, indent=1))
    return cache[key]


if __name__ == "__main__":
    rows = {n: [] for n in LINES}
    for name in sorted({t for _, _, pool in LINES.values() for t in pool}):
        y = load(name)
        for n, (_, _, pool) in LINES.items():
            if name in pool:
                rows[n].append(evaluate(name, y, n))
        print("scored", name, flush=True)

    song, report = orig.copy(), {}
    for n in sorted(LINES):
        ok = [r for r in rows[n] if r["err"] <= 60 and r["iou"] >= 0.7 and (r["margin"] > 0 or r["key"])]
        best = max(ok, key=lambda r: r["margin"] + 10 * r["key"]) if ok else None
        if best:
            a, b = bounds(n)
            song = splice_into(song, local(load(best["take"]), a, b), a, b)
        report[n] = best
        print(f"L{n:02d} " + (f"{best['take']:10s} {best['text']!r:40s} pitch {best['err']:3d}c IoU {best['iou']:.2f} "
                              f"fit {best['margin']:+6.1f} | {best['heard']}" if best else "KEPT ORIGINAL (no take kept melody + words)"),
              flush=True)
    import soundfile as sf
    sf.write(HERE / "pdoom_EU_v3.wav", song.T, SR)
    mp3(song, OUT / "pdoom_EU_edition_v3.mp3", "320k")
    (HERE / "eu_final_report.json").write_text(json.dumps({f"L{n}": r for n, r in report.items()}, indent=1))

    gap, reel, idx, t = np.zeros((2, int(0.6 * SR)), dtype=np.float32), [], [], 0.0
    for n, r in report.items():
        if not r:
            continue
        a, b = bounds(n)
        for lab, y in (("original", orig), (r["text"], song)):
            c = y[:, int((a - 1) * SR):int((b + 1) * SR)]
            idx.append(f"{int(t // 60)}:{t % 60:04.1f}  L{n:02d} {lab}")
            reel += [c, gap]
            t += c.shape[1] / SR + 0.6
    mp3(np.concatenate(reel, 1), OUT / "v3_changes_before_after.mp3")
    (OUT / "v3_changes_before_after.txt").write_text("\n".join(idx) + "\n")
