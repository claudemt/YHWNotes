import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""Two-color PINEM sideband interference and dispersive temporal caustics."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style
from scipy.special import jv

B1,B2=2.1,1.05
n=np.arange(-36,37); th=np.linspace(-np.pi,np.pi,280,endpoint=False)
phases=np.linspace(-np.pi,np.pi,71)
alphas=np.linspace(0,.38,114)
EX=np.exp(1j*np.outer(n,th))

def amps(phi):
    c=np.zeros(len(n),complex)
    for n1 in range(-18,19):
        for n2 in range(-9,10):
            nn=n1+2*n2
            if abs(nn)>36:continue
            c[nn+36]+=jv(n1,2*B1)*jv(n2,2*B2)*np.exp(1j*n2*phi)
    return c/np.linalg.norm(c)

def wave(phi,alpha):
    c=amps(phi)*np.exp(-1j*alpha*n**2)
    field=c@EX
    return np.abs(field)**2/(np.sum(np.abs(field)**2)/len(th))

fig,axs=plt.subplots(2,3,figsize=(11.4,7.0),layout='constrained');axs=axs.ravel()
# a spectral interference vs relative phase
spec=np.array([abs(amps(phi))**2 for phi in phases])
a=axs[0];im=a.imshow(spec.T,origin='lower',aspect='auto',extent=[-np.pi,np.pi,n[0]-.5,n[-1]+.5],
                        cmap='magma',vmax=np.percentile(spec,99.3))
a.set(xlim=(-np.pi,np.pi),ylim=(-14,14),xlabel=r'relative phase $\phi_2$',ylabel=r'energy order $n$')
fig.colorbar(im,ax=a,shrink=.88,label=r'$P_n$')
# b: the initial state has constant INTENSITY, so plotting two
# intensity curves hides all phase information. Plot the actual phase
# modulations; these are the physical input to dispersive propagation.
for phi,style in [(0,'-'),(np.pi/2,'--')]:
    phase=2*B1*np.sin(th)+2*B2*np.sin(2*th+phi)
    axs[1].plot(th,phase,ls=style,label=fr'$\phi_2={phi/np.pi:g}\pi$')
axs[1].set(xlabel=r'optical phase $\theta$',ylabel=r'initial phase $\Phi(\theta)$ (rad)')
axs[1].legend(frameon=False)
# c propagation caustics for phase 0
a=axs[2];evo=np.array([wave(0,alpha) for alpha in alphas])
im=a.imshow(evo,origin='lower',aspect='auto',extent=[-np.pi,np.pi,alphas[0],alphas[-1]],cmap='inferno',vmax=np.percentile(evo,99.5))
a.set(xlabel=r'optical phase $\theta$',ylabel=r'dispersion $\alpha$');fig.colorbar(im,ax=a,shrink=.88,label=r'$2\pi\rho$')
# d compare propagation shapes at focus
alpha_focus=alphas[np.argmax(evo.max(axis=1))]
a=axs[3]
for phi in [-np.pi/2,0,np.pi/2]:a.plot(th,wave(phi,alpha_focus),label=fr'$\phi_2={phi/np.pi:g}\pi$')
a.set(xlabel=r'optical phase $\theta$',ylabel=r'$2\pi\rho(\theta,\alpha_*)$')
a.legend(frameon=False,ncol=1)
# e harmonic bunching from same wavefunction
a=axs[4]
for q in [1,2,3]:
    bunch=np.abs(np.mean(evo*np.exp(1j*q*th)[None,:],axis=1))
    a.plot(alphas,bunch,label=fr'$q={q}$')
a.set(xlabel=r'dispersion $\alpha$',ylabel=r'$|\langle e^{\mathrm{i}q\theta}\rangle|$');a.legend(frameon=False)
# f relative optical phase controls peak caustic concentration
# computed from exactly the same Bessel coefficients and propagator
phif=np.linspace(-np.pi,np.pi,51);af=np.linspace(0,.38,83)
maxmap=np.empty((len(af),len(phif)))
for j,phi in enumerate(phif):
    c=amps(phi)
    states=(c[None,:]*np.exp(-1j*np.outer(af,n*n)))@EX
    maxmap[:,j]=np.max(abs(states)**2,axis=1)
a=axs[5];im=a.imshow(maxmap,origin='lower',aspect='auto',extent=[-np.pi,np.pi,af[0],af[-1]],cmap='viridis')
a.set(xlabel=r'relative phase $\phi_2$',ylabel=r'dispersion $\alpha$');fig.colorbar(im,ax=a,shrink=.88,label=r'$\max_\theta 2\pi\rho$')
titles=['(a) Interfering two-color sideband paths','(b) Phase modulation before propagation',
        '(c) Formation of temporal caustics','(d) Optical phase steers the focus',
        '(e) Harmonic bunching after dispersion','(f) Phase-controlled compression landscape']
for ax,t in zip(axs,titles):ax.set_title(t,loc='left',pad=8,fontweight='bold')
book_save(fig,Path(__file__).with_suffix('.pdf'));plt.close(fig)
