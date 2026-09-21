import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, add_legend, COLORS


def profile(z, tau):
    return 0.5 * (erf((1 + np.abs(z)) / (2 * np.sqrt(tau))) + erf((1 - np.abs(z)) / (2 * np.sqrt(tau))))


def main():
    z = np.linspace(-4, 4, 1800)
    taus = [0.01, 0.1, 1.0]
    with figure_style():
        fig, ax = plt.subplots()
        for i, tau in enumerate(taus):
            ax.plot(z, profile(z, tau), color=COLORS[i], label=rf"$\nu t={tau:g}$")
        ax.set(xlabel=r"$z/a$", ylabel=r"$H(z,t)/H_0$")
        ax.set_xlim(-4, 4); ax.set_ylim(0, 1.04)
        polish_axes(ax); add_legend(ax, loc="upper right")
        save_figure(fig, "one_dimensional_magnetic_field_diffusion_schematic_diagram.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)

if __name__ == "__main__": main()
