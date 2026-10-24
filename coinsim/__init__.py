"""Coin tosses: law of large numbers, central limit theorem and the accuracy of the normal approximation."""

from .simulation import freedman_diaconis_bins_v1, lattice_bins, running_means, sample_proportions
from .theory import (BERRY_ESSEEN_C, berry_esseen_bound, binomial_pmf, kolmogorov_distance, lil_envelope,
                     lil_exceeds_band_from, normal_cdf, standard_error)

__version__ = "2.1.0"
