from _electron_worked_models import *
from scipy.integrate import quad
with figure_style():
    fig,ax=plt.subplots(1,2,figsize=(10,4.5))
    energy=np.linspace(-8,8,1000); beta=1.2; sigma=np.hypot(.25,.15)
    for width in [sigma,.8]: ax[0].plot(energy,spectrum(energy,beta,width),label=rf'$\sigma_E={width:.3f}$ eV')
    ax[0].set(xlabel=r'Readout offset $\varepsilon_d$ (eV)',ylabel=r'Density (eV$^{-1}$)',ylim=(0,.70))
    add_legend(ax[0],loc='upper right',fontsize=10)
    widths=np.linspace(.7,5,100)
    estimates=[]
    for w in widths:
        bound=w*photon_eV
        normal=quad(lambda x:spectrum([x],beta,sigma)[0],-bound,bound)[0]
        second=quad(lambda x:x*x*spectrum([x],beta,sigma)[0],-bound,bound)[0]/normal
        estimates.append(np.sqrt(max(0,second-sigma*sigma)/(2*photon_eV**2)))
    ax[1].plot(widths,estimates,label='Naive variance inversion')
    ax[1].axhline(beta,color='.35',ls='--',label='True coupling')
    ax[1].set(xlabel=r'Half-window $W/(\hbar\omega)$',ylabel=r'Inferred $|\beta|$',ylim=(0,1.65))
    add_legend(ax[1],loc='upper left',fontsize=10)
    finish(fig,ax,'electron_detector_forward')
