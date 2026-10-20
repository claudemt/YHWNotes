import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
OUT=Path(__file__).with_suffix('.pdf')
x,y,beta,meas,bhat,err=ne.complex_beta_tomography(nx=72,ny=72,counts=30000,seed=9); extent=[x[0],x[-1],y[0],y[-1]]
fig=pubfig(9.2,6.2,top=.92,left=.065,right=.97,bottom=.08); gs=fig.add_gridspec(2,3,wspace=.58,hspace=.60); ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
im=ax[0].imshow(abs(beta),origin='lower',extent=extent,cmap='magma'); safe_colorbar(fig,im,ax[0],'|beta|'); ax[0].set(xlabel='x',ylabel='y'); safe_title(ax[0],'True coupling amplitude'); safe_panel(ax[0],'a')
im=ax[1].imshow(np.angle(beta),origin='lower',extent=extent,cmap='twilight',vmin=-np.pi,vmax=np.pi); safe_colorbar(fig,im,ax[1],'phase [rad]'); ax[1].set(xlabel='x',ylabel='y'); safe_title(ax[1],'True coupling phase'); safe_panel(ax[1],'b')
im=ax[2].imshow(meas[0],origin='lower',extent=extent,cmap='viridis'); safe_colorbar(fig,im,ax[2],'P(+1)'); ax[2].set(xlabel='x',ylabel='y'); safe_title(ax[2],'One interferometric measurement'); safe_panel(ax[2],'c')
im=ax[3].imshow(abs(bhat),origin='lower',extent=extent,cmap='magma',vmin=0,vmax=abs(beta).max()); safe_colorbar(fig,im,ax[3],'|beta_hat|'); ax[3].set(xlabel='x',ylabel='y'); safe_title(ax[3],'Reconstructed amplitude'); safe_panel(ax[3],'d')
im=ax[4].imshow(np.angle(bhat),origin='lower',extent=extent,cmap='twilight',vmin=-np.pi,vmax=np.pi); safe_colorbar(fig,im,ax[4],'phase [rad]'); ax[4].set(xlabel='x',ylabel='y'); safe_title(ax[4],'Reconstructed phase'); safe_panel(ax[4],'e')
mask=abs(beta)>.06; ax[5].scatter(beta.real[mask][::8],bhat.real[mask][::8],s=4,alpha=.4,label='Re beta'); ax[5].scatter(beta.imag[mask][::8],bhat.imag[mask][::8],s=4,alpha=.4,label='Im beta'); lim=.45; ax[5].plot([-lim,lim],[-lim,lim],'k--',lw=.8); ax[5].legend(frameon=False); ax[5].set(xlabel='true component',ylabel='reconstructed component'); safe_title(ax[5],'Complex-field fidelity'); safe_panel(ax[5],'f')
for a in ax: clean(a)
finish_pub(fig,OUT)
