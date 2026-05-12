"""
plot_config.py
Shared configuration for all Hopper HPC utilization paper figures.
Academic-paper quality settings: LaTeX-compatible fonts, consistent colors,
publication-ready DPI and dimensions.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Color palette  (colorblind-friendly, works in B&W print)
# ---------------------------------------------------------------------------
COLORS = {
    "blue":        "#2166AC",
    "light_blue":  "#74ADD1",
    "red":         "#D6604D",
    "light_red":   "#F4A582",
    "green":       "#4DAC26",
    "light_green": "#A1D76A",
    "orange":      "#E08214",
    "purple":      "#762A83",
    "gray":        "#878787",
    "dark":        "#1A1A1A",
}

# Ordered palette for multi-bar / multi-line plots
PALETTE = [
    COLORS["blue"],
    COLORS["red"],
    COLORS["green"],
    COLORS["orange"],
    COLORS["purple"],
    COLORS["light_blue"],
    COLORS["gray"],
]

# ---------------------------------------------------------------------------
# Global rcParams  (matches LaTeX article class metrics)
# ---------------------------------------------------------------------------
def set_style():
    mpl.rcParams.update({
        "figure.dpi":           150,
        "savefig.dpi":          300,
        "figure.facecolor":     "white",
        "axes.facecolor":       "white",
        "axes.edgecolor":       "#333333",
        "axes.linewidth":       0.8,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.grid":            True,
        "axes.grid.axis":       "y",
        "grid.color":           "#E5E5E5",
        "grid.linewidth":       0.6,
        "xtick.major.width":    0.8,
        "ytick.major.width":    0.8,
        "xtick.labelsize":      9,
        "ytick.labelsize":      9,
        "axes.labelsize":       10,
        "axes.titlesize":       11,
        "axes.titleweight":     "bold",
        "legend.fontsize":      9,
        "legend.frameon":       True,
        "legend.framealpha":    0.9,
        "legend.edgecolor":     "#CCCCCC",
        "font.family":          "sans-serif",
        "font.sans-serif":      ["DejaVu Sans", "Arial", "Helvetica"],
        "lines.linewidth":      1.8,
        "lines.markersize":     5,
        "patch.linewidth":      0.5,
    })

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def save_fig(fig, path, tight=True):
    """Save figure to path with consistent settings."""
    if tight:
        fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved: {path}")


def format_number(n):
    """Human-readable number: 1234567 -> '1.23M'."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


def add_value_labels(ax, bars, fmt="{:.0f}", fontsize=8, color="white",
                     threshold_pct=0.05, padding=3):
    """Add value labels inside or above bar chart bars."""
    max_val = max(b.get_height() for b in bars)
    for bar in bars:
        h = bar.get_height()
        if h == 0:
            continue
        text = fmt.format(h)
        if h / max_val > threshold_pct:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    h / 2,
                    text,
                    ha="center", va="center",
                    fontsize=fontsize, color=color, fontweight="bold")
        else:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    h + padding,
                    text,
                    ha="center", va="bottom",
                    fontsize=fontsize - 1, color="#444444")
