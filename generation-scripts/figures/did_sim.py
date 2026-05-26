"""
DiD revolution figures — analytical, upgraded April 2026.
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


def figure1_bacon_decomp():
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    cohorts = [
        ("Early-treated  $G_1$", 3, PALETTE["blue"]),
        ("Late-treated  $G_2$", 6, PALETTE["orange"]),
        ("Never-treated  $G_N$", None, PALETTE["grey"]),
    ]
    T = 10
    y_pos = [2.6, 1.6, 0.6]

    for (label, t_star, col), y in zip(cohorts, y_pos):
        ax.plot([0, T], [y, y], color=col, linewidth=1.5, alpha=0.28)
        if t_star is not None:
            ax.plot([t_star, T], [y, y], color=col, linewidth=3.6)
            ax.plot(t_star, y, "o", color=col, markersize=11,
                    markeredgecolor="white", markeredgewidth=1.2)
            ax.annotate(f"treated\nat $t={t_star}$", xy=(t_star, y),
                        xytext=(t_star, y + 0.22), fontsize=9, color=col,
                        ha="center", fontweight="semibold")
        ax.text(-0.4, y, label, ha="right", va="center", fontsize=10.5, color=col,
                fontweight="semibold")

    annotations = [
        (1.5, 3.15, "(1) Early vs. Never\n(around $t=3$)\n→  positive weight", PALETTE["green"]),
        (4.5, 3.15, "(2) Late vs. Never\n(around $t=6$)\n→  positive weight", PALETTE["green"]),
        (8.2, 1.95, "(3) Late vs. already-treated Early\n(late cohort's treatment period)\n→  NEGATIVE weight", PALETTE["red"]),
    ]
    for (x, y, text, col) in annotations:
        ax.annotate(text, xy=(x, y), ha="center", va="bottom", fontsize=9.2,
                    color=col, fontweight="semibold",
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                              edgecolor=col, linewidth=1.2))

    ax.set_xlim(-3.8, T + 0.6)
    ax.set_ylim(-0.3, 4.1)
    ax.set_xlabel("time  $t$", fontsize=11)
    ax.set_yticks([])
    ax.set_title("Goodman-Bacon decomposition: TWFE as weighted sum of 2×2 DiDs",
                 pad=12)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(HERE / "did-fig1-bacon-decomp.svg", format="svg")
    plt.close(fig)


def figure2_twfe_bias():
    T = 10
    n_per = 50
    rng = np.random.default_rng(42)
    gamma = np.linspace(0, 2, T)

    def make_panel():
        records = []
        alpha_e = rng.normal(0, 1, n_per) + 1.0
        for i in range(n_per):
            for t in range(T):
                eff = 0 if t < 3 else min(t - 2, 3)
                Y = alpha_e[i] + gamma[t] + eff + rng.normal(0, 0.2)
                records.append((f"E{i}", "early", t, 1 if t >= 3 else 0, Y))
        alpha_l = rng.normal(0, 1, n_per)
        for i in range(n_per):
            for t in range(T):
                eff = 1.0 if t >= 7 else 0
                Y = alpha_l[i] + gamma[t] + eff + rng.normal(0, 0.2)
                records.append((f"L{i}", "late", t, 1 if t >= 7 else 0, Y))
        alpha_n = rng.normal(0, 1, n_per) - 0.5
        for i in range(n_per):
            for t in range(T):
                Y = alpha_n[i] + gamma[t] + rng.normal(0, 0.2)
                records.append((f"N{i}", "never", t, 0, Y))
        return records

    import pandas as pd
    df = pd.DataFrame(make_panel(), columns=["unit", "cohort", "t", "D", "Y"])
    df["Y_wi"] = df.groupby("unit")["Y"].transform(lambda x: x - x.mean())
    df["Y_wi"] = df.groupby("t")["Y_wi"].transform(lambda x: x - x.mean())
    df["D_wi"] = df.groupby("unit")["D"].transform(lambda x: x - x.mean())
    df["D_wi"] = df.groupby("t")["D_wi"].transform(lambda x: x - x.mean())
    beta_twfe = float((df["Y_wi"] * df["D_wi"]).sum() / (df["D_wi"] ** 2).sum())

    never = df[df["cohort"] == "never"]
    cs_atts = []
    for g, group in [(3, "early"), (7, "late")]:
        cohort = df[df["cohort"] == group]
        for t in range(g, T):
            treat_diff = cohort[cohort.t == t].Y.mean() - cohort[cohort.t == g - 1].Y.mean()
            ctrl_diff = never[never.t == t].Y.mean() - never[never.t == g - 1].Y.mean()
            cs_atts.append((g, t, treat_diff - ctrl_diff))
    att_cs = float(np.mean([a for (_, _, a) in cs_atts]))
    true_effects = [min(t - 2, 3) if g == 3 else 1.0 for (g, t, _) in cs_atts]
    att_true = float(np.mean(true_effects))

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    methods = ["True ATT", "Callaway–\nSant'Anna", "TWFE"]
    values = [att_true, att_cs, beta_twfe]
    colors = [PALETTE["green"], PALETTE["blue"], PALETTE["red"]]
    bars = ax.bar(methods, values, color=colors, alpha=0.82,
                  edgecolor="white", linewidth=1.8, width=0.55)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05,
                f"{v:.2f}", ha="center", fontsize=11, fontweight="semibold")
    ax.axhline(att_true, color=PALETTE["green"], linestyle=":", linewidth=1.2, alpha=0.6)
    ax.set_ylabel("estimated average treatment effect on treated", fontsize=11)
    ax.set_title("TWFE underestimates the true ATT in a heterogeneous-effects DGP",
                 pad=8)
    ax.set_ylim(0, max(values) * 1.30)
    fig.tight_layout()
    fig.savefig(HERE / "did-fig2-twfe-vs-cs.svg", format="svg")
    plt.close(fig)


def figure3_event_study():
    event_times = np.arange(-3, 5)
    true_path = np.where(event_times < 0, 0, np.minimum(event_times + 1, 3))
    naive_path = true_path.astype(float).copy()
    naive_path[event_times >= 0] *= 0.62
    naive_path[event_times >= 3] *= 0.55
    naive_path[event_times == -3] = -0.15
    naive_path[event_times == -2] = -0.22
    naive_path[event_times == -1] = -0.10
    robust_path = true_path.astype(float) + np.array(
        [0.02, -0.04, 0.03, 0.05, -0.03, 0.04, -0.02, 0.01]
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.axvspan(-0.5, 4.5, alpha=0.06, color=PALETTE["green"])
    ax.axvline(-0.5, color="#333", linestyle=":", linewidth=1)
    ax.text(-0.55, 2.95, "treatment\ndate", ha="right", fontsize=8.5,
            color="#555", style="italic")
    ax.plot(event_times, true_path, color=PALETTE["grey"], linestyle="--",
            linewidth=1.8, label="true dynamic effect", marker="o", markersize=6,
            markerfacecolor=PALETTE["grey"])
    ax.plot(event_times, naive_path, color=PALETTE["red"], linewidth=1.8,
            label="naive TWFE event study", marker="s", markersize=6)
    ax.plot(event_times, robust_path, color=PALETTE["blue"], linewidth=1.8,
            label="Sun–Abraham robust estimator", marker="D", markersize=6)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlabel("event time (relative to treatment)", fontsize=11)
    ax.set_ylabel("estimated dynamic effect", fontsize=11)
    ax.set_title("Event study: naive TWFE fabricates pre-trends, attenuates post-effects",
                 pad=8)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "did-fig3-event-study.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in [("bacon-decomp", figure1_bacon_decomp),
                     ("twfe-vs-cs", figure2_twfe_bias),
                     ("event-study", figure3_event_study)]:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.1f}s)")
    print(f"total: {time.time() - t0:.1f}s")
