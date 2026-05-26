"""
Repaired conceptual diagrams (April 2026 revision):
- Fixes align-fig1-mesa: redesigned as a simple 2-row "what you specify vs. what
  you get" table with a single explicit arrow labeled "distribution shift exposes
  the gap." Arrows no longer cross; text doesn't overlap annotations.
- Fixes rag-fig1-architecture: arrows go one direction between components;
  failure-mode callouts are positioned in clean margins without overlapping
  the pipeline.
- Fixes agents-fig3-error-taxonomy: bullet lists fit inside boxes; more vertical
  space; no text wrapping outside box edges.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()


def _box(ax, x, y, w, h, text, color, fontsize=10.5, bold=False):
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4, edgecolor=color, facecolor=color, alpha=0.18,
    )
    ax.add_patch(rect)
    weight = "semibold" if bold else "normal"
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color="#111", fontweight=weight, wrap=True)


def _arrow(ax, xy0, xy1, color="#444", lw=1.3, ls="-"):
    ax.annotate("", xy=xy1, xytext=xy0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls,
                                shrinkA=2, shrinkB=2,
                                mutation_scale=14))


# ============================================================
# FIX: align-fig1-mesa
# Layout: outer ring (what we specify) -> training -> deployment -> gap callout
# ============================================================

def fig_align_mesa():
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.2, 5.2)
    ax.axis("off")

    # Row 1: "What you specify"
    ax.text(0.15, 4.6, "What you specify", fontsize=11, fontweight="semibold",
            color=PALETTE["blue"])
    _box(ax, 0.15, 3.55, 2.8, 0.85,
         "Outer objective $r$\n(reward, loss)", PALETTE["blue"])
    _box(ax, 3.45, 3.55, 2.8, 0.85,
         "Training\ndistribution", PALETTE["grey"])
    _box(ax, 6.75, 3.55, 2.8, 0.85,
         "Deployment\ndistribution", PALETTE["grey"])

    # Row 2: "What you get"
    ax.text(0.15, 2.55, "What the optimizer produces", fontsize=11,
            fontweight="semibold", color=PALETTE["red"])
    _box(ax, 0.15, 1.5, 2.8, 0.85,
         "Mesa-optimizer with\n*inner* objective $r^{*}$",
         PALETTE["red"])
    _box(ax, 3.45, 1.5, 2.8, 0.85,
         "Behavior matches $r$\n(training reward is maximized)",
         PALETTE["green"])
    _box(ax, 6.75, 1.5, 2.8, 0.85,
         "Behavior pursues $r^{*}$\n($r$ no longer achieved)",
         PALETTE["orange"])

    # Vertical arrows (what you specify -> what you get)
    for x in [1.55, 4.85, 8.15]:
        _arrow(ax, (x, 3.5), (x, 2.4), color="#666", lw=1.1)

    # Horizontal reading-order arrows row 2
    _arrow(ax, (3.0, 1.93), (3.4, 1.93), color="#444")
    _arrow(ax, (6.3, 1.93), (6.7, 1.93), color="#444")

    # Bottom annotation
    ax.text(5.35, 0.4,
            "The gap between $r$ and $r^{*}$ is invisible under training distribution; "
            "distribution shift exposes it at deployment.",
            ha="center", fontsize=10, style="italic", color="#333")

    ax.set_title("Mesa-optimization: what you specify vs. what the optimizer produces",
                 fontsize=12.5, pad=14)
    fig.tight_layout()
    fig.savefig(HERE / "align-fig1-mesa.svg", format="svg")
    plt.close(fig)


# ============================================================
# FIX: rag-fig1-architecture
# Left-to-right pipeline; corpus feeds retriever (one-way);
# failure-mode callouts in clean margins.
# ============================================================

def fig_rag():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.3, 5.3)
    ax.axis("off")

    # Main pipeline: query -> retriever -> reranker -> generator -> response
    _box(ax, 0.1, 2.3, 1.5, 0.9, "User query\n$q$", PALETTE["grey"])
    _box(ax, 2.15, 2.3, 2.0, 0.9,
         "Retriever\n$R(q)$  →  top-$k$", PALETTE["blue"])
    _box(ax, 4.7, 2.3, 2.0, 0.9, "Reranker\n(optional)", PALETTE["orange"])
    _box(ax, 7.25, 2.3, 2.2, 0.9,
         "Generator LLM\n$p(y \\mid q, \\text{docs})$", PALETTE["green"])
    _box(ax, 9.95, 2.3, 0.95, 0.9, "Response\n$y$", PALETTE["grey"])

    # Document corpus above
    _box(ax, 2.4, 4.0, 2.0, 0.7,
         "Document corpus\n(dense index)", PALETTE["lightgrey"],
         fontsize=9.5)
    _arrow(ax, (3.4, 4.0), (3.2, 3.22), color="#555")
    ax.text(3.55, 3.55, "retrieves from", fontsize=8.5,
            style="italic", color="#555", ha="left")

    # Pipeline arrows (all left-to-right)
    _arrow(ax, (1.6, 2.75), (2.15, 2.75))
    _arrow(ax, (4.15, 2.75), (4.7, 2.75))
    _arrow(ax, (6.7, 2.75), (7.25, 2.75))
    _arrow(ax, (9.45, 2.75), (9.95, 2.75))

    # Failure modes as margin callouts with pointers
    def callout(x, y, text, target_xy, color):
        ax.text(x, y, text, ha="center", va="center", fontsize=9,
                style="italic", color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=color, linewidth=1))
        _arrow(ax, (x, y + 0.35), target_xy, color=color, lw=0.9, ls=":")

    callout(3.15, 0.65, "(a) retrieval miss:\nwrong passages",
            (3.15, 2.3), PALETTE["red"])
    callout(5.7, 4.55, "(b) index staleness:\nfacts outdated",
            (3.4, 4.0), PALETTE["red"])
    callout(8.35, 0.65, "(c) context pollution:\nirrelevant text\n→ answer drift",
            (8.35, 2.3), PALETTE["red"])

    ax.set_title("RAG pipeline and its three primary failure modes",
                 fontsize=12.5, pad=12)
    fig.tight_layout()
    fig.savefig(HERE / "rag-fig1-architecture.svg", format="svg")
    plt.close(fig)


# ============================================================
# FIX: agents-fig3-error-taxonomy
# Wider boxes, smaller bullets, more vertical breathing room.
# ============================================================

def fig_agents_taxonomy():
    fig, ax = plt.subplots(figsize=(11.5, 6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    # Title
    ax.text(5.75, 6.2, "A working taxonomy of LLM-agent errors",
            fontsize=13, fontweight="semibold", ha="center", color="#111")
    ax.text(5.75, 5.75,
            "Each category has different failure patterns and different remediation strategies",
            fontsize=10, ha="center", style="italic", color="#555")

    boxes = [
        {
            "x": 0.3, "w": 3.5,
            "title": "Specification errors",
            "color": PALETTE["blue"],
            "desc": "User request is ambiguous;\nagent commits to wrong\ninterpretation silently.",
            "examples": ("•  \"delete old files\"\n"
                         "    → which files? how old?\n"
                         "•  \"refactor this\"\n"
                         "    → preserve behavior?"),
            "detect": "detectable via schema\nvalidation + clarification",
        },
        {
            "x": 4.0, "w": 3.5,
            "title": "Tool-call errors",
            "color": PALETTE["orange"],
            "desc": "Argument to a tool is\nmalformed, type-mismatched,\nor semantically wrong.",
            "examples": ("•  string passed where\n    int expected\n"
                         "•  valid type, wrong value\n    (e.g. wrong user id)"),
            "detect": "detectable via strict\ntyping + retry w/ error",
        },
        {
            "x": 7.7, "w": 3.5,
            "title": "Reasoning errors",
            "color": PALETTE["red"],
            "desc": "Chain of reasoning is invalid;\nconclusions don't follow\nfrom premises.",
            "examples": ("•  agent asserts fact\n    contradicted by its\n    own tool output\n"
                         "•  math error in reasoning"),
            "detect": "hardest to detect:\nagent sounds confident",
        },
    ]

    for b in boxes:
        x = b["x"]
        w = b["w"]
        # outer box
        rect = mpatches.FancyBboxPatch(
            (x, 0.9), w, 4.5,
            boxstyle="round,pad=0.05",
            linewidth=1.4, edgecolor=b["color"], facecolor=b["color"], alpha=0.12,
        )
        ax.add_patch(rect)
        # title
        ax.text(x + w / 2, 5.05, b["title"], fontsize=11.5,
                fontweight="semibold", ha="center", color=b["color"])
        # description
        ax.text(x + w / 2, 4.2, b["desc"], fontsize=9.5, ha="center",
                va="center", color="#222")
        # examples
        ax.text(x + 0.2, 2.95, b["examples"], fontsize=8.8, ha="left",
                va="top", color="#444", family="monospace")
        # detect caption below box
        ax.text(x + w / 2, 0.55, b["detect"],
                fontsize=8.5, style="italic", ha="center", color="#555")

    fig.tight_layout()
    fig.savefig(HERE / "agents-fig3-error-taxonomy.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    import time
    t0 = time.time()
    for name, fn in [("align-mesa", fig_align_mesa),
                     ("rag-architecture", fig_rag),
                     ("agents-taxonomy", fig_agents_taxonomy)]:
        t = time.time()
        print(f"fig {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.2f}s)")
    print(f"total: {time.time() - t0:.1f}s")
