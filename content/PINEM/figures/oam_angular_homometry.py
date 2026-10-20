"""Phase-only PINEM angular homometry: one actual 3D phase surface plus five spectra.
Reproduces a source manuscript's exact six-sector construction, not its figures.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.special import jv
from preamble import pubfig, finish_pub
from oam_higher_order_models import (MASK_A, MASK_B, MASK_C, MASK_D,
    normalized_oam, total_variation, conditional_oam)

BLUE='#2677a8'; ORANGE='#c77641'; GREEN='#258676'

def plot():
    fig=pubfig()
    gs=fig.add_gridspec(2,3,wspace=.52,hspace=.54)
    axs=[fig.add_subplot(gs[0,0],projection='3d')]+[
        fig.add_subplot(gs[k//3,k%3]) for k in range(1,6)]
    a,b,c,d,e,f=axs
    # (a) Height + cyclic color both encode actual piecewise angular phase.
    angles=np.linspace(0,2*np.pi,241)
    rr=np.linspace(.53,1.05,12)
    tt,r=np.meshgrid(angles,rr)
    for shift,mask in [(-1.25,MASK_A),(1.25,MASK_B)]:
        ind=(np.floor((tt%(2*np.pi-1e-12))/(2*np.pi/6))).astype(int)%6
        chi=np.angle(mask[ind]);z=0.62*chi/np.pi
        X=shift+r*np.cos(tt);Y=r*np.sin(tt)
        fc=cm.twilight((chi+np.pi)/(2*np.pi))
        a.plot_surface(X,Y,z,facecolors=fc,linewidth=0,antialiased=False,
                       rstride=1,cstride=1,shade=False)
        a.plot(shift+1.08*np.cos(angles),1.08*np.sin(angles),-.78+angles*0,color='.65',lw=.48,alpha=.6)
    a.set(xlim=(-2.4,2.4),ylim=(-1.2,1.2),zlim=(-.9,.9))
    a.set_box_aspect((3.0,1.65,1.0), zoom=1.20)
    a.view_init(elev=27,azim=-61)
    a.set_axis_off()
    a.text2D(.20,.14,'A',transform=a.transAxes,fontsize=10,ha='center')
    a.text2D(.75,.14,'B',transform=a.transAxes,fontsize=10,ha='center')
    a.text2D(.20,.97,r'$\arg s(\varphi)$',transform=a.transAxes,fontsize=9,ha='center')
    # (b) Exactly identical energy-only population.
    ns=np.arange(-5,6);p=jv(ns,1.6)**2
    b.plot(ns,p,'o-',ms=3,color=BLUE,label='A')
    b.plot(ns,p,'s',ms=3.2,markerfacecolor='none',color=ORANGE,label='B')
    b.set(xlabel='Photon order $n$',ylabel='$P_n$',xlim=(-5.5,5.5),ylim=(0,.53))
    b.legend(loc='upper right',frameon=False,ncol=2)
    # (c,d) Detector blur: 1.1 hbar FWHM, conditional mode collection.
    modes=np.arange(-250,251)
    for ax,n in [(c,1),(d,2)]:
        pa=normalized_oam(MASK_A,n,modes,fwhm=1.1)
        pb=normalized_oam(MASK_B,n,modes,fwhm=1.1)
        sel=(abs(modes)<=9)
        ax.plot(modes[sel],pa[sel],'-o',ms=2.7,color=BLUE,label='A')
        ax.plot(modes[sel],pb[sel],'--s',ms=2.5,color=ORANGE,label='B')
        ax.set(xlabel='OAM $M$',ylabel=rf'$P(M\mid n={n})$',xlim=(-9,9))
        ax.set_xticks([-8,-4,0,4,8])
        ax.legend(loc='upper right',frameon=False,ncol=2)
    # (e) Two distinct exact homometry classes: onset at order two versus three.
    MM=np.arange(-10,11)
    contrasts=[]
    for left,right,n in [(MASK_A,MASK_B,1),(MASK_A,MASK_B,2),
                         (MASK_C,MASK_D,2),(MASK_C,MASK_D,3)]:
        pa=normalized_oam(left,n,modes,1.1)
        pb=normalized_oam(right,n,modes,1.1)
        contrasts.append((pb-pa)[np.isin(modes,MM)])
    contrast=np.array(contrasts)
    e.imshow(contrast,origin='lower',aspect='auto',extent=[-10.5,10.5,.5,4.5],
             cmap='RdBu_r',vmin=-.8,vmax=.8,interpolation='nearest')
    e.set(xlabel='OAM $M$',ylabel='Mask and order')
    e.set_xticks([-10,-5,0,5,10]);e.set_yticks([1,2,3,4])
    e.set_yticklabels(['A/B: 1','A/B: 2','C/D: 2','C/D: 3'])
    # (f) Novel interpretation: compare two exact hierarchy classes and finite signal weight.
    nseq=np.arange(1,6)
    Dab=[];Dcd=[]
    for n in nseq:
        Dab.append(total_variation(normalized_oam(MASK_A,n,modes,1.1),normalized_oam(MASK_B,n,modes,1.1)))
        Dcd.append(total_variation(normalized_oam(MASK_C,n,modes,1.1),normalized_oam(MASK_D,n,modes,1.1)))
    f.plot(nseq,Dab,'-o',color=BLUE,label='A/B distance')
    f.plot(nseq,Dcd,'--s',color=ORANGE,label='C/D distance')
    f.plot(nseq,jv(nseq,1.6)**2,':^',color=GREEN,label='$P_n$')
    f.set(xlabel='Photon order $n$',ylabel='Distance / probability',xlim=(.8,5.2),ylim=(-.035,1.05))
    f.set_xticks(nseq)
    f.legend(loc='upper right',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))

if __name__=='__main__':
    plot()
