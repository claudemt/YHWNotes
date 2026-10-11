from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

with figure_style():
    eta = np.linspace(-1.4, 1.4, 701)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    for i, S in enumerate([2, 8, 32, 128]):
        ax.plot(eta, np.cos(eta / 2)**(2*S), color=COLORS[i], label=rf'$S={S}$')
    ax.set_xlabel(r'Angular departure $\eta$ (rad)')
    ax.set_ylabel(r'$|\mathcal{A}_S|^2/|\mathcal{A}_S|^2_{\max}$')
    ax.set_ylim(0, 1.045)
    ax.set_xlim(-1.4, 1.4)
    add_legend(ax, corner='upper right')
    polish_axes(ax, grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig, 'relative_angle_profiles', OUT)
