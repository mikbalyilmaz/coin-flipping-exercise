"""Analysis 2: how accurate the normal approximation to the sample proportion is, computed exactly.

Why: version 1 judged the central limit theorem by eye, from simulated histograms. The distance between the
binomial distribution and its normal approximation can be computed exactly, without simulation, and compared
with the Berry-Esseen bound. The question is how many tosses the approximation needs, and how that depends
on p: the further p is from 1/2, the more skewed the binomial distribution.

Design: for p in {0.5, 0.1, 0.01} and 46 values of n from 5 to 10^5, the Kolmogorov distance
D_n = sup_x |P(S_n <= x) - Phi((x - n p) / sigma_n)|, with and without continuity correction, and the
Berry-Esseen bound 0.4748 (p^2 + q^2) / sqrt(p q n).
"""

import numpy as np

from common import save_table
from coinsim import berry_esseen_bound, kolmogorov_distance
from coinsim.style import BLUE, INK, MUTED, RED, L, end_label, fit_log_axis, may_touch, num, save_figure, use_style

PS = (0.5, 0.1, 0.01)
NS = np.unique(np.round(np.logspace(np.log10(5), 5, 46)).astype(int))

rows = []
for p in PS:
    for n in NS:
        rows.append({"p": p, "n": int(n), "kolmogorov": kolmogorov_distance(int(n), p),
                     "kolmogorov_cc": kolmogorov_distance(int(n), p, continuity_correction=True),
                     "berry_esseen": berry_esseen_bound(int(n), p)})
save_table(rows, "table3_clt_accuracy")

# Selected values for the notes, and the smallest n on the grid from which D_n stays below 0.01.
selected = []
for p in PS:
    sub = [r for r in rows if r["p"] == p]
    below = [r["n"] for i, r in enumerate(sub) if all(s["kolmogorov"] < 0.01 for s in sub[i:])]
    entry = {"p": p, "n_for_distance_below_0.01": below[0] if below else ""}
    for target in (30, 100, 1000, 10_000):
        entry[f"D_at_{target}"] = kolmogorov_distance(target, p)
        entry[f"Dcc_at_{target}"] = kolmogorov_distance(target, p, continuity_correction=True)
        entry[f"BE_at_{target}"] = berry_esseen_bound(target, p)
    slope_rows = [r for r in sub if r["n"] >= 1000]
    entry["slope_n_ge_1e3"] = float(np.polyfit(np.log([r["n"] for r in slope_rows]),
                                               np.log([r["kolmogorov"] for r in slope_rows]), 1)[0])
    selected.append(entry)
save_table(selected, "table4_clt_summary")
for s in selected:
    print(s)

use_style()
COLORS = dict(zip(PS, (INK, BLUE, MUTED)))


def draw():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4.75, 2.5), constrained_layout=True)
    values = []
    for p in PS:
        sub = [r for r in rows if r["p"] == p]
        ns = [r["n"] for r in sub]
        d = [r["kolmogorov"] for r in sub]
        b = [r["berry_esseen"] for r in sub]
        values += d + b
        ax.plot(ns, d, color=COLORS[p], lw=1.4, marker="o", ms=2)
        ax.plot(ns, b, color=COLORS[p], lw=0.9, ls=(0, (3, 2)))
        end_label(ax, ns[-1], d[-1], f"p = {num(p)}", COLORS[p])
    may_touch(ax.axhline(0.01, color=RED, lw=0.8, ls=(0, (1, 1.4))))
    fit_log_axis(ax, "x", [r["n"] for r in rows])
    fit_log_axis(ax, "y", values)
    ax.set_xlabel(L("Number of tosses n", "Atış sayısı n"))
    ax.set_title(L("Solid: exact distance $D_n$. Dashed: Berry–Esseen bound. Red: 0.01",
                   "Düz: kesin uzaklık $D_n$. Kesikli: Berry–Esseen sınırı. Kırmızı: 0,01"))
    return fig


save_figure("fig2_clt_accuracy", draw,
            heading=lambda: L("Figure 2. Distance between the binomial distribution and its normal approximation",
                              "Şekil 2. Binom dağılımı ile normal yaklaşım arasındaki uzaklık"))
