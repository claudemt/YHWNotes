import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from fig_style_python import figure_style, polish_axes, save_figure, COLORS

def response(F, s, a, zeta, eps=0.025):
    with np.errstate(divide="ignore", invalid="ignore"):
        return (
            (zeta / eps) ** 2
            + ((3 * s - 1) / eps - 3 * a * a / 8 - 3 * F * F / (4 * (1 - s * s) ** 2)) ** 2
            - F ** 6 / (8 * a * a * (1 - s * s) ** 6)
        )

def main():
    eps, force = 0.025, 2.0
    zetas = [0.0, 0.025, 0.05, 0.075]
    s = np.linspace(0.325, 0.45, 900)
    a = np.linspace(1e-3, 5.1, 900)
    S, A = np.meshgrid(s, a)
    with figure_style():
        fig, ax = plt.subplots(figsize=(12.8, 8.0))
        handles = []
        for i, zeta in enumerate(zetas):
            ax.contour(S, A, response(force, S, A, zeta, eps), levels=[0],
                       colors=[COLORS[i]], linewidths=2.8)
            handles.append(Line2D([0], [0], color=COLORS[i], label=rf"$\zeta={zeta:g}$"))
        ax.set(
            xlabel=r"$s$", ylabel=r"$a_s$",
            title=rf"Responce curve: $\epsilon={eps:g}$, $F={force:g}$",
            xlim=(0.325, 0.45), ylim=(0, 5.1),
        )
        polish_axes(ax)
        ax.legend(handles=handles, loc="upper left")
        save_figure(fig, "duffing_superharmonic_response_epsilon_negative.png")

if __name__ == "__main__":
    main()
