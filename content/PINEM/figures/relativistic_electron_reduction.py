"""Relativistic Dirac dispersion, spinor weights and controlled narrow-band expansion.
Dimensionless u=p/(mc) and eps=E/(mc^2), all definitions in chapter 1.
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import pubfig,safe_panel,safe_title,clean,finish_pub
OUT=Path(__file__).with_suffix('.pdf')

u=np.linspace(-3.5,3.5,450)
gamma=np.sqrt(1+u*u)
pos=np.sqrt(1+u*u)
fig=pubfig(8.3,5.9,top=.90,left=.08,right=.97,bottom=.085)
gs=fig.add_gridspec(2,3,wspace=.50,hspace=.68)
ax=[fig.add_subplot(gs[j//3,j%3]) for j in range(6)]

ax[0].plot(u,pos,label=r'$E_+$')
ax[0].plot(u,-pos,label=r'$E_-$')
ax[0].fill_between(u,-pos,pos,alpha=.08)
ax[0].set(xlabel=r'$p/(mc)$',ylabel=r'$E/(mc^2)$')
ax[0].legend(frameon=False,fontsize=7,loc='upper left')
safe_panel(ax[0],'a');safe_title(ax[0],'Positive and negative Dirac bands')

ax[1].plot(u,u/np.sqrt(1+u*u))
ax[1].axhline(1,color='0.5',ls=':',lw=.7)
ax[1].axhline(-1,color='0.5',ls=':',lw=.7)
ax[1].set(xlabel=r'$p/(mc)$',ylabel=r'$v_g/c$',ylim=(-1.08,1.08))
safe_panel(ax[1],'b');safe_title(ax[1],'Group speed approaches the light cone')

uf=np.linspace(0,3.2,180);ga=np.sqrt(1+uf*uf)
ax[2].plot(uf,ga,label='transverse mass')
ax[2].plot(uf,ga**3,label='longitudinal mass')
ax[2].set(xlabel=r'$p/(mc)$',ylabel=r'$m_{\mathrm{eff}}/m$')
ax[2].legend(frameon=False,fontsize=7,loc='upper left')
safe_panel(ax[2],'c');safe_title(ax[2],'Longitudinal and transverse curvature')

ax[3].plot(uf,(ga+1)/(2*ga),label='upper-spinor norm')
ax[3].plot(uf,(ga-1)/(2*ga),label='lower-spinor norm')
ax[3].set(xlabel=r'$p/(mc)$',ylabel='norm fraction',ylim=(0,1.06))
ax[3].legend(frameon=False,fontsize=7,loc='center right')
safe_panel(ax[3],'d');safe_title(ax[3],'Relativistic four-spinor mixing')

ax[4].plot(uf,2*ga,label=r'$E_+-E_-$')
for a,color in [(.25,'0.4'),(.75,'0.6')]:
    ax[4].axhline(a,ls='--',lw=.8,color=color,label=rf'$\hbar\omega/(mc^2)={a}$')
ax[4].set(xlabel=r'$p/(mc)$',ylabel=r'energy / $(mc^2)$')
ax[4].legend(frameon=False,fontsize=6.6,loc='upper left')
safe_panel(ax[4],'e');safe_title(ax[4],'Interband gap sets an energy scale')

du=np.geomspace(.015,.8,130)
for u0 in [.5,2,5]:
    gg=np.sqrt(1+u0*u0)
    exactly=np.sqrt(1+(u0+du)**2)
    approx=gg+(u0/gg)*du+(du**2)/(2*gg**3)
    ax[5].loglog(du,np.abs(exactly-approx),label=rf'$p_0/(mc)={u0:g}$')
ax[5].set(xlabel=r'$\Delta p/(mc)$',ylabel=r'$|\Delta E_{\mathrm{Taylor}}|/(mc^2)$')
ax[5].legend(frameon=False,fontsize=6.7,loc='lower right')
safe_panel(ax[5],'f');safe_title(ax[5],'Error of the quadratic energy expansion')

for a in ax:clean(a)
finish_pub(fig,OUT)
print('Saved',OUT, 'max gamma',ga[-1], 'p0=2 expansion error at dp=.8', abs(np.sqrt(1+(2+.8)**2) -(np.sqrt(5)+2/np.sqrt(5)*.8+.8**2/(2*5**1.5))))
