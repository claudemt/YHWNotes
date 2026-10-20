"""Six-model-panel figure: phase-noise nullspace of the (1,1,-1) PINEM loop."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from preamble import pubfig,finish_pub,COLORS,safe_colorbar,style_3d
from relation_noise_geometry_model import (
    phase_signal,signal_at,averaged_coefficients,independent_covariance,
    locked_covariance,closed_relation_variance,relation_variance,fisher_binary,
    TAU,U)

BLUE=COLORS['blue']; ORANGE=COLORS['orange']; GREEN=COLORS['green']; PURPLE=COLORS['purple']


def plot():
    fig=pubfig()
    gs=fig.add_gridspec(2,3,wspace=.57,hspace=.58)
    ax=[fig.add_subplot(gs[0,0],projection='3d')]
    ax += [fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]
    a,b,c,d,e,f=ax
    phi,exact,coef=phase_signal(512)
    # (a) A phase-noise *plane* in parameter space, not in electron configuration space.
    xx=np.linspace(-1.05,1.05,15); yy=np.linspace(-1.05,1.05,15)
    X,Y=np.meshgrid(xx,yy); Z=X+Y
    a.plot_surface(X,Y,Z,color=BLUE,alpha=.18,linewidth=0,shade=False)
    a.plot([-1,1],[0,0],[-1,1],lw=1.2,color=BLUE,alpha=.6)
    rng=np.random.default_rng(101)
    uv=rng.uniform(-.85,.85,(26,2))
    zz=uv[:,0]+uv[:,1]+rng.normal(0,.08,len(uv))
    a.scatter(uv[:,0],uv[:,1],zz,color=GREEN,s=10,alpha=.92,depthshade=False)
    for coord in [0.25,-0.6]:
        point=np.array([coord,0.,coord])
        a.plot([point[0],point[0]+U[0]*.28],[point[1],point[1]+U[1]*.28],
               [point[2],point[2]+U[2]*.28],color=ORANGE,lw=1.6)
    a.view_init(elev=26,azim=-53)
    a.set_xlim(-1.1,1.1);a.set_ylim(-1.1,1.1);a.set_zlim(-2.1,2.1)
    a.set_xticks([-1,0,1]);a.set_yticks([-1,0,1]);a.set_zticks([-2,0,2])
    a.set_xlabel(r'$\delta\theta_1$',labelpad=0)
    a.set_ylabel(r'$\delta\theta_2$',labelpad=0)
    a.set_zlabel(r'$\delta\theta_3$',labelpad=0)
    a.set_box_aspect((1,1,.98),zoom=.84)
    # (b) Exact finite-time output has higher Fourier harmonics beyond weak coupling.
    b.plot(phi/np.pi,exact,color=BLUE,label='Exact unitary')
    m=np.fft.fftfreq(len(coef),d=1/len(coef))
    c1=coef.copy();c1[np.abs(m)>1]=0
    c2=coef.copy();c2[np.abs(m)>2]=0
    b.plot(phi/np.pi,signal_at(phi,c1),ls='--',color=ORANGE,label=r'$|h|\leq1$')
    b.plot(phi/np.pi,signal_at(phi,c2),ls=':',color=GREEN,label=r'$|h|\leq2$')
    b.set(xlabel=r'Relation phase $\Phi/\pi$',ylabel=r'$P_f$',xlim=(0,2),ylim=(0,1))
    b.legend(loc='upper right',frameon=False)
    # (c) Gaussian averaging protects correlated/phase-locked noise.
    ss=.8;eps=.12
    v_ind=relation_variance(independent_covariance(ss))
    v_lock=relation_variance(locked_covariance(ss,1.,eps))
    c.plot(phi/np.pi,exact,color=BLUE,label='No noise')
    c.plot(phi/np.pi,signal_at(phi,coef,v_ind),color=ORANGE,label='Independent')
    c.plot(phi/np.pi,signal_at(phi,coef,v_lock),color=GREEN,ls='--',label='Phase locked')
    c.set(xlabel=r'Relation phase $\Phi/\pi$',ylabel=r'$\overline{P}_f$',xlim=(0,2),ylim=(0,1))
    c.legend(loc='upper right',frameon=False)
    # (d) Exact Fourier-harmonic factor exp(-h^2 V/2), no weak-coupling assumption.
    orders=np.arange(1,5)
    for v,col,lab,st in [(0.,BLUE,'No noise','-'),(v_lock,GREEN,'Phase locked','--'),
                         (v_ind,ORANGE,'Independent',':')]:
        cc=averaged_coefficients(coef,v)
        d.semilogy(orders,np.abs(cc[orders]),color=col,ls=st,marker='o',ms=3,label=lab)
    d.set(xlabel=r'Relation-harmonic index $h$',ylabel=r'$|c_h|$',xlim=(.8,4.2),ylim=(1e-9,.4))
    d.set_xticks([1,2,3,4]);d.legend(loc='lower left',frameon=False)
    # (e) A 2D geometry map of phase-locking mismatch.
    sigmas=np.linspace(.0,2.2,91);lams=np.linspace(0,1.4,85)
    LL,SS=np.meshgrid(lams,sigmas)
    attenuation=np.exp(-.5*(2*(1-LL)**2*SS**2+eps**2))
    im=e.imshow(attenuation,origin='lower',aspect='auto',extent=[lams[0],lams[-1],sigmas[0],sigmas[-1]],
                cmap='viridis',vmin=0,vmax=1,interpolation='bilinear')
    e.axvline(1.,color='white',ls='--',lw=.9)
    e.set(xlabel=r'Locking coefficient $\lambda$',ylabel=r'Single-drive noise $\sigma$')
    safe_colorbar(fig,im,e)
    # (f) Per-incident-electron binary FI for loop phase: noise affects derivative.
    bias=np.linspace(0,2*np.pi,128,endpoint=False)
    best=bias[np.argmax([fisher_binary(p,coef,0) for p in bias])]
    noise=np.linspace(0,1.7,70)
    ref=fisher_binary(best,coef,0)
    for lam,col,lab,style in [(0.,ORANGE,r'$\lambda=0$','-'),(.65,PURPLE,r'$\lambda=0.65$','--'),
                              (1.,GREEN,r'$\lambda=1$','-')]:
        eff=np.array([fisher_binary(best,coef,closed_relation_variance(s,lam,eps))/ref for s in noise])
        f.plot(noise,eff,color=col,ls=style,label=lab)
    f.set(xlabel=r'Noise $\sigma$',ylabel=r'$F_{\Phi\Phi}/F_{\Phi\Phi}^{(0)}$',xlim=(0,1.7),ylim=(0,1.05))
    f.legend(loc='lower left',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))
    print('max_harmonics',abs(coef[1]),abs(coef[2]),'protected_variance',v_lock,
          'uncorrelated_variance',v_ind,'FI_bias',best,'FI_clean',ref)

if __name__=='__main__':
    plot()
