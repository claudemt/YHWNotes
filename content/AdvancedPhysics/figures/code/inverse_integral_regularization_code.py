#!/usr/bin/env python3
"""Noise amplification in a first-kind integral equation and Tikhonov recovery."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

OUT = Path(__file__).resolve().parents[1] / "generated"
n = 120
h = 1.0 / n
x = h * np.arange(1, n + 1)
midpoints = x - h / 2
true_unknown = 1.0 + np.sin(2 * np.pi * midpoints)
true_data = x + (1.0 - np.cos(2 * np.pi * x)) / (2 * np.pi)
rng = np.random.default_rng(20260927)
noise_level = 0.003
observed = true_data + noise_level * rng.standard_normal(n)

# Cellwise-constant quadrature: (K phi)_i=h*sum_{j<=i} phi_j.
K = h * np.tril(np.ones((n, n)))
naive = np.diff(np.r_[0.0, observed]) / h
alpha = 3.0e-4
regularized = np.linalg.solve(K.T @ K + alpha * np.eye(n), K.T @ observed)
naive_error = np.sqrt(h * np.sum((naive - true_unknown)**2))
regularized_error = np.sqrt(h * np.sum((regularized - true_unknown)**2))
assert regularized_error < naive_error / 3

with figure_style():
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 8.0))
    axes[0].plot(x, true_data, "k--", label="exact data")
    axes[0].plot(x[::3], observed[::3], ".", ms=3,
                 label="noisy observations")
    axes[0].set(xlabel="$x$", ylabel="$(K\\phi)(x)$",
                title="Integration hides perturbations")
    polish_axes(axes[0], grid=True)
    add_legend(axes[0])

    axes[1].plot(midpoints, true_unknown, "k--", label="true $\\phi$")
    axes[1].plot(midpoints, naive, alpha=0.65,
                 label="direct differentiation")
    axes[1].plot(midpoints, regularized, label="Tikhonov recovery")
    axes[1].set(xlabel="$x$", ylabel="$\\phi(x)$",
                title="First-kind inverse problem", ylim=(-0.9, 3.2))
    polish_axes(axes[1], grid=True)
    add_legend(axes[1], corner="lower left")
    fig.tight_layout()
    save_pdf_png_pair(fig, "inverse_integral_regularization", OUT)
    plt.close(fig)

print("noise standard deviation:", noise_level)
print("naive L2 error:", naive_error)
print("regularized L2 error:", regularized_error)
