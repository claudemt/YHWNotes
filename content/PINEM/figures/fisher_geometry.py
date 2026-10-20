import common
from pathlib import Path
import sys, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import matplotlib.pyplot as plt
from preamble import pubfig, clean, safe_panel, safe_title, safe_colorbar, finish_pub
from models import novel_extensions as ne

OUT=Path(__file__).with_suffix('.pdf')

B2=1.8
L1,L2=-1,-2
SIG=.85
NMAX=9
DB=0.035
DP=0.045


def distribution(b1,phi):
    Ns,Ls,_,Q=ne.measured_joint_distribution(b1,B2,L1,L2,sigma_n=SIG,sigma_l=SIG,nmax=NMAX,phi2=phi)
    return Ns,Ls,Q

def fisher_matrix(b1,phi):
    Ns,Ls,q=distribution(b1,phi)
    _,_,qp=distribution(b1,phi+DP)
    _,_,qm=distribution(b1,phi-DP)
    _,_,bp=distribution(b1+DB,phi)
    _,_,bm=distribution(max(0.05,b1-DB),phi)
    dqphi=(qp-qm)/(2*DP)
    dqb=(bp-bm)/(2*DB)
    den=np.maximum(q,1e-14)
    F11=np.sum(dqb*dqb/den)
    F22=np.sum(dqphi*dqphi/den)
    F12=np.sum(dqb*dqphi/den)
    F=np.array([[F11,F12],[F12,F22]])
    return Ns,Ls,q,dqb,dqphi,F

def ellipse_from_cov(C,n=300):
    w,V=np.linalg.eigh(C)
    w=np.maximum(w,1e-12)
    u=np.linspace(0,2*np.pi,n)
    pts=V@np.diag(np.sqrt(w))@np.vstack([np.cos(u),np.sin(u)])
    pts/=np.sqrt(np.trace(C)+1e-12)  # compare shape/orientation rather than absolute scale
    return pts

bvals=np.linspace(0.45,3.0,26)
pvals=np.linspace(-np.pi,np.pi,29)
logdet=np.empty((len(pvals),len(bvals)))
lmin=np.empty_like(logdet)
phi_info=np.empty_like(logdet)
for ip,phi in enumerate(pvals):
    for ib,b in enumerate(bvals):
        _,_,q,dqb,dqphi,F=fisher_matrix(b,phi)
        ew=np.linalg.eigvalsh(F)
        lmin[ip,ib]=ew.min()
        logdet[ip,ib]=np.log10(max(np.linalg.det(F),1e-12))
        phi_info[ip,ib]=F[1,1]

# robust working point = maximize min eigenvalue
opt_idx=np.unravel_index(np.argmax(lmin),lmin.shape)
phi_star=pvals[opt_idx[0]]; b_star=bvals[opt_idx[1]]
Ns,Ls,qstar,dqb_star,dqphi_star,Fstar=fisher_matrix(b_star,phi_star)

# additional comparison working points
cands=[(0.75,phi_star),(b_star,phi_star),(2.6,0.0)]
ellipses=[]; labels=[]
for b,phi in cands:
    _,_,_,_,_,F=fisher_matrix(b,phi)
    C=np.linalg.inv(F+1e-9*np.eye(2))
    ellipses.append(ellipse_from_cov(C))
    labels.append(f'b1={b:.2f}, phi={phi:.2f}')

# cumulative information budgets at the optimal point
Ib=(dqb_star*dqb_star/np.maximum(qstar,1e-14)).ravel()
Ip=(dqphi_star*dqphi_star/np.maximum(qstar,1e-14)).ravel()
Ib=np.sort(Ib)[::-1]; Ip=np.sort(Ip)[::-1]
cb=np.cumsum(Ib)/Ib.sum(); cp=np.cumsum(Ip)/Ip.sum(); k=np.arange(1,len(cb)+1)

fig=pubfig(8.55,6.15,top=.92,left=.075,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.55,hspace=.62)
axs=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
ext=[bvals.min(),bvals.max(),pvals.min(),pvals.max()]
qext=[Ns.min()-.5,Ns.max()+.5,Ls.min()-.5,Ls.max()+.5]

# a response matrix at optimum
im=axs[0].imshow(qstar,origin='lower',extent=qext,aspect='auto',cmap='magma')
axs[0].set(xlabel='energy index N',ylabel='OAM index L')
safe_panel(axs[0],'a'); safe_title(axs[0],f'Joint response q(N,L) at robust optimum')
safe_colorbar(fig,im,axs[0],'probability',pad=.015)

# b local phase-information budget
Iphi=(dqphi_star*dqphi_star/np.maximum(qstar,1e-14))
im=axs[1].imshow(Iphi,origin='lower',extent=qext,aspect='auto',cmap='cividis')
axs[1].set(xlabel='energy index N',ylabel='OAM index L')
safe_panel(axs[1],'b'); safe_title(axs[1],'Channelwise phase-information budget')
safe_colorbar(fig,im,axs[1],r'$I_{NL}^{(\phi)}$',pad=.015)

# c error ellipses
for pts,lbl in zip(ellipses,labels):
    axs[2].plot(pts[0],pts[1],lw=1.2,label=lbl)
axs[2].axhline(0,lw=.6,color='0.5'); axs[2].axvline(0,lw=.6,color='0.5')
axs[2].set(xlabel=r'$\delta b_1$',ylabel=r'$\delta\phi$')
axs[2].legend(frameon=False,fontsize=5.9,loc='upper right')
axs[2].set_aspect('equal','box')
axs[2].set_xlim(-1.15,1.15); axs[2].set_ylim(-1.15,1.15)
safe_panel(axs[2],'c'); safe_title(axs[2],'Error ellipses (shape normalized)')

# d log det map
im=axs[3].imshow(logdet,origin='lower',extent=ext,aspect='auto',cmap='viridis')
axs[3].plot([b_star],[phi_star],marker='*',ms=9,mec='k',mfc='w')
axs[3].set(xlabel=r'coupling $b_1$',ylabel=r'relative phase $\phi$')
safe_panel(axs[3],'d'); safe_title(axs[3],'D-optimality map: log10 det F')
safe_colorbar(fig,im,axs[3],r'$\log_{10}\det F$',pad=.015)

# e min-eigenvalue map
im=axs[4].imshow(lmin,origin='lower',extent=ext,aspect='auto',cmap='plasma')
axs[4].plot([b_star],[phi_star],marker='*',ms=9,mec='k',mfc='w')
axs[4].set(xlabel=r'coupling $b_1$',ylabel=r'relative phase $\phi$')
safe_panel(axs[4],'e'); safe_title(axs[4],'Robust-workpoint criterion: lambda_min(F)')
safe_colorbar(fig,im,axs[4],r'$\lambda_{\min}(F)$',pad=.015)

# f cumulative budget
axs[5].plot(k,cb,label=r'amplitude $b_1$')
axs[5].plot(k,cp,label=r'phase $\phi$')
axs[5].set(xlabel='ranked channels kept',ylabel='cumulative FI fraction')
axs[5].set_ylim(0,1.02)
axs[5].legend(frameon=False,fontsize=6.3,loc='lower right')
safe_panel(axs[5],'f'); safe_title(axs[5],'Information budget concentrates in a few channels')

for a in axs:
    clean(a)
finish_pub(fig,OUT,'Fisher geometry: error ellipses, workpoint maps and information budget')
