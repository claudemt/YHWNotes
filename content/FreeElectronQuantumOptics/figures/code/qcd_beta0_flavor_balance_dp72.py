from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import (  # noqa: E402
    COLORS,
    LINE_STYLES,
    add_legend,
    figure_style,
    polish_axes,
    save_pdf_png_pair,
)

OUT = ROOT / 'figures' / 'generated'

# Eq. (qcd-beta0-su3-dp10): beta_0 = 11 - 2 n_f / 3 for SU(3).
nf = np.linspace(0.0, 18.0, 361)
gauge_ghost = np.full_like(nf, 11.0)
quark_screening = -(2.0 / 3.0) * nf
beta0 = gauge_ghost + quark_screening

with figure_style():
    fig, ax = plt.subplots(figsize=(8.8, 5.5))
    ax.plot(
        nf,
        gauge_ghost,
        label=r'gauge + ghost: $+11$',
        color=COLORS[0],
        linestyle=LINE_STYLES[0],
    )
    ax.plot(
        nf,
        quark_screening,
        label=r'quarks: $-2n_f/3$',
        color=COLORS[1],
        linestyle=LINE_STYLES[1],
    )
    ax.plot(
        nf,
        beta0,
        label=r'total: $\beta_0$',
        color=COLORS[2],
        linestyle=LINE_STYLES[2],
        linewidth=2.2,
    )
    ax.axhline(0.0, color='0.35', linewidth=1.2, linestyle=':')
    ax.axvline(16.5, color='0.45', linewidth=1.2, linestyle=':')
    ax.text(16.15, 1.0, r'$n_f=16.5$', ha='right', va='bottom')
    ax.set_xlabel(r'$n_f$')
    ax.set_ylabel(r'one-loop coefficient')
    ax.set_title(r'QCD one-loop $\beta_0$ balance')
    ax.set_xlim(0.0, 18.0)
    ax.set_ylim(-13.0, 13.0)
    polish_axes(ax, grid=True)
    add_legend(ax, )
    fig.tight_layout()
    save_pdf_png_pair(fig, 'qcd_beta0_flavor_balance_dp72', output_dir=OUT)
