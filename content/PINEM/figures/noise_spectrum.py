from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pubfig, clean, safe_panel, finish_pub

fig, axs = plt.subplots(2,3,figsize=(10.6,7.9),constrained_layout=True)
axs=axs.ravel()
w=np.logspace(-2,2,500); spectra={'white':np.ones_like(w),'OU':1/(1+w*w),'narrow':.08/((w-5)**2+.08)}
for k,s in spectra.items(): axs[0].loglog(w,s/np.trapezoid(s,w),label=k)
axs[0].set_xlabel('$\\omega\\tau$'); axs[0].set_ylabel('normalized $S(\\omega)$'); axs[0].legend()
T=np.logspace(-1,1,180)
for k,s in spectra.items():
 vals=[]
 for tt in T:
  F=4*np.sin(w*tt/2)**2; vals.append(np.trapezoid(s*F/(w*w+1e-12),w)/np.trapezoid(s,w))
 axs[1].loglog(T,vals,label=k)
axs[1].set_xlabel('$T/\\tau$'); axs[1].set_ylabel('$\\chi(T)$'); axs[1].legend()
W,Tm=np.meshgrid(w,T); F=4*np.sin(W*Tm/2)**2/(W*W+1e-12); im=axs[2].pcolormesh(w,T,F,shading='auto'); axs[2].set_xscale('log'); axs[2].set_yscale('log'); axs[2].set_xlabel('$\\omega$'); axs[2].set_ylabel('$T$'); fig.colorbar(im,ax=axs[2],label='filter weight')
for k,sp in spectra.items():
 vals=np.array([np.trapezoid(sp*4*np.sin(w*tt/2)**2/(w*w+1e-12),w)/np.trapezoid(sp,w) for tt in T])
 # Time-local dephasing rate d chi/dT from the *same* non-Markovian overlap.
 # Its negative segments (if any) indicate coherence revivals, not an independently fitted decay channel.
 axs[3].plot(T,np.gradient(vals,T),label=k)
axs[3].axhline(0,ls=':',lw=.8,color='0.4')
axs[3].set_xscale('log'); axs[3].set(xlabel=r'$T/\tau$',ylabel=r'$\mathrm{d}\chi/\mathrm{d}T$',title='Time-local dephasing rate'); axs[3].legend(fontsize=7)
# e: coherence from exactly the same filter overlap, no independent damping rate.
for name,sp in spectra.items():
 vals=np.array([np.trapezoid(sp*4*np.sin(w*tt/2)**2/(w*w+1e-12),w)/np.trapezoid(sp,w) for tt in T])
 axs[4].semilogx(T,np.exp(-vals),label=name)
axs[4].set(xlabel=r'$T/\tau$',ylabel=r'$\exp[-\chi(T)]$',title='Coherence from spectral overlap')
axs[4].legend(fontsize=7)
# f: the explicit experimental/numerical bandwidth assumption: for each cutoff
# renormalize the OU spectrum over the retained discrete nodes.
sp=spectra['OU']
for cutoff in [.3,1.,3.,10.]:
 mask=w<=cutoff
 ww=w[mask]; ss=sp[mask]
 vals=np.array([np.trapezoid(ss*4*np.sin(ww*tt/2)**2/(ww*ww+1e-12),ww)/np.trapezoid(ss,ww) for tt in T])
 axs[5].semilogx(T,np.exp(-vals),label=fr'$\omega_c={cutoff:g}$')
axs[5].set(xlabel=r'$T/\tau$',ylabel='OU coherence',title='Bandwidth-dependent dephasing')
axs[5].legend(fontsize=7)
for i,ax in enumerate(axs):
    clean(ax); safe_panel(ax,chr(97+i))
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
