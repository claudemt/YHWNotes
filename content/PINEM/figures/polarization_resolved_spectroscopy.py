"""Six aligned panels: PINEM spectra and phase-sensitive imaging of a Rayleigh sphere.
Every population is obtained from the same coherent beta as the companion figure.
"""
from pathlib import Path
import sys
import numpy as np
from scipy.special import jv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from preamble import pubfig, safe_colorbar, clean, finish_pub, COLORS
from polarization_model import (radius as a, beta, cancellation_angle,
                                inelastic, sideband, check)

b0=2*a
theta0=cancellation_angle(b0)
phase=np.linspace(-np.pi,np.pi,361)
angles=np.linspace(-np.pi,np.pi,361)
fig=pubfig()
axs=[fig.add_subplot(2,3,j+1) for j in range(6)]

# (a) Complex phase of the electron coupling; one trajectory crosses an exact zero.
for azimuth,color,label in [(0.,COLORS['blue'],r'$\varphi=0$'),
                            (np.pi/3,COLORS['orange'],r'$\varphi=\pi/3$')]:
    value=beta(b0,theta0,phase,azimuth)
    arg=np.angle(value,deg=True)
    arg[np.abs(value)<1e-9]=np.nan
    axs[0].plot(np.degrees(phase),arg,color=color,label=label)
axs[0].set(xlabel=r'$\delta$ (deg)',ylabel=r'$\arg\beta$ (deg)',ylim=(-195,195))
axs[0].legend(loc='lower right',frameon=False)

# (b) The equality of plus/minus sidebands is visible: plot P0, P_{+-1}, P_{+-2}.
p=abs(beta(b0,theta0,phase))
for n,color,label in [(0,COLORS['blue'],r'$P_0$'),(1,COLORS['orange'],r'$P_{\pm1}$'),
                      (2,COLORS['green'],r'$P_{\pm2}$')]:
    axs[1].plot(np.degrees(phase),jv(n,2*p)**2,color=color,label=label)
axs[1].axvline(-90,color='.6',ls=':',lw=.7)
axs[1].set(xlabel=r'$\delta$ (deg)',ylabel=r'$P_n$',ylim=(-.035,1.035))
axs[1].legend(loc='upper right',frameon=False)

# (c) Polarization handedness swaps the spatial PINEM contrast.
for d,col,lab in [(np.pi/2,COLORS['blue'],r'$\delta=+\pi/2$'),
                   (-np.pi/2,COLORS['orange'],r'$\delta=-\pi/2$')]:
    axs[2].plot(np.degrees(angles),inelastic(beta(b0,np.pi/4,d,angles)),
                color=col,label=lab)
axs[2].set(xlabel=r'$\varphi$ (deg)',ylabel=r'$1-P_0$',ylim=(-.03,1.03))
axs[2].legend(loc='upper right',frameon=False)

# (d) A complete observable symmetric energy ladder, not just a selected sideband.
n=np.arange(-6,7)
response=jv(n[:,None],2*p[None,:])**2
im=axs[3].imshow(response,extent=[-180,180,-6.5,6.5],origin='lower',aspect='auto',
                 cmap='viridis',vmin=0,vmax=1)
axs[3].set(xlabel=r'$\delta$ (deg)',ylabel=r'$n$',yticks=[-6,-3,0,3,6])
safe_colorbar(fig,im,axs[3],r'$P_n$')

# (e) Two distinct departures from the exact destructive-interference condition.
axs[4].plot(np.degrees(phase),np.maximum(abs(beta(b0,theta0,phase)),1e-5),
            color=COLORS['blue'],label=r'$\theta=\theta_0$')
axs[4].plot(np.degrees(phase),np.maximum(abs(beta(b0,theta0+np.deg2rad(6),phase)),1e-5),
            color=COLORS['orange'],label=r'$\theta=\theta_0+6^\circ$')
axs[4].axvline(-90,color='.6',ls=':',lw=.7)
axs[4].set(xlabel=r'$\delta$ (deg)',ylabel=r'$|\beta|$',yscale='log',ylim=(1e-5,3))
axs[4].legend(loc='upper right',frameon=False)

# (f) Chirality-dependent image: signed normalized asymmetry in inelastic counts.
thetas=np.linspace(0,np.pi/2,161)
phis=np.linspace(-np.pi,np.pi,271)
TH,PH=np.meshgrid(thetas,phis)
plus=inelastic(beta(b0,TH,np.pi/2,PH))
minus=inelastic(beta(b0,TH,-np.pi/2,PH))
asymmetry=(plus-minus)/np.maximum(plus+minus,1e-10)
im=axs[5].imshow(asymmetry,origin='lower',aspect='auto',extent=[0,90,-180,180],
                 cmap='RdBu_r',vmin=-1,vmax=1)
axs[5].set(xlabel=r'$\theta$ (deg)',ylabel=r'$\varphi$ (deg)')
safe_colorbar(fig,im,axs[5],r'$\mathcal{A}$')

for ax in axs:clean(ax)
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
assert check()
assert np.max(abs(jv(1,2*p)**2-jv(-1,2*p)**2))<1e-14
assert np.max(abs(asymmetry))<=1+1e-12
print('PASS: coherent PINEM spectroscopy, P(+n)=P(-n), handedness asymmetry')
