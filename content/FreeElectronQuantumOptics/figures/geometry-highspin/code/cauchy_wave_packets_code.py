"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# 1+1 wave equation with Gaussian u(0,x) and vanishing initial velocity.
x=np.linspace(-5,5,850)
sigma=.55
with figure_style():
    fig,ax=plt.subplots(figsize=(6.5,3.8))
    for i,t in enumerate((0,.8,1.6,2.5)):
        u=.5*(np.exp(-.5*((x-t)/sigma)**2)+np.exp(-.5*((x+t)/sigma)**2))
        ax.plot(x,u,color=COLORS[i],label=rf'$ct={t:g}$')
    ax.set(xlabel=r'Position $x$',ylabel=r'$u(t,x)$',xlim=(-5,5),ylim=(0,1.06))
    add_legend(ax,'upper right',ncol=2);polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'cauchy_wave_packets',OUT)
