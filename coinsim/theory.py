"""Exact results for the sample proportion of n Bernoulli(p) trials.

Everything here is computed without simulation: the binomial distribution, its distance from the normal
approximation, the Berry-Esseen bound on that distance, and the curves used to judge a running mean.

Author: Muhammed Ikbal Yilmaz
"""

import math

import numpy as np

# Best published upper bound for the absolute constant in the Berry-Esseen inequality for identically
# distributed summands (Shevtsova, 2011): C0 < 0.4748.
BERRY_ESSEEN_C = 0.4748


def _check(n, p):
    if int(n) != n or n < 1:
        raise ValueError("n must be a positive integer")
    if not 0.0 < p < 1.0:
        raise ValueError("p must lie strictly between 0 and 1")


def binomial_pmf(n, p):
    """P(S = k) for k = 0, ..., n, where S ~ Binomial(n, p), computed in log space.

    log C(n, k) is accumulated as a running sum of log((n - k + 1) / k), which needs no special functions.
    Rounding in that sum gives a relative error of about 1e-9 at n = 100,000 (checked in the unit tests).
    """
    _check(n, p)
    k = np.arange(1, n + 1, dtype=float)
    log_comb = np.concatenate(([0.0], np.cumsum(np.log(n - k + 1) - np.log(k))))
    kk = np.arange(n + 1, dtype=float)
    return np.exp(log_comb + kk * math.log(p) + (n - kk) * math.log1p(-p))


def normal_cdf(z):
    """Standard normal CDF, vectorised."""
    z = np.asarray(z, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


def kolmogorov_distance(n, p, continuity_correction=False):
    """sup_x |P(S <= x) - Phi((x - n p) / sigma)| for S ~ Binomial(n, p), sigma = sqrt(n p (1 - p)).

    The supremum is attained at a jump of the binomial CDF, so it is enough to compare Phi at each integer k
    with the CDF just after the jump, F(k), and just before it, F(k - 1). With the continuity correction the
    approximation of P(S <= k) is Phi((k + 0.5 - n p) / sigma), and the error is evaluated at the integers.
    """
    pmf = binomial_pmf(n, p)
    cdf = np.minimum(np.cumsum(pmf), 1.0)
    k = np.arange(n + 1)
    sigma = math.sqrt(n * p * (1 - p))
    if continuity_correction:
        return float(np.max(np.abs(cdf - normal_cdf((k + 0.5 - n * p) / sigma))))
    phi = normal_cdf((k - n * p) / sigma)
    before = np.concatenate(([0.0], cdf[:-1]))
    return float(max(np.max(np.abs(cdf - phi)), np.max(np.abs(before - phi))))


def berry_esseen_bound(n, p, c=BERRY_ESSEEN_C):
    """Berry-Esseen bound C * rho / (sigma^3 sqrt(n)) for Bernoulli(p) summands.

    For a Bernoulli(p) variable, sigma^2 = p q and rho = E|X - p|^3 = p q (p^2 + q^2), with q = 1 - p.
    """
    _check(n, p)
    q = 1.0 - p
    return c * (p * p + q * q) / math.sqrt(p * q * n)


def standard_error(n, p):
    """Standard deviation of the sample proportion, sqrt(p (1 - p) / n)."""
    return np.sqrt(p * (1.0 - p) / np.asarray(n, dtype=float))


def lil_envelope(n, p):
    """Half-width sqrt(2 p (1 - p) log log n / n) of the law of the iterated logarithm (defined for n > e).

    By the law of the iterated logarithm, limsup |p_hat_n - p| / envelope(n) = 1 with probability one.
    """
    n = np.asarray(n, dtype=float)
    out = np.full(n.shape, np.nan)
    ok = n > math.e
    out[ok] = np.sqrt(2.0 * p * (1.0 - p) * np.log(np.log(n[ok])) / n[ok])
    return out


def lil_exceeds_band_from(z=1.96):
    """Smallest n at which the LIL envelope is wider than the pointwise band p +/- z * SE(n).

    The envelope is wider when sqrt(2 log log n) > z, i.e. n > exp(exp(z^2 / 2)).
    """
    return math.floor(math.exp(math.exp(z * z / 2.0))) + 1
