import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from scipy.special import jv
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub

OUT=Path(__file__).with_suffix('.pdf')
fig=pubfig(8.4,6.0,top=.92,left=.07,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.47,hspace=.62)

# Shared parameters
m0=5
kp=1.0
eta_show=3.0
R=np.linspace(0,18,600)
XY=np.linspace(-14,14,320)
X,Y=np.meshgrid(XY,XY)
RR=np.hypot(X,Y)
PH=np.arctan2(Y,X)
field=jv(m0,kp*RR)*np.exp(1j*m0*PH)

# a: plasmon-vortex near-field intensity
ax=fig.add_subplot(gs[0,0])
im=ax.imshow(np.abs(field)**2,origin='lower',extent=[XY[0],XY[-1],XY[0],XY[-1]],cmap='inferno')
ax.set(xlabel=r'$k_px$',ylabel=r'$k_py$')
safe_panel(ax,'a')
safe_title(ax,fr'Plasmon vortex intensity ($m={m0}$)')
safe_colorbar(fig,im,ax,'intensity',pad=.015)
clean(ax)

# b: near-field phase winding
ax=fig.add_subplot(gs[0,1])
phase=np.angle(field)
im=ax.imshow(phase,origin='lower',extent=[XY[0],XY[-1],XY[0],XY[-1]],cmap='twilight',vmin=-np.pi,vmax=np.pi)
ax.contour(X,Y,np.abs(field)**2,levels=np.linspace(np.max(np.abs(field)**2)*0.1,np.max(np.abs(field)**2)*0.8,5),colors='w',linewidths=0.35,alpha=0.35)
ax.set(xlabel=r'$k_px$',ylabel=r'$k_py$')
safe_panel(ax,'b')
safe_title(ax,'Vortex phase')
safe_colorbar(fig,im,ax,'phase',pad=.015)
clean(ax)

# c: radial coupling envelopes
ax=fig.add_subplot(gs[0,2])
for m in [1,5,10]:
    ax.plot(R,jv(m,kp*R)**2,label=fr'$m={m}$')
ax.set(xlabel=r'$k_pR$',ylabel=r'$|J_m(k_pR)|^2$')
ax.legend(frameon=False,fontsize=7.1)
safe_panel(ax,'c')
safe_title(ax,'Radial coupling rings')
clean(ax)

# d: velocity matching efficiency
ax=fig.add_subplot(gs[1,0])
xi=np.logspace(-2,2,450)
eta_rel=2*xi/(1+xi**2)
ax.semilogx(xi,eta_rel)
ax.axvline(1,ls='--',lw=.75,color='0.35')
ax.text(.98,.94,'matched',transform=ax.transAxes,ha='right',va='top',fontsize=7.2)
ax.set(xlabel=r'$\xi=\omega_p\lambda_p/(2\pi v)$',ylabel=r'$\eta/g$')
safe_panel(ax,'d')
safe_title(ax,'Velocity matching')
clean(ax)

# e: joint energy--OAM channel fan vs coupling
ax=fig.add_subplot(gs[1,1])
eta_grid=np.linspace(0,8,280)
nvals=np.arange(-8,9)
R0=7.0
local=abs(jv(m0,kp*R0))
P=np.array([jv(n,2*eta_grid*local)**2 for n in nvals])
Lvals=nvals*m0
im=ax.imshow(P,origin='lower',aspect='auto',extent=[eta_grid.min(),eta_grid.max(),Lvals.min()-m0/2,Lvals.max()+m0/2],cmap='magma')
for n in nvals:
    ax.hlines(n*m0,eta_grid.min(),eta_grid.max(),color='w',lw=0.25,alpha=0.18)
ax.set(xlabel=r'coupling $\eta$',ylabel=r'orbital transfer $\Delta L_z/\hbar$')
safe_panel(ax,'e')
safe_title(ax,'Energy--OAM selection rule')
safe_colorbar(fig,im,ax,'population',pad=.015)
clean(ax)

# f: OAM bandwidth scaling with topological charge
ax=fig.add_subplot(gs[1,2])
eta_scan=np.linspace(0,8,240)
for m,color in zip([1,5,10],['#1f77b4','#2ca02c','#d62728']):
    local=abs(jv(m,kp*7.0))
    n=np.arange(-18,19)
    probs=np.array([jv(nn,2*eta_scan*local)**2 for nn in n])
    sigmaL=np.sqrt(np.sum((n[:,None]*m)**2*probs,axis=0))
    ax.plot(eta_scan,sigmaL,label=fr'$m={m}$')
ax.set(xlabel=r'coupling $\eta$',ylabel=r'$\sigma_{L_z}/\hbar$')
ax.legend(frameon=False,fontsize=7.2)
safe_panel(ax,'f')
safe_title(ax,'OAM bandwidth vs. vortex charge')
clean(ax)

finish_pub(fig,OUT)
