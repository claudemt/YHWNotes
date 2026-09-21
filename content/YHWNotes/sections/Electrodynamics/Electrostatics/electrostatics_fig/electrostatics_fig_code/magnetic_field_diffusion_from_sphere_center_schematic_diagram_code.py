import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS


def main():
    t = np.linspace(1e-4, 2.0, 1600)
    y = erf(1.0 / (2.0 * np.sqrt(t))) - np.exp(-1.0 / (4.0 * t)) / np.sqrt(np.pi * t)
    with figure_style():
        fig, ax = plt.subplots()
        ax.plot(t, y, color=COLORS[0])
        ax.set(xlabel=r"$\nu t$", ylabel=r"$B(0,t)/B_0$")
        ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.04)
        polish_axes(ax)
        save_figure(fig, "magnetic_field_diffusion_from_sphere_center_schematic_diagram.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)

if __name__ == "__main__": main()
