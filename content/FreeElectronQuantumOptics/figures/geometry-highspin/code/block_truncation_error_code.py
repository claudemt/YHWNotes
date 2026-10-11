"""Exact relative truncation errors for the diagonal d=4 scalar conformal block."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    x=.5
    rho=x/(1+np.sqrt(1-x))**2
    q=rho**2
    n=np.arange(1,11)
    z_error=x**n
    rho_error=q**n*(n+1-n*q)
    fig,ax=plt.subplots(figsize=(6.5, 4.0))
    ax.semilogy(n,z_error,'-o',color=COLORS[0],markersize=4,label=r'$z$-series')
    ax.semilogy(n,rho_error,'-s',color=COLORS[1],markersize=4,label=r'$\rho$-series')
    ax.set_xticks(n)
    ax.set_xlim(1,10)
    ax.set_ylim(1e-16,1)
    ax.set_xlabel(r'Number of nonzero terms $N$')
    ax.set_ylabel('Exact relative truncation error')
    add_legend(ax, corner='upper right')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'block_truncation_error', OUT)
