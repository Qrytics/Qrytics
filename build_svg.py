"""Build dark.svg and light.svg for the Qrytics GitHub profile README."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
PORTRAIT = ROOT / "portrait.txt"

# Match Karthik's ASCII placement (scaled in the SVG)
START_X = -10
START_Y = 0
LINE_HEIGHT = 9


def portrait_tspans() -> str:
    lines = [line.rstrip() for line in PORTRAIT.read_text(encoding="utf-8").splitlines()]
    y = START_Y
    parts: list[str] = []
    for line in lines:
        parts.append(f'<tspan x="{START_X}" y="{y}">{escape(line)}</tspan>')
        y += LINE_HEIGHT
    return "\n".join(parts)


def info_panel(panel_fill: str, header_fill: str, section_fill: str, rule_fill: str) -> str:
    # Field layout mirrors Karthik; stats IDs must match update.py
    return f"""<text x="500" y="30" fill="{panel_fill}">
<tspan x="520" y="30" fill="{header_fill}" fontsize="17px">Qrytics@cmu-ece</tspan><tspan fill="{rule_fill}"> -----------------------------------------------</tspan>
<tspan x="520" y="50" class="cc">. </tspan><tspan class="key">Subject</tspan>:<tspan class="cc"> ....................... </tspan><tspan class="value">Mario A. Belmonte</tspan>
<tspan x="520" y="70" class="cc">. </tspan><tspan class="key">Role</tspan>:<tspan class="cc"> ...... </tspan><tspan class="value">ECE Student | Full-Stack Developer</tspan>
<tspan x="520" y="90" class="cc">. </tspan><tspan class="key">Origin</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">Pittsburgh, PA</tspan>
<tspan x="520" y="110" class="cc">. </tspan><tspan class="key">Status</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">Building · Learning · Shipping</tspan>
<tspan x="520" y="130" class="cc">. </tspan><tspan class="key">ToolChain</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">VS Code, Git, Docker, Linux</tspan>
<tspan x="520" y="150" class="cc">. </tspan>
<tspan x="520" y="170" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Core</tspan>:<tspan class="cc"> ..... </tspan><tspan class="value">TypeScript, Python, C/C++, SystemVerilog</tspan>
<tspan x="520" y="190" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Frontend</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">React, Next.js, HTML/CSS, d3</tspan>
<tspan x="520" y="210" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Backend</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">FastAPI, Docker, PostgreSQL, AWS</tspan>
<tspan x="520" y="230" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">Hardware</tspan>:<tspan class="cc"> ........ </tspan><tspan class="value">ESP32, FPGA, Quartus, MQTT</tspan>
<tspan x="520" y="250" class="cc">. </tspan><tspan class="key">Stack</tspan>.<tspan class="key">ML</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">PyTorch, OpenCV, LiteLLM</tspan>
<tspan x="520" y="270" class="cc">. </tspan>
<tspan x="520" y="290" fill="{section_fill}">- Contact</tspan><tspan fill="{rule_fill}"> ---------------------------------------------------------</tspan>
<tspan x="520" y="310" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Mail</tspan>:<tspan class="cc"> ................ </tspan><tspan class="value">mario4.belmonte@gmail.com</tspan>
<tspan x="520" y="330" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Portfolio</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">mario-belmonte.com</tspan>
<tspan x="520" y="350" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ............ </tspan><tspan class="value">mario-belmonte</tspan>
<tspan x="520" y="370" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Github</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">Qrytics</tspan>
<tspan x="520" y="390" class="cc">. </tspan><tspan class="key">Link</tspan>.<tspan class="key">Resume</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">mario-belmonte.com/resume</tspan>
<tspan x="520" y="420" fill="{section_fill}">- GitHub Stats</tspan><tspan fill="{rule_fill}"> ----------------------------------------------------</tspan>
<tspan x="520" y="440" class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan> {{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>   }}  | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............ </tspan><tspan class="value" id="star_data">0</tspan>
<tspan x="520" y="460" class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> .................... </tspan><tspan class="value" id="commit_data">0</tspan>       | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ........ </tspan><tspan class="value" id="follower_data">0</tspan>
<tspan x="520" y="480" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan> ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, <tspan id="loc_del_dots">. </tspan><tspan class="delColor" id="loc_del">0</tspan><tspan class="delColor">--</tspan> )
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

    portrait = portrait_tspans()
    panel = info_panel(panel_fill, header_fill, section_fill, rule_fill)

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1180" height="530" viewBox="0 0 1180 530" fontsize="15px">
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
    <rect width="1180" height="530" rx="15"/>
  </clipPath>
  <clipPath id="portrait">
    <rect x="0" y="0" width="510" height="530"/>
  </clipPath>
</defs>
<rect width="1180px" height="530px" fill="{bg}" rx="15"/>
<g clip-path="url(#card)">
  <g clip-path="url(#portrait)">
    <g transform="translate(18,12) scale(0.40,0.82)">
      <text x="0" y="0" fill="{ascii_fill}" class="ascii">
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


if __name__ == "__main__":
    main()
