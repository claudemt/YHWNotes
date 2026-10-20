import common  # shared style + embedded model helpers
import sys; from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from scipy.constants import c,e,hbar
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
from models.pinem_core import spp_dispersion,electron_relativistic,dipole_nearfield_Ez,pinem_g_from_field,field_decay_length_cylinder

fig=pubfig(7.5,5.8,top=.91); gs=fig.add_gridspec(2,3,wspace=.48,hspace=.65)
# a dispersion
ax=fig.add_subplot(gs[0,0]); wp=9.1*e/hbar; k=np.linspace(.001,18,700)*1e7; w=spp_dispersion(k,wp); ax.plot(k/1e7,hbar*w/e,label='SPP'); ax.plot(k/1e7,hbar*c*k/e,'--',label='photon')
rel=electron_relativistic(200e3); ax.plot(k/1e7,hbar*rel['v']*k/e,':',label='200 keV electron')
ax.axhline(9.1/np.sqrt(2),lw=.8,ls='-.'); ax.set(xlabel='$k_\\parallel$ ($10^7$ m$^{-1}$)',ylabel='Energy (eV)',ylim=(0,8)); ax.legend(frameon=False,ncol=3); safe_panel(ax,'a'); safe_title(ax,'Surface-plasmon phase matching'); clean(ax)
# b phase velocity
ax=fig.add_subplot(gs[0,1]); mask=w>0; ax.plot(hbar*w[mask]/e,w[mask]/k[mask]/c,label='$v_\\phi/c$'); ax.axhline(rel['beta'],ls='--',lw=.9,label='electron'); ax.set(xlabel='SPP energy (eV)',ylabel='Velocity / $c$',ylim=(0,1.05)); ax.legend(frameon=False); safe_panel(ax,'b'); safe_title(ax,'Velocity crossing'); clean(ax)
# c real field
ax=fig.add_subplot(gs[1,0]); z=np.linspace(-500,500,1000)*1e-9; Ez=dipole_nearfield_Ez(z,70e-9); Ez/=np.max(np.abs(Ez)); ax.plot(z*1e9,Ez.real); ax.plot(z*1e9,np.abs(Ez),'--'); ax.set(xlabel='$z$ (nm)',ylabel='$E_z$ (norm.)'); safe_panel(ax,'d'); safe_title(ax,'Longitudinal near field'); clean(ax)
# d spatial spectrum
ax=fig.add_subplot(gs[1,1]); dz=z[1]-z[0]; F=np.fft.fftshift(np.fft.fft(np.fft.ifftshift(Ez))); kk=np.fft.fftshift(np.fft.fftfreq(len(z),dz))*2*np.pi; ax.plot(kk/1e7,np.abs(F)/np.max(np.abs(F)))
for ke in [30,60,120,200]: r=electron_relativistic(ke*1e3); kz=(2*np.pi*c/519e-9)/r['v']; ax.axvline(kz/1e7,lw=.7,alpha=.7)
ax.set(xlabel='$k_z$ ($10^7$ m$^{-1}$)',ylabel='Fourier amplitude',xlim=(0,12)); safe_panel(ax,'e'); safe_title(ax,'Momentum supplied by near field'); clean(ax)
# e decay length
ax=fig.add_subplot(gs[1,2]); lam=np.linspace(350,900,250)*1e-9
for ke in [30,60,120,200]: ax.plot(1240/(lam*1e9),np.array([field_decay_length_cylinder(L,ke*1e3) for L in lam])*1e9,label=f'{ke} keV')
ax.set(xlabel='Photon energy (eV)',ylabel='Phase-matched decay length (nm)'); ax.legend(frameon=False,fontsize=7.0); safe_panel(ax,'f'); safe_title(ax,'Electron-energy control of confinement'); clean(ax)
# c: Fourier overlap as electron energy changes, at fixed 519 nm.
ax=fig.add_subplot(gs[0,2]); kin=np.geomspace(2e3,2.5e5,100)
om=2*np.pi*c/519e-9
arr=np.array([abs(np.interp((om/electron_relativistic(Ee)['v']),kk,np.abs(F),left=0,right=0)) for Ee in kin])
ax.semilogx(kin/1e3,arr/max(arr.max(),1e-30)); ax.set(xlabel='electron kinetic energy (keV)',ylabel='normalized field overlap',ylim=(0,1.05)); safe_panel(ax,'c'); safe_title(ax,'Trajectory Fourier overlap'); clean(ax)
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
