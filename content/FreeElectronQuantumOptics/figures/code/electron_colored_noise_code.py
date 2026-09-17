from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend
out=Path(__file__).resolve().parents[1]/'generated'
t=np.linspace(0,12,500)
free=.04*(t+np.expm1(-t))
echo=.04*(t+4*np.expm1(-t/2)-np.expm1(-t))
with figure_style():
    fig,axes=plt.subplots(1,2,figsize=(9.,4.))
    for ax,d in zip(axes,[1,3]):
        for chi,label,style in [(free,'Free','-'),(echo,'Ideal echo','--'),(.04*t,'Constant rate',':')]:
            ax.plot(t,np.exp(-d*d*chi),label=label,ls=style)
        ax.set(xlabel=r'Time $t/\tau_\varphi$',ylabel='Coherence factor',title=rf'$|\ell-m|={d}$',ylim=(0,1.05),xlim=(0,12))
        polish_axes(ax)
        add_legend(ax,loc='lower left' if d==1 else 'upper right')
    fig.tight_layout()
    save_pdf_png_pair(fig,'electron_colored_noise',out)
    plt.close(fig)
