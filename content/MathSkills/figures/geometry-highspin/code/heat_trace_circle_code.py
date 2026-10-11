"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

# S^1 of radius 1: eigenvalues n^2, n in integers.
t=np.linspace(0.06,6.0,550)
n=np.arange(-65,66)
theta=np.sum(np.exp(-t[:,None]*n[None,:]**2),axis=1)
leading=np.sqrt(np.pi/t)
relative=theta/leading-1
with figure_style():
    fig,ax=plt.subplots(figsize=(6.4,3.7))
    ax.plot(t,relative,color=COLORS[0],label=r'$\Theta(t)/\sqrt{\pi/t}-1$')
    ax.axhline(0,**REFERENCE_LINE_STYLE)
    ax.set(xlabel=r'Heat time $t/R^2$',ylabel='Relative correction',xlim=(.06,6.0),ylim=(-.025,.45))
    add_legend(ax,'upper left'); polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'heat_trace_circle',OUT)
