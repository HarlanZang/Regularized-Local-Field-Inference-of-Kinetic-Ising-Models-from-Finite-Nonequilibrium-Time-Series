"""Fig. 6: robustness (N=20).

(a) off-diagonal MSE under independent observation flips p_flip
(b) paired gain of PBNN over SUH for coupling symmetries c = 0, 0.5, 1
    (bars: mean paired difference of log10 MSE; error bars: 95% CI).

Usage: python make_fig6_robustness.py [data_dir] [out.pdf]
"""
import sys, csv, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import style

style.apply()
d = sys.argv[1] if len(sys.argv) > 1 else "../data"
out = sys.argv[2] if len(sys.argv) > 2 else "../figures/Fig6_robustness.pdf"
noise = list(csv.DictReader(open(f"{d}/S_panelE.csv")))
asym = list(csv.DictReader(open(f"{d}/S_asym.csv")))

fig, (ax, bx) = plt.subplots(2, 1, figsize=(style.COL_W, 3.55),
                             gridspec_kw={"height_ratios": [1, 1]})
fig.subplots_adjust(left=0.19, right=0.97, top=0.865, bottom=0.12, hspace=0.45)

# (a) observation noise
p = [float(r["p_flip"]) for r in noise]
for m in ["nMF", "SUH", "SUH+mom.", "SUH+ridge", "PANN", "PBNN"]:
    c = style.COLORS[m]
    ax.errorbar(p, [float(r[m]) for r in noise], yerr=[float(r[m + "_err"]) for r in noise],
                color=c, marker=style.MARKERS[m], ls=style.LINES[m], lw=1.8, ms=5,
                mfc="white" if m in style.OPEN else c, mec=c, elinewidth=1.2, capsize=2.5,
                label=style.LABELS.get(m, m))
ax.set_yscale("log")
ax.set_xlim(-0.005, 0.105); ax.set_xticks([0, 0.05, 0.1])
ax.set_xticklabels(["0", "0.05", "0.1"])
ax.set_ylim(3e-4, 1e-1)
ax.set_xlabel(r"$p_{\rm flip}$", labelpad=1)
ax.set_ylabel("MSE")
style.panel_label(ax, "(a)")
h, l = ax.get_legend_handles_labels()
# legend is filled column-wise: rows read nMF, SUH+moment, PANN / SUH, SUH+ridge, PBNN
fig.legend(h, l,
           ncol=3, loc="upper center", bbox_to_anchor=(0.56, 1.0),
           columnspacing=1.0, handlelength=2.4, handletextpad=0.4, labelspacing=0.3)

# (b) asymmetry of the coupling ensemble
rho = {500: 26, 2000: 105}
groups = [(0.3, 500), (1.0, 500), (0.3, 2000), (1.0, 2000)]
cs = [0.0, 0.5, 1.0]
x = np.arange(len(groups)); w = 0.26
for k, c in enumerate(cs):
    y, e = [], []
    for g, L in groups:
        r = next(r for r in asym if float(r["c"]) == c and float(r["g"]) == g and float(r["L"]) == L)
        y.append(float(r["Delta_PBNN"])); e.append(float(r["Delta_PBNN_err"]))
    bx.bar(x + (k - 1) * w, y, w, yerr=e, capsize=2.5, color=style.C_BLUES[k],
           edgecolor="k", lw=0.9, error_kw={"lw": 1.2, "capthick": 1.2},
           label=f"$c$={c:.1f}", zorder=3)
bx.axhline(0, color="k", lw=1.2)
bx.set_xticks(x)
bx.set_xticklabels([f"$g$={g:.1f}\n$\\rho$={rho[L]}" for g, L in groups], linespacing=1.15)
bx.tick_params(axis="x", which="both", top=False, bottom=False)
bx.set_xlim(-0.55, len(groups) - 0.45)
bx.set_ylim(-0.32, 0.0); bx.set_yticks([-0.3, -0.2, -0.1, 0.0])
bx.set_ylabel(r"$\Delta$ PBNN")
bx.legend(loc="lower right", ncol=1, handlelength=1.4, borderaxespad=0.4, labelspacing=0.25)
style.panel_label(bx, "(b)")

fig.savefig(out)
fig.savefig(out.replace(".pdf", ".png"), dpi=300)
print("wrote", out)
