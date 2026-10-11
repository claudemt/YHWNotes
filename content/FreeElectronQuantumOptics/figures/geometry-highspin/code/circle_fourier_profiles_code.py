"""Departure from first non-Gaussian correction at finite spin."""
from pathlib import Path
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'
with figure_style():
    x=np.linspace(-2.25,2.25,600)
    phi=np.exp(-x*x/2)/np.sqrt(2*np.pi)
    a1=phi*(1/8-x**4/24)
    fig,ax=plt.subplots(figsize=(6.5,4.0))
    for color,S in zip(COLORS,(4,12,64)):
        eta=x*np.sqrt(2/S)
        logp=S*math.log(4)-math.log(2*math.pi)-(math.lgamma(2*S+1)-2*math.lgamma(S+1))
        scaled=np.sqrt(2/S)*np.exp(logp+2*S*np.log(np.cos(eta/2)))
        residual=S*(scaled-phi)-a1
        ax.plot(x,residual,color=color,label=rf'$S={S}$')
    ax.axhline(0,**REFERENCE_LINE_STYLE,label=r'first-order asymptotic')
    ax.set(xlabel=r'$x=\sqrt{S/2}\,\eta$',
           ylabel=r'$S(q_S^{(x)}-\phi)-\phi(1/8-x^4/24)$')
    ax.set_xlim(-2.25,2.25)
    polish_axes(ax,grid=True)
    ax.set_ylim(-0.00335,0.0017)
    add_legend(ax,corner='upper right',ncol=2)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'circle_fourier_profiles',OUT)
