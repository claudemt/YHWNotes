"""Exact unitary radial potentials for constant-curvature 3-spaces."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORS,figure_style,polish_axes,add_legend,save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
x=np.linspace(.72,2.44,640)
lam=2*3
adata=[x, np.sin(x), np.sinh(x)]
vdata=[lam/x**2,lam/np.sin(x)**2-1,lam/np.sinh(x)**2+1]
labels=[r'$\mathbb{R}^3$',r'$S^3$',r'$\mathbb{H}^3$']
with figure_style():
    fig, axs=plt.subplots(1,2,figsize=(9.3,3.55))
    for j in range(3):
        axs[0].plot(x,adata[j],c=COLORS[j],label=labels[j])
        axs[1].plot(x,vdata[j],c=COLORS[j],label=labels[j])
    axs[0].set(xlabel=r'$r/L$',ylabel=r'$a(r)/L$',xlim=(.7,2.47))
    axs[1].set(xlabel=r'$r/L$',ylabel=r'$L^2 V_{\ell=2}(r)$',xlim=(.7,2.47),ylim=(0,17.5))
    add_legend(axs[0],'upper left')
    add_legend(axs[1],'upper center')
    for ax in axs: polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'warped_radial_potentials',OUT)
