"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# Exact k_{2h}(1-y) versus leading Bessel kernel along y=(xi/(2h))^2.
from scipy.special import hyp2f1, gammaln, k0
xi=np.linspace(.55,4.3,190)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.5,3.8))
    for i,h in enumerate((12,24,48)):
        y=(xi/(2*h))**2
        z=1-y
        exact=np.exp(2*gammaln(h)-gammaln(2*h)-np.log(2))*z**h*hyp2f1(h,h,2*h,z)
        rel=np.abs(exact/k0(xi)-1)
        ax.semilogy(xi,rel,color=COLORS[i],label=rf'$h={h}$')
    ax.set(xlabel=r'Joint scaling variable $\xi=2h\sqrt{y}$',ylabel=r'$|k_{2h}(1-y)/(C_h K_0(\xi))-1|$',xlim=(.55,4.3),ylim=(3e-4,3))
    add_legend(ax,'lower right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'lightcone_bessel_error',OUT)
