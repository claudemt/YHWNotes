"""Information loss in phase-stepped PINEM under a calibrated Gaussian detector.

Computes exact derivatives of coherent Bessel probabilities, followed by a
parameter-independent stochastic detection response.  Four phase settings
with equal electron dose measure two Cartesian quadratures of beta.
"""
from pathlib import Path
import numpy as np
from scipy.special import jv,jvp
from scipy.special import ndtr
from common import atlas_figure,atlas_save,ATLAS_COLORS
from phase_reference_response import X,Y,B,N,PHASES,coupling,populations
OUT=Path(__file__).with_suffix('.pdf')
C=ATLAS_COLORS
# finite bin width in hbar omega units, with near-unity coverage
OBS=np.arange(-18,18.0001,.25)
EDGES=np.r_[OBS-.125,OBS[-1]+.125]

def response(sigma):
    if sigma<=0: raise ValueError('positive Gaussian width required')
    r=ndtr((EDGES[1:,None]-N[None,:])/sigma)-ndtr((EDGES[:-1,None]-N[None,:])/sigma)
    return r/np.maximum(r.sum(axis=0,keepdims=True),1e-300)

def fisher(b=B,sigma=.7,x=X,y=Y,blur=True):
    R=response(sigma) if blur else None
    F=np.zeros((2,2))
    for phi in PHASES:
        z=coupling(phi,b,x,y); g=np.abs(z)
        jj=jv(N,2*g); p=jj**2
        # d[J_n(2g)^2]/dg = 4 J_n(2g) J'_n(2g)
        dpdg=4*jj*jvp(N,2*g)
        grad=np.array([(z.real)/max(g,1e-15),(z.imag)/max(g,1e-15)])
        dq=dpdg[:,None]*grad[None,:]
        if blur:
            p=R@p;dq=R@dq
        F += ((dq[:,:,None]*dq[:,None,:])/np.maximum(p[:,None,None],1e-13)).sum(axis=0)/4
    return .5*(F+F.T)

def ellipse(ax,F,scale=1.,color=None,label=None):
    inv=np.linalg.inv(F)
    ev,vec=np.linalg.eigh(inv)
    ang=np.linspace(0,2*np.pi,260)
    xy=vec@(np.sqrt(np.maximum(ev,0))[:,None]*np.stack([np.cos(ang),np.sin(ang)]))*scale
    ax.plot(xy[0],xy[1],c=color,label=label)


def render():
    fig,axs=atlas_figure()
    a,b,c,d,e,f=axs
    R=response(.7)
    im=a.imshow(R,origin='lower',aspect='auto',extent=[N[0]-.5,N[-1]+.5,OBS[0]-.125,OBS[-1]+.125],cmap='viridis',vmin=0,vmax=.22)
    a.set(xlim=(-9,9),ylim=(-10,10),xlabel=r'True sideband $n$',ylabel=r'Measured $E/(\hbar\omega)$')
    cb=fig.colorbar(im,ax=a,shrink=.75);cb.set_ticks([0,.1,.2]);cb.ax.set_yticklabels(['0','0.1','0.2'])

    p=populations(PHASES[0])
    # Integrate over unit-width detector channels so both displayed quantities
    # are discrete channel probabilities (not a mixture of mass and density).
    coarse=ndtr((N[:,None]+.5-N[None,:])/.7)-ndtr((N[:,None]-.5-N[None,:])/.7)
    q=coarse@p
    b.stem(N,p,linefmt=C[0],markerfmt=' ',basefmt=' ',label='Ideal')
    b.plot(N,q,color=C[1],label='Measured channels')
    b.set(xlim=(-9,9),xlabel=r'Electron order $n$',ylabel=r'$P_n$')
    b.legend(loc='upper right',fontsize=7.4)

    bvals=np.linspace(.12,2.0,55)
    eig0=np.array([np.linalg.eigvalsh(fisher(bv,.7,blur=False))[0] for bv in bvals])
    eig1=np.array([np.linalg.eigvalsh(fisher(bv,.7,blur=True))[0] for bv in bvals])
    c.plot(bvals,eig0,c=C[0],label='Ideal channels');c.plot(bvals,eig1,c=C[1],label=r'$\sigma_E=0.7$')
    c.set(xlabel=r'Reference coupling $B$',ylabel=r'$\lambda_{\min}(F_1)$')
    c.legend(loc='upper right',fontsize=7.3)

    sigmas=np.linspace(.18,1.5,37)
    eig=np.array([np.linalg.eigvalsh(fisher(B,ss))[0] for ss in sigmas])
    d.plot(sigmas,eig,c=C[0]);d.axhline(np.linalg.eigvalsh(fisher(B,.7,blur=False))[0],ls='--',color=C[1],label='Ideal')
    d.set(xlabel=r'Resolution $\sigma_E/(\hbar\omega)$',ylabel=r'$\lambda_{\min}(F_1)$')
    d.legend(loc='upper right',fontsize=7.4)

    # Unit electron FI ellipses, magnified for visibility: factor sqrt(1/N) suppressed.
    ellipse(e,fisher(B,.7,blur=False),color=C[0],label='Ideal')
    ellipse(e,fisher(B,.7,blur=True),color=C[1],label=r'$\sigma_E=0.7$')
    e.set(xlabel=r'$\delta\operatorname{Re}\beta$',ylabel=r'$\delta\operatorname{Im}\beta$')
    e.set_aspect('equal',adjustable='datalim');e.legend(loc='lower left',fontsize=7.2)

    # Information ratio per electron: determinant (geometric area) is explicitly declared.
    for bv,col in [(0.4,C[0]),(.85,C[1]),(1.4,C[2])]:
        f0=fisher(bv,.7,blur=False)
        det0=max(np.linalg.det(f0),1e-30)
        ratio=[np.sqrt(max(np.linalg.det(fisher(bv,ss)),0)/det0) for ss in sigmas]
        f.plot(sigmas,ratio,c=col,label=rf'$B={bv:g}$')
    f.set(xlabel=r'$\sigma_E/(\hbar\omega)$',ylabel=r'$\mathcal{R}_F$',ylim=(0,1.03))
    f.legend(loc='lower left',fontsize=7.5)
    atlas_save(fig,OUT)
    print('saved',OUT,'F(ideal)',fisher(B,.7,blur=False),'F(det)',fisher(B,.7))
if __name__=='__main__':render()
