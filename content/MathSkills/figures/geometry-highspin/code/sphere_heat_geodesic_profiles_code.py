"""Exact Legendre-series sphere heat kernels as functions of geodesic distance."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import eval_legendre
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0,str(ROOT))
from preamble import COLORS,REFERENCE_LINE_STYLE,figure_style,polish_axes,add_legend,save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
theta=np.linspace(0,np.pi,600)
with figure_style():
    fig,ax=plt.subplots(figsize=(6.9,3.85))
    for i,q in enumerate((.06,.20,.75)):
        L=int(np.ceil(np.sqrt(45/q)))+4
        vals=np.zeros_like(theta)
        for l in range(L+1): vals+=(2*l+1)*np.exp(-q*l*(l+1))*eval_legendre(l,np.cos(theta))
        ax.plot(theta,vals,color=COLORS[i],label=rf'$t/R^2={q:g}$')
    ax.axhline(1,**REFERENCE_LINE_STYLE,label=r'$4\pi R^2K_{\infty}=1$')
    ax.set(xlabel=r'Geodesic angle $\theta$',ylabel=r'$4\pi R^2 K_t(\theta)$',xlim=(0,np.pi),ylim=(0,19))
    ax.set_xticks([0,np.pi/4,np.pi/2,3*np.pi/4,np.pi],labels=['0',r'$\pi/4$',r'$\pi/2$',r'$3\pi/4$',r'$\pi$'])
    add_legend(ax,'upper right'); polish_axes(ax,grid=True)
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'sphere_heat_geodesic_profiles',OUT)
