"""Order-resolved OAM phase-correlation information and detector-dose budget.

Every scientific panel is computed from the exact sector Fourier coefficients,
a column-stochastic OAM sorter, and the joint PINEM detection distribution.
No synthetic 3D height represents a new physical coordinate: in (a) it is the
absolute difference of two *complex angular correlation functions*.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.special import jv
from matplotlib import pyplot as plt
from preamble import pubfig, finish_pub, safe_colorbar, COLORS
from oam_higher_order_models import (
    MASK_A,MASK_B,angular_increment_correlation,order_overlap,
    normalized_oam,per_electron_exponent,error_probability_bound,
    total_variation)


def plot():
    mode=np.arange(-250,251)
    order=np.arange(1,9)
    overlap=np.array([order_overlap(MASK_A,MASK_B,int(n),mode,1.1) for n in order])
    fig=pubfig()
    gs=fig.add_gridspec(2,3,wspace=.60,hspace=.56)
    a=fig.add_subplot(gs[0,0],projection='3d')
    b,c,d,e,f=[fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]

    # (a) A true 3D plot of a computed observable: higher circular moments of
    # the phase increment, and their magnitude difference between hypotheses.
    deltas=np.linspace(0,np.pi,121)
    ns=np.arange(1,8)
    delta_c=np.array([np.abs(angular_increment_correlation(MASK_A,int(n),deltas,mode)-
                             angular_increment_correlation(MASK_B,int(n),deltas,mode)) for n in ns])
    xx,yy=np.meshgrid(deltas/np.pi,ns)
    a.plot_surface(xx,yy,delta_c,cmap='viridis',vmin=0.,vmax=1.65,
                   linewidth=0,antialiased=False,alpha=.96)
    a.set(xlabel=r'$\Delta/\pi$',ylabel='Order $n$',zlabel='',
          xlim=(0,1),ylim=(1,7),zlim=(0,1.7))
    a.set_yticks([1,2,4,6]);a.set_xticks([0,.5,1])
    a.set_box_aspect((1.5,1.2,.90),zoom=.86)
    a.text2D(.07,.96,r'$|C_n^A-C_n^B|$',transform=a.transAxes,fontsize=10)
    a.view_init(elev=26,azim=-58)

    # (b) Resolution changes the contrast, not the underlying analytic masks.
    nplot=np.arange(1,9)
    for fw,style,col,label in [(.0,'-',COLORS['blue'],'Ideal'),
                               (1.1,'--',COLORS['orange'],r'$1.1\hbar$'),
                               (2.3,':',COLORS['green'],r'$2.3\hbar$')]:
        curve=[]
        for n in nplot:
            A=normalized_oam(MASK_A,int(n),mode,None if fw==0 else fw)
            B=normalized_oam(MASK_B,int(n),mode,None if fw==0 else fw)
            curve.append(total_variation(A,B))
        b.plot(nplot,curve,style,marker='o',markersize=2.8,color=col,label=label)
    b.set(xlabel='Photon order $n$',ylabel='Total variation $D_n$',
          xlim=(.8,8.2),ylim=(-.04,1.02))
    b.set_xticks([1,2,3,4,5,6,7,8]);b.legend(loc='upper right',frameon=False)

    # (c) A one-photon response can have many counts and no information.
    amplitude=.8
    count=jv(nplot,2*amplitude)**2
    informative=count*(1-overlap)
    c.plot(nplot,count,'-o',color=COLORS['orange'],markersize=3,label=r'$P_n$')
    c.plot(nplot,informative,'-s',color=COLORS['blue'],markersize=3,
           label=r'$P_n(1-B_n)$')
    c.set(xlabel='Photon order $n$',ylabel='Per-electron weight',
          xlim=(.8,8.2),ylim=(-.01,.37))
    c.set_xticks([1,2,3,4,5,6,7,8]);c.legend(loc='upper right',frameon=False)

    # (d) The best order changes when a crosses a Bessel zero.
    amp=np.linspace(.22,3.3,116)
    b2=overlap[1];b6=overlap[5]
    r2=np.array([per_electron_exponent(x,[2],[b2]) for x in amp])
    r6=np.array([per_electron_exponent(x,[6],[b6]) for x in amp])
    rj=np.array([per_electron_exponent(x,[2,6],[b2,b6]) for x in amp])
    d.plot(amp,r2,color=COLORS['blue'],label=r'$\pm2$')
    d.plot(amp,r6,color=COLORS['orange'],label=r'$\pm6$')
    d.plot(amp,rj,'--',color=COLORS['green'],label='Joint')
    d.set(xlabel='Coupling $a$',ylabel='Exponent per electron',xlim=(amp[0],amp[-1]))
    d.legend(loc='upper left',frameon=False)

    # (e) Explicit joint budget of detector resolution and incident dose.
    fwhm=np.linspace(.0,3.0,27)
    contrasts=np.array([1-order_overlap(MASK_A,MASK_B,2,mode,None if fw==0 else fw) for fw in fwhm])
    ampl=np.linspace(.40,3.1,85)
    weighted=2*jv(2,2*ampl[None,:])**2*contrasts[:,None]
    rate=-np.log1p(-np.clip(weighted,0,.999999999))
    # N_1% is the dose needed to make the *bound* drop below one percent.
    dose=np.log(50)/np.maximum(rate,1e-12)
    image=e.imshow(np.log10(dose),origin='lower',interpolation='nearest',aspect='auto',
                   extent=[ampl[0],ampl[-1],fwhm[0],fwhm[-1]],
                   cmap='viridis',vmin=1,vmax=5.0)
    e.set(xlabel='Coupling $a$',ylabel=r'OAM FWHM / $\hbar$')
    safe_colorbar(fig,image,e,label='')

    # (f) The old single-coupling probability bounds had nearly the same
    # exponent and visually overlapped. Instead show the experimentally
    # actionable sufficient dose versus coupling, retaining the Bessel zeros.
    a_grid=np.linspace(.45,3.3,301)
    for sel,color,lin,label in [([2],COLORS['blue'],'-',r'$\pm2$'),
                                ([6],COLORS['orange'],'--',r'$\pm6$'),
                                ([2,6],COLORS['green'],':','Joint')]:
        rr=np.array([per_electron_exponent(x,sel,[overlap[n-1] for n in sel]) for x in a_grid])
        required=np.log(50)/np.maximum(rr,1e-16)
        valid=(required>=1)&(required<=1e5)
        f.semilogy(a_grid,np.where(valid,required,np.nan),lin,color=color,label=label)
    f.axhline(1e2,lw=.6,ls=':',color='.42')
    f.set(xlabel='Coupling $a$',ylabel=r'Sufficient dose $N_{1\%}$',
          xlim=(.45,3.3),ylim=(1,1e5))
    f.legend(loc='upper right',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))

if __name__=='__main__':
    plot()
