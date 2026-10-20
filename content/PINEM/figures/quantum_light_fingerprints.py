import common  # shared style + embedded model helpers
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
import numpy as np, matplotlib.pyplot as plt
from preamble import pubfig,safe_panel,safe_title,safe_colorbar,finish_pub,clean
from models import novel_extensions as ne
from models.all_paper_reconstructions import photon_number_distributions

OUT=Path(__file__).with_suffix('.pdf')
res=ne.quantum_light_spectra(ne=8,nph=34,mean=10,pulse_area=.38)
fig=pubfig(9.0,6.2,top=.92,left=.07,right=.97,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.55,hspace=.58)
ax=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]

# a: electron spectra fingerprints
for k in ['coherent','fock','thermal','squeezed']:
    n,pe,pp,P,psi=res[k]
    ax[0].plot(n,pe,'o-',ms=2.5,label=k)
ax[0].legend(frameon=False,ncol=2,fontsize=7.3)
ax[0].set(xlabel='electron order $n$',ylabel='probability')
safe_title(ax[0],'Electron spectra distinguish photon statistics')
safe_panel(ax[0],'a')

# b: input photon number statistics
nph,dist=photon_number_distributions(mean=10,nmax=35,squeeze_r=np.arcsinh(np.sqrt(10)))
for key in ['coherent','fock','thermal','squeezed']:
    ax[1].plot(nph,dist[key],label=key)
ax[1].set(xlim=(0,30),xlabel='photon number $m$',ylabel='probability')
ax[1].legend(frameon=False,ncol=2,fontsize=7.3)
safe_title(ax[1],'Same mean, different optical fluctuations')
safe_panel(ax[1],'b')

# c: joint ladder for number state
n,pe,pp,P,psi=res['fock']
im=ax[2].imshow(P.T,origin='lower',aspect='auto',extent=[n[0]-.5,n[-1]+.5,-.5,P.shape[1]-.5],cmap='magma')
safe_colorbar(fig,im,ax[2],'joint probability')
ax[2].set(xlabel='electron order $n$',ylabel='photon number $m$')
safe_title(ax[2],'Joint energy ladder for a Fock-state input')
safe_panel(ax[2],'c')

# d: heralded nonclassicality map
areas=np.linspace(.08,.72,34)
heralds=np.arange(-4,5)
A,H,F,G,Pr=ne.heralded_nonclassicality_map(mean=8.0,areas=areas,heralds=heralds,ne=7,nph=28)
im=ax[3].imshow(F,origin='lower',aspect='auto',extent=[A[0],A[-1],H[0],H[-1]],cmap='viridis',vmin=0.6,vmax=1.8)
safe_colorbar(fig,im,ax[3],'conditional Fano factor')
ax[3].contour(A,H,Pr,levels=[0.02,0.08],colors='w',linewidths=0.7,alpha=0.85)
ax[3].set(xlabel='interaction area',ylabel='electron herald $n$')
safe_title(ax[3],'Electron heralding reshapes photon statistics')
safe_panel(ax[3],'d')

# e: entanglement entropy scaling by input light state
means=np.linspace(1,18,18)
for key,kwargs in [
    ('coherent',{}),
    ('fock',{}),
    ('squeezed',{'squeeze_r':0.9})
]:
    vals=[]
    for mu in means:
        if key=='squeezed':
            rr=np.arcsinh(np.sqrt(mu))
            n,m,P,psi=ne.quantum_pinem_joint(key,ne=6,nph=max(28,int(mu+8*np.sqrt(mu)+8)),mean=1,pulse_area=.34,squeeze_r=rr)
        else:
            n,m,P,psi=ne.quantum_pinem_joint(key,ne=6,nph=max(28,int(mu+8*np.sqrt(mu)+8)),mean=float(mu),pulse_area=.34)
        vals.append(ne.bipartite_entropy_from_state(psi,6,max(28,int(mu+8*np.sqrt(mu)+8)))[0])
    ax[4].plot(means,vals,label=key)
ax[4].set(xlabel='mean photon number',ylabel='entropy [bits]')
ax[4].legend(frameon=False,fontsize=7.2)
safe_title(ax[4],'Electron--photon entanglement budget')
safe_panel(ax[4],'e')

# f: conditional optical state after an electron herald
m,pn,prob,nav,g2,c=ne.heralded_photon_state(mean=8,pulse_area=.45,herald_n=2,ne=7,nph=30)
_,dist0=photon_number_distributions(mean=8,nmax=31,squeeze_r=1.0)
ax[5].plot(m,dist0['coherent'][:len(m)],label='input coherent state')
ax[5].plot(m,pn,label=fr'conditioned on $n=+2$ (success={prob:.2f})')
ax[5].text(.98,.96,fr'$\bar m_{{\rm cond}}={nav:.2f}$',transform=ax[5].transAxes,ha='right',va='top',fontsize=7.8)
ax[5].text(.98,.86,fr'$g^{{(2)}}_{{\rm cond}}(0)={g2:.2f}$',transform=ax[5].transAxes,ha='right',va='top',fontsize=7.8)
ax[5].set(xlim=(0,18),xlabel='photon number $m$',ylabel='probability')
ax[5].legend(frameon=False,fontsize=7.0,loc='lower right')
safe_title(ax[5],'Measurement back-action on the optical mode')
safe_panel(ax[5],'f')

for a in ax:
    clean(a)
finish_pub(fig,OUT)
