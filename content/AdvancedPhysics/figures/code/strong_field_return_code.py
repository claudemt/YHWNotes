from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
ROOT = Path(__file__).resolve().parents[5]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

def F(phi_r,phi_0): return np.cos(phi_r)-np.cos(phi_0)+(phi_r-phi_0)*np.sin(phi_0)
def first_return(phi0):
    xs=np.linspace(phi0+1e-3,phi0+2*np.pi,3000); vals=F(xs,phi0)
    for a,b,fa,fb in zip(xs[:-1],xs[1:],vals[:-1],vals[1:]):
        if fa==0 or fa*fb<0:
            try:
                r=brentq(lambda x:F(x,phi0),a,b)
                if r>phi0+0.05: return r
            except ValueError: pass
    return np.nan
with figure_style():
    phi0=np.linspace(0.03,1.15,500); phir=np.array([first_return(x) for x in phi0]); mask=np.isfinite(phir); phi0=phi0[mask]; phir=phir[mask]
    Kret=2*(np.sin(phir)-np.sin(phi0))**2; Kresc=2*(2*np.sin(phir)-np.sin(phi0))**2; imax=np.argmax(Kret); jmax=np.argmax(Kresc)
    fig,ax=plt.subplots(); ax.plot(phi0,Kret,label=r'$K_{\rm ret}/U_p$'); ax.plot(phi0,Kresc,label=r'$K_{\rm resc}/U_p$'); ax.scatter([phi0[imax]],[Kret[imax]],zorder=4); ax.scatter([phi0[jmax]],[Kresc[jmax]],zorder=4)
    ax.annotate(f'{Kret[imax]:.2f}',(phi0[imax],Kret[imax]),xytext=(10,10),textcoords='offset points'); ax.annotate(f'{Kresc[jmax]:.2f}',(phi0[jmax],Kresc[jmax]),xytext=(10,-16),textcoords='offset points')
    ax.set_xlabel(r'Ionization phase $\phi_0$ (rad)'); ax.set_ylabel(r'Energy / $U_p$'); ax.set_xlim(phi0.min(),phi0.max()); ax.set_ylim(0,max(Kresc)*1.08)
    add_legend(ax); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'strong_field_return',Path(__file__).resolve().parents[1]/'generated')
