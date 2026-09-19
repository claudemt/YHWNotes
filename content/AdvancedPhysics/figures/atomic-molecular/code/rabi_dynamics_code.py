from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair
with figure_style():
    x=np.linspace(0,4*np.pi,700); fig,ax=plt.subplots()
    for d in [0.0,1.0,2.0]:
        OmR=np.sqrt(1+d*d); ax.plot(x,(1/OmR**2)*np.sin(OmR*x/2)**2,label=rf'$\Delta/\Omega={d:g}$')
    ax.set_xlabel(r'Pulse time $\Omega t$'); ax.set_ylabel(r'Excited-state probability $P_e$'); ax.set_ylim(0,1.04)
    add_legend(ax,loc='upper center',frameon=False); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'rabi_dynamics',Path(__file__).resolve().parents[1]/'generated')
