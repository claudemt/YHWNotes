from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend
out=Path(__file__).resolve().parents[1]/'generated'
energy=np.geomspace(10,150,240)
alpha=.18/(1+(23/3)*.18*np.log((energy/10)**2)/(4*np.pi))
q=15/31+(.6-15/31)*(alpha/.18)**(62/69)
with figure_style():
    fig,ax=plt.subplots(figsize=(7.2,4.5))
    ax.semilogx(energy,q,label='Quarks + antiquarks',color='C0')
    ax.semilogx(energy,1-q,label='Gluons',color='C1')
    ax.axhline(15/31,ls='--',color='C0',lw=1)
    ax.axhline(16/31,ls='--',color='C1',lw=1)
    ax.set(xlabel=r'Factorization energy $c\mu_{\rm F}$ (GeV)',ylabel='Longitudinal momentum fraction',ylim=(.33,.67))
    polish_axes(ax)
    add_legend(ax,loc='upper right')
    fig.tight_layout()
    save_pdf_png_pair(fig,'qcd_momentum_evolution',out)
    plt.close(fig)
