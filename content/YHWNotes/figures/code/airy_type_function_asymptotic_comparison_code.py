import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv, kv
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, add_legend, COLORS


def relative_error(m,x):
    exact=jv(m,m*(1-x))
    approx=np.sqrt(2*x)/(np.pi*np.sqrt(3))*kv(1/3,m/3*(2*x)**1.5)
    return approx/exact-1


def main():
    x=np.linspace(1e-5,0.2,1800)
    with figure_style():
        fig,ax=plt.subplots()
        for i,m in enumerate((1,10,20)):
            ax.plot(x,relative_error(m,x),color=COLORS[i],label=rf"$m={m}$")
        ax.set(xlabel=r"$x$",ylabel="relative error")
        ax.set_xlim(0,0.2); ax.set_ylim(-0.012,0.17)
        polish_axes(ax); add_legend(ax, loc="upper left")
        save_figure(fig, "airy_type_function_asymptotic_comparison.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
