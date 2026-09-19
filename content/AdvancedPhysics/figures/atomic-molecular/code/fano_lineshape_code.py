from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair
with figure_style():
    eps=np.linspace(-5,5,1000); fig,ax=plt.subplots()
    for q in [-1.0,0.0,1.0,3.0]: ax.plot(eps,(q+eps)**2/(1+eps**2),label=rf'$q={q:g}$')
    ax.axvline(0,lw=0.8,alpha=0.35); ax.set_xlabel(r'Reduced detuning $\epsilon$'); ax.set_ylabel(r'$\sigma/\sigma_{\rm bg}$'); ax.set_ylim(0,10.6)
    add_legend(ax,loc='upper left',frameon=False,ncol=2); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'fano_lineshape',Path(__file__).resolve().parents[1]/'generated')
