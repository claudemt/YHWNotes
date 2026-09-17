from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
BOOK_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[4]
ROOT = BOOK_ROOT
sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend
K=np.linspace(0,1000,500) # keV
gamma=1+K/511.0
with figure_style():
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(K,gamma,label=r'$m_\perp/m_e=\gamma$',color=COLORS[1])
    ax.plot(K,gamma**3,label=r'$m_\parallel/m_e=\gamma^3$',color=COLORS[0])
    ax.set_xlabel(r'$K$ [keV]')
    ax.set_ylabel('mass ratio')
    polish_axes(ax,grid=True)
    add_legend(ax, frameon=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'relativistic_effective_mass', output_dir=ROOT/'figures'/'generated')
