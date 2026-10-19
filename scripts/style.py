"""Shared matplotlib style for the paper figures.

Bold sans-serif text, thick lines and inward ticks on all four sides,
sized for one column of Phys. Rev. E (3.4 in wide).
"""
import matplotlib as mpl

COL_W = 3.404   # one-column width in inches (245 pt)

COLORS = {"nMF": "#000000", "SUH": "#1b9e77", "SUH+mom.": "#a6761d",
          "SUH+ridge": "#7570b3", "PANN": "#d95f02", "PBNN": "#6a3d9a"}
MARKERS = {"nMF": "s", "SUH": "o", "SUH+mom.": "^",
           "SUH+ridge": "v", "PANN": "D", "PBNN": "P"}
LINES = {"nMF": "-", "SUH": "-", "SUH+mom.": "--",
         "SUH+ridge": "-", "PANN": "--", "PBNN": ":"}
OPEN = {"SUH+ridge", "PANN"}                 # open (white-filled) markers
LABELS = {"SUH+mom.": "SUH+moment"}

# calibration regimes (g, rho) -> colour, as in the paper
REGIME_COLORS = {(0.3, 26): "#d95f02", (0.3, 526): "#1b9e77",
                 (1.0, 26): "#6a3d9a", (1.0, 526): "#e7298a"}
RMSE_GRAY = "#999999"
C_BLUES = ["#c6dbef", "#4292c6", "#08306b"]
G_COLORS = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#000000"]
G_MARKERS = ["o", "s", "^", "D", "v"]


def apply():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
        "font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold",
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans:bold", "mathtext.it": "Liberation Sans:bold:italic",
        "mathtext.bf": "Liberation Sans:bold", "mathtext.sf": "Liberation Sans:bold",
        "mathtext.cal": "Liberation Sans:bold", "mathtext.tt": "Liberation Mono:bold",
        "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "axes.linewidth": 1.2, "lines.linewidth": 1.8,
        "lines.markersize": 5, "lines.markeredgewidth": 1.2,
        "errorbar.capsize": 2.5,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": True, "ytick.right": True,
        "xtick.major.width": 1.1, "ytick.major.width": 1.1,
        "xtick.major.size": 3.5, "ytick.major.size": 3.5,
        "xtick.minor.width": 0.9, "ytick.minor.width": 0.9,
        "xtick.minor.size": 2.0, "ytick.minor.size": 2.0,
        "legend.frameon": False, "legend.handlelength": 2.2,
        "axes.grid": False, "hatch.linewidth": 1.0,
        "savefig.bbox": "standard",
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })


def panel_label(ax, text, x=0.0, y=1.01):
    """'(a)' placed just above the top-left corner of the axes."""
    ax.text(x, y, text, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=9, fontweight="bold")
