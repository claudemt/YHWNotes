from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair, COLORS

with figure_style():
    s = np.linspace(0.0, 1.0, 500)
    fig, ax = plt.subplots()
    for i, alpha in enumerate([0.01, 0.05, 0.1, 0.3, 1.0]):
        ax.plot(s, s / (s + alpha), color=COLORS[i], linewidth=1.7,
                label=rf'$\alpha={alpha}$')
    ax.plot(s, s, color="0.4", linewidth=1.2, linestyle="--",
            label=r'no shrinkage $q=s$')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.05)
    ax.set_xlabel(r'eigenvalue $\lambda_i$'); ax.set_ylabel(r'ridge factor $\lambda_i/(\lambda_i+\alpha)$')
    ax.set_title(r'Ridge spectral shrinkage $\lambda_i/(\lambda_i+\alpha)$')
    add_legend(ax, loc='lower right')
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'ridge_spectrum', Path(__file__).resolve().parents[1] / 'generated')
print('ridge_spectrum done')
