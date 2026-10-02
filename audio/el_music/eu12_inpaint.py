"""EU lyrics, round 12: L23 "That was fast enough, we reckoned" (safe -> fast) and L25 "Now privacy in chats obsolete"
(low conditioning; takes 6-10 with alternative spellings). usage: eu12_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

TEXT = {False: ["[Chorus 2]\nThat was fast enough, we reckoned", "[Chorus 2]\nNow privacy in chats obsolete"],
        True: ["[Chorus 2]\nThat was FAST enough, we reckoned", "[Chorus 2]\nNow pri-va-cy in chats ob-so-lete"]}
RANGES = [(69760, 74060), (77720, 81210)]


def plan(alt):
    chunks, t = [], 0
    for (a, b), text in zip(RANGES, TEXT[alt]):
        pos, neg = styles(a)
        if a > t:
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
    name = f"eu12_{k}"
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
