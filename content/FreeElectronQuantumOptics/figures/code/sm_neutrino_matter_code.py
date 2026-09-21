from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend
out=Path(__file__).resolve().parents[1]/'generated'
hc=1.973269804e-7
V=np.sqrt(2)*1.16638e-23*hc**3*1.5e30
theta=np.deg2rad(8.6)
res=.0025*np.cos(2*theta)/(2*V)
energies=np.geomspace(.3,30,450)*1e9
def matter(E,potential):
    delta=.0025/(2*E)
    gap=np.hypot(delta*np.cos(2*theta)-potential,delta*np.sin(2*theta))
    return (delta*np.sin(2*theta)/gap)**2,gap
with figure_style():
    fig,axes=plt.subplots(1,2,figsize=(10,4.3))
    for potential,name,style in [(V,r'$\nu$','-'),(-V,r'$\bar\nu$','--')]:
        amp,gap=matter(energies,potential)
        axes[0].semilogx(energies/1e9,amp,label=name,ls=style)
    axes[0].axvline(res/1e9,color='.55',lw=1,ls=':')
    axes[0].set(xlabel=r'Energy $E_\nu$ (GeV)',ylabel=r'Mixing amplitude $\sin^2(2\theta_m)$',ylim=(0,1.3))
    lengths=np.linspace(0,22000,700)*1e3
    for potential,name,style in [(V,'Matter','-'),(0,'Vacuum','--')]:
        amp,gap=matter(res,potential)
        axes[1].plot(lengths/1e3,amp*np.sin(gap*lengths/(2*hc))**2,label=name,ls=style)
    axes[1].set(xlabel=r'Baseline $L$ (km)',ylabel=r'Conversion probability $P_{e\to x}$',ylim=(0,1.3))
    for ax in axes:
        polish_axes(ax)
        add_legend(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig,'sm_neutrino_matter',out)
    plt.close(fig)
