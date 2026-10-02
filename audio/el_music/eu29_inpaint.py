"""Round 29 (2026-10-01): "Now plastic straws are obsolete" (the user: round 25 sang "plastic" as one word; it must
split plas | tic over the original's von | Neu, and "are" fills the missing sound). Spellings push the split.
Same window and conditioning as eu12/eu26. usage: eu29_inpaint.py <first> <last>  -> eu29_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 77720, 81210
TEXTS = ["[Chorus 2]\nNow plas-tic straws are ob-so-lete", "[Chorus 2]\nNow plaaas-tic straws are obsolete", "[Chorus 2]\nNow PLAS. TIC. straws are obsolete"]


def plan(k):
    pos, neg = styles(A)
    chunks = [{"song_id": SID, "range": {"start_ms": 0, "end_ms": A}},
              {"text": TEXTS[(k - 1) % len(TEXTS)], "duration_ms": B - A, "positive_styles": pos, "negative_styles": neg,
               "context_adherence": "high", "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}},
               "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu29_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(take, range(int(sys.argv[1]), int(sys.argv[2]) + 1)):
            print(r, flush=True)
