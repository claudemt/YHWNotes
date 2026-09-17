from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

with figure_style():
    s = np.linspace(0.015, 1.0, 1200)
    alpha1, alpha2, tau = 0.01, 0.04, 0.18
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    ax.plot(s, 1.0/s, label=r'formal inverse $1/s$')
    ax.plot(s, s/(s**2+alpha1), label=rf'Tikhonov $\alpha={alpha1}$')
    ax.plot(s, s/(s**2+alpha2), label=rf'Tikhonov $\alpha={alpha2}$')
    ax.plot(s, np.where(s >= tau, 1.0/s, 0.0), label=rf'TSVD $\tau={tau}$')
    ax.set_xlim(0, 1); ax.set_ylim(0, 12)
    ax.set_xlabel(r'singular value $s$'); ax.set_ylabel(r'filter $q(s)$')
    add_legend(ax, loc='upper right')
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'tikhonov_filter', Path(__file__).resolve().parents[1] / 'generated')
