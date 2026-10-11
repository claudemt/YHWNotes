"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# Unit sphere cylinder modes: e^(-(ell+nu)u); d=4 -> nu=1.
u=np.linspace(0,2.2,550)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.4,3.8))
    for i,ell in enumerate((0,1,2,5)):
        ax.plot(u,np.exp(-(ell+1)*u),color=COLORS[i],label=rf'$\ell={ell}$')
    ax.set(xlabel=r'Radial cylinder time $u=\log(r/R)$',ylabel=r'$\exp[-(\ell+1)u]$',xlim=(0,2.2),ylim=(0,1.045))
    add_legend(ax,'upper right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'cylinder_mode_decay',OUT)
