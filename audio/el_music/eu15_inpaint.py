"""L20-only regeneration. The L19-L20 span is re-sung so the chunk is long enough; L19 is not for use.
Rounds 14-16 sang "to the moon" or a garbled name, never Nokia in that slot. Round 17 gives the
whole span nothing but the name, so the NVDA notes have no other lyric to fall back on.
Takes 1-3 repeat the near-hit spelling, 4-6 repeat the word itself.
usage: eu15_inpaint.py <first> <last>   writes eu17_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

GEN = [(60580, 64100, [
    "[Chorus 2]\nNo-kai-ya. No-kai-ya. No-kai-ya.",
    "[Chorus 2]\nNokia. Nokia. Nokia.",
])]


def plan(k):
    chunks, t = [], 0
    for a, b, texts in GEN:
        pos, neg = styles(a)
        if a > t:
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": texts[0 if k <= 3 else 1], "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu17_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    first, last = int(sys.argv[1]), int(sys.argv[2])
    bad = 0
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(take, range(first, last + 1)):
            print(r, flush=True)
            if not r.endswith(" ok"):
                bad += 1
    sys.exit(1 if bad else 0)
