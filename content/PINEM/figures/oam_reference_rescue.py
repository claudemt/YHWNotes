"""OAM homometry with a coherent OAM-zero reference at a Bessel zero.

Six fully computed panels, one calibrated six-sector effective interaction.
All logarithmic distinguishability plots include the unselected/outside-detection
record, no conditional renormalization or postselection shortcut.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.special import jn_zeros
from matplotlib import pyplot as plt
from preamble import pubfig, finish_pub, COLORS
from oam_higher_order_models import MASK_A, MASK_B
from oam_reference_bridge_model import (
    gamma, observation, angular_amplitudes, sector_amplitudes,
    bhattacharyya, tv)

A0=float(jn_zeros(2,1)[0]/2)
MODES=np.arange(-12,13)
FW=1.1
EFF=.72


def rate(r,chi,a=A0,n=1):
    return gamma(MASK_A,MASK_B,a,r,chi,MODES,FW,EFF,n)


def plot():
    fig=pubfig()
    gs=fig.add_gridspec(2,3,wspace=.56,hspace=.53)
    ax=[fig.add_subplot(gs[0,0],projection='3d')]
    ax += [fig.add_subplot(gs[k//3,k%3]) for k in range(1,6)]
    a,b,c,d,e,f=ax
    # (a) A real observable in 3D: per-incident-electron Bhattacharyya exponent.
    rgrid=np.linspace(0,1.2,36)
    phigrid=np.linspace(-np.pi,np.pi,61)
    surf=np.array([[rate(rr,ph) for rr in rgrid] for ph in phigrid])
    RR,PP=np.meshgrid(rgrid,phigrid/np.pi)
    a.plot_surface(RR,PP,surf,cmap='viridis',linewidth=0,antialiased=False,alpha=.98)
    a.set(xlabel=r'$r$',ylabel=r'$\chi/\pi$',zlabel='',zlim=(0,max(.001,surf.max()*1.07)))
    a.set_xticks([0,.4,.8,1.2]);a.set_yticks([-1,0,1])
    a.set_box_aspect((1.3,1.30,.9),zoom=.85)
    a.view_init(elev=27,azim=-54)
    # (b) With no reference the first sideband is homometric; with one, not.
    chi_opt=phigrid[np.argmax([rate(.8,x) for x in phigrid])]
    ms=np.arange(-9,10)
    pnone=np.abs(angular_amplitudes(MASK_A,A0,0,0,ms,n=1))**2
    pa=np.abs(angular_amplitudes(MASK_A,A0,.8,chi_opt,ms,n=1))**2
    pb=np.abs(angular_amplitudes(MASK_B,A0,.8,chi_opt,ms,n=1))**2
    b.plot(ms,pnone,':',color='.5',label=r'$r=0$: A=B')
    b.plot(ms,pa,'-o',ms=2.3,color=COLORS['blue'],label='A')
    b.plot(ms,pb,'--s',ms=2.1,color=COLORS['orange'],label='B')
    b.set(xlabel='OAM $M$',ylabel=r'$P_{1M}$',xlim=(-9,9))
    b.set_xticks([-8,-4,0,4,8]);b.legend(loc='upper right',frameon=False)
    # (c) Even energy-only *with the reference* can become informative.
    phis=np.linspace(-np.pi,np.pi,111)
    for mask,color,label in [(MASK_A,COLORS['blue'],'A'),(MASK_B,COLORS['orange'],'B')]:
        prob=np.array([np.mean(np.abs(sector_amplitudes(mask,A0,.8,x,n=1))**2) for x in phis])
        c.plot(phis/np.pi,prob,color=color,label=label)
    c.axvline(chi_opt/np.pi,ls=':',lw=.8,color='.5')
    c.set(xlabel=r'Reference phase $\chi/\pi$',ylabel=r'$P_{n=1}$',xlim=(-1,1))
    c.legend(loc='upper right',frameon=False)
    # (d) One-photon reference-assisted exponent versus reference strength.
    rs=np.linspace(0,1.22,55)
    ga_opt=np.array([max(rate(rr,ph) for ph in np.linspace(-np.pi,np.pi,31)) for rr in rs])
    ga_fixed=np.array([rate(rr,np.pi) for rr in rs])
    ga2=rate(0,0,n=2)
    d.plot(rs,ga_opt,color=COLORS['blue'],label='Phase optimized')
    d.plot(rs,ga_fixed,'--',color=COLORS['orange'],label=r'$\chi=\pi$')
    d.axhline(max(ga2,0),ls=':',color=COLORS['green'],label='No ref., $n=2$')
    d.set(xlabel='Reference strength $r$',ylabel=r'Per-electron $\Gamma$',xlim=(0,1.22))
    d.legend(loc='upper left',frameon=False)
    # (e) The rescue only applies in part of the coupling-reference parameter plane.
    avec=np.linspace(1.78,3.0,73);rvec=np.linspace(0,1.18,49)
    rates=np.array([[rate(r,np.pi,a=aa) for aa in avec] for r in rvec])
    im=e.imshow(rates,origin='lower',aspect='auto',interpolation='nearest',cmap='viridis',
                extent=[avec[0],avec[-1],rvec[0],rvec[-1]])
    e.axvline(A0,ls='--',lw=.8,color='white')
    e.set(xlabel='Sample coupling $a$',ylabel='Reference strength $r$')
    # The common six-panel template reserves a slim colorbar gutter.
    from preamble import safe_colorbar
    safe_colorbar(fig,im,e,label='')
    # (f) Conditional spectra are not doses: the 'other' event is counted.
    nn=np.arange(0,850)
    configurations=[(0.,'No reference',':','.4'),(.4,r'$r=0.4$','--',COLORS['orange']),
                    (.8,r'$r=0.8$','-',COLORS['blue'])]
    for rr,label,style,color in configurations:
        gsrate=max(rate(rr,ph) for ph in phigrid)
        f.semilogy(nn,.5*np.exp(-nn*gsrate),ls=style,color=color,label=label)
    f.axhline(.01,ls=':',color='.55',lw=.8)
    f.set(xlabel=r'Incident electrons $N_{\mathrm{e}}$',ylabel='',
          xlim=(0,850),ylim=(.0004,.65))
    f.legend(loc='upper right',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))
    print('A0',A0,'chi_opt',chi_opt,'gamma_ref',rate(.8,chi_opt),'gamma_no_ref2',ga2,
          'dose_1pct',int(np.ceil(np.log(50)/rate(.8,chi_opt))))

if __name__=='__main__':
    plot()
