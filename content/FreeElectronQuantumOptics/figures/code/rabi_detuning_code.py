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
x = np.linspace(0, 4 * np.pi, 500)
styles = ["-", "--", ":"]

with figure_style():
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for d, ls in zip([0, 1, 2], styles):
        OmR = np.sqrt(1 + d * d)
        Pe = (1 / OmR**2) * np.sin(OmR * x / 2) ** 2
        ax.plot(x / np.pi, Pe, color="black", linestyle=ls, label=rf"$\Delta/|\Omega|={d}$")
    ax.set_xlabel(r"$|\Omega|t/\pi$")
    ax.set_ylabel(r"$P_e$")
    ax.set_ylim(-0.03, 1.24)
    add_legend(ax, corner="upper right")
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout(pad=0.35)
    save_pdf_png_pair(fig, "rabi_detuning", output_dir=out)
