"""Simulation of coin tosses: running means of many paths, and sample proportions of repeated experiments.

Author: Muhammed Ikbal Yilmaz
"""

import numpy as np


def running_means(n, paths, p, rng):
    """Running means p_hat_1, ..., p_hat_n of `paths` independent sequences of n Bernoulli(p) tosses.

    Returns an array of shape (paths, n). Heads are counted with integers, so the means are exact ratios.
    """
    tosses = rng.random((paths, n)) < p
    heads = np.cumsum(tosses, axis=1, dtype=np.int64)
    return heads / np.arange(1, n + 1, dtype=float)


def sample_proportions(n, experiments, p, rng):
    """Sample proportions of `experiments` independent experiments of n tosses each.

    The number of heads in one experiment is Binomial(n, p); drawing it directly is equivalent to tossing n
    coins and much faster.
    """
    return rng.binomial(n, p, size=experiments) / n


def lattice_bins(n):
    """Histogram edges for a sample proportion of n tosses: one bin of width 1/n centred on each value k/n."""
    return (np.arange(n + 2) - 0.5) / n


def freedman_diaconis_bins_v1(data, min_bins=25, max_bins=160):
    """The binning rule of version 1, kept unchanged so that its effect can be shown."""
    d = np.asarray(data, dtype=float)
    if d.size <= 1:
        return max(10, min_bins)
    q1, q3 = np.percentile(d, [25, 75])
    iqr = q3 - q1
    n = d.size
    if iqr <= 0:
        bins = int(np.sqrt(n))
    else:
        h = 2 * iqr / (n ** (1 / 3))
        data_range = d.max() - d.min()
        bins = int(np.ceil(data_range / h)) if (h > 0 and data_range > 0) else int(np.sqrt(n))
    return int(np.clip(bins, min_bins, max_bins))
