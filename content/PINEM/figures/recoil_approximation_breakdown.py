import common  # shared style + embedded model helpers
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub
from models.reliability_design import recoil_relative_error, exact_photon_momentum_shift, nonrecoil_q

kes=np.geomspace(1e3,3e5,150); ph=np.linspace(.5,5.0,150)
E=np.array([[recoil_relative_error(k,p,1) for p in ph] for k in kes])
E50=np.array([[recoil_relative_error(k,p,50) for p in ph] for k in kes])
orders=np.arange(1,101)
fig=pubfig(7.7,5.3,top=.91)
gs=fig.add_gridspec(2,3,wspace=.52,hspace=.58)
ax=fig.add_subplot(gs[0,0]); im=ax.pcolormesh(ph,kes/1e3,np.log10(np.maximum(E,1e-14)),shading='auto',cmap='viridis'); ax.set_yscale('log'); safe_panel(ax,'a'); safe_title(ax,'Single-photon recoil error'); ax.set_xlabel('photon energy (eV)'); ax.set_ylabel('electron kinetic energy (keV)'); safe_colorbar(fig,im,ax,label=r'$\log_{10}\epsilon_q$')
ax=fig.add_subplot(gs[0,1]); im=ax.pcolormesh(ph,kes/1e3,np.log10(np.maximum(E50,1e-14)),shading='auto',cmap='magma'); ax.set_yscale('log'); safe_panel(ax,'b'); safe_title(ax,'50-photon accumulated error'); ax.set_xlabel('photon energy (eV)'); ax.set_ylabel('electron kinetic energy (keV)'); safe_colorbar(fig,im,ax,label=r'$\log_{10}\epsilon_q$')
ax=fig.add_subplot(gs[0,2]);
for ke in [5e3,30e3,200e3]: ax.semilogy(orders,[recoil_relative_error(ke,2.4,int(n)) for n in orders],label=f'{ke/1e3:g} keV')
safe_panel(ax,'c'); safe_title(ax,'Order dependence at 2.4 eV'); ax.set_xlabel('sideband order $|n|$'); ax.set_ylabel('relative momentum error'); ax.legend(frameon=False)
ax=fig.add_subplot(gs[1,0]); photon=2.4
qex=np.array([exact_photon_momentum_shift(k,photon,1) for k in kes]); qnr=np.array([nonrecoil_q(k,photon,1) for k in kes])
delta=np.abs(qex/qnr-1); ax.loglog(kes/1e3,delta,color='#2677a8',label=r'$|q^{\rm ex}/q^{(0)}-1|$')
ax.set(xlabel='electron energy (keV)',ylabel='fractional recoil correction',ylim=(1e-7,2e-3))
safe_panel(ax,'d'); safe_title(ax,'Recoil correction, one photon')
ax=fig.add_subplot(gs[1,1]);
for en in [1.,2.4,5.]: ax.loglog(kes/1e3,[recoil_relative_error(k,en,20) for k in kes],label=f'{en:g} eV')
ax.axhline(1e-3,ls=':',c='k'); safe_panel(ax,'e'); safe_title(ax,'Practical $10^{-3}$ validity line'); ax.set_xlabel('electron energy (keV)'); ax.set_ylabel('relative error, $n=20$'); ax.legend(frameon=False)
ax=fig.add_subplot(gs[1,2]); Ls=np.geomspace(10e-9,10e-6,120)
# Phase slip in radians across a finite interaction length, with an exact recoil momentum.
for ke in [5e3,30e3,200e3]:
 dq=abs(exact_photon_momentum_shift(ke,2.4,20)-nonrecoil_q(ke,2.4,20))
 ax.loglog(Ls*1e6,dq*Ls,label=f'{ke/1e3:g} keV')
ax.axhline(.1,ls=':',c='0.3'); ax.set(xlabel='interaction length (um)',ylabel='recoil phase slip (rad)'); ax.legend(frameon=False,fontsize=7); safe_panel(ax,'f'); safe_title(ax,'Accumulated finite-length phase error')
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
