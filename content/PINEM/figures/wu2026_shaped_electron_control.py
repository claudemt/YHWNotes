import common  # shared style + embedded model helpers
import sys; from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,clean,finish_pub
from models.wu2026 import electron_autocorr,steady_state,coherence,config,V0,OMEGA_PINEM
fig=pubfig(7.5,5.9,top=.91); gs=fig.add_gridspec(2,3,wspace=.46,hspace=.66)
# a autocorrelation vs propagation
ax=fig.add_subplot(gs[0,0]); L=np.linspace(.02,.28,220); w31,w32=config(1); I31=np.array([electron_autocorr(w31/V0,2.2,l) for l in L]); I32=np.array([electron_autocorr(w32/V0,2.2,l) for l in L]); ax.plot(L,np.abs(I31),label='$|I_{31}|$'); ax.plot(L,np.abs(I32),label='$|I_{32}|$'); ax.set(xlabel='Propagation length $L_p$ (m)',ylabel='Electron autocorrelation'); ax.legend(frameon=False); safe_panel(ax,'a'); safe_title(ax,'Shaped-electron spectral coherence'); clean(ax)
# b phase
ax=fig.add_subplot(gs[0,1]); ax.plot(L,np.unwrap(np.angle(I31)),label=r'$\arg I_{31}$'); ax.plot(L,np.unwrap(np.angle(I32)),label=r'$\arg I_{32}$'); ax.set(xlabel='$L_p$ (m)',ylabel='Phase (rad)'); ax.legend(frameon=False); safe_panel(ax,'b'); safe_title(ax,'Free propagation tunes quantum phase'); clean(ax)
# c control points
ax=fig.add_subplot(gs[0,2]); pts=[(1.1,.08),(2.2,.10),(3.2,.14),(4.0,.20)];
for g,Lp in pts:
    r=steady_state(g,Lp,1); ax.scatter(r[0,0].real,r[1,1].real,s=35,label=f'$g={g},L={Lp}$')
ax.plot([0,1,0,0],[0,0,1,0],color='.75',lw=.8); ax.set(xlabel=r'$\rho_{11}$',ylabel=r'$\rho_{22}$',xlim=(0,1),ylim=(0,1)); ax.legend(frameon=False,fontsize=7.0); safe_panel(ax,'c'); safe_title(ax,'Reachable ground-state populations'); clean(ax)
# d-e coarse maps
G=np.linspace(.8,4.2,13); LP=np.linspace(.04,.24,15); P1=np.zeros((len(LP),len(G))); C12=np.zeros_like(P1)
for i,l in enumerate(LP):
  for j,g in enumerate(G):
    r=steady_state(g,l,1); P1[i,j]=r[0,0].real; C12[i,j]=coherence(r,0,1)
ax=fig.add_subplot(gs[1,0]); im=ax.imshow(P1,origin='lower',aspect='auto',extent=[G.min(),G.max(),LP.min(),LP.max()],cmap='RdYlBu_r',vmin=0,vmax=1); ax.set(xlabel=r'PINEM shaping strength $|g_m|$',ylabel='$L_p$ (m)'); safe_colorbar(fig,im,ax,r'$\rho_{11}$'); safe_panel(ax,'d'); safe_title(ax,'Steady-state population control landscape')
ax=fig.add_subplot(gs[1,1]); im=ax.imshow(C12,origin='lower',aspect='auto',extent=[G.min(),G.max(),LP.min(),LP.max()],cmap='viridis',vmin=0,vmax=1); ax.set(xlabel='$|g_m|$',ylabel='$L_p$ (m)'); safe_colorbar(fig,im,ax,'coherence'); safe_panel(ax,'e'); safe_title(ax,'Ground-state coherence landscape')
# f: fixed-propagation cut distinguishes population from coherence tuning.
ax=fig.add_subplot(gs[1,2]); j=np.argmin(abs(LP-.12)); ax.plot(G,P1[j],label=r'$\rho_{11}$'); ax.plot(G,C12[j],label=r'$C_{12}$')
ax.set(xlabel=r'$|g_m|$',ylabel='state observable'); ax.legend(frameon=False,fontsize=7); safe_panel(ax,'f'); safe_title(ax,'Control cut at L=0.12 m'); clean(ax)
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
