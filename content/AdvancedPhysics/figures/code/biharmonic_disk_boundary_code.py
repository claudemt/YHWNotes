#!/usr/bin/env python3
"""A biharmonic Fourier mode on the unit disk with zero edge slope."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORMAPS, figure_style, polish_axes, save_pdf_png_pair

OUT = Path(__file__).resolve().parents[1] / "generated"

grid = np.linspace(-1.0, 1.0, 401)
x, y = np.meshgrid(grid, grid)
r = np.hypot(x, y)
theta = np.arctan2(y, x)
inside = r <= 1.0
u = np.ma.masked_where(~inside, (2.0 * r**2 - r**4) * np.cos(2.0 * theta))

theta_edge = np.linspace(0.0, 2.0 * np.pi, 257)
edge_u = np.cos(2.0 * theta_edge)
r_edge = np.ones_like(theta_edge)
edge_slope = (4.0 * r_edge - 4.0 * r_edge**3) * edge_u
assert np.allclose(edge_u[[0, 64, 128, 192, 256]], [1, -1, 1, -1, 1])
assert np.allclose(edge_slope, 0.0)

with figure_style():
    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    image = ax.contourf(
        x, y, u, levels=np.linspace(-1.0, 1.0, 25),
        cmap=COLORMAPS["signed_field"], vmin=-1.0, vmax=1.0, extend="both",
    )
    ax.plot(np.cos(theta_edge), np.sin(theta_edge), color="black", linewidth=1.0)
    ax.set(xlabel="$x$", ylabel="$y$", title="Biharmonic disk solution")
    ax.set_aspect("equal", adjustable="box")
    fig.colorbar(image, ax=ax, shrink=0.82, label="$u(r,\\theta)$")
    polish_axes(ax, grid=False)
    fig.tight_layout()
    save_pdf_png_pair(fig, "biharmonic_disk_boundary", OUT)
    plt.close(fig)

print("boundary displacement: cos(2 theta)")
print("maximum boundary-slope residual:", float(np.max(np.abs(edge_slope))))
