import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, add_legend, COLORS


def real_polylog(order, x):
    try:
        z=complex(mp.fp.polylog(order,float(x)))
        return z.real if abs(z.imag)<1e-9 else np.nan
    except Exception:
        return np.nan


def main():
    x=np.linspace(-2.5,1.18,1300)
    orders=(0.5,1.0,1.5,2.5)
    with figure_style():
        fig,ax=plt.subplots()
        for i,d in enumerate(orders):
            y=np.array([real_polylog(d,v) for v in x])
            y[np.abs(y)>4]=np.nan
            ax.plot(x,y,color=COLORS[i],label=rf"$\nu={d:g}$")
        ax.set(xlabel=r"$x$",ylabel=r"$\operatorname{Li}_{\nu}(x)$")
        ax.set_xlim(-2.5,1.2); ax.set_ylim(-2.1,3.1)
        polish_axes(ax); add_legend(ax, loc="upper left")
        save_figure(fig, "polylogarithm_function.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
