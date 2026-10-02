"""Round 25, the user's new L25 (2026-10-01): "Now plastic straws obsolete" in place of "Now von Neumann's obsolete"
(plas-tic-straws on von-Neu-mann's, syllable for syllable; the EU's single-use plastics directive (EU) 2019/904 took
plastic straws off the market from 3 July 2021). The line's own window, conditioned low on the original (as eu12,
whose take 8 is L25 in v9). k % 3 picks the spelling. usage: eu25_inpaint.py <first> <last>  -> eu25_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 77720, 81210
TEXTS = ["[Chorus 2]\nNow plastic straws obsolete", "[Chorus 2]\nNow plas-tic straws ob-so-lete", "[Chorus 2]\nNow PLAS-tic STRAWS obsolete"]


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
    name = f"eu25_{k}"
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
