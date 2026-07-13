"""Convert portrait.txt into SVG <tspan> lines for embedding in dark/light.svg."""

from html import escape
from pathlib import Path

INPUT = Path(__file__).parent / "portrait.txt"
OUTPUT = Path(__file__).parent / "portrait_tspan.txt"

START_X = -10
START_Y = 6
LINE_HEIGHT = 9
TRIM_LEFT = 0
TRIM_RIGHT = 0
REMOVE_EMPTY = False


def main() -> None:
    lines = INPUT.read_text(encoding="utf-8", errors="ignore").splitlines()
    lines = [line.rstrip() for line in lines]

    if REMOVE_EMPTY:
        lines = [line for line in lines if line.strip()]

    processed: list[str] = []
    for line in lines:
        if TRIM_RIGHT > 0:
            line = line[:-TRIM_RIGHT]
        if TRIM_LEFT > 0:
            line = line[TRIM_LEFT:]
        processed.append(line)

    y = START_Y
    svg: list[str] = []
    for line in processed:
        svg.append(f'<tspan x="{START_X}" y="{y}">{escape(line)}</tspan>')
        y += LINE_HEIGHT

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"Generated {len(svg)} tspans -> {OUTPUT.name}")


if __name__ == "__main__":
    main()
