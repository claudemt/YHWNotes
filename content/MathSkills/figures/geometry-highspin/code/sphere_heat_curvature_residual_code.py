"""Diagonal S2 heat kernel curvature coefficient via convergent spectral sums."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORS,REFERENCE_LINE_STYLE,figure_style,polish_axes,add_legend,save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
q=np.linspace(.018,.64,95)
res=[]
for v in q:
    max_l=int(np.ceil(np.sqrt(44/v)))+8
    l=np.arange(max_l+1)
    T=np.sum((2*l+1)*np.exp(-v*l*(l+1)))
    res.append((v*T-1-v/3)/v**2)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.7,3.7))
    ax.plot(q,res,c=COLORS[0],label=r'Exact spectral series')
    ax.axhline(1/15,**REFERENCE_LINE_STYLE,label=r'$1/15$ asymptotic coefficient')
    ax.set(xlabel=r'$q=t/R^2$',ylabel=r'$(4\pi tK_t(0)-1-q/3)/q^2$',xlim=(0,.66))
    add_legend(ax,'lower right');polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'sphere_heat_curvature_residual',OUT)
