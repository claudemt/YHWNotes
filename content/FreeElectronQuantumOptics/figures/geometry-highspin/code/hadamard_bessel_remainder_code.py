"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# Massive Euclidean Green function in dimension two: G=K_0(mr)/(2 pi).
from scipy.special import k0
r=np.geomspace(.02,1.8,650)
G=k0(r)/(2*np.pi)
local=(-np.log(r/2)-np.euler_gamma)/(2*np.pi)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.5,3.8))
    ax.plot(r,G,color=COLORS[0],label=r'$G_m(r)=K_0(mr)/(2\pi)$')
    ax.plot(r,local,color=COLORS[1],linestyle='--',label='Leading local singularity')
    ax.plot(r,G-local,color=COLORS[2],label='Residual after leading log')
    ax.set(xlabel=r'Dimensionless distance $mr$',ylabel=r'Green function / subtracted part',xlim=(.02,1.8))
    add_legend(ax,'upper right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'hadamard_bessel_remainder',OUT)
