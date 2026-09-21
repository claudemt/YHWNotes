from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend

q=np.arange(0,13)
lam=800e-9
c=299792458.0
omega=2*np.pi*c/lam
with figure_style():
    fig,ax=plt.subplots()
    for j,sigma_as in enumerate([50,100,250]):
        st=sigma_as*1e-18
        V=np.exp(-0.5*(q*omega*st)**2)
        ax.plot(q,V,marker='o',label=rf'$\sigma_t={sigma_as}\,\mathrm{{as}}$',color=COLORS[j])
    ax.set_xlabel(r'diagonal distance $q$')
    ax.set_ylabel(r'visibility $V_q$')
    ax.set_ylim(-0.02,1.04)
    ax.set_xticks(q)
    polish_axes(ax,grid=True,minor_ticks=False)
    add_legend(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'tomography_jitter_visibility', output_dir=ROOT/'figures'/'generated')
