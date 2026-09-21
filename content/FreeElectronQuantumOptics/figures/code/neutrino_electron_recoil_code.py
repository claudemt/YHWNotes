from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend
out=Path(__file__).resolve().parents[1]/'generated'
E,m=1.,.510999
tm=2*E**2/(m+2*E)
T=np.linspace(0,tm,400)
with figure_style():
    fig,ax=plt.subplots()
    for L,R,label,style,color in [(.731,.231,r'$\nu_e$', '-', 'C0'),(.231,.731,r'$\bar\nu_e$', '--','C0'),
                                 (-.269,.231,r'$\nu_\mu$', '-', 'C1'),(.231,-.269,r'$\bar\nu_\mu$', '--','C1')]:
        ax.plot(T,L*L+R*R*(1-T/E)**2-L*R*m*T/E**2,label=label,ls=style,color=color)
    ax.axvline(tm,color='.5',ls=':',lw=1)
    ax.set(xlabel=r'Electron recoil $T_e$ (MeV)',ylabel=r'$(d\sigma/dT_e)/C_{\nu e}$',xlim=(0,.82),ylim=(0,.78))
    polish_axes(ax)
    add_legend(ax, ncol=2)
    fig.tight_layout()
    save_pdf_png_pair(fig,'neutrino_electron_recoil',out)
    plt.close(fig)
