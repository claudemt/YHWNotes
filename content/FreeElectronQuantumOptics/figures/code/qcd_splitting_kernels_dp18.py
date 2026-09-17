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

CF = 4.0 / 3.0
TF = 0.5
z = np.linspace(0.02, 0.98, 800)
Pqq_real = CF * (1.0 + z**2) / (1.0 - z)
Pgq = CF * (1.0 + (1.0 - z)**2) / z
Pqg = TF * (z**2 + (1.0 - z)**2)
clip = 12.0

with figure_style():
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    ax.plot(z, np.minimum(Pqq_real, clip), label=r'$q\to qg:\ C_F(1+z^2)/(1-z)$', color=COLORS[0], linestyle=LINE_STYLES[0])
    ax.plot(z, np.minimum(Pgq, clip), label=r'$q\to gq:\ C_F[1+(1-z)^2]/z$', color=COLORS[1], linestyle=LINE_STYLES[1])
    ax.plot(z, Pqg, label=r'$g\to q\bar q:\ T_F[z^2+(1-z)^2]$', color=COLORS[2], linestyle=LINE_STYLES[2])
    ax.axhline(clip, color='0.55', linestyle=':', linewidth=1.2)
    ax.text(0.79, clip + 0.18, 'display clip', fontsize=13)
    ax.set_xlabel(r'$z$')
    ax.set_ylabel('kernel shape')
    ax.set_title('LO splitting kernels')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, clip + 1.0)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'qcd_splitting_kernels_dp18', output_dir=OUT)
