"""Magnetic synthetic lattice: explicitly specified Harper-Hofstadter model.
Six physical panels use the same hopping model with stated boundary conditions.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import expm_multiply
from common import pubfig, safe_panel, safe_title, safe_colorbar, clean, finish_pub

DEST=Path(__file__).with_suffix('.pdf')
tx=ty=1.0; alpha=0.25

def strip(k, a=alpha, ny=32, periodic=False):
    y=np.arange(ny)
    h=np.diag(-2*tx*np.cos(k+2*np.pi*a*y))
    idx=np.arange(ny-1)
    h[idx,idx+1]=-ty; h[idx+1,idx]=-ty
    if periodic: h[0,-1]=h[-1,0]=-ty
    return h

def finite_h(nx=30, ny=18, a=alpha):
    dim=nx*ny
    h=lil_matrix((dim,dim), dtype=complex)
    for y in range(ny):
        for x in range(nx):
            i=y*nx+x
            if x+1<nx:
                j=i+1; val=-tx*np.exp(2j*np.pi*a*y)
                h[j,i]=val;h[i,j]=np.conj(val)
            if y+1<ny:
                j=i+nx;h[j,i]=-ty;h[i,j]=-ty
    return csr_matrix(h)

nx,ny=30,18
xx,yy=np.meshgrid(np.arange(nx),np.arange(ny),indexing='xy')
initial=np.exp(-((xx-6.0)**2/(2*2.1**2)+(yy-1.1)**2/(2*0.9**2)))*np.exp(1j*0.75*xx)
initial=(initial/np.linalg.norm(initial)).ravel()
Hf=finite_h()
ts=np.linspace(0,9,75)
phis=expm_multiply(-1j*Hf,initial,start=0,stop=9,num=len(ts),endpoint=True)
probs=(abs(phis)**2).reshape(len(ts),ny,nx)
P0=probs[0]; Pmid=probs[np.argmin(abs(ts-7.2))]; Pend=probs[-1]
edge_mass=np.sum(probs[:,:3,:],axis=(1,2))
meanx=np.einsum('tyx,x->t',probs,np.arange(nx))
# control without magnetic flux (identical seed and boundary)
zero=expm_multiply(-1j*finite_h(a=0), initial,start=0,stop=9,num=len(ts),endpoint=True)
pzero=(abs(zero)**2).reshape(len(ts),ny,nx)
edge_zero=np.sum(pzero[:,:3,:],axis=(1,2))

fig=pubfig(8.4,6.0,top=.92,left=.08,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.56,hspace=.62)
axes=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
# a magnetic miniband cuts with ky=0 (different flux numerators, same circumference)
ax=axes[0]
q=24
for p in range(0,13):
    a=p/q
    for k in np.linspace(-np.pi,np.pi,28,endpoint=False):
        vals=np.linalg.eigvalsh(strip(k,a,ny=q,periodic=True))
        ax.scatter(np.full(q,a),vals,s=0.55,color='#245d75',alpha=.55,rasterized=True)
ax.set(xlabel=r'Flux $\alpha=\Phi_{\mathrm{p}}/(2\pi)$',ylabel=r'Energy $E/t$')
safe_panel(ax,'a');safe_title(ax,'Magnetic minibands at fixed transverse twist')
# b strip spectrum weighted by edge probability
ax=axes[1]; kvals=np.linspace(-np.pi,np.pi,121)
energies=[];weights=[]
for k in kvals:
    w,v=eigh(strip(k,ny=ny+14))
    weights.append(np.sum(abs(v[[0,1,-2,-1],:])**2,axis=0))
    energies.append(w)
Es=np.array(energies);W=np.array(weights)
sc=ax.scatter(np.repeat(kvals,Es.shape[1]),Es.ravel(),c=W.ravel(),cmap='inferno',s=1.4,vmin=0,vmax=0.6,rasterized=True)
ax.set(xlabel=r'$k_x$',ylabel=r'Ribbon energy $E/t$')
safe_panel(ax,'b');safe_title(ax,'Edge-weighted ribbon spectrum')
safe_colorbar(fig,sc,ax,'edge fraction',pad=.014)
# c transverse profile of a strongly localized edge eigenstate
ax=axes[2]
iy,ix=np.unravel_index(np.argmax(W*((abs(Es)<1.75)&(abs(Es)>0.15))),W.shape)
ki=kvals[iy]
e,vec=eigh(strip(ki,ny=ny+14))
ps=abs(vec[:,ix])**2
ax.plot(np.arange(len(ps)),ps,lw=1.4)
ax.fill_between(np.arange(len(ps)),ps,alpha=.28)
ax.set(xlabel=r'Transverse site $y$',ylabel=r'$|u_y(k_x)|^2$')
safe_panel(ax,'c');safe_title(ax,'Edge-mode transverse profile')
# d initial density
ax=axes[3];im=ax.imshow(P0,origin='lower',aspect='auto',extent=[0,nx-1,0,ny-1],cmap='magma',vmin=0,vmax=max(P0.max(),Pmid.max()))
ax.set(xlabel=r'Longitudinal site $x$',ylabel=r'Transverse site $y$')
safe_panel(ax,'d');safe_title(ax,'Edge-localized input packet')
safe_colorbar(fig,im,ax,'site probability',pad=.014)
# e later propagated density
ax=axes[4];im=ax.imshow(Pmid,origin='lower',aspect='auto',extent=[0,nx-1,0,ny-1],cmap='magma',vmin=0,vmax=Pmid.max())
ax.set(xlabel=r'Longitudinal site $x$',ylabel=r'Transverse site $y$')
safe_panel(ax,'e');safe_title(ax,'Propagated packet at $t=7.2$')
safe_colorbar(fig,im,ax,'site probability',pad=.014)
# f edge retention
ax=axes[5]
ax.plot(ts,edge_mass,label=r'flux $\alpha=1/4$')
ax.plot(ts,edge_zero,label=r'zero-flux control',ls='--')
ax.set(xlabel=r'Dimensionless time $t\,t_x$',ylabel='Probability in bottom three rows',ylim=(0,1.02))
ax.legend(fontsize=7.2,frameon=False)
safe_panel(ax,'f');safe_title(ax,'Boundary retention under flux')
for a in axes:clean(a)
finish_pub(fig,DEST)

# Verification: Hermiticity and exact evolution norm
assert (Hf-Hf.getH()).nnz==0
assert np.max(abs(probs.sum(axis=(1,2))-1))<1e-9
print('synthetic_flux pass; chosen edge',float(ki),int(ix),'norm',float(probs.sum(axis=(1,2)).min()))
