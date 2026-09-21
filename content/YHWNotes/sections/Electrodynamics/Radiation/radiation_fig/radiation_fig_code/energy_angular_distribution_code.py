import numpy as np
import matplotlib.pyplot as plt

import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import COLORS, add_legend, figure_style, polish_polar_axes, save_figure


def antenna_pattern(theta, kd):
    numerator = np.cos(0.5 * kd * np.cos(theta)) - np.cos(0.5 * kd)
    denominator = np.sin(theta)
    with np.errstate(divide="ignore", invalid="ignore"):
        value = (numerator / denominator) ** 2
    return np.nan_to_num(value, nan=0.0, posinf=0.0, neginf=0.0)


def main():
    theta = np.linspace(0.0, 2.0 * np.pi, 3600)
    kd_values = (7.0, 9.5, 11.0)
    with figure_style():
        fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
        for i, kd in enumerate(kd_values):
            ax.plot(theta, antenna_pattern(theta, kd), color=COLORS[i], label=rf"$kd={kd:g}$")
        ax.set_rlim(0.0, 4.2)
        polish_polar_axes(ax, radial_grid=True, radial_labels=False)
        add_legend(ax)
        save_figure(fig, "energy_angular_distribution.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
