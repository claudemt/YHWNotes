#!/usr/bin/env python3
"""Finite-size coherence: exact form factors and long-wave limits."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

OUT = Path(__file__).resolve().parents[2] / 'generated' / Path(__file__).resolve().parent.name

kappa = np.linspace(0.0, 4.0, 1601)
shell = np.ones_like(kappa)
mask = kappa != 0.0
shell[mask] = (np.sin(kappa[mask]) / kappa[mask])**2
gaussian = np.exp(-0.5 * kappa**2)

k_small = np.linspace(0.0, 1.1, 441)
shell_lw = 1.0 - k_small**2 / 3.0
gaussian_lw = 1.0 - k_small**2 / 2.0

with figure_style():
    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    ax.plot(kappa, shell, label=r"thin shell: $\mathrm{sinc}^2\kappa_{\rm src}$")
    ax.plot(kappa, gaussian, label=r"Gaussian: $e^{-\kappa_{\rm src}^2/2}$")
    ax.plot(k_small, shell_lw, "--", label=r"shell LW: $1-\kappa_{\rm src}^2/3$")
    ax.plot(k_small, gaussian_lw, "--", label=r"Gaussian LW: $1-\kappa_{\rm src}^2/2$")
    ax.axvline(1.0, linestyle=":", linewidth=1.0, label=r"$\kappa_{\rm src}=1$")
    ax.set_xlabel(r"$\kappa_{\rm src}=\omega a_{\rm src}/c$")
    ax.set_ylabel(r"$I(\omega)/I_{\rm point}(\omega)$")
    ax.set_xlim(0.0, 4.0)
    ax.set_ylim(-0.02, 1.05)
    polish_axes(ax, grid=True)
    add_legend(ax, loc="upper right", frameon=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "form_factor_shell", OUT)
    plt.close(fig)
