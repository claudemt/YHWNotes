"""Two-fermion correlation benchmark with richer visual diagnostics."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from common import pubfig, safe_panel, safe_title, safe_colorbar, clean, finish_pub

OUT=Path(__file__).with_suffix('.pdf')
fig=pubfig(8.35,6.0,top=.92,left=.07,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.46,hspace=.62)
axs=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]

x=np.linspace(-4.5,4.5,320)
X1,X2=np.meshgrid(x,x,indexing='xy')
d=1.40

def orbital(z,origin):
    return np.pi**(-0.25)*np.exp(-0.5*(z-origin)**2)
A1=orbital(X1,d/2); B1=orbital(X1,-d/2)
A2=orbital(X2,d/2); B2=orbital(X2,-d/2)
S=np.exp(-d*d/4)
Pd=0.5*(A1*A1*B2*B2 + B1*B1*A2*A2)
Pf=(A1*B2 - B1*A2)**2/(2*(1-S*S))
dx=x[1]-x[0]
Pd/=np.sum(Pd)*dx*dx
Pf/=np.sum(Pf)*dx*dx
extent=[x[0],x[-1],x[0],x[-1]]

# marginals / correlations
p1=np.trapezoid(Pf,x,axis=1)
p2=np.trapezoid(Pf,x,axis=0)
prod=np.outer(p1,p2)
C=Pf-prod
M=Pf-Pd

# a: distinguishable benchmark
im=axs[0].imshow(Pd,origin='lower',extent=extent,aspect='equal',cmap='magma',vmin=0,vmax=max(Pd.max(),Pf.max()))
axs[0].set(xlabel=r'$x_1/\sigma$',ylabel=r'$x_2/\sigma$')
safe_panel(axs[0],'a'); safe_title(axs[0],'Distinguishable reference')
safe_colorbar(fig,im,axs[0],'joint density',pad=.015)

# b: fermionic joint density
im=axs[1].imshow(Pf,origin='lower',extent=extent,aspect='equal',cmap='magma',vmin=0,vmax=max(Pd.max(),Pf.max()))
axs[1].plot(x,x,color='w',lw=.75,ls='--',alpha=.7)
axs[1].set(xlabel=r'$x_1/\sigma$',ylabel=r'$x_2/\sigma$')
safe_panel(axs[1],'b'); safe_title(axs[1],'Antisymmetric fermions')
safe_colorbar(fig,im,axs[1],'joint density',pad=.015)

# c: exchange-only correction
vm=max(abs(M.min()),abs(M.max()))
im=axs[2].imshow(M,origin='lower',extent=extent,aspect='equal',cmap='RdBu_r',vmin=-vm,vmax=vm)
axs[2].plot(x,x,color='k',lw=.55,ls=':')
axs[2].set(xlabel=r'$x_1/\sigma$',ylabel=r'$x_2/\sigma$')
safe_panel(axs[2],'c'); safe_title(axs[2],'Exchange correction $P_F-P_D$')
safe_colorbar(fig,im,axs[2],'difference',pad=.015)

# d: center-of-mass / relative-coordinate map
Xcm=np.linspace(-3.5,3.5,240)
R=np.linspace(-6.0,6.0,280)
XX,RR=np.meshgrid(Xcm,R,indexing='xy')
Z1=XX+RR/2
Z2=XX-RR/2
A=orbital(Z1,d/2); B=orbital(Z1,-d/2); Cc=orbital(Z2,d/2); Dd=orbital(Z2,-d/2)
Pcm=(A*Dd-B*Cc)**2/(2*(1-S*S))
im=axs[3].imshow(Pcm,origin='lower',aspect='auto',extent=[Xcm[0],Xcm[-1],R[0],R[-1]],cmap='viridis')
axs[3].axhline(0,color='w',lw=.8,ls='--',alpha=.75)
axs[3].set(xlabel=r'center coordinate $(x_1+x_2)/(2\sigma)$',ylabel=r'relative coordinate $(x_1-x_2)/\sigma$')
safe_panel(axs[3],'d'); safe_title(axs[3],'Relative-coordinate exchange hole')
safe_colorbar(fig,im,axs[3],'density',pad=.015)

# e: same-bin coincidence slice + connected correlator cut
axs[4].plot(x,np.diag(Pd),label='distinguishable $P_D(x,x)$')
axs[4].plot(x,np.diag(Pf),label='fermionic $P_F(x,x)$',ls='--')
axs[4].plot(x,np.diag(C),label='connected $C(x,x)$',lw=1.0)
axs[4].set(xlabel=r'position $x/\sigma$',ylabel='same-bin signal')
axs[4].legend(frameon=False,fontsize=6.7,loc='upper center')
safe_panel(axs[4],'e'); safe_title(axs[4],'Pauli suppression on the diagonal')

# f: antibunching visibility vs orbital separation and detector window
axs[5].set_prop_cycle(None)
dscan=np.linspace(0.15,4.0,220)
for eps in [0.2,0.5,1.0]:
    vis=[]
    for dd in dscan:
        S=np.exp(-dd*dd/4)
        A1=orbital(X1,dd/2); B1=orbital(X1,-dd/2)
        A2=orbital(X2,dd/2); B2=orbital(X2,-dd/2)
        Pd_loc=0.5*(A1*A1*B2*B2 + B1*B1*A2*A2)
        Pf_loc=(A1*B2 - B1*A2)**2/(2*(1-S*S+1e-15))
        Pd_loc/=np.sum(Pd_loc)*dx*dx; Pf_loc/=np.sum(Pf_loc)*dx*dx
        mask=np.abs(X1-X2)<eps
        cd=np.sum(Pd_loc[mask])*dx*dx
        cf=np.sum(Pf_loc[mask])*dx*dx
        vis.append(1-cf/(cd+1e-15))
    axs[5].plot(dscan,vis,label=fr'$|x_1-x_2|<{eps}\sigma$')
axs[5].set(xlabel=r'orbital separation $d/\sigma$',ylabel='antibunching visibility')
axs[5].legend(frameon=False,fontsize=7.0)
safe_panel(axs[5],'f'); safe_title(axs[5],'Finite-window antibunching')

for ax in axs: clean(ax)
finish_pub(fig,OUT)
