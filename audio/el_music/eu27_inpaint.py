"""Round 27, the user's ideas (2026-10-01): L11 "See through Pinocchio's lies" (the plate on screen there; was "See through
the shoggoth's lies") and L12 "with your Eurovision eyes" (Eu-ro-vi-sion on shi-ni-ga-mi, syllable for syllable).
One chunk over both lines, conditioned low on the original's; it ends after the held "eyes".
k % 3 picks the spelling of each line. usage: eu27_inpaint.py <first> <last>  -> eu27_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

# one chunk over both lines (a chunk must be >= 3 s; L12 alone to the end of its held "eyes" is 2.2 s), both lines in the
# text, which also landed the hard name in L20
GEN = [(29910, 35600, ["[Chorus 1]\nSee through Pinocchio's lies\nwith your Eurovision eyes",
                       "[Chorus 1]\nSee through Pi-noc-chi-o's lies\nwith your Eu-ro-vi-sion eyes",
                       "[Chorus 1]\nSee through the Pinocchio's lies\nwith Eurovision eyes"])]


def plan(k):
    chunks, t = [], 0
    for a, b, texts in GEN:
        pos, neg = styles(a)
        if a > t:
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": texts[(k - 1) % len(texts)], "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high", "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu27_{k}"
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
