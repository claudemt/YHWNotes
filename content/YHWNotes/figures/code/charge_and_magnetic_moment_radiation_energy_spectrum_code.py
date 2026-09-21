import numpy as np
import matplotlib.pyplot as plt

import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import COLORS, figure_style, polish_axes, save_figure, add_legend


def integrand_point_charge(nu):
    return (1.0 + 2.0 * nu**2) * np.log1p(nu ** -2) - 2.0


def integrand_magnetic_dipole(nu):
    return 5.0 * nu**2 * integrand_point_charge(nu)


def main():
    nu = np.linspace(1.0e-5, 8.0, 3000)

    with figure_style():
        fig, ax = plt.subplots()
        ax.plot(
            nu,
            integrand_point_charge(nu),
            color=COLORS[1],
            label=r"point charge",
        )
        ax.plot(
            nu,
            integrand_magnetic_dipole(nu),
            color=COLORS[4],
            label=r"magnetic dipole",
        )
        ax.set(xlabel=r"$\nu$", ylabel=r"$\nu$ spectrum power")
        ax.set_xlim(0.0, 8.0)
        ax.set_ylim(0.0, 1.0)
        polish_axes(ax)
        add_legend(ax, loc="upper right", framealpha=0.94)
        save_figure(fig, "charge_and_magnetic_moment_radiation_energy_spectrum.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
