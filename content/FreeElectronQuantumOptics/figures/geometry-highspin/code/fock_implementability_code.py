"""Partial Hilbert-Schmidt norms for diagonal Bogoliubov power laws."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORS, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'
n=np.arange(1,100001,dtype=float)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.8,3.85))
    for i,p in enumerate((0.4,0.5,0.7,1.0)):
        t=np.cumsum((n+1)**(-2*p))
        at=np.unique(np.geomspace(1,len(n),450).astype(int))-1
        ax.plot(n[at],t[at],label=rf'$p={p:g}$',color=COLORS[i])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(0.3,100)
    ax.set(xlim=(1,1e5),xlabel=r'Number of modes $N$',ylabel=r'$\sum_{j=1}^{N}|\beta_j|^2$')
    add_legend(ax,corner='upper left',ncol=1);polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'fock_implementability',OUT)
