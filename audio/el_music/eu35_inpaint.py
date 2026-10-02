"""Round 35 (2026-10-01): L21 "The Omega Point's coming soon" (64.10 s) tried as "The UBI point's coming soon" (the EU
basic-income citizens' initiative, registered 7 Jul 2026). U-B-I on O-me-ga, syllable for syllable, the stress moving
to the I. L21 is 2.1 s and a chunk must be >= 3 s, so the chunk runs over L20 and L21 (the moon/soon couplet), both lines
in the text, conditioned low on the original's own stretch; only L21 is spliced. k % 3 picks the spelling.
usage: eu35_inpaint.py <first> <last>  -> eu35_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

A, B = 62540, 66220
L20 = "Nokia to the moon"
TEXTS = ["The U-B-I point's coming soon", "The you-bee-eye point's coming soon", "The UBI Point's coming soon"]


def plan(k):
    pos, neg = styles(A)
    chunks = [{"song_id": SID, "range": {"start_ms": s0, "end_ms": min(A, s0 + 120000)}} for s0 in range(0, A, 120000)]
    chunks += [{"text": f"[Chorus 2]\n{L20}\n{TEXTS[(k - 1) % len(TEXTS)]}", "duration_ms": B - A, "positive_styles": pos,
                "negative_styles": neg, "context_adherence": "high",
                "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}}, "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu35_{k}"
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
