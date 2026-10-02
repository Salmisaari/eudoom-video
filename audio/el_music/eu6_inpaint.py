"""EU lyrics, round 6 (review of animatic_v4): new words for L16, L19, L24, L25, L26, L34, L37, L40 and softer-E hooks,
each chunk conditioned (low) on the original audio of the same range. Takes 1-5 sing the hooks "my you-doom",
6-10 "my U-doom". usage: eu6_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

ATTITUDE = ["sassy", "attitude", "punchy vocals"]
GEN = [(22760, 26320, "[Chorus 1]\n{hook}\n'Cause the future goes foom", []),
       (49560, 52830, "[Verse 2]\nI feel my Ay-See max rearranging", []),
       (59130, 62540, "[Chorus 2]\n{hook}\nI hear the basic income gloom", []),
       (74060, 77720, "[Chorus 2]\nForward Gee-Dee-Pee, backward, repeat", []),
       (77720, 85000, "[Verse 3]\nNow private chats obsolete\nSharp left overseas and there you are", []),
       (95470, 98820, "[Chorus 3]\n{hook}\nAs paperclips fill the room", []),
       (105960, 110180, "[Chorus 3]\nEurope open borders blues", ATTITUDE),
       (115200, 118755, "[Bridge]\nBuild post Ay-Eye trends\nBreaking through each safety fence", []),
       (120760, 127920, "[Bridge]\nEe-You Inc fixes Ee-You soon\n[Outro]\n{hook}\nJust as foretold by Loom", [])]


def plan(hook):
    chunks, t = [], 0
    for a, b, text, extra in GEN:
        pos, neg = styles(a)
        if a > t:  # back-to-back chunks need no reference between them
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text.format(hook=hook), "duration_ms": b - a, "positive_styles": pos + extra,
                       "negative_styles": neg, "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": END}})
    return {"chunks": chunks}


def take(k):
    name = f"eu6_{k}"
    hook = "I'm upping my you-doom" if k <= 5 else "I'm upping my U-doom"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(hook), "model_id": "music_v2_5"}).encode(),
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
