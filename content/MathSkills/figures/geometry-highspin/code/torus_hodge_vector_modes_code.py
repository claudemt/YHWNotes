"""Exact vs coexact eigen-one-forms on the flat 2-torus, f=sin(2x+y)."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORMAPS,figure_style,polish_axes,save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
vals=np.linspace(0,2*np.pi,16,endpoint=False)
x,y=np.meshgrid(vals,vals,indexing='xy')
c=np.cos(2*x+y)
fields=[(2*c/np.sqrt(5),c/np.sqrt(5)),(-c/np.sqrt(5),2*c/np.sqrt(5))]
with figure_style():
    fig,axs=plt.subplots(1,2,figsize=(9.3,4.05))
    for ax,(u,v),title in zip(axs,fields,[r'Exact: $\mathrm{d}f$',r'Coexact: $*\mathrm{d}f$']):
        arrows=ax.quiver(x,y,u,v,c,cmap=COLORMAPS['signed_field'],clim=(-1,1),
                         scale=15,width=.0055,pivot='mid',headwidth=3.9,headlength=4.6)
        ax.set(title=title,xlabel=r'$x$',ylabel=r'$y$',xlim=(-.18,2*np.pi+.18),ylim=(-.18,2*np.pi+.18))
        ax.set_aspect('equal');ticks=[0,np.pi,2*np.pi]
        ax.set_xticks(ticks,['0',r'$\pi$',r'$2\pi$']);ax.set_yticks(ticks,['0',r'$\pi$',r'$2\pi$'])
        polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'torus_hodge_vector_modes',OUT)
