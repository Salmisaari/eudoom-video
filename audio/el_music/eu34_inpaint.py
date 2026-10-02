"""Round 34 (2026-10-01): "EU" sung ee-YOO, with the /j/ glide into the U (the user: "same with EU that's EJU or E-yu").
Measured in v13 (glide.py): L18 and L41 have it; L7 holds "ee" straight into "doom" (no U), L29 has no "ee" (sung
"you doom"), L40 sings an open "eh-oo" into "Inc". One chunk per line (>= 3 s: the hooks run on into the next line),
conditioned low on the original's own stretch, spellings forcing the glide, k % 4. Only "EU doom" (the hooks) or
"EU" (L40) is spliced; "I'm upping my" stays the original singer's, as built since v5.
usage: eu34_inpaint.py <line> <first> <last>  -> eu34_L<line>_<k>.mp3"""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

SPELL = ["ee-YOO", "E-yu", "Ee-you", "E.U. (ee-yoo)"]
LINES = {7: (22760, 26320, "[Chorus 1]\nI'm upping my {eu} doom\n'Cause the future goes FOOM"),
         29: (95470, 98820, "[Chorus 3]\nI'm upping my {eu} doom,\nAs paperclips fill the room"),
         40: (120760, 124520, "[Bridge]\n{eu} Inc fixes things soon")}


def plan(n, k):
    A, B, text = LINES[n]
    pos, neg = styles(A)
    chunks = [{"song_id": SID, "range": {"start_ms": s0, "end_ms": min(A, s0 + 120000)}} for s0 in range(0, A, 120000)]  # refs <= 120 s
    chunks += [{"text": text.format(eu=SPELL[(k - 1) % len(SPELL)]), "duration_ms": B - A, "positive_styles": pos,
               "negative_styles": neg, "context_adherence": "high",
               "conditioning_ref": {"song_id": SID, "range": {"start_ms": A, "end_ms": B}}, "condition_strength": "low"}]
    for s0 in range(B, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(args):
    n, k = args
    name = f"eu34_L{n}_{k}"
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
                                 data=json.dumps({"composition_plan": plan(n, k), "model_id": "music_v2_5"}).encode(),
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        (HERE / f"{name}.mp3").write_bytes(urllib.request.urlopen(req, timeout=900).read())
        return f"{name} ok"
    except urllib.error.HTTPError as e:
        return f"{name} {e.code} {e.read()[:300].decode()}"


if __name__ == "__main__":
    n = int(sys.argv[1])
    with ThreadPoolExecutor(5) as ex:
        for r in ex.map(take, [(n, k) for k in range(int(sys.argv[2]), int(sys.argv[3]) + 1)]):
            print(r, flush=True)
