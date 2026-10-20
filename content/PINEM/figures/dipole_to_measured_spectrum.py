"""Rayleigh sphere -> trajectory Fourier integral -> PINEM -> detector, six reproducible panels."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import elementary_charge as qe, hbar, c, epsilon_0
from scipy.special import kv, jv
from scipy.integrate import simpson

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from preamble import pubfig, safe_panel, safe_title, safe_colorbar, clean, finish_pub

OUT=Path(__file__).with_suffix('.pdf')
a=30e-9; lam=800e-9; v=.60*c; Ein=1.0e9
eps_r=3.0+0.10j
chi=(eps_r-1)/(eps_r+2)
w=2*np.pi*c/lam; kap=w/v
p=4*np.pi*epsilon_0*a**3*chi*Ein
ha=hbar*w/qe  # photon energy eV

def Ez(z,b):
    # transverse x dipole centered at origin; electron travels in z at x=b
    return 3*p*b*z/(4*np.pi*epsilon_0*(b*b+z*z)**2.5)

def F_analytic(b,kappa):
    return -1j*p*kappa*kappa/(2*np.pi*epsilon_0)*kv(1, kappa*b)

def beta(b,kappa=kap):
    return qe*F_analytic(b,kappa)/(2*hbar*w)

def bessel_probs(b,N=10):
    n=np.arange(-N,N+1)
    return n,jv(n,2*abs(beta(b)))**2

fig=pubfig(9.6,6.95,top=.88,bottom=.09,left=.075,right=.965)
gs=fig.add_gridspec(2,3,wspace=.57,hspace=.71)
axs=[fig.add_subplot(gs[j//3,j%3]) for j in range(6)]

# a. Actual signed longitudinal electric field in the electron plane
xx=np.linspace(1.02,5.0,215); zz=np.linspace(-5,5,260)
X,Z=np.meshgrid(xx,zz)
val=(3*(p*1.0).real*X*Z/(4*np.pi*epsilon_0*a**3*(X*X+Z*Z)**2.5))/Ein
lim=np.quantile(np.abs(val),.996)
im=axs[0].imshow(val,origin='lower',aspect='auto',extent=[xx[0],xx[-1],zz[0],zz[-1]],
             cmap='RdBu_r',vmin=-lim,vmax=lim)
axs[0].set(xlabel=r'$x/a$',ylabel=r'$z/a$')
safe_colorbar(fig,im,axs[0],r'$\operatorname{Re}E_z/E_0$',pad=.025)
safe_panel(axs[0],'a'); safe_title(axs[0],'Odd longitudinal near field')

# b. Spatial field along trajectories
zs=np.linspace(-6,6,560)
for bs in [1.3,2.0,3.4]:
    axs[1].plot(zs,(Ez(a*zs,bs*a)/Ein).real,label=rf'$b/a={bs:g}$')
axs[1].axhline(0,lw=.65,c='0.5'); axs[1].set(xlabel=r'$z/a$',ylabel=r'$\operatorname{Re}E_z/E_0$')
axs[1].legend(loc='upper right',fontsize=7.8)
safe_panel(axs[1],'b'); safe_title(axs[1],'Field sampled by three trajectories')

# c. Fourier integral compared with analytical K1 identity
ka=np.linspace(.25,2.25,45); bb=2.0*a
fa=np.array([F_analytic(bb,u/a) for u in ka])
z_num=np.linspace(-300*a,300*a,22001)
fn=np.array([simpson(Ez(z_num,bb)*np.exp(-1j*(u/a)*z_num),x=z_num) for u in ka])
scale=abs(fa[0]);
axs[2].plot(ka,abs(fa)/scale,label='Bessel-$K_1$ result')
axs[2].plot(ka,abs(fn)/scale,'o',ms=2.3,markevery=4,label='trajectory quadrature')
axs[2].set(xlabel=r'$\kappa a$',ylabel=r'$|\mathcal{F}_{\parallel}|/|\mathcal{F}_{\parallel}(0.25/a)|$')
axs[2].legend(loc='upper right',fontsize=7.4)
safe_panel(axs[2],'c'); safe_title(axs[2],'Exact Fourier transform of the dipole field')

# d. complex coupling magnitude vs impact distance
ba=np.linspace(1.03,5.5,320)
bv=np.array([abs(beta(a*t)) for t in ba])
axs[3].plot(ba,bv)
for x in [1.3,2.0,3.4]: axs[3].axvline(x,color='0.6',ls=':',lw=.65)
axs[3].set(xlabel=r'$b/a$',ylabel=r'$|\beta(b)|$')
safe_panel(axs[3],'d'); safe_title(axs[3],'Evanescent coupling versus impact parameter')

# e. Exact Bessel populations at three impacts
for bb0 in [1.3,2.0,3.4]:
    n,P=bessel_probs(a*bb0,12)
    axs[4].plot(n,P,'o-',ms=2.2,label=rf'$b/a={bb0:g}$')
axs[4].set(xlabel=r'electron sideband $n$',ylabel=r'$P_n$')
axs[4].legend(loc='upper right',fontsize=7.6)
safe_panel(axs[4],'e'); safe_title(axs[4],'Discrete electron energy populations')

# f. Explicit Gaussian detector response, not a heuristic smooth fit
energy=np.linspace(-12,12,700); sigma=.34
for bb0 in [1.3,2.0,3.4]:
    n,P=bessel_probs(a*bb0,22)
    pdf=np.sum(P[:,None]*np.exp(-.5*((energy[None,:]-n[:,None])/sigma)**2)/(np.sqrt(2*np.pi)*sigma),axis=0)
    axs[5].plot(energy,pdf,label=rf'$b/a={bb0:g}$')
axs[5].set(xlabel=r'$\Delta\mathcal{E}/(\hbar\omega)$',ylabel=r'measured density $(\hbar\omega)^{-1}$')
axs[5].legend(loc='upper right',fontsize=7.4)
safe_panel(axs[5],'f'); safe_title(axs[5],'Spectrum after Gaussian detector broadening')

for ax in axs: clean(ax)
finish_pub(fig,OUT)
print(f'dipole: a={a:.3g}, lambda={lam:.3g}, v/c={v/c:.3g}, eps={eps_r}, |beta(1.3a)|={abs(beta(1.3*a)):.6g}, quadrature_err_max={np.max(np.abs(fn-fa))/np.max(abs(fa)):.3g}')
