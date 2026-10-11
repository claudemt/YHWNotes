from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    eta = np.linspace(-.7, .7, 300)
    theta = np.linspace(0, .62, 220)
    E, T = np.meshgrid(eta, theta)
    S = 32
    logw = S * np.log((1 + np.cos(T)**2 + 2*np.cos(T)*np.cos(E))/4)
    w = np.exp(logw)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    mesh = ax.pcolormesh(E, T, w, shading='auto', cmap='viridis', vmin=0, vmax=1)
    cs = ax.contour(E, T, w, levels=[.15, .4, .7], colors='white', linewidths=.7, alpha=.82)
    ax.clabel(cs, inline=True, fontsize=9, fmt='%.2f')
    ax.set_xlabel(r'Angular departure $\eta$ (rad)')
    ax.set_ylabel(r'Transverse angle $\theta$ (rad)')
    cb=fig.colorbar(mesh, ax=ax, pad=.02)
    cb.set_label(r'$|\mathcal{A}_{32}|^2/|\mathcal{A}_{32}|^2_{\max}$')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'antipodal_peak_map', OUT)
