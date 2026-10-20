"""Phase-stepped PINEM: coherent coupling and exact spectral-moment demodulation.

All distributions and plotted results are generated from Bessel probabilities.
This is a controlled *same-frequency coherent reference* model; free drift,
frequency mismatch, finite optical phase diffusion and reference calibration
error are excluded from the forward model.
"""
import numpy as np
from scipy.special import jv
from common import atlas_figure,atlas_save,ATLAS_COLORS
from pathlib import Path
OUT=Path(__file__).with_suffix('.pdf')
PHASES=np.arange(4)*np.pi/2
X,Y=.67,.46
B=.85
N=np.arange(-15,16)
RNG_SEED=20261009
C=ATLAS_COLORS

def coupling(phi,b=B,x=X,y=Y):
    return x+1j*y+b*np.exp(1j*np.asarray(phi))

def populations(phi,b=B,x=X,y=Y):
    return jv(N,2*np.abs(coupling(phi,b,x,y)))**2

def moment(phi,b=B,x=X,y=Y):
    # Sideband moment identity: E[n^2]/2 = |beta_tot|^2.
    return np.abs(coupling(phi,b,x,y))**2

def demodulate(values,b=B):
    values=np.asarray(values)
    return np.array([(values[0]-values[2])/(4*b),
                     (values[1]-values[3])/(4*b)])

def simulate_moments(n_per_phase=1200,sigma=.7,repeats=1,seed=RNG_SEED,b=B,x=X,y=Y):
    rng=np.random.default_rng(seed)
    p=np.stack([populations(p,b,x,y) for p in PHASES])
    p/=p.sum(axis=1,keepdims=True)
    # sampled (continuous) measured energy E/(hbar omega) = n + Gaussian noise
    arr=np.empty((repeats,4))
    for j in range(4):
        samples=rng.choice(N,size=(repeats,n_per_phase),p=p[j]);
        measured=samples+sigma*rng.standard_normal(samples.shape)
        arr[:,j]=.5*np.mean(measured**2,axis=1)
    dem=np.stack([(arr[:,0]-arr[:,2])/(4*b),
                  (arr[:,1]-arr[:,3])/(4*b)],axis=1)
    return dem

def variance_y(betatot,sigma):
    g2=np.abs(betatot)**2
    return (g2+g2*g2+4*g2*sigma*sigma+sigma**4)/2


def render():
    fig,axs=atlas_figure()
    a,b,c,d,e,f=axs
    phi=np.linspace(0,2*np.pi,340)
    bet=coupling(phi)
    a.plot(bet.real,bet.imag,c=C[0],lw=1.65)
    a.scatter(coupling(PHASES).real,coupling(PHASES).imag,c=C[1],s=25,zorder=4)
    a.scatter([X],[Y],c=C[2],marker='x',s=45)
    a.axhline(0,color='.75',lw=.6);a.axvline(0,color='.75',lw=.6)
    a.set(xlabel=r'$\operatorname{Re}\beta_{\mathrm{tot}}$',ylabel=r'$\operatorname{Im}\beta_{\mathrm{tot}}$')
    a.set_aspect('equal',adjustable='datalim')

    for j,ph in enumerate(PHASES):
        b.plot(N,populations(ph),marker='o',ms=2.3,color=C[j],label=[r'$\phi_r=0$',r'$\phi_r=\pi/2$',r'$\phi_r=\pi$',r'$\phi_r=3\pi/2$'][j])
    b.set(xlim=(-8,8),xlabel=r'Electron order $n$',ylabel=r'$P_n$');b.legend(loc='upper right',fontsize=7.6)

    raw=moment(phi)
    c.plot(phi/np.pi,raw,c=C[0],lw=1.7)
    c.scatter(PHASES/np.pi,moment(PHASES),c=C[1],s=30,zorder=5)
    c.set(xlabel=r'$\phi_r/\pi$',ylabel=r'$\langle n^2\rangle/2$',xlim=(0,2))

    theta=np.linspace(-np.pi,np.pi,160)
    x_true=.8*np.cos(theta);y_true=.8*np.sin(theta)
    x_dem=[];y_dem=[]
    for xx,yy in zip(x_true,y_true):
        xs=demodulate(moment(PHASES,x=xx,y=yy))
        x_dem.append(xs[0]);y_dem.append(xs[1])
    d.plot(theta/np.pi,x_true,color=C[0],label=r'$\operatorname{Re}\beta$')
    d.plot(theta/np.pi,y_true,color=C[1],label=r'$\operatorname{Im}\beta$')
    d.scatter(theta[::14]/np.pi,np.asarray(x_dem)[::14],s=13,facecolors='none',edgecolors=C[0])
    d.scatter(theta[::14]/np.pi,np.asarray(y_dem)[::14],s=13,facecolors='none',edgecolors=C[1])
    d.set(xlabel=r'Signal phase $\arg\beta/\pi$',ylabel=r'Quadrature estimate',xlim=(-1,1));d.legend(loc='upper left',fontsize=7.6)

    for ss,col in [(.0,C[0]),(.7,C[1]),(1.3,C[2])]:
        e.plot(phi/np.pi,moment(phi)+ss**2/2, color=col, label=rf'$\sigma_E={ss:g}$')
    e.set(xlabel=r'$\phi_r/\pi$',ylabel=r'$\langle E^2\rangle/[2(\hbar\omega)^2]$',xlim=(0,2))
    e.legend(loc='upper right',fontsize=7.6)

    sizes=np.array([200,400,800,1600,3200])
    rms=[];expect=[]
    for size in sizes:
        out=simulate_moments(size,.7,180,seed=RNG_SEED+int(size))
        rms.append(np.sqrt(np.mean(np.sum((out-[X,Y])**2,axis=1))))
        v=sum(variance_y(coupling(PHASES[j]),.7) for j in range(4))
        expect.append(np.sqrt(v/(16*B*B*size)))
    f.plot(sizes,np.asarray(expect),color=C[0],label='Exact variance')
    f.scatter(sizes,rms,color=C[1],s=24,label='Monte Carlo')
    f.set(xscale='log',yscale='log',xlabel=r'Electrons per phase $M$',ylabel=r'Quadrature RMSE')
    f.legend(loc='upper right',fontsize=7.5)
    atlas_save(fig,OUT)
    print('saved',OUT,'moment-demod',demodulate(moment(PHASES)))
if __name__=='__main__':render()
