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
    fig, ax = plt.subplots(figsize=(5.0, 6.6))
    ell = np.array([-1, 0, 1, 2])
    E = np.array([2.0, 0.0, 0.0, 2.0])
    labels = ['-1', '0', '1', '2']
    for lv, en, lab in zip(ell, E, labels):
        ax.hlines(en, lv-0.32, lv+0.32, linewidth=3.0, color=COLORS[0])
        ax.text(lv, en+0.12, rf'$\ell={lab}$', ha='center')
    ax.add_patch(FancyArrowPatch((0, 0.08), (1, 0.08), arrowstyle='<->', mutation_scale=18, linewidth=2.0, color=COLORS[1]))
    ax.text(0.5, 0.26, 'resonant', ha='center')
    ax.text(-1, 2.18, r'$\delta_{-1}\approx2\omega_r$', ha='center')
    ax.text(2, 2.18, r'$\delta_{2}\approx2\omega_r$', ha='center')
    ax.set_xlim(-1.8, 2.8)
    ax.set_ylim(-0.4, 2.8)
    ax.set_xlabel('momentum ladder index')
    ax.set_ylabel('effective detuning scale')
    ax.set_title('Recoil-selected two-level window')
    polish_axes(ax, grid=False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'recoil_two_level_selection', output_dir=OUT)
