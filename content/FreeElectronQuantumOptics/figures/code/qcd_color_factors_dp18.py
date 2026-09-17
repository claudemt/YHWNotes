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

Nc = np.arange(2, 9)
CF = (Nc**2 - 1) / (2 * Nc)
CA = Nc.astype(float)
TF = 0.5 * np.ones_like(Nc, dtype=float)
ratio = CF / CA

with figure_style():
    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    ax.plot(Nc, CF, marker='o', label=r'$C_F=(N_c^2-1)/(2N_c)$', color=COLORS[0], linestyle=LINE_STYLES[0])
    ax.plot(Nc, CA, marker='s', label=r'$C_A=N_c$', color=COLORS[1], linestyle=LINE_STYLES[1])
    ax.plot(Nc, TF, marker='^', label=r'$T_F=1/2$', color=COLORS[2], linestyle=LINE_STYLES[2])
    ax.plot(Nc, ratio, marker='d', label=r'$C_F/C_A$', color=COLORS[3], linestyle=LINE_STYLES[3])
    ax.axvline(3, color='0.4', linestyle=':', linewidth=1.6)
    ax.text(3.08, 2.75, r'QCD: $N_c=3$')
    ax.set_xlabel(r'number of colors $N_c$')
    ax.set_ylabel('group invariant')
    ax.set_title(r'$SU(N_c)$ color factors')
    ax.set_xlim(1.8, 8.2)
    ax.set_ylim(0.0, 8.6)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94, ncol=2)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'qcd_color_factors_dp18', output_dir=OUT)
