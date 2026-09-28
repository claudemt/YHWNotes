from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, m_e, e

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, figure_style, polish_axes, save_pdf_png_pair, add_legend  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "generated"
OUT.mkdir(parents=True, exist_ok=True)

# Exact relativistic dispersion and its local first/second-order expansions.
with figure_style():
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    mc2 = m_e * c**2
    K0 = 200.0e3 * e
    E0 = mc2 + K0
    p0 = np.sqrt(E0**2 - mc2**2) / c
    v0 = c**2 * p0 / E0
    gamma0 = E0 / mc2
    mpar = gamma0**3 * m_e
    q = np.linspace(-0.38, 0.38, 700)
    dp = q * p0
    E_exact = np.sqrt(mc2**2 + c**2 * (p0 + dp) ** 2)
    y_exact = (E_exact - E0) / mc2
    y_lin = v0 * dp / mc2
    y_quad = (v0 * dp + dp**2 / (2.0 * mpar)) / mc2
    ax.plot(q, y_exact, color=COLORS[0], label="exact relativistic dispersion")
    ax.plot(q, y_lin, linestyle="--", color=COLORS[1], label="linear expansion")
    ax.plot(q, y_quad, linestyle="-.", color=COLORS[2], label="quadratic expansion")
    ax.set_xlabel(r"$\delta p/p_0$")
    ax.set_ylabel(r"$(E-E_0)/(m_ec^2)$")
    add_legend(ax, frameon=True)
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, "dispersion_control", output_dir=OUT)
