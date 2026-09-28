#!/usr/bin/env python3
"""Volterra Nyström convergence and Fredholm rank-one resonance."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import (
    COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend,
    save_pdf_png_pair,
)

OUT = Path(__file__).resolve().parents[1] / "generated"


def volterra_trapezoid(n, coupling=2.0):
    """Solve u(x)=1+coupling*integral_0^x u(y)dy by composite trapezoids."""
    h = 1.0 / n
    x = np.linspace(0.0, 1.0, n + 1)
    u = np.empty(n + 1)
    u[0] = 1.0
    for i in range(1, n + 1):
        u[i] = (1.0 + coupling * h * (0.5 * u[0] + u[1:i].sum())) / (
            1.0 - 0.5 * coupling * h)
    return x, u


sizes = np.array([20, 40, 80, 160, 320])
errors = []
for n in sizes:
    x, u = volterra_trapezoid(int(n))
    h = 1.0 / n
    discrete_exact = ((1 + h) / (1 - h)) ** np.arange(n + 1)
    assert np.allclose(u, discrete_exact, rtol=1e-12, atol=1e-12)
    errors.append(np.max(np.abs(u - np.exp(2 * x))))
errors = np.asarray(errors)
assert np.all(np.diff(errors) < 0)
assert np.all((errors[:-1] / errors[1:]) > 3.9)
h_finest = 1.0 / sizes[-1]
leading_error = (2 * np.e**2 / 3) * h_finest**2
assert abs(errors[-1] / leading_error - 1) < 1e-3

nodes, weights = leggauss(24)
nodes, weights = (nodes + 1) / 2, weights / 2
kernel = np.outer(nodes, nodes)
couplings = np.concatenate((np.linspace(0, 2.97, 180),
                            np.linspace(3.03, 3.7, 60)))
condition_numbers = np.array([
    np.linalg.cond(np.eye(len(nodes)) - lam * kernel * weights[None, :])
    for lam in couplings
])

with figure_style():
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 8.0))
    h_values = 1.0 / sizes
    axes[0].loglog(h_values, errors, "o-", label="maximum error")
    axes[0].loglog(
        h_values, errors[-1] * (h_values / h_values[-1])**2,
        **REFERENCE_LINE_STYLE, label="$h^2$ reference")
    axes[0].set(xlabel="mesh spacing $h$", ylabel="maximum error",
                title="Trapezoid convergence")
    polish_axes(axes[0], grid=True)
    add_legend(axes[0], corner="upper left")

    axes[1].semilogy(couplings[:180], condition_numbers[:180])
    axes[1].semilogy(couplings[180:], condition_numbers[180:],
                     color=COLORS[0])
    axes[1].axvline(3.0, **REFERENCE_LINE_STYLE, label="$\\lambda=3$")
    axes[1].set(xlabel="Fredholm parameter $\\lambda$",
                ylabel="matrix condition number", title="Rank-one resonance")
    polish_axes(axes[1], grid=True)
    add_legend(axes[1], corner="upper left")
    fig.tight_layout()
    save_pdf_png_pair(fig, "integral_equations", OUT)
    plt.close(fig)

print("Volterra maximum errors:", errors)
print("rank-one quadrature moment:", np.dot(weights, nodes**2))
