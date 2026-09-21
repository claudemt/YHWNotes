from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
BOOK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT = BOOK_ROOT
sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend
k=np.linspace(-1.2,1.2,400)
beta=0.70
with figure_style():
    fig,ax=plt.subplots()
    ax.plot(k,np.abs(k),label=r'light cone $\omega/c=|k_z|$',color=COLORS[1])
    ax.plot(k,beta*np.abs(k),linestyle='--',label=r'electron $\omega/c=\beta_0|k_z|$',color=COLORS[0])
    ax.fill_between(k,beta*np.abs(k),np.abs(k),alpha=.12,color=COLORS[2])
    ax.set_xlabel(r'$k_z/k_0$')
    ax.set_ylabel(r'$\omega/(ck_0)$')
    ax.set_xlim(-1.2,1.2); ax.set_ylim(0,1.25)
    polish_axes(ax,grid=True); add_legend(ax)
    fig.tight_layout(); save_pdf_png_pair(fig, 'light_cone_synchronism', output_dir=ROOT/'figures'/'generated')
