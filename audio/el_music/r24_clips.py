"""Round 24 L10 clips: words that keep the original's vowels (with a BAG of SHROOMS). The words land (Whisper: "with the
facts that zoom" / "facts of doom"), the melody is far from the original (in50 23-51). Next letters in eu_v8_lines."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v8_refine import write, V

ZOOMS = (V.ALL_WORDS(10), "WITH A BAG OF SHROOMS", "WITH A FAX THAT ZOOMS", "with a fax that zooms")
DOOM = (V.ALL_WORDS(10), "WITH A BAG OF SHROOMS", "WITH A FAX OF DOOM", "with a fax of doom")
if __name__ == "__main__":
    for take, plan, heard in (("eu24_9", ZOOMS, "With the facts that soon"), ("eu24_1", ZOOMS, "With the facts that zoom"),
                              ("eu24_8", DOOM, "With the facts of doom")):
        write(10, take, plan, "htdemucs_ft", False, None, f"new words, whole line (Whisper: {heard})", plan[3])
