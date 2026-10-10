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
from coinsim.style import BLUE, MUTED, ORANGE, L, save_figure, use_style

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
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.3), constrained_layout=True)
    ax = axes[0]
    for path in shown:
        ax.plot(n, path, color=BLUE, lw=0.6, alpha=0.45)
    ax.plot(n, P + band, color=ORANGE, lw=1.1, label=L("Pointwise 95% band", "Noktasal %95 bandı"))
    ax.plot(n, P - band, color=ORANGE, lw=1.1)
    env = lil_envelope(n, P)
    ax.plot(n, P + env, color=MUTED, lw=1, ls="--", label=L("LIL envelope", "LIL zarfı"))
    ax.plot(n, P - env, color=MUTED, lw=1, ls="--")
    ax.set_xscale("log")
    ax.set_ylim(0.2, 0.8)
    ax.set_xlim(1, N)
    ax.set_xlabel("n")
    ax.set_ylabel("$\\hat p_n$")
    ax.set_title(L(f"{SHOWN} running means", f"{SHOWN} yürüyen ortalama"))
    ax.legend(loc="upper right")

    ax = axes[1]
    ax.plot(n, 100 * outside_now, color=BLUE, lw=1.4, label=L("Outside the band at n", "n anında band dışında"))
    ax.plot(n, 100 * outside_ever, color=ORANGE, lw=1.6,
            label=L("Outside at least once up to n", "n'ye kadar en az bir kez dışarıda"))
    ax.axhline(5, color=MUTED, lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_xlim(1, N)
    ax.set_ylim(0, 100)
    ax.set_xlabel("n")
    ax.set_ylabel(L(f"Share of {PATHS:,} paths (%)", f"{PATHS:,} yolun payı (%)".replace(",", ".")))
    ax.set_title(L("How often paths leave the band", "Yollar bandı ne sıklıkla terk ediyor"))
    ax.legend(loc="center left")
    return fig


save_figure("fig1_lln", draw,
            heading=lambda: L("Figure 1. Running means and the pointwise 95% band",
                              "Şekil 1. Yürüyen ortalamalar ve noktasal %95 bandı"))
