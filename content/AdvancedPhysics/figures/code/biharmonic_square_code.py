#!/usr/bin/env python3
"""Navier biharmonic plate: two Poisson solves and mesh convergence."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import (
    COLORMAPS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend,
    save_pdf_png_pair,
)

OUT = Path(__file__).resolve().parents[1] / "generated"


def solve_plate(n):
    """Solve (-Delta_h)^2 u=f with u=Delta_h u=0 on a unit square."""
    h = 1.0 / (n + 1)
    x = h * np.arange(1, n + 1)
    xx, yy = np.meshgrid(x, x, indexing="ij")
    forcing = np.sin(np.pi * xx) * np.sin(np.pi * yy)
    one_d = diags((-np.ones(n - 1), 2 * np.ones(n), -np.ones(n - 1)),
                  (-1, 0, 1), format="csc") / h**2
    laplace = kron(one_d, eye(n, format="csc"), format="csc") + kron(
        eye(n, format="csc"), one_d, format="csc")
    # v=(-Delta_h)u; solve (-Delta_h)v=f, then (-Delta_h)u=v.
    v = spsolve(laplace, forcing.ravel(order="C"))
    u = spsolve(laplace, v).reshape((n, n), order="C")
    exact = forcing / (4 * np.pi**4)
    return x, u, exact


sizes = np.array([15, 31, 63, 127])
errors = []
for size in sizes:
    x, u, exact = solve_plate(int(size))
    errors.append(np.max(np.abs(u - exact)))
errors = np.asarray(errors)
h_values = 1.0 / (sizes + 1)
assert np.all(np.diff(errors) < 0)
assert np.all((errors[:-1] / errors[1:]) > 3.5)

with figure_style():
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 8.0))
    im = axes[0].imshow(u.T, origin="lower", extent=(0, 1, 0, 1),
                        cmap=COLORMAPS["field"],
                        vmin=0, vmax=1 / (4 * np.pi**4))
    axes[0].set(xlabel="$x$", ylabel="$y$", title="Discrete deflection")
    fig.colorbar(im, ax=axes[0], shrink=0.81, label="$u_h$")
    polish_axes(axes[0], grid=False)

    axes[1].loglog(h_values, errors, "o-", label="maximum error")
    axes[1].loglog(
        h_values, errors[-1] * (h_values / h_values[-1])**2,
        **REFERENCE_LINE_STYLE, label="$h^2$ reference")
    axes[1].set(xlabel="mesh spacing $h$", ylabel="$\\|u_h-u\\|_\\infty$",
                title="Second-order convergence")
    polish_axes(axes[1], grid=True)
    add_legend(axes[1], corner="upper left")
    fig.tight_layout()
    save_pdf_png_pair(fig, "biharmonic_square", OUT)
    plt.close(fig)

print("mesh sizes:", sizes)
print("maximum errors:", errors)
