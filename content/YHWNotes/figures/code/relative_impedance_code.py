import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sici

import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import COLORS, figure_style, polish_axes, save_figure

EULER_GAMMA = 0.5772156649015329


def relative_impedance(x):
    si_x, ci_x = sici(x)
    si_2x, ci_2x = sici(2.0 * x)
    value = (
        EULER_GAMMA
        + np.log(x)
        - (1.0 + np.cos(x)) * ci_x
        + 0.5 * np.cos(x) * (EULER_GAMMA + ci_2x + np.log(0.5 * x))
        + 0.5 * np.sin(x) * (-2.0 * si_x + si_2x)
    )
    return value / (2.0 * np.pi)


def main():
    x = np.linspace(1.0e-3, 40.0, 2400)
    with figure_style():
        fig, ax = plt.subplots()
        ax.plot(x, relative_impedance(x), color=COLORS[1])
        ax.set(xlabel=r"$kd$", ylabel=r"$z_{\mathrm{rad}}$")
        ax.set_xlim(0.0, 40.0)
        ax.set_ylim(0.0, 1.08)
        polish_axes(ax)
        save_figure(fig, "relative_impedance.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
