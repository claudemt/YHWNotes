from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair
with figure_style():
    x=np.linspace(-3.5,-0.08,800); T=0.25*(1+(2*x)**2)/np.abs(2*x)
    fig,ax=plt.subplots(); ax.plot(x,T,label=r'$k_B T/(\hbar\Gamma_{\rm sp})$'); ax.scatter([-0.5],[0.5],zorder=4)
    ax.annotate(r'$\Delta=-\Gamma/2$' + '\n' + r'$T_D=\hbar\Gamma/(2k_B)$',(-0.5,0.5),xytext=(-90,52),textcoords='offset points',arrowprops={'arrowstyle':'->','lw':0.8})
    ax.set_xlabel(r'Detuning $\Delta/\Gamma_{\rm sp}$'); ax.set_ylabel(r'$k_B T/(\hbar\Gamma_{\rm sp})$'); ax.set_ylim(0.42,2.4)
    add_legend(ax); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'doppler_limit',Path(__file__).resolve().parents[1]/'generated')
