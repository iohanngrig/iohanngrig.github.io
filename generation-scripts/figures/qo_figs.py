#!/usr/bin/env python3
"""Figures for Note 17 — quantum computing for constrained optimization."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _style import apply, PALETTE  # noqa: E402

apply()
FIGS = Path(__file__).resolve().parent.parent / "iohanngrig.github.io" / "content" / "research-notes" / "figures"
if not FIGS.exists():
    FIGS = Path("/Users/hgrig/FuturePlans/iohanngrig.github.io/content/research-notes/figures")


def fig1_speedups():
    """Classical vs. Grover vs. Shor: work vs. n (bits)."""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    n = np.arange(10, 71, 1)  # bits
    brute = 2.0 ** n
    grover = 2.0 ** (n / 2)
    # GNFS classical factoring: exp( c * (ln N)^(1/3) * (ln ln N)^(2/3) )
    lnN = n * np.log(2.0)
    gnfs = np.exp(1.923 * (lnN ** (1 / 3)) * (np.log(lnN) ** (2 / 3)))
    shor = n ** 3  # Shor O((log N)^3)

    ax.semilogy(n, brute, "-", color=PALETTE["grey"], lw=2.3, label="Brute force $2^n$ (NP-hard enumeration)")
    ax.semilogy(n, grover, "-", color=PALETTE["orange"], lw=2.3, label="Grover $\\sqrt{2^n} = 2^{n/2}$ (quadratic)")
    ax.semilogy(n, gnfs, "-", color=PALETTE["purple"], lw=2.3, label="GNFS (best classical factoring)")
    ax.semilogy(n, shor, "-", color=PALETTE["blue"], lw=2.5, label="Shor $O(n^3)$ (polynomial)")

    ax.axvline(30, ls=":", color="gray", alpha=0.5, lw=1)
    ax.text(30.5, 1e18, "$n=30$", fontsize=9, color="gray")
    ax.axvline(60, ls=":", color="gray", alpha=0.5, lw=1)
    ax.text(60.5, 1e18, "$n=60$", fontsize=9, color="gray")

    ax.set_xlabel("Input size $n$ (bits)")
    ax.set_ylabel("Operations (log scale)")
    ax.set_title("Scaling of known classical and quantum algorithms")
    ax.set_ylim(1e1, 1e22)
    ax.legend(loc="upper left", frameon=True, fontsize=9.5)
    ax.grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    out = FIGS / "qo-fig1-speedups.svg"
    plt.savefig(out, format="svg", bbox_inches="tight")
    plt.close()
    print(f"wrote {out}")


def fig2_qaoa_hardware():
    """QAOA on Sycamore: native vs. non-native (Harrigan 2020 stylized)."""
    fig, ax = plt.subplots(figsize=(8.5, 5))
    n_range = np.arange(6, 24, 1)

    # Stylized curves matching Harrigan 2020 narrative:
    # native: approximation ratio ~constant ~0.72, slight upward drift with depth
    # non-native: approx ratio declining with problem size (compilation overhead kills it)

    native_ratio = 0.70 + 0.02 * np.tanh((n_range - 12) / 4)
    native_ratio += 0.005 * np.random.default_rng(1).normal(size=len(n_range))

    nonnative_ratio = 0.68 - 0.015 * (n_range - 8)
    nonnative_ratio = np.maximum(nonnative_ratio, 0.51)
    nonnative_ratio += 0.008 * np.random.default_rng(2).normal(size=len(n_range))

    random_guess = np.full_like(n_range, 0.5, dtype=float)
    gw_bound = np.full_like(n_range, 0.8786, dtype=float)

    ax.plot(n_range, native_ratio, "o-", color=PALETTE["blue"], lw=2.2, ms=5,
            label="QAOA on hardware-native graphs")
    ax.plot(n_range, nonnative_ratio, "s-", color=PALETTE["orange"], lw=2.2, ms=5,
            label="QAOA on non-native (Max-Cut, SK)")
    ax.plot(n_range, gw_bound, "--", color=PALETTE["green"], lw=1.8,
            label="Goemans-Williamson SDP: 0.8786")
    ax.plot(n_range, random_guess, ":", color="gray", lw=1.5, label="Random guessing: 0.5")

    ax.set_xlabel("Problem size $n$ (qubits)")
    ax.set_ylabel("Approximation ratio (cut fraction)")
    ax.set_title("QAOA on Sycamore: hardware-native vs. non-native problems")
    ax.set_ylim(0.45, 0.95)
    ax.legend(loc="center right", fontsize=9, frameon=True)
    ax.grid(True, alpha=0.3)

    # Annotation explaining the story
    ax.annotate(
        "Compilation overhead\nkills advantage\non non-native graphs",
        xy=(20, 0.54), xytext=(13.5, 0.60),
        fontsize=9, ha="left", color=PALETTE["orange"],
        arrowprops=dict(arrowstyle="-", color=PALETTE["orange"], alpha=0.6),
    )

    ax.text(0.02, 0.02, "Stylized after Harrigan, Arute, et al. 2020, Nature Physics.",
            transform=ax.transAxes, fontsize=8, style="italic", color="gray")

    plt.tight_layout()
    out = FIGS / "qo-fig2-qaoa-hardware.svg"
    plt.savefig(out, format="svg", bbox_inches="tight")
    plt.close()
    print(f"wrote {out}")


if __name__ == "__main__":
    fig1_speedups()
    fig2_qaoa_hardware()
