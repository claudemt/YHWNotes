import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""Exactly antisymmetric 1D two-fermion wavepackets under a soft-Coulomb relative potential.
Teaching benchmark in dimensionless hbar=m=1; not a calibrated 3D electron-electron experiment.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style

Nx=176; L=9.; x=np.linspace(-L,L,Nx,endpoint=False);dx=x[1]-x[0]
X1,X2=np.meshgrid(x,x,indexing='ij')
sigma=.65; x0=2.0; p0=1.8; u=3.2; a=.45
phiL=np.exp(-(x+x0)**2/(4*sigma**2)+1j*p0*x)
phiR=np.exp(-(x-x0)**2/(4*sigma**2)-1j*p0*x)
psi0=(phiL[:,None]*phiR[None,:]-phiR[:,None]*phiL[None,:])
psi0/=np.sqrt(np.sum(abs(psi0)**2)*dx*dx)
k=2*np.pi*np.fft.fftfreq(Nx,d=dx)
K1,K2=np.meshgrid(k,k,indexing='ij'); K2energy=(K1**2+K2**2)/2
RR=X1-X2; Urel=u/np.sqrt(RR**2+a**2)
T=1.35;steps=180;dt=T/steps
kin=np.exp(-1j*K2energy*dt)
mask=np.abs(RR)<.75

def propagate(strength):
    psi=psi0.copy();rec=[]
    for i in range(steps+1):
        P=abs(psi)**2
        rec.append(np.sum(P[mask])*dx*dx)
        if i==steps:break
        phase=np.exp(-.5j*dt*strength*Urel)
        psi=phase*psi
        psi=np.fft.ifft2(np.fft.fft2(psi)*kin)
        psi=phase*psi
    return psi,np.array(rec)

psif,free=propagate(0);psiu,inter=propagate(1)
Pf=np.abs(psif)**2;Pu=np.abs(psiu)**2;P0=np.abs(psi0)**2
# sum along antidiagonals for relative probability density using density-integration over center:
rgrid=np.linspace(-8,8,300)
# fast discretized rel marginal with histogram

def rel_hist(p):
    bins=np.linspace(-8,8,201)
    val=np.histogram(RR.ravel(),bins=bins,weights=(p*dx*dx).ravel())[0]
    centers=.5*(bins[1:]+bins[:-1]); return centers,val/(bins[1]-bins[0])

fig,axs=plt.subplots(2,3,figsize=(11.3,7.5),layout='constrained');axs=axs.ravel()
axs[0].plot(rgrid,u/np.sqrt(rgrid**2+a*a),lw=2)
axs[0].set(xlabel=r'relative coordinate $r=x_1-x_2$',ylabel=r'$V(r)$',xlim=(-5,5))
for j,P in [(1,P0),(2,Pf),(3,Pu)]:
    ax=axs[j]
    im=ax.imshow(P.T,origin='lower',extent=[x[0],x[-1],x[0],x[-1]],cmap='magma',vmin=0,vmax=.13,aspect='equal')
    ax.set(xlim=(-5.2,5.2),ylim=(-5.2,5.2),xlabel=r'$x_1$',ylabel=r'$x_2$')
    ax.plot([-5.2,5.2],[-5.2,5.2],'w--',lw=.7,alpha=.55)
fig.colorbar(im,ax=axs[3],shrink=.81,pad=.02,label=r'$P(x_1,x_2)$')
for P,lab in [(Pf,'free fermions'),(Pu,'interacting fermions')]:
    rx,dens=rel_hist(P);axs[4].plot(rx,dens,lw=1.7,label=lab)
axs[4].set(xlim=(-5,5),xlabel=r'relative distance $x_1-x_2$',ylabel=r'$p(r,T)$');axs[4].legend(frameon=False)
times=np.arange(steps+1)*dt
axs[5].plot(times,free,label='exchange only $u=0$')
axs[5].plot(times,inter,label=fr'with repulsion $u={u}$')
axs[5].set(xlabel=r'time $t$',ylabel=r'$\Pr(|x_1-x_2|<0.75)$');axs[5].legend(frameon=False)
titles=['(a) Soft-Coulomb repulsion','(b) Incoming fermion pair',
'(c) Free exchange evolution','(d) Interacting collision',
'(e) Relative-coordinate density','(f) Near-coincidence statistics']
for ax,title in zip(axs,titles):ax.set_title(title,loc='left',fontweight='bold',pad=8)
book_save(fig,Path(__file__).with_suffix('.pdf'));plt.close(fig)
print('collision norm',np.sum(Pu)*dx*dx,'antisym error',np.max(np.abs(psiu+psiu.T)),'final coinc',free[-1],inter[-1])
