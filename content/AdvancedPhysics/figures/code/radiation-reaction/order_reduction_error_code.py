#!/usr/bin/env python3
"""Quantitative error of first-order Landau--Lifshitz order reduction."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.laguerre import laggauss
import sys
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

OUT = Path(__file__).resolve().parents[2] / 'generated' / Path(__file__).resolve().parent.name

nodes, weights = laggauss(96)
t = np.linspace(-4.0, 4.0, 2001)
eps_values = np.logspace(-3, -0.35, 28)
errors = []

for eps in eps_values:
    shifted = t[:, None] + eps * nodes[None, :]
    exact = (np.exp(-shifted**2) * weights[None, :]).sum(axis=1)
    force = np.exp(-t**2)
    dforce = -2.0 * t * force
    reduced = force + eps * dforce
    err = np.sqrt(
        np.trapezoid((exact - reduced)**2, t)
        / np.trapezoid(exact**2, t)
    )
    errors.append(err)

errors = np.asarray(errors)
reference = errors[0] * (eps_values / eps_values[0])**2

with figure_style():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.loglog(eps_values, errors, label="numerical error")
    ax.loglog(eps_values, reference, "--",
              label=r"$\mathcal{O}[(\tau_{\rm rr}/T)^2]$")
    ax.set_xlabel(r"$\tau_{\rm rr}/T$")
    ax.set_ylabel(r"relative $L^2$ error")
    polish_axes(ax, grid=False)
    add_legend(ax, loc="upper left", frameon=False)
    fig.tight_layout()
    save_pdf_png_pair(fig, "order_reduction_error", OUT)
    plt.close(fig)
