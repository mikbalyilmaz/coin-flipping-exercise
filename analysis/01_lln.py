"""Analysis 1: the law of large numbers along a path, and what a pointwise 95% band does and does not say.

Why: version 1 drew one running mean with the band p +/- 1.96 SE(n), SE(n) = sqrt(p(1-p)/n), and called it a
95% band. At each fixed n about 95% of paths are inside it. But a path is judged over all n at once, and the
law of the iterated logarithm implies that every path leaves the band again and again. This analysis
measures both statements on 2,000 simulated paths.

Design: 2,000 paths of 10^5 fair-coin tosses. For each n: the share of paths outside the band at n, the share
that has been outside at least once up to n, and the root mean square of p_hat_n - p.
"""

import numpy as np

from common import P, SEED, save_table
from coinsim import lil_envelope, lil_exceeds_band_from, running_means, standard_error
from coinsim.style import BLUE, INK, MUTED, RED, L, fit_log_axis, may_touch, save_figure, use_style, value_axis

N = 100_000
PATHS = 2_000
CHUNK = 100
Z = 1.96
SHOWN = 20

n = np.arange(1, N + 1)
band = Z * standard_error(n, P)
rng = np.random.default_rng(SEED)

outside_now = np.zeros(N)
outside_ever = np.zeros(N)
squared_error = np.zeros(N)
shown = None
for start in range(0, PATHS, CHUNK):
    means = running_means(N, CHUNK, P, rng)
    if shown is None:
        shown = means[:SHOWN].copy()
    out = np.abs(means - P) > band
    outside_now += out.sum(axis=0)
    outside_ever += np.logical_or.accumulate(out, axis=1).sum(axis=0)
    squared_error += ((means - P) ** 2).sum(axis=0)
outside_now /= PATHS
outside_ever /= PATHS
rms = np.sqrt(squared_error / PATHS)

grid = np.unique(np.round(np.logspace(0, 5, 51)).astype(int))
save_table([{"n": int(k), "share_outside_at_n": outside_now[k - 1], "share_outside_by_n": outside_ever[k - 1],
             "rms_error": rms[k - 1], "theory_se": float(standard_error(k, P))} for k in grid], "table1_lln")

late = n >= 1000
slope = np.polyfit(np.log(n[late]), np.log(rms[late]), 1)[0]
summary = [{
    "paths": PATHS, "n_max": N,
    "share_outside_at_n_mean_1e3_to_1e5": float(outside_now[999:].mean()),
    "share_outside_by_1e3": float(outside_ever[999]), "share_outside_by_1e5": float(outside_ever[-1]),
    "rms_slope_n_ge_1e3": float(slope),
    "rms_over_se_at_1e5": float(rms[-1] / standard_error(N, P)),
    "lil_wider_than_band_from_n": lil_exceeds_band_from(Z),
}]
save_table(summary, "table2_lln_summary")
print(summary)

use_style()


def draw():
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(4.75, 2.5), constrained_layout=True)
    ax = axes[0]
    for path in shown:
        ax.plot(n, path, color=BLUE, lw=0.5, alpha=0.45)
    ax.plot(n, P + band, color=INK, lw=1.2, label=L("Pointwise 95% band", "Noktasal %95 bandı"))
    ax.plot(n, P - band, color=INK, lw=1.2)
    env = lil_envelope(n, P)
    ax.plot(n, P + env, color=MUTED, lw=1.0, ls=(0, (3, 2)), label=L("LIL envelope", "LIL zarfı"))
    ax.plot(n, P - env, color=MUTED, lw=1.0, ls=(0, (3, 2)))
    fit_log_axis(ax, "x", [1, N])
    value_axis(ax, "y", 0, 1, 0.25)
    ax.set_xlabel("n")
    ax.set_title(L(f"(a) {SHOWN} running means $\\hat p_n$", f"(a) {SHOWN} yürüyen ortalama $\\hat p_n$"))
    ax.legend(loc="upper right", fontsize=6.3, handlelength=2.2)

    ax = axes[1]
    ax.plot(n, 100 * outside_now, color=BLUE, lw=1.2, label=L("Outside the band at n", "n anında band dışında"))
    ax.plot(n, 100 * outside_ever, color=INK, lw=1.4,
            label=L("Outside at least once up to n", "n'ye kadar en az bir kez dışarıda"))
    may_touch(ax.axhline(5, color=RED, lw=0.8, ls=(0, (1, 1.4))))
    fit_log_axis(ax, "x", [1, N])
    value_axis(ax, "y", 0, 100, 25)
    ax.set_xlabel("n")
    ax.set_title(L(f"(b) Share of {PATHS:,} paths, %", f"(b) {PATHS:,} yolun payı, %".replace(",", ".")))
    ax.legend(loc="upper left", fontsize=6.3, handlelength=2.2)
    return fig


save_figure("fig1_lln", draw,
            heading=lambda: L("Figure 1. Running means and the pointwise 95% band",
                              "Şekil 1. Yürüyen ortalamalar ve noktasal %95 bandı"))
