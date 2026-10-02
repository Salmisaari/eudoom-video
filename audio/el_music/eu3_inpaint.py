"""EU lyrics, round 3: regenerate only the lines the user sent back, each as its own short chunk (>= 3 s,
padded with the following line) conditioned (low) on the original audio of that range.
usage: eu3_inpaint.py <variant A|B> <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

HOOK = {"A": "I'm upping my EU doom", "B": "I'm upping my U-doom"}
TEXT = {
    "A": [(22760, 26320, "[Chorus 1]\n{hook}\n'Cause the future goes foom"),
          (59130, 62540, "[Chorus 2]\n{hook}\nI hear the bazooka boom"),
          (66220, 69760, "[Chorus 2]\nOne E thirty forms a second"),
          (95470, 98820, "[Chorus 3]\n{hook}\nAs paperclips fill the room"),
          (98820, 102460, "[Chorus 3]\nBrussels guy's on PTO\nNow there's nowhere left to go"),
          (124520, 127920, "[Outro]\n{hook}\nJust as foretold by Loom"),
          (132020, 137380, "[Outro]\nWhat did Drah-ghee see? We'll never know")],
    "B": [(22760, 26320, "[Chorus 1]\n{hook}\n'Cause the future goes foom"),
          (59130, 62540, "[Chorus 2]\n{hook}\nI hear the basic income boom"),
          (66220, 69760, "[Chorus 2]\nOne E thirty forms a second"),
          (95470, 98820, "[Chorus 3]\n{hook}\nAs paperclips fill the room"),
          (98820, 102460, "[Chorus 3]\nWhole EU's on PTO\nNow there's nowhere left to go"),
          (124520, 127920, "[Outro]\n{hook}\nJust as foretold by Loom"),
          (132020, 137380, "[Outro]\nWhat did Draghi see? We'll never know")],
}


def plan(v):
    chunks, t = [], 0
    for a, b, text in TEXT[v]:
        pos, neg = styles(a)
        if a > t:
            chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text.format(hook=HOOK[v]), "duration_ms": b - a, "positive_styles": pos,
                       "negative_styles": neg, "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": END}})
    return {"chunks": chunks}


def take(args):
    v, k = args
    name = f"eu3_{v}{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(v), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    v, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(take, [(v, k) for k in range(a, b + 1)]):
            print(r)
