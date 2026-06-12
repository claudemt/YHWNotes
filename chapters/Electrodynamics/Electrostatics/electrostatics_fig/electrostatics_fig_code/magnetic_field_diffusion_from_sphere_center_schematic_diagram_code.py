import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from fig_style_python import figure_style, polish_axes, save_figure, COLORS


def main():
    t = np.linspace(1e-4, 2.0, 1600)
    y = erf(1.0 / (2.0 * np.sqrt(t))) - np.exp(-1.0 / (4.0 * t)) / np.sqrt(np.pi * t)
    with figure_style():
        fig, ax = plt.subplots(figsize=(11.5, 7.4))
        ax.plot(t, y, color=COLORS[0])
        ax.set(xlabel=r"$\nu t$", ylabel=r"$B(0,t)/B_0$",
               title=r"Magnetic-field diffusion from the centre of a sphere")
        ax.set_xlim(0, 2.0); ax.set_ylim(0, 1.04)
        polish_axes(ax)
        save_figure(fig, "magnetic_field_diffusion_from_sphere_center_schematic_diagram.png")

if __name__ == "__main__": main()
