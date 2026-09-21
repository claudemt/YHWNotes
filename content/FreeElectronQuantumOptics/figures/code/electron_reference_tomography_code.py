from _electron_worked_models import *
with figure_style():
    fig,ax=plt.subplots()
    phase=np.linspace(0,2*np.pi,500)
    ax.plot(phase/np.pi,reference(phase),label='With coherence')
    ax.plot(phase/np.pi,reference(phase,coherence=0),ls='--',label='Same spectrum, phase mixed')
    scans=np.arange(4)*np.pi/2
    p=reference(scans)
    ax.errorbar(scans/np.pi,p,yerr=np.sqrt(p*(1-p)/1e4),fmt='o',color='black',capsize=4,label='Four settings')
    ax.set(xlabel=r'Reference phase $\varphi_R/\pi$',ylabel=r'Central-channel probability $P_0$',ylim=(.30,.87))
    add_legend(ax, fontsize=11)
    finish(fig,ax,'electron_reference_tomography')
