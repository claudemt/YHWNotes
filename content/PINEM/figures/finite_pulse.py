from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pubfig, clean, safe_panel, finish_pub

fig, axs = plt.subplots(2,3,figsize=(10.6,7.9),constrained_layout=True)
axs=axs.ravel()
from scipy.special import jv
T=np.linspace(-4,4,600); ratios=[.35,.7,1.4,2.8]; beta0=2.8
axs[0].plot(T,beta0*np.exp(-T*T/2),lw=2,label=r'$|\beta(t)|$')
for r in ratios:
 w=np.exp(-T*T/(2*r*r)); w/=np.trapezoid(w,T); axs[0].plot(T,beta0*w/w.max(),ls='--',alpha=.7,label=fr'$w_e,\;r={r:g}$')
axs[0].legend(fontsize=7,ncol=2,frameon=False)
axs[0].set_xlabel('$t/\\tau_L$'); axs[0].set_ylabel('$|\\beta(t)|$')
ns=np.arange(-8,9)
for r in ratios:
 w=np.exp(-T*T/(2*r*r)); w/=np.trapezoid(w,T); bt=beta0*np.exp(-T*T/2); P=np.array([np.trapezoid(w*jv(n,2*bt)**2,T) for n in ns]); axs[1].plot(ns,P,'o-',label=f'{r}')
axs[1].set_xlabel('$n$'); axs[1].set_ylabel('$\\bar P_n$'); axs[1].legend(title='$\\tau_e/\\tau_L$')
R=np.linspace(.15,3,90); B=np.linspace(.2,4,100)
# Reuse the same forward kernel and quadrature weights for all 9000 cells.
# This is a mathematically identical trapezoidal integration, not an interpolation.
dt=T[1]-T[0]
trap_weights=np.full_like(T,dt); trap_weights[0]*=.5;trap_weights[-1]*=.5
weights=np.exp(-T[None,:]**2/(2*R[:,None]**2))
weights/=np.sum(weights*trap_weights,axis=1,keepdims=True)
J2=jv(ns[:,None,None],2*np.exp(-T[None,:,None]**2/2)*B[None,None,:])**2
Pgrid=np.einsum('rt,ntb,t->rnb',weights,J2,trap_weights,optimize=True)
Pgrid/=Pgrid.sum(axis=1,keepdims=True)
entropy=-np.sum(Pgrid*np.log(Pgrid+1e-14),axis=1)
im=axs[2].imshow(entropy,origin='lower',aspect='auto',extent=[B[0],B[-1],R[0],R[-1]]); axs[2].set_xlabel('$|\\beta_0|$'); axs[2].set_ylabel('$\\tau_e/\\tau_L$'); fig.colorbar(im,ax=axs[2],label='spectral entropy')
axs[3].plot(B,entropy[np.argmin(abs(R-.35))],label='short electron'); axs[3].plot(B,entropy[np.argmin(abs(R-2.8))],label='long electron'); axs[3].set_xlabel('$|\\beta_0|$'); axs[3].set_ylabel('entropy'); axs[3].legend()
# Finite-pulse width: two independent predictions beyond the original four panels.
RR=np.linspace(.18,3.2,64); rms=[]; p0=[]
for rr in RR:
    ww=np.exp(-T*T/(2*rr*rr)); ww/=np.trapezoid(ww,T)
    bt=beta0*np.exp(-T*T/2)
    pp=np.array([np.trapezoid(ww*jv(int(nn),2*bt)**2,T) for nn in ns]); pp/=pp.sum()
    rms.append(np.sqrt(np.dot(ns**2,pp))); p0.append(pp[len(ns)//2])
axs[4].plot(RR,rms); axs[4].set(xlabel=r'$\tau_e/\tau_L$',ylabel=r'$\sqrt{\langle n^2\rangle}$',title='Measured spectral width')
axs[5].plot(RR,p0); axs[5].set(xlabel=r'$\tau_e/\tau_L$',ylabel=r'$\bar P_0$',title='Unscattered electron fraction')
for i,ax in enumerate(axs):
    clean(ax); safe_panel(ax,chr(97+i))
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
