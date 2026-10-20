import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
from models.li2026 import joint_distribution,dispersion,dos,mode_entropy
from models.novel_extensions import lifshitz_quench

OUT=Path(__file__).with_suffix('.pdf')
fig=pubfig(8.4,6.15,top=.92,left=.07,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.44,hspace=.60)

# a: joint synthetic lattice shown as weighted sites on the geometric lattice
P=joint_distribution(2.0,2.0,-1,-1,18)
Ns=sorted(set(k[0] for k in P)); Ls=sorted(set(k[1] for k in P))
ax=fig.add_subplot(gs[0,0])
for n1 in range(-12,13):
    pts=np.array([[n1+2*n2, -n1-n2] for n2 in range(-12,13)])
    ax.plot(pts[:,0],pts[:,1],lw=0.38,color='#cad2cf',zorder=0)
for n2 in range(-12,13):
    pts=np.array([[n1+2*n2, -n1-n2] for n1 in range(-12,13)])
    ax.plot(pts[:,0],pts[:,1],lw=0.38,color='#cad2cf',zorder=0)
xy=np.array([[N,L] for (N,L) in P])
val=np.array([P[k] for k in P])
sc=ax.scatter(xy[:,0],xy[:,1],c=val,s=14+760*val/val.max(),cmap='magma',edgecolor='0.15',linewidth=0.25,zorder=3)
ax.arrow(0,0,1,-1,width=.035,length_includes_head=True,head_width=.38,color='#e67e22',zorder=4)
ax.arrow(0,0,2,-1,width=.035,length_includes_head=True,head_width=.38,color='#2ca089',zorder=4)
ax.text(.96,.96,r'$\boldsymbol{v}_1=(1,-1)$',fontsize=8.1,transform=ax.transAxes,ha='right',va='top',bbox=dict(fc='white',ec='none',alpha=.87,pad=1))
ax.text(.96,.86,r'$\boldsymbol{v}_2=(2,-1)$',fontsize=8.1,transform=ax.transAxes,ha='right',va='top',bbox=dict(fc='white',ec='none',alpha=.87,pad=1))
ax.set(xlabel='Energy index $N$',ylabel=r'OAM index $\ell$',xlim=(-20,20),ylim=(-15,15))
ax.tick_params(labelsize=8.0)
safe_panel(ax,'a')
safe_title(ax,'Energy--OAM lattice')
cb=safe_colorbar(fig,sc,ax,'probability',pad=.015)
cb.ax.tick_params(labelsize=7.0,pad=1)
clean(ax)

# b: Schmidt spectrum / nonseparability
ax=fig.add_subplot(gs[0,1])
S,s=mode_entropy(2,2,-1,-1,20)
keep=min(12,len(s))
ax.bar(np.arange(1,keep+1),s[:keep],width=0.78)
ax.text(.98,.96,fr'$S={S:.3f}\,\mathrm{{bits}}$',transform=ax.transAxes,ha='right',va='top',fontsize=8.0)
ax.text(.98,.85,fr'$K_\mathrm{{eff}}={1/np.sum(s*s):.2f}$',transform=ax.transAxes,ha='right',va='top',fontsize=8.0)
ax.set(xlabel='Schmidt mode',ylabel='Weight')
ax.tick_params(labelsize=8.0)
safe_panel(ax,'b')
safe_title(ax,'Mode-weight spectrum')
clean(ax)

# c: 3D band surface with zero contour projected
k=np.linspace(-np.pi,np.pi,180)
KN,KL=np.meshgrid(k,k)
E=dispersion(KN,KL,1,1,-1,-1)
ax=fig.add_subplot(gs[0,2],projection='3d')
step=3
ax.plot_surface(KN[::step,::step],KL[::step,::step],E[::step,::step],cmap='coolwarm',edgecolor='none',alpha=.92)
ax.contour(KN,KL,E,levels=[0],zdir='z',offset=E.min()-0.55,colors=['k'],linewidths=1.2)
ax.set_xlabel(r'$K_N$',labelpad=-2)
ax.set_ylabel(r'$K_\ell$',labelpad=-2)
ax.set_zlabel(r'$\varepsilon$',labelpad=-1)
ax.set_xlim(-np.pi,np.pi); ax.set_ylim(-np.pi,np.pi); ax.set_zlim(E.min()-0.55,E.max())
ax.view_init(elev=28,azim=-60)
ax.tick_params(labelsize=7.0,pad=0)
ax.xaxis.pane.set_alpha(0.0); ax.yaxis.pane.set_alpha(0.0); ax.zaxis.pane.set_alpha(0.0)
safe_panel(ax,'c')
safe_title(ax,'Synthetic-band dispersion')

# d: zero-energy contours across the Lifshitz tuning
ax=fig.add_subplot(gs[1,0])
colors=['#2d71a4','#22a884','#be6235']
for ratio,color in zip([1/3,1,3],colors):
    eps=dispersion(KN,KL,1,ratio,-1,-1)
    ax.contour(KN,KL,eps,levels=[0],colors=[color],linewidths=1.45)
ax.set(xlabel=r'$K_N$',ylabel=r'$K_\ell$',xlim=(-np.pi,np.pi),ylim=(-np.pi,np.pi),aspect='equal')
ax.set_xticks([-np.pi,0,np.pi]); ax.set_xticklabels([r'$-\pi$','0',r'$\pi$'])
ax.set_yticks([-np.pi,0,np.pi]); ax.set_yticklabels([r'$-\pi$','0',r'$\pi$'])
ax.text(.02,.97,r'$|\beta_{2\omega}/\beta_\omega|=1/3$',transform=ax.transAxes,ha='left',va='top',fontsize=6.9,color=colors[0])
ax.text(.02,.88,r'$|\beta_{2\omega}/\beta_\omega|=1$',transform=ax.transAxes,ha='left',va='top',fontsize=6.9,color=colors[1])
ax.text(.02,.79,r'$|\beta_{2\omega}/\beta_\omega|=3$',transform=ax.transAxes,ha='left',va='top',fontsize=6.9,color=colors[2])
ax.tick_params(labelsize=8.0)
safe_panel(ax,'d')
safe_title(ax,'Lifshitz contour reconnection')
clean(ax)

# e: DOS across the same tuning
ax=fig.add_subplot(gs[1,1])
for ratio,color in zip([1/3,1,3],colors):
    en,d=dos(1,ratio,-1,-1,n=360,bins=250)
    ax.plot(en,d,lw=1.35,color=color,label=fr'$|\beta_2/\beta_1|={ratio:g}$')
ax.set(xlabel='Quasienergy',ylabel='DOS')
ax.legend(frameon=False,fontsize=7.0,loc='upper right')
ax.tick_params(labelsize=8.0)
safe_panel(ax,'e')
safe_title(ax,'Density-of-states peaks')
clean(ax)

# f: quantitative ballistic spreading, calculated by unitary FFT at every
# time step. The original four image snapshots were almost entirely black.
ax=fig.add_subplot(gs[1,2])
_,E,_,_,_,_=lifshitz_quench(b1=1.0,b2=3.0,l1=-1,l2=-1,nk=120,sigma_k=0.55)
nk=E.shape[0]
sites=np.arange(nk)-nk//2
NN,LL=np.meshgrid(sites,sites,indexing='ij')
tgrid=np.linspace(0,3,91)
sN=[];sL=[]
for t in tgrid:
    psi=np.fft.fftshift(np.fft.ifft2(np.exp(-1j*E*t)))
    prob=np.abs(psi)**2;prob/=prob.sum()
    mn=(prob*NN).sum();ml=(prob*LL).sum()
    sN.append(np.sqrt((prob*(NN-mn)**2).sum()))
    sL.append(np.sqrt((prob*(LL-ml)**2).sum()))
ax.plot(tgrid,sN,color='#2677a8',label=r'$\sigma_N(t)$')
ax.plot(tgrid,sL,color='#c77641',label=r'$\sigma_\ell(t)$')
ax.set(xlabel='evolution parameter $t$',ylabel='RMS site width',xlim=(0,3))
ax.legend(loc='upper left',frameon=False)
safe_panel(ax,'f');safe_title(ax,'Ballistic wavepacket spreading')
clean(ax)
print('quench widths at 3',sN[-1],sL[-1])

finish_pub(fig,OUT)
