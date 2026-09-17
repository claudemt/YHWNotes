from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

OUT_DIR = ROOT / 'figures'
beta = 3.0
Lmax = 32
ell = np.arange(-Lmax, Lmax + 1)
c = jv(ell, 2.0 * beta)
theta = np.linspace(-np.pi, np.pi, 520, endpoint=False)
s_over_pi = np.linspace(0.0, 2.0, 360)
s = np.pi * s_over_pi
phase_theta = np.exp(1j * np.outer(ell, theta))
I = np.empty((len(s), len(theta)))
for i, si in enumerate(s):
    psi = (c * np.exp(-1j * si * ell**2)) @ phase_theta
    I[i] = np.abs(psi)**2
I /= np.mean(I[0])

with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.5))
    im = ax.imshow(I, origin='lower', aspect='auto',
                   extent=[-0.5, 0.5, 0.0, 2.0])
    ax.set_xlabel(r'$\theta/(2\pi)$')
    ax.set_ylabel(r'$s/\pi$')
    cb = fig.colorbar(im, ax=ax)
    cb.set_label('Normalized density')
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "talbot_time_focusing", output_dir=OUT_DIR)
print(OUT_DIR / "talbot_time_focusing.png")
