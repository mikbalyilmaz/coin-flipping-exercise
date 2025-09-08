# coin-flipping-exercise
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A compact, reproducible simulation that demonstrates both the **Law of Large Numbers (LLN)** and the **Central Limit Theorem (CLT)** via coin tosses. The repository renders two coordinated panels—(A) a running mean (LLN) and (B) a sampling-distribution histogram with a Normal overlay (CLT)—across an extended sequence of sample sizes.

---

## What it shows
- **LLN (single path):** The running mean  
  \[
  \hat p_n=\frac{1}{n}\sum_{i=1}^n X_i
  \]
  stabilizes near \(p\) as \(n\) grows (for a fair coin \(p=0.5\)).
- **CLT (many paths):** For fixed \(N\), the distribution of \(\hat p\) over repeated experiments is approximately Normal,
  \[
  \hat p \approx \mathcal{N}\!\big(p,\;p(1-p)/N\big),
  \]
  and tightens as \(N\) increases.

---

## Key Features
- **Extended schedule:**  
  \[
  N \in \{5,\,30,\,100,\,300,\,800,\,1{,}000,\,2{,}500,\,4{,}000,\,10{,}000,\,50{,}000,\,100{,}000\}.
  \]
- **Notebook-safe by default:** No blocking `input()`. Optional `--interactive` for terminal use.
- **Adaptive repetitions (M):** More experiments for small/medium \(N\) → smoother, more Gaussian-looking histograms.
- **Adaptive binning:** Freedman–Diaconis rule with safeguards to avoid spiky histograms.
- **Deterministic seeding:** Fixed seed unless you pass `--seed None`.
- **Heads/Tails counts:** Printed for each \(N\).
- **Single-plot view (bonus):** One figure that overlays running means with 95% and \(3\sigma\) bands.

---

## Quick Start

### Prerequisites
- Python ≥ 3.9  
- Packages: `numpy`, `matplotlib`

Install:
    pip install numpy matplotlib
    # or:
    # pip install -r requirements.txt

### Run from the command line (recommended)
Save the main script as `coin_experiment.py`, then:
    # Default schedule; deterministic output
    python coin_experiment.py --p 0.5 --seed 42

    # Interactive stepping (press Enter to advance; 'q' to quit)
    python coin_experiment.py --interactive

    # Save each figure as PNG into ./plots
    python coin_experiment.py --outdir plots

    # Custom N schedule (comma-separated)
    python coin_experiment.py --ns "5,30,100,300,800,1000,2500,4000,10000,50000,100000"

    # Fresh randomness (no fixed seed)
    python coin_experiment.py --seed None

### Run in Jupyter / Notebook
The script ignores unknown ipykernel args and is safe to `%run`:
    %run coin_experiment.py --p 0.5 --seed 42
    # or with a custom schedule:
    %run coin_experiment.py --ns "5,30,100,300,800,1000,2500,4000,10000,50000,100000"

Alternatively, import and call the driver:
    from coin_experiment import run_experiment, NS_DEFAULT
    run_experiment(NS=NS_DEFAULT, p=0.5, seed=42, interactive=False, outdir=None)

**Single-plot view (running mean + bands):**
    from running_mean_single import plot_running_mean_single_graph

    # One path, save figure to ./plots
    plot_running_mean_single_graph(
        N=100_000, p=0.5, K=1, seed=42,
        save=True, outdir="plots", dpi=180, show=True
    )

    # Overlay multiple paths (not saved)
    # plot_running_mean_single_graph(N=100_000, p=0.5, K=8, seed=42, save=False, show=True)

---

## Methodological Notes
- **Model.** \(X_i \sim \mathrm{Bernoulli}(p)\), i.i.d.; heads \(=1\), tails \(=0\).
- **LLN panel (A).** Log-scale \(n\) axis highlights early fluctuations and long-run stabilization around \(p\).
- **CLT panel (B).** Builds \(\{\hat p^{(j)}\}_{j=1}^M\) from \(M\) independent experiments of size \(N\); overlays \(\mathcal{N}(p,\,p(1-p)/N)\).
- **Smoothing.** \(M\) and histogram bins are chosen adaptively (Freedman–Diaconis) to balance fidelity and runtime.

---

## License
© Licensed under the **MIT License** — free to use, modify, and distribute with attribution.

---

## How to Cite
> Yılmaz, M. İ. (2025). *coin-flipping-exercise*. GitHub. https://github.com/mikbalyilmaz/coin-flipping-exercise

**APA citation:**  
Yılmaz, M. İ. (2025). *coin-flipping-exercise*. GitHub. Retrieved September 8, 2025, from https://github.com/mikbalyilmaz/coin-flipping-exercise

**BibTeX:**
    @misc{coin_flipping_exercise_2025,
      author       = {Muhammed İkbal Yılmaz},
      title        = {coin-flipping-exercise},
      year         = {2025},
      howpublished = {\url{https://github.com/mikbalyilmaz/coin-flipping-exercise}},
      note         = {Accessed: 2025-09-08}
    }
