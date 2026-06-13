import numpy as np
import matplotlib.pyplot as plt
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / "fig"))
from fig_style_python import figure_style, polish_axes, save_figure, LIGHT_BLUE, COLORS


def main():
    x=np.linspace(0,20,900); y=np.linspace(0,10,700); X,Y=np.meshgrid(x,y)
    region=(X>=27*Y/16)&((Y/8)*(X-63*Y/32)>=1)
    with figure_style():
        fig,ax=plt.subplots(figsize=(10.5,8.2))
        ax.contourf(X,Y,region.astype(float),levels=[0.5,1.5],colors=[LIGHT_BLUE])
        ax.contour(X,Y,region.astype(float),levels=[0.5],colors=[COLORS[0]],linewidths=2.8)
        ax.set(xlabel=r"$\sigma\epsilon/\zeta$",ylabel=r"$A^2\epsilon/\zeta$",title="Region of subharmonic resonance")
        ax.set_xlim(0,20); ax.set_ylim(0,10); polish_axes(ax)
        save_figure(fig,"duffing_system_subharmonic_resonance_response_plot.png")
if __name__=="__main__": main()
