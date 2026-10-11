"""Robin self-adjoint boundary reflection and normalized bound states."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]

k=np.linspace(0.035,6,600)
x=np.linspace(0,5,300)
with figure_style():
    fig,(ax,bx)=plt.subplots(1,2,figsize=(8.1,3.45))
    for i,h in enumerate((-2.0,-0.6,0.6,2.0)):
        r=(1j*k+h)/(1j*k-h)
        phase=np.unwrap(np.angle(r))
        ax.plot(k,phase/np.pi,label=rf'$h={h:g}$',color=COLORS[i])
    ax.set(xlim=(0,6),xlabel=r'Wave number $k$',ylabel=r'Unwrapped $\arg\mathcal{R}_h(k)/\pi$')
    ax.set_yticks(np.arange(-1.25,1.26,0.5))
    add_legend(ax,corner='upper right',ncol=1)
    polish_axes(ax,grid=True)
    for i,h in enumerate((-0.6,-1,-2)):
        density=(-2*h)*np.exp(2*h*x)
        bx.plot(x,density,color=COLORS[i],label=rf'$h={h:g}$')
    bx.set(xlim=(0,5),ylim=(0,4.15),xlabel=r'Position $x$',ylabel=r'$|\psi_{\rm b}(x)|^2$')
    add_legend(bx,corner='upper right'); polish_axes(bx,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'robin_scattering',OUT)
