"""Regenerate only 'I hear the basilisk boom / NVDA to the moon' (60.58-64.10 s) with ElevenLabs Music inpainting."""
import json, os, pathlib, sys, urllib.request

HERE = pathlib.Path(__file__).parent
up = json.loads((HERE / "upload.json").read_text())
SID = up["song_id"]
chorus = next(c for c in up["composition_plan"]["chunks"] if c["text"].startswith("[Chorus 2]"))
A, B, END = 60580, 64100, 156650


def plan(word, strength):
    gen = {"text": f"[Chorus 2]\nI hear the basilisk boom\n{word} to the moon",
           "duration_ms": B - A,
           "positive_styles": chorus["positive_styles"], "negative_styles": chorus["negative_styles"],
           "context_adherence": "high"}
    if strength:
        gen |= {"conditioning_ref": {"song_id": SID, "range": {"start_ms": 58417, "end_ms": 74779}},
                "condition_strength": strength}
    return {"chunks": [{"song_id": SID, "range": {"start_ms": 0, "end_ms": A}}, gen,
                       {"song_id": SID, "range": {"start_ms": B, "end_ms": END}}]}


for name, word, strength in [(a, b, c) for a, b, c in (x.split(":") for x in sys.argv[1:])]:
    body = {"composition_plan": plan(word, strength or None), "model_id": "music_v2_5"}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps(body).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=600).read())
        print(name, "ok")
    except urllib.error.HTTPError as e:
        print(name, e.code, e.read()[:600].decode())
