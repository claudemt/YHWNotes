import common  # shared style + embedded model helpers
common._norm_fs = lambda value, role='body': value
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
from models.feist2015 import free_evolution_density, wigner_periodic, sideband_coefficients

OUT=Path(__file__).with_suffix('.pdf')

g=3.8
disp=0.03
t_focus=12.0
t_revival=24.0

def contrast_of(rho):
    return (rho.max()-rho.min())/(rho.max()+rho.min()+1e-15)

fig=pubfig(8.5,6.0,top=.92,left=.07,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.54,hspace=.62)

# a,b: periodic Wigner cylinders before and near focus
for j,(tau,title,panel_id) in enumerate([
    (0.0,'Initial energy--phase state','a'),
    (t_focus,'Focused attosecond phase-space packet','b')
]):
    ax=fig.add_subplot(gs[0,j])
    theta,n,W=wigner_periodic(g,tau,dispersion=disp,nmax=18,ntheta=320)
    im=ax.imshow(W,origin='lower',aspect='auto',extent=[theta[0],theta[-1],n[0]-0.5,n[-1]+0.5],
                 cmap='RdBu_r',vmin=-1,vmax=1)
    ax.contour(theta,n,W,levels=[-0.5,0.5],colors=['#2b6ea6','#b44b39'],linewidths=0.55,alpha=0.8)
    ax.set_xlabel(r'Optical phase $\theta$',fontsize=9.5)
    if j==0:
        ax.set_ylabel('Electron order $n$',fontsize=9.5)
    ax.tick_params(labelsize=8.2)
    safe_panel(ax,panel_id)
    safe_title(ax,title)
    cb=safe_colorbar(fig,im,ax,'Wigner proxy',pad=.017)
    cb.ax.tick_params(labelsize=7.2,pad=1)

# c: density evolution map
ax=fig.add_subplot(gs[0,2])
taus=np.linspace(0,34,190)
theta=np.linspace(-np.pi,np.pi,440)
D=[]
for tau in taus:
    th,rho=free_evolution_density(g,tau,dispersion=disp,nmax=22,nt=len(theta))
    D.append(rho)
D=np.array(D)
im=ax.imshow(D,origin='lower',aspect='auto',extent=[th[0],th[-1],taus[0],taus[-1]],
             cmap='magma',vmax=np.percentile(D,99.7))
for tt in [0,t_focus,t_revival]:
    ax.axhline(tt,color='white',ls='--',lw=0.75,alpha=0.9)
ax.set_xlabel(r'Optical phase $\theta$',fontsize=9.5)
ax.set_ylabel('Propagation parameter',fontsize=9.5)
ax.tick_params(labelsize=8.2)
safe_panel(ax,'c')
safe_title(ax,'Temporal caustics and pulse-train formation')
cb=safe_colorbar(fig,im,ax,'density',pad=.017)
cb.ax.tick_params(labelsize=7.2,pad=1)

# d: waveform snapshots at selected propagation distances
ax=fig.add_subplot(gs[1,0])
for tau,lab,alpha in [(0,r'$\tau=0$',0.9),(t_focus,fr'$\tau={t_focus:g}$',1.0),(t_revival,fr'$\tau={t_revival:g}$',0.95)]:
    th,rho=free_evolution_density(g,tau,dispersion=disp,nmax=22,nt=700)
    rho=rho/rho.max()
    ax.plot(th,rho,label=lab,alpha=alpha)
ax.set_xlabel(r'Optical phase $\theta$',fontsize=9.5)
ax.set_ylabel('Normalized density',fontsize=9.5)
ax.set_ylim(-0.02,1.05)
ax.legend(frameon=False,fontsize=7.2,loc='upper right')
ax.tick_params(labelsize=8.2)
safe_panel(ax,'d')
safe_title(ax,'Waveform sharpening and partial revival')
clean(ax)

# e: harmonic bunching factors
ax=fig.add_subplot(gs[1,1])
orders=[1,2,3,4]
for q in orders:
    B=[]
    for row in D:
        B.append(abs(np.trapz(row*np.exp(1j*q*theta),theta)))
    B=np.asarray(B)
    ax.plot(taus,B,label=fr'$q={q}$')
ax.set_xlabel('Propagation parameter',fontsize=9.5)
ax.set_ylabel(r'$|\langle e^{\mathrm{i}q\theta}\rangle|$',fontsize=9.5)
ax.legend(frameon=False,ncol=2,fontsize=7.0,loc='upper right')
ax.tick_params(labelsize=8.2)
safe_panel(ax,'e')
safe_title(ax,'Growth of harmonic bunching')
clean(ax)

# f: peak density and temporal contrast
ax=fig.add_subplot(gs[1,2])
peak=D.max(axis=1)
contrast=np.array([contrast_of(rho) for rho in D])
peak=peak/peak[0]
ax.plot(taus,peak,label='peak compression')
ax.plot(taus,contrast,label='temporal contrast')
ax.axvline(t_focus,color='0.35',ls=':',lw=0.9)
ax.axvline(t_revival,color='0.35',ls=':',lw=0.9)
ax.set_xlabel('Propagation parameter',fontsize=9.5)
ax.set_ylabel('Dimensionless response',fontsize=9.5)
ax.legend(frameon=False,fontsize=7.0,loc='upper right')
ax.tick_params(labelsize=8.2)
safe_panel(ax,'f')
safe_title(ax,'Compression metrics along propagation')
clean(ax)

finish_pub(fig,OUT)
