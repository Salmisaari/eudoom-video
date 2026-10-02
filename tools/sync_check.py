"""Proof sheet (add "first" to sample the first words of lines) that the words land on their sung frame: for sampled words, the rendered video's frame before the
onset and the onset frame itself, side by side (the word should be absent, then present).
  analysis/.venv/bin/python tools/sync_check.py out/typo_v1.mp4 out/sync_typo_v1.jpg [n_words]"""
import json, random, subprocess, sys, pathlib, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
T = json.loads((ROOT / "data/timing_eu.json").read_text())
FPS = 60


def frame(video, n, out):
    # accurate seek keeps the first frame at or after -ss: a quarter frame early lands on frame n
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(n - 0.25) / FPS:.4f}", "-i", str(video), "-frames:v", "1",
                    "-vf", "scale=640:-1", str(out)], check=True)


def main(video, out, k=12, first=False):
    words = [(L["n"], w) for L in T["lines"] for w in L["words"]]
    if first:  # the first word of each line: the page arrives before it
        words = [(L["n"], L["words"][0]) for L in T["lines"]]
    random.seed(7)
    pick = sorted(random.sample(words, k), key=lambda x: x[1]["start"])
    font = ImageFont.truetype(str(ROOT / "app/public/fonts/CourierPrime-Bold.ttf"), 22)
    sheet = Image.new("RGB", (2 * 650 + 10, k * 400 + 10), (243, 238, 227))
    d = ImageDraw.Draw(sheet)
    with tempfile.TemporaryDirectory() as tmp:
        for i, (ln, w) in enumerate(pick):
            n1 = max(1, int(-(-((w["start"] - 1 / 120) * FPS) // 1)))  # first frame within half a frame of the onset
            for j, n in enumerate((n1 - 1, n1)):
                f = pathlib.Path(tmp) / f"{i}_{j}.png"
                frame(video, n, f)
                sheet.paste(Image.open(f).convert("RGB"), (10 + j * 650, 10 + i * 400 + 34))
                d.text((10 + j * 650, 10 + i * 400 + 4), f"L{ln} “{w['w']}” sung at {w['start']:.3f}s · frame {n} ({n / FPS:.3f}s)", fill=(29, 27, 32), font=font)
    sheet.save(out, quality=88)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12, 'first' in sys.argv[4:])
