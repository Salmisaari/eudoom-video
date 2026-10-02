"""Round 36 (2026-10-01): L21 round 2. The user OK'd adjusting the lyric; the stressed "I" goes on the strong beat where
"Point's" was (64.74 s), the letters before it on O-me-ga. Three lyrics, 4 takes each (2 spellings x 2), the same couplet
chunk and conditioning as round 35 (eu35_inpaint.py):
  A  "Your U-B-I's coming soon"
  B  "The U-B-I's coming soon"
  C  "The E-U-B-I's coming soon"  (the EU's UBI: ee-yoo-bee-eye on O-me-ga-Point's, one letter per note)
usage: eu36_inpaint.py A|B|C <first> <last>  -> eu36a_<k>.mp3 ... (k % 2 picks the spelling)"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles
from eu35_inpaint import A, B, L20

TEXTS = {"A": ["Your you-bee-eye's coming soon", "Your U-B-I's coming soon"],
         "B": ["The you-bee-eye's coming soon", "The U-B-I's coming soon"],
         "C": ["The ee-you-bee-eye's coming soon", "The E-U-B-I's coming soon"]}


def plan(lyric, k):
    pos, neg = styles(A)
    chunks = [{"song_id": SID, "range": {"start_ms": s0, "end_ms": min(A, s0 + 120000)}} for s0 in range(0, A, 120000)]
    chunks += [{"text": f"[Chorus 2]\n{L20}\n{TEXTS[lyric][(k - 1) % 2]}", "duration_ms": B - A, "positive_styles": pos,
                "negative_styles": neg, "context_adherence": "high",
                "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}}, "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(args):
    lyric, k = args
    name = f"eu36{lyric.lower()}_{k}"
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
