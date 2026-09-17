from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend
out=Path(__file__).resolve().parents[1]/'generated'
tau=np.geomspace(.003,.2,400)
R=.12*(4/3)/np.pi*np.log(1/tau)**2
with figure_style():
    fig,ax=plt.subplots(figsize=(7.2,4.5))
    ax.semilogx(tau,np.exp(-R),label='Double-log resummation')
    ax.semilogx(tau,1-R,ls='--',label='First-order expansion')
    ax.axhline(0,color='.5',lw=1)
    ax.set(xlabel=r'Thrust cut $\tau$',ylabel=r'Cumulative fraction $\Sigma_T(\tau)$',ylim=(-.8,1.35))
    polish_axes(ax)
    add_legend(ax,loc='upper left')
    fig.tight_layout()
    save_pdf_png_pair(fig,'qcd_thrust_sudakov',out)
    plt.close(fig)
