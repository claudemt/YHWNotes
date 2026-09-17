from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import k1

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend  # noqa: E402

OUT_DIR = ROOT / 'figures'
x = np.linspace(0.08, 7.0, 700)
sphere = x**2 * k1(x)
cylinder = x * np.exp(-x)
sphere /= np.max(sphere)
cylinder /= np.max(cylinder)

with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.3))
    ax.plot(x, sphere, label=r'sphere: $x^2K_1(x)$', color=COLORS[1])
    ax.plot(x, cylinder, '--', label=r'cylinder: $xe^{-x}$', color=COLORS[4])
    ax.set_xlabel(r'$x=\Delta k\,b$')
    ax.set_ylabel(r'$|\widetilde F_z|$ (norm.)')
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 1.05)
    add_legend(ax, frameon=False)
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "park_geometry_decay", output_dir=OUT_DIR)
print(OUT_DIR / "park_geometry_decay.png")
