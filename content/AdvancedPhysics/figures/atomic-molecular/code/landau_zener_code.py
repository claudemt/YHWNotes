from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair
with figure_style():
    t=np.linspace(-4,4,800); V=1.0; a=1.0; Ep=np.sqrt((a*t/2)**2+V**2)
    fig,ax=plt.subplots(); ax.plot(t,a*t/2,'--',label='Diabatic'); ax.plot(t,-a*t/2,'--'); ax.plot(t,Ep,label='Adiabatic'); ax.plot(t,-Ep)
    ax.annotate(r'$2|V|$',(0,V),xytext=(22,-30),textcoords='offset points',arrowprops={'arrowstyle':'->','lw':0.8})
    ax.set_xlabel('Sweep coordinate / time'); ax.set_ylabel('Energy (arb. units)'); add_legend(ax,loc='upper left',frameon=False); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'landau_zener',Path(__file__).resolve().parents[1]/'generated')
