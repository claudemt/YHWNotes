import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""Exactly solvable Gaussian Ornstein--Uhlenbeck phase noise: FID vs ideal Hahn echo.
All quantities are dimensionless and share the same covariance and two-sided spectrum.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style

sigma=.8; tc=1.0
T=np.linspace(0,7,450); omega=np.linspace(.001,10,600)

def chi_f(T,tc):
    z=T/tc
    return sigma**2 *tc**2*(z+np.expm1(-z))
def chi_e(T,tc):
    z=T/tc
    return sigma**2*tc**2*(z-3+4*np.exp(-z/2)-np.exp(-z))
def Sf(w,tc): return 2*sigma*sigma*tc/(1+(w*tc)**2)
def Ff(w,t):return 4*np.sin(w*t/2)**2/(w*w)
def Fe(w,t):return 16*np.sin(w*t/4)**4/(w*w)
fig,axs=plt.subplots(2,3,figsize=(11.3,7.5),layout='constrained');axs=axs.ravel()
a=axs[0];tau=np.linspace(0,6,250)
for c in [.25,1.,3.]:a.plot(tau,sigma**2*np.exp(-tau/c),label=fr'$\tau_c={c}$')
a.set(xlabel=r'lag $|t-t\prime|$',ylabel=r'$C(t-t\prime)$');a.legend(frameon=False)
a=axs[1]
for c in [.25,1.,3.]:a.loglog(omega,Sf(omega,c),label=fr'$\tau_c={c}$')
a.set(xlabel=r'angular frequency $\omega$',ylabel=r'$S(\omega)$');a.legend(frameon=False)
a=axs[2]; T0=3.
a.plot(omega,Ff(omega,T0),label='free induction'); a.plot(omega,Fe(omega,T0),label='Hahn echo')
a.set(xlabel=r'$\omega$',ylabel=r'$|Y_T(\omega)|^2$',xlim=(0,7));a.legend(frameon=False)
a=axs[3]
for c,col in [(.3,'tab:orange'),(1,'tab:blue'),(3,'tab:green')]:
    a.plot(T,np.exp(-chi_f(T,c)),color=col,ls='-',label=fr'free, $\tau_c={c}$')
    a.plot(T,np.exp(-chi_e(T,c)),color=col,ls='--',label=fr'echo, $\tau_c={c}$')
a.set(xlabel=r'free evolution $T$',ylabel='coherence $W(T)$',ylim=(-.02,1.04));a.legend(frameon=False,ncol=2,fontsize=7.1)
a=axs[4]; tcc=np.geomspace(.15,6,90);tt=np.linspace(.1,6,90)
TT,CC=np.meshgrid(tt,tcc);enh=np.exp(-chi_e(TT,CC))/np.maximum(np.exp(-chi_f(TT,CC)),1e-10)
im=a.imshow(np.log10(enh),origin='lower',aspect='auto',extent=[tt[0],tt[-1],tcc[0],tcc[-1]],cmap='viridis')
a.set(xlabel=r'evolution time $T$',ylabel=r'correlation time $\tau_c$');fig.colorbar(im,ax=a,shrink=.83,label=r'$\log_{10}(W_{\rm echo}/W_{\rm FID})$')
a=axs[5];early=np.geomspace(.04,1.1,120)
a.loglog(early,chi_f(early,tc),label='FID $\chi(T)$')
a.loglog(early,chi_e(early,tc),label='echo $\chi(T)$')
a.loglog(early,sigma**2*early**2/2,'k:',lw=1,label=r'$\propto T^2$')
a.loglog(early,sigma**2*early**3/(12*tc),'k--',lw=1,label=r'$\propto T^3$')
a.set(xlabel=r'short time $T$',ylabel=r'phase variance exponent $\chi(T)$');a.legend(frameon=False,fontsize=7.1,ncol=2)
titles=['(a) Colored-noise correlation','(b) Two-sided noise spectrum',
'(c) Control filter functions','(d) Coherence with and without echo',
'(e) Echo enhancement regime','(f) Short-time scaling test']
for ax,ttl in zip(axs,titles):ax.set_title(ttl,loc='left',fontweight='bold',pad=8)
book_save(fig,Path(__file__).with_suffix('.pdf'))
# Numeric spectral identity using positive frequencies: chi = integral_0^inf S*|Y|^2/(2*pi)
w=np.linspace(.00001,350,250000)
valf=np.trapezoid(Sf(w,1)*Ff(w,3),w)/(2*np.pi)
vale=np.trapezoid(Sf(w,1)*Fe(w,3),w)/(2*np.pi)
print('noise: FID analytical/spectral',chi_f(3,1),valf,'echo',chi_e(3,1),vale)
assert abs(valf-chi_f(3,1))<1e-4 and abs(vale-chi_e(3,1))<1e-4
