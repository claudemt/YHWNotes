import numpy as np
import matplotlib.pyplot as plt

import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import COLORS, figure_style, polish_axes, save_figure


def g_nu(nu):
    log_term = np.log1p(nu ** -2)
    numerator = (
        (5.0 * nu**3 + 6.0 * nu**5) * log_term
        - 6.0 * nu**3
        - 2.0 * nu
        + 2.0 * np.arctan(nu)
    )
    denominator = (
        (3.0 * nu + 2.0 * nu**3) * log_term
        - 2.0 * nu
        + 2.0 * np.arctan(nu)
    )
    return numerator / denominator


def main():
    nu = np.linspace(1.0e-3, 20.0, 2200)
    with figure_style():
        fig, ax = plt.subplots(figsize=(11.5, 7.4))
        ax.plot(nu, g_nu(nu), color=COLORS[1])
        ax.set(xlabel=r"$\nu_{\max}$", ylabel=r"$G(\nu_{\max})$")
        ax.set_xlim(0.0, 20.0)
        ax.set_ylim(0.0, 1.02)
        polish_axes(ax)
        save_figure(fig, "spectral_weight_function_g_nu_plot.png")


if __name__ == "__main__":
    main()
