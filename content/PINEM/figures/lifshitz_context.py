"""Six-panel Lifshitz geometry with unobstructed torus projections."""
import common
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,clean,finish_pub
from models.li2026 import dispersion

OUT=Path(__file__).with_suffix('.pdf')
fig=pubfig(8.2,5.75,top=.92,left=.06,right=.985,bottom=.08)
gs=fig.add_gridspec(2,3,hspace=.54,wspace=.22)
ratios=[1/3,1.0,3.0]
colors=['#1c78b5','#1fa187','#c65b38']
labels=['Detached loops','Critical neck','Reconnected sheets']
k=np.linspace(-np.pi,np.pi,401)
K,KL=np.meshgrid(k,k,indexing='xy')
levels=np.linspace(-4.5,4.5,10)

# torus + custom orthographic projection
R0=2.05; r0=0.72

def torus(u,v,extra=0.0):
    rr=r0+extra
    x=(R0+rr*np.cos(v))*np.cos(u)
    y=(R0+rr*np.cos(v))*np.sin(u)
    z=rr*np.sin(v)
    return np.stack([x,y,z],axis=0)

def project(points,elev=28,azim=-37):
    az=np.deg2rad(azim); el=np.deg2rad(elev)
    Rz=np.array([[np.cos(az),-np.sin(az),0],[np.sin(az),np.cos(az),0],[0,0,1]])
    Rx=np.array([[1,0,0],[0,np.cos(el),-np.sin(el)],[0,np.sin(el),np.cos(el)]])
    P=Rx@Rz@points.reshape(3,-1)
    return P[0].reshape(points.shape[1:]),P[1].reshape(points.shape[1:]),P[2].reshape(points.shape[1:])

def split_visible(x2,y2,z2):
    vis=z2>=0
    out=[]
    start=0
    current=vis[0]
    for i in range(1,len(vis)):
        if vis[i]!=current:
            out.append((slice(start,i+1),current))
            start=i
            current=vis[i]
    out.append((slice(start,len(vis)),current))
    return out

U=np.linspace(-np.pi,np.pi,260)
V=np.linspace(-np.pi,np.pi,180)
UU,VV=np.meshgrid(U,V)
TX,TY,TZ=project(torus(UU,VV),elev=28,azim=-37)

for j,(ratio,c,label) in enumerate(zip(ratios,colors,labels)):
    E=dispersion(K,KL,1.0,ratio,-1,-1)
    # top: Brillouin-zone level set geometry
    ax=fig.add_subplot(gs[0,j])
    im=ax.contourf(K,KL,E,levels=levels,cmap='coolwarm',extend='both',alpha=0.92)
    ax.contour(K,KL,E,levels=levels[::2],colors='w',linewidths=0.45,alpha=0.55)
    cs=ax.contour(K,KL,E,levels=[0],colors=[c],linewidths=2.2)
    # highlight zone corners + periodic seam guides
    ax.axvline(-np.pi,color='0.2',lw=.6,ls=':'); ax.axvline(np.pi,color='0.2',lw=.6,ls=':')
    ax.axhline(-np.pi,color='0.2',lw=.6,ls=':'); ax.axhline(np.pi,color='0.2',lw=.6,ls=':')
    ax.scatter([0,0],[0,np.pi],s=10,color='k',alpha=0.5,zorder=5)
    ax.set(xlim=(-np.pi,np.pi),ylim=(-np.pi,np.pi),aspect='equal',xlabel=r'$K_N$')
    if j==0: ax.set_ylabel(r'$K_\ell$')
    ax.set_xticks([-np.pi,0,np.pi]); ax.set_xticklabels([r'$-\pi$','0',r'$\pi$'])
    ax.set_yticks([-np.pi,0,np.pi]); ax.set_yticklabels([r'$-\pi$','0',r'$\pi$'])
    safe_panel(ax,chr(97+j))
    safe_title(ax,fr'$|\beta_2/\beta_1|={ratio:g}$: {label}')
    clean(ax)

    # bottom: torus lift with front/back split
    ax=fig.add_subplot(gs[1,j])
    # wireframe first
    for vv in np.linspace(-np.pi,np.pi,9):
        pts=torus(U,np.full_like(U,vv))
        x2,y2,z2=project(pts,elev=28,azim=-37)
        ax.plot(x2,y2,color='0.82',lw=.5,zorder=1,alpha=0.9 if np.mean(z2)>0 else 0.45)
    for uu in np.linspace(-np.pi,np.pi,12,endpoint=False):
        pts=torus(np.full_like(V,uu),V)
        x2,y2,z2=project(pts,elev=28,azim=-37)
        ax.plot(x2,y2,color='0.85',lw=.42,zorder=1,alpha=0.85 if np.mean(z2)>0 else 0.35)
    # torus silhouette
    for vv in [-np.pi,0]:
        pts=torus(U,np.full_like(U,vv))
        x2,y2,z2=project(pts,elev=28,azim=-37)
        ax.plot(x2,y2,color='0.55',lw=.9,alpha=.55)
    for seg in cs.allsegs[0]:
        if len(seg)<3: 
            continue
        pts=torus(seg[:,0],seg[:,1],extra=0.06)
        x2,y2,z2=project(pts,elev=28,azim=-37)
        for sl,front in split_visible(x2,y2,z2):
            ax.plot(x2[sl],y2[sl],color=c,lw=2.4 if front else 1.4,
                    ls='-' if front else (0,(2.1,1.4)),alpha=1.0 if front else 0.45,
                    solid_capstyle='round',zorder=10 if front else 5)
    ax.set_aspect('equal')
    ax.set_xlim(TX.min()*1.06,TX.max()*1.06); ax.set_ylim(TY.min()*1.08,TY.max()*1.08)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
    safe_panel(ax,chr(100+j))
    safe_title(ax,'Same contour lifted to the Brillouin-zone torus')

finish_pub(fig,OUT)
