"""Convert headshot.png to portrait.txt ASCII art for the profile SVG."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SRC = Path(__file__).parent / "headshot.png"
OUT = Path(__file__).parent / "portrait.txt"

# Scaled down in SVG via scale(~0.40, ~0.82), so generate denser art
COLS = 108
TARGET_ROWS = 60
CHARS = " .:-=+*#%@"
BLACK_THRESHOLD = 28


def main() -> None:
    img = Image.open(SRC).convert("RGBA")
    bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
    composed = Image.alpha_composite(bg, img).convert("L")

    w, h = composed.size
    left = int(w * 0.22)
    right = int(w * 0.78)
    top = int(h * 0.0)
    bottom = int(h * 0.80)
    composed = composed.crop((left, top, right, bottom))

    composed = ImageOps.autocontrast(composed, cutoff=3)
    composed = ImageEnhance.Contrast(composed).enhance(1.5)
    composed = composed.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=4))

    resized = composed.resize((COLS, TARGET_ROWS), Image.Resampling.LANCZOS)

    pixels = list(resized.getdata())
    lines: list[str] = []
    for y in range(TARGET_ROWS):
        row: list[str] = []
        for x in range(COLS):
            p = pixels[y * COLS + x]
            if p < BLACK_THRESHOLD:
                row.append(" ")
            else:
                idx = int((p / 255) * (len(CHARS) - 1))
                row.append(CHARS[idx])
        lines.append("".join(row).rstrip())

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    while lines:
        dense = sum(1 for c in lines[-1] if c not in " .")
        if dense < 8:
            lines.pop()
        else:
            break

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} lines, max width {max(len(l) for l in lines)}")


if __name__ == "__main__":
    main()
