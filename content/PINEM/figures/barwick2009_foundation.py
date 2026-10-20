import common  # shared style + embedded model helpers
import sys; from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
from models.pinem_core import bessel_populations,temporal_bessel_population,impact_coupling,coherent_spectrum

fig=pubfig(7.5,5.7,top=.91); gs=fig.add_gridspec(2,3,wspace=.42,hspace=.62)
# a sidebands
ax=fig.add_subplot(gs[0,0]); E=np.linspace(-25,25,1200); y=coherent_spectrum(E,2.4,2.8,.38,10); ax.plot(E,y); ax.set(xlabel='Energy shift (eV)',ylabel='Normalized intensity',xlim=(-24,24)); safe_panel(ax,'a'); safe_title(ax,'Multiphoton energy ladder'); clean(ax)
# b populations
ax=fig.add_subplot(gs[0,1]); n,p=bessel_populations(2.8,10); ax.stem(n,p,basefmt=' '); ax.set(xlabel='Photon order $n$',ylabel='$P_n$',xlim=(-9.5,9.5)); safe_panel(ax,'b'); safe_title(ax,'Coherent sideband weights'); clean(ax)
# c spatial field
ax=fig.add_subplot(gs[0,2]); b=np.linspace(70,400,320)*1e-9; g=impact_coupling(b,L=50e-9,g_surface=2.8,b0=70e-9); signal=1-np.array([bessel_populations(x,12)[1][12] for x in g]); ax.semilogy(b*1e9,np.maximum(signal,1e-5)); ax.set(xlabel='Distance from nanostructure (nm)',ylabel='Gain/loss fraction',ylim=(1e-4,1)); safe_panel(ax,'c'); safe_title(ax,'Evanescent spatial gate'); clean(ax)
# d temporal orders
ax=fig.add_subplot(gs[1,0]); t=np.linspace(-700,700,500)
for n in [1,2,3,4]: ax.plot(t,temporal_bessel_population(t,n,2.8,180,110),label=f'$|n|={n}$')
ax.set(xlabel='Electron-photon delay (fs)',ylabel='Sideband probability',xlim=(-650,650)); ax.legend(ncol=2,frameon=False,fontsize=7,loc='upper right'); safe_panel(ax,'d'); safe_title(ax,'Nonlinear temporal gating'); clean(ax)
# e field movie proxy
ax=fig.add_subplot(gs[1,1]); x=np.linspace(-300,300,260); tt=np.linspace(-450,450,220); X,T=np.meshgrid(x,tt); Z=np.exp(-np.abs(X)/75)*np.exp(-(T/230)**2)*(1+0.35*np.cos(2*np.pi*T/180)); im=ax.imshow(Z,origin='lower',aspect='auto',extent=[x.min(),x.max(),tt.min(),tt.max()],cmap='magma'); ax.set(xlabel='Transverse position (nm)',ylabel='Delay (fs)'); safe_colorbar(fig,im,ax,'PINEM signal'); safe_panel(ax,'e'); safe_title(ax,'Space-time near-field movie')
# f: resolved high-order population as a function of the *same* Bessel coupling.
ax=fig.add_subplot(gs[1,2]); bb=np.linspace(0,4.5,180)
for cutoff in (1,3,5):
    tail=np.array([sum(bessel_populations(float(q),18)[1][abs(bessel_populations(float(q),18)[0])>=cutoff]) for q in bb])
    ax.plot(bb,tail,label=fr'$|n|\geq {cutoff}$')
ax.set(xlabel=r'$|\beta|$',ylabel='tail probability',ylim=(0,1.05)); ax.legend(frameon=False,fontsize=7); safe_panel(ax,'f'); safe_title(ax,'High-order spectral occupancy'); clean(ax)
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
