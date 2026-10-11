"""Scalar-Casimir spectral shifts of homogeneous line-bundle rough Laplacians."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORS,REFERENCE_LINE_STYLE,figure_style,polish_axes,add_legend,save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
with figure_style():
    fig,ax=plt.subplots(figsize=(7.2,4.1))
    for s in range(4):
        ell=np.arange(s,9)
        ax.scatter(ell,np.full_like(ell,-s*s),s=23+7*(2*ell+1),color=COLORS[s],
                   alpha=.83,edgecolors='white',linewidths=.7,label=rf'$s={s}$')
    ax.set(xlabel=r'$SO(3)$ angular momentum $\ell$',ylabel=r'$\lambda_{\ell,s}-\ell(\ell+1)$',
           xlim=(-.6,8.6),ylim=(-10.4,3.5))
    ax.set_xticks(range(9));ax.set_yticks([-9,-4,-1,0])
    add_legend(ax,'upper right',ncol=2);polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'spin_weight_bundle_spectrum',OUT)
