"""Order-resolved angular homometry under independent vs common sector noise."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from matplotlib import pyplot as plt
from preamble import pubfig,finish_pub,COLORS,safe_colorbar
from oam_sector_noise_model import (MODES,MASK_A,MASK_B,sector_ensemble,
    detected_mode_weights,conditional_tv,incident_rate,FW,EFF,WINDOW)
from oam_higher_order_models import angular_increment_correlation

BLUE=COLORS['blue'];ORANGE=COLORS['orange'];GREEN=COLORS['green'];PURPLE=COLORS['purple']


def plot():
    fig=pubfig();gs=fig.add_gridspec(2,3,wspace=.57,hspace=.53)
    ax=[fig.add_subplot(gs[0,0],projection='3d')]
    ax += [fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]
    a,b,c,d,e,f=ax
    # (a) Observable three-dimensional contrast: C_2(Delta) spectral autocorrelation.
    ds=np.linspace(0,np.pi,50);sig=np.linspace(0,.75,29)
    m=MODES
    d0=sector_ensemble(MASK_A,2,m,0)-sector_ensemble(MASK_B,2,m,0)
    di=np.sinc(m/6.)**2/6
    # Common incoherent contribution cancels from A-B; jitter attenuates contrast.
    original=np.abs(np.exp(1j*np.outer(ds,m))@d0)
    ZZ=np.exp(-4*sig[:,None]**2)*original[None,:]
    D,S=np.meshgrid(ds/np.pi,sig)
    a.plot_surface(D,S,ZZ,cmap='viridis',linewidth=0,alpha=.96,rstride=1,cstride=1,
                   antialiased=False)
    a.view_init(elev=25,azim=-55)
    a.set(xlabel=r'$\Delta/\pi$',ylabel=r'$\sigma$',zlabel='')
    a.set_zlim(0,max(.01,ZZ.max()*1.05));a.set_yticks([0,.35,.7])
    a.set_box_aspect((1.27,1.1,.85),zoom=.82)
    # (b,c) actual detector-resolved OAM spectra, normalized conditional on detection.
    ms=MODES[np.abs(MODES)<=WINDOW]
    for axis,sigma in [(b,0.),(c,.55)]:
        for mask,col,label,sty in [(MASK_A,BLUE,'A','-'),(MASK_B,ORANGE,'B','--')]:
            y=detected_mode_weights(mask,2,sigma,0.)
            y=y/y.sum()
            axis.plot(ms,y,color=col,ls=sty,marker='o',ms=2.1,label=label)
        axis.set(xlabel=r'OAM index $M$',ylabel=r'$P(M\mid n=2)$',xlim=(-10,10))
        axis.set_xticks([-10,-5,0,5,10]);axis.legend(loc='upper right',frameon=False)
    # (d) observable D_n, shared global noise does not alter any mode probability.
    orders=np.arange(1,8)
    for sg,col,label,sty in [(0.,BLUE,'Ideal','-'),(.25,GREEN,r'$\sigma=0.25$','--'),
                             (.55,ORANGE,r'$\sigma=0.55$',':')]:
        vals=np.array([conditional_tv(int(n),sg,0) for n in orders])
        d.plot(orders,vals,marker='o',ms=3,color=col,ls=sty,label=label)
    d.set(xlabel=r'Photon order $n$',ylabel=r'OAM distance $D_n$',xlim=(.8,7.2),ylim=(0,1))
    d.legend(loc='upper left',frameon=False)
    # (e) information ladder under jitter: original n=2,6 harmonics survive at sigma=0.
    nvec=np.arange(1,9);svec=np.linspace(0,.8,56)
    dist=np.array([[conditional_tv(int(n),ss,0) for n in nvec] for ss in svec])
    im=e.imshow(dist,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1,
                extent=[.5,8.5,svec[0],svec[-1]],interpolation='nearest')
    e.set(xlabel=r'Photon order $n$',ylabel=r'Sector noise $\sigma$')
    e.set_xticks([1,2,3,4,5,6,7,8])
    safe_colorbar(fig,im,e)
    # (f) End-to-end incident-electron sufficient dose for 1% Bhattacharyya bound.
    ss=np.linspace(0,.8,55);a0=.8
    for rho,col,label,sty in [(0.,ORANGE,'Independent','-'),(.7,PURPLE,r'$\rho=0.7$','--'),
                              (1.,GREEN,'Common-mode','-')]:
        rate=np.array([incident_rate(2,a0,x,rho) for x in ss])
        sufficient=np.log(50.)/np.maximum(rate,1e-15)
        f.semilogy(ss,sufficient,color=col,ls=sty,label=label)
    f.set(xlabel=r'Sector noise $\sigma$',ylabel=r'Sufficient electrons $N_{\mathrm{e}}$',xlim=(0,.8))
    f.legend(loc='upper left',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))
    print('D2 ideal/jitter',conditional_tv(2,0,0),conditional_tv(2,.55,0),'Dose ideal',
          np.log(50)/incident_rate(2,.8,0,0))
if __name__=='__main__':plot()
