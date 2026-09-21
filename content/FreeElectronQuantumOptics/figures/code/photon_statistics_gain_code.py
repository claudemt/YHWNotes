from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend  # noqa: E402

out = ROOT / "figures"
k = np.arange(1, 6)
nbar = 3.0
coh = nbar**k / (factorial(k)**2)
thermal = factorial(k) * nbar**k / (factorial(k)**2)

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(k, coh, color="black", linestyle="-", marker="o", markerfacecolor="white", markeredgewidth=0.8, label="coherent")
    ax.plot(k, thermal, color="black", linestyle="--", marker="s", markerfacecolor="white", markeredgewidth=0.8, label="single-mode thermal")
    ax.set_yscale("log")
    ax.set_xlabel(r"gain order $k$")
    ax.set_ylabel(r"$P_{+k}/|g|^{2k}$")
    ax.set_xticks(k)
    add_legend(ax)
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout(pad=0.35)
    save_pdf_png_pair(fig, "photon_statistics_gain", output_dir=out)
