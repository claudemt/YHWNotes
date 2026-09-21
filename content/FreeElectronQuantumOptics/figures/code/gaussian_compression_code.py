from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
BOOK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT = BOOK_ROOT
sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend
u=np.linspace(-1,3,500) # t/t*
# normalized example: sigma_z^2=1, choose C=-0.6, sigma_p/m scaled so t*=1
# sigma^2=1-1.2u+0.6u^2 -> minimum 0.4 at u=1
s2=1-1.2*u+0.6*u**2
with figure_style():
    fig,ax=plt.subplots()
    ax.plot(u,np.sqrt(s2),color=COLORS[0])
    ax.axvline(1,linestyle='--',color=COLORS[1],label=r'$t=t_*$')
    ax.set_xlabel(r'$t/t_*$')
    ax.set_ylabel(r'$\sigma_z(t)/\sigma_z(0)$')
    polish_axes(ax,grid=True); add_legend(ax)
    fig.tight_layout(); save_pdf_png_pair(fig, 'gaussian_compression', output_dir=ROOT/'figures'/'generated')
