from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pubfig, clean, safe_panel, finish_pub

fig, axs = plt.subplots(2,3,figsize=(10.6,7.9),constrained_layout=True)
axs=axs.ravel()
from scipy.special import jv
n=np.arange(-18,19); c=jv(n,5); th=np.linspace(-np.pi,np.pi,500); sig=np.linspace(0,1.2,120); al=.48; I=np.zeros((len(sig),len(th)))
for i,s in enumerate(sig):
 rho=np.outer(c,c)*np.exp(-1j*al*(n[:,None]**2-n[None,:]**2))*np.exp(-.5*(n[:,None]-n[None,:])**2*s*s); e=np.exp(1j*n[:,None]*th); I[i]=np.real(np.sum((rho@e)*np.conj(e),axis=0))
im=axs[0].imshow(I,origin='lower',aspect='auto',extent=[-np.pi,np.pi,0,1.2]); axs[0].set_xlabel('$\\theta$'); axs[0].set_ylabel('$\\sigma_\\phi$'); fig.colorbar(im,ax=axs[0],label='density')
for s in [0,.2,.5,1]: axs[1].plot(th,I[np.argmin(abs(sig-s))],label=f'{s}'); axs[1].set_xlabel('$\\theta$'); axs[1].set_ylabel('density'); axs[1].legend()
contrast=(I.max(1)-I.min(1))/(I.max(1)+I.min(1)); axs[2].plot(sig,contrast); axs[2].set_xlabel('$\\sigma_\\phi$'); axs[2].set_ylabel('temporal contrast')
width=[]
for row in I:
 r=row/row.max(); width.append(np.sum(r>.5)*(th[1]-th[0]))
axs[3].plot(sig,width); axs[3].set_xlabel('$\\sigma_\\phi$'); axs[3].set_ylabel('FWHM proxy')
# Parseval gives a phase-space purity proxy without adding arbitrary noise curves.
pop=abs(c)**2
purity=np.array([np.sum(np.outer(pop,pop)*np.exp(-(n[:,None]-n[None,:])**2*z*z)) for z in sig])
axs[4].plot(sig,purity); axs[4].set(xlabel=r'$\sigma_\phi$',ylabel=r'$\mathrm{Tr}\,\rho^2$',title='Loss of energy coherence')
first_harmonic=np.abs(np.trapz(I*np.exp(1j*th[None,:]),th,axis=1))/(2*np.pi)
axs[5].plot(sig,first_harmonic); axs[5].set(xlabel=r'$\sigma_\phi$',ylabel='first temporal harmonic',title='Interference harmonic decay')
for i,ax in enumerate(axs):
    clean(ax); safe_panel(ax,chr(97+i))
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
