"""Round 32 (2026-10-01): L37 "Post-Chinchilla, super-dense" (115.2 s), the user: "POST AI BUBBLE", and "POST BUBBLE ALL
MAKES SENSE could be also another alternative ... when the ai bubble pops then we see what's left". Two lyrics:
  A  "Post-AI-bubble, super-dense"  post-A-I-bub-ble su-per-dense on post-chin-chil-la su-per-dense (one syllable
     more); four spellings, the last literally "Post AI bubble" stretched over the line
  B  "Post-bubble, all makes sense"  post-bub-ble all makes sense, rhyming with L38's "fence"
L37 is 1.8 s and a chunk must be >= 3 s, so the chunk runs over L37 and L38 ("Breaking through each safety fence", the
rhyme), both lines in the text, conditioned low on the original's own stretch; L37 is spliced alone (like eu27).
usage: eu32_inpaint.py A|B <first> <last>  -> eu32a_<k>.mp3 / eu32b_<k>.mp3 (k % len(spellings) picks the spelling)"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 115200, 118760
L38 = "Breaking through each safety fence"
TEXTS = {"A": ["Post-AI-bubble, super-dense", "Post A.I. bubble, super-dense", "Post-AI bubble, super-dense", "Post AI bubble"],
         "B": ["Post-bubble, all makes sense", "Post-bub-ble, all makes sense", "POST-bubble, ALL makes SENSE"]}


def plan(lyric, k):
    pos, neg = styles(A)
    text = TEXTS[lyric][(k - 1) % len(TEXTS[lyric])]
    chunks = [{"song_id": SID, "range": {"start_ms": 0, "end_ms": A}},
              {"text": f"[Bridge]\n{text}\n{L38}", "duration_ms": B - A, "positive_styles": pos, "negative_styles": neg,
               "context_adherence": "high", "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}},
               "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(args):
    lyric, k = args
    name = f"eu32{lyric.lower()}_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(lyric, k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    lyric = sys.argv[1]
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(take, [(lyric, k) for k in range(int(sys.argv[2]), int(sys.argv[3]) + 1)]):
            print(r, flush=True)
