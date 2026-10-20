"""Six computed panels: reconstruct observable relation-phase covariance."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,finish_pub,safe_colorbar,COLORS,style_3d
from oam_relation_covariance_model import (G_TRUE,U,covariance_from_projection,coeffs,
    probability,reconstruct_G,trial_estimates)
BLUE=COLORS['blue']; ORANGE=COLORS['orange'];GREEN=COLORS['green'];PURPLE=COLORS['purple']

def plot():
    fig=pubfig();gs=fig.add_gridspec(2,3,wspace=.63,hspace=.64)
    ax=[fig.add_subplot(gs[0,0],projection='3d')]
    ax += [fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]
    a,b,c,d,e,f=ax
    # a: a genuine 3D phase-torus probability landscape, no fictitious coordinate.
    ang=np.linspace(0,2*np.pi,74); X,Y=np.meshgrid(ang,ang,indexing='ij')
    PP=probability(X,Y)
    a.plot_surface(X/np.pi,Y/np.pi,PP,cmap='viridis',rstride=2,cstride=2,alpha=.95,linewidth=0)
    a.set(xlabel=r'$\Phi_u/\pi$',ylabel=r'$\Phi_v/\pi$',zlabel=r'$P_x$')
    a.set_xticks([0,1,2]);a.set_yticks([0,1,2])
    a.set_box_aspect((1,1,.62),zoom=.84);style_3d(a,27,-62)
    # b: recorded average after Gaussian phase jitter, exactly averaged Fourier series.
    blurred=probability(X,Y,G_TRUE)
    im=b.imshow(blurred.T,origin='lower',extent=[0,2,0,2],vmin=0,vmax=.65,
                aspect='auto',cmap='viridis',interpolation='bilinear')
    b.set(xlabel=r'$\Phi_u/\pi$',ylabel=r'$\Phi_v/\pi$')
    safe_colorbar(fig,im,b)
    # c: scan one phase at fixed value of other phase.
    ph=np.linspace(0,2*np.pi,240)
    for G,col,lab,st in [(None,BLUE,'Coherent','-'),(G_TRUE,ORANGE,'Gaussian noise','--')]:
        c.plot(ph/np.pi,probability(ph,0.,G),color=col,ls=st,label=lab)
    c.set(xlabel=r'$\Phi_u/\pi$',ylabel=r'$P_x(\Phi_v=0)$',xlim=(0,2),ylim=(0,.67))
    c.legend(frameon=False,loc='upper right')
    # d: exact measurable amplitudes and predicted Gaussian attenuations.
    ks=[(1,0),(0,1),(1,1),(1,-1)];xx=np.arange(4)
    predicted=[np.exp(-.5*np.array(k)@G_TRUE@np.array(k)) for k in ks]
    from oam_relation_covariance_model import estimate_fourier
    rng=np.random.default_rng(317)
    grid=24; phase=2*np.pi*np.arange(grid)/grid
    xgrid,ygrid=np.meshgrid(phase,phase,indexing='ij')
    pgrid=probability(xgrid,ygrid,G_TRUE)
    empirical=[]
    for _ in range(150):
        sampled=rng.binomial(250,pgrid)
        fcoef=estimate_fourier(sampled,250)
        empirical.append([abs(fcoef[k]/coeffs()[k]) for k in ks])
    empirical=np.array(empirical)
    d.bar(xx,predicted,width=.45,color=BLUE,alpha=.78,label='Theory')
    d.errorbar(xx+.18,np.mean(empirical,axis=0),yerr=np.std(empirical,axis=0),fmt='o',
               color=ORANGE,capsize=2.5,ms=3.5,label='Finite counts')
    d.set_xticks(xx,[r'$u$',r'$v$',r'$u+v$',r'$u-v$'])
    d.set(xlabel='Relation harmonic',ylabel=r'$|c_m/c_m^{(0)}|$',ylim=(0,1.15))
    d.legend(frameon=False,loc='lower left')
    # e: calibrated Fourier-based recovery with finite binomial data.
    est=trial_estimates(600,trials=160,seed=2410)
    keys=[(0,0),(1,1),(0,1)];vtrue=[G_TRUE[i,j] for i,j in keys]
    vals=np.array([[g[i,j] for i,j in keys] for g in est]); avg=np.mean(vals,axis=0);std=vals.std(axis=0)
    e.bar(xx[:3]-.2,vtrue,width=.38,color=GREEN,label='True projection')
    e.errorbar(xx[:3]+.2,avg,yerr=std,fmt='o',color=PURPLE,capsize=3,label='Reconstructed')
    e.set_xticks(xx[:3],[r'$G_{11}$',r'$G_{22}$',r'$G_{12}$'])
    e.set(ylabel=r'Covariance (rad$^2$)',ylim=(-.08,.5))
    e.legend(loc='upper right',frameon=False)
    # f: strongly fluctuating absolute optical phases can be completely invisible.
    blind=np.linspace(0,2.5,100)
    sigma=np.array([covariance_from_projection(G_TRUE,t) for t in blind])
    for k,col in [(0,BLUE),(1,ORANGE),(2,PURPLE)]:
        f.plot(blind,np.sqrt(np.maximum(sigma[:,k,k],0)),color=col,label=rf'$\sigma_{{\theta_{k+1}}}$')
    f.plot(blind,[np.sqrt(U[:,0]@S@U[:,0]) for S in sigma],color=GREEN,ls='--',label=r'$\sigma_{\Phi_u}$')
    f.set(xlabel='Blind-noise amplitude',ylabel=r'Phase rms (rad)',xlim=(0,2.5),ylim=(0,2.6))
    f.legend(frameon=False,loc='upper left')
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))
    print('model attenuation',predicted,'G estimates',avg,std)
if __name__=='__main__':plot()
