"""Common set-up for the analysis scripts: import path, seed and a CSV writer."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from coinsim.style import FIG_DIR  # noqa: E402

SEED = 20261010
P = 0.5  # fair coin, as in version 1


def save_table(rows, name):
    """Write a list of dicts as figures/<name>.csv."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(FIG_DIR / f"{name}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote figures/{name}.csv ({len(rows)} rows)")
