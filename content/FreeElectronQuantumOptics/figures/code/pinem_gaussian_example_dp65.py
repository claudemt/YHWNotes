from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, hbar, e, m_e, pi
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

K_eV = 200.0e3
lambda0 = 800.0e-9
E0 = 20.0e6
L = 100.0e-9

gamma0 = 1.0 + K_eV / (m_e * c**2 / e)
v0 = c * np.sqrt(1.0 - gamma0**-2)
omega = 2.0 * pi * c / lambda0
eta = omega * L / v0
beta_abs = (e * E0 * np.sqrt(2.0 * pi) * L / (hbar * omega)) * np.exp(-0.5 * eta**2)

ell = np.arange(-8, 9)
prob = jv(ell, 2.0 * beta_abs) ** 2

with figure_style():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    markerline, stemlines, _ = ax.stem(ell, prob, linefmt='k-', markerfmt='ko', basefmt=' ')
    markerline.set_markerfacecolor('white')
    markerline.set_markeredgewidth(1.0)
    stemlines.set_linewidth(1.0)
    ax.set_xlabel(r'sideband $\ell$')
    ax.set_ylabel(r'$P_\ell$')
    ax.set_xticks(np.arange(-8, 9, 2))
    ax.set_ylim(0.0, max(prob) * 1.24)
    ax.text(0.03, 0.94, rf'$|\beta|={beta_abs:.3f}$', transform=ax.transAxes,
            ha='left', va='top')
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout(pad=0.35)
    save_pdf_png_pair(fig, 'pinem_gaussian_example_dp65', output_dir=ROOT / 'figures')
