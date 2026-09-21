from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair

# Eq. (two-body-threshold-beta-dp8): x = sqrt(s)/(2 m c) >= 1,
# beta_* = sqrt(1 - 1/x^2).  The plot is dimensionless and model-independent.
x = np.linspace(1.0, 4.0, 900)
beta = np.sqrt(np.clip(1.0 - 1.0/x**2, 0.0, None))

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(x, beta, linewidth=3.2)
    ax.axvline(1.0, linestyle='--', linewidth=2.0)
    ax.set_xlabel(r'$x=\sqrt{s}/(2mc)$')
    ax.set_ylabel(r'$\beta_*(s)=\sqrt{1-x^{-2}}$')
    ax.set_xlim(0.96, 4.0)
    ax.set_ylim(-0.02, 1.02)
    polish_axes(ax, grid=True)
    ax.text(1.08, 0.10, 'two-particle threshold')
    fig.subplots_adjust(left=0.17, bottom=0.18, right=0.98, top=0.97)
    save_pdf_png_pair(fig, 'two_body_cut_threshold', output_dir=ROOT/'figures'/'generated')

