from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pubfig, clean, safe_panel, finish_pub

fig, axs = plt.subplots(2,3,figsize=(10.6,7.9),constrained_layout=True)
axs=axs.ravel()
from scipy.special import jv
n=np.arange(-18,19); c=jv(n,5.2); al=np.linspace(0,2*np.pi,360); th=np.linspace(-np.pi,np.pi,500); I=np.zeros((len(al),len(th)))
for i,a in enumerate(al):
 psi=np.sum(c[:,None]*np.exp(-1j*a*n[:,None]**2)*np.exp(1j*n[:,None]*th[None,:]),axis=0); I[i]=np.abs(psi)**2
im=axs[0].imshow(I,origin='lower',aspect='auto',extent=[-np.pi,np.pi,0,2*np.pi]); axs[0].set_xlabel('longitudinal phase $\\theta$'); axs[0].set_ylabel('$\\alpha$'); fig.colorbar(im,ax=axs[0],label='density')
for a in [0,np.pi/4,np.pi/2,np.pi]:
 psi=np.sum(c[:,None]*np.exp(-1j*a*n[:,None]**2)*np.exp(1j*n[:,None]*th[None,:]),axis=0); axs[1].plot(th,np.abs(psi)**2,label=f'{a/np.pi:.2g}$\\pi$')
axs[1].set_xlabel('$\\theta$'); axs[1].set_ylabel('density'); axs[1].legend()
contrast=(I.max(1)-I.min(1))/(I.max(1)+I.min(1)); axs[2].plot(al/np.pi,contrast); axs[2].set_xlabel('$\\alpha/\\pi$'); axs[2].set_ylabel('contrast')
particip=(I.sum(1)**2)/(np.sum(I*I,1)+1e-12); axs[3].plot(al/np.pi,particip); axs[3].set_xlabel('$\\alpha/\\pi$'); axs[3].set_ylabel('temporal participation')
# Revival fidelity is the modulus of the return amplitude of the energy comb.
recoil_fidelity=np.array([abs(np.sum(abs(c)**2*np.exp(-1j*a*n*n)))**2 for a in al])
axs[4].plot(al/np.pi,recoil_fidelity); axs[4].set(xlabel=r'$\alpha/\pi$',ylabel='return fidelity',title='Talbot recurrence')
axs[5].plot(al/np.pi,I.max(1)); axs[5].set(xlabel=r'$\alpha/\pi$',ylabel=r'$\max_\theta I(\theta)$',title='Propagation-dependent bunching')
for i,ax in enumerate(axs):
    clean(ax); safe_panel(ax,chr(97+i))
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
