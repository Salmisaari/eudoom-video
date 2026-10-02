"""L25 "Now privacy in chats obsolete" was chopped in v8 (v7's eu12_3 insert: four hisses of 80-200 ms break the
original's legato "von Neumann's", and two joins sit inside continuous singing). l25_scan.py: eu12_8 (spelled
"pri-va-cy in chats ob-so-lete") is the most legato take (97 % of the original's voiced frames, longest gap 30 ms,
78 % on the melody; eu12_3: 69 %, 200 ms, 62 %), then eu12_10. v7's review had dropped eu12_8 for "ghost" measured on
the Demucs split. Clips on the RoFormer split, centre/sides levelled (round 6), next letters in eu_v8_lines."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rof_clips  # RoFormer split of the original as V.VO
from rof_clips import ms
from v8_refine import write, V
from select10 import PLANS

P25 = (V.ALL_WORDS(25), "NOW VON NEUMANN'S OBSOLETE", "NOW PRIVACY IN CHATS OBSOLETE", "Now privacy in chats obsolete")
P25_INS = PLANS[25][0][1]
CLIPS = {"I": ("eu12_8", P25, "eu12_8 whole line (the most legato take)"),
         "J": ("eu12_10", P25, "eu12_10 whole line"),
         "K": ("eu12_8", P25_INS, "eu12_8 'privacy in chats' inserted, the original's 'Now' and 'obsolete'")}
if __name__ == "__main__":
    for letter, (take, plan, desc) in CLIPS.items():
        if len(sys.argv) == 1 or letter in sys.argv[1:]:
            write(25, take, plan, "bsroformer", False, ms(None, 25), desc + ", RoFormer split, levelled",
                  "Now privacy in chats obsolete", letter=letter)
