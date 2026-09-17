from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.special import jv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair

L = 16
ells = np.arange(-L, L+1)
N = len(ells)
idx0 = np.where(ells == 0)[0][0]
idx1 = np.where(ells == 1)[0][0]

A_vals = np.logspace(-1.0, np.log10(4.0), 48)
Phi_vals = np.logspace(-2.5, 1.3, 58)
err_b = np.zeros((len(Phi_vals), len(A_vals)))
err_2 = np.zeros_like(err_b)
edge_prob = np.zeros_like(err_b)

psi0 = np.zeros(N, dtype=complex)
psi0[idx0] = 1.0

for ip, Phi in enumerate(Phi_vals):
    diag = Phi * ells * (ells - 1)  # Phi_lin=-Phi_r: edge 0<->1 exactly resonant
    for ia, A in enumerate(A_vals):
        H = np.diag(diag.astype(float))
        off = np.full(N-1, A, dtype=float)
        H += np.diag(off, 1) + np.diag(off, -1)
        w, V = eigh(H)
        amp_eig = V.conj().T @ psi0
        psi = V @ (np.exp(-1j*w) * amp_eig)
        p = np.abs(psi)**2
        p /= p.sum()

        pb = jv(ells, 2*A)**2
        pb /= pb.sum()
        p2 = np.zeros(N)
        p2[idx0] = np.cos(A)**2
        p2[idx1] = np.sin(A)**2
        err_b[ip, ia] = 0.5*np.sum(np.abs(p-pb))
        err_2[ip, ia] = 0.5*np.sum(np.abs(p-p2))
        edge_prob[ip, ia] = p[0] + p[-1]

# Numerical truncation is negligible throughout the plotted window.
assert edge_prob.max() < 2e-7, edge_prob.max()

X, Y = np.meshgrid(A_vals, Phi_vals)
levels = [0.05]

with figure_style():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8), sharex=True, sharey=True)
    for ax, data, title in [
        (axes[0], err_b, 'Bessel error'),
        (axes[1], err_2, 'Two-level error'),
    ]:
        z = np.log10(np.maximum(data, 1e-4))
        mesh = ax.pcolormesh(X, Y, z, shading='auto', cmap='viridis', vmin=-4, vmax=0)
        ax.contour(X, Y, data, levels=levels, linewidths=1.0)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title(title)
        ax.set_xlabel(r'$\mathscr{A}_{\mathrm{hop}}$')
        polish_axes(ax, grid=False, minor_ticks=True)
    axes[0].set_ylabel(r'$\omega_{\rm r}T$')
    cbar = fig.colorbar(mesh, ax=axes, pad=0.025, fraction=0.035)
    cbar.set_label(r'$\log_{10}\epsilon$')
    fig.subplots_adjust(left=0.10, right=0.91, bottom=0.17, top=0.88, wspace=0.12)
    save_pdf_png_pair(fig, 'recoil_regime_map', output_dir=ROOT/'figures'/'generated')
