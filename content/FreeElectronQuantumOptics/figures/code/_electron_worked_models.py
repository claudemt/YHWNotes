from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c,hbar,e,m_e
from scipy.special import jv,ndtr
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from preamble import figure_style,polish_axes,save_pdf_png_pair,add_legend
OUT=Path(__file__).resolve().parents[1]/'generated'
gamma0=1+200e3*e/(m_e*c*c)
v0=c*np.sqrt(1-gamma0**-2)
omega=2*np.pi*c/800e-9
photon_eV=hbar*omega/e
kappa=omega/v0
mass_parallel=gamma0**3*m_e
recoil=hbar*kappa**2/(2*mass_parallel)

def lattice(ratio,area=np.pi,cutoff=25):
    ell=np.arange(-cutoff,cutoff+1)
    H=np.diag(ell*(ell-1.)).astype(float)
    H+=np.diag(np.full(2*cutoff,ratio/2),1)+np.diag(np.full(2*cutoff,ratio/2),-1)
    energy,basis=eigh(H)
    state=basis@(basis[cutoff,:,None]*np.exp(-1j*energy[:,None]*np.atleast_1d(area)/ratio))
    return ell,abs(state)**2

def density(theta,beta,phase,cutoff=30):
    ell=np.arange(-cutoff,cutoff+1)
    amp=jv(ell,2*beta)*np.exp(-1j*ell**2*phase)
    return abs(np.exp(1j*np.outer(theta,ell))@amp)**2

def spectrum(energy,beta,sigma):
    ell=np.arange(-30,31)
    delta=np.asarray(energy)[:,None]-ell*photon_eV
    return np.exp(-delta**2/(2*sigma*sigma))@(jv(ell,2*beta)**2)/(np.sqrt(2*np.pi)*sigma)

def bins(edges,beta,sigma):
    ell=np.arange(-30,31)
    response=np.diff(ndtr((np.asarray(edges)[:,None]-ell*photon_eV)/sigma),axis=0)
    return response@(jv(ell,2*beta)**2)

def reference(phases,p=.65,coherence=.2+.15j):
    u0,u1=jv(0,.8),jv(1,.8)
    return u0*u0*p+u1*u1*(1-p)-2*u0*u1*np.real(coherence*np.exp(1j*np.asarray(phases)))

def finish(fig,axes,stem):
    for ax in np.atleast_1d(axes): polish_axes(ax)
    fig.tight_layout()
    save_pdf_png_pair(fig,stem,OUT)
    plt.close(fig)
