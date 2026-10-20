import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from scipy.special import jv
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
OUT=Path(__file__).with_suffix('.pdf')
beta=1.8; means=np.geomspace(.5,32,20); tv=[]; ent=[]; widths=[]
for mu in means:
 area=beta/np.sqrt(mu); nph=max(26,int(mu+5.5*np.sqrt(mu)+8)); n,m,P,psi=ne.quantum_pinem_joint('coherent',ne=8,nph=nph,mean=mu,pulse_area=area); pe=P.sum(1); pcl=jv(n,2*beta)**2; pcl/=pcl.sum(); tv.append(.5*np.sum(abs(pe-pcl))); ent.append(ne.bipartite_entropy_from_state(psi,8,nph)[0]); av=np.sum(n*pe); widths.append(np.sqrt(np.sum((n-av)**2*pe)))
fig=pubfig(9.0,6.2,top=.92,left=.07,right=.97,bottom=.08); gs=fig.add_gridspec(2,3,wspace=.58,hspace=.60); ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
for mu in [.5,2,10,30]:
 area=beta/np.sqrt(mu); nph=max(26,int(mu+5.5*np.sqrt(mu)+8)); n,m,P,psi=ne.quantum_pinem_joint('coherent',ne=8,nph=nph,mean=mu,pulse_area=area); ax[0].plot(n,P.sum(1),'o-',ms=2.4,label=f'nbar={mu}')
pcl=jv(n,2*beta)**2; pcl/=pcl.sum(); ax[0].plot(n,pcl,'k--',lw=1.4,label='classical Bessel'); ax[0].legend(frameon=False,ncol=2); ax[0].set(xlabel='electron order',ylabel='probability'); safe_title(ax[0],'Spectral convergence to classical PINEM'); safe_panel(ax[0],'a')
ax[1].loglog(means,tv,'o-'); ax[1].set(xlabel='mean photon occupation',ylabel='TV distance to classical spectrum'); safe_title(ax[1],'Quantitative classical limit'); safe_panel(ax[1],'b')
ax[2].semilogx(means,ent,'o-'); ax[2].set(xlabel='mean photon occupation',ylabel='electron-photon entropy [bits]'); safe_title(ax[2],'Disappearing quantum entanglement'); safe_panel(ax[2],'c')
for mu,aidx in [(1,0),(30,1)]:
 area=beta/np.sqrt(mu); nph=max(26,int(mu+5.5*np.sqrt(mu)+8)); n,m,P,psi=ne.quantum_pinem_joint('coherent',ne=8,nph=nph,mean=mu,pulse_area=area); target=ax[3+aidx]; im=target.imshow(P.T,origin='lower',aspect='auto',extent=[n[0]-.5,n[-1]+.5,-.5,len(m)-.5],cmap='magma'); safe_colorbar(fig,im,target,'joint P'); target.set(xlabel='electron order',ylabel='photon number'); safe_title(target,f'Joint state at nbar={mu}'); safe_panel(target,'d' if aidx==0 else 'e')
ax[5].semilogx(means,widths,label='quantum rms width'); ax[5].axhline(np.sqrt(np.sum(n*n*pcl)),ls='--',label='classical width'); ax[5].legend(frameon=False); ax[5].set(xlabel='mean photon occupation',ylabel='electron rms order'); safe_title(ax[5],'Bandwidth-state crossover'); safe_panel(ax[5],'f')
for a in ax: clean(a)
finish_pub(fig,OUT)
