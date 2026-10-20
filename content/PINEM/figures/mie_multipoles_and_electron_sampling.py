"""Quantitative six-panel Mie scattering and trajectory-sampling atlas.
Uniform nonmagnetic sphere; all model and plotting parameters documented in ch05.
"""
from pathlib import Path
import sys
import numpy as np
from scipy.special import spherical_jn, spherical_yn, k1
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preamble import pubfig, safe_title, safe_panel, safe_colorbar, clean, finish_pub

OUT=Path(__file__).with_suffix('.pdf')
m=1.7+0.03j
chi=(m*m-1)/(m*m+2)
x=np.linspace(0.10,4.0,240)
L=14

def riccati(l,z):
    psi=z*spherical_jn(l,z)
    psip=spherical_jn(l,z)+z*spherical_jn(l,z,derivative=True)
    h=spherical_jn(l,z)+1j*spherical_yn(l,z)
    hp=spherical_jn(l,z,derivative=True)+1j*spherical_yn(l,z,derivative=True)
    xi=z*h
    xip=h+z*hp
    return psi,psip,xi,xip

def mie(ka):
    aa=[];bb=[]
    for ell in range(1,L+1):
        psi_m,pm,_,_=riccati(ell,m*ka)
        psi,p,xi,xip=riccati(ell,ka)
        aa.append((m*psi_m*p-psi*pm)/(m*psi_m*xip-xi*pm))
        bb.append((psi_m*p-m*psi*pm)/(psi_m*xip-m*xi*pm))
    return np.asarray(aa),np.asarray(bb)

A=[];B=[]
for xx in x:
    aa,bb=mie(xx)
    A.append(aa);B.append(bb)
A=np.asarray(A);B=np.asarray(B)
ell=np.arange(1,L+1)
q_sca=2/(x*x)*np.sum((2*ell+1)[None,:]*(abs(A)**2+abs(B)**2),axis=1)
q_ray=(8/3)*x**4*abs(chi)**2

th=np.linspace(0,np.pi,400)
mu=np.cos(th)

def differential(ka):
    aa,bb=mie(ka)
    pi0=np.zeros_like(mu)
    pi1=np.ones_like(mu)
    S1=np.zeros_like(mu,dtype=complex)
    S2=np.zeros_like(mu,dtype=complex)
    for n in range(1,L+1):
        if n==1: pi_n=pi1
        else:
            pi_n=((2*n-1)/(n-1))*mu*pi1-(n/(n-1))*pi0
            pi0,pi1=pi1,pi_n
        tau=n*mu*pi_n-(n+1)*pi0
        coef=(2*n+1)/(n*(n+1))
        S1+=coef*(aa[n-1]*pi_n+bb[n-1]*tau)
        S2+=coef*(aa[n-1]*tau+bb[n-1]*pi_n)
    p=(abs(S1)**2+abs(S2)**2)/2
    norm=np.trapezoid(p*np.sin(th),th)
    return p/norm

fig=pubfig(8.4,5.85,top=.90,left=.085,right=.965,bottom=.085)
gs=fig.add_gridspec(2,3,wspace=.51,hspace=.67)
axs=[fig.add_subplot(gs[j//3,j%3]) for j in range(6)]

# a: electric multipole fractions from exact Mie coefficients
for n in [1,2,3,4]:
    axs[0].plot(x,(2*n+1)*abs(A[:,n-1])**2,label=rf'$\ell={n}$')
axs[0].set(xlabel=r'size parameter $x=k_{\mathrm{h}}a$',ylabel=r'$(2\ell+1)|a_\ell|^2$')
axs[0].legend(frameon=False,fontsize=7,loc='upper left')
safe_panel(axs[0],'a');safe_title(axs[0],'Electric multipole contributions')

# b: the approximation is tested by a signed relative residual.
# Mie and Rayleigh curves are indistinguishable at small x: the residual
# exposes the onset and the 10% validity boundary without hiding data.
err=np.abs(q_sca/q_ray-1)
axs[1].semilogy(x,err,lw=1.6)
axs[1].axhline(.1,ls=':',lw=1.0,color='.4',label='10% error')
axs[1].set(xlabel=r'$k_{\mathrm{h}}a$',ylabel=r'$|Q_{\mathrm{Mie}}/Q_{\mathrm{Ray}}-1|$',
           xlim=(.1,1.8),ylim=(1e-3,2))
axs[1].legend(frameon=False,loc='upper left')
safe_panel(axs[1],'b');safe_title(axs[1],'Mie vs. Rayleigh scattering')

# c: complex dipole a1 as size changes
sc=axs[2].scatter(A[:,0].real,A[:,0].imag,c=x,s=11,cmap='viridis',rasterized=True)
axs[2].plot(A[:,0].real,A[:,0].imag,lw=.4,alpha=.45,c='0.3')
axs[2].set(xlabel=r'$\operatorname{Re}a_1$',ylabel=r'$\operatorname{Im}a_1$')
safe_colorbar(fig,sc,axs[2],r'$k_{\mathrm{h}}a$',pad=.022)
safe_panel(axs[2],'c');safe_title(axs[2],'Complex electric-dipole coefficient')

# d: angular phase-function for multiple sizes
for ka in [0.40,1.60,3.20]:
    pp=differential(ka)
    axs[3].plot(th*180/np.pi,pp,label=rf'$x={ka:.2f}$')
axs[3].set(xlabel=r'scattering angle $\theta$ (deg)',ylabel=r'$p(\theta)$')
axs[3].legend(frameon=False,fontsize=7.1,loc='upper left')
safe_panel(axs[3],'d');safe_title(axs[3],'Angular scattering profiles')

# e: optical anisotropy: angular first cosine moment
g=[]
for ka in np.linspace(.15,4,85):
    pp=differential(ka)
    g.append(np.trapezoid(np.cos(th)*pp*np.sin(th),th))
axs[4].plot(np.linspace(.15,4,85),g)
axs[4].axhline(0,ls=':',lw=.65,c='0.4')
axs[4].set(xlabel=r'$k_{\mathrm{h}}a$',ylabel=r'$g=\langle\cos\theta\rangle$',ylim=(-.1,1))
safe_panel(axs[4],'e');safe_title(axs[4],'Forward-scattering anisotropy')

# f: electron trajectory integral in sphere quasistatic limit
ba=np.linspace(1,5,230)
for ua in [.15,.35,.65]:
    y=abs(chi)*ua*ua*k1(ua*ba)
    axs[5].plot(ba,y,label=rf'$\kappa a={ua:.2f}$')
axs[5].set(xlabel=r'impact parameter $b/a$',ylabel=r'$|\beta|\hbar\omega/(e|E_0|a)$')
axs[5].legend(frameon=False,fontsize=7,loc='upper right')
safe_panel(axs[5],'f');safe_title(axs[5],'Electron trajectory coupling')

for ax in axs:clean(ax)
finish_pub(fig,OUT)
print('OUTPUT',OUT,'Q_sca',round(q_sca.max(),4),'phase_g_range',round(min(g),4),round(max(g),4))
