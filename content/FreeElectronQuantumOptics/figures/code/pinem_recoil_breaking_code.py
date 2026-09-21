from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend

beta = 2.5
L = 12
ells = np.arange(-L, L+1)
N = len(ells)

# Dimensionless evolution s in [0,1]: i dc/ds = H c.
# Translation-invariant hopping beta reproduces J_l(2 beta).
def probs(chi):
    H = np.zeros((N,N), dtype=complex)
    H[np.arange(N), np.arange(N)] = chi * ells**2
    for n in range(N-1):
        H[n, n+1] = beta
        H[n+1, n] = beta
    psi0 = np.zeros(N, dtype=complex)
    psi0[L] = 1.0
    psi = expm(-1j*H) @ psi0
    return np.abs(psi)**2

p0 = jv(ells, 2*beta)**2
p1 = probs(0.20)
p2 = probs(0.40)

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(ells, p0, marker='o', label=r'ideal $J_\ell^2(2|\beta|)$', color=COLORS[0])
    ax.plot(ells, p1, marker='s', linestyle='--', label=r'$\chi=\omega_{\rm curv}T=0.20$', color=COLORS[1])
    ax.plot(ells, p2, marker='^', linestyle='-.', label=r'$\chi=0.40$', color=COLORS[2])
    ax.set_xlabel(r'sideband index $\ell$')
    ax.set_ylabel(r'probability $P_\ell$')
    ax.set_xlim(-8, 8)
    ax.set_ylim(0, 0.23)
    polish_axes(ax, grid=True, minor_ticks=False)
    add_legend(ax, corner="upper right")
    fig.tight_layout()
    save_pdf_png_pair(fig, 'pinem_recoil_breaking', output_dir=ROOT/'figures'/'generated')
