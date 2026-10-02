"""Round 22, after the user's review of the eu_v8_lines clips:
  L24  every take sang "SIP" / "S-O-P"; it must be S-A-P, the company, three letters. Chunk over L23-L24 (the wider
       window that landed Nokia), L23 sung with its v7 words and not used.
  L40  eu20_1 (L40A) was closest, but "EU" must sound like the "EU doom" hooks (eu6, sung "you-doom" / "U-doom").
       Chunk over L39-L40 as round 20.
Spellings change with the take: k % 3 == 1, 2, 0 -> the first, second, third text of each line.
usage: eu22_inpaint.py <first> <last>   writes eu22_<k>.mp3
Round 23 (ROUND=23): L24 only, in its own 3.7 s window (round 14's eu14_10 there was 90 % on the melody, no ghost; the
wider window left the old vocal in). Round 22's letters came out "N-A-P" / "M-A-P": the first letter keeps the
original "em", so the S is stressed. k % 4 picks the spelling.
Round 24 (ROUND=24): the user heard the S as silent; their spellings "AS AE P" / "ES-AE-PEE". Same generations carry L10
with words that keep the original's vowels (with a BAG of SHROOMS: i uh a uh oo): "with a fax that zooms" /
"with a fax of doom" (every "where the faxes zoom" take broke on "-es zoom")."""
import json, os, pathlib, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eu2_inpaint import SID, END, HERE, styles

GEN = [(69760, 77720, ["[Chorus 2]\nThat was fast enough, we reckoned\nForward S-A-P, backward, repeat",
                       "[Chorus 2]\nThat was fast enough, we reckoned\nForward Ess. Ay. Pee. Backward, repeat",
                       "[Chorus 2]\nThat was fast enough, we reckoned\nForward S. A. P., backward, repeat"]),
       (118700, 124520, ["[Bridge]\nHundred thousand GPU\nYou-Inc fixes things, soooon",
                         "[Bridge]\nHundred thousand GPU\nEE-YOU Inc fixes things, soooon",
                         "[Bridge]\nHundred thousand GPU\nU-Inc fixes things, soooon"])]


ROUND = os.environ.get("ROUND", "22")
if ROUND == "23":
    GEN = [(74060, 77720, ["[Chorus 2]\nForward S A P, backward, repeat", "[Chorus 2]\nForward Esss, Ay, Pee, backward, repeat",
                           "[Chorus 2]\nForward, SS-AY-PEE, backward, repeat", "[Chorus 2]\nForward S.A.P., backward, repeat"])]
if ROUND == "24":
    GEN = [(26320, 29910, ["[Chorus 1]\nTrapped in the Brussels room,\nwith a fax that zooms",
                           "[Chorus 1]\nTrapped in the Brussels room,\nwith a fax of doom"]),
           (74060, 77720, ["[Chorus 2]\nForward AS-AE-P, backward, repeat", "[Chorus 2]\nForward AS AY PEE, backward, repeat",
                           "[Chorus 2]\nForward ES-AE-PEE, backward, repeat", "[Chorus 2]\nForward ESS AE P, backward, repeat"])]


def plan(k):
    chunks, t = [], 0
    for a, b, texts in GEN:
        pos, neg = styles(a)
        chunks.append({"song_id": SID, "range": {"start_ms": t, "end_ms": a}})
        chunks.append({"text": texts[(k - 1) % len(texts)], "duration_ms": b - a, "positive_styles": pos, "negative_styles": neg,
                       "context_adherence": "high",
                       "conditioning_ref": {"song_id": SID, "range": {"start_ms": a, "end_ms": b}},
                       "condition_strength": "low"})
        t = b
    for s0 in range(t, END, 120000):
        chunks.append({"song_id": SID, "range": {"start_ms": s0, "end_ms": min(END, s0 + 120000)}})
    return {"chunks": chunks}


def take(k):
    name = f"eu{ROUND}_{k}"
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
