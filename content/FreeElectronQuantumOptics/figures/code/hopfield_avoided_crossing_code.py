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

OUT = ROOT / 'figures'

# Dimensionless form of Eq. (hopfield_rwa_polariton_frequencies):
# delta = (omega_c_bar - omega_m)/|g_cm|,
# (omega_+-omega_bar)/|g_cm| = +sqrt(delta^2/4 + 1), etc.
delta = np.linspace(-8.0, 8.0, 1200)
bare_c = 0.5 * delta
bare_m = -0.5 * delta
dressed = np.sqrt(0.25 * delta**2 + 1.0)

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(delta, bare_c, color='0.55', linestyle='--', linewidth=1.5, label='renorm. photon')
    ax.plot(delta, bare_m, color='0.55', linestyle=':', linewidth=1.5, label='bare matter')
    ax.plot(delta, dressed, color=COLORS[0], linestyle=LINE_STYLES[0], label=r'$\omega_+$')
    ax.plot(delta, -dressed, color=COLORS[1], linestyle=LINE_STYLES[0], label=r'$\omega_-$')
    ax.axvline(0.0, color='0.35', linestyle=':', linewidth=1.0)
    ax.set_xlabel(r'$(\bar\omega_c-\omega_m)/|g_{\rm cm}|$')
    ax.set_ylabel(r'$(\omega-\bar\omega)/|g_{\rm cm}|$')
    ax.set_title('RWA avoided crossing')
    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(-4.8, 4.8)
    polish_axes(ax, grid=True)
    add_legend(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'hopfield_avoided_crossing', output_dir=OUT)
