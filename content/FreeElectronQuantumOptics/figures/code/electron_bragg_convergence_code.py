from _electron_worked_models import *
with figure_style():
    fig,ax=plt.subplots(1,2,figsize=(10,4.6))
    area=np.linspace(0,2*np.pi,400)
    ax[0].plot(area/np.pi,np.sin(area/2)**2,'k--',label='Two states')
    for ratio in [.2,1,5]:
        ell,p=lattice(ratio,area)
        ax[0].plot(area/np.pi,p[26],label=rf'$r_\Omega={ratio}$')
    ax[0].set(xlabel=r'Pulse area $|\Omega|T/\pi$',ylabel=r'Transfer $P_1$',ylim=(0,1.5))
    add_legend(ax[0], ncol=2, fontsize=10)
    ratios=np.geomspace(.025,7,140)
    values=np.array([[lattice(r)[1][26,0],1-lattice(r)[1][25:27,0].sum()] for r in ratios])
    ax[1].semilogx(ratios,values[:,0],label=r'$P_1$')
    ax[1].semilogx(ratios,values[:,1],label=r'$P_{\rm leak}$')
    ax[1].set(xlabel=r'Drive ratio $|\Omega|/\omega_{\rm r}$',ylabel='Probability at a pi pulse',ylim=(0,1.4))
    add_legend(ax[1], ncol=2)
    finish(fig,ax,'electron_bragg_convergence')
