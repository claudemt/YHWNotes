"""Bessel sideband moments and the energy-detector inverse problem.

A single normalized ideal distribution is used for all six panels.
The only phenomenological element is a normalized Gaussian detector response.
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save, COLORS

rng=np.random.default_rng(2409)
orders=np.arange(-24,25)
bs=np.linspace(0,3.6,160)

def pn(beta):
    p=jv(orders,2*beta)**2
    return p/p.sum()

def blurred_energy(beta,sigma,energy):
    pp=pn(beta)
    kernel=np.exp(-0.5*((energy[:,None]-orders[None,:])/sigma)**2)/(
        np.sqrt(2*np.pi)*sigma)
    return kernel@pp

fig,axs=plt.subplots(2,3,figsize=(9.6,6.55))
axs=axs.ravel()

# (a) a common unit-normalized probability family
ax=axs[0]
for beta,col in zip([0.5,1.7,3.0],[COLORS['blue'],COLORS['orange'],COLORS['green']]):
    pp=pn(beta)
    ax.plot(orders,pp,'o-',lw=1.3,ms=2.3,color=col,label=fr'$|\beta|={beta:g}$')
ax.set(xlim=(-12,12),xlabel=r'Energy order $n$',ylabel=r'$P_n$')
ax.legend(frameon=False,loc='upper right',fontsize=7.6)

# (b) complete Bessel oscillations
ax=axs[1]
data=np.stack([pn(beta) for beta in bs],axis=1)
im=ax.imshow(data,origin='lower',aspect='auto',extent=[bs[0],bs[-1],orders[0]-.5,orders[-1]+.5],
             cmap='magma',interpolation='nearest',vmin=0)
ax.set(xlabel=r'$|\beta|$',ylabel=r'Order $n$',ylim=(-12,12))
fig.colorbar(im,ax=ax,shrink=0.82,label='Population')

# (c) how much detected probability is lost by a finite energy window
ax=axs[2]
variance=(orders[:,None]**2*data).sum(axis=0)
for N,col in [(2,COLORS['blue']),(5,COLORS['orange']),(10,COLORS['green'])]:
    tail=data[np.abs(orders)>N].sum(axis=0)
    ax.semilogy(bs, np.where(tail>=1e-5,tail,np.nan),color=col,label=rf'$|n|>{N}$')
ax.set(xlabel=r'$|\beta|$',ylabel='Probability outside window',ylim=(1e-5,1.02),xlim=(0,3.6))
ax.legend(frameon=False,loc='lower right')

# (d) fourth cumulant, negative = non-Gaussian distribution
ax=axs[3]
kappa4=2*bs**2-6*bs**4
numerical=(orders[:,None]**4*data).sum(axis=0)-3*variance**2
ax.axhline(0,lw=0.75,color='0.55')
ax.plot(bs,kappa4,lw=1.7,color=COLORS['green'])
ax.axvline(1/np.sqrt(3),ls='--',lw=1,color=COLORS['orange'])
ax.text(.97,.90,r'$\kappa_4=0: |\beta|=1/\sqrt{3}$',transform=ax.transAxes,
        ha='right',va='top',fontsize=8.5)
ax.set(xlabel=r'$|\beta|$',ylabel=r'Fourth cumulant $\kappa_4(n)$',xlim=(0,.95),ylim=(-3.2,0.8))

# (e) detector resolution without any change of the electron density operator
ax=axs[4]
E=np.linspace(-7,7,1600)
for ss,col in zip([0.15,0.55,1.15],[COLORS['blue'],COLORS['orange'],COLORS['green']]):
    ax.plot(E,blurred_energy(1.7,ss,E),lw=1.15,color=col,label=fr'$\sigma_E/(\hbar\omega)={ss}$')
ax.set(xlabel=r'$(E-E_0)/(\hbar\omega)$',ylabel='Measured density')
ax.legend(loc='upper right',frameon=False,fontsize=6.7)

# (f) finite-count precision of variance-inversion estimator
ax=axs[5]
sigma_grid=np.linspace(0.15,1.40,17)
rep=140; nshots=1800; beta=1.7
values=[]
for sig in sigma_grid:
    # independent sample, not an analytic noise curve
    samples=rng.choice(orders,size=(rep,nshots),p=pn(beta))
    data_E=samples + rng.normal(0,sig,(rep,nshots))
    # known E0: second central moment of the measured energy law
    v_est=np.mean(data_E**2,axis=1)-sig**2
    bhat=np.sqrt(np.maximum(v_est,0)/2)
    values.append(np.sqrt(np.mean((bhat-beta)**2)))
ax.plot(sigma_grid,values,'o-',ms=3.0,color=COLORS['blue'],lw=1.4)
ax.set(xlabel=r'$\sigma_E/(\hbar\omega)$',ylabel=r'$\operatorname{RMSE}(\hat\beta)$')
ax.set_ylim(bottom=0)

for a in axs:
    a.grid(False)
    a.tick_params(direction='out',length=3,width=0.65)
save(fig,Path(__file__).with_suffix('.pdf'))
