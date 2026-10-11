"""Finite-spin errors of the exact hypergeometric mode distribution."""
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
    fig,ax=plt.subplots(figsize=(6.5,4.0))
    for i,S in enumerate((8,32,128)):
        k=np.arange(S+1)
        logp=np.array([2*math.lgamma(S+1)-2*math.lgamma(j+1)-2*math.lgamma(S-j+1)
           -math.lgamma(2*S+1)+2*math.lgamma(S+1) for j in k])
        p=np.exp(logp)
        assert abs(p.sum()-1)<1e-10
        x=(k-S/2)/np.sqrt(S)
        gauss=2/np.sqrt(np.pi)*np.exp(-4*x*x)
        mask=np.abs(x)<=.75
        ax.plot(x[mask],(np.sqrt(S)*p-gauss)[mask],'-o',color=COLORS[i],
                markersize=3.6,label=rf'$S={S}$')
    ax.axhline(0,**REFERENCE_LINE_STYLE,label='Gaussian limit')
    ax.set(xlabel=r'$(k-S/2)/\sqrt{S}$',
           ylabel=r'$\sqrt{S}\,p_k-2e^{-4x^2}/\sqrt{\pi}$')
    ax.set_xlim(-.78,.78)
    polish_axes(ax,grid=True)
    add_legend(ax,corner='lower right')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'mode_occupation',OUT)
