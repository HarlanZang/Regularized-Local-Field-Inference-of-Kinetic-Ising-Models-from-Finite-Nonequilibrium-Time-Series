"""Fig. 5: paired stabilization gain versus information ratio rho (N=20).

(a) PBNN vs SUH, (b) PANN vs SUH+ridge; one line per coupling strength g.
Points are mean paired differences of log10 MSE over 20 realizations; error
bars are 95% confidence intervals. Points of different g are shifted by a few
percent along the (logarithmic) rho axis so that the error bars do not overlap.

Usage: python make_fig5_regime.py [S_regime.csv] [out.pdf]
"""
import sys, csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import style

style.apply()
src = sys.argv[1] if len(sys.argv) > 1 else "../data/S_regime.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "../figures/Fig5_regime.pdf"
rows = list(csv.DictReader(open(src)))
gs = sorted({float(r["g"]) for r in rows})
rhos = sorted({float(r["rho"]) for r in rows})
dodge = {g: 1.0 + 0.045 * (k - (len(gs) - 1) / 2) for k, g in enumerate(gs)}

fig, axes = plt.subplots(2, 1, figsize=(style.COL_W, 3.9), sharex=True)
fig.subplots_adjust(left=0.2, right=0.97, top=0.915, bottom=0.11, hspace=0.16)
panels = [("PBNN_vs_SUH", "(a)", "PBNN vs SUH"),
          ("PANN_vs_SUH+ridge", "(b)", "PANN vs SUH+ridge")]
for ax, (key, tag, name) in zip(axes, panels):
    ax.axhline(0, color="k", lw=1.2, ls="--", zorder=1)
    for k, g in enumerate(gs):
        sub = sorted((r for r in rows if float(r["g"]) == g), key=lambda r: float(r["rho"]))
        ax.errorbar([float(r["rho"]) * dodge[g] for r in sub], [float(r[key]) for r in sub],
                    yerr=[float(r[key + "_err"]) for r in sub],
                    color=style.G_COLORS[k], marker=style.G_MARKERS[k], ms=4.5,
                    mfc=style.G_COLORS[k], mec=style.G_COLORS[k], lw=1.6, elinewidth=1.2,
                    capsize=2.0, label=f"$g$={g:.1f}", zorder=3 + k)
    ax.set_xscale("log")
    ax.set_ylabel(r"$\Delta\log_{10}$MSE")
    pos = (0.97, 0.06, "right", "bottom") if tag == "(a)" else (0.03, 0.94, "left", "top")
    ax.text(pos[0], pos[1], f"{tag} {name}", transform=ax.transAxes,
            ha=pos[2], va=pos[3], fontsize=9, fontweight="bold")
axes[1].set_xticks(rhos)
axes[1].set_xticklabels([f"{r:.0f}" for r in rhos])
axes[1].minorticks_off(); axes[0].minorticks_off()
axes[1].set_xlim(10.5, 680)
axes[1].set_xlabel(r"$\rho$", labelpad=1)
axes[0].set_ylim(-0.46, 0.07); axes[0].set_yticks([-0.4, -0.2, 0.0])
axes[1].set_ylim(-0.04, 0.30); axes[1].set_yticks([0.0, 0.1, 0.2])
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, ncol=5, loc="upper center", bbox_to_anchor=(0.585, 1.0),
           columnspacing=0.8, handlelength=1.6, handletextpad=0.35)
fig.savefig(out)
fig.savefig(out.replace(".pdf", ".png"), dpi=300)
print("wrote", out)
