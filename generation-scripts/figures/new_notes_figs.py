"""
Figures for new notes 7-16 (AI topics, AGI foundations, paradoxes).
All analytical / conceptual — no Monte Carlo simulations needed.
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


# ============================================================
# Note 7: Chain-of-thought
# ============================================================

def fig_cot_scaling():
    """Illustrate CoT performance as function of model scale.
    Conceptual based on Wei 2022: CoT gains only emerge at ~100B params."""
    model_scale = np.logspace(8, 12, 60)  # 10^8 to 10^12 params
    # Standard prompting: smooth monotone improvement
    standard = 10 + 25 * (np.log10(model_scale) - 8) / 4
    # CoT: kicks in sharply around 10^11
    x = np.log10(model_scale)
    cot = 10 + 25 * (x - 8) / 4 + 45 / (1 + np.exp(-4 * (x - 10.8)))
    cot = np.clip(cot, 10, 80)

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.semilogx(model_scale, standard, "-o", color=PALETTE["grey"],
                linewidth=2, markersize=4, label="standard prompting")
    ax.semilogx(model_scale, cot, "-D", color=PALETTE["blue"],
                linewidth=2.2, markersize=5, label="chain-of-thought prompting")
    ax.axvspan(1e11, 1e12, alpha=0.08, color=PALETTE["green"])
    ax.text(3e11, 72, "CoT gain\nemerges", ha="center", fontsize=9.5,
            color=PALETTE["green"], fontweight="semibold")
    ax.set_xlabel("model parameters  (log scale)", fontsize=11)
    ax.set_ylabel("GSM8K accuracy  (%)", fontsize=11)
    ax.set_title("Chain-of-thought gains emerge only at ~100B+ parameters",
                 pad=8)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_ylim(0, 90)
    fig.tight_layout()
    fig.savefig(HERE / "cot-fig1-scaling.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 8: RAG reliability
# ============================================================

def fig_rag_architecture():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")
    boxes = [
        (0.5, 2, "User query\n$q$", PALETTE["grey"]),
        (2.6, 2, "Retriever\n$R(q)$ → top-$k$\npassages", PALETTE["blue"]),
        (4.8, 2.9, "Document corpus\n(dense vector index)", PALETTE["lightgrey"]),
        (4.8, 1.1, "Reranker\n(optional)", PALETTE["orange"]),
        (7.2, 2, "Generator LLM\n$p(y \\mid q, \\text{docs})$", PALETTE["green"]),
        (9.4, 2, "Response\n$y$", PALETTE["grey"]),
    ]
    for (x, y, t, c) in boxes:
        ax.annotate(t, xy=(x, y), ha="center", va="center", fontsize=9.5,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=c,
                              alpha=0.2, edgecolor=c, linewidth=1.5))
    def arr(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color="#444", lw=1.2))
    arr(1.1, 2, 2.1, 2)
    arr(3.3, 2.1, 4.3, 2.8)
    arr(4.3, 2.6, 3.3, 2.1)
    arr(3.3, 1.9, 4.3, 1.2)
    arr(4.3, 1.3, 3.3, 1.9)
    arr(3.3, 2, 6.5, 2)
    arr(5.5, 1.2, 6.7, 1.85)
    arr(7.9, 2, 8.9, 2)
    # Failure-mode annotations
    failures = [
        (2.6, 0.2, "(a) retrieval miss:\nwrong passages",
         PALETTE["red"]),
        (7.2, 0.2, "(c) context pollution:\nirrelevant text in context\n→ answer drift",
         PALETTE["red"]),
        (4.8, 3.65, "(b) index staleness:\nfacts outdated",
         PALETTE["red"]),
    ]
    for (x, y, t, c) in failures:
        ax.annotate(t, xy=(x, y), ha="center", va="center", fontsize=8.5,
                    color=c, style="italic",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              edgecolor=c, linewidth=1))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.5, 4.2)
    ax.set_title("RAG pipeline and its three primary failure modes", fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(HERE / "rag-fig1-architecture.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 9: Mechanism design for AI
# ============================================================

def fig_md_proper_scoring():
    """Illustrate expected score of a proper scoring rule (Brier)."""
    p_reported = np.linspace(0.01, 0.99, 100)
    # Brier score for binary outcome with true p=0.7
    # E[score] = p(1-p_r)^2 + (1-p)p_r^2
    true_p = 0.7
    expected = true_p * (1 - p_reported)**2 + (1 - true_p) * p_reported**2

    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(p_reported, expected, color=PALETTE["blue"], linewidth=2.2)
    ax.axvline(true_p, color=PALETTE["green"], linestyle="--", linewidth=1.4,
               label=f"true  $p = {true_p}$  (minimizer)")
    ax.plot(true_p, true_p * (1 - true_p),
            "o", color=PALETTE["green"], markersize=10, zorder=5)
    ax.set_xlabel(r"reported probability  $\hat p$", fontsize=11)
    ax.set_ylabel("expected Brier score (lower = better)", fontsize=11)
    ax.set_title(r"Proper scoring rule: truthful report  $\hat p = p$  minimizes expected loss",
                 pad=8)
    ax.legend(loc="upper center", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(HERE / "md-fig1-proper-scoring.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 10: Multi-agent coordination
# ============================================================

def fig_ma_prisoners():
    """Payoff matrix heatmap for iterated prisoner's dilemma."""
    labels = ["Cooperate", "Defect"]
    payoffs = np.array([[[3, 3], [0, 5]],
                        [[5, 0], [1, 1]]])  # row player, col player

    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    cells = np.zeros((2, 2, 3))  # RGB
    base_cmap = plt.colormaps["RdYlGn"]
    row_score = payoffs[..., 0]
    for i in range(2):
        for j in range(2):
            norm = row_score[i, j] / 5
            color = base_cmap(norm * 0.85)
            ax.add_patch(plt.Rectangle((j, 1 - i), 1, 1,
                                        facecolor=color, edgecolor="white",
                                        linewidth=2.5))
            ax.text(j + 0.5, 1 - i + 0.65, f"({payoffs[i, j, 0]}, {payoffs[i, j, 1]})",
                    ha="center", va="center", fontsize=13, fontweight="semibold")
            ax.text(j + 0.5, 1 - i + 0.3,
                    ["mutual coop", "sucker", "temptation", "mutual defect"][i * 2 + j],
                    ha="center", va="center", fontsize=9, style="italic")
    ax.set_xticks([0.5, 1.5])
    ax.set_yticks([0.5, 1.5])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticklabels(labels[::-1], fontsize=10)
    ax.set_xlabel("Player 2", fontsize=11)
    ax.set_ylabel("Player 1", fontsize=11)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_title("Prisoner's dilemma: mutual defection is the one-shot Nash equilibrium",
                 pad=8, fontsize=11.5)
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(HERE / "ma-fig1-prisoners.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 11: Scaling hypothesis
# ============================================================

def fig_scaling_laws():
    """Kaplan/Hoffmann-style power-law loss curves."""
    compute = np.logspace(18, 23, 60)  # FLOPs
    # Kaplan law: L ~ (C_c/C)^alpha with alpha~0.05
    L_kaplan = 1.7 * (1e22 / compute)**0.05 + 1.7
    # Chinchilla: similar alpha but different intercept
    L_chinchilla = 1.9 * (1e22 / compute)**0.055 + 1.5
    # Hypothetical saturation (alleged diminishing returns)
    L_saturate = np.where(compute < 1e22, L_kaplan, 2.2)

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.loglog(compute, L_kaplan, "-", color=PALETTE["blue"], linewidth=2.2,
              label="Kaplan et al. 2020 power law")
    ax.loglog(compute, L_chinchilla, "--", color=PALETTE["orange"], linewidth=2.2,
              label="Hoffmann/Chinchilla 2022 (rebalanced)")
    ax.loglog(compute, L_saturate, ":", color=PALETTE["red"], linewidth=2.2,
              label="hypothetical saturation")
    ax.set_xlabel("training compute  $C$  (FLOPs, log scale)", fontsize=11)
    ax.set_ylabel("validation loss  (log scale)", fontsize=11)
    ax.set_title("Scaling laws: empirical power law vs. hypothetical saturation",
                 pad=8)
    ax.legend(loc="upper right", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(HERE / "scaling-fig1-laws.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 12: Alignment problem
# ============================================================

def fig_alignment_mesa():
    """Mesa-optimization diagram: outer vs. inner objective mismatch."""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")
    boxes = [
        (1, 3, "Outer training objective\n(what we optimize)", PALETTE["blue"]),
        (1, 1, "Inner learned policy\n(what the model does)", PALETTE["red"]),
        (5, 3, "Training distribution\n$\\mathcal{D}_\\text{train}$", PALETTE["grey"]),
        (5, 1, "Deployment distribution\n$\\mathcal{D}_\\text{deploy}$", PALETTE["grey"]),
        (8.5, 2, "Mesa-objective\nmismatch:\nsame behavior\non train,\ndifferent on deploy",
         PALETTE["orange"]),
    ]
    for (x, y, t, c) in boxes:
        ax.annotate(t, xy=(x, y), ha="center", va="center", fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=c,
                              alpha=0.18, edgecolor=c, linewidth=1.5))
    ax.annotate("", xy=(5, 1), xytext=(1, 1),
                arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3))
    ax.annotate("optimized on", xy=(3, 1.15), ha="center", fontsize=8.5, color="#555")
    ax.annotate("", xy=(5, 3), xytext=(1, 3),
                arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3))
    ax.annotate("measured on", xy=(3, 3.15), ha="center", fontsize=8.5, color="#555")
    ax.annotate("", xy=(8.5, 2), xytext=(5.5, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=PALETTE["orange"], lw=1.3))
    ax.annotate("", xy=(8.5, 2), xytext=(5.5, 2.5),
                arrowprops=dict(arrowstyle="-|>", color=PALETTE["orange"], lw=1.3))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.5)
    ax.set_title("Mesa-optimization: inner policy develops its own objective",
                 fontsize=12, pad=10)
    fig.tight_layout()
    fig.savefig(HERE / "align-fig1-mesa.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 13: Godel, Lob, formal limits
# ============================================================

def fig_godel_diagonalization():
    """Conceptual sketch of Godel's second incompleteness via diagonalization."""
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    # Central statement G
    ax.annotate("$G$ : \"This sentence is not provable in $T$\"",
                xy=(5, 3.5), ha="center", va="center", fontsize=12,
                bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["blue"],
                          alpha=0.18, edgecolor=PALETTE["blue"], linewidth=1.6))
    # Two branches
    ax.annotate("If $T \\vdash G$:\nthen $G$ is provable,\nbut $G$ says it is not\n$\\Rightarrow T$ is inconsistent",
                xy=(2, 1.5), ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.5", facecolor=PALETTE["red"],
                          alpha=0.15, edgecolor=PALETTE["red"], linewidth=1.3))
    ax.annotate("If $T \\nvdash G$:\nthen $G$ is true but unprovable\n$\\Rightarrow T$ is incomplete",
                xy=(8, 1.5), ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.5", facecolor=PALETTE["orange"],
                          alpha=0.15, edgecolor=PALETTE["orange"], linewidth=1.3))
    ax.annotate("", xy=(3, 2.2), xytext=(4.2, 3.2),
                arrowprops=dict(arrowstyle="->", color="#444", lw=1.2))
    ax.annotate("", xy=(7, 2.2), xytext=(5.8, 3.2),
                arrowprops=dict(arrowstyle="->", color="#444", lw=1.2))
    ax.annotate("Any consistent, sufficiently strong, effectively axiomatized theory $T$ is incomplete.",
                xy=(5, 4.7), ha="center", va="center", fontsize=11,
                fontweight="semibold", color="#111")
    ax.set_title("Gödel's First Incompleteness Theorem via diagonalization",
                 fontsize=11.5, pad=10)
    fig.tight_layout()
    fig.savefig(HERE / "godel-fig1-diagonalization.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 14: AIXI / Solomonoff induction
# ============================================================

def fig_solomonoff():
    """Illustrate Solomonoff prior: weight programs by 2^(-length)."""
    lengths = np.arange(1, 20)
    weights = 2.0 ** (-lengths.astype(float))
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.semilogy(lengths, weights, "-D", color=PALETTE["blue"], markersize=6,
                linewidth=1.8)
    ax.fill_between(lengths, 1e-8, weights, color=PALETTE["blue"], alpha=0.1)
    for i, (l, w) in enumerate(zip(lengths[:6], weights[:6])):
        ax.annotate(f"$2^{{-{l}}}$", xy=(l, w), xytext=(0, 10),
                    textcoords="offset points", ha="center", fontsize=8.5,
                    color=PALETTE["blue"])
    ax.set_xlabel("program length  $\\ell(p)$  (bits)", fontsize=11)
    ax.set_ylabel(r"Solomonoff prior  $M(p) = 2^{-\ell(p)}$", fontsize=11)
    ax.set_title("Solomonoff prior: simpler programs have exponentially higher weight",
                 pad=8)
    ax.set_xticks(np.arange(0, 20, 2))
    ax.grid(True, which="both", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(HERE / "aixi-fig1-solomonoff.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 15: World models
# ============================================================

def fig_worldmodel_loop():
    """Model-based RL / world model loop."""
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.axis("off")
    center = (5, 2)
    nodes = [
        (1, 2, "Environment\n$\\mathcal{E}$", PALETTE["grey"]),
        (4, 3.4, "Observation\n$o_t$", PALETTE["blue"]),
        (7, 3.4, "World model\n$p_\\theta(s_{t+1} \\mid s_t, a_t)$", PALETTE["green"]),
        (8.5, 2, "Latent state\n$s_t$", PALETTE["green"]),
        (7, 0.6, "Planner\n$\\pi(a \\mid s)$", PALETTE["orange"]),
        (4, 0.6, "Action\n$a_t$", PALETTE["red"]),
    ]
    for (x, y, t, c) in nodes:
        ax.annotate(t, xy=(x, y), ha="center", va="center", fontsize=9.5,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=c,
                              alpha=0.18, edgecolor=c, linewidth=1.4))
    def arr(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.2))
    arr(1.7, 2.2, 3.4, 3.2)
    arr(4.6, 3.4, 6.3, 3.4)
    arr(7.6, 3.1, 8.3, 2.3)
    arr(8.3, 1.7, 7.6, 0.9)
    arr(6.3, 0.6, 4.6, 0.6)
    arr(3.4, 0.8, 1.7, 1.8)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.3, 4.1)
    ax.set_title("World-model agent loop: observe → encode → imagine → plan → act",
                 fontsize=11.5, pad=10)
    fig.tight_layout()
    fig.savefig(HERE / "wm-fig1-loop.svg", format="svg")
    plt.close(fig)


# ============================================================
# Note 16: Computational irreducibility
# ============================================================

def fig_no_free_lunch():
    """Illustrate no-free-lunch: averaged over all problems, all algorithms tie."""
    n_algos = 6
    n_problems = 100
    rng = np.random.default_rng(42)
    # Each algorithm performs well on roughly random problems but averages the same
    performance = rng.beta(2, 5, size=(n_algos, n_problems))
    # normalize rows so means are similar
    performance = performance / performance.mean(axis=1, keepdims=True) * 0.5

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.3))
    # Left: per-problem performance (one algorithm's view)
    algo_idx = 0
    ax1.bar(np.arange(n_problems), performance[algo_idx],
            color=PALETTE["blue"], alpha=0.7, edgecolor="white", linewidth=0.3)
    ax1.set_xlabel("problem index  (each a different optimization task)", fontsize=11)
    ax1.set_ylabel("algorithm $A$'s performance", fontsize=11)
    ax1.set_title("Algorithm $A$ beats others on some problems...", fontsize=10.5, pad=8)

    # Right: averaged over all problems, all algorithms tie
    mean_perf = performance.mean(axis=1)
    colors = plt.colormaps["viridis"](np.linspace(0.15, 0.85, n_algos))
    bars = ax2.bar([f"$A_{i+1}$" for i in range(n_algos)], mean_perf,
                   color=colors, alpha=0.85, edgecolor="white", linewidth=1.2)
    for bar, v in zip(bars, mean_perf):
        ax2.text(bar.get_x() + bar.get_width() / 2, v + 0.008, f"{v:.3f}",
                 ha="center", fontsize=9)
    ax2.axhline(mean_perf.mean(), color="black", linestyle="--", linewidth=1,
                label=f"common mean $\\approx${mean_perf.mean():.3f}")
    ax2.set_ylabel("performance averaged over all problems", fontsize=11)
    ax2.set_title("...but averaged over all problems, all algorithms tie", fontsize=10.5, pad=8)
    ax2.legend(fontsize=9)
    ax2.set_ylim(0, mean_perf.max() * 1.25)

    fig.suptitle("No-Free-Lunch: Wolpert & Macready 1997",
                 fontsize=12.5, y=1.01, fontweight="semibold")
    fig.tight_layout()
    fig.savefig(HERE / "nfl-fig1-tradeoff.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    figures = [
        ("cot scaling", fig_cot_scaling),
        ("rag architecture", fig_rag_architecture),
        ("mechanism design", fig_md_proper_scoring),
        ("prisoners", fig_ma_prisoners),
        ("scaling laws", fig_scaling_laws),
        ("mesa-opt", fig_alignment_mesa),
        ("godel", fig_godel_diagonalization),
        ("solomonoff", fig_solomonoff),
        ("world model", fig_worldmodel_loop),
        ("no-free-lunch", fig_no_free_lunch),
    ]
    for name, fn in figures:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.2f}s)")
    print(f"total: {time.time() - t0:.1f}s")
