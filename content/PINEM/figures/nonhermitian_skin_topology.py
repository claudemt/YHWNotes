import common
from pathlib import Path
import sys, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import matplotlib.pyplot as plt
from scipy.linalg import eig
from preamble import pubfig,safe_panel,safe_title,clean,finish_pub

OUT=Path(__file__).with_suffix('.pdf')

def hatano_nelson_obc(n=56,t=1.0,eta=0.65):
    tr=t*np.exp(eta); tl=t*np.exp(-eta)
    H=np.zeros((n,n),complex)
    for j in range(n-1):
        H[j+1,j]=tr
        H[j,j+1]=tl
    return H,tr,tl

def hatano_nelson_pbc(n=140,t=1.0,eta=0.65):
    H,tr,tl=hatano_nelson_obc(n,t,eta)
    H[0,-1]=tr; H[-1,0]=tl
    return H,tr,tl

def spectrum_and_modes(H):
    ev,VR=eig(H)
    eL,VL=eig(H.conj().T)
    order=np.argsort(ev.real)
    ev=ev[order]; VR=VR[:,order]
    # match left eigenvectors by nearest eigenvalue
    matched=[]
    remaining=list(range(len(eL)))
    for z in ev:
        j=min(remaining,key=lambda q: abs(eL[q].conjugate()-z))
        matched.append(j); remaining.remove(j)
    VL=VL[:,matched]
    return ev,VR,VL

def mode_center(V):
    n=V.shape[0]; x=np.arange(n)
    p=np.abs(V)**2; p/=p.sum(axis=0,keepdims=True)
    return (x[:,None]*p).sum(axis=0)

def ipr(V):
    p=np.abs(V)**2; p/=p.sum(axis=0,keepdims=True)
    return (p*p).sum(axis=0)

eta0=0.65; n=56; t=1.0
Hp,tr,tl=hatano_nelson_pbc(220,t,eta0)
Ho,_,_=hatano_nelson_obc(n,t,eta0)
ep,VP,_=spectrum_and_modes(Hp)
eo,VO,VL=spectrum_and_modes(Ho)
cent=mode_center(VO)
site=np.arange(n)
mid=np.argmin(np.abs(eo.real))
pR=np.abs(VO[:,mid])**2; pR/=pR.sum()
pL=np.abs(VL[:,mid])**2; pL/=pL.sum()

# heatmap of right-eigenstate intensities sorted by Re E
heat=(np.abs(VO)**2)
heat/=heat.sum(axis=0,keepdims=True)

etas=np.linspace(0,1.0,61)
mean_shift=[]; avg_ipr=[]; xi_num=[]; xi_th=[]
for e in etas:
    H,_,_=hatano_nelson_obc(n,t,e)
    ev,V,_=spectrum_and_modes(H)
    c=mode_center(V)/(n-1)
    mean_shift.append(np.mean(c))
    avg_ipr.append(np.mean(ipr(V)))
    pm=np.abs(V[:,np.argmin(np.abs(ev.real))])**2
    pm/=pm.sum()
    x=site[:n//2]
    y=np.log(np.maximum(pm[:n//2],1e-14))
    a,b=np.polyfit(x,y,1)
    xi_num.append(-2.0/a if a<0 else np.nan)
    xi_th.append(1.0/max(e,1e-9))
mean_shift=np.array(mean_shift); avg_ipr=np.array(avg_ipr); xi_num=np.array(xi_num); xi_th=np.array(xi_th)

# generalized Brillouin zone
th=np.linspace(0,2*np.pi,400)
r=np.sqrt(tr/tl)

fig=pubfig(8.45,6.1,top=.92,left=.075,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.5,hspace=.60)
axs=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]

# a PBC spectrum
kloop=np.linspace(-np.pi,np.pi,500)
Eloop=tr*np.exp(-1j*kloop)+tl*np.exp(1j*kloop)
axs[0].plot(Eloop.real,Eloop.imag,lw=1.35)
axs[0].scatter(ep.real[::5],ep.imag[::5],s=5,alpha=.45)
axs[0].set(xlabel='Re E',ylabel='Im E')
safe_panel(axs[0],'a'); safe_title(axs[0],'Periodic-boundary complex spectrum')

# b OBC spectrum
axs[1].scatter(eo.real,eo.imag,s=8)
axs[1].set(xlabel='Re E',ylabel='Im E')
axs[1].set_xlim(-2.3,2.3)
axs[1].set_ylim(-0.15,0.15)
safe_panel(axs[1],'b'); safe_title(axs[1],'Open-boundary spectrum')

# c GBZ
axs[2].plot(np.cos(th),np.sin(th),ls='--',lw=.8,color='0.5',label=r'$|\beta|=1$')
axs[2].plot(r*np.cos(th),r*np.sin(th),lw=1.2,label='generalized zone')
axs[2].set(xlabel=r'$\operatorname{Re}\beta$',ylabel=r'$\operatorname{Im}\beta$')
axs[2].set_aspect('equal','box')
axs[2].legend(frameon=False,fontsize=6.6,loc='upper right')
safe_panel(axs[2],'c'); safe_title(axs[2],'Generalized Brillouin zone')

# d localization heatmap
im=axs[3].imshow(heat.T,origin='lower',aspect='auto',extent=[0,n-1,0,len(eo)-1],cmap='magma')
axs[3].set(xlabel='site index',ylabel='mode index')
safe_panel(axs[3],'d'); safe_title(axs[3],'Right-eigenmode skin accumulation')
fig.colorbar(im,ax=axs[3],fraction=.05,pad=.02).set_label('prob.')

# e scan versus eta
axs[4].plot(etas,mean_shift,label='right-mode mean position')
axs[4].plot(etas,avg_ipr/avg_ipr.max(),label='mean IPR / max')
axs[4].set(xlabel=r'nonreciprocity $\eta$',ylabel='normalized response')
axs[4].legend(frameon=False,fontsize=6.6,loc='lower right')
safe_panel(axs[4],'e'); safe_title(axs[4],'Skin localization vs. nonreciprocity')

# f left/right profiles and decay length
axs[5].plot(site,pR,label='right mode')
axs[5].plot(site,pL,label='left mode')
axs[5].set(xlabel='site index',ylabel='probability')
axs[5].legend(frameon=False,fontsize=6.3,loc='upper right')
axs[5].text(0.06,0.83,fr'$\xi_{{\mathrm{{amp}}}}=1/\eta={1/eta0:.2f}$',transform=axs[5].transAxes,fontsize=7.0,va='top')
safe_panel(axs[5],'f'); safe_title(axs[5],'Opposite-edge left and right modes')

for a in axs:
    clean(a)
finish_pub(fig,OUT)
