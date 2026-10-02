"""Round 33 (2026-10-01): L37 once more from the user's favourite, L37v17 (eu32a_3: "Post-AI bubble, super-dense"):
"really close, only AI should be almost like AIJAI so there's the 'yah' sound between A I like normally in its
pronunciation", i.e. the English glide, ay-YAI. The same chunk and conditioning as round 32 (eu32_inpaint.py, over L37
and L38, low on the original); spellings that force the glide, k % 4.
usage: eu33_inpaint.py <first> <last>  -> eu33_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles
from eu32_inpaint import A, B, L38

TEXTS = ["Post-ay-yai bubble, super-dense", "Post-A-yai bubble, super-dense", "Post-Ay-Eye bubble, super-dense",
         "Post-AY-YAI bubble, super-dense"]


def plan(k):
    pos, neg = styles(A)
    chunks = [{"song_id": SID, "range": {"start_ms": 0, "end_ms": A}},
              {"text": f"[Bridge]\n{TEXTS[(k - 1) % len(TEXTS)]}\n{L38}", "duration_ms": B - A, "positive_styles": pos,
               "negative_styles": neg, "context_adherence": "high",
               "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}}, "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu33_{k}"
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
