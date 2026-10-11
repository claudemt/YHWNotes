"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

# Dirichlet Laplacian on (0, pi): k_n = n, n=1,2,...
k=np.linspace(0,20,1601)
N=np.floor(k).astype(int)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.4,3.75))
    ax.step(k,N,where='post',color=COLORS[0],label=r'Exact $N(k)$')
    ax.plot(k,k,color=COLORS[1],linestyle='--',label=r'Leading Weyl term $k$')
    ax.set(xlabel=r'Wave number $k$',ylabel=r'Number of eigenvalues $\leq k^2$',xlim=(0,20),ylim=(0,21))
    ax.set_xticks([0,5,10,15,20]); add_legend(ax,'upper left');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'weyl_staircase',OUT)
