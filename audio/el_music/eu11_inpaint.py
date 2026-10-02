"""EU lyrics, round 11: more takes for L35 "Build unicorns all the way!" and L40 "EU Inc fixes things soon" (low
conditioning; takes 6-10 with alternative spellings). usage: eu11_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

TEXT = {False: ["[Bridge]\nBuild unicorns all the way!", "[Bridge]\nEe-You Inc fixes things soon"],
        True: ["[Bridge]\nBuild you-ni-corns all the way!", "[Bridge]\nE. U. Inc. fixes things soon"]}
RANGES = [(110180, 113340), (120760, 124520)]


def plan(alt):
    chunks, t = [], 0
    for (a, b), text in zip(RANGES, TEXT[alt]):
        pos, neg = styles(a)
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text, "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu11_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(k > 5), "model_id": "music_v2_5"}).encode(),
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
