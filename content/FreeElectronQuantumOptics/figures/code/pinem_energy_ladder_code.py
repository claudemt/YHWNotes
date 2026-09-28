from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "generated"
OUT.mkdir(parents=True, exist_ok=True)

with figure_style():
    fig, ax = plt.subplots(figsize=(5.4, 6.8))
    levels = np.arange(-3, 4)
    for l in levels:
        y = l
        ax.hlines(y, -0.6, 0.6, color=COLORS[0], linewidth=2.8)
        ax.text(0.72, y-0.08, rf'$E_0{l:+d}\hbar\omega$')
    ax.add_patch(FancyArrowPatch((-0.25, -2.4), (-0.25, 2.4), arrowstyle='<->', mutation_scale=20, linewidth=2.0, color=COLORS[1]))
    ax.text(-0.92, 0.0, r'absorption / emission', rotation=90, va='center')
    ax.text(-0.1, -3.75, r'uniform spacing $\hbar\omega$')
    ax.set_xlim(-1.3, 2.6)
    ax.set_ylim(-3.9, 3.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Recoil-free PINEM ladder')
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'pinem_energy_ladder', output_dir=OUT)
