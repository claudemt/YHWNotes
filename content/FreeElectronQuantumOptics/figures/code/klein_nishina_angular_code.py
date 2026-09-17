from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, LINE_STYLES, save_pdf_png_pair, add_legend

theta = np.linspace(0.0, np.pi, 1200)
theta_deg = np.degrees(theta)
epsilons = [0.02, 0.2, 1.0, 5.0]

with figure_style():
    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    for i, eps in enumerate(epsilons):
        ratio = 1.0 / (1.0 + eps * (1.0 - np.cos(theta)))
        dsdo = 0.5 * ratio**2 * (ratio + 1.0 / ratio - np.sin(theta)**2)
        ax.plot(theta_deg, dsdo, label=fr'$\hbar\omega/(m_e c^2)={eps:g}$', color=COLORS[i], linestyle=LINE_STYLES[i])
    ax.set_xlabel(r'$\theta$ [deg]')
    ax.set_ylabel(r'$r_e^{-2}\,d\sigma/d\Omega$')
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1.26)
    add_legend(ax, frameon=True, ncol=2, corner="upper right")
    polish_axes(ax, grid=True)
    fig.subplots_adjust(left=0.16, bottom=0.15, right=0.98, top=0.98)
    save_pdf_png_pair(fig, 'klein_nishina_angular', output_dir=ROOT/'figures'/'generated')
