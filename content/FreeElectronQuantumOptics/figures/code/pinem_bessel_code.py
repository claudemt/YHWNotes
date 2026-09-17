from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

out = ROOT / "figures"
ell = np.arange(-12, 13)
beta = 2.5
P = jv(ell, 2 * beta) ** 2

with figure_style():
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    markerline, stemlines, _ = ax.stem(ell, P, linefmt="k-", markerfmt="ko", basefmt=" ")
    markerline.set_markerfacecolor("white")
    markerline.set_markeredgewidth(0.8)
    stemlines.set_linewidth(0.85)
    ax.set_xlabel(r"sideband $\ell$")
    ax.set_ylabel(r"$P_\ell=J_\ell^2(2|\beta|)$")
    ax.set_xticks(np.arange(-12, 13, 3))
    ax.set_ylim(bottom=0)
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout(pad=0.35)
    save_pdf_png_pair(fig, "pinem_bessel", output_dir=out)
