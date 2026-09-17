from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend  # noqa: E402

out = ROOT / "figures"
x = np.linspace(0, 2.5, 400)
styles = ["-", "--", ":"]

with figure_style():
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for dl, ls in zip([1, 2, 4], styles):
        y = np.exp(-0.5 * dl**2 * x)
        ax.plot(x, y, color="black", linestyle=ls, label=rf"$|\ell-m|={dl}$")
    ax.set_xlabel(r"$\Gamma_\phi t$")
    ax.set_ylabel(r"$|\rho_{\ell m}(t)|/|\rho_{\ell m}(0)|$")
    ax.set_ylim(-0.02, 1.03)
    add_legend(ax)
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout(pad=0.35)
    save_pdf_png_pair(fig, "dephasing_coherence", output_dir=out)
