import numpy as np
import matplotlib.pyplot as plt

import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / "fig"))
from fig_style_python import COLORS, add_legend, figure_style, polish_polar_axes, save_figure

PARAMS = [(3.8, 1.5), (0.48, 0.95), (0.30, 1.10), (1.10, 0.85)]
LABELS = [rf"$\tilde{{\alpha}}={a:.2f},\ \tilde{{E}}={b:.2f}$" for a, b in PARAMS]


def disc(a, b):
    return a * a * b * b - (b * b - 1) * (a * a - 1)


def r_curve(index, phi):
    a, b = PARAMS[index]
    D = np.sqrt(disc(a, b))
    if index == 0:
        den = -a * b + D * np.cosh(np.sqrt(a * a - 1) * phi)
        return (a * a - 1) / np.sqrt(np.where(den > 0, den, np.nan))
    if index == 1:
        return (1 - a * a) / (a * b + D * np.cos(np.sqrt(1 - a * a) * phi))
    if index == 2:
        e = np.sqrt(1 - ((b * b - 1) * (a * a - 1)) / (a * a * b * b))
        return (1 - a * a) / (1 + e * np.cos(np.sqrt(1 - a * a) * phi))
    return (a * a - 1) / (-a * b + D * np.cosh(np.sqrt(a * a - 1) * phi))


def main():
    ranges = [(0.1, 8 * np.pi), (-8 * np.pi, 8 * np.pi), (-2.3, 2.3), (0, 8 * np.pi)]
    with figure_style():
        fig, ax = plt.subplots(figsize=(11.5, 9.7), subplot_kw={"projection": "polar"})
        for i, (lo, hi) in enumerate(ranges):
            phi = np.linspace(lo, hi, 6500)
            radius = r_curve(i, phi)
            visible = np.isfinite(radius) & (radius >= 0.0) & (radius <= 10.0)
            ax.plot(phi[visible], radius[visible], color=COLORS[i], label=LABELS[i])
        ax.scatter([0.0], [0.0], s=75, color="black", zorder=10, label="force centre")
        ax.set_rlim(0.0, 10.0)
        polish_polar_axes(ax, radial_grid=True, radial_labels=True)
        add_legend(ax, outside=True, bbox_to_anchor=(1.06, 0.5))
        save_figure(fig, "attractive_orbit_radius_vs_azimuth_examples.png")


if __name__ == "__main__":
    main()
