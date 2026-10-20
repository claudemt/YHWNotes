"""Six computed panels: rank-limited covariance tomography and counting error."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,finish_pub,safe_colorbar,COLORS,style_3d
from oam_relation_covariance_model import (G_TRUE,U,A,HISTORIES,probability,
    fisher_grid,coeffs,trial_estimates)
BLUE=COLORS['blue']; ORANGE=COLORS['orange'];GREEN=COLORS['green'];PURPLE=COLORS['purple']

def plot():
    fig=pubfig();gs=fig.add_gridspec(2,3,wspace=.65,hspace=.66)
    ax=[fig.add_subplot(gs[0,0],projection='3d')]
    ax += [fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]
    a,b,c,d,e,f=ax
    # a: actual nonnegative integer exchange-history coordinates, with u/v edges.
    # h4 is recovered from h1,h2,h3 and the common endpoint; no fake physical height.
    pts=HISTORIES[:,:3]
    for j,k,col in [(0,1,BLUE),(0,2,GREEN),(1,3,GREEN),(2,3,BLUE)]:
        a.plot(*np.stack([pts[j],pts[k]]).T,color=col,lw=2.1,alpha=.92)
    for j,pos in enumerate(pts):
        a.scatter(*pos,color=[PURPLE,BLUE,GREEN,ORANGE][j],s=32,depthshade=False)
    a.set(xlabel=r'$h_1$',ylabel=r'$h_2$',zlabel=r'$h_3$')
    a.set_xlim(-.15,2.2);a.set_ylim(-.15,2.2);a.set_zlim(-.15,1.3)
    a.set_xticks([0,1,2]);a.set_yticks([0,1,2]);a.set_zticks([0,1])
    a.set_box_aspect((1.2,1.1,.72),zoom=.82);style_3d(a,23,-61)
    # b: harmonic support for exactly calibrated four-path endpoint.
    cc=coeffs(G_TRUE); xx=np.arange(-1,2)
    mags=np.array([[abs(cc.get((i,j),0)) for i in xx] for j in xx])
    im=b.imshow(mags,origin='lower',extent=[-1.5,1.5,-1.5,1.5],cmap='viridis',aspect='auto')
    b.set_xticks([-1,0,1]);b.set_yticks([-1,0,1])
    b.set(xlabel=r'Index $m_u$',ylabel=r'Index $m_v$')
    safe_colorbar(fig,im,b)
    # c: Fisher for the 3 identifiable entries of projected covariance.
    ff=fisher_grid(G_TRUE,24)
    im=c.imshow(ff,cmap='viridis',aspect='auto',vmin=0,vmax=.05)
    c.set_xticks([0,1,2],[r'$G_{11}$',r'$G_{22}$',r'$G_{12}$'])
    c.set_yticks([0,1,2],[r'$G_{11}$',r'$G_{22}$',r'$G_{12}$'])
    safe_colorbar(fig,im,c)
    # d: embed Fisher in the 10-dimensional symmetric Sigma space. Rank at most 3.
    basis=[]
    for i in range(4):
        for j in range(i,4):
            unit=np.zeros((4,4));unit[i,j]=unit[j,i]=1
            tmp=U.T@unit@U
            basis.append([tmp[0,0],tmp[1,1],tmp[0,1]])
    J=np.array(basis).T
    fisher10=J.T@ff@J
    ev=np.linalg.eigvalsh(fisher10)[::-1]
    d.semilogy(np.arange(1,11),np.maximum(ev,1e-13),'o-',color=BLUE,ms=4)
    d.axvline(3.5,color=ORANGE,ls='--',lw=1)
    d.set(xlabel=r'Fisher eigenvalue index',ylabel=r'$\lambda(F_\Sigma)$',xlim=(.7,10.3),ylim=(1e-13,20))
    d.set_xticks([1,2,3,4,6,8,10])
    # e: Monte Carlo error against correctly marginalized CRLB.
    ns=np.array([30,80,200,600,1600]);res=[]
    for n in ns:
        estimates=trial_estimates(int(n),trials=200,seed=3232+int(n))
        res.append(np.sqrt(np.mean((estimates[:,0,1]-G_TRUE[0,1])**2)))
    total=ns*24*24
    e.loglog(total,res,'o-',color=ORANGE,label='Moment estimator')
    cr=np.sqrt(np.linalg.inv(ff)[2,2]/total)
    e.loglog(total,cr,'--',color=BLUE,label='Full-count CRLB')
    e.set(xlabel='Total electrons',ylabel=r'RMSE of $G_{12}$')
    e.legend(frameon=False,loc='upper right')
    # f: finite-count scatter shows covariance-level uncertainty, 95% Fisher ellipse.
    estimates=trial_estimates(250,trials=220,seed=109)
    f.scatter(estimates[:,0,0],estimates[:,1,1],s=6,color=BLUE,alpha=.4,label='Synthetic counts')
    C=np.linalg.inv(ff)/(250*24*24)
    eig,evect=np.linalg.eigh(C[:2,:2]); tt=np.linspace(0,2*np.pi,200)
    xy=G_TRUE.diagonal()[:,None]+np.sqrt(5.991)*evect@np.diag(np.sqrt(eig))@np.stack([np.cos(tt),np.sin(tt)])
    f.plot(xy[0],xy[1],color=ORANGE,label='95% CRLB ellipse')
    f.plot([G_TRUE[0,0]],[G_TRUE[1,1]],marker='*',ms=7,color=GREEN,label='True')
    f.set(xlabel=r'$G_{11}$',ylabel=r'$G_{22}$',xlim=(.13,.6),ylim=(.05,.53))
    f.legend(frameon=False,loc='upper right')
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))
    print('F3 eigenvalues',np.linalg.eigvalsh(ff),'F10 rank3',ev[:5], 'RMSE',res)
if __name__=='__main__':plot()
