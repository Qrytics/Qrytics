"""Build dark.svg and light.svg for the Qrytics GitHub profile README."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
PORTRAIT = ROOT / "portrait.txt"

START_X = 0
START_Y = 12
# Must be >= ascii fontsize or stacked lines squash the face
LINE_HEIGHT = 13
CHAR_WIDTH = 7.4
PANEL_W = 500
# Empty character rows around the portrait art (bottom looks larger visually, so keep it smaller)
VOID_ROWS_TOP = 2
VOID_ROWS_BOTTOM = 1
# Right-panel text baselines; card bottom pad matches top pad
TEXT_TOP_Y = 30
TEXT_BOTTOM_Y = 470
# Same dark margin below LOC line as above the header (~2 char / 30px)
CARD_HEIGHT = TEXT_BOTTOM_Y + TEXT_TOP_Y  # 500


def _line_density(line: str) -> int:
    """Count solid portrait chars (ignore space / soft fringe)."""
    return sum(1 for c in line if c not in " .:-`'")


def portrait_lines() -> list[str]:
    """Art lines only; strip trailing sparse fringe so bottom void stays tight."""
    lines = [line.rstrip() for line in PORTRAIT.read_text(encoding="utf-8").splitlines()]
    # Bottom fringe is mostly .:-= noise; require real density to keep a row
    while lines and _line_density(lines[-1]) < 18:
        lines.pop()
    while lines and _line_density(lines[0]) < 6:
        lines.pop(0)
    return lines


def padded_portrait_lines(art: list[str]) -> list[str]:
    """Art with void buffers — bottom is intentionally smaller than top."""
    return ([""] * VOID_ROWS_TOP) + art + ([""] * VOID_ROWS_BOTTOM)


def portrait_tspans(lines: list[str]) -> str:
    y = START_Y
    parts: list[str] = []
    for line in lines:
        parts.append(f'<tspan x="{START_X}" y="{y}">{escape(line)}</tspan>')
        y += LINE_HEIGHT
    return "\n".join(parts)


def portrait_transform(art: list[str]) -> str:
    """
    Top void starts near TEXT_TOP_Y; bottom void ends at TEXT_BOTTOM_Y.
    VOID_ROWS_BOTTOM < VOID_ROWS_TOP so the bottom gap matches the top visually.
    """
    lines = padded_portrait_lines(art)
    max_w = max((len(l) for l in lines), default=1)
    raw_w = max(1, max_w) * CHAR_WIDTH

    y_first = START_Y
    last_index = len(lines) - 1
    y_last = START_Y + last_index * LINE_HEIGHT

    span_local = max(1.0, y_last - y_first)
    sy = (TEXT_BOTTOM_Y - TEXT_TOP_Y) / span_local
    sx = sy
    if raw_w * sx > PANEL_W * 1.08:
        sx = (PANEL_W * 1.08) / raw_w
        sy = sx

    ty = TEXT_BOTTOM_Y - y_last * sy
    tx = 12.0
    return f"translate({tx:.1f},{ty:.1f}) scale({sx:.4f},{sy:.4f})"


def info_panel(panel_fill: str, header_fill: str, section_fill: str, rule_fill: str) -> str:
    return f"""<text x="500" y="30" fill="{panel_fill}">
<tspan x="520" y="30" fill="{header_fill}" fontsize="17px">Qrytics@IBM</tspan><tspan fill="{rule_fill}"> ---------------------------------------------------</tspan>
<tspan x="520" y="50" class="cc">. </tspan><tspan class="key">Subject</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">Mario A. Belmonte</tspan>
<tspan x="520" y="70" class="cc">. </tspan><tspan class="key">Role</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">Cloud Consultant @ IBM</tspan>
<tspan x="520" y="90" class="cc">. </tspan><tspan class="key">Origin</tspan>:<tspan class="cc"> ........................... </tspan><tspan class="value">Mcallen, TX</tspan>
<tspan x="520" y="110" class="cc">. </tspan><tspan class="key">Status</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">Building · Learning</tspan>
<tspan x="520" y="130" class="cc">. </tspan><tspan class="key">ToolChain</tspan>:<tspan class="cc"> ................ </tspan><tspan class="value">VS Code, Git, Docker, Linux</tspan>
<tspan x="520" y="150" class="cc">. </tspan>
<tspan x="520" y="170" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Core</tspan>:<tspan class="cc"> ............ </tspan><tspan class="value">TypeScript, Python, C/C++, SystemVerilog</tspan>
<tspan x="520" y="190" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Frontend</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">React, Next.js, HTML/CSS, d3</tspan>
<tspan x="520" y="210" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Backend</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">FastAPI, Docker, PostgreSQL, AWS</tspan>
<tspan x="520" y="230" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Hardware</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">ESP32, FPGA, Quartus, MQTT</tspan>
<tspan x="520" y="250" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">ML</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">PyTorch, OpenCV, LiteLLM</tspan>
<tspan x="520" y="290" fill="{section_fill}">- Contact</tspan><tspan fill="{rule_fill}"> ---------------------------------------------------------</tspan>
<tspan x="520" y="310" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Mail</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">mario4.belmonte@gmail.com</tspan>
<tspan x="520" y="330" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Portfolio</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">mario-belmonte.com</tspan>
<tspan x="520" y="350" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">linkedin.com/in/mario-belmonte/</tspan>
<tspan x="520" y="370" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Resume</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">mario-belmonte.com/resume</tspan>
<tspan x="520" y="410" fill="{section_fill}">- GitHub Stats</tspan><tspan fill="{rule_fill}"> ----------------------------------------------------</tspan>
<tspan x="520" y="430" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>   }}  | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............ </tspan><tspan class="value" id="star_data">0</tspan>
<tspan x="520" y="450" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> .................... </tspan><tspan class="value" id="commit_data">0</tspan>       | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ........ </tspan><tspan class="value" id="follower_data">0</tspan>
<tspan x="520" y="470" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan> ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots">. </tspan><tspan class="delColor" id="loc_del">0</tspan><tspan class="delColor">--</tspan> )
</text>"""


def build_svg(*, dark: bool) -> str:
    if dark:
        key = "#5EEAD4"
        value = "#E5E7EB"
        cc = "#5f6b7a"
        bg = "black"
        ascii_fill = "#7DF9FF"
        header_fill = "#7DF9FF"
        section_fill = "#FF5F87"
        panel_fill = "#dbeafe"
        rule_fill = "#5f6b7a"
    else:
        key = "#0550ae"
        value = "#24292f"
        cc = "#8c959f"
        bg = "#f6f8fa"
        ascii_fill = "#000000"
        header_fill = "#0969da"
        section_fill = "#CF222E"
        panel_fill = "#24292f"
        rule_fill = "#8c959f"

    art = portrait_lines()
    lines = padded_portrait_lines(art)
    portrait = portrait_tspans(lines)
    transform = portrait_transform(art)
    panel = info_panel(panel_fill, header_fill, section_fill, rule_fill)

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1180" height="{CARD_HEIGHT}" viewBox="0 0 1180 {CARD_HEIGHT}" fontsize="15px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key      {{ fill: {key}; }}
.value    {{ fill: {value}; }}
.cc       {{ fill: {cc}; }}
.addColor {{ fill: #39ff14; }}
.delColor {{ fill: #ef4444; }}
text, tspan {{ white-space: pre; }}
</style>
<defs>
  <clipPath id="card">
    <rect width="1180" height="{CARD_HEIGHT}" rx="15"/>
  </clipPath>
  <clipPath id="portrait">
    <rect x="0" y="0" width="510" height="{CARD_HEIGHT}"/>
  </clipPath>
</defs>
<rect width="1180px" height="{CARD_HEIGHT}px" fill="{bg}" rx="15"/>
<g clip-path="url(#card)">
  <g clip-path="url(#portrait)">
    <g transform="{transform}">
      <text x="0" y="0" fill="{ascii_fill}" class="ascii" fontsize="12px">
{portrait}
      </text>
    </g>
  </g>
{panel}
</g>
</svg>
"""


def main() -> None:
    if not PORTRAIT.exists():
        raise SystemExit("portrait.txt missing — run generate_portrait.py first")

    dark = build_svg(dark=True)
    light = build_svg(dark=False)
    (ROOT / "dark.svg").write_text(dark, encoding="utf-8")
    (ROOT / "light.svg").write_text(light, encoding="utf-8")
    print("Wrote dark.svg and light.svg")
    art = portrait_lines()
    print("portrait transform:", portrait_transform(art))
    print(f"void buffers: {VOID_ROWS_TOP} top + {VOID_ROWS_BOTTOM} bottom")
    print(f"block spans text y={TEXT_TOP_Y}..{TEXT_BOTTOM_Y}")
    print(f"card {CARD_HEIGHT}px (top/bottom edge pad={TEXT_TOP_Y}px)")
    print(f"art lines after fringe trim: {len(art)}")


if __name__ == "__main__":
    main()
