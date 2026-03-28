"""
Generate the hero progression figure for the README.
Three-row layout: one row per parallel research direction.
Filled dots = above significance threshold. Hollow = below.
"""
import matplotlib.pyplot as plt
import numpy as np

# ── data ──────────────────────────────────────────────────────────────────────
DIRECTIONS = [
    {
        "name":    "Does accuracy become misleading under class imbalance?",
        "finding": "accuracy diverges from F1 at imbalance ratio 5:1",
        "scores":  [8, 7, 6],
        "color":   "#4C72B0",
    },
    {
        "name":    "Which metrics reliably track model quality?",
        "finding": "F1 / MCC outperform AUC as quality proxies",
        "scores":  [8, 6, 7, 8, 6],
        "color":   "#CC6677",
    },
    {
        "name":    "Can threshold tuning recover performance at high imbalance?",
        "finding": "threshold 0.10 recovers F1 from 0 → 0.31 at ratio 20:1",
        "scores":  [8, 7, 6, 8],
        "color":   "#44AA99",
    },
]
THRESHOLD = 7
N_COLS    = 5

# ── figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(len(DIRECTIONS), 1, figsize=(11, 7.2), sharex=False)
fig.patch.set_facecolor("white")
fig.subplots_adjust(hspace=0.18, left=0.04, right=0.97, top=0.76, bottom=0.10)

for i, (ax, d) in enumerate(zip(axes, DIRECTIONS)):
    scores = d["scores"]
    color  = d["color"]
    xs     = list(range(1, len(scores) + 1))

    ax.set_facecolor("#fafafa")

    # ── threshold band & line ─────────────────────────────────────────────────
    ax.axhspan(THRESHOLD, 10.8, color="#2ecc71", alpha=0.08, zorder=0)
    ax.axhline(THRESHOLD, color="#ccc", linestyle="--", linewidth=1.1, zorder=1)
    ax.text(0.42, THRESHOLD + 0.2, "significance threshold",
            fontsize=7, color="#bbb", va="bottom")

    # ── fill under curve ─────────────────────────────────────────────────────
    ax.fill_between(xs, scores, 3.0, color=color, alpha=0.08, zorder=2)

    # ── connecting line ───────────────────────────────────────────────────────
    ax.plot(xs, scores, "-", color=color, linewidth=2.2, alpha=0.85,
            solid_capstyle="round", zorder=3)

    # ── dots ──────────────────────────────────────────────────────────────────
    for x, s in zip(xs, scores):
        filled = s >= THRESHOLD
        ax.plot(x, s, "o", color=color, markersize=11,
                markerfacecolor=color if filled else "white",
                markeredgewidth=2.2, zorder=5)
        ax.text(x, s + 0.48, str(s), ha="center", va="bottom",
                fontsize=9, color=color, fontweight="bold")

    # ── "✓ finalized" next to last dot ────────────────────────────────────────
    ax.text(xs[-1] + 0.22, scores[-1], "✓ finalized",
            fontsize=8, color=color, va="center", ha="left", fontweight="semibold")

    # ── axes styling ──────────────────────────────────────────────────────────
    ax.set_xlim(0.35, N_COLS + 1.0)
    ax.set_ylim(3.0, 10.8)
    ax.set_yticks([4, 6, 8, 10])
    ax.tick_params(axis="y", labelsize=8, colors="#aaa", length=2, pad=3)
    ax.tick_params(axis="x", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e8e8e8")
    ax.spines["bottom"].set_color("#e8e8e8")
    ax.grid(axis="y", color="#efefef", linewidth=0.8, zorder=0)
    ax.set_xticks(range(1, len(scores) + 1))

    # show x tick labels only on bottom subplot
    if i < len(DIRECTIONS) - 1:
        ax.set_xticklabels([])
    else:
        ax.set_xticklabels([f"exp_{j:03d}" for j in range(1, len(scores) + 1)],
                           fontsize=9, color="#aaa")
        ax.set_xlabel("experiment", fontsize=9, color="#aaa", labelpad=5)

    # ── two-line header above each subplot (using transAxes) ─────────────────
    # direction name — bold, colored
    ax.text(0.0, 1.18, d["name"],
            transform=ax.transAxes,
            fontsize=10, fontweight="bold", color=color,
            va="bottom", ha="left")
    # key finding — italic, gray
    ax.text(0.0, 1.04, "→  " + d["finding"],
            transform=ax.transAxes,
            fontsize=8.5, fontstyle="italic", color="#666",
            va="bottom", ha="left")

# ── figure title ──────────────────────────────────────────────────────────────
fig.text(0.5, 0.985,
         "demo run  ·  3 parallel directions  ·  12 experiments  ·  avg score 7.3 / 10",
         ha="center", fontsize=9.5, color="#888")

# ── legend ────────────────────────────────────────────────────────────────────
filled_dot = plt.Line2D([0], [0], marker="o", linestyle="none",
                         markerfacecolor="#555", markeredgecolor="#555",
                         markersize=8, label="score ≥ 7  (significant finding)")
hollow_dot = plt.Line2D([0], [0], marker="o", linestyle="none",
                         markerfacecolor="white", markeredgecolor="#999",
                         markeredgewidth=1.8, markersize=8,
                         label="score < 7  (keep iterating)")
fig.legend(handles=[filled_dot, hollow_dot],
           loc="lower center", ncol=2,
           fontsize=8.5, frameon=False,
           bbox_to_anchor=(0.5, 0.01),
           labelcolor="#666")

plt.savefig("assets/progression.png", dpi=160, bbox_inches="tight",
            facecolor="white", edgecolor="none")
print("saved assets/progression.png")
