from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

with figure_style():
    t = np.linspace(0, 1.25, 350)
    xis = np.linspace(-2.2, 2.2, 17)
    fig, ax = plt.subplots()
    for xi in xis:
        u0 = -np.tanh(xi)
        ax.plot(xi + t * u0, t)
    ax.axhline(1.0, linestyle='--', linewidth=1.3, label=r'$t_*=1$')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$t$')
    add_legend(ax)
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'burgers_characteristics', Path(__file__).resolve().parents[1] / 'generated')
