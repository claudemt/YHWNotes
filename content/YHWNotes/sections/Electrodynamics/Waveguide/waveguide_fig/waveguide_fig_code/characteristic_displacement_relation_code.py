import numpy as np
import matplotlib.pyplot as plt
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS, Line2D, add_dual_legend

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

def displacement_tm(m, theta):
    d = delta(theta)
    denominator = (N1**4*np.cos(theta)**2 + N2**4*np.sin(theta)**2 - N1**2*N2**2) * d
    numerator = (N1**2 - N2**2) * N2**2 * np.cos(theta) / np.sin(theta)
    return 2 * numerator / (omega_tm(m, theta) * denominator)


def add_waveguide_legends(ax, *, loc):
    style_handles = [
        Line2D([0], [0], color="black", lw=2.8, ls="-", label=r"$\mathrm{TE}$"),
        Line2D([0], [0], color="black", lw=2.8, ls="--", label=r"$\mathrm{TM}$"),
    ]
    mode_handles = [
        Line2D([0], [0], color=COLORS[i], lw=2.8, label=rf"$m={m}$")
        for i, m in enumerate((0, 1, 2))
    ]
    return add_dual_legend(ax, style_handles, mode_handles,
                           kw1=dict(loc="upper left"), kw2=dict(loc="upper left", bbox_to_anchor=(0.0, 0.73)))


def main():
    theta=np.linspace(0.035, THETA_MAX-0.018, 1800)
    with figure_style():
        fig,ax=plt.subplots(figsize=(11.8,7.5))
        for i,m in enumerate((0,1,2)):
            ax.plot(theta,displacement_te(m,theta),color=COLORS[i],ls="-")
            ax.plot(theta,displacement_tm(m,theta),color=COLORS[i],ls="--")
        ax.set(xlabel=r"$\theta\;(\mathrm{rad})$",ylabel=r"$D_m/a$",title=r"Characteristic displacement relation")
        ax.set_xlim(0,THETA_MAX); ax.set_ylim(0,6.6)
        polish_axes(ax); add_waveguide_legends(ax, loc="upper left")
        save_figure(fig,"characteristic_displacement_relation.png")
if __name__=="__main__": main()
