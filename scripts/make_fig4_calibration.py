"""Fig. 4: calibration of the PBNN posterior (N=20).

(a) coverage deviation (empirical - nominal, in %) vs nominal credible level
(b) histogram of standardized errors z_ij with the N(0,1) density
(c) sharpness: realized RMSE vs mean posterior sigma
    (20 realizations x 380 off-diagonal couplings per regime; the values are
    those of the posterior-calibration table in the manuscript source).

Usage: python make_fig4_calibration.py [data_dir] [out.pdf]
"""
import sys, csv, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import style

style.apply()
d = sys.argv[1] if len(sys.argv) > 1 else "../data"
out = sys.argv[2] if len(sys.argv) > 2 else "../figures/Fig4_calibration.pdf"

regimes = [(0.3, 26), (0.3, 526), (1.0, 26), (1.0, 526)]
rmse  = {(0.3, 26): 0.0401, (0.3, 526): 0.0104, (1.0, 26): 0.0651, (1.0, 526): 0.0145}
sigma = {(0.3, 26): 0.0380, (0.3, 526): 0.0105, (1.0, 26): 0.0631, (1.0, 526): 0.0145}

cov = list(csv.DictReader(open(f"{d}/fig4_coverage.csv")))
hist = list(csv.DictReader(open(f"{d}/fig4_zhist.csv")))

fig = plt.figure(figsize=(style.COL_W, 3.15))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.82], hspace=0.62, wspace=0.42,
                      left=0.16, right=0.985, top=0.83, bottom=0.135)
ax, bx = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
cx = fig.add_subplot(gs[1, :])

def lab(g, r): return f"$g$={g:.1f}, $\\rho$={r}"

# (a) coverage deviation
lv = [float(r["nominal_level"]) for r in cov]
ax.axhline(0, color="k", lw=1.4, ls="--", zorder=1)
for g, r in regimes:
    ax.plot(lv, [float(x[f"dev_pct_g{g}_rho{r}"]) for x in cov],
            color=style.REGIME_COLORS[(g, r)], lw=1.6, zorder=3)
ax.set_xlim(0, 1); ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(["0", "0.5", "1"])
ax.set_ylim(-3.3, 1.3); ax.set_yticks([-2, 0])
ax.set_xlabel("nominal level", labelpad=2)
ax.set_ylabel("coverage\ndeviation (%)", linespacing=1.0)
style.panel_label(ax, "(a)")

# (b) standardized errors
for g, r in regimes:
    hs = [h for h in hist if float(h["g"]) == g and int(h["rho"]) == r]
    edges = [float(hs[0]["bin_left"])] + [float(h["bin_right"]) for h in hs]
    dens = [float(h["density"]) for h in hs]
    bx.stairs(dens, edges, color=style.REGIME_COLORS[(g, r)], lw=1.3, zorder=3)
z = np.linspace(-4, 4, 400)
bx.plot(z, np.exp(-z**2 / 2) / np.sqrt(2 * np.pi), "k--", lw=1.4, zorder=4)
bx.set_xlim(-4, 4); bx.set_xticks([-4, -2, 0, 2, 4])
bx.set_ylim(0, 0.47); bx.set_yticks([0, 0.2, 0.4])
bx.set_xlabel("$z_{ij}$", labelpad=1)
bx.set_ylabel("density")
style.panel_label(bx, "(b)")

# (c) sharpness
x = np.arange(len(regimes)); w = 0.36
for k, reg in enumerate(regimes):
    cx.bar(x[k] - w/2, rmse[reg], w, color=style.RMSE_GRAY, edgecolor="k", lw=0.9, zorder=3)
    cx.bar(x[k] + w/2, sigma[reg], w, color=style.REGIME_COLORS[reg], edgecolor="k",
           hatch="////", lw=0.9, zorder=3)
cx.set_xticks(x)
cx.set_xticklabels([f"$g$={g:.1f}\n$\\rho$={r}" for g, r in regimes], linespacing=1.15)
cx.tick_params(axis="x", which="both", top=False, bottom=False)
cx.set_xlim(-0.6, len(regimes) - 0.4)
cx.set_ylim(0, 0.1); cx.set_yticks([0, 0.04, 0.08]); cx.set_yticklabels(["0.00", "0.04", "0.08"])
cx.set_ylabel("scale")
cx.legend([plt.Rectangle((0, 0), 1, 1, fc=style.RMSE_GRAY, ec="k", lw=0.9),
           plt.Rectangle((0, 0), 1, 1, fc="white", ec="k", hatch="////", lw=0.9)],
          ["RMSE", r"mean posterior $\sigma$"], loc="upper right", ncol=2,
          handlelength=1.8, columnspacing=1.2, borderaxespad=0.35)
style.panel_label(cx, "(c)", x=0.015, y=0.80)

# shared legend for the four regimes
handles = [Line2D([], [], color=style.REGIME_COLORS[k], lw=1.8) for k in regimes]
order = [0, 1, 2, 3]   # filled column-wise: row 1 = rho=26, row 2 = rho=526
fig.legend([handles[i] for i in order], [lab(*regimes[i]) for i in order],
           ncol=2, loc="upper center", bbox_to_anchor=(0.57, 1.0),
           columnspacing=1.2, handlelength=1.8, handletextpad=0.5, labelspacing=0.25)

fig.savefig(out)
fig.savefig(out.replace(".pdf", ".png"), dpi=300)
print("wrote", out)
