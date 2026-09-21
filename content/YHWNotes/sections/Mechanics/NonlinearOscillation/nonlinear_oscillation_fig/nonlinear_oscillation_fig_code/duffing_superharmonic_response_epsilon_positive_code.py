import numpy as np
import matplotlib.pyplot as plt
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS, add_legend
from matplotlib.lines import Line2D

def response(F,s,a,zeta,eps):
    with np.errstate(divide="ignore",invalid="ignore"):
        return (zeta/eps)**2+((3*s-1)/eps-3*a*a/8-3*F*F/(4*(1-s*s)**2))**2-F**6/(8*a*a*(1-s*s)**6)

def make_plot(eps,xlim,ylim,filename):
    Fs=[1.6,1.8,2.0,2.2]; zeta=0.04
    s=np.linspace(*xlim,850); a=np.linspace(1e-3,ylim[1],850); S,A=np.meshgrid(s,a)
    with figure_style():
        fig,ax=plt.subplots(); handles=[]
        for i,F in enumerate(Fs):
            ax.contour(S,A,response(F,S,A,zeta,eps),levels=[0],colors=[COLORS[i]],linewidths=2.8)
            handles.append(Line2D([0],[0],color=COLORS[i],label=rf"$F={F:g}$"))
        ax.set(xlabel=r"$s$",ylabel=r"$a_s$")
        ax.set_xlim(*xlim); ax.set_ylim(*ylim); polish_axes(ax); add_legend(ax, handles=handles, loc="upper left")
        save_figure(fig, filename, output_dir=pathlib.Path(__file__).resolve().parent.parent)


def main(): make_plot(0.025,(0.325,0.45),(0,5),"duffing_superharmonic_response_epsilon_positive.png")
if __name__=="__main__": main()
