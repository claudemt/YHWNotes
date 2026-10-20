"""Exact two-path pure-dephasing quantum eraser with coherent-state environment.
All six panels derive from controlled oscillator displacements, no fitted rates.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
from preamble import pubfig, safe_panel, safe_colorbar, clean, finish_pub


def overlap(delta):
    return np.exp(-np.asarray(delta,dtype=float)**2/2)


def entropy(delta):
    d=overlap(delta)
    pp=(1+d)/2; pm=(1-d)/2
    return -(np.where(pp>0,pp*np.log2(np.maximum(pp,1e-300)),0)
             +np.where(pm>0,pm*np.log2(np.maximum(pm,1e-300)),0))


def helstrom_error(delta):
    d=overlap(delta)
    return (1-np.sqrt(1-d*d))/2


def make_figure():
    out=Path(__file__).with_suffix('.pdf')
    fig=pubfig(9.2,6.12,top=.91,bottom=.1,left=.085,right=.965)
    gs=fig.add_gridspec(2,3,wspace=.61,hspace=.49)
    ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
    # (a) environment Husimi distributions for two path-conditioned coherent states
    d0=2.0
    v=np.linspace(-2.8,2.8,201)
    X,Y=np.meshgrid(v,v)
    QA=np.exp(-((X-d0/2)**2+Y**2))/np.pi
    QB=np.exp(-((X+d0/2)**2+Y**2))/np.pi
    img=ax[0].contourf(X,Y,(QA+QB)/2,levels=25,cmap='magma')
    ax[0].contour(X,Y,QA,levels=[.1,.2],colors=['#89d0d5'],linewidths=.9)
    ax[0].contour(X,Y,QB,levels=[.1,.2],colors=['#bbddb9'],linewidths=.9)
    ax[0].scatter([-d0/2,d0/2],[0,0],s=18,c=['#bbddb9','#89d0d5'],edgecolor='k',linewidth=.4)
    ax[0].set(xlabel=r'$\operatorname{Re}\zeta$',ylabel=r'$\operatorname{Im}\zeta$',aspect='equal')
    safe_colorbar(fig,img,ax[0],r'$Q(\zeta)$')
    # (b) overlap of the environment states versus separation
    delta=np.linspace(0,3.5,260)
    d=overlap(delta)
    ax[1].plot(delta,d,lw=1.6)
    ax[1].set(xlabel=r'Pointer separation $|\Delta\alpha|$',ylabel=r'$|\langle\alpha_B|\alpha_A\rangle|$')
    # (c) unconditioned electron fringes across three pointer separations
    phi=np.linspace(-np.pi,np.pi,360)
    for dd in [0,.8,1.6,2.4]:
        ax[2].plot(phi,(1+overlap(dd)*np.cos(phi))/2,label=rf'$|\Delta\alpha|={dd:g}$')
    ax[2].set(xlabel=r'Electron phase $\phi$',ylabel='Output probability')
    ax[2].legend(frameon=False,fontsize=7,loc='upper right',ncol=2)
    # (d) entanglement entropy and purity (pure system+environment)
    ax[3].plot(delta,entropy(delta),label='Entropy [bits]')
    ax[3].plot(delta,(1+d*d)/2,label='Electron purity')
    ax[3].set(xlabel=r'Pointer separation $|\Delta\alpha|$',ylabel='Information measure',ylim=(0,1.025))
    ax[3].legend(frameon=False,fontsize=7,loc='lower right')
    # (e) optimal which-path discrimination from Helstrom theorem
    D=np.sqrt(1-d*d)
    ax[4].plot(delta,D,label='Trace distance')
    ax[4].plot(delta,helstrom_error(delta),label='Minimum error')
    ax[4].set(xlabel=r'Pointer separation $|\Delta\alpha|$',ylabel='Which-path information')
    ax[4].legend(frameon=False,fontsize=7,loc='lower right')
    # (f) conditional quantum eraser: complementary unit-visibility outcomes
    erase_d=1.8
    ax[5].plot(phi,(1+overlap(erase_d)*np.cos(phi))/2,'k--',label='Unconditioned')
    ax[5].plot(phi,(1+np.cos(phi))/2,label='Eraser: +')
    ax[5].plot(phi,(1-np.cos(phi))/2,label='Eraser: -')
    ax[5].set(xlabel=r'Electron phase $\phi$',ylabel='Output probability')
    # Line meaning is fully stated in the caption; no obscuring legend over the fringes.
    for i,a in enumerate(ax):
        safe_panel(a,chr(ord('a')+i))
        clean(a)
    finish_pub(fig,out)
    return out

if __name__=='__main__':
    print(make_figure())
