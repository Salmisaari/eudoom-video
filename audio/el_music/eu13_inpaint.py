"""EU lyrics, round 13: L25 "Now privacy in chats obsolete" and L40 "EU Inc fixes things soon" with a held "soon" (the
original holds "askew"; round 11 sang extra words into it). Takes 1-4 low, 5-7 low with alternative spellings, 8-10 medium. usage: eu13_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

TEXT = {"A": ["[Chorus 2]\nNow privacy in chats obsolete", "[Bridge]\nEe-You Inc fixes things soo-oon"],
        "B": ["[Chorus 2]\nNow privacy-in-chats obsolete", "[Bridge]\nE. U. Inc. fixes things, soooon"]}
KIND = {k: ("A", "low") if k <= 4 else ("B", "low") if k <= 7 else ("A", "medium") for k in range(1, 11)}
RANGES = [(77720, 81210), (120760, 124520)]


def plan(k):
    alt, strength = KIND[k]
    chunks, t = [], 0
    for (a, b), text in zip(RANGES, TEXT[alt]):
        pos, neg = styles(a)
        if a > t:
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text, "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": strength})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu13_{k}"
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
            print(r)
