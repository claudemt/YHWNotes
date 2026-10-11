"""Boundary-domain norm of the nonregular inverse-square radial branch."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

with figure_style():
    rmin=np.geomspace(1e-3,0.3,300)
    fig,ax=plt.subplots(figsize=(6.5, 4.0))
    for i,nu in enumerate((0.5,1.0,1.5)):
        if nu==1.0: val=np.log(1/rmin)
        else: val=(1-rmin**(2-2*nu))/(2-2*nu)
        ax.plot(rmin,val,color=COLORS[i],label=rf'$\nu={nu:g}$')
    ax.set_xscale('log');ax.set_yscale('log')
    ax.set_xlim(0.001,0.3);ax.set_xlabel(r'Lower cutoff $\varepsilon$')
    ax.set_ylabel(r'$\int_\varepsilon^1 r^{1-2\nu}\,dr$')
    add_legend(ax, corner='upper right');polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'conic_boundary_modes', OUT)
