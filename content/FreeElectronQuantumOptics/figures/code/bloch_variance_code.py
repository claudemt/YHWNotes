from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
BOOK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT = BOOK_ROOT
sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend
x=np.linspace(0,4*np.pi,600)
# x = delta_B t
ratio=0.75
var_bloch=8*ratio**2*np.sin(x/2)**2
var_ball=2*(ratio*x)**2
with figure_style():
    fig,ax=plt.subplots()
    ax.plot(x/np.pi,var_bloch,label='linear detuning',color=COLORS[0])
    ax.plot(x/np.pi,var_ball,linestyle='--',label='zero detuning: ballistic walk',color=COLORS[1])
    ax.set_xlabel(r'$\delta_B t/\pi$')
    ax.set_ylabel(r'$\mathrm{Var}(\ell)$')
    polish_axes(ax,grid=True); add_legend(ax)
    fig.tight_layout(); save_pdf_png_pair(fig, 'bloch_variance', output_dir=ROOT/'figures'/'generated')
