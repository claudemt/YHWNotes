"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

# Exact squeezed-vacuum number distribution, including parity selection.
from scipy.special import gammaln
n=np.arange(0,15)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.5,3.8))
    for i,r in enumerate((.45,.85,1.25)):
        logs=gammaln(2*n+1)-2*gammaln(n+1)-n*np.log(4)+2*n*np.log(np.tanh(r))-np.log(np.cosh(r))
        ax.semilogy(2*n,np.exp(logs),marker=['o','s','^'][i],markersize=4.0,linewidth=1.7,color=COLORS[i],label=rf'$r={r:g}$')
    ax.set(xlabel=r'Even occupation number $2n$',ylabel=r'Probability $P_{2n}$',xlim=(-.4,28.5),ylim=(3e-8,1.1))
    add_legend(ax,'upper right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'squeezed_even_statistics',OUT)
