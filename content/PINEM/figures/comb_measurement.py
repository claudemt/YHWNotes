import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""Finite-energy comb, optical-pointer readout and information-budget benchmark.
Gaussian optical readout is a declared effective homodyne pointer model, not a device calibration.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style

rng=np.random.default_rng(1609)
phi0=.86; g=.85; r=.65; sigma_det=.09
var=.25*np.exp(-2*r)+sigma_det**2
sig=np.sqrt(var)
ph=np.linspace(-np.pi,np.pi,700)
fig,axs=plt.subplots(2,3,figsize=(11.3,7.5),layout='constrained'); axs=axs.ravel()
# a finite comb energy populations
a=axs[0]
for M in [5,11,21]:
    n=np.arange(-12,13);p=(np.abs(n)<=(M-1)//2)/M
    a.plot(n,p,'o-',ms=2.4,label=fr'$M={M}$')
a.set(xlabel=r'energy order $n$',ylabel=r'$|c_n|^2$',xlim=(-12,12));a.legend(frameon=False)
# b canonical phase-POVM response of finite comb
ax=axs[1]
for M in [5,11,21]:
    p=np.abs(np.sum(np.exp(1j*np.arange(M)[:,None]*ph[None,:]),axis=0))**2/(2*np.pi*M)
    ax.plot(ph,p,label=fr'$M={M}$')
ax.set(xlabel=r'phase difference $\delta$',ylabel=r'$p_M(\delta)$');ax.legend(frameon=False)
# c homodyne pointer as phase-encoded circle
ax=axs[2]; xx=g*np.cos(ph);yy=g*np.sin(ph)
ax.plot(xx,yy,color='#576c8e',lw=1.2,label='ideal pointer mean')
shots=g*np.array([np.cos(phi0),np.sin(phi0)])[None,:] + rng.normal(0,sig,size=(130,2))
ax.scatter(shots[:,0],shots[:,1],c='tab:orange',s=9,alpha=.35,label='single-shot records')
ax.scatter([g*np.cos(phi0)],[g*np.sin(phi0)],color='k',s=28,marker='x')
ax.set(xlabel=r'$X$',ylabel=r'$P$',aspect='equal');ax.legend(frameon=False,fontsize=7.0)
# d posteriors for accumulating records from one sample
a=axs[3]
for N in [1,4,20]:
    Y=shots[:N]
    dist2=np.sum((Y[:,None,:]-g*np.stack([np.cos(ph),np.sin(ph)],axis=1)[None,:,:])**2,axis=(0,2))
    lp=-dist2/(2*var);p=np.exp(lp-np.max(lp));p/=np.trapezoid(p,ph)
    a.plot(ph,p,label=fr'$N_e={N}$')
a.axvline(phi0,color='0.4',ls='--',lw=.9);a.set(xlabel=r'candidate phase $\phi$',ylabel='normalized likelihood');a.legend(frameon=False)
# e Fisher vs squeez parameter and noise floor
a=axs[4]; rs=np.linspace(0,1.6,120)
for noise in [.05,.15,.30]:
    FF=g*g/(.25*np.exp(-2*rs)+noise**2)
    a.plot(rs,FF,label=fr'$\sigma_{{\mathrm{{det}}}}={noise}$')
a.set(xlabel=r'squeezing $r$',ylabel=r'$F_{\phi\phi}$ per event');a.legend(frameon=False)
# f empirical circular phase RMSE vs shot count vs CRB
a=axs[5]; Ns=np.array([1,2,3,5,8,12,20,35,60,100,160])
MC=2300
for label,ss,linestyle in [('squeezed',sig,'-'),('vacuum',np.sqrt(.25+sigma_det**2),'--')]:
    mmax=int(Ns[-1]); eps=rng.normal(0,ss,size=(MC,mmax,2))
    Ys=np.cumsum(g*np.array([np.cos(phi0),np.sin(phi0)])[None,None,:]+eps,axis=1)
    RM=[]
    for N in Ns:
        est=np.arctan2(Ys[:,N-1,1],Ys[:,N-1,0]); err=np.angle(np.exp(1j*(est-phi0)))
        RM.append(np.sqrt(np.mean(err**2)))
    a.loglog(Ns,RM,'o'+linestyle,ms=3,label=label+' MC')
    a.loglog(Ns,ss/(g*np.sqrt(Ns)),linestyle,color='0.45',alpha=.68,label=label+' local CRB')
a.set(xlabel='accepted electron events',ylabel='circular phase RMSE [rad]');a.legend(frameon=False,fontsize=7.1,ncol=2)

titles=['(a) Finite energy comb','(b) Canonical phase kernel',
'(c) Noisy optical pointer','(d) Conditional phase likelihood',
'(e) Fisher information vs squeezing','(f) Estimation RMSE vs dose']
for ax,title in zip(axs,titles):ax.set_title(title,loc='left',fontweight='bold',pad=8)
book_save(fig,Path(__file__).with_suffix('.pdf'))
print('comb: POVM area M=11', np.trapezoid(np.abs(np.sum(np.exp(1j*np.arange(11)[:,None]*ph[None,:]),axis=0))**2/(2*np.pi*11),ph), 'pointervar',var)
