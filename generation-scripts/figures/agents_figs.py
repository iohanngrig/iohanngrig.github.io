"""
LLM agents figures — benchmark summaries and error-taxonomy diagrams.
No heavy simulation; illustrates published numbers and a conceptual taxonomy.

Numbers used:
    - GAIA benchmark scores (top-of-leaderboard ranges as of late 2025)
    - SWE-bench Verified trend (approximate published agent scores)
    - Human baseline on GAIA (~92%)
These are drawn from the original papers (Mialon et al. 2023, Jimenez et al. 2024)
and widely-reported public leaderboards. They are illustrative, not authoritative.

Three figures:
    agents-fig1-benchmark-gap.svg     GAIA: LLM vs. human, by difficulty level
    agents-fig2-swebench-trend.svg    SWE-bench Verified: agent scores over time
    agents-fig3-error-taxonomy.svg    Agent-error taxonomy diagram
"""
import sys
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()


def figure1_gaia():
    """GAIA benchmark: LLM agent scores vs. human baseline, by difficulty level.

    Numbers from Mialon et al. 2023 (original GAIA paper) and widely-reported
    ranges from the GAIA leaderboard. GPT-4 with tools and top Sonnet-class agents
    were in the 30-50% range on Level 1, lower on Levels 2-3; humans achieve ~92%.
    """
    levels = ["Level 1\n(simpler)", "Level 2", "Level 3\n(hardest)"]
    # Approximate ranges — illustrative, not authoritative
    agent_score = [48, 33, 22]
    human_score = [94, 92, 87]

    x = np.arange(len(levels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars_a = ax.bar(x - width / 2, agent_score, width, color=PALETTE["red"],
                    alpha=0.85, edgecolor="white", linewidth=1.2,
                    label="best LLM agent (2025)")
    bars_h = ax.bar(x + width / 2, human_score, width, color=PALETTE["blue"],
                    alpha=0.85, edgecolor="white", linewidth=1.2,
                    label="human baseline")
    for bars, vals in [(bars_a, agent_score), (bars_h, human_score)]:
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v}%",
                    ha="center", fontsize=9)
    ax.set_ylim(0, 110)
    ax.set_xticks(x)
    ax.set_xticklabels(levels, fontsize=10)
    ax.set_ylabel("accuracy on GAIA tasks (%)")
    ax.set_title("GAIA: the honest benchmark. Humans outperform best LLM agents "
                 "by 40–70 percentage points")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    fig.savefig(HERE / "agents-fig1-benchmark-gap.svg", format="svg")
    plt.close(fig)


def figure2_swebench():
    """SWE-bench Verified trend — published agent scores over time.

    Numbers approximate the publicly reported SWE-bench Verified progress from
    ~1% (early 2024) to ~60%+ (late 2025). These are widely discussed but not
    all from a single peer-reviewed source — the dates and values are
    representative rather than exact.
    """
    dates = ["2024-01", "2024-06", "2024-11", "2025-04", "2025-10"]
    scores = [1.9, 13.9, 34.2, 49.1, 61.0]  # illustrative; rounded from leaderboard
    methods = ["SWE-agent\nbaseline", "Agentless", "SWE-Gym\n+RL", "Agent frameworks\n+ Claude 3.5", "Agent frameworks\n+ GPT-4-class"]

    fig, ax = plt.subplots(figsize=(8.5, 4.3))
    x = np.arange(len(dates))
    ax.plot(x, scores, "-D", color=PALETTE["blue"], markersize=8, linewidth=1.8)
    for xi, yi, m in zip(x, scores, methods):
        ax.annotate(f"{yi}%", xy=(xi, yi), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=9)
        ax.annotate(m, xy=(xi, yi), xytext=(0, -18),
                    textcoords="offset points", ha="center", fontsize=8,
                    color=PALETTE["grey"])

    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=9)
    ax.set_ylim(0, 75)
    ax.set_ylabel("SWE-bench Verified resolved rate (%)")
    ax.set_title("SWE-bench Verified: the dramatic but imperfect agent story")
    ax.axhspan(50, 80, alpha=0.08, color=PALETTE["green"],
               label="")
    ax.text(0.5, 70, "deployed close rates\n(Cognition, Sourcegraph, etc.)\nreport substantially lower",
            fontsize=8, style="italic", color=PALETTE["grey"])
    fig.savefig(HERE / "agents-fig2-swebench-trend.svg", format="svg")
    plt.close(fig)


def figure3_error_taxonomy():
    """Diagram of the three agent error categories with example failure modes."""
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.axis("off")

    # Three colored boxes
    boxes = [
        {
            "x": 0.5, "y": 2.5, "w": 2.8, "h": 2.0,
            "title": "Specification errors",
            "desc": "User request is ambiguous;\nagent commits to wrong\ninterpretation silently.",
            "examples": "• \"delete old files\"\n  → which files? how old?\n• \"refactor this\"\n  → preserve behavior?",
            "color": PALETTE["blue"],
        },
        {
            "x": 3.7, "y": 2.5, "w": 2.8, "h": 2.0,
            "title": "Tool-call errors",
            "desc": "Argument to a tool is\nmalformed, type-mismatched,\nor semantically wrong.",
            "examples": "• passes string where int expected\n• semantically valid type\n  with wrong value\n  (e.g., wrong user id)",
            "color": PALETTE["orange"],
        },
        {
            "x": 6.9, "y": 2.5, "w": 2.8, "h": 2.0,
            "title": "Reasoning errors",
            "desc": "Chain of reasoning is invalid;\nconclusions don't follow\nfrom premises.",
            "examples": "• agent asserts fact\n  contradicted by its tool output\n• math error in reasoning\n• confident on false premise",
            "color": PALETTE["red"],
        },
    ]
    for b in boxes:
        rect = mpatches.FancyBboxPatch(
            (b["x"], b["y"]), b["w"], b["h"],
            boxstyle="round,pad=0.05", linewidth=1.5,
            edgecolor=b["color"], facecolor=b["color"], alpha=0.18,
        )
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"] / 2, b["y"] + b["h"] - 0.25, b["title"],
                fontsize=11, fontweight="bold", ha="center", color=b["color"])
        ax.text(b["x"] + b["w"] / 2, b["y"] + b["h"] - 0.8, b["desc"],
                fontsize=9, ha="center", va="top")
        ax.text(b["x"] + 0.15, b["y"] + 0.85, b["examples"],
                fontsize=8, ha="left", va="top", family="monospace",
                color=PALETTE["grey"])

    # Detection-difficulty indicator at bottom
    ax.text(0.5 + 2.8 / 2, 2.1, "detectable via schema\nvalidation & prompt",
            fontsize=8, ha="center", style="italic", color=PALETTE["grey"])
    ax.text(3.7 + 2.8 / 2, 2.1, "detectable via strict\ntype + retry with error",
            fontsize=8, ha="center", style="italic", color=PALETTE["grey"])
    ax.text(6.9 + 2.8 / 2, 2.1, "hardest to detect:\nagent sounds confident",
            fontsize=8, ha="center", style="italic", color=PALETTE["grey"])

    # Title
    ax.text(5, 5.0, "A working taxonomy of LLM-agent errors",
            fontsize=13, fontweight="bold", ha="center")
    ax.text(5, 4.6,
            "Each category has different failure patterns and different remediation strategies",
            fontsize=10, ha="center", style="italic", color=PALETTE["grey"])

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    fig.savefig(HERE / "agents-fig3-error-taxonomy.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in [("benchmark-gap", figure1_gaia),
                     ("swebench-trend", figure2_swebench),
                     ("error-taxonomy", figure3_error_taxonomy)]:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.1f}s)")
    print(f"total: {time.time() - t0:.1f}s")
