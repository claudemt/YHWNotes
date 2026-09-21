from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
from scipy.special import jv
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend

ells=np.arange(-8,9)
b1=1.6
b2=0.75
phases=[0.0,np.pi/2]
def amp(l,phi21):
    m=np.arange(-20,21)
    return np.sum(jv(l-2*m,2*b1)*jv(m,2*b2)*np.exp(1j*m*phi21))
with figure_style():
    fig,ax=plt.subplots()
    width=0.34
    for j,ph in enumerate(phases):
        P=np.array([abs(amp(int(l),ph))**2 for l in ells])
        ax.bar(ells+(j-0.5)*width,P,width=width,label=rf'$\Phi_{{21}}={ph/np.pi:.1f}\pi$',color=COLORS[j],alpha=0.78)
    ax.set_xlabel(r'energy sideband $\ell$')
    ax.set_ylabel(r'$P_\ell$')
    ax.set_xticks(ells[::2])
    polish_axes(ax,grid=False,minor_ticks=False)
    add_legend(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'multicolor_pinem', output_dir=ROOT/'figures'/'generated')
