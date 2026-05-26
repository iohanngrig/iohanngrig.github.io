"""
Shared matplotlib style for research-notes figures.
Upgraded (April 2026 pass): higher visual rigor, colorblind-safe palette,
better typography, consistent annotation, publication-quality defaults.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

# Colorblind-safe, high-contrast palette (inspired by Okabe-Ito and ColorBrewer).
PALETTE = {
    "blue":      "#0072B2",
    "orange":    "#D55E00",
    "green":     "#009E73",
    "red":       "#CC3311",
    "purple":    "#AA4499",
    "teal":      "#117733",
    "grey":      "#4B4B4B",
    "lightgrey": "#BDBDBD",
    "softblue":  "#7FB3D5",
    "softred":   "#E57373",
}

# Ordered list for automatic cycling (distinct hues, safe for most CVDs).
PALETTE_ORDER = [
    PALETTE["blue"], PALETTE["orange"], PALETTE["green"],
    PALETTE["red"], PALETTE["purple"], PALETTE["teal"],
]


def apply():
    mpl.rcParams.update({
        # typography
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Georgia", "Times New Roman", "serif"],
        "font.size": 11,
        "axes.labelsize": 11,
        "axes.titlesize": 12.5,
        "axes.titleweight": "semibold",
        "axes.titlepad": 10,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9,
        "legend.frameon": False,
        # axes
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#222222",
        "axes.titlecolor": "#111111",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.major.width": 0.9,
        "ytick.major.width": 0.9,
        # grid
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.linestyle": ":",
        "grid.alpha": 0.35,
        "grid.linewidth": 0.6,
        "grid.color": "#888888",
        # lines
        "lines.linewidth": 1.8,
        "lines.markersize": 5.5,
        "lines.markeredgewidth": 0.6,
        "lines.markeredgecolor": "white",
        # figure
        "figure.dpi": 110,
        "figure.facecolor": "white",
        "figure.edgecolor": "white",
        # saving
        "savefig.dpi": 180,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.18,
        "savefig.facecolor": "white",
        # color cycle
        "axes.prop_cycle": mpl.cycler(color=PALETTE_ORDER),
    })


def annotate_point(ax, text, xy, xytext=None, color=None, fontsize=9, ha="center"):
    """Consistent annotation style for pointing at a specific value."""
    if xytext is None:
        xytext = (0, 12)
    if color is None:
        color = "#222222"
    ax.annotate(
        text, xy=xy, xytext=xytext, textcoords="offset points",
        ha=ha, va="bottom", fontsize=fontsize, color=color,
        arrowprops=dict(arrowstyle="-", color=color, lw=0.5, alpha=0.7),
    )


def finish(fig, title=None, subtitle=None):
    """Apply a consistent title block to a figure.
    title: main title (larger)
    subtitle: italic caption underneath (smaller, grey)
    """
    if title:
        fig.suptitle(title, fontsize=13, fontweight="semibold", y=0.995,
                     color="#111111")
    if subtitle:
        fig.text(0.5, 0.935, subtitle, fontsize=9.5, style="italic",
                 ha="center", color="#555555")
