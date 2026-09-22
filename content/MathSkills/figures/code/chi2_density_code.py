from pathlib import Path
import sys
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair, COLORS

with figure_style():
    x = np.linspace(0.01, 30, 600)
    fig, ax = plt.subplots()
    for i, k in enumerate([1, 2, 5, 10, 20]):
        ax.plot(x, chi2.pdf(x, k), color=COLORS[i], linewidth=1.7,
                label=rf'$k={k}$')
    ax.set_xlim(0, 30); ax.set_ylim(0, 0.5)
    ax.set_xlabel(r'$x$'); ax.set_ylabel(r'density $f_k(x)$')
    ax.set_title(r'$\chi^2_k$ density for different degrees of freedom')
    add_legend(ax, loc='upper right')
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'chi2_density', Path(__file__).resolve().parents[1] / 'generated')
print('chi2_density done')
