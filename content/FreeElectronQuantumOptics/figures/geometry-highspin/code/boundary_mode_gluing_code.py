"""Exact mode-by-mode boundary coupling in an Euclidean Gaussian cylinder."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'
T = np.linspace(0.17, 3.0, 700)
with figure_style():
    fig, ax = plt.subplots(figsize=(6.4, 3.65))
    for i, w in enumerate([1, 2, 4]):
        ax.semilogy(T, w / np.sinh(w*T), color=COLORS[i], label=rf'$\omega={w}$')
    ax.set(xlabel=r'Euclidean separation $T$', ylabel=r'Endpoint coupling $\omega/\sinh(\omega T)$', xlim=(T.min(),T.max()), ylim=(1e-4,8))
    add_legend(ax, 'lower left')
    polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'boundary_mode_gluing', OUT)
