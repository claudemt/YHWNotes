from _electron_worked_models import *
with figure_style():
    fig,ax=plt.subplots(1,2,figsize=(10,4.3))
    mismatch=np.linspace(-10,10,700)
    beta=1/photon_eV
    ax[0].plot(mismatch,np.sinc(mismatch/(2*np.pi)))
    ax[0].axhline(0,color='.6',lw=1)
    ax[0].set(xlabel=r'Mismatch $\Delta\kappa L_{\rm int}$',ylabel=r'$\beta/\beta_{\rm sync}$')
    ell=np.arange(-5,6)
    ax[1].bar(ell,jv(ell,2*beta)**2,color='#2874a6',width=.68)
    ax[1].set(xlabel=r'Electron order $\ell$',ylabel=r'Probability $P_\ell$',ylim=(0,.45))
    ax[1].set_xticks([-4,-2,0,2,4])
    finish(fig,ax,'electron_field_calibration')
