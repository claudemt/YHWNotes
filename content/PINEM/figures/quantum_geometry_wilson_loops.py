import common  # shared helpers + models
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne

OUT=Path(__file__).with_suffix('.pdf')

# --- helpers ---
def qzw_strip(kx,m=-1.0,ny=44):
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.array([[1,0],[0,-1]],complex)
    dim=2*ny
    H=np.zeros((dim,dim),complex)
    onsite=np.sin(kx)*sx + (m+np.cos(kx))*sz
    hop=0.5*sz - 0.5j*sy
    for y in range(ny):
        sl=slice(2*y,2*y+2)
        H[sl,sl]=onsite
        if y<ny-1:
            sl2=slice(2*(y+1),2*(y+1)+2)
            H[sl2,sl]+=hop
            H[sl,sl2]+=hop.conj().T
    return H

def ribbon_spectrum(m=-1.0,ny=44,nk=160):
    k=np.linspace(-np.pi,np.pi,nk)
    E=[]; edge=[]
    for kk in k:
        H=qzw_strip(kk,m=m,ny=ny)
        ev,V=eigh(H)
        edge_w=np.zeros(2*ny)
        for y in range(ny):
            w=np.exp(-y/4)+np.exp(-(ny-1-y)/4)
            edge_w[2*y:2*y+2]=w
        edge.append(np.sum((np.abs(V)**2)*edge_w[:,None],axis=0))
        E.append(ev)
    return k,np.asarray(E),np.asarray(edge)

def direct_gap(m,nk=None):
    """Exact direct gap of Qi--Wu--Zhang, including all true gap closings.

    Write u=cos(kx),v=cos(ky). |d|²=2-u²-v²+(m+u+v)² is
    affine in u at fixed v, and affine in v at fixed u. Hence a
    global minimum on [-1,1]² lies at u,v=+/-1.
    """
    return 2*min(abs(m+2),abs(m),abs(m-2))

# --- compute geometric fields ---
m0=-1.0
k,F,gtr,W=ne.qwz_geometry(m=m0,nk=91)
ext=[-np.pi,np.pi,-np.pi,np.pi]
ratio=np.abs(F)/(gtr+1e-12)
kr,Er,edge=ribbon_spectrum(m=m0,ny=42,nk=170)
ms,ch,vol=ne.geometry_mass_scan(ms=np.linspace(-3,3,121),nk=41)
gap=np.array([direct_gap(mm,nk=61) for mm in ms])

fig=pubfig(8.55,6.15,top=.92,left=.075,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.57,hspace=.60)
axs=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]

# a Berry curvature
im=axs[0].imshow(F.T,origin='lower',extent=ext,cmap='RdBu_r')
axs[0].set(xlabel=r'$k_x$',ylabel=r'$k_y$')
safe_panel(axs[0],'a'); safe_title(axs[0],'Berry curvature')
safe_colorbar(fig,im,axs[0],'curvature',pad=.015)

# b quantum metric
im=axs[1].imshow(gtr.T,origin='lower',extent=ext,cmap='magma')
axs[1].set(xlabel=r'$k_x$',ylabel=r'$k_y$')
safe_panel(axs[1],'b'); safe_title(axs[1],'Quantum metric')
safe_colorbar(fig,im,axs[1],'metric',pad=.015)

# c Wilson loop
axs[2].plot(k,W,lw=1.25)
axs[2].axhline(0,ls='--',lw=.7,color='0.45')
axs[2].set(xlabel=r'$k_y$',ylabel='hybrid Wannier center')
axs[2].set_ylim(-.1,1.1)
safe_panel(axs[2],'c'); safe_title(axs[2],'Wilson-loop winding')

# d ribbon spectrum with edge states
sc=axs[3].scatter(np.repeat(kr,Er.shape[1]),Er.ravel(),c=edge.ravel(),s=2.1,cmap='viridis',rasterized=True)
axs[3].set(xlabel=r'$k_x$',ylabel='energy')
safe_panel(axs[3],'d'); safe_title(axs[3],'Chiral edge branches')
safe_colorbar(fig,sc,axs[3],'edge weight',pad=.015)

# e: exact lattice Chern numbers, undefined at gap closings.
axs[4].axhline(0,color='.72',lw=.65)
for left,right,C in [(-3,-2,0),(-2,0,-1),(0,2,1),(2,3,0)]:
    xx=np.linspace(left,right,150)
    axs[4].plot(xx,np.full_like(xx,C),lw=1.65,color='#2677a8')
for xc,adjacent in [(-2,(0,-1)),(0,(-1,1)),(2,(1,0))]:
    axs[4].axvline(xc,ls=':',lw=1.0,color='.55')
    for C in adjacent:
        axs[4].plot([xc],[C],marker='o',ms=5,mfc='white',mec='#2677a8',zorder=4)
axs[4].set(xlabel='mass $m$',ylabel='Chern number',ylim=(-1.45,1.45))
axs[4].set_xticks([-3,-2,-1,0,1,2,3])
safe_panel(axs[4],'e'); safe_title(axs[4],'Topological phase boundaries')

# f topology-geometry local bound
im=axs[5].imshow(ratio.T,origin='lower',extent=ext,cmap='cividis',vmin=0,vmax=np.nanpercentile(ratio,98))
axs[5].set(xlabel=r'$k_x$',ylabel=r'$k_y$')
safe_panel(axs[5],'f'); safe_title(axs[5],'Curvature-metric ratio')
# The ratio is dimensionless; a fourth colorbar would clip in the book column.
axs[5].text(.03,.05,r'$|\Omega_{xy}|/\mathrm{Tr}\,g$',transform=axs[5].transAxes,fontsize=8,ha='left',va='bottom',bbox=dict(fc='white',ec='none',alpha=.8,pad=1))

for a in axs:
    clean(a)
finish_pub(fig,OUT)
