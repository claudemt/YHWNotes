"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# Perturbative 4-epsilon scalar fixed point: leading ratio for even s>=2.
s=np.arange(2,65,2)
f=1-6/(s*(s+1))
with figure_style():
    fig,ax=plt.subplots(figsize=(6.4,3.8))
    ax.plot(s,f,color=COLORS[0],marker='o',markersize=3.5,label=r'$\gamma_s/\gamma_{\infty}$ at $O(\epsilon^2)$')
    ax.axhline(1,color=COLORS[1],linestyle='--',linewidth=1.5,label=r'Large-spin limit')
    ax.set(xlabel=r'Even spin $s$',ylabel=r'$1-6/[s(s+1)]$',xlim=(2,64),ylim=(-.03,1.06))
    add_legend(ax,'lower right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'anomalous_spin_profile',OUT)
