from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, hbar, alpha, physical_constants, electron_volt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, LINE_STYLES, save_pdf_png_pair, add_legend

m_mu = physical_constants['muon mass'][0]
gev = 1.0e9 * electron_volt
E_thr = 2.0 * m_mu * c**2
E_cm = np.geomspace(1.001 * E_thr, 50.0 * gev, 1200)
s = (E_cm / c)**2
beta = np.sqrt(np.maximum(0.0, 1.0 - (2.0 * m_mu * c**2 / E_cm)**2))
sigma_exact = (4.0 * np.pi * hbar**2 * alpha**2 / (3.0 * s)) * beta * (1.0 + 2.0 * m_mu**2 * c**2 / s)
sigma_ur = 4.0 * np.pi * alpha**2 * (hbar * c)**2 / (3.0 * E_cm**2)
# 1 pb = 1e-40 m^2
pb = 1.0e-40

with figure_style():
    fig, ax = plt.subplots(figsize=(9.0, 5.7))
    ax.loglog(E_cm / gev, sigma_exact / pb, color=COLORS[0], label=r'$m_\mu\neq0$')
    ax.loglog(E_cm / gev, sigma_ur / pb, color=COLORS[1], linestyle=LINE_STYLES[1], label=r'$m_\mu\to0:\ 1/E_{\rm CM}^2$')
    ax.axvline(E_thr / gev, linewidth=1.5, color=COLORS[5], linestyle=':', label=r'$E_{\rm thr}=2m_\mu c^2$')
    ax.set_xlabel(r'$E_{\rm CM}\ [{\rm GeV}]$')
    ax.set_ylabel(r'$\sigma_{\mu\mu}$ [pb]')
    ax.set_xlim(E_thr/gev * 0.98, 50.0)
    add_legend(ax, frameon=False, )
    polish_axes(ax, grid=True)
    fig.subplots_adjust(left=0.16, bottom=0.16, right=0.98, top=0.98)
    save_pdf_png_pair(fig, 'ee_mumu_total_cross_section_dp61', output_dir=ROOT/'figures'/'generated')
