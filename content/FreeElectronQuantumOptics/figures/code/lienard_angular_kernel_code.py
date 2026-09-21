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

theta = np.linspace(1e-4, np.pi - 1e-4, 1200)
theta_deg = theta * 180.0 / np.pi
betas = [0.3, 0.7, 0.95]

with figure_style():
    fig, ax = plt.subplots()
    for i, beta in enumerate(betas):
        kernel = np.sin(theta)**2 / (1.0 - beta * np.cos(theta))**5
        kernel /= np.max(kernel)
        ax.plot(theta_deg, kernel, label=fr'$\beta_{{\rm rel}}={beta:.2f}$', color=COLORS[i], linestyle=LINE_STYLES[i])
    ax.set_xlabel(r'$\theta$ (deg)')
    ax.set_ylabel('normalized angular kernel')
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1.05)
    add_legend(ax)
    polish_axes(ax, grid=True)
    fig.subplots_adjust(left=0.12, bottom=0.15, right=0.98, top=0.98)
    save_pdf_png_pair(fig, 'lienard_angular_kernel', output_dir=ROOT/'figures'/'generated')
