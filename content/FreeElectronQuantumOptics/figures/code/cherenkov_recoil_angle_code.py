from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, LINE_STYLES, save_pdf_png_pair, add_legend

beta = 0.95
ns = [1.2, 1.5, 2.0]
x = np.linspace(0.0, 0.58, 500)

with figure_style():
    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    for i, n in enumerate(ns):
        cos_theta = (1.0 + 0.5 * x * (n**2 - 1.0)) / (n * beta)
        theta = np.full_like(x, np.nan)
        mask = (cos_theta >= -1.0) & (cos_theta <= 1.0)
        theta[mask] = np.degrees(np.arccos(cos_theta[mask]))
        ax.plot(x, theta, label=fr'$n={n:.1f}$', color=COLORS[i], linestyle=LINE_STYLES[i])
        theta0 = np.degrees(np.arccos(1.0/(n*beta)))
        ax.hlines(theta0, 0, x[-1], colors=COLORS[i], linestyles=':', linewidth=1.8)
    ax.set_xlabel(r'$x=\hbar\omega/E_i$')
    ax.set_ylabel(r'$\theta$ [deg]')
    ax.set_xlim(0, x[-1])
    ax.set_ylim(0, 70)
    ax.text(0.02, 0.96, r'$\beta_{\rm rel}=0.95$\nsolid: exact; dotted: $x\to0$', transform=ax.transAxes, va='top')
    add_legend(ax, frameon=False, ncol=1)
    polish_axes(ax, grid=True)
    fig.subplots_adjust(left=0.12, bottom=0.15, right=0.98, top=0.97)
    save_pdf_png_pair(fig, 'cherenkov_recoil_angle', output_dir=ROOT/'figures'/'generated')
