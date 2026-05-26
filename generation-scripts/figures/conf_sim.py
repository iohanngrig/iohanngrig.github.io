"""
Conformal prediction figures.

Three figures:
    conf-fig1-split-conformal.svg     Split conformal procedure illustrated
    conf-fig2-marginal-vs-cond.svg    Marginal vs. conditional coverage example
    conf-fig3-cqr-widths.svg          Conformalized quantile regression interval widths
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


def figure1_split_conformal():
    """Illustrate split conformal on a regression example with a noisy 1d signal."""
    rng = np.random.default_rng(42)
    n = 1000
    x = rng.uniform(0, 10, n)
    y = np.sin(x) + 0.3 * x + rng.normal(0, 0.5 + 0.1 * x)

    # Split
    idx = rng.permutation(n)
    train_idx = idx[: n // 2]
    cal_idx = idx[n // 2 :]

    # Simple model: polynomial fit on train
    poly_coefs = np.polyfit(x[train_idx], y[train_idx], 3)
    mu_hat = np.poly1d(poly_coefs)

    # Nonconformity scores on calibration set
    scores = np.abs(y[cal_idx] - mu_hat(x[cal_idx]))
    alpha = 0.1
    n_cal = len(cal_idx)
    q_hat = np.quantile(scores, np.ceil((n_cal + 1) * (1 - alpha)) / n_cal)

    # Grid for plotting
    x_grid = np.linspace(0, 10, 200)
    pred = mu_hat(x_grid)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))
    # Left: raw data + fit
    ax1.scatter(x, y, s=3, color=PALETTE["grey"], alpha=0.4, label="data")
    ax1.plot(x_grid, pred, color=PALETTE["blue"], linewidth=1.8,
             label=r"fit $\hat\mu(x)$")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_title("Step 1: fit any predictor on the training fold")
    ax1.legend(frameon=False, loc="upper left", fontsize=9)

    # Right: prediction band
    ax2.scatter(x, y, s=3, color=PALETTE["grey"], alpha=0.4)
    ax2.fill_between(x_grid, pred - q_hat, pred + q_hat,
                     color=PALETTE["blue"], alpha=0.18,
                     label=rf"split-conformal 90% band")
    ax2.plot(x_grid, pred, color=PALETTE["blue"], linewidth=1.5)
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.set_title(f"Step 2: widen band by $\\hat q = {q_hat:.2f}$ (cal. quantile)")
    ax2.legend(frameon=False, loc="upper left", fontsize=9)

    fig.suptitle("Split conformal prediction: model-agnostic, distribution-free")
    fig.tight_layout()
    fig.savefig(HERE / "conf-fig1-split-conformal.svg", format="svg")
    plt.close(fig)


def figure2_marginal_vs_conditional():
    """Show that conformal coverage is marginal: one group can be under-covered
    even when overall coverage is at nominal."""
    rng = np.random.default_rng(7)

    # Simulate: two groups, one easy and one hard. Same band used for both.
    n_grp = 400
    y_easy = rng.normal(0, 0.5, n_grp)
    y_hard = rng.normal(0, 1.5, n_grp)
    # Naive band calibrated for marginal 90% coverage
    all_y = np.concatenate([y_easy, y_hard])
    band = np.quantile(np.abs(all_y - 0), 0.9)

    cov_easy = np.mean(np.abs(y_easy) <= band)
    cov_hard = np.mean(np.abs(y_hard) <= band)
    cov_marg = np.mean(np.abs(all_y) <= band)

    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    groups = ["easy group\n($\\sigma=0.5$)", "hard group\n($\\sigma=1.5$)",
              "marginal\n(both, pooled)"]
    values = [cov_easy, cov_hard, cov_marg]
    colors = [PALETTE["blue"], PALETTE["red"], PALETTE["green"]]
    bars = ax.bar(groups, values, color=colors, alpha=0.82, edgecolor="white",
                  linewidth=1.5)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01, f"{v * 100:.1f}%",
                ha="center", fontsize=10)
    ax.axhline(0.9, color="black", linestyle="--", linewidth=1, label="nominal 90%")
    ax.set_ylabel("empirical coverage of 90% band")
    ax.set_title("Marginal coverage guarantee does NOT imply conditional coverage")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, loc="lower right")
    fig.savefig(HERE / "conf-fig2-marginal-vs-cond.svg", format="svg")
    plt.close(fig)


def figure3_cqr_widths():
    """Compare split-conformal (fixed-width) vs. conformalized quantile regression
    (adaptive-width) on heteroscedastic 1D regression."""
    rng = np.random.default_rng(123)
    n = 1200
    x = rng.uniform(0, 10, n)
    sigma_x = 0.3 + 0.25 * x  # heteroscedastic noise
    y = np.sin(x) + 0.3 * x + rng.normal(0, sigma_x)

    idx = rng.permutation(n)
    train_idx = idx[: n // 2]
    cal_idx = idx[n // 2 :]

    # Method 1: split conformal with |residual| score
    poly_coefs = np.polyfit(x[train_idx], y[train_idx], 3)
    mu_hat = np.poly1d(poly_coefs)
    scores = np.abs(y[cal_idx] - mu_hat(x[cal_idx]))
    alpha = 0.1
    q_hat = np.quantile(scores, np.ceil((len(cal_idx) + 1) * (1 - alpha)) / len(cal_idx))

    # Method 2: CQR — fit quantile regressions q_{0.05}, q_{0.95}
    from sklearn.ensemble import GradientBoostingRegressor
    q_lo_model = GradientBoostingRegressor(loss="quantile", alpha=0.05,
                                           n_estimators=100, max_depth=3, random_state=0)
    q_hi_model = GradientBoostingRegressor(loss="quantile", alpha=0.95,
                                           n_estimators=100, max_depth=3, random_state=0)
    q_lo_model.fit(x[train_idx].reshape(-1, 1), y[train_idx])
    q_hi_model.fit(x[train_idx].reshape(-1, 1), y[train_idx])

    q_lo_cal = q_lo_model.predict(x[cal_idx].reshape(-1, 1))
    q_hi_cal = q_hi_model.predict(x[cal_idx].reshape(-1, 1))
    # CQR nonconformity score
    s_cqr = np.maximum(q_lo_cal - y[cal_idx], y[cal_idx] - q_hi_cal)
    q_hat_cqr = np.quantile(s_cqr, np.ceil((len(cal_idx) + 1) * (1 - alpha)) / len(cal_idx))

    x_grid = np.linspace(0, 10, 200)
    mu_g = mu_hat(x_grid)
    q_lo_g = q_lo_model.predict(x_grid.reshape(-1, 1))
    q_hi_g = q_hi_model.predict(x_grid.reshape(-1, 1))

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(x, y, s=3, color=PALETTE["grey"], alpha=0.35, label="data")
    ax.fill_between(x_grid, mu_g - q_hat, mu_g + q_hat,
                    color=PALETTE["red"], alpha=0.14,
                    label="split conformal (fixed width)")
    ax.fill_between(x_grid, q_lo_g - q_hat_cqr, q_hi_g + q_hat_cqr,
                    color=PALETTE["blue"], alpha=0.18,
                    label="CQR (adaptive width)")
    ax.plot(x_grid, mu_g, color=PALETTE["red"], linewidth=1.2, linestyle="--")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("CQR adapts to heteroscedasticity; split conformal does not")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    fig.savefig(HERE / "conf-fig3-cqr-widths.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in [("split-conformal", figure1_split_conformal),
                     ("marginal-vs-cond", figure2_marginal_vs_conditional),
                     ("cqr-widths", figure3_cqr_widths)]:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.1f}s)")
    print(f"total: {time.time() - t0:.1f}s")
