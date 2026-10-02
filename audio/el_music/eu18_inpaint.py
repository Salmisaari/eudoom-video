"""L20 "Nokia to the moon", round 18. Rounds 14-17 used a 3.5 s L19-L20 chunk and never landed the name. This goes
back to the round 2 layout that landed "Ay-Ess-Em-Ell to the moon" (v4's L20): one 5 s chunk over L18-L20, all three
lines in the text. Only L20 is used. Takes 1-4 "Nokia", 5-8 "Noh-kee-ah", 9-12 "No-kee-yah". Round 19 (takes 13-28)
kept the two spellings that hit: the spelling changes every 4 takes, cycling through the names given.
Round 21 (takes 29-40, WIDE=1): 7.6 s over L18-L21, so the name sits mid-phrase with "The Omega Point's coming soon"
after it.
usage: [WIDE=1] eu18_inpaint.py <first> <last> [name ...]   writes eu18_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

WIDE = os.environ.get("WIDE") == "1"
A, B = (58620, 66220) if WIDE else (59130, 64100)
NAMES = sys.argv[3:] or ["Nokia", "Noh-kee-ah", "No-kee-yah"]


def spelling(k):
    return NAMES[(k - 1) // 4 % len(NAMES)]


def plan(k):
    pos, neg = styles(A)
    text = f"[Chorus 2]\nI'm upping Ee-You doom\nI hear the basic income gloom\n{spelling(k)} to the moon" + ("\nThe Omega Point's coming soon" if WIDE else "")
    return {"chunks": [{"song_id": SID, "range": {"start_ms": 0, "end_ms": A}},
                       {"text": text, "duration_ms": B - A, "positive_styles": pos, "negative_styles": neg,
                        "context_adherence": "high",
                        "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}},
                        "condition_strength": "low"}]
                      + [{"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}} for s0 in range(B, END, 120000)]}


def take(k):
    name = f"eu18_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok ({spelling(k)})"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    first, last = int(sys.argv[1]), int(sys.argv[2])
    bad = 0
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(take, range(first, last + 1)):
            print(r, flush=True)
            if not r.endswith(" ok"):
                bad += 1
    sys.exit(1 if bad else 0)
