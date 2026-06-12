import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS


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
        fig,ax=plt.subplots(figsize=(12.0,7.4))
        for i,d in enumerate(orders):
            y=np.array([real_polylog(d,v) for v in x])
            y[np.abs(y)>4]=np.nan
            ax.plot(x,y,color=COLORS[i],label=rf"$\nu={d:g}$")
        ax.set(xlabel=r"$x$",ylabel=r"$\operatorname{Li}_{\nu}(x)$")
        ax.set_xlim(-2.5,1.2); ax.set_ylim(-2.1,3.1)
        polish_axes(ax); add_legend(ax, outside=False, loc="upper left")
        save_figure(fig,"polylogarithm_function.png")
if __name__=="__main__": main()
