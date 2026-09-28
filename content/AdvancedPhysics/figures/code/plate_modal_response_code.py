#!/usr/bin/env python3
"""Uniformly driven, lightly damped Navier plate: modal response."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import (
    COLORMAPS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend,
    save_pdf_png_pair,
)

OUT = Path(__file__).resolve().parents[1] / "generated"
odd_modes = np.arange(1, 10, 2)
omega_11 = 2 * np.pi**2
zeta = 0.025


def response(omega, x, y):
    """Complex amplitude for u_tt+2*zeta*omega_11*u_t+Delta^2 u=1."""
    result = np.zeros(np.broadcast_shapes(np.shape(x), np.shape(y)), dtype=complex)
    for m in odd_modes:
        for n in odd_modes:
            phi = 2 * np.sin(m * np.pi * x) * np.sin(n * np.pi * y)
            force_coefficient = 8 / (m * n * np.pi**2)
            eigenfrequency = np.pi**2 * (m*m + n*n)
            result += force_coefficient * phi / (
                eigenfrequency**2 - omega**2 -
                2j * zeta * omega_11 * omega)
    return result


frequencies = np.linspace(0.0, 5.6 * omega_11, 1200)
center = np.array([response(w, 0.5, 0.5) for w in frequencies])
static_center = abs(response(0.0, 0.5, 0.5))
assert static_center > 0

grid = np.linspace(0, 1, 101)
xx, yy = np.meshgrid(grid, grid, indexing="ij")
fields = [np.abs(response(w, xx, yy)) for w in (omega_11, 5 * omega_11)]

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(frequencies / omega_11, np.abs(center) / static_center)
    ax.axvline(1.0, **REFERENCE_LINE_STYLE)
    ax.axvline(5.0, **REFERENCE_LINE_STYLE)
    ax.set(xlabel="$\\omega/\\omega_{11}$",
           ylabel="center response / static response")
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "plate_modal_response", OUT)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 4.5))
    for ax, field, title in zip(
            axes, fields,
            ("$\\omega=\\omega_{11}$", "$\\omega=5\\omega_{11}$")):
        ax.imshow(field.T / np.max(field), origin="lower", extent=(0, 1, 0, 1),
                  cmap=COLORMAPS["amplitude"], vmin=0, vmax=1)
        ax.set(xlabel="$x$", ylabel="$y$", title=title)
        polish_axes(ax, grid=False)
    fig.tight_layout()
    save_pdf_png_pair(fig, "plate_modal_shapes", OUT)
    plt.close(fig)

print("static center response:", static_center)
print("first-mode peak ratio:", max(abs(center)) / static_center)
