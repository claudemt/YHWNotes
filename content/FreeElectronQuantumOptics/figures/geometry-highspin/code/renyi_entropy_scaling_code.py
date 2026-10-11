"""Finite-spin errors: exact entropies minus leading asymptotics, scaled by S."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from math import lgamma, log, pi, e
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    ss=np.arange(2, 102, 2)
    delta1=[];delta2=[]
    for s in ss:
        ks=np.arange(s+1)
        lp=np.array([2*(lgamma(s+1)-lgamma(int(k)+1)-lgamma(s-int(k)+1))
                     -(lgamma(2*s+1)-2*lgamma(s+1)) for k in ks])
        p=np.exp(lp);p/=sum(p)
        h1=-np.dot(p,np.log(p))
        h2=-log(np.dot(p,p))
        delta1.append(s*(h1-.5*log(pi*e*s/4)))
        delta2.append(s*(h2-.5*log(pi*s/2)))
    fig,ax=plt.subplots(figsize=(6.5, 4.0))
    ax.plot(ss,delta1,color=COLORS[0],label=r'$S(H_1-H_1^{(0)})$')
    ax.plot(ss,delta2,color=COLORS[1],label=r'$S(H_2-H_2^{(0)})$')
    ax.axhline(.25,color=COLORS[0],linestyle=':',linewidth=1.5,label=r'$1/4$')
    ax.axhline(5/16,color=COLORS[1],linestyle=':',linewidth=1.5,label=r'$5/16$')
    ax.set_xlabel(r'Even spin $S$')
    ax.set_ylabel(r'$S$ times finite-spin correction')
    ax.set_xlim(2,100)
    ax.set_ylim(.205,.335)
    add_legend(ax, corner='lower right', ncol=2)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'renyi_entropy_scaling', OUT)
