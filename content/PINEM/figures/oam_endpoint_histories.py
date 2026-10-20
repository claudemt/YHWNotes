"""Finite Hermitian energy--OAM endpoint-history interferometer.

The extra grading is an *orthogonal resolved degree of freedom*, not a numerical
suppression of a hopping. A graded endpoint must be summed incoherently over
orthogonal ancilla labels if that label is ignored by the readout.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from matplotlib import pyplot as plt
import numpy as np
from preamble import pubfig,finish_pub
from oam_higher_order_models import endpoint_signal,populations,harmonic_coefficient

BLUE='#2677a8';ORANGE='#c77641';GREEN='#258676';PURPLE='#8463ac'

def plot():
    fig=pubfig()
    gs=fig.add_gridspec(2,3,wspace=.60,hspace=.54)
    axes=[fig.add_subplot(gs[0,0],projection='3d')]+[
        fig.add_subplot(gs[i//3,i%3]) for i in range(1,6)]
    a,b,c,d,e,f=axes
    # (a) Endpoints are integer coordinates. Auxiliary height disambiguates paths,
    # and is expressly NOT a physical dimension.
    pts=np.array([[0,0,0],[1,1,.8],[1,-1,.8],[2,0,0]],float)
    edges=[(0,1,BLUE),(1,3,ORANGE),(0,2,BLUE),(2,3,ORANGE),(0,3,GREEN)]
    for i,j,color in edges:
        p=pts[i];q=pts[j]
        a.plot(*np.vstack([p,q]).T,lw=2,color=color)
        mid=p+.67*(q-p)
        a.scatter(*mid,s=7,color=color,depthshade=False)
    # Faint ground-plane shadows and vertical guides make the auxiliary
    # plotting height legible without inventing an extra physical charge.
    for j in (1,2):
        x,y,z=pts[j]
        a.plot([x,x],[y,y],[0,z],':',lw=.85,color='.57',alpha=.9)
        a.scatter([x],[y],[0],s=15,color='.72',depthshade=False)
    a.plot([0,2],[0,0],[0,0],':',lw=.55,color='.75')
    a.scatter(pts[:,0],pts[:,1],pts[:,2],c=[GREEN,BLUE,BLUE,ORANGE],s=36,depthshade=False)
    a.set(xlim=(-.18,2.28),ylim=(-1.35,1.35),zlim=(-.1,1.25))
    a.view_init(elev=27,azim=-58)
    a.set_box_aspect((1.5,1.5,.75),zoom=1.40)
    a.set_axis_off()
    a.text2D(.46,.92,r'$(N,L)$',transform=a.transAxes,ha='center',fontsize=9)
    # (b) Coherent versus graded: cannot interfere across orthogonal tags.
    theta=np.linspace(0,2*np.pi,121)
    coherent=np.array([endpoint_signal(t) for t in theta])
    graded=np.array([endpoint_signal(t,graded=True) for t in theta])
    b.plot(theta/np.pi,coherent,color=BLUE,label='Same endpoint')
    b.plot(theta/np.pi,graded,'--',color=ORANGE,label='Tagged endpoint')
    b.set(xlabel=r'$\phi/\pi$',ylabel=r'$P(2,0)$',xlim=(0,2),ylim=(0,.35))
    b.legend(loc='upper right',frameon=False)
    # (c) Remove the direct channel; all loop-phase modulation disappears.
    without=np.array([endpoint_signal(t,g3=0.) for t in theta])
    c.plot(theta/np.pi,coherent,color=BLUE,label='$g_3=0.34$')
    c.plot(theta/np.pi,without,'--',color=GREEN,label='$g_3=0$')
    c.set(xlabel=r'$\phi/\pi$',ylabel=r'$P(2,0)$',xlim=(0,2),ylim=(0,.35))
    c.legend(loc='upper right',frameon=False)
    # (d) Ordered endpoint populations, at two phases.
    lab=np.arange(4)
    for theta0,col,shift,label in [(0.,BLUE,-.15,r'$\phi=0$'),(np.pi/2,ORANGE,.15,r'$\phi=\pi/2$')]:
        vals=populations(theta0)
        d.bar(lab+shift,vals,width=.29,color=col,alpha=.83,label=label)
    d.set(xlabel='Endpoint index',ylabel='Probability',xticks=lab,ylim=(0,1.0))
    d.set_xticklabels(['$0$','$1{+}$','$1{-}$','$2$'])
    d.legend(loc='upper right',frameon=False)
    # (e) True phase response for a continuously scanned direct-path strength.
    gg=np.linspace(0,.7,42);tt=np.linspace(0,2*np.pi,64,endpoint=False)
    grid=np.array([[endpoint_signal(t,g3=g) for t in tt] for g in gg])
    e.imshow(grid,origin='lower',aspect='auto',cmap='viridis',interpolation='bilinear',
             extent=[0,2,0,.7],vmin=0,vmax=.40)
    e.set(xlabel=r'$\phi/\pi$',ylabel='$g_3$')
    # (f) Harmonic witness is zero when the direct path is disabled or resolved.
    gscan=np.linspace(0,.7,31)
    tscan=np.linspace(0,2*np.pi,64,endpoint=False)
    mod_coh=[];mod_tag=[]
    for g in gscan:
        sig=np.array([endpoint_signal(t,g3=g) for t in tscan])
        tags=np.array([endpoint_signal(t,g3=g,graded=True) for t in tscan])
        mod_coh.append(2*abs(harmonic_coefficient(sig)))
        mod_tag.append(2*abs(harmonic_coefficient(tags)))
    f.plot(gscan,mod_coh,color=BLUE,label='Same endpoint')
    f.plot(gscan,mod_tag,'--',color=ORANGE,label='Orthogonal tag')
    f.set(xlabel='Direct coupling $g_3$',ylabel='Harmonic amplitude',xlim=(0,.7))
    f.legend(loc='upper left',frameon=False)
    finish_pub(fig,Path(__file__).with_suffix('.pdf'))

if __name__=='__main__':
    plot()
