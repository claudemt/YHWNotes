"""MCWF unraveling of resonant two-level driven emitter."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.stats import poisson
from common import pubfig, safe_panel, safe_title, safe_colorbar, clean, finish_pub

DEST=Path(__file__).with_suffix('.pdf')
omega=1.5; gamma=0.9
T=13.; dt=0.026; steps=500
ntraj=850; rng=np.random.default_rng(20261009)
# basis ground=0, excited=1
sm=np.array([[0,1],[0,0]],complex); sp=sm.conj().T
sx=sm+sp; proj=sp@sm
H=omega*sx/2; Heff=H-0.5j*gamma*proj
M=expm(-1j*Heff*dt)
psi=np.zeros((2,ntraj),complex); psi[0,:]=1
counts=np.zeros(ntraj,dtype=int)
count_history=np.zeros((steps+1,ntraj),dtype=np.int16)
pe_history=np.empty((steps+1,ntraj),float); pe_history[0]=0
jump_raster=np.zeros((steps,ntraj),dtype=np.int8)
waiting=[]; times_since=np.zeros(ntraj)
for i in range(steps):
    candidate=M@psi
    norm2=np.sum(abs(candidate)**2,axis=0)
    jumps=rng.random(ntraj)>(norm2)
    psi=candidate/np.sqrt(np.maximum(norm2,1e-15))[None,:]
    if np.any(jumps):
        psi[:,jumps]=np.array([1.,0.])[:,None]
        waiting.extend((times_since[jumps]+dt).tolist())
        times_since[jumps]=0
    times_since[~jumps]+=dt
    counts+=jumps
    jump_raster[i]=jumps
    count_history[i+1]=counts
    pe_history[i+1]=abs(psi[1,:])**2

ts=np.arange(steps+1)*dt

def rhs(t,flattened):
    rho=flattened.reshape(2,2)
    d=-1j*(H@rho-rho@H)+gamma*(sm@rho@sp-0.5*(proj@rho+rho@proj))
    return d.ravel()

rho0=np.array([[1,0],[0,0]],complex)
sol=solve_ivp(rhs,(0,ts[-1]),rho0.ravel(),t_eval=ts,rtol=2e-10,atol=2e-11)
rhos=sol.y.T.reshape(-1,2,2)
p_master=np.real(rhos[:,1,1]); mean_pe=pe_history.mean(axis=1)
err=np.max(abs(p_master-mean_pe))
assert err<0.085,(err, 'ensemble master mismatch')
# exact unnormalized first waiting-time density (starting from ground after each jump)
unorm=np.array([expm(-1j*Heff*t)@np.array([1,0],complex) for t in ts])
w_exact=gamma*abs(unorm[:,1])**2
counts_mu=np.mean(count_history,axis=1)
counts_var=np.var(count_history,axis=1,ddof=1)
Fano=counts_var/np.maximum(counts_mu,1e-10)

fig=pubfig(8.35,6.0,top=.92,left=.07,right=.98,bottom=.08)
gs=fig.add_gridspec(2,3,wspace=.48,hspace=.60)
axes=[fig.add_subplot(gs[i//3,i%3]) for i in range(6)]
# a single quantum trajectory
ax=axes[0]
ax.plot(ts,pe_history[:,0],lw=1)
for idx in np.where(jump_raster[:,0]>0)[0]: ax.axvline(ts[idx+1],lw=.65,color='#bb542c',alpha=.8)
ax.set(xlabel=r'Time $t$',ylabel=r'Excited population $p_e$',ylim=(-.02,1.03))
safe_panel(ax,'a'); safe_title(ax,'A single detected-emission trajectory')
# b raster
ax=axes[1]; jj,jk=np.where(jump_raster[:,:70])
ax.scatter(ts[jj],jk,s=3.7,marker='|',color='#1b5b75',rasterized=True)
ax.set(xlabel=r'Time $t$',ylabel='Trajectory index',ylim=(-2,72))
safe_panel(ax,'b'); safe_title(ax,'Quantum jumps across individual records')
# c master vs MCWF mean
ax=axes[2]
ax.plot(ts,p_master,label='GKSL',lw=1.6)
ax.plot(ts,mean_pe,ls='--',label='trajectory average',lw=1.1)
ax.set(xlabel=r'Time $t$',ylabel=r'$\langle p_e\rangle$',ylim=(0,.7))
ax.legend(frameon=False,fontsize=7)
safe_panel(ax,'c');safe_title(ax,'Ensemble recovers the Lindblad master equation')
# d waiting time
ax=axes[3]
wait=np.asarray(waiting)
ax.hist(wait,bins=35,range=(0,13),density=True,color='#6694a8',alpha=.65,label='trajectory histogram')
ax.plot(ts,w_exact,label=r'$w(t)=\Gamma|c_e^{(0)}(t)|^2$',lw=1.45,color='#a64b2b')
ax.set(xlabel=r'Waiting time $\tau$',ylabel='Density',xlim=(0,7))
ax.legend(frameon=False,fontsize=6.4)
safe_panel(ax,'d'); safe_title(ax,'Non-exponential emission waiting-time density')
# e emission counts
ax=axes[4]
nmax=int(np.quantile(counts,.995))+2
bins=np.arange(-.5,nmax+1.5,1)
ax.hist(counts,bins=bins,density=True,alpha=.6,label='simulated records')
ax.plot(np.arange(nmax+1),poisson.pmf(np.arange(nmax+1),np.mean(counts)), 'o-',ms=2.5,label='Poisson, same mean')
ax.set(xlabel=r'Emitted photons $N_{\gamma}$',ylabel='Probability')
ax.legend(frameon=False,fontsize=6.7)
safe_panel(ax,'e'); safe_title(ax,'Emission counting versus Poisson baseline')
# f time-dependent photon number statistics
ax=axes[5]
ax.plot(ts[1:],Fano[1:],label='trajectory Fano factor')
ax.axhline(1,color='0.3',ls='--',lw=.85,label='Poisson baseline')
ax.set(xlabel=r'Time $t$',ylabel=r'$\mathrm{Var}(N_\gamma)/\langle N_\gamma\rangle$',ylim=(0,2.1))
ax.legend(frameon=False,fontsize=6.8)
safe_panel(ax,'f'); safe_title(ax,'Count fluctuations are not fixed by the mean')
for a in axes: clean(a)
finish_pub(fig,DEST)
assert np.max(abs(np.trace(rhos,axis1=1,axis2=2)-1))<1e-8
print('quantum trajectories pass; max deviation',err,'mean photon',np.mean(counts),'mean waiting',wait.mean())
