"""Exact occupation after a harmonic-oscillator frequency quench."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
with figure_style():
    ratio=np.geomspace(0.22, 4.5, 500)
    occ=(ratio-1)**2/(4*ratio)
    fig,ax=plt.subplots(figsize=(6.5,4.0))
    ax.plot(ratio,occ,color=COLORS[0],label=r'$|\beta|^2=(r-1)^2/(4r)$')
    ax.axvline(1, color=COLORS[1], linewidth=1.25, linestyle='--',label='no quench: $r=1$')
    ax.set_xscale('log')
    ax.set_xlim(.22,4.5)
    ax.set_ylim(0,1.32)
    ax.set_xlabel(r'frequency ratio $r=\omega_1/\omega_0$')
    ax.set_ylabel(r'new particles $\langle N_1\rangle$')
    ax.set_xticks([.25,.5,1,2,4],labels=['0.25','0.5','1','2','4'])
    polish_axes(ax,grid=True)
    add_legend(ax,corner='upper center')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'quench_particles',OUT)
