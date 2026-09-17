from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, LINE_STYLES, figure_style, polish_axes, save_pdf_png_pair, add_legend  # noqa: E402

OUT = ROOT / 'figures' / 'generated'

x = np.linspace(-1.0, 1.0, 600)
w_same = (1.0 + x) ** 2
w_oppo = (1.0 - x) ** 2
w_vector = 1.0 + x**2

with figure_style():
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    ax.plot(x, w_same, label=r'same chirality', color=COLORS[0], linestyle=LINE_STYLES[0])
    ax.plot(x, w_oppo, label=r'opposite chirality', color=COLORS[1], linestyle=LINE_STYLES[1])
    ax.plot(x, w_vector, label=r'pure vector sum $1+\cos^2\theta$', color=COLORS[2], linestyle=LINE_STYLES[2])
    ax.set_xlabel(r'$\cos\theta$')
    ax.set_ylabel('angular weight')
    ax.set_title(r'Chiral angular weights')
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(0.0, 4.15)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'sm_chiral_angular_weights_dp18', output_dir=OUT)
