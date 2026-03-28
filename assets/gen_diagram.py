#!/usr/bin/env python3
"""Generate architecture diagram as clean SVG (stdlib only, no matplotlib)."""

W, H, mid_y = 1300, 555, 267
DIR_COLORS = ["#4C72B0", "#CC6677", "#44AA99"]
DIR_TITLES = [
    ("e.g.  Does accuracy become", "misleading under imbalance?"),
    ("e.g.  Which metrics reliably", "track model quality?"),
    ("e.g.  Can threshold tuning", "recover performance?"),
]
DIR_EXPS = [
    "3 experiments  \u00b7  score 8/10",
    "5 experiments  \u00b7  score 8/10",
    "4 experiments  \u00b7  score 8/10",
]

# workers: h=150, gap=22 → tops=[20,192,364], centers=[95,267,439]
WX, WW, WH = 535, 450, 150
w_tops    = [20, 20 + WH + 22, 20 + 2 * (WH + 22)]   # [20, 192, 364]
w_centers = [t + WH // 2 for t in w_tops]              # [95, 267, 439]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rect(x, y, w, h, fill, stroke, sw=1.6, rx=12, opacity=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')

def arr(x1, y1, x2, y2, col="#aaaaaa"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{col}" stroke-width="2.2" marker-end="url(#arr)"/>')

def txt(x, y, s, size=13, fill="#333333", bold=False, italic=False, anchor="middle"):
    fw = "bold" if bold else "normal"
    fs = "italic" if italic else "normal"
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" dominant-baseline="central" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
            f'font-weight="{fw}" font-style="{fs}" fill="{fill}">{esc(s)}</text>')

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">',
    '<defs>',
    '  <marker id="arr" markerWidth="14" markerHeight="10" refX="13" refY="5"'
    ' orient="auto" markerUnits="userSpaceOnUse">',
    '    <path d="M0,1 L13,5 L0,9 Z" fill="#aaaaaa"/>',
    '  </marker>',
    '</defs>',
    f'<rect width="{W}" height="{H}" fill="white"/>',
]

# ── "you" box ────────────────────────────────────────────────────────────────
out += [
    rect(20, mid_y - 60, 162, 120, "#f7f7f7", "#cccccc", sw=2.2),
    txt(101, mid_y - 22, "you", size=24, fill="#444444", bold=True),
    txt(101, mid_y + 8,  '\u201cRead program.md', size=16, fill="#888888", italic=True),
    txt(101, mid_y + 28, 'and begin\u201d',        size=16, fill="#888888", italic=True),
]

# ── arrow you → program.md ───────────────────────────────────────────────────
out.append(arr(182, mid_y, 252, mid_y))

# ── program.md box ───────────────────────────────────────────────────────────
out += [
    rect(252, mid_y - 95, 216, 190, "#f7f7f7", "#aaaaaa", sw=2.2),
    txt(360, mid_y - 50, "program.md",        size=22, fill="#333333", bold=True),
    txt(360, mid_y - 24, "orchestrator",       size=17, fill="#999999", italic=True),
    txt(360, mid_y +  4, "spawns one worker",  size=16, fill="#aaaaaa"),
    txt(360, mid_y + 24, "per direction",      size=16, fill="#aaaaaa"),
]

# ── arrows program.md → workers ──────────────────────────────────────────────
for cy in w_centers:
    out.append(arr(468, mid_y, WX, cy))

# ── worker boxes ─────────────────────────────────────────────────────────────
for t, cy, col, (line1, line2), exp in zip(w_tops, w_centers, DIR_COLORS, DIR_TITLES, DIR_EXPS):
    wx = WX + WW // 2
    out += [
        rect(WX, t, WW, WH, col, col, sw=0, opacity=0.10),
        rect(WX, t, WW, WH, "none", col, sw=2.5),
        txt(wx, cy - 24, line1, size=18, fill=col, bold=True),
        txt(wx, cy -  2, line2, size=18, fill=col, bold=True),
        txt(wx, cy + 28, exp,   size=16, fill="#777777"),
    ]

# ── arrows workers → findings.md ─────────────────────────────────────────────
FX = 1058
for cy in w_centers:
    out.append(arr(WX + WW, cy, FX, mid_y))

# ── findings.md box ──────────────────────────────────────────────────────────
fcx = FX + 118
out += [
    rect(FX, mid_y - 95, 236, 190, "#f7f7f7", "#aaaaaa", sw=2.2),
    txt(fcx, mid_y - 50, "findings.md",            size=22, fill="#333333", bold=True),
    txt(fcx, mid_y - 20, "quantified results",     size=16, fill="#999999"),
    txt(fcx, mid_y +  2, "counterarguments",       size=16, fill="#999999"),
    txt(fcx, mid_y + 24, "prioritised follow-ups", size=16, fill="#999999"),
]

out.append('</svg>')

svg = "\n".join(out)
with open("assets/diagram.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"saved assets/diagram.svg  ({len(svg):,} bytes)")
