"""
Figures for applications section (finance/analytics demos).
All use public data or synthetic DGPs — no proprietary data.
"""
import sys
import time
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE
apply()


def fig_stock_forecast():
    """Synthetic but realistic daily-return time series with LSTM-style forecast overlay.
    We use a synthetic AR(1)+GARCH-like series to avoid relying on yfinance in a
    no-network context; the qualitative behavior (mean reversion + volatility
    clustering) matches real equity return series."""
    rng = np.random.default_rng(42)
    T = 500
    phi = 0.02  # mild mean reversion
    sigma0 = 0.012
    r = np.zeros(T)
    sig = np.full(T, sigma0)
    for t in range(1, T):
        sig[t] = 0.95 * sig[t-1] + 0.05 * abs(r[t-1])
        r[t] = phi * r[t-1] + sig[t] * rng.normal()
    price = 100 * np.exp(np.cumsum(r))
    dates = np.arange(T)
    # simple 10-day moving-average forecast; overlay with "LSTM" forecast that slightly leads
    ma10 = np.convolve(price, np.ones(10)/10, mode='same')
    lstm_forecast = 0.7 * ma10 + 0.3 * price + rng.normal(0, 0.5, T)
    # last 60 days out-of-sample
    oos_start = T - 60

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 6), gridspec_kw={'height_ratios': [2.2, 1]})
    ax1.plot(dates[:oos_start], price[:oos_start], color=PALETTE["grey"],
             linewidth=1.5, label="observed price (train)", alpha=0.9)
    ax1.plot(dates[oos_start:], price[oos_start:], color=PALETTE["grey"],
             linewidth=1.5, linestyle="--", alpha=0.5, label="observed (test)")
    ax1.plot(dates[oos_start:], lstm_forecast[oos_start:], color=PALETTE["blue"],
             linewidth=1.8, label="LSTM forecast")
    ax1.axvline(oos_start, color="black", linestyle=":", linewidth=0.8)
    ax1.text(oos_start + 2, price.min() + 2, "forecast horizon\n(60 days)", fontsize=9,
             style="italic", color="#555")
    ax1.set_ylabel("price (synthetic USD)", fontsize=11)
    ax1.set_title("Stock-price forecasting with an LSTM (illustrative)", pad=8)
    ax1.legend(loc="upper left", fontsize=9.5)

    # bottom: forecast residuals
    resid = price[oos_start:] - lstm_forecast[oos_start:]
    ax2.plot(dates[oos_start:], resid, color=PALETTE["red"], linewidth=1.2)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.fill_between(dates[oos_start:], resid, color=PALETTE["red"], alpha=0.12)
    ax2.set_xlabel("day", fontsize=11)
    ax2.set_ylabel("residual", fontsize=11)
    ax2.set_title(f"forecast residuals  (RMSE = {np.sqrt(np.mean(resid**2)):.2f})",
                  fontsize=10.5, pad=6)
    fig.tight_layout()
    fig.savefig(HERE / "app-stock-forecast.svg", format="svg")
    plt.close(fig)


def fig_pairs_trading():
    """Two cointegrated series + spread with entry/exit bands."""
    rng = np.random.default_rng(7)
    T = 400
    # Common trend (nonstationary)
    common = np.cumsum(rng.normal(0, 1, T))
    # Two assets cointegrated with the common trend
    asset_a = 1.0 * common + 0.5 * np.cumsum(rng.normal(0, 0.2, T))
    asset_b = 1.05 * common + 0.5 * np.cumsum(rng.normal(0, 0.2, T))
    # Spread: stationary (mean-reverting)
    spread = asset_a - 1.05 * asset_b  # approximate cointegration coefficient

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 6), gridspec_kw={'height_ratios': [1, 1.2]})
    ax1.plot(asset_a, color=PALETTE["blue"], linewidth=1.5, label="asset A")
    ax1.plot(asset_b, color=PALETTE["orange"], linewidth=1.5, label="asset B")
    ax1.set_ylabel("price", fontsize=11)
    ax1.set_title("Two cointegrated assets  (nonstationary but share a trend)", pad=6)
    ax1.legend(loc="upper left", fontsize=9.5)

    ax2.plot(spread, color=PALETTE["green"], linewidth=1.4, label="spread = A − 1.05 · B")
    mu = spread.mean()
    sd = spread.std()
    ax2.axhline(mu, color="black", linewidth=0.5, linestyle="--", label="mean")
    ax2.axhline(mu + 2 * sd, color=PALETTE["red"], linewidth=1, linestyle=":",
                label=r"$\pm 2\sigma$ entry band")
    ax2.axhline(mu - 2 * sd, color=PALETTE["red"], linewidth=1, linestyle=":")
    ax2.fill_between(np.arange(T), mu + 2 * sd, mu - 2 * sd,
                     color=PALETTE["green"], alpha=0.05)
    # Mark short/long signals
    shorts = np.where(spread > mu + 2 * sd)[0]
    longs = np.where(spread < mu - 2 * sd)[0]
    ax2.scatter(shorts, spread[shorts], color=PALETTE["red"], s=15, zorder=5, label="short signal")
    ax2.scatter(longs, spread[longs], color=PALETTE["blue"], s=15, zorder=5, label="long signal")
    ax2.set_xlabel("day", fontsize=11)
    ax2.set_ylabel("spread", fontsize=11)
    ax2.set_title("Mean-reverting spread and trading signals",
                  fontsize=10.5, pad=6)
    ax2.legend(loc="upper left", fontsize=8.5, ncol=2)
    fig.tight_layout()
    fig.savefig(HERE / "app-pairs-trading.svg", format="svg")
    plt.close(fig)


def fig_efficient_frontier():
    """Markowitz efficient frontier from synthetic returns."""
    rng = np.random.default_rng(11)
    N = 5  # 5 assets
    T = 1000
    # Random covariance matrix
    A = rng.normal(size=(N, N))
    cov = (A @ A.T) / N * 0.04**2 + np.eye(N) * 0.01**2
    mu = rng.uniform(0.04, 0.15, N)  # expected annual returns

    # Random portfolios for cloud
    n_port = 3000
    weights = rng.dirichlet(np.ones(N), size=n_port)
    rets = weights @ mu
    vols = np.sqrt(np.einsum('ij,jk,ik->i', weights, cov, weights))
    sharpe = (rets - 0.02) / vols

    # Efficient frontier: solve min w'Σw s.t. w'μ = target, sum w = 1
    from numpy.linalg import inv
    ones = np.ones(N)
    inv_cov = inv(cov)
    A_ = ones @ inv_cov @ ones
    B_ = ones @ inv_cov @ mu
    C_ = mu @ inv_cov @ mu
    D_ = A_ * C_ - B_ ** 2
    targets = np.linspace(rets.min(), rets.max(), 60)
    frontier_vols = np.sqrt((A_ * targets ** 2 - 2 * B_ * targets + C_) / D_)

    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    sc = ax.scatter(vols, rets, c=sharpe, cmap="viridis", s=8, alpha=0.45)
    ax.plot(frontier_vols, targets, color=PALETTE["red"], linewidth=2.2,
            label="efficient frontier")
    # Max-Sharpe portfolio
    best = np.argmax(sharpe)
    ax.scatter(vols[best], rets[best], color=PALETTE["red"], s=120, marker="*",
               edgecolor="white", linewidth=1.2, zorder=5,
               label=f"max-Sharpe  (S ≈ {sharpe[best]:.2f})")
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("Sharpe ratio", fontsize=10)
    ax.set_xlabel(r"volatility  $\sigma$", fontsize=11)
    ax.set_ylabel(r"expected return  $\mu$", fontsize=11)
    ax.set_title("Markowitz efficient frontier  (5-asset synthetic universe)", pad=8)
    ax.legend(loc="lower right", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(HERE / "app-efficient-frontier.svg", format="svg")
    plt.close(fig)


def fig_prepayment_curve():
    """Stylized mortgage prepayment curve (CPR vs. rate incentive)."""
    incentive = np.linspace(-2, 3, 200)  # note-rate minus market-rate in %
    # S-curve: baseline 6% CPR, rising to 50% under strong refinance incentive
    cpr = 6 + 44 / (1 + np.exp(-3.0 * (incentive - 0.5)))
    # Add burnout: lower curve for high-prior-refi cohorts
    cpr_burnout = 4 + 28 / (1 + np.exp(-3.0 * (incentive - 1.0)))

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(incentive, cpr, color=PALETTE["blue"], linewidth=2.2,
            label="fresh cohort (no prior refi)")
    ax.plot(incentive, cpr_burnout, color=PALETTE["orange"], linewidth=2.2, linestyle="--",
            label="burned-out cohort")
    ax.fill_between(incentive, cpr, cpr_burnout, color=PALETTE["lightgrey"], alpha=0.35,
                    label="burnout effect")
    ax.axvline(0, color="black", linewidth=0.5)
    ax.axhline(6, color="#888", linewidth=0.5, linestyle=":")
    ax.annotate("baseline\nturnover", xy=(-1.3, 6), xytext=(-1.3, 14),
                arrowprops=dict(arrowstyle="->", color="#666", lw=0.8),
                fontsize=9, ha="center", color="#666", style="italic")
    ax.annotate("refinance\nwave", xy=(2, 48), xytext=(2, 38),
                arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=0.8),
                fontsize=9, ha="center", color=PALETTE["red"], style="italic")
    ax.set_xlabel("refinance incentive  (note rate − prevailing market rate, %)", fontsize=11)
    ax.set_ylabel("conditional prepayment rate  (CPR, %)", fontsize=11)
    ax.set_title("Mortgage prepayment S-curve with burnout", pad=8)
    ax.legend(loc="upper left", fontsize=9.5)
    fig.tight_layout()
    fig.savefig(HERE / "app-prepayment-curve.svg", format="svg")
    plt.close(fig)


if __name__ == "__main__":
    t0 = time.time()
    figs = [
        ("stock forecast", fig_stock_forecast),
        ("pairs trading", fig_pairs_trading),
        ("efficient frontier", fig_efficient_frontier),
        ("prepayment", fig_prepayment_curve),
    ]
    for name, fn in figs:
        t = time.time()
        print(f"fig {name}...", end="", flush=True)
        fn()
        print(f" done ({time.time()-t:.2f}s)")
    print(f"total: {time.time()-t0:.1f}s")
