import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS

N1, N2 = 2.5, 1.5
THETA_MAX = np.arccos(N2/N1)

def delta(theta):
    return np.sqrt(np.maximum(N1**2*np.cos(theta)**2-N2**2, 0.0))

def omega_te(m, theta):
    return (m*np.pi/2 + np.arctan2(delta(theta), N1*np.sin(theta))) / (N1*np.sin(theta))

def omega_tm(m, theta):
    return (m*np.pi/2 + np.arctan2(N1*delta(theta), N2**2*np.sin(theta))) / (N1*np.sin(theta))

def group_velocity_te(m, theta):
    w = omega_te(m, theta); d = delta(theta)
    return (np.cos(theta)/N1) * (1 + 1/(w*d)) / (1 + np.cos(theta)**2/(w*d))

def displacement_te(m, theta):
    return 2*np.cos(theta)/(np.sin(theta)*omega_te(m,theta)*delta(theta))


def add_waveguide_legends(ax, *, loc):
    mode_handles = [
        Line2D([0], [0], color=COLORS[i], lw=2.8, label=rf"$m={m}$")
        for i, m in enumerate((0, 1, 2))
    ]
    style_handles = [
        Line2D([0], [0], color="black", lw=2.8, ls="-", label=r"$\mathrm{TE}$"),
        Line2D([0], [0], color="black", lw=2.8, ls="--", label=r"$\mathrm{TM}$"),
    ]
    style_legend = ax.legend(handles=style_handles, loc=loc, frameon=False)
    ax.add_artist(style_legend)
    return ax.legend(handles=mode_handles, loc="center right", frameon=True, framealpha=0.94)


def main():
    theta=np.linspace(0.035, THETA_MAX-0.018, 1800)
    with figure_style():
        fig,ax=plt.subplots(figsize=(11.8,7.5))
        for i,m in enumerate((0,1,2)):
            ax.plot(theta,omega_te(m,theta),color=COLORS[i],ls="-")
            ax.plot(theta,omega_tm(m,theta),color=COLORS[i],ls="--")
        ax.set(xlabel=r"$\theta\;(\mathrm{rad})$",ylabel=r"$\omega_m a/c$",title=r"Angular-frequency relation")
        ax.set_xlim(0,THETA_MAX); ax.set_ylim(0,17)
        polish_axes(ax); add_waveguide_legends(ax, loc="upper right")
        save_figure(fig,"angular_frequency_relation.png")
if __name__=="__main__": main()
