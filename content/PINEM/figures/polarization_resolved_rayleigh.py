"""Six aligned panels: the two Rayleigh dipole fields and their coherent couplings.
A companion six-panel spectroscopy figure is polarization_resolved_spectroscopy.py.
"""
from pathlib import Path
import sys
import numpy as np
from scipy.special import kv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from preamble import pubfig, safe_colorbar, clean, finish_pub, COLORS
from polarization_model import (radius as a, kappa, incident_field as E0, beta_scale,
                                beta_parts, beta, field_z, integrate_beta,
                                cancellation_angle, check)

fig=pubfig()
axs=[fig.add_subplot(2,3,j+1) for j in range(6)]
b0=2*a

# (a) Signed field along a real electron trajectory.
z=np.linspace(-5,5,501)
for component, style, label in [('transverse',COLORS['blue'],r'$p_b$'),
                                ('longitudinal',COLORS['orange'],r'$p_z$')]:
    axs[0].plot(z,np.real(field_z(z*a,b0,component)/E0),color=style,label=label)
axs[0].axhline(0,color='.6',lw=.6)
axs[0].set(xlabel=r'$z/a$',ylabel=r'$\operatorname{Re}(E_{\omega,z}/E_0)$')
axs[0].legend(frameon=False,loc='upper right')

# (b) The analytically different Bessel kernels, with quadrature checkpoints.
scales=np.linspace(1.12,5.0,110)
impacts=scales*a
bb,bz=beta_parts(impacts)
axs[1].plot(scales,abs(bb/beta_scale),color=COLORS['blue'],label=r'$K_1$')
axs[1].plot(scales,abs(bz/beta_scale),color=COLORS['orange'],label=r'$K_0$')
checkpoints=np.array([1.2,1.7,2.2,3.,4.4])
for component,color in [('transverse',COLORS['blue']),('longitudinal',COLORS['orange'])]:
    v=np.array([integrate_beta(u*a,component) for u in checkpoints])
    axs[1].scatter(checkpoints,abs(v/beta_scale),s=17,facecolors='white',edgecolors=color,zorder=4)
axs[1].set(xlabel=r'$b/a$',ylabel=r'$|\beta_\alpha/B|$')
axs[1].legend(frameon=False,loc='upper right')

# (c) Coherent versus separately populated dipole components as impact changes.
axs[2].plot(scales,abs(bb),color=COLORS['blue'],label=r'$p_b$')
axs[2].plot(scales,abs(bz),color=COLORS['orange'],label=r'$p_z$')
axs[2].plot(scales,abs(beta(impacts,np.pi/4,-np.pi/2)),color=COLORS['green'],label='coherent')
axs[2].set(xlabel=r'$b/a$',ylabel=r'$|\beta|$')
axs[2].legend(frameon=False,loc='upper right')

# (d) Real contribution to the Fourier integrand, with odd/even field parity.
zs=np.linspace(-7,7,701)
for component,color,label in [('transverse',COLORS['blue'],r'$p_b$'),
                               ('longitudinal',COLORS['orange'],r'$p_z$')]:
    value=field_z(a*zs,b0,component)*np.exp(-1j*kappa*a*zs)/E0
    axs[3].plot(zs,np.real(value),color=color,label=label)
axs[3].axhline(0,color='.6',lw=.6)
axs[3].set(xlabel=r'$z/a$',ylabel=r'$\operatorname{Re}[E_{\omega,z}\mathrm{e}^{-\mathrm{i}\kappa z}]/E_0$')
axs[3].legend(frameon=False,loc='upper right')

# (e) Interference magnitude over two real polarization controls.
theta=np.linspace(0,np.pi/2,161)
delta=np.linspace(-np.pi,np.pi,241)
TH,DE=np.meshgrid(theta,delta)
field=abs(beta(b0,TH,DE))
im=axs[4].imshow(field,extent=[0,90,-180,180],origin='lower',aspect='auto',
                 cmap='viridis',vmin=0,vmax=1.3)
null=np.degrees(cancellation_angle(b0))
axs[4].plot(null,-90,marker='o',color='white',markeredgecolor='.2',markersize=5)
axs[4].set(xlabel=r'$\theta$ (deg)',ylabel=r'$\delta$ (deg)')
safe_colorbar(fig,im,axs[4],r'$|\beta|$')

# (f) Locus in the complex coupling plane while one phase winds through 2pi.
angles=np.linspace(-np.pi,np.pi,501)
combined=beta(b0,cancellation_angle(b0),angles)
coordinates=combined/beta_scale
axs[5].plot(coordinates.real,coordinates.imag,color=COLORS['blue'])
axs[5].scatter([0],[0],marker='+',s=90,c=COLORS['orange'],zorder=5)
axs[5].scatter([coordinates[0].real],[coordinates[0].imag],s=21,c=COLORS['green'],zorder=6)
axs[5].axhline(0,color='.8',lw=.6);axs[5].axvline(0,color='.8',lw=.6)
axs[5].set(xlabel=r'$\operatorname{Re}(\beta/B)$',ylabel=r'$\operatorname{Im}(\beta/B)$')
axs[5].set_aspect('auto')

for ax in axs:clean(ax)
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
assert check()
print('PASS: polarization near-field panel data and Fourier quadrature')
