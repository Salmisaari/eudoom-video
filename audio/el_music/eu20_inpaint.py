"""Round 20: the wider-window layout that landed Nokia in round 18, for the other lines the user heard as broken in v7
and that round 14's 3.5 s chunks never sang cleanly. Each chunk carries the line before it with its current words.
  L7-L10  "I'm upping Ee-You doom / 'Cause the future goes foom / Trapped in the Brussels room, / where the faxes zoom"
  L15-16  "And you're optimizing, accelerating, / I feel (my) Ay-See temperatures rearranging"
  L39-40  "Hundred thousand GPU / Ee-You Ink fixes things, soooon"
Odd takes: L16 without "my" (the user's wording), L40 "Ee-You Ink"; even takes: with "my", "E. U. Inc.".
usage: eu20_inpaint.py <first> <last>   writes eu20_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

GEN = [(22760, 29910, ["[Chorus 1]\nI'm upping Ee-You doom\n'Cause the future goes foom\nTrapped in the Brussels room,\nwhere the faxes zoom"] * 2),
       (45060, 52830, ["[Verse 2]\nAnd you're optimizing, accelerating,\nI feel Ay-See temperatures rearranging",
                       "[Verse 2]\nAnd you're optimizing, accelerating,\nI feel my Ay-See temperatures rearranging"]),
       (118700, 124520, ["[Bridge]\nHundred thousand GPU\nEe-You Ink fixes things, soooon",
                         "[Bridge]\nHundred thousand GPU\nE. U. Inc. fixes things, soooon"])]


def plan(k):
    chunks, t = [], 0
    for a, b, texts in GEN:
        pos, neg = styles(a)
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": texts[(k - 1) % 2], "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu20_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
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
