import numpy as np
import matplotlib.pyplot as plt
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS, add_dual_legend
from matplotlib.lines import Line2D

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

def group_velocity(m, theta, omega_func):
    h = 1.0e-5
    theta_plus = np.minimum(theta + h, THETA_MAX - 1.0e-7)
    theta_minus = np.maximum(theta - h, 1.0e-7)
    omega_plus = omega_func(m, theta_plus)
    omega_minus = omega_func(m, theta_minus)
    beta_plus = N1 * omega_plus * np.cos(theta_plus)
    beta_minus = N1 * omega_minus * np.cos(theta_minus)
    return (omega_plus - omega_minus) / (beta_plus - beta_minus)

def displacement_te(m, theta):
    return 2*np.cos(theta)/(np.sin(theta)*omega_te(m,theta)*delta(theta))


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
    theta=np.linspace(0.003, THETA_MAX-0.018, 1800)
    with figure_style():
        fig,ax=plt.subplots()
        for i,m in enumerate((0,1,2)):
            ax.plot(theta,group_velocity(m,theta,omega_te),color=COLORS[i],ls="-")
            ax.plot(theta,group_velocity(m,theta,omega_tm),color=COLORS[i],ls="--")
        ax.set(xlabel=r"$\theta\;(\mathrm{rad})$",ylabel=r"$v_m/c$")
        ax.set_xlim(0,THETA_MAX); ax.set_ylim(0.32,0.65)
        polish_axes(ax); add_waveguide_legends(ax, loc="upper left")
        save_figure(fig, "group_velocity_relation.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
