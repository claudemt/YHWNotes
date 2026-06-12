import numpy as np
import matplotlib.pyplot as plt

from fig_style_python import COLORS, add_legend, figure_style, polish_polar_axes, save_figure


def f_harmonic(theta, beta):
    s, c = np.sin(theta), np.cos(theta)
    return s**2 * (4 + beta**2 * c**2) / (1 - beta**2 * c**2)**3.5


def log10_intensity(values):
    return np.log10(np.maximum(values, 1.0e-3))


def plot_log_curve(ax, theta, values, *, floor, **kwargs):
    return ax.plot(theta, log10_intensity(values) - floor, **kwargs)


def main():
    theta = np.linspace(0, 2 * np.pi, 3600)
    log_floor = -3.0
    log_ticks = np.arange(-3.0, 4.1, 1.0)
    with figure_style():
        fig, ax = plt.subplots(figsize=(11.2, 9.5), subplot_kw={"projection": "polar"})
        for i, beta in enumerate((0.7, 0.8, 0.9)):
            plot_log_curve(
                ax,
                theta,
                f_harmonic(theta, beta),
                floor=log_floor,
                color=COLORS[i],
                label=rf"$\beta={beta:.1f}$",
            )
        ax.set_title(r"Harmonic-motion radiation", pad=26)
        ax.set_rlim(0.0, 6.8)
        ax.set_yticks(log_ticks - log_floor)
        ax.set_yticklabels([rf"${tick:g}$" for tick in log_ticks])
        polish_polar_axes(ax, radial_grid=True, radial_labels=False)
        add_legend(ax, outside=False, loc="center", bbox_to_anchor=(1.15, 0.86))
        save_figure(fig, "harmonic_motion_radiation_angular_distribution.png")


if __name__ == "__main__":
    main()
