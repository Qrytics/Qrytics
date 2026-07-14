"""Convert headshot.png to portrait.txt ASCII art for the profile SVG."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SRC = Path(__file__).parent / "headshot.png"
OUT = Path(__file__).parent / "portrait.txt"

COLS = 80
# Tuned for LINE_HEIGHT≈13 + fontsize 12 in the SVG
CHAR_ASPECT = 0.72
CHARS = " .:-=+*#%@"
BLACK_THRESHOLD = 5
LEFT_PAD = 3
BBOX_BG = 16
BBOX_PAD_L = 28
BBOX_PAD_R = 8
BBOX_PAD_Y = 2


def subject_bbox(img: Image.Image) -> tuple[int, int, int, int]:
    """Tight crop around non-black subject to remove empty margins."""
    w, h = img.size
    px = img.load()
    min_x, min_y = w, h
    max_x, max_y = 0, 0
    found = False
    for y in range(h):
        for x in range(w):
            if px[x, y] > BBOX_BG:
                found = True
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    if not found:
        return 0, 0, w, h
    min_x = max(0, min_x - BBOX_PAD_L)
    min_y = max(0, min_y - BBOX_PAD_Y)
    TRIM_RIGHT = 0  # pixels to cut from the right of the subject
    max_x = min(w, max_x - TRIM_RIGHT + 1)
    max_y = min(h, max_y + BBOX_PAD_Y + 1)
    return min_x, min_y, max_x, max_y


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
    composed = Image.alpha_composite(bg, img).convert("L")

    box = subject_bbox(composed)
    composed = composed.crop(box)
    print(f"subject bbox crop: {box} -> {composed.size}")

    composed = ImageOps.autocontrast(composed, cutoff=1)
    composed = ImageEnhance.Contrast(composed).enhance(1.25)

    cw, ch = composed.size
    rows = max(60, int(COLS * (ch / cw) * CHAR_ASPECT))
    resized = composed.resize((COLS, rows), Image.Resampling.LANCZOS)

    pixels = list(resized.getdata())
    lines: list[str] = []
    pad = " " * LEFT_PAD
    for y in range(rows):
        row: list[str] = []
        for x in range(COLS):
            p = pixels[y * COLS + x]
            if p < BLACK_THRESHOLD:
                row.append(" ")
            else:
                idx = min(len(CHARS) - 1, int((p / 255) * (len(CHARS) - 1)))
                row.append(CHARS[idx])
        lines.append((pad + "".join(row)).rstrip())

    def density(line: str) -> int:
        return sum(1 for c in line if c not in " .")

    while lines and density(lines[0]) < 10:
        lines.pop(0)
    while lines and density(lines[-1]) < 8:
        lines.pop()

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} lines, max width {max(len(l) for l in lines)}")


if __name__ == "__main__":
    main()
