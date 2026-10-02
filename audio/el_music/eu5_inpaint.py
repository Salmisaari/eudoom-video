"""EU lyrics, round 5: L34 "Euro open borders blues" (with attitude) and L37 "Post AI bubble trends",
each conditioned (low) on the original audio of the same range. usage: eu5_inpaint.py <first> <last>"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

GEN = [(105960, 110180, "[Chorus 3]\nEuro open borders blues", ["sassy", "attitude", "punchy vocals"]),
       (115200, 118755, "[Bridge]\nPost Ay-Eye bubble trends\nBreaking through each safety fence", [])]


def plan():
    chunks, t = [], 0
    for a, b, text, extra in GEN:
        pos, neg = styles(a)
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": text, "duration_ms": b - a, "positive_styles": pos + extra, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": END}})
    return {"chunks": chunks}


def take(k):
    name = f"eu5_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(), "model_id": "music_v2_5"}).encode(),
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
