"""
QTE figures — analytical, no MC needed.

Three figures:
    qte-fig1-two-qtes.svg       Conditional vs. unconditional QTE visualization
    qte-fig2-rif-decomp.svg     RIF regression illustrated on a small example
    qte-fig3-panel-pitfall.svg  Conditional-on-FE vs cross-sectional quantile groups
"""
import sys
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()


def figure1_two_qtes():
    """Show the distinction between conditional QTEs and the unconditional QTE."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    y = np.linspace(-2, 6, 400)

    # Left panel: conditional QTEs at two X values
    from scipy.stats import norm
    f_ctrl_x1 = norm.pdf(y, loc=1.0, scale=0.8)
    f_treat_x1 = norm.pdf(y, loc=1.5, scale=0.8)  # +0.5 at x1
    f_ctrl_x2 = norm.pdf(y, loc=3.0, scale=0.8)
    f_treat_x2 = norm.pdf(y, loc=4.2, scale=0.8)  # +1.2 at x2

    ax[0].fill_between(y, 0, f_ctrl_x1, color=PALETTE["grey"], alpha=0.3,
                       label=r"$f_{Y(0) \mid X = x_1}$")
    ax[0].fill_between(y, 0, f_treat_x1, color=PALETTE["blue"], alpha=0.3,
                       label=r"$f_{Y(1) \mid X = x_1}$")
    ax[0].fill_between(y, 0, f_ctrl_x2, color=PALETTE["grey"], alpha=0.3)
    ax[0].fill_between(y, 0, f_treat_x2, color=PALETTE["orange"], alpha=0.3,
                       label=r"$f_{Y(1) \mid X = x_2}$")
    ax[0].annotate("", xy=(1.5, 0.46), xytext=(1.0, 0.46),
                   arrowprops=dict(arrowstyle="->", color=PALETTE["blue"], lw=1.5))
    ax[0].text(1.25, 0.52, r"$\mathrm{QTE}_{0.5}(x_1) = 0.5$",
               ha="center", color=PALETTE["blue"], fontsize=9)
    ax[0].annotate("", xy=(4.2, 0.46), xytext=(3.0, 0.46),
                   arrowprops=dict(arrowstyle="->", color=PALETTE["orange"], lw=1.5))
    ax[0].text(3.6, 0.52, r"$\mathrm{QTE}_{0.5}(x_2) = 1.2$",
               ha="center", color=PALETTE["orange"], fontsize=9)
    ax[0].set_title("Conditional QTEs at two values of $X$")
    ax[0].legend(frameon=False, loc="upper right", fontsize=8)
    ax[0].set_xlabel(r"$Y$")
    ax[0].set_ylabel("density")

    # Right panel: unconditional (marginalized)
    f_ctrl = 0.5 * norm.pdf(y, 1.0, 0.8) + 0.5 * norm.pdf(y, 3.0, 0.8)
    f_treat = 0.5 * norm.pdf(y, 1.5, 0.8) + 0.5 * norm.pdf(y, 4.2, 0.8)
    ax[1].fill_between(y, 0, f_ctrl, color=PALETTE["grey"], alpha=0.5,
                       label=r"$f_{Y(0)}$  (marginal)")
    ax[1].fill_between(y, 0, f_treat, color=PALETTE["blue"], alpha=0.5,
                       label=r"$f_{Y(1)}$  (marginal)")
    # Compute medians numerically
    F_ctrl = np.cumsum(f_ctrl); F_ctrl /= F_ctrl[-1]
    F_treat = np.cumsum(f_treat); F_treat /= F_treat[-1]
    q50_ctrl = y[np.searchsorted(F_ctrl, 0.5)]
    q50_treat = y[np.searchsorted(F_treat, 0.5)]
    qte_uncond = q50_treat - q50_ctrl
    ax[1].axvline(q50_ctrl, color=PALETTE["grey"], linestyle="--", alpha=0.7)
    ax[1].axvline(q50_treat, color=PALETTE["blue"], linestyle="--", alpha=0.7)
    ax[1].annotate("", xy=(q50_treat, 0.22), xytext=(q50_ctrl, 0.22),
                   arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax[1].text((q50_ctrl + q50_treat) / 2, 0.24,
               rf"$\mathrm{{QTE}}_{{0.5}} = {qte_uncond:.2f}$  (unconditional)",
               ha="center", fontsize=9)
    ax[1].set_title("Unconditional QTE $\\ne$ average of conditional QTEs")
    ax[1].legend(frameon=False, loc="upper right", fontsize=8)
    ax[1].set_xlabel(r"$Y$")

    fig.suptitle("Two quantile treatment effects, both at $\\tau = 0.5$")
    fig.tight_layout()
    fig.savefig(HERE / "qte-fig1-two-qtes.svg", format="svg")
    plt.close(fig)


def figure2_rif_decomp():
    """RIF visualization: how the influence function works for the tau-th quantile."""
    from scipy.stats import norm
    tau = 0.75
    y = np.linspace(-3, 5, 500)
    f = norm.pdf(y, loc=1.0, scale=1.2)
    F = norm.cdf(y, loc=1.0, scale=1.2)
    q_tau = norm.ppf(tau, loc=1.0, scale=1.2)
    f_at_q = norm.pdf(q_tau, loc=1.0, scale=1.2)

    # RIF(y; q_tau) = q_tau + (tau - 1{y <= q_tau}) / f(q_tau)
    rif = q_tau + (tau - (y <= q_tau).astype(float)) / f_at_q

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 5.5), sharex=True)

    # Top: density + quantile
    ax1.fill_between(y, 0, f, color=PALETTE["blue"], alpha=0.25,
                     label=r"$f_Y(y)$")
    ax1.axvline(q_tau, color=PALETTE["red"], linestyle="--", linewidth=1.2,
                label=rf"$q_\tau = {q_tau:.2f}$ ($\tau = {tau}$)")
    ax1.set_ylabel("density")
    ax1.legend(frameon=False, loc="upper left", fontsize=9)
    ax1.set_title("RIF = recentered influence function of the $\\tau$-th quantile")

    # Bottom: RIF
    ax2.plot(y, rif, color=PALETTE["green"], linewidth=1.8,
             label=r"$\mathrm{RIF}(y; q_\tau)$")
    ax2.axhline(q_tau, color=PALETTE["red"], linestyle="--", linewidth=1.2,
                label=rf"$q_\tau$ (= $\mathbb{{E}}[\mathrm{{RIF}}]$)")
    ax2.axvline(q_tau, color=PALETTE["red"], linestyle=":", linewidth=0.8)
    ax2.set_xlabel(r"$y$")
    ax2.set_ylabel(r"$\mathrm{RIF}(y; q_\tau)$")
    ax2.legend(frameon=False, loc="upper left", fontsize=9)

    fig.tight_layout()
    fig.savefig(HERE / "qte-fig2-rif-decomp.svg", format="svg")
    plt.close(fig)


def figure3_panel_pitfall():
    """Show how conditioning on unit fixed effects changes the subgroup definition."""
    rng = np.random.default_rng(42)
    n_units = 40
    alpha = rng.normal(0, 1.5, n_units)  # unit FEs
    t = np.arange(5)
    data = []
    for i in range(n_units):
        for t_ in t:
            Y = alpha[i] + 0.2 * t_ + rng.normal(0, 0.3)
            data.append((i, t_, alpha[i], Y))
    import pandas as pd
    df = pd.DataFrame(data, columns=["unit", "t", "alpha", "Y"])
    df["Y_wi"] = df.groupby("unit")["Y"].transform(lambda x: x - x.mean())

    # Top-quartile by raw Y
    q_raw = df["Y"].quantile(0.75)
    df["top_raw"] = df["Y"] >= q_raw
    # Top-quartile by residualized Y
    q_wi = df["Y_wi"].quantile(0.75)
    df["top_wi"] = df["Y_wi"] >= q_wi

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.3))

    # Left: raw Y, top quartile highlighted
    for _, row in df.iterrows():
        c = PALETTE["red"] if row["top_raw"] else PALETTE["grey"]
        axes[0].plot(row["t"], row["Y"], "o", color=c, markersize=4, alpha=0.7)
    axes[0].axhline(q_raw, color="black", linestyle="--", linewidth=1,
                    label=f"top-quartile cutoff (raw): {q_raw:.2f}")
    axes[0].set_title("Top-quartile group by raw $Y$")
    axes[0].set_xlabel("time")
    axes[0].set_ylabel("$Y$")
    axes[0].legend(frameon=False, loc="lower right", fontsize=9)

    # Right: within-transformed Y
    for _, row in df.iterrows():
        c = PALETTE["blue"] if row["top_wi"] else PALETTE["grey"]
        axes[1].plot(row["t"], row["Y_wi"], "o", color=c, markersize=4, alpha=0.7)
    axes[1].axhline(q_wi, color="black", linestyle="--", linewidth=1,
                    label=f"top-quartile cutoff (within): {q_wi:.2f}")
    axes[1].set_title("Top-quartile group by within-transformed $Y - \\bar Y_i$")
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("$Y - \\bar Y_i$")
    axes[1].legend(frameon=False, loc="lower right", fontsize=9)

    fig.suptitle("Panel-data pitfall: conditional QTE targets a different "
                 "subpopulation than the unconditional QTE")
    fig.tight_layout()
    fig.savefig(HERE / "qte-fig3-panel-pitfall.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in [("two-qtes", figure1_two_qtes),
                     ("rif-decomp", figure2_rif_decomp),
                     ("panel-pitfall", figure3_panel_pitfall)]:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.1f}s)")
    print(f"total: {time.time() - t0:.1f}s")
