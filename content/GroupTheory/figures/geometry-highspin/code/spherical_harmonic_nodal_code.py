"""Reproducible teaching figure; analytical formula specified in chapter."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1] / 'generated'

# Real harmonic on S^2 proportional to Re(Y_4^2), normalization immaterial.
th=np.linspace(0,np.pi,240)
ph=np.linspace(-np.pi,np.pi,400)
TH,PH=np.meshgrid(th,ph,indexing='ij')
Z=(1-np.cos(TH)**2)*(7*np.cos(TH)**2-1)*np.cos(2*PH)
Z/=np.max(np.abs(Z))
with figure_style():
    fig,ax=plt.subplots(figsize=(6.7,3.6))
    im=ax.imshow(Z,origin='lower',extent=(-180,180,0,180),aspect='auto',cmap='RdBu_r',vmin=-1,vmax=1,interpolation='bilinear')
    ax.contour(np.rad2deg(ph),np.rad2deg(th),Z,levels=[0],colors='black',linewidths=.72)
    ax.set(xlabel=r'Azimuth $\phi$ (deg)',ylabel=r'Polar angle $\theta$ (deg)')
    ax.set_xticks([-180,-90,0,90,180]);ax.set_yticks([0,45,90,135,180]);polish_axes(ax)
    cb=fig.colorbar(im,ax=ax,pad=.025,shrink=.87)
    cb.set_label(r'$\mathrm{Re}\,Y_4^2$ (rescaled)')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'spherical_harmonic_nodal',OUT)
