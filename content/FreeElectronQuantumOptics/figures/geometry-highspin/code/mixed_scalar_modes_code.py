"""Generalized-free two-primary highest-weight mode distributions."""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt

import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    S = 16
    k = np.arange(S + 1)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    for j, (da, db) in enumerate(((1, 1), (1, 5), (2, 8))):
        logw = np.array([
            -math.lgamma(i+1) - math.lgamma(S-i+1)
            -math.lgamma(da+i) + math.lgamma(da)
            -math.lgamma(db+S-i) + math.lgamma(db)
            for i in k
        ])
        weights = np.exp(logw-logw.max())
        p = weights / weights.sum()
        assert np.isclose(p.sum(), 1.0, atol=1e-12)
        ax.plot(k,p,'o-',color=COLORS[j],label=rf'$\Delta_A={da},\ \Delta_B={db}$', markersize=4)
    ax.set_xlim(3, 14)
    ax.set_ylim(0, 0.34)
    ax.set_xlabel(r'Derivatives assigned to $A$: $k$')
    ax.set_ylabel(r'$p_k^{AB}$')
    add_legend(ax, corner='upper right')
    polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'mixed_scalar_modes', OUT)
