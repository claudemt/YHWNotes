import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
OUT=Path(__file__).with_suffix('.pdf')

fig=pubfig(8.6,6.0,top=.92,left=.075,right=.97,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.62,hspace=.58)
ax=[]
for r in range(2):
 for c in range(3): ax.append(fig.add_subplot(gs[r,c]))
n,t,P,pur,coh,gap=ne.open_system_ladder_dynamics(g=1.8,dephasing=.18,relaxation=.035)
im=ax[0].imshow(P.T,origin='lower',aspect='auto',extent=[t[0],t[-1],n[0],n[-1]],cmap='magma')
safe_colorbar(fig,im,ax[0],'population'); ax[0].set(xlabel='time',ylabel='photon order n'); safe_title(ax[0],'Open-system energy ladder'); safe_panel(ax[0],'a')
ax[1].plot(t,pur,label='purity'); ax[1].plot(t,coh,label='coherence'); ax[1].legend(frameon=False); ax[1].set(xlabel='time',ylabel='normalized measure',ylim=(0,1.05)); safe_title(ax[1],'Coherence buildup and loss'); safe_panel(ax[1],'b')
gam,gaps=ne.liouvillian_gap_scan(nmax=4,dephasings=np.linspace(0,1.5,41)); ax[2].plot(gam,gaps); ax[2].axvline(.18,ls='--',lw=.8,color='0.3'); ax[2].set(xlabel='dephasing rate',ylabel='Liouvillian gap'); safe_title(ax[2],'Relaxation spectrum'); safe_panel(ax[2],'c')
for k,gg in enumerate([0,.08,.25]):
 n2,t2,P2,_,_,_=ne.open_system_ladder_dynamics(g=1.8,dephasing=gg,relaxation=.02,times=np.linspace(0,5,101)); ax[3].plot(n2,P2[-1],label=f'gamma={gg:.2f}')
ax[3].legend(frameon=False); ax[3].set(xlabel='photon order n',ylabel='final population'); safe_title(ax[3],'Finite-time spectral broadening'); safe_panel(ax[3],'d')
# dissipative spectral atlas from the exact Liouvillian (small basis for scan)
G=np.linspace(0.3,2.8,12); D=np.linspace(0,0.8,12); Z=np.zeros((len(D),len(G)))
for i,d in enumerate(D):
 for j,g in enumerate(G):
  nn,HH=ne.energy_ladder_hamiltonian(nmax=3,g=g); LL=ne.lindblad_superoperator(HH,d,.03); ev=np.linalg.eigvals(LL); sr=np.sort(ev.real)[::-1]; Z[i,j]=max(0,-sr[1])
im2=ax[4].imshow(Z,origin='lower',aspect='auto',extent=[G[0],G[-1],D[0],D[-1]],cmap='viridis'); safe_colorbar(fig,im2,ax[4],'Liouvillian gap'); ax[4].set(xlabel='coupling g',ylabel='dephasing'); safe_title(ax[4],'Dissipative spectral atlas'); safe_panel(ax[4],'e')
# spectral moments
means=(P*n[None,:]).sum(1); vars=(P*(n[None,:]-means[:,None])**2).sum(1)
ax[5].plot(t,means,label='<n>'); ax[5].plot(t,np.sqrt(vars),label='sigma_n'); ax[5].legend(frameon=False); ax[5].set(xlabel='time',ylabel='moment'); safe_title(ax[5],'Transport observables'); safe_panel(ax[5],'f')
for a in ax: clean(a)
finish_pub(fig,OUT)
