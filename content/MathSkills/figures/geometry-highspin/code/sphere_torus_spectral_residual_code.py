"""Weyl-law spectral staircase residual for equal-area sphere and square torus."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

with figure_style():
    lam=np.linspace(20,230,1000)
    ell=np.floor((-1+np.sqrt(1+4*lam))/2).astype(int)
    nsphere=(ell+1)**2
    m=np.arange(-10,11)
    i,j=np.meshgrid(m,m)
    eigen=np.sort((np.pi*(i*i+j*j)).ravel())
    ntorus=np.searchsorted(eigen,lam,side='right')
    fig,ax=plt.subplots(figsize=(6.5, 4.0))
    for idx,(N,label) in enumerate(((nsphere,r'$S^2$'),(ntorus,r'Flat $T^2$'))):
        residual=(N-lam)/np.sqrt(lam)
        ax.plot(lam,residual,color=COLORS[idx],label=label,lw=1.45)
    ax.axhline(0,color='gray',alpha=.5,lw=.8)
    ax.set_xlim(20,230)
    ax.set_xlabel(r'Laplace eigenvalue threshold $\Lambda$')
    ax.set_ylabel(r'$(N(\Lambda)-\Lambda)/\sqrt{\Lambda}$')
    add_legend(ax, corner='upper right');polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'sphere_torus_spectral_residual', OUT)
