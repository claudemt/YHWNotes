import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""Recoil-resolved ladder: exact finite-chain Schr. dynamics against resonant two-level truncation."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style
from scipy.linalg import eigh_tridiagonal

chi=1.; N=12; n=np.arange(-N,N+1)
initial=np.zeros(n.size,complex); initial[N]=1.

def evolve(g,t,cut=N):
    nn=np.arange(-cut,cut+1)
    lam,V=eigh_tridiagonal(chi*nn*(nn-1),np.full(len(nn)-1,g),check_finite=False)
    u=V@ (np.exp(-1j*lam*t)* V[cut,:])
    return nn,u

def metrics(g):
    tt=np.pi/(4*g)
    nn,psi=evolve(g,tt)
    q=np.abs(psi)**2
    leakage=1-q[np.isin(nn,[0,1])].sum()
    targ=np.zeros_like(psi); targ[np.where(nn==0)[0][0]]=1/np.sqrt(2); targ[np.where(nn==1)[0][0]]=-1j/np.sqrt(2)
    fidelity=abs(np.vdot(targ,psi))**2
    return leakage,fidelity,q

fig,axs=plt.subplots(2,3,figsize=(11.3,7.5),layout='constrained')
axs=axs.ravel()
a=axs[0]
a.plot(n,n*(n-1),'o-',ms=4,lw=1.5)
a.scatter([0,1],[0,0],s=55,c='#d85d3a',zorder=5)
a.set(xlim=(-5,6),ylim=(-1,33),xlabel=r'order $n$',ylabel=r'$\epsilon_n/\chi$')
# b: population vs ratio
G=np.geomspace(.045,3.3,95); mat=[]; leak=[]; fid=[]
for gg in G:
    ll,ff,qq=metrics(gg); leak.append(ll);fid.append(ff);mat.append(qq)
mat=np.array(mat);leak=np.array(leak);fid=np.array(fid)
a=axs[1]; im=a.imshow(mat.T,origin='lower',aspect='auto',extent=[G.min(),G.max(),n.min()-.5,n.max()+.5],cmap='magma',vmin=0,vmax=.6)
a.set(xscale='log',xlabel=r'$g/\chi$',ylabel=r'order $n$',ylim=(-7.5,8.5))
fig.colorbar(im,ax=a,shrink=.82,pad=.02,label=r'$P_n(\tau_{\pi/2})$')
# c: leak and fidelity
a=axs[2]; a.semilogx(G,leak,label='leakage',lw=1.9); a.semilogx(G,1-fid,label='infidelity',lw=1.9)
a.axhline(.01,color='0.5',lw=.8,ls=':'); a.set(xlabel=r'$g/\chi$',ylabel='error probability',ylim=(-.01,.9)); a.legend(frameon=False,loc='upper left')
# d: transition oscillations in bragg regime and crossover
a=axs[3]
for gg in [.12,.6,1.7]:
    tgrid=np.linspace(0,1.5*np.pi/(2*gg),150)
    nn=np.arange(-N,N+1); lam,V=eigh_tridiagonal(nn*(nn-1),np.full(len(nn)-1,gg))
    amp=V[N,:] # source at |0>
    psi=V@(amp[:,None]*np.exp(-1j*lam[:,None]*tgrid[None,:]))
    a.plot(gg*tgrid,np.abs(psi[nn==1,:][0])**2,label=fr'$g/\chi={gg}$')
a.plot(gg*tgrid,np.sin(gg*tgrid)**2,'k--',lw=1,label='two-level')
a.set(xlabel=r'pulse area $g\tau$',ylabel=r'$P_1$',ylim=(0,1.04));a.legend(frameon=False,ncol=2,loc='upper right')
# e: large-g wavefront, not pure readout duplication
a=axs[4]
for gg in [.12,.65,2.4]:
    nn,psi=evolve(gg,np.pi/(4*gg)); a.plot(nn,np.abs(psi)**2,'o-',ms=2.9,label=fr'$g/\chi={gg}$')
a.set(xlim=(-8,9),xlabel=r'order $n$',ylabel=r'$P_n(\tau_{\pi/2})$');a.legend(frameon=False)
# f: cutoff convergence
C=[3,4,5,6,8,10,12,16,20]
a=axs[5]
for gg in [.4,1.4,3.0]:
    vals=[]
    _,u_ref=evolve(gg,np.pi/(4*gg),cut=32)
    for cut in C:
        _,u=evolve(gg,np.pi/(4*gg),cut=cut)
        shared=u_ref[32-cut:33+cut]
        vals.append(1-np.abs(np.vdot(shared,u))**2)
    a.semilogy(C,np.maximum(vals,1e-14),'o-',ms=3,label=fr'$g/\chi={gg}$')
a.set(xlabel='ladder half-width $N$',ylabel='embedding infidelity');a.legend(frameon=False)

titles=['(a) Recoil ladder','(b) Sideband population fan',
'(c) Error at the nominal pulse','(d) Beyond two-level Rabi dynamics',
'(e) Output spectra','(f) Cutoff convergence']
for ax,title in zip(axs,titles):ax.set_title(title,loc='left',fontweight='bold',pad=8)
book_save(fig,Path(__file__).with_suffix('.pdf'));plt.close(fig)
print('recoil: pnorm',mat.sum(axis=1).min(),mat.sum(axis=1).max(),'leak bounds',leak.min(),leak.max())
