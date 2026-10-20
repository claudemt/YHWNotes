import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
OUT=Path(__file__).with_suffix('.pdf')
n,Pf,Pd,E=ne.two_electron_exchange_map(2.0,2,12); gs,ss,V=ne.two_electron_visibility_scan()
fig=pubfig(9.0,6.2,top=.92,left=.07,right=.97,bottom=.08); grid=fig.add_gridspec(2,3,wspace=.58,hspace=.60); ax=[fig.add_subplot(grid[i//3,i%3]) for i in range(6)]
for a,M,title in [(ax[0],Pd,'Distinguishable electrons'),(ax[1],Pf,'Identical fermions')]:
 im=a.imshow(M,origin='lower',extent=[n[0]-.5,n[-1]+.5,n[0]-.5,n[-1]+.5],cmap='magma',vmin=0,vmax=max(Pd.max(),Pf.max())); safe_colorbar(fig,im,a,'coincidence'); a.set(xlabel='electron 1 order',ylabel='electron 2 order'); safe_title(a,title)
safe_panel(ax[0],'a'); safe_panel(ax[1],'b')
im=ax[2].imshow(E,origin='lower',extent=[n[0]-.5,n[-1]+.5,n[0]-.5,n[-1]+.5],cmap='RdBu_r',vmin=-np.max(abs(E)),vmax=np.max(abs(E))); safe_colorbar(fig,im,ax[2],'fermionic correction'); ax[2].set(xlabel='order n1',ylabel='order n2'); safe_title(ax[2],'Exchange hole and redistribution'); safe_panel(ax[2],'c')
for i,s in enumerate(ss): ax[3].plot(gs,V[i],label=f'separation {s}')
ax[3].legend(frameon=False); ax[3].set(xlabel='PINEM coupling g',ylabel='total variation vs distinguishable'); safe_title(ax[3],'Exchange visibility'); safe_panel(ax[3],'d')
diag_f=np.diag(Pf); diag_d=np.diag(Pd); ax[4].plot(n,diag_d,'o-',label='distinguishable'); ax[4].plot(n,diag_f,'s--',label='fermions'); ax[4].legend(frameon=False); ax[4].set(xlabel='equal output order n',ylabel='P(n,n)'); safe_title(ax[4],'Pauli suppression'); safe_panel(ax[4],'e')
# anticorrelation observable
N1,N2=np.meshgrid(n,n,indexing='ij'); covf=np.sum(N1*N2*Pf)-np.sum(N1*Pf)*np.sum(N2*Pf); covd=np.sum(N1*N2*Pd)-np.sum(N1*Pd)*np.sum(N2*Pd)
ax[5].bar(['distinguishable','fermions'],[covd,covf]); ax[5].set(ylabel='energy-bin covariance'); safe_title(ax[5],'Exchange-modified correlations'); safe_panel(ax[5],'f')
for a in ax: clean(a)
finish_pub(fig,OUT)
