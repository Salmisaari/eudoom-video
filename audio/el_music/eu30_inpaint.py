"""Round 30 (2026-10-01): L9-10 "Trapped in the Brussels room, where the faxes zoom" once more. v11 still uses eu2_low4
on the old mid-tuned Demucs path, and the user hears it as a little rough. This round uses what L11/L12 (eu27) taught:
one chunk over the two lines only, both lines in the text, conditioned low on the original's own stretch
("Trapped in the Chinese room, with a bag of shrooms": Chi-nese on Brus-sels, with-a-bag-of-shrooms on where-the-fax-es-
zoom). The chunk starts after the held "FOOM" (its note ends 26.08) and ends after the held "zoom", where L11 begins.
k % 3 picks the spelling. usage: eu30_inpaint.py <first> <last>  -> eu30_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 26200, 29910
TEXTS = ["[Chorus 1]\nTrapped in the Brussels room,\nwhere the faxes zoom",
         "[Chorus 1]\nTrapped in the Brus-sels room,\nwhere the fax-es zoom",
         "[Chorus 1]\nTrapped in the BRUS-sels room,\nwhere the FAX-es ZOOM"]


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
    name = f"eu30_{k}"
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
