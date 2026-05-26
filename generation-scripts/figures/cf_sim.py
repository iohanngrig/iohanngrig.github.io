"""
Causal forests simulation — upgraded style, April 2026.
"""
import sys
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()

RNG_SEED = 42
N_JOBS = -1


def tau_true(x0):
    return 2.0 / (1.0 + np.exp(-3.0 * x0)) - 1.0


def dgp(n, rng, p=5):
    X = rng.normal(size=(n, p))
    g0 = 0.5 * X[:, 1] + 0.3 * X[:, 2] ** 2
    D = rng.binomial(1, 0.5, size=n)
    eps = rng.normal(scale=0.5, size=n)
    Y = g0 + D * tau_true(X[:, 0]) + eps
    return X, D, Y


def fit_cate_forest(X, D, Y, honest=True, n_trees=200, seed=0):
    rng = np.random.default_rng(seed)
    n = len(Y)
    if honest:
        idx_split = rng.permutation(n)
        half = n // 2
        est_idx = idx_split[half:]
        rf1 = RandomForestRegressor(n_estimators=n_trees, min_samples_leaf=10,
                                    random_state=seed, n_jobs=N_JOBS)
        rf0 = RandomForestRegressor(n_estimators=n_trees, min_samples_leaf=10,
                                    random_state=seed + 1, n_jobs=N_JOBS)
        t_idx = est_idx[D[est_idx] == 1]
        c_idx = est_idx[D[est_idx] == 0]
        rf1.fit(X[t_idx], Y[t_idx])
        rf0.fit(X[c_idx], Y[c_idx])
    else:
        rf1 = RandomForestRegressor(n_estimators=n_trees, min_samples_leaf=10,
                                    random_state=seed, n_jobs=N_JOBS)
        rf0 = RandomForestRegressor(n_estimators=n_trees, min_samples_leaf=10,
                                    random_state=seed + 1, n_jobs=N_JOBS)
        rf1.fit(X[D == 1], Y[D == 1])
        rf0.fit(X[D == 0], Y[D == 0])
    return rf1, rf0


def tau_forest(rf1, rf0, X_new):
    return rf1.predict(X_new) - rf0.predict(X_new)


def bootstrap_ci(X, D, Y, X_eval, honest, n_boot=30, seed=0):
    n = len(Y)
    rng = np.random.default_rng(seed)
    preds = np.zeros((n_boot, len(X_eval)))
    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        rf1, rf0 = fit_cate_forest(X[idx], D[idx], Y[idx],
                                   honest=honest, n_trees=50, seed=seed + b)
        preds[b] = tau_forest(rf1, rf0, X_eval)
    return preds.mean(axis=0), np.quantile(preds, 0.025, axis=0), np.quantile(preds, 0.975, axis=0)


def figure1_cate_surface():
    rng = np.random.default_rng(RNG_SEED)
    X, D, Y = dgp(n=3000, rng=rng)
    x0_grid = np.linspace(-2.5, 2.5, 60)
    X_eval = np.zeros((len(x0_grid), 5))
    X_eval[:, 0] = x0_grid
    rf1, rf0 = fit_cate_forest(X, D, Y, honest=True, seed=0)
    tau_hat = tau_forest(rf1, rf0, X_eval)

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.plot(x0_grid, tau_true(x0_grid), color=PALETTE["grey"],
            linestyle="--", linewidth=2.0, label=r"true $\tau(x_1)$")
    ax.plot(x0_grid, tau_hat, color=PALETTE["blue"], linewidth=2.2,
            label=r"honest forest $\hat\tau(x_1)$")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.fill_between(x0_grid, np.minimum(tau_true(x0_grid), tau_hat),
                    np.maximum(tau_true(x0_grid), tau_hat),
                    color=PALETTE["blue"], alpha=0.09)
    ax.set_xlabel(r"covariate  $x_1$", fontsize=11)
    ax.set_ylabel(r"treatment effect  $\tau(x_1)$", fontsize=11)
    ax.set_title("Heterogeneous treatment effect recovery  ($n = 3000$)", pad=8)
    ax.legend(loc="upper left", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(HERE / "cf-fig1-cate-surface.svg", format="svg")
    plt.close(fig)


def figure2_coverage():
    x0_eval = np.array([-1.5, -0.5, 0.0, 0.5, 1.5])
    X_eval = np.zeros((len(x0_eval), 5))
    X_eval[:, 0] = x0_eval
    tau_vals = tau_true(x0_eval)
    n_reps = 30
    cov_honest = np.zeros(len(x0_eval))
    cov_adaptive = np.zeros(len(x0_eval))
    for r in range(n_reps):
        rng = np.random.default_rng(RNG_SEED + 100 * r)
        X, D, Y = dgp(n=2000, rng=rng)
        _, lo_h, hi_h = bootstrap_ci(X, D, Y, X_eval, honest=True, n_boot=20, seed=r)
        _, lo_a, hi_a = bootstrap_ci(X, D, Y, X_eval, honest=False, n_boot=20, seed=r)
        cov_honest += (lo_h <= tau_vals) & (tau_vals <= hi_h)
        cov_adaptive += (lo_a <= tau_vals) & (tau_vals <= hi_a)
    cov_honest /= n_reps
    cov_adaptive /= n_reps

    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    width = 0.30
    x_pos = np.arange(len(x0_eval))
    ax.axhspan(0.925, 0.975, color=PALETTE["green"], alpha=0.10)
    bars_h = ax.bar(x_pos - width / 2, cov_honest, width, color=PALETTE["blue"],
                    label="honest-split forest", alpha=0.86, edgecolor="white", linewidth=1.2)
    bars_a = ax.bar(x_pos + width / 2, cov_adaptive, width, color=PALETTE["red"],
                    label="adaptive (in-sample) forest", alpha=0.86, edgecolor="white", linewidth=1.2)
    ax.axhline(0.95, color=PALETTE["green"], linestyle="--", linewidth=1, label="nominal 95%")
    for bars in [bars_h, bars_a]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                    f"{bar.get_height() * 100:.0f}%", ha="center", fontsize=8.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"$x_1 = {v}$" for v in x0_eval], fontsize=9.5)
    ax.set_ylabel("empirical 95% CI coverage", fontsize=11)
    ax.set_title(f"Pointwise coverage: honest splitting restores validity  "
                 f"($n=2000$, {n_reps} reps)", pad=8)
    ax.set_ylim(0.35, 1.06)
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "cf-fig2-coverage.svg", format="svg")
    plt.close(fig)


def figure3_honest_split_diagram():
    fig, ax = plt.subplots(figsize=(8.8, 3.8))
    ax.axis("off")
    boxes = [
        (0.7, 2.0, "Full subsample\n(bootstrap draw)", PALETTE["grey"]),
        (3.4, 3.0, "Split half  $\\mathcal{I}$:\nchoose tree splits", PALETTE["orange"]),
        (3.4, 1.0, "Split half  $\\mathcal{J}$:\ncompute leaf means", PALETTE["blue"]),
        (6.4, 2.0, "Honest tree:\nstructure from  $\\mathcal{I}$\nvalues from  $\\mathcal{J}$", PALETTE["green"]),
    ]
    for (x, y, text, col) in boxes:
        ax.annotate(text, xy=(x, y), xycoords="data",
                    ha="center", va="center", fontsize=10.5,
                    bbox=dict(boxstyle="round,pad=0.55", facecolor=col,
                              alpha=0.18, edgecolor=col, linewidth=1.6))
    def arr(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color="#444", lw=1.3))
    arr(1.55, 2.12, 2.6, 2.92)
    arr(1.55, 1.88, 2.6, 1.08)
    arr(4.2, 2.9, 5.55, 2.15)
    arr(4.2, 1.1, 5.55, 1.85)
    ax.set_xlim(0, 7.8)
    ax.set_ylim(0, 4.2)
    ax.set_title("Honest-tree construction  (Wager & Athey 2018)", fontsize=12, pad=10)
    fig.tight_layout()
    fig.savefig(HERE / "cf-fig3-honest-split.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in [("CATE surface", figure1_cate_surface),
                     ("coverage", figure2_coverage),
                     ("honest-split diagram", figure3_honest_split_diagram)]:
        t = time.time()
        print(f"figure {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time() - t:.1f}s)")
    print(f"total: {time.time() - t0:.1f}s")
