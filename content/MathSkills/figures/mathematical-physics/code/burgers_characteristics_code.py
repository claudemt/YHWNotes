from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

with figure_style():
    t = np.linspace(0, 1.25, 350)
    xis = np.linspace(-2.2, 2.2, 17)
    fig, ax = plt.subplots(figsize=(6.4, 4.5))
    for xi in xis:
        u0 = -np.tanh(xi)
        ax.plot(xi + t * u0, t)
    ax.axhline(1.0, linestyle='--', linewidth=1.3, label=r'$t_*=1$')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$t$')
    ax.set_title(r'Characteristics for $u_0(\xi)=-\tanh\xi$')
    add_legend(ax, loc='upper left')
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'burgers_characteristics', Path(__file__).resolve().parents[1] / 'generated')
