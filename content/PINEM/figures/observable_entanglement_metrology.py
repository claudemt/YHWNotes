import common  # shared style + embedded model helpers
from pathlib import Path
import sys,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import matplotlib.pyplot as plt
from models.novel_extensions import measured_joint_distribution,mutual_information,phase_fisher
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
OUT=Path(__file__).with_suffix('.pdf'); fig=pubfig(7.5,5.4,top=.91); gs=fig.add_gridspec(2,3,wspace=.48,hspace=.52)
Ns,Ls,P,Q=measured_joint_distribution(2,2,-1,-2,0,0,phi2=-np.pi/2)
from matplotlib.colors import PowerNorm
# Here ell_1=-1 and ell_2=-2. Every *ideal* transition satisfies
# r = ell+N = 0. The sheared coordinates (N,r) expose selection-rule
# violations caused by the actual instrument, without large black
# corners of a diagonal ridge in the original (N,ell) square.
rvals=np.arange(-6,7)
nkeep=np.flatnonzero((Ns>=-14)&(Ns<=14))
def shear_joint(M):
    out=np.zeros((len(rvals),len(nkeep)))
    lookup={int(ell):i for i,ell in enumerate(Ls)}
    for j,ind in enumerate(nkeep):
        for a,r in enumerate(rvals):
            ix=lookup.get(int(r-Ns[ind]))
            if ix is not None: out[a,j]=M[ix,ind]
    return out
_,_,_,blur=measured_joint_distribution(2,2,-1,-2,1.2,1.2,phi2=-np.pi/2)
shot=measured_joint_distribution(2,2,-1,-2,1.2,1.2,counts=25000,seed=2,phi2=-np.pi/2)[3]
retained=[shear_joint(M).sum()/M.sum() for M in (P,blur,shot)]
print('SHEARED_WINDOW_PROBABILITY',retained)
assert min(retained)>.99, 'The selected detector display must retain over 99% of events'
common_norm=PowerNorm(gamma=.58,vmin=0,vmax=float(P.max()))
for j,(M,title) in enumerate([(P,'Ideal selection rule'),(blur,'Finite resolution'),(shot,'Poisson counts')]):
 ax=fig.add_subplot(gs[0,j]); im=ax.imshow(shear_joint(M),origin='lower',
     extent=[Ns[nkeep[0]]-.5,Ns[nkeep[-1]]+.5,rvals[0]-.5,rvals[-1]+.5],
     interpolation='nearest',aspect='auto',cmap='magma',norm=common_norm)
 ax.set(xlabel='energy order $N$',ylabel=r'residual OAM $r=\ell+N$' if j==0 else '')
 safe_panel(ax,chr(97+j)); safe_title(ax,title); clean(ax)
 if j==2:safe_colorbar(fig,im,ax,'prob.',pad=.04)
# resolution map MI
sig=np.linspace(0,2.2,45); MI=np.zeros((len(sig),len(sig))); FI=np.zeros_like(MI)
for i,sn in enumerate(sig):
 for j,sl in enumerate(sig):
  _,_,_,M=measured_joint_distribution(2,2,-1,-2,sn,sl,nmax=11,phi2=-np.pi/2)
  MI[j,i]=mutual_information(M)
  if i%2==0 and j%2==0: FI[j,i]=phase_fisher(2,2,-1,-2,sn,sl,nmax=9)
ax=fig.add_subplot(gs[1,0]); im=ax.imshow(MI,origin='lower',extent=[0,2.2,0,2.2],aspect='auto',cmap='viridis'); ax.set(xlabel=r'$\sigma_N$',ylabel=r'$\sigma_\ell$'); safe_panel(ax,'d'); safe_title(ax,'Measurable mutual information'); clean(ax); safe_colorbar(fig,im,ax,'bits',pad=.04)
# fisher one-dimensional cuts for speed/readability
ax=fig.add_subplot(gs[1,1]); vals=[]
for s in sig: vals.append(phase_fisher(2,2,-1,-2,s,s,nmax=10))
ax.semilogy(sig,np.maximum(vals,1e-8)); ax.set(xlabel='isotropic resolution $\\sigma$',ylabel='phase Fisher information'); safe_panel(ax,'e'); safe_title(ax,'Phase Fisher at $\\theta_2=-\\pi/2$'); clean(ax)
# score signal versus measured energy: finite-resolution differentiation is
# computed from the SAME forward model, not an arbitrary scaled CRLB line.
ax=fig.add_subplot(gs[1,2]); delta=1e-3
for s,label,col in [(0.,'Ideal', '#2677a8'),(1.2,r'$\sigma=1.2$','#c77641')]:
    _,_,_,pplus=measured_joint_distribution(2,2,-1,-2,s,s,nmax=16,phi2=-np.pi/2+delta)
    _,_,_,pminus=measured_joint_distribution(2,2,-1,-2,s,s,nmax=16,phi2=-np.pi/2-delta)
    deriv=(pplus-pminus).sum(axis=0)/(2*delta)
    ax.plot(Ns,deriv,color=col,label=label)
ax.axhline(0,color='.55',lw=.65)
ax.set(xlabel='energy order $N$',ylabel=r'$\partial_{\phi}P_N$',xlim=(-12,12))
ax.legend(frameon=False); safe_panel(ax,'f'); safe_title(ax,'Phase-response spectrum'); clean(ax)
finish_pub(fig,OUT)
