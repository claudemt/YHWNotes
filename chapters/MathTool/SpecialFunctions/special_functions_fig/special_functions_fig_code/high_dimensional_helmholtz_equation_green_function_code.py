import numpy as np
import matplotlib.pyplot as plt
from scipy.special import kv
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / "fig"))
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS


def main():
    x=np.linspace(0.2,1.4,1200)
    with figure_style():
        fig,ax=plt.subplots(figsize=(12.0,7.4))
        for i,d in enumerate((1,2,3)):
            y=x**(1-d/2)*kv(d/2-1,x)
            ax.plot(x,y,color=COLORS[i],label=rf"$d={d}$")
        ax.set(xlabel=r"$x$",ylabel=r"$x^{1-d/2}K_{d/2-1}(x)$")
        ax.set_xlim(0.2,1.4)
        polish_axes(ax); add_legend(ax, outside=False, loc="upper right")
        save_figure(fig,"high_dimensional_helmholtz_equation_green_function.png")
if __name__=="__main__": main()
