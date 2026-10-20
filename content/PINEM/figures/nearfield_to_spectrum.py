import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""From a prescribed near field to an averaged and detector-resolved PINEM spectrum.
All lengths and energies are dimensionless; see the corresponding chapter's model notes.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style
from scipy.special import jv



G0=2.6; W=1.0; WB=0.65
n=np.arange(-13,14)
x=np.linspace(-2.5,2.5,261)
weight=np.exp(-x*x/(2*WB*WB)); weight/=np.trapezoid(weight,x)

def beta(g,x,d=0):
    return g*np.exp(-x*x/(2*W*W))*np.exp(-0.5*d*d)

def pop(g, average):
    b=beta(g,x)
    p=jv(n[:,None],2*b[None,:])**2
    out=np.trapezoid(p*weight[None,:],x,axis=1) if average else jv(n,2*g)**2
    return out/out.sum()

def spectrum(p,sig,E):
    k=np.exp(-0.5*((E[:,None]-n[None,:])/sig)**2)/(np.sqrt(2*np.pi)*sig)
    y=k@p
    return y/np.trapezoid(y,E)

fig,axs=plt.subplots(2,3,figsize=(11.4,7.0),layout='constrained')
axs=axs.ravel()
# a field in longitudinal and transverse coordinates
Z,X=np.meshgrid(np.linspace(-3,3,301),np.linspace(-2.5,2.5,261))
Efield=np.exp(-X*X/2-Z*Z/2)*np.cos(5.5*Z)
a=axs[0]; im=a.imshow(Efield,origin='lower',extent=[-3,3,-2.5,2.5],cmap='RdBu_r',vmin=-1,vmax=1,aspect='auto')
a.set(xlabel=r'$z/\sigma_z$',ylabel=r'$x/w$');fig.colorbar(im,ax=a,shrink=.87,label=r'$\operatorname{Re} E_z/E_0$')
# b complex coupling magnitude from analytic integral
a=axs[1]; dd=np.linspace(-3,3,181); XX,DD=np.meshgrid(x/W,dd)
B=G0*np.exp(-XX**2/2-DD**2/2)
im=a.imshow(B,origin='lower',extent=[-2.5,2.5,-3,3],cmap='magma',aspect='auto')
a.set(xlabel=r'$x/w$',ylabel=r'$\sigma_z\Delta k$');fig.colorbar(im,ax=a,shrink=.87,label=r'$|\beta(x,\Delta k)|$')
# c coherent and beam averaged sidebands
a=axs[2]; ideal=pop(G0,False); avg=pop(G0,True)
a.plot(n,ideal,'o-',markersize=2.9,label='narrow probe')
a.plot(n,avg,'s-',markersize=2.9,label='finite beam')
a.set(xlim=(-9,9),xlabel=r'exchange order $n$',ylabel=r'$P_n$');a.legend(frameon=False,loc='upper center',ncol=2,fontsize=7.2)
# d convolution with resolution
a=axs[3]; En=np.linspace(-10,10,1001)
for ss in [.28,.8]:a.plot(En,spectrum(avg,ss,En),label=fr'$\sigma_E/(\hbar\omega)={ss}$')
a.set(xlim=(-8,8),xlabel=r'$(E-E_0)/(\hbar\omega)$',ylabel='probability density');a.legend(frameon=False)
# e nonlinear PINEM contrast, not proportional to the near-field intensity
a=axs[4]; C=1-jv(0,2*B)**2
im=a.imshow(C,origin='lower',extent=[-2.5,2.5,-3,3],cmap='viridis',vmin=0,vmax=1,aspect='auto')
a.set(xlabel=r'$x/w$',ylabel=r'$\sigma_z\Delta k$');fig.colorbar(im,ax=a,shrink=.87,label=r'$1-P_0$')
# f Fisher loss under instrumental spectral convolution
a=axs[5]; sigmas=np.linspace(.12,1.2,45); delta=.012
for av,name in [(False,'narrow probe'),(True,'finite beam')]:
    f=[]
    for s in sigmas:
        p=spectrum(pop(G0,av),s,En)
        dp=(spectrum(pop(G0+delta,av),s,En)-spectrum(pop(G0-delta,av),s,En))/(2*delta)
        f.append(np.trapezoid(dp*dp/np.maximum(p,1e-13),En))
    a.plot(sigmas,f,label=name)
a.set(xlabel=r'resolution $\sigma_E/(\hbar\omega)$',ylabel=r'$F_{|\beta_0|\,|\beta_0|}$');a.legend(frameon=False)
titles=['(a) Prescribed longitudinal near field','(b) Phase-matched coupling','(c) Beam-average changes sidebands',
        '(d) Energy-resolution convolution','(e) Nonlinear PINEM image','(f) Information lost to averaging']
for ax,t in zip(axs,titles):ax.set_title(t,loc='left',pad=8,fontweight='bold')
book_save(fig,Path(__file__).with_suffix('.pdf'))
plt.close(fig)
