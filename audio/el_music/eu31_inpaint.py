"""Round 31 (2026-10-01): L16 "I feel my AC temperatures rearranging", like round 30 did L9-10 (the user: "AC
temperatures need similar work"). One chunk over the line, conditioned low on the original's own stretch, "I feel my
atoms rearranging", whose "atoms" is a melisma on four notes (65 63 63 60, 50.25-51.04 s): A-C tem-pra-tures takes
one syllable per note and the last on the tail; "-ranging" holds 70 67 67 (52.13-52.71). k % 3 picks the spelling.
usage: eu31_inpaint.py <first> <last>  -> eu31_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 49560, 52830
TEXTS = ["[Verse 2]\nI feel my AC temperatures rearranging",
         "[Verse 2]\nI feel my A-C tem-pra-tures re-ar-rang-ing",
         "[Verse 2]\nI feel my AY-SEE TEM-pra-tures re-ar-RANG-ing"]


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
    name = f"eu31_{k}"
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
