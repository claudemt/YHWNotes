import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / "fig"))
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS


def profile(z, tau):
    return 0.5 * (erf((1 + np.abs(z)) / (2 * np.sqrt(tau))) + erf((1 - np.abs(z)) / (2 * np.sqrt(tau))))


def main():
    z = np.linspace(-4, 4, 1800)
    taus = [0.01, 0.1, 1.0]
    with figure_style():
        fig, ax = plt.subplots(figsize=(12.6, 7.4))
        for i, tau in enumerate(taus):
            ax.plot(z, profile(z, tau), color=COLORS[i], label=rf"$\nu t={tau:g}$")
        ax.set(xlabel=r"$z/a$", ylabel=r"$H(z,t)/H_0$",
               title=r"One-dimensional magnetic-field diffusion")
        ax.set_xlim(-4, 4); ax.set_ylim(0, 1.04)
        polish_axes(ax); add_legend(ax, outside=False, loc="upper right")
        save_figure(fig, "one_dimensional_magnetic_field_diffusion_schematic_diagram.png")

if __name__ == "__main__": main()
