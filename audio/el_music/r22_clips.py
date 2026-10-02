"""Round 22 (eu22_inpaint.py) clips for the user: L24 takes that sang three letters ("N-A-P" / "M-A-P" to Whisper, the
S may be there), as whole lines and with only the letters inserted (the original "Forward" and "backward, repeat");
L40 takes sung with the hooks' "you-doom" EU, whole lines. Written as the next letters in eu_v8_lines (v8_refine.write)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from v8_refine import write, V

P24 = (V.ALL_WORDS(24), "FORWARD EM EL PEE BACKWARD REPEAT", "FORWARD ESS AY PEE BACKWARD REPEAT", "Forward SAP, backward, repeat")
P24_INS = ([1], "EM EL PEE", "ESS AY PEE", "SAP,")
P40 = (V.ALL_WORDS(40), "AR EL AITCH EF GOES ASKEW", "EE YOU INC FIXES THINGS SOON", "EU Inc fixes things soon")
if __name__ == "__main__":
    for take, heard in (("eu22_3", "Forward, N-A-P, backward, repeat"), ("eu22_12", "Fall on an M-A-P, backward, repeat"),
                        ("eu22_7", "4, N, A, B, backward repeat")):
        write(24, take, P24, "htdemucs_ft", False, None, f"whole line (Whisper: {heard})", "Forward SAP, backward, repeat")
        write(24, take, P24_INS, "htdemucs_ft", False, None, f"only the letters (Whisper on the whole: {heard})", "Forward SAP, backward, repeat")
    for take, heard in (("eu22_3", "Only fix those things as soon as I"), ("eu22_4", "It fixes things too"),
                        ("eu22_1", "You ain't fixin' things too"), ("eu22_7", "You will fix your things soon")):
        write(40, take, P40, "htdemucs_ft", False, None, f"whole line, hook EU (Whisper: {heard})", "EU Inc fixes things soon")
