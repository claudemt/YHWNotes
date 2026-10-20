import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from scipy.stats import poisson
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
OUT=Path(__file__).with_suffix('.pdf')
N=np.arange(19); true=poisson.pmf(N,6.2); true/=true.sum(); ns,N,K,p,y,wh,c=ne.invert_photon_statistics(true,max_input=18,ne=7,nph=30,pulse_area=.42,counts=18000,seed=4,reg=1e-3)
fig=pubfig(9.0,6.2,top=.92,left=.07,right=.97,bottom=.08); gs=fig.add_gridspec(2,3,wspace=.58,hspace=.60); ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
im=ax[0].imshow(K,origin='lower',aspect='auto',extent=[N[0]-.5,N[-1]+.5,ns[0]-.5,ns[-1]+.5],cmap='viridis'); safe_colorbar(fig,im,ax[0],'P(n|Nph)'); ax[0].set(xlabel='input photon number',ylabel='electron order'); safe_title(ax[0],'Quantum PINEM response matrix'); safe_panel(ax[0],'a')
ax[1].bar(ns,y,width=.8,label='measured'); ax[1].plot(ns,p,'o-',ms=3,label='noise-free'); ax[1].legend(frameon=False); ax[1].set(xlabel='electron order n',ylabel='probability'); safe_title(ax[1],'Electron-only measurement'); safe_panel(ax[1],'b')
ax[2].plot(N,true,'o-',label='true photon statistics'); ax[2].plot(N,wh,'s--',label='reconstructed'); ax[2].legend(frameon=False); ax[2].set(xlabel='photon number',ylabel='probability'); safe_title(ax[2],'Photon-number reconstruction'); safe_panel(ax[2],'c')
counts_grid=np.unique(np.logspace(2.5,5,18).astype(int)); err=[]
for cc in counts_grid:
 *_,wh2,c2=ne.invert_photon_statistics(true,max_input=18,ne=7,nph=30,pulse_area=.42,counts=int(cc),seed=3,reg=1e-3); err.append(.5*np.sum(abs(wh2-true)))
ax[3].loglog(counts_grid,err,'o-'); ax[3].set(xlabel='detected electrons',ylabel='TV reconstruction error'); safe_title(ax[3],'Shot-noise scaling'); safe_panel(ax[3],'d')
areas=np.linspace(.08,.75,30); cond=[]
for a in areas:
 _,_,KK=ne.photon_statistics_response(18,7,30,a); s=np.linalg.svd(KK,compute_uv=False); cond.append(s[0]/max(s[-1],1e-12))
ax[4].semilogy(areas,cond); ax[4].set(xlabel='interaction pulse area',ylabel='response condition number'); safe_title(ax[4],'Identifiability window'); safe_panel(ax[4],'e')
resid=y-K@wh; ax[5].bar(ns,resid,width=.8); ax[5].axhline(0,lw=.7); ax[5].set(xlabel='electron order',ylabel='data-model residual'); safe_title(ax[5],'Forward-model residual'); safe_panel(ax[5],'f')
for a in ax: clean(a)
finish_pub(fig,OUT)
