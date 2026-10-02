"""L9-L10 as one span from one take. In the original "room" runs straight into "with" (no gap), so a seam between L9
(v5: eu2_low4) and L10 (eu2_low3, which starts "where" ~0.1 s before the line) lands inside two voices at once: the
flicker the user hears ~1 s into every L10 clip. One take for both lines keeps the transition the singer's own; the
seams move to the start of L9 (where v5's approved L9 already had one) and the end of L10. The user found L10D
(eu2_low3 mid-tuned) best but its intonation off: tuned variants here, and one with the timing warped first so the
tune follows the original note by note. Clips "L9-10<letter> - ..." in eu_v8_lines."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v8_refine import write, V, TUNE

L9, L10 = V.LYR[8], V.LYR[9]
V.LYR.append(dict(start=L9["start"], end=L10["end"], words=L9["words"] + L10["words"]))
N = len(V.LYR)
PLAN = (V.ALL_WORDS(N), "TRAPPED IN THE CHINESE ROOM WITH A BAG OF SHROOMS", "TRAPPED IN THE BRUSSELS ROOM WHERE THE FAXES ZOOM",
        "Trapped in the Brussels room, where the faxes zoom")
if __name__ == "__main__":
    for take, warp, tune, desc in (("eu2_low3", False, None, "L10's take (L10A/D) for both lines, untouched"),
                                   ("eu2_low3", False, TUNE, "L10D's take for both lines, mid-tuned"),
                                   ("eu2_low3", True, TUNE, "L10D's take for both lines, timing then tune to the original"),
                                   ("eu2_low4", False, None, "L9's take (approved in v5) for both lines, untouched"),
                                   ("eu2_low4", False, TUNE, "L9's take for both lines, mid-tuned")):
        write(N, take, PLAN, "htdemucs_ft", warp, tune, desc, "Trapped in the Brussels room, where the faxes zoom", label="L9-10")
