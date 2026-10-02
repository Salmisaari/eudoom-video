"""EU lyrics, round 2: every regenerated stretch is conditioned on the original audio of that same stretch
(so the model hears the melody, phrasing and voice it must keep) and uses the uploaded song's own
section styles. Replacement words keep the original syllable count and stress.
usage: eu2_inpaint.py <strength> <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent
up = json.loads((HERE / "upload.json").read_text())
SID, END = up["song_id"], 156650

# section styles from the upload's extracted plan, by start time
sections, t = [], 0
for c in up["composition_plan"]["chunks"]:
    sections.append((t, c))
    t += c["duration_ms"]


def styles(ms):
    c = [c for s, c in sections if s <= ms][-1]
    return c["positive_styles"], c["negative_styles"]


GEN = [
    (22760, 29910, "[Chorus 1]\nI'm upping Ee-You doom\n'Cause the future goes foom\nTrapped in the Brussels room\nWhere the faxes zoom"),
    (59130, 64100, "[Chorus 2]\nI'm upping Ee-You doom\nI hear the basic income boom\nAy-Ess-Em-Ell to the moon"),
    (66220, 69760, "[Chorus 2]\nOne E thirty forms a second"),
    (85000, 100720, "[Chorus 2]\nWithout a single Gee-Dee-Pee-Arr\n[Chorus 3]\nNATO, please don't let me go\n"
                    "I'm upping Ee-You doom\nAs paperclips fill the room\nEe-You guy's on Pee-Tee-Oh"),
    (105960, 110180, "[Chorus 3]\nEuro-banality thesis blues"),
    (120760, 126120, "[Bridge]\nThe Ay-Eye Act goes askew\n[Outro]\nI'm upping Ee-You doom"),
    (132020, 137380, "[Outro]\nWhat did Draghi see? We'll never know"),
]


def plan(strength):
    chunks, t = [], 0
    for a, b, text in GEN:
        pos, neg = styles(a)
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text, "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": strength})
        t = b
    chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": END}})
    return {"chunks": chunks}


def take(args):
    strength, k = args
    name = f"eu2_{strength}{k}"
    body = {"composition_plan": plan(strength), "model_id": "music_v2_5"}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps(body).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:400].decode()}"


if __name__ == "__main__":
    s, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(take, [(s, k) for k in range(a, b + 1)]):
            print(r)
