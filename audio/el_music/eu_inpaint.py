"""Sing the animatic's EU_LYRICS into the song: one ElevenLabs Music plan that regenerates every changed
stretch (>= 3 s each) and references the original audio everywhere else. usage: eu_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent
up = json.loads((HERE / "upload.json").read_text())
SID, END = up["song_id"], 156650
POS, NEG = ["energetic", "synthpop", "female vocals", "danceable"], ["slow", "acoustic"]

# (start_ms, end_ms, text): line starts from data/lyrics.json; letter-words spelled for singing
GEN = [
    (22760, 29910, "[Chorus]\nI'm upping Ee-You doom\n'Cause the future goes foom\nTrapped in the notary's room\nWhere the faxes zoom"),
    (59130, 64100, "[Chorus]\nI'm upping Ee-You doom\nI hear the basic income boom\nNokia to the moon"),
    (66220, 69760, "[Chorus]\nOne to thirty faxes a second"),
    (85000, 100720, "[Verse 3]\nWithout a single Gee-Dee-Pee-Arr\n[Pre-Chorus]\nNATO, please don't let me go\n"
                    "[Chorus]\nI'm upping Ee-You doom\nAs paperclips fill the room\nEe-You switch: all on Pee-Tee-Oh"),
    (105960, 110180, "[Chorus]\nEuro originality thesis blues"),
    (120760, 126120, "[Bridge]\nAy-Ess-Em-Ell sales through the roof\n[Final Chorus]\nI'm upping Ee-You doom"),
    (132020, 137380, "[Final Chorus]\nWhat did Draghi see? We'll never know"),
]


def plan():
    chunks, t = [], 0
    for a, b, text in GEN:
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text, "duration_ms": b - a, "positive_styles": POS, "negative_styles": NEG,
                       "context_adherence": "high"})
        t = b
    chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": END}})
    return {"chunks": chunks}


def take(k):
    body = {"composition_plan": plan(), "model_id": "music_v2_5"}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps(body).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"eu_take{k}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"eu_take{k} ok"
    except urllib.error.HTTPError as e:
        return f"eu_take{k} {e.code} {e.read()[:400].decode()}"


if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(take, range(int(sys.argv[1]), int(sys.argv[2]) + 1)):
            print(r)
