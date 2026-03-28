#!/usr/bin/env python3
"""Generate papers pipeline diagram as clean SVG (stdlib only, no matplotlib)."""

W, H = 1300, 480
WORKER_COLOR = "#9B6B9B"
TIER_COLORS  = ["#E07B39", "#5B8DB8", "#44AA99"]
TIER_LABELS  = ["index.md", "overview/", "condensed/"]
TIER_DESCS   = [
    ("one-liner per paper", "loaded at worker startup"),
    ("15-line structured summary", "loaded on demand"),
    ("10-20% of original paper", "loaded when directly relevant"),
]

# 3 workers: h=130, gap=22 → tops=[15,167,319], centers=[80,232,384]
WX, WW, WH = 520, 245, 130
w_tops    = [15, 15 + WH + 22, 15 + 2 * (WH + 22)]   # [15, 167, 319]
w_centers = [t + WH // 2 for t in w_tops]              # [80, 232, 384]
mid_y     = w_centers[1]                               # 232

# 3 output boxes: same vertical positions as workers
OX, OW, OH = 840, 360, 130
o_tops    = w_tops
o_centers = w_centers

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rect(x, y, w, h, fill, stroke, sw=2.0, rx=12, opacity=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
            f'fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')

def arr(x1, y1, x2, y2, col="#aaaaaa", sw=2.2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{col}" stroke-width="{sw}" marker-end="url(#arr)"/>')

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

# ── papers/raw/ box ───────────────────────────────────────────────────────────
RAW_CX = 105
out += [
    rect(20, mid_y - 105, 175, 210, "#f7f7f7", "#cccccc"),
    txt(RAW_CX, mid_y - 62, "papers/raw/",       size=21, fill="#444444", bold=True),
    txt(RAW_CX, mid_y - 32, "e.g.  paper_a.pdf", size=14, fill="#999999", italic=True),
    txt(RAW_CX, mid_y - 10, "e.g.  paper_b.pdf", size=14, fill="#999999", italic=True),
    txt(RAW_CX, mid_y + 20, '\u201cRead ingest.md', size=14, fill="#aaaaaa", italic=True),
    txt(RAW_CX, mid_y + 42, 'and begin\u201d',      size=14, fill="#aaaaaa", italic=True),
]

# ── arrow raw → ingest.md ─────────────────────────────────────────────────────
out.append(arr(195, mid_y, 265, mid_y))

# ── ingest.md box ─────────────────────────────────────────────────────────────
PROG_CX = 375
out += [
    rect(265, mid_y - 105, 215, 210, "#f7f7f7", "#aaaaaa"),
    txt(PROG_CX, mid_y - 50, "ingest.md",          size=21, fill="#333333", bold=True),
    txt(PROG_CX, mid_y - 22, "orchestrator",        size=17, fill="#999999", italic=True),
    txt(PROG_CX, mid_y +  8, "one worker per PDF",  size=16, fill="#aaaaaa"),
]

# ── arrows ingest.md → workers ────────────────────────────────────────────────
for cy in w_centers:
    out.append(arr(480, mid_y, WX, cy))

PAPER_NAMES = ["paper_a.pdf", "paper_b.pdf", "paper_c.pdf"]

# ── per-paper worker boxes ────────────────────────────────────────────────────
for t, cy, paper in zip(w_tops, w_centers, PAPER_NAMES):
    wx = WX + WW // 2
    out += [
        rect(WX, t, WW, WH, WORKER_COLOR, WORKER_COLOR, sw=0, opacity=0.10),
        rect(WX, t, WW, WH, "none", WORKER_COLOR, sw=2.2),
        txt(wx, cy - 20, paper,            size=15, fill=WORKER_COLOR, bold=True),
        txt(wx, cy +  8, "reads + distils", size=14, fill="#888888"),
    ]

# ── arrows workers → outputs (all-to-all, faint) ─────────────────────────────
for cy in w_centers:
    for oy in o_centers:
        out.append(arr(WX + WW, cy, OX, oy, col="#dddddd", sw=1.2))

# ── output tier boxes ─────────────────────────────────────────────────────────
for t, cy, col, lbl, (desc1, desc2) in zip(o_tops, o_centers, TIER_COLORS, TIER_LABELS, TIER_DESCS):
    ox = OX + OW // 2
    out += [
        rect(OX, t, OW, OH, col, col, sw=0, opacity=0.10),
        rect(OX, t, OW, OH, "none", col, sw=2.2),
        txt(ox, cy - 28, lbl,   size=18, fill=col, bold=True),
        txt(ox, cy -  2, desc1, size=14, fill="#777777"),
        txt(ox, cy + 20, desc2, size=14, fill="#777777"),
    ]

out.append('</svg>')

svg = "\n".join(out)
with open("assets/papers_diagram.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"saved assets/papers_diagram.svg  ({len(svg):,} bytes)")
