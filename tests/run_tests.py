"""Unit tests. Run from the repository root:  python tests/run_tests.py

Each result is compared with an independent computation: exact rational arithmetic (fractions.Fraction and
math.comb), a plain loop, a brute-force search, or a published bound.
"""

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coinsim import (berry_esseen_bound, binomial_pmf, freedman_diaconis_bins_v1, kolmogorov_distance,  # noqa: E402
                     lattice_bins, lil_envelope, lil_exceeds_band_from, normal_cdf, running_means,
                     sample_proportions, standard_error)

failed = 0


def check(name, ok):
    global failed
    print(f"{'ok' if ok else 'FAIL':<5}{name}")
    if not ok:
        failed += 1


# Binomial distribution -------------------------------------------------------------------------------
def exact_pmf(n, p):
    p = Fraction(p)
    return [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


check("binomial pmf equals exact rational values (n <= 60)",
      all(np.allclose(binomial_pmf(n, p), [float(v) for v in exact_pmf(n, p)], rtol=1e-12, atol=1e-300)
          for n in (1, 2, 5, 30, 60) for p in (0.5, 0.1, 0.37)))

# Rounding in the running sum of logarithms leaves an error of about 1e-9 at n = 100,000, far below the
# distances of 1e-4 and more that are measured with these probabilities.
check("binomial pmf sums to one within 1e-8 for n = 100,000",
      all(abs(binomial_pmf(100_000, p).sum() - 1.0) < 1e-8 for p in (0.5, 0.1, 0.01)))

check("normal_cdf matches known values",
      abs(float(normal_cdf(0.0)) - 0.5) < 1e-15 and abs(float(normal_cdf(1.959963984540054)) - 0.975) < 1e-12)


# Kolmogorov distance ---------------------------------------------------------------------------------
def brute_distance(n, p, points=200_001):
    """Evaluate |F(x) - Phi(x)| on a dense grid, including just before and at each jump."""
    pmf = [float(v) for v in exact_pmf(n, p)]
    cdf = np.cumsum(pmf)
    sigma = math.sqrt(n * p * (1 - p))
    xs = np.concatenate((np.linspace(-1, n + 1, points), np.arange(n + 1), np.arange(n + 1) - 1e-9))
    f = np.where(xs < 0, 0.0, cdf[np.clip(np.floor(xs).astype(int), 0, n)])
    return float(np.max(np.abs(f - normal_cdf((xs - n * p) / sigma))))


check("Kolmogorov distance equals a brute-force search (n <= 40)",
      all(abs(kolmogorov_distance(n, p) - brute_distance(n, p)) < 1e-6
          for n in (1, 5, 13, 40) for p in (0.5, 0.2, 0.05)))

check("Berry-Esseen bound holds for every n tested (5 to 100,000)",
      all(kolmogorov_distance(n, p) <= berry_esseen_bound(n, p)
          for n in (5, 30, 100, 1000, 10_000, 100_000) for p in (0.5, 0.1, 0.01)))

# Simulation -------------------------------------------------------------------------------------------
rng = np.random.default_rng(1)
paths = running_means(500, 3, 0.5, np.random.default_rng(7))
tosses = np.random.default_rng(7).random((3, 500)) < 0.5
loop = []
for row in tosses:
    heads, out = 0, []
    for i, t in enumerate(row, start=1):
        heads += int(t)
        out.append(heads / i)
    loop.append(out)
check("running means equal a plain loop", np.array_equal(paths, np.array(loop)))

props = sample_proportions(100, 200_000, 0.3, rng)
check("simulated proportions have mean p and variance p(1-p)/n (within 3 standard errors)",
      abs(props.mean() - 0.3) < 3 * math.sqrt(0.21 / 100 / 200_000)
      and abs(props.var() / (0.21 / 100) - 1) < 3 * math.sqrt(2 / 200_000))

edges = lattice_bins(30)
check("lattice bins hold exactly one possible proportion each",
      all(np.sum((np.arange(31) / 30 >= a) & (np.arange(31) / 30 < b)) == 1 for a, b in zip(edges, edges[1:])))

v1 = sample_proportions(30, 20_000, 0.5, np.random.default_rng(42))
bins = freedman_diaconis_bins_v1(v1)
check("version 1 binning gives bins narrower than the lattice spacing 1/n for n = 30",
      (v1.max() - v1.min()) / bins < 1 / 30)

# Curves -----------------------------------------------------------------------------------------------
n0 = lil_exceeds_band_from(1.96)
check("LIL envelope is narrower than the 95% band below n0 and wider from n0 on",
      lil_envelope([n0 - 1], 0.5)[0] < 1.96 * standard_error(n0 - 1, 0.5)
      and lil_envelope([n0], 0.5)[0] > 1.96 * standard_error(n0, 0.5))

print(f"\n{failed} check(s) failed.")
sys.exit(1 if failed else 0)
