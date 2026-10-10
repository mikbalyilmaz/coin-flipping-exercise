"""Writes every number and table of the project notes from ../figures/*.csv, so that the text cannot drift
away from the analysis. Run from inside paper/:  python make_paper.py

Output, once in English (suffix _en, for coin_note.tex) and once in Turkish (suffix _tr, for coin_notu.tex):
numbers_xx.tex (one macro per quoted number) and tab_clt_xx.tex (table body ending with its bottom rule,
because a rule cannot follow \\input directly inside a tabular).
"""

import csv
import math
from pathlib import Path

FIG = Path(__file__).resolve().parents[1] / "figures"
OUT = Path(__file__).resolve().parent


def read(name):
    with open(FIG / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


lln = read("table2_lln_summary")[0]
clt = {r["p"]: r for r in read("table4_clt_summary")}
hist = read("table5_histogram")[0]

SEP = {"en": {"big": "{,}", "dec": "."}, "tr": {"big": ".", "dec": "{,}"}}


def build(lang):
    t = SEP[lang]

    def dec(x, d):
        return f"{float(x):.{d}f}".replace(".", t["dec"])

    def num(x):
        return f"{round(float(x)):,}".replace(",", t["big"])

    def sci(x, d=1):
        mant, exp = f"{float(x):.{d}e}".split("e")
        return f"{mant.replace('.', t['dec'])}\\times 10^{{{int(exp)}}}"

    def small(x):
        # three significant digits; scientific notation below 0.001
        x = float(x)
        return f"${sci(x, 1)}$" if x < 1e-3 else dec(x, max(0, 2 - math.floor(math.log10(x))))

    m = {}
    m["Paths"] = num(lln["paths"])
    m["ShareNow"] = dec(100 * float(lln["share_outside_at_n_mean_1e3_to_1e5"]), 1)
    m["ShareByThousand"] = dec(100 * float(lln["share_outside_by_1e3"]), 1)
    m["ShareByMax"] = dec(100 * float(lln["share_outside_by_1e5"]), 1)
    share = float(lln["share_outside_by_1e5"])
    m["ShareByMaxSe"] = dec(100 * math.sqrt(share * (1 - share) / float(lln["paths"])), 1)
    m["RmsSlope"] = dec(lln["rms_slope_n_ge_1e3"], 3)
    m["RmsOverSe"] = dec(lln["rms_over_se_at_1e5"], 3)
    m["LilFrom"] = num(lln["lil_wider_than_band_from_n"])
    m["LilThreeSigma"] = sci(math.exp(math.exp(4.5)), 1)

    for key, p in (("Half", "0.5"), ("Tenth", "0.1"), ("Hundredth", "0.01")):
        r = clt[p]
        m[f"NBelow{key}"] = num(r["n_for_distance_below_0.01"])
        m[f"Slope{key}"] = dec(r["slope_n_ge_1e3"], 3)
    r = clt["0.5"]
    m["DHalfThirty"] = dec(r["D_at_30"], 3)
    m["DccHalfThirty"] = small(r["Dcc_at_30"])
    m["DHalfThousand"] = dec(r["D_at_1000"], 4)
    m["DccHalfThousand"] = small(r["Dcc_at_1000"])
    m["DccHalfTenThousand"] = small(r["Dcc_at_10000"])
    m["DccRatioHalf"] = dec(float(r["Dcc_at_1000"]) / float(r["Dcc_at_10000"]), 1)
    r = clt["0.1"]
    m["DccRatioTenth"] = dec(float(r["Dcc_at_1000"]) / float(r["Dcc_at_10000"]), 2)
    m["DRootNHalf"] = dec(float(clt["0.5"]["D_at_10000"]) * 100, 4)
    m["DHundredthThirty"] = dec(clt["0.01"]["D_at_30"], 2)
    m["BeOverDHalf"] = dec(float(clt["0.5"]["BE_at_1000"]) / float(clt["0.5"]["D_at_1000"]), 2)
    m["BeOverDHundredth"] = dec(float(clt["0.01"]["BE_at_1000"]) / float(clt["0.01"]["D_at_1000"]), 2)

    m["HistN"] = num(hist["n"])
    m["HistM"] = num(hist["experiments"])
    m["VoneBins"] = num(hist["v1_bins"])
    m["VoneWidth"] = dec(hist["v1_bin_width"], 4)
    m["Spacing"] = dec(hist["lattice_spacing"], 4)
    m["VoneEmpty"] = num(hist["v1_empty_bins"])
    m["VoneMax"] = dec(hist["v1_max_height"], 1)
    m["LatticeMax"] = dec(hist["lattice_max_height"], 2)
    m["ExactMax"] = dec(hist["exact_max_height"], 2)
    m["NormalPeak"] = dec(hist["normal_peak"], 2)
    m["PeakRatio"] = dec(float(hist["v1_max_height"]) / float(hist["normal_peak"]), 1)

    (OUT / f"numbers_{lang}.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in m.items()), encoding="utf-8")

    lines = []
    for p in ("0.5", "0.1", "0.01"):
        r = clt[p]
        cells = [f"${dec(p, len(p) - 2)}$"]
        for n in ("30", "100", "1000", "10000"):
            cells += [small(r[f"D_at_{n}"]), small(r[f"Dcc_at_{n}"])]
        cells.append(num(r["n_for_distance_below_0.01"]))
        lines.append(" & ".join(cells) + " \\\\")
    lines.append("\\bottomrule")
    (OUT / f"tab_clt_{lang}.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


for lang in ("en", "tr"):
    build(lang)
print("Wrote numbers_*.tex and tab_clt_*.tex (en, tr).")
