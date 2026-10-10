# Coin Tosses: the Running Mean, the 95% Band and the Normal Approximation

Version 2 of a small study of the proportion of heads in $n$ coin tosses,

$$\hat p_n = \frac{1}{n}\sum_{i=1}^{n} X_i, \qquad X_i \sim \text{Bernoulli}(p) \text{ independent}.$$

Version 1 illustrated the law of large numbers and the central limit theorem with simulated plots that were judged by
eye. Version 2 measures what those plots show: how often paths leave the pointwise 95% band, how far the binomial
distribution is from its normal approximation (computed exactly and compared with the Berry–Esseen bound), and why the
histograms of version 1 looked spiky. A short project note (English and Turkish) explains why each analysis was done
and what it shows.

## Contents

| Path | What it is |
|---|---|
| `coinsim/theory.py` | Binomial probabilities, exact Kolmogorov distance to the normal approximation, Berry–Esseen bound, standard error, LIL envelope |
| `coinsim/simulation.py` | Running means of many paths, repeated experiments, histogram bins (version 1 rule and bins matched to the possible values) |
| `coinsim/style.py` | Shared figure style (Latin Modern Roman, colours, English and Turkish versions of each figure) |
| `tests/run_tests.py` | Unit tests against exact rational arithmetic, plain loops, brute-force search and published bounds |
| `analysis/01_lln.py` | Running means and the pointwise 95% band over 2,000 paths (Figure 1) |
| `analysis/02_clt_accuracy.py` | Exact distance between Binomial(n, p) and the normal approximation for p = 0.5, 0.1, 0.01 (Figure 2) |
| `analysis/03_histogram.py` | Histograms of a sample proportion with two choices of bins (Figure 3) |
| `analysis/run_all.py` | Runs the three analyses in order |
| `figures/` | Figures as PNG (300 dpi) and PDF, every reported table as CSV; `figures/tr/` holds the Turkish figures |
| `paper/coin_note.pdf`, `paper/coin_notu.pdf` | Project note in English and in Turkish; `make_paper.py` writes all their numbers from `figures/*.csv` |
| `legacy/` | Version 1, unchanged: the notebook and the R script |
| `fonts/` | Latin Modern Roman (GUST Font License) |

## How to run

```
pip install -r requirements.txt
python tests/run_tests.py
cd analysis
python run_all.py                    # about 15 seconds
cd ../paper
python make_paper.py
xelatex coin_note.tex && xelatex coin_note.tex       # English; needs XeLaTeX
xelatex coin_notu.tex && xelatex coin_notu.tex       # Turkish
```

Seeds are fixed, so every number is the same at every run.

## Usage

```python
import numpy as np
from coinsim import running_means, kolmogorov_distance, berry_esseen_bound

rng = np.random.default_rng(1)
paths = running_means(10_000, 5, 0.5, rng)              # 5 running means of 10,000 tosses
kolmogorov_distance(30, 0.5)                             # exact distance at n = 30
kolmogorov_distance(30, 0.5, continuity_correction=True)
berry_esseen_bound(30, 0.5)
```

## Main results

- **The 95% band is pointwise.** At each $n$ between $10^3$ and $10^5$, 5.1% of 2,000 fair-coin paths are outside
  $p \pm 1.96\sqrt{p(1-p)/n}$, as it should be. But 53.1% of the paths have left the band at least once by $n = 10^3$
  and 74.4% by $n = 10^5$. By the law of the iterated logarithm every path leaves it infinitely often: from $n = 922$ on,
  the LIL envelope is wider than the band.
- **The accuracy of the normal approximation depends on p.** The exact Kolmogorov distance falls like $n^{-1/2}$ for
  every $p$, close to the Berry–Esseen bound. It stays below 0.01 from $n = 1{,}904$ for $p = 0.5$, from $n = 7{,}129$
  for $p = 0.1$ and from $n = 80{,}246$ for $p = 0.01$. At $n = 30$ it is 0.072 for a fair coin.
- **The continuity correction matters.** For $p = 0.5$ it reduces the distance at $n = 30$ from 0.072 to
  $9.2\times10^{-4}$. For skewed cases it helps much less, because the remaining error comes from skewness.
- **The spiky histograms were caused by the bins.** A sample proportion of 30 tosses takes values $1/30$ apart; the
  Freedman–Diaconis rule of version 1 used 72 bins of width 0.0097, so 51 bins were empty and the tallest bar was 3.5
  times the normal peak. Bins of width $1/n$ match the exact binomial probabilities.

All numbers are in `figures/*.csv` and in the project note.

## Changes from version 1

See [`NEWS.md`](NEWS.md). In short: the version 1 README described scripts and a `requirements.txt` that were not in
the repository; the histograms were not reproducible despite a fixed seed; the histogram bins were narrower than the
spacing of the possible values; the pointwise band was presented as a region a path stays in; and the R script set a
success probability that its simulation did not use.

## Limitations

Only independent tosses and three values of $p$ are studied. The Kolmogorov distance measures the largest error in a
probability, not the relative error in the tails. The thresholds for $D_n < 0.01$ are the first of 46 values of $n$ on
a logarithmic grid.

## References

- Freedman, D., Diaconis, P. (1981). On the histogram as a density estimator: $L_2$ theory. *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete*, 57(4), 453–476.
- Hartman, P., Wintner, A. (1941). On the law of the iterated logarithm. *American Journal of Mathematics*, 63, 169–176.
- Khintchine, A. (1924). Über einen Satz der Wahrscheinlichkeitsrechnung. *Fundamenta Mathematicae*, 6, 9–20.
- Shevtsova, I. G. (2011). On the absolute constants in the Berry–Esseen type inequalities for identically distributed summands. [arXiv:1111.6554](https://arxiv.org/abs/1111.6554)

## Citation

Citation metadata are in [`CITATION.cff`](CITATION.cff); GitHub shows them under "Cite this repository".

## Licence

MIT; see [`LICENSE`](LICENSE). The fonts in `fonts/` are distributed under the GUST Font License.
