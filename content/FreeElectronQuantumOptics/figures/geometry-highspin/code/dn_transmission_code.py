"""Spectral cross-boundary coupling from the exact Dirichlet-to-Neumann matrix."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    frequencies=np.linspace(0.05,8.0,350)
    fig,ax=plt.subplots(figsize=(6.5, 4.0))
    for i,T in enumerate((0.5,1.0,2.0)):
        ratio=1/np.cosh(frequencies*T)
        ax.plot(frequencies,ratio,color=COLORS[i],label=rf'$T={T:g}$')
    ax.set_xlim(0,8);ax.set_ylim(0,1.02)
    ax.set_xlabel(r'Spectral frequency $\omega$')
    ax.set_ylabel(r'$|\Lambda_{12}|/\Lambda_{11}$')
    add_legend(ax, corner='upper right');polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'dn_transmission', OUT)
