"""Exact single-mode PINEM Fock-state kernel and its six physical diagnostics.

Input: |0,N>. U=exp(xi*b*a^dagger - xi.conj()*b^dagger*a), s=|xi|^2.
Positive electron order gains photons' energy. No phenomenological fit parameters.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
from scipy.special import eval_genlaguerre, gammaln, jv
from scipy.stats import poisson
from preamble import pubfig, safe_panel, safe_colorbar, clean, finish_pub


def fock_amplitude(n, N, xi):
    """<n,N-n|U|0,N>, exact for ideal unbounded electron ladder.
    Return zero for an impossible negative final photon number.
    """
    n=int(n); N=int(N)
    if N < 0 or N-n < 0:
        return 0j
    s=abs(xi)**2
    if n >= 0:
        return (np.exp(-s/2 + (gammaln(N-n+1)-gammaln(N+1))/2)
                * (-np.conj(xi))**n * eval_genlaguerre(N-n,n,s))
    l=-n
    return (np.exp(-s/2 + (gammaln(N+1)-gammaln(N+l+1))/2)
            * xi**l * eval_genlaguerre(N,l,s))


def fock_probability(n,N,s):
    return abs(fock_amplitude(n,N,np.sqrt(s)))**2


def distribution(N,s,nmax=32):
    n=np.arange(-nmax,nmax+1)
    p=np.array([fock_probability(k,N,s) for k in n])
    return n,p


def coherent_spectrum(mean,beta,nmax=8):
    """Photon-number averaged kernel for an initial coherent state.
    Source photon count is Poisson, and xi=beta/sqrt(mean).
    """
    Nlim=int(max(mean+11*np.sqrt(mean+1),30))
    ns=np.arange(-nmax,nmax+1)
    weights=poisson.pmf(np.arange(Nlim+1),mean)
    s=beta**2/mean
    p=np.zeros(len(ns))
    for N,w in enumerate(weights):
        if w>1e-14:
            p+=w*np.array([fock_probability(n,N,s) for n in ns])
    return ns,p


def make_figure():
    outfile=Path(__file__).with_suffix('.pdf')
    fig=pubfig(9.2,6.1,top=.91,bottom=.1,left=.085,right=.96)
    gs=fig.add_gridspec(2,3,wspace=.60,hspace=.49)
    ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
    # (a) exact transition response, n labels energy; intensity conditional on N
    Ns=np.arange(0,32)
    ns=np.arange(-11,12)
    s0=0.20
    Q=np.array([[fock_probability(int(n),int(N),s0) for N in Ns] for n in ns])
    im=ax[0].imshow(Q,extent=[-.5,31.5,-11.5,11.5],origin='lower',aspect='auto',cmap='magma',vmin=0)
    ax[0].set(xlabel='Photon number $N$',ylabel='Electron order $n$')
    safe_colorbar(fig,im,ax[0],r'$P(n\mid N)$')
    # (b) the carrier and multiple sidebands for different number states
    ns_b=np.arange(-14,15)
    for N in [0,4,12,30]:
        ax[1].plot(ns_b,[fock_probability(n,N,s0) for n in ns_b],'-o',ms=2.4,label=rf'$N={N}$')
    ax[1].set(xlabel='Electron order $n$',ylabel='Probability',xlim=(-11,11))
    ax[1].legend(frameon=False,loc='upper left',ncol=1,fontsize=7)
    # (c) detailed absorption-emission asymmetry versus input photon number
    Ns_c=np.arange(0,45)
    for s in [.03,.15,.36]:
        yy=np.array([fock_probability(-1,int(N),s)-fock_probability(1,int(N),s) for N in Ns_c])
        ax[2].plot(Ns_c,yy,label=rf'$|\xi|^2={s:g}$')
    ax[2].set(xlabel='Photon number $N$',ylabel=r'$P(-1)-P(+1)$')
    ax[2].axhline(0,color='.5',lw=.7)
    ax[2].legend(frameon=False,loc='best',fontsize=7)
    # (d) Laguerre zeros produce coherent suppression in specified channels
    sscan=np.linspace(0,4,440)
    for n in [0,1,2,3]:
        ax[3].plot(sscan,[fock_probability(n,8,s) for s in sscan],label=rf'$n={n}$')
    ax[3].set(xlabel=r'Pulse area $|\xi|^2$',ylabel=r'$P(n\mid N=8)$')
    ax[3].legend(frameon=False,loc='upper right',ncol=2,fontsize=7)
    # (e) absolute error of weak-coupling factorial-moment prediction
    eps=np.linspace(.001,1.3,140)
    for N in [2,8,20]:
        sw=eps/(N+1)
        exact=np.array([fock_probability(2,N,s) for s in sw])
        weak=(sw**2/4)*N*(N-1)
        ax[4].plot(eps,abs(exact-weak),label=rf'$N={N}$')
    ax[4].set(xlabel=r'Expansion scale $|\xi|^2(N+1)$',ylabel='Absolute error')
    ax[4].legend(frameon=False,loc='upper left',fontsize=7)
    # (f) fixed beta coherent scaling to classical Bessel pattern
    beta=1.7
    nc=np.arange(-7,8)
    ax[5].plot(nc,jv(nc,2*beta)**2,'k--',lw=1.6,label='Classical limit')
    for mean in [4,15,60]:
        n,p=coherent_spectrum(mean,beta,nmax=7)
        ax[5].plot(n,p,'-o',ms=2.6,label=rf'$\bar N={mean}$')
    ax[5].set(xlabel='Electron order $n$',ylabel='Probability')
    ax[5].legend(frameon=False,fontsize=7,loc='upper left',ncol=1)
    for i,a in enumerate(ax):
        safe_panel(a,chr(ord('a')+i))
        clean(a)
    finish_pub(fig,outfile)
    return outfile

if __name__=='__main__':
    print(make_figure())
