from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
from scipy.special import gammaln
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend

n=np.arange(0,13)
with figure_style():
    fig,ax=plt.subplots()
    for j,g in enumerate([0.7,1.4,2.2]):
        lam=g*g
        P=np.exp(-lam+n*np.log(lam+1e-300)-gammaln(n+1))
        ax.plot(n,P,marker='o',label=rf'$|g|={g}$',color=COLORS[j])
    ax.set_xlabel(r'$n=-\ell$')
    ax.set_ylabel(r'$P_n$')
    ax.set_xticks(n)
    polish_axes(ax,grid=True,minor_ticks=False)
    add_legend(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'qpin_vacuum_poisson', output_dir=ROOT/'figures'/'generated')
