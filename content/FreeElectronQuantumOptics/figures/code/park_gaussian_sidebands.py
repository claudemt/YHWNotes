from pathlib import Path
import math
import sys
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

OUT_DIR = ROOT / 'figures'
beta0 = 2.6
R_sigma = 0.55
ells = np.arange(-8, 9)
R_tau = np.linspace(-4.0, 4.0, 321)
jmax = 22

def C(ell: int, j: int) -> float:
    lp = max(ell, 0)
    lm = max(-ell, 0)
    return (beta0 ** (j + lp) * (-beta0) ** (j + lm)
            / (math.factorial(j + lp) * math.factorial(j + lm)))

P = np.empty((len(ells), len(R_tau)))
for ie, ell in enumerate(ells):
    coeff = np.array([C(int(ell), j) for j in range(jmax + 1)], dtype=float)
    jj, kk = np.meshgrid(np.arange(jmax + 1), np.arange(jmax + 1), indexing='ij')
    S = abs(int(ell)) + jj + kk
    pref = np.outer(coeff, coeff) / np.sqrt(1.0 + S * R_sigma**2)
    for it, rt in enumerate(R_tau):
        weight = np.exp(-S * rt**2 / (2.0 * (1.0 + S * R_sigma**2)))
        P[ie, it] = np.sum(pref * weight)
P = np.maximum(P, 0.0)
P /= np.maximum(P.sum(axis=0, keepdims=True), np.finfo(float).tiny)

with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    im = ax.imshow(P, origin='lower', aspect='auto',
                   extent=[R_tau[0], R_tau[-1], ells[0]-0.5, ells[-1]+0.5])
    ax.set_xlabel(r'Delay $\tau/\sigma_{\rm p}$')
    ax.set_ylabel(r'Sideband order $\ell$')
    ax.set_yticks(np.arange(-8, 9, 2))
    cb = fig.colorbar(im, ax=ax)
    cb.set_label(r'$P_\ell(\tau)$')
    polish_axes(ax, grid=False, minor_ticks=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "park_gaussian_sidebands", output_dir=OUT_DIR)
print(OUT_DIR / "park_gaussian_sidebands.png")
