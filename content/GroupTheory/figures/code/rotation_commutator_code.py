#!/usr/bin/env python3
"""SO(3) rotation order and the quadratic commutator limit."""
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import (
    COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend,
    save_pdf_png_pair,
)

OUT = Path(__file__).resolve().parents[1] / "generated"
v = np.array([1.0, 0.0, 0.0])


def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((1, 0, 0), (0, c, -s), (0, s, c)))


def rotate_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, 0, s), (0, 1, 0), (-s, 0, c)))


small = np.geomspace(1e-3, 0.55, 70)
small_separation = np.array([
    np.linalg.norm((rotate_x(t) @ rotate_y(t) -
                    rotate_y(t) @ rotate_x(t)) @ v)
    for t in small
])
assert np.allclose(small_separation[:8] / small[:8]**2, 1, rtol=2e-5)

with figure_style():
    fig, ax = plt.subplots()
    ax.loglog(small, small**2, **REFERENCE_LINE_STYLE,
              label="$\\theta^2$ reference")
    ax.loglog(small, small_separation, color=COLORS[0], marker="o",
              markevery=8, label="rotation-order difference")
    ax.set(xlabel="angle $\\theta$", ylabel="$\\|(R_xR_y-R_yR_x)v\\|$")
    polish_axes(ax, grid=True)
    add_legend(ax, corner="upper left")
    fig.tight_layout()
    save_pdf_png_pair(fig, "rotation_commutator", OUT)
    plt.close(fig)

print("quadratic ratio at theta=0.001:", small_separation[0] / small[0]**2)
