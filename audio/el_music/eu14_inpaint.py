"""EU lyrics, round 14 (after animatic_v7): fresh takes for every line the user heard as broken or not smooth, sung
as whole phrases so they can be spliced untouched (no time-warp, no pitch-tune -- the lines the user flagged in v7
were all warped and/or tuned):
  L9-L10  "Trapped in the Brussels room, where the faxes zoom" (one take across the transition the user heard broken)
  L16     "I feel AC temperatures rearranging" (takes 1-5, 11-15: the user's wording) / "I feel my AC ..." (6-10, 16-20)
  L19-20  "... Nokia to the moon" (NVDA -> Nokia; the chunk must be >= 3 s, so L19 is re-sung but not used)
  L24     "Forward SAP, backward, repeat"
  L25     "Now private chats get obsolete"
  L40     "EU Inc fixes things soon", "soon" held like the original "askew"
Low conditioning on the same original range. usage: eu14_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

GEN = [(26320, 29910, ["[Chorus 1]\nTrapped in the Brussels room,\nwhere the faxes zoom"] * 2),
       (49560, 52830, ["[Verse 2]\nI feel Ay-See temperatures rearranging", "[Verse 2]\nI feel my Ay-See temperatures rearranging"]),
       (60580, 64100, ["[Chorus 2]\nI hear the basic income gloom\nNo-ki-a to the moon", "[Chorus 2]\nI hear the basic income gloom\nNOKIA to the moon"]),
       (74060, 77720, ["[Chorus 2]\nForward Ess-Ay-Pee, backward, repeat"] * 2),
       (77720, 81210, ["[Verse 3]\nNow private chats get obsolete"] * 2),
       (120760, 124520, ["[Bridge]\nE. U. Inc. fixes things, soooon", "[Bridge]\nEe-You Inc fixes things... soooon"])]


def plan(k):
    chunks, t = [], 0
    for a, b, texts in GEN:
        pos, neg = styles(a)
        if a > t:
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": texts[(k - 1) // 5 % 2], "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu14_{k}"
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
            print(r)
