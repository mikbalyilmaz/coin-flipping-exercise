# Changes

## Version 2.1.0

No result changed: every table and every number in the notes is the same as in version 2.0.0.

- Figures redrawn in the style of the charts on muhammedikbalyilmaz.com: series in black and deep blue (#0033a0),
  red dotted lines for dates and reference values, labels at the end of the lines where possible, bold panel titles,
  Latin Modern Roman. Every figure is 4.75 inches wide, the width of the text in the notes.
- Every figure is drawn in English and in Turkish (decimal comma), as before.
- Axis rule: every value axis starts and ends at a labelled tick, and there are no minor ticks. Before a figure is
  saved, `coinsim/style.py` checks it and stops with an error if an axis limit is not a labelled tick, if two pieces of
  text overlap, if a note or a legend lies on a data line, or if a note leaves its panel.
- The colour words in the notes were changed to match the new figures.
- The project notes now use the note template: 11 pt, A4, 4.5 cm side margins, a header with the short name and
  the compilation date, and the page count. Wide equations and tables were split or set in a smaller size to fit the
  narrower text block.
- References: one paragraph per entry with a 1.27 cm hanging indent, an ampersand before the last author (APA 7) and
  the issue number of *American Journal of Mathematics* 63(1).
- Compiled Python files (`__pycache__/`) and LaTeX build files (`paper/*.aux`, `paper/*.log`) that had been
  committed are removed from the repository; `.gitignore` already excluded them.

## Version 2.0.0

### New

- `coinsim/` holds the simulation and the exact computations; the analyses and the tests are separate from it.
- Exact binomial probabilities, the exact Kolmogorov distance to the normal approximation (with and without continuity
  correction), the Berry–Esseen bound and the envelope of the law of the iterated logarithm.
- Unit tests (`tests/run_tests.py`) against exact rational arithmetic, plain loops, a brute-force search and the
  Berry–Esseen bound.
- Three analyses with fixed seeds, three figures (English and Turkish), CSV tables, and a project note in English and
  Turkish whose numbers are written from the tables.
- `CITATION.cff`, `requirements.txt`.

### Corrections to version 1

| # | Version 1 | Version 2 |
|---|---|---|
| 1 | The README told users to run `coin_experiment.py` and `running_mean_single.py` and to install from `requirements.txt`; none of these files was in the repository. The code existed only inside the notebook. | Code in the `coinsim` package and in `analysis/`; `requirements.txt` included; the README describes only files that exist. |
| 2 | The output was described as deterministic with `--seed 42`, but the histograms used a generator created with `seed=None`, so they changed at every run. | Every random number comes from a fixed seed. |
| 3 | Histogram bins came from the Freedman–Diaconis rule, which assumes continuous data. For $n = 30$ it gave 72 bins of width 0.0097 for values $1/30$ apart: 51 bins were empty and the tallest bar was 3.5 times the normal peak. | Bins of width $1/n$ centred on the possible values; the effect of the old rule is shown in analysis 3. |
| 4 | The band $p \pm 1.96\,\mathrm{SE}$ around a running mean was presented as a 95% band for the path. It holds only at each fixed $n$. | Analysis 1 measures both: 5.1% of paths are outside at a given $n$, but 74.4% have left the band by $n = 10^5$, and by the law of the iterated logarithm every path leaves it infinitely often. |
| 5 | The normal approximation was judged by eye from simulated histograms, and the running mean was said to be "very close to 0.5" by $n \gtrsim 10^4$. | The distance to the normal approximation is computed exactly and compared with the Berry–Esseen bound for three values of $p$; closeness is stated through the standard error. |
| 6 | The R script set `p_success <- 0.5677` but used it for a single draw only; the coin simulation used a fair `sample()` and a reference line at 0.5. | The R script is kept unchanged in `legacy/`; version 2 uses one parameter $p$ throughout. |
| 7 | An HTML and a PDF export duplicated the notebook; the `plots/` folder held outputs of the notebook and the R script; the README contained a note on typesetting math on GitHub. | Version 1 kept as `legacy/coin_experiment_v1.ipynb` and `legacy/bernoulli_simulation_v1.R`; the exports and plots remain in the `v1.0.0` release. |

## Version 1.0.0

First version: a notebook that shows a running mean and histograms of sample proportions for sample sizes from 5 to
100,000, and an R script that simulates 1,000 coin tosses.
