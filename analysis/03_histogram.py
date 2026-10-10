"""Analysis 3: why the version 1 histograms were taller than the normal curve, and how to draw them.

Why: a sample proportion of n tosses can only take the values 0, 1/n, ..., 1. Version 1 chose histogram bins
with the Freedman-Diaconis rule, which assumes a continuous variable. For n = 30 the bins were narrower than
the spacing 1/n, so most bins were empty and the others, scaled as a density, rose far above the normal
curve. Bins of width 1/n centred on the possible values fix this, and the exact binomial probabilities can be
drawn on the same scale.

Design: 20,000 experiments of n = 30 fair-coin tosses, as in version 1, drawn twice: with version 1's bins and
with lattice bins.
"""

import math

import numpy as np

from common import P, SEED, save_table
from coinsim import binomial_pmf, freedman_diaconis_bins_v1, lattice_bins, sample_proportions
from coinsim.style import BLUE, MUTED, ORANGE, L, decimal_axis, num, save_figure, use_style

N = 30
M = 20_000

rng = np.random.default_rng(SEED + 1)
props = sample_proportions(N, M, P, rng)
v1_bins = freedman_diaconis_bins_v1(props)
v1_heights, v1_edges = np.histogram(props, bins=v1_bins, density=True)
lat_heights, lat_edges = np.histogram(props, bins=lattice_bins(N), density=True)
pmf = binomial_pmf(N, P)
sigma = math.sqrt(P * (1 - P) / N)
normal_peak = 1.0 / (math.sqrt(2 * math.pi) * sigma)

summary = [{
    "n": N, "experiments": M, "v1_bins": v1_bins, "v1_bin_width": float(v1_edges[1] - v1_edges[0]),
    "lattice_spacing": 1.0 / N, "v1_empty_bins": int(np.sum(v1_heights == 0)),
    "v1_max_height": float(v1_heights.max()), "lattice_max_height": float(lat_heights.max()),
    "exact_max_height": float(pmf.max() * N), "normal_peak": normal_peak,
}]
save_table(summary, "table5_histogram")
print(summary)

use_style()
x = np.linspace(0.05, 0.95, 400)
normal = np.exp(-0.5 * ((x - P) / sigma) ** 2) / (math.sqrt(2 * math.pi) * sigma)


def draw():
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2), sharey=True, constrained_layout=True)
    panels = [(axes[0], v1_heights, v1_edges, L(f"Version 1: {v1_bins} Freedman–Diaconis bins",
                                               f"Sürüm 1: {v1_bins} Freedman–Diaconis aralığı")),
              (axes[1], lat_heights, lat_edges, L("Bins of width 1/n on the possible values",
                                                 "Olası değerlere ortalanmış 1/n genişliğinde aralıklar"))]
    for ax, heights, edges, title in panels:
        ax.bar(edges[:-1], heights, width=np.diff(edges), align="edge", color=BLUE, alpha=0.75, lw=0)
        ax.plot(x, normal, color=ORANGE, lw=1.6, label=L("Normal approximation", "Normal yaklaşım"))
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("$\\hat p$")
        ax.set_xlim(0.1, 0.9)
        decimal_axis(ax, "x")
    k = np.arange(N + 1) / N
    axes[1].plot(k, pmf * N, "o", ms=2.8, color=MUTED, label=L("Exact binomial", "Kesin binom"))
    axes[0].set_ylabel(L("Density", "Yoğunluk"))
    decimal_axis(axes[0], "y")
    axes[1].legend(loc="upper right", fontsize=8)
    return fig


save_figure("fig3_histogram", draw,
            heading=lambda: L(f"Figure 3. {M:,} sample proportions of n = {N} tosses, two choices of bins",
                              f"Şekil 3. n = {N} atışlık {M:,} örneklem oranı, iki farklı aralık seçimi".replace(",", ".")))
