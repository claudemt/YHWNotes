from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, LINE_STYLES, save_pdf_png_pair, add_legend

alpha = 1.0 / 137.035999084
q_over_mc = np.logspace(-3, 4, 600)
x = np.linspace(0.0, 1.0, 5001)
w = x * (1.0 - x)
# Book convention: Pi_R(-Q^2) < 0, and the transverse inverse propagator
# contains 1 + Pi_R.  Q/(m_e c) is dimensionless.
logarg = 1.0 + q_over_mc[:, None]**2 * w[None, :]
pi_r = (2.0 * alpha / np.pi) * np.trapezoid(w[None, :] * np.log(1.0 / logarg), x, axis=1)
ratio = 1.0 / (1.0 + pi_r)
percent = 100.0 * (ratio - 1.0)

# Large-Q asymptotic from Eq. Pi-spacelike-asymptotic-r12.
pi_as = -(alpha / (3.0 * np.pi)) * np.log(q_over_mc**2) + 5.0 * alpha / (9.0 * np.pi)
ratio_as = 1.0 / (1.0 + pi_as)
mask = q_over_mc >= 5.0

with figure_style():
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    ax.plot(q_over_mc, percent, linewidth=3.0, label='one-loop integral')
    ax.plot(q_over_mc[mask], 100.0 * (ratio_as[mask] - 1.0), linestyle='--', linewidth=2.6,
            label='large-$Q$ asymptotic')
    ax.set_xscale('log')
    ax.set_xlabel(r'$Q/(m_e c)$')
    ax.set_ylabel(r'$\Delta\alpha/\alpha$ [\%]')
    add_legend(ax, frameon=False)
    polish_axes(ax, grid=True)
    fig.subplots_adjust(left=0.17, bottom=0.17, right=0.98, top=0.98)
    save_pdf_png_pair(fig, 'qed_running_alpha', output_dir=ROOT/'figures'/'generated')
