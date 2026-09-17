from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

OUT = ROOT / 'figures' / 'generated'

# Representative Wolfenstein-apex values for visualization only.
rho_bar = 0.145
eta_bar = 0.343
pts = np.array([[0.0, 0.0], [1.0, 0.0], [rho_bar, eta_bar], [0.0, 0.0]])

with figure_style():
    fig, ax = plt.subplots(figsize=(7.6, 6.6))
    ax.plot(pts[:, 0], pts[:, 1], color=COLORS[0], linewidth=2.8)
    ax.scatter(pts[:-1, 0], pts[:-1, 1], s=80, color=COLORS[1], zorder=3)
    ax.plot([rho_bar, rho_bar], [0, eta_bar], linestyle='--', color=COLORS[2], linewidth=2.0)
    ax.text(0.48, -0.055, r'$1$')
    ax.text(rho_bar + 0.02, eta_bar + 0.02, r'$(\bar\rho,\bar\eta)$')
    ax.text(0.23, 0.20, r'$V_{ud}V_{ub}^*$')
    ax.text(0.54, 0.22, r'$V_{cd}V_{cb}^*$')
    ax.text(0.41, -0.09, r'$V_{td}V_{tb}^*$')
    ax.set_xlabel(r'$\bar\rho$')
    ax.set_ylabel(r'$\bar\eta$')
    ax.set_title('CKM unitarity triangle')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.10, 0.72)
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'sm_ckm_unitarity_triangle_dp18', output_dir=OUT)
