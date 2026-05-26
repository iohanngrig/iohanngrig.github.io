"""
Monte Carlo simulation: compare 4 estimators of the treatment effect theta_0
in a partially linear model Y = theta * D + g(X) + U, D = m(X) + V.

Figures (upgraded April 2026):
    dml-fig1-rate-vs-n.svg      log-log bias vs. sample size with annotations
    dml-fig2-sampling-dist.svg  4-panel histograms with bias/SE annotations
    dml-fig3-coverage.svg       95% CI coverage + reference band
"""
import sys
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()

THETA_0 = 1.0
N_ESTIMATORS = 50
N_JOBS = -1


def dgp(n, rng, p=10):
    X = rng.normal(size=(n, p))
    g = np.sin(X[:, 0]) + 0.5 * X[:, 1] ** 2 + X[:, 2]
    m = 0.5 * X[:, 0] + 0.3 * np.tanh(X[:, 3])
    V = rng.normal(scale=0.5, size=n)
    D = m + V
    U = rng.normal(scale=1.0, size=n)
    Y = THETA_0 * D + g + U
    return X, D, Y


def rf(seed):
    return RandomForestRegressor(
        n_estimators=N_ESTIMATORS, min_samples_leaf=5,
        random_state=seed, n_jobs=N_JOBS,
    )


def est_ols(X, D, Y):
    A = np.column_stack([D, np.ones_like(D)])
    return float(np.linalg.lstsq(A, Y, rcond=None)[0][0])


def est_plugin_rf(X, D, Y):
    g_hat = rf(0).fit(X, Y).predict(X)
    resid = Y - g_hat
    return float(np.mean(resid * D) / np.mean(D ** 2))


def est_dml(X, D, Y, k_folds=1):
    n = len(Y)
    if k_folds == 1:
        l_hat = rf(0).fit(X, Y).predict(X)
        m_hat = rf(1).fit(X, D).predict(X)
    else:
        l_hat = np.zeros(n)
        m_hat = np.zeros(n)
        for tr, te in KFold(n_splits=k_folds, shuffle=True, random_state=0).split(X):
            l_hat[te] = rf(0).fit(X[tr], Y[tr]).predict(X[te])
            m_hat[te] = rf(1).fit(X[tr], D[tr]).predict(X[te])
    U_hat = Y - l_hat
    V_hat = D - m_hat
    theta = float(np.mean(V_hat * U_hat) / np.mean(V_hat ** 2))
    psi = V_hat * (U_hat - theta * V_hat)
    se = float(np.sqrt(np.mean(psi ** 2) / np.mean(V_hat ** 2) ** 2 / n))
    return theta, se


def mc_run(n, reps, seed_base):
    out = {k: [] for k in ["ols", "plugin", "dml_nocf", "dml_cf"]}
    ci_nocf, ci_cf = [], []
    for r in range(reps):
        rng = np.random.default_rng(seed_base + r)
        X, D, Y = dgp(n, rng)
        out["ols"].append(est_ols(X, D, Y))
        out["plugin"].append(est_plugin_rf(X, D, Y))
        t_nocf, se_nocf = est_dml(X, D, Y, k_folds=1)
        out["dml_nocf"].append(t_nocf)
        ci_nocf.append((t_nocf - 1.96 * se_nocf, t_nocf + 1.96 * se_nocf))
        t_cf, se_cf = est_dml(X, D, Y, k_folds=5)
        out["dml_cf"].append(t_cf)
        ci_cf.append((t_cf - 1.96 * se_cf, t_cf + 1.96 * se_cf))
    return out, ci_nocf, ci_cf


def figure1(ns, bias_dict):
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    labels = {
        "ols": ("OLS (misspecified)", PALETTE["grey"], "-", "o"),
        "plugin": ("Plug-in RF", PALETTE["orange"], "--", "s"),
        "dml_nocf": ("DML (no cross-fit)", PALETTE["red"], "-.", "^"),
        "dml_cf": ("DML + 5-fold cross-fit", PALETTE["blue"], "-", "D"),
    }
    for k, (lbl, col, ls, mk) in labels.items():
        ax.loglog(ns, bias_dict[k], ls, color=col, marker=mk, label=lbl,
                  linewidth=1.8, markersize=6)
    # Reference line for parametric n^{-1/2} rate
    ns_arr = np.array(ns, dtype=float)
    ref = 0.5 / np.sqrt(ns_arr)  # scaled so it sits near dml_cf
    ax.loglog(ns_arr, ref, ":", color="#888", linewidth=1.0, alpha=0.9,
              label=r"parametric $n^{-1/2}$ reference")
    ax.set_xlabel("Sample size  $n$", fontsize=11)
    ax.set_ylabel(r"$|\hat\theta - \theta_0|$  (mean absolute bias)", fontsize=11)
    ax.set_title("Bias vs. sample size — only DML + cross-fit matches the parametric rate",
                 pad=8)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "dml-fig1-rate-vs-n.svg", format="svg")
    plt.close(fig)


def figure2(results_n2000):
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 6), sharex=True, sharey=True)
    labels = [
        ("ols", "OLS (misspecified)", PALETTE["grey"]),
        ("plugin", "Plug-in RF", PALETTE["orange"]),
        ("dml_nocf", "DML (no cross-fit)", PALETTE["red"]),
        ("dml_cf", "DML + 5-fold cross-fit", PALETTE["blue"]),
    ]
    for ax, (k, lbl, col) in zip(axes.flat, labels):
        vals = np.array(results_n2000[k])
        bias = np.mean(vals) - THETA_0
        se = np.std(vals)
        ax.hist(vals, bins=32, color=col, alpha=0.78,
                edgecolor="white", linewidth=0.6)
        ax.axvline(THETA_0, color="black", linestyle="--", linewidth=1.1, alpha=0.8)
        ax.axvline(np.mean(vals), color=col, linestyle="-", linewidth=1.6)
        ax.text(0.03, 0.95,
                f"bias = {bias:+.3f}\nSE = {se:.3f}",
                transform=ax.transAxes, fontsize=9, va="top",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="#bbb", linewidth=0.6, alpha=0.85))
        ax.set_title(lbl, fontsize=10.5)
    # Axis labels on outer plots only
    for ax in axes[-1, :]:
        ax.set_xlabel(r"$\hat\theta$", fontsize=11)
    for ax in axes[:, 0]:
        ax.set_ylabel("count", fontsize=11)
    fig.suptitle(r"Sampling distribution of $\hat\theta$  "
                 rf"($n = 2000$, $\theta_0 = 1$, 300 MC replications)",
                 fontsize=12.5, y=1.01, fontweight="semibold")
    fig.text(0.5, 0.965,
             "dashed line = true parameter; colored line = MC mean",
             ha="center", fontsize=9, style="italic", color="#555")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(HERE / "dml-fig2-sampling-dist.svg", format="svg")
    plt.close(fig)


def figure3(ns, cov_nocf, cov_cf):
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    # Nominal band ±5% tolerance
    ax.axhspan(0.925, 0.975, color=PALETTE["green"], alpha=0.10)
    ax.axhline(0.95, color=PALETTE["green"], linestyle="--", linewidth=1,
               label="nominal 95%")
    ax.plot(ns, cov_nocf, "-^", color=PALETTE["red"],
            label="DML (no cross-fit)", linewidth=1.8, markersize=7)
    ax.plot(ns, cov_cf, "-D", color=PALETTE["blue"],
            label="DML + 5-fold cross-fit", linewidth=1.8, markersize=7)
    for xi, yi in zip(ns, cov_cf):
        ax.annotate(f"{yi * 100:.0f}%", (xi, yi), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=8,
                    color=PALETTE["blue"])
    for xi, yi in zip(ns, cov_nocf):
        ax.annotate(f"{yi * 100:.0f}%", (xi, yi), xytext=(0, -14),
                    textcoords="offset points", ha="center", fontsize=8,
                    color=PALETTE["red"])
    ax.set_xlabel("Sample size  $n$", fontsize=11)
    ax.set_ylabel("empirical 95% CI coverage", fontsize=11)
    ax.set_title("CI coverage: honesty requires cross-fitting", pad=8)
    ax.set_ylim(0.52, 1.02)
    ax.set_xscale("log")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "dml-fig3-coverage.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    NS = [250, 500, 1000, 2000, 4000]
    REPS = {250: 60, 500: 60, 1000: 60, 2000: 300, 4000: 60}
    bias = {k: [] for k in ["ols", "plugin", "dml_nocf", "dml_cf"]}
    cov_nocf_list, cov_cf_list = [], []
    results_n2000 = None

    for n in NS:
        reps = REPS[n]
        print(f"n={n} reps={reps} ...", end="", flush=True)
        t = time.time()
        results, ci_nocf, ci_cf = mc_run(n, reps, seed_base=1000 + n)
        for k in bias:
            bias[k].append(abs(np.mean(results[k]) - THETA_0))
        cov_nocf_list.append(sum(1 for lo, hi in ci_nocf if lo <= THETA_0 <= hi) / reps)
        cov_cf_list.append(sum(1 for lo, hi in ci_cf if lo <= THETA_0 <= hi) / reps)
        if n == 2000:
            results_n2000 = results
        print(f" done ({time.time() - t:.1f}s)")

    print("rendering figures ...")
    figure1(NS, bias)
    figure2(results_n2000)
    figure3(NS, cov_nocf_list, cov_cf_list)
    print(f"total: {time.time() - t0:.0f}s")
