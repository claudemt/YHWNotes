import numpy as np
import matplotlib.pyplot as plt
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS, LIGHT_BLUE, add_legend
from matplotlib.lines import Line2D

def f_region(s,A,eps,zeta):
    return eps**2*A**4-(16/9)*(s*s-1)*eps*A*A+(16/27)*((s*s-1)**2+4*zeta*zeta*s*s)
def g_turn(s,A,eps,zeta): return eps*A*A-(4/3)*(2*zeta*zeta+s*s-1)
def B_value(s,A,eps,zeta,negative=False):
    val=A*np.sqrt((1-s*s+3*eps*A*A/4)**2+(2*zeta*s)**2)
    return val/abs(eps) if negative else val


def main():
    eps,zeta=0.14,0.12; Bs=[0.2,0.4,0.6,0.8]
    s=np.linspace(0,2,850); A=np.linspace(0,2.75,750); S,AA=np.meshgrid(s,A)
    with figure_style():
        fig,ax=plt.subplots()
        ax.contourf(S,AA,f_region(S,AA,eps,zeta),levels=[-1e9,0],colors=[LIGHT_BLUE])
        handles=[]
        for i,b in enumerate(Bs):
            ax.contour(S,AA,B_value(S,AA,eps,zeta)-b,levels=[0],colors=[COLORS[i]],linewidths=2.8)
            handles.append(Line2D([0],[0],color=COLORS[i],label=rf"$B={b:g}$"))
        ax.contour(S,AA,g_turn(S,AA,eps,zeta),levels=[0],colors="black",linestyles="--",linewidths=2.2)
        ax.contour(S,AA,f_region(S,AA,eps,zeta),levels=[0],colors="gray",linestyles="--",linewidths=2.2)
        handles += [Line2D([0],[0],color="black",ls="--",label=r"$\mathrm{d}a_s=0$"),Line2D([0],[0],color="gray",ls="--",label=r"$\mathrm{d}s=0$")]
        ax.set(xlabel=r"$s$",ylabel=r"$a_s$")
        ax.set_xlim(0,2); ax.set_ylim(0,2.75); polish_axes(ax); add_legend(ax, handles=handles, corner="upper left")
        save_figure(fig, "duffing_near_resonance_phase_portrait_epsilon_positive.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
