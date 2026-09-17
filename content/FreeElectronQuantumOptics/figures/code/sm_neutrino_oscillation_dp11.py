from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import (  # noqa: E402
    add_legend,    COLORS,
    LINE_STYLES,
    figure_style,
    polish_axes,
    save_pdf_png_pair,
)

OUT = ROOT / "figures" / "generated"


def pmns(t12, t13, t23, delta):
    s12, c12 = np.sin(t12), np.cos(t12)
    s13, c13 = np.sin(t13), np.cos(t13)
    s23, c23 = np.sin(t23), np.cos(t23)
    e_m, e_p = np.exp(-1j * delta), np.exp(1j * delta)
    return np.array(
        [
            [c12 * c13, s12 * c13, s13 * e_m],
            [-s12 * c23 - c12 * s23 * s13 * e_p,
             c12 * c23 - s12 * s23 * s13 * e_p, s23 * c13],
            [s12 * s23 - c12 * c23 * s13 * e_p,
             -c12 * s23 - s12 * c23 * s13 * e_p, c23 * c13],
        ],
        dtype=complex,
    )


# Representative values are used only to expose the full three-flavor
# interference pattern; the plotted variable is the dimensionless phase.
U = pmns(np.deg2rad(33.4), np.deg2rad(8.6), np.deg2rad(49.0), np.deg2rad(195.0))
r = 0.030
x = np.linspace(0.0, 6.0 * np.pi, 1800)
phase = np.vstack([
    np.ones_like(x, dtype=complex),
    np.exp(-2j * r * x),
    np.exp(-2j * x),
])
alpha = 1
probs = []
for beta in range(3):
    amp = np.sum((U[beta, :] * np.conjugate(U[alpha, :]))[:, None] * phase, axis=0)
    probs.append(np.abs(amp) ** 2)
probs = np.asarray(probs)

with figure_style():
    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    labels = [
        r"$P_{\nu_\mu\to\nu_e}$",
        r"$P_{\nu_\mu\to\nu_\mu}$",
        r"$P_{\nu_\mu\to\nu_\tau}$",
    ]
    for i, (y, label) in enumerate(zip(probs, labels)):
        ax.plot(x / np.pi, y, label=label, color=COLORS[i], linestyle=LINE_STYLES[i])
    ax.plot(
        x / np.pi,
        probs.sum(axis=0),
        label=r"$\sum_\beta P_{\mu\to\beta}$",
        color=COLORS[5],
        linestyle="--",
    )
    ax.set_xlabel(r"$\Delta_{31}/\pi$")
    ax.set_ylabel("probability")
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(-0.03, 1.27)
    polish_axes(ax, grid=True)
    add_legend(ax, ncol=2, frameon=True, framealpha=0.94, corner="upper right")
    fig.tight_layout()
    save_pdf_png_pair(fig, "sm_neutrino_oscillation_dp11", output_dir=OUT)
