import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from preamble import save as book_save
"""A complete, explicitly phenomenological PINEM detector/inference problem.
The model includes spatial illumination, energy sidebands, detector mixing,
Poisson counts, likelihood and Fisher information without hidden calibration.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import common  # shared publication typography and figure style
from scipy.special import jv

X=np.linspace(-2.4,2.4,23)
N=np.arange(-7,8)
N_COUNT=45000
BKG=1.5
SIG_B=1.30
G_TRUE,W_TRUE=2.1,.90
SIGX=.25
SIGE=.48
DELTA=.008
RNG=np.random.default_rng(27)
beam=np.exp(-.5*(X/SIG_B)**2);beam/=beam.sum()

def kernel(points,sigma):
    k=np.exp(-.5*((points[:,None]-points[None,:])/sigma)**2)
    return k/k.sum(axis=0,keepdims=True)
KX=kernel(X,SIGX)

def ideal(g,w):
    amplitudes=g*np.exp(-.5*(X/w)**2)
    q=beam[:,None]*jv(N[None,:],2*amplitudes[:,None])**2
    return q/q.sum()

def predicted(g,w,sige=SIGE,spatial=True):
    kE=kernel(N,sige)
    q=KX@ideal(g,w)@kE.T
    if not spatial:q=q.sum(axis=0)
    return N_COUNT*q+BKG if spatial else N_COUNT*q+len(X)*BKG

def fisher(g,w,sige=SIGE,spatial=True):
    mu=predicted(g,w,sige,spatial)
    p1=(predicted(g+DELTA,w,sige,spatial)-predicted(g-DELTA,w,sige,spatial))/(2*DELTA)
    p2=(predicted(g,w+DELTA,sige,spatial)-predicted(g,w-DELTA,sige,spatial))/(2*DELTA)
    F=np.array([[np.sum(p1*p1/mu),np.sum(p1*p2/mu)],
                [np.sum(p1*p2/mu),np.sum(p2*p2/mu)]])
    return F

q0=ideal(G_TRUE,W_TRUE)
mu0=predicted(G_TRUE,W_TRUE)
y=RNG.poisson(mu0)
G_GRID=np.linspace(1.91,2.31,61)
W_GRID=np.linspace(.73,1.10,61)
NLL=np.empty((len(W_GRID),len(G_GRID)))
for iw,w in enumerate(W_GRID):
    for ig,g in enumerate(G_GRID):
        m=predicted(g,w)
        NLL[iw,ig]=np.sum(m-y*np.log(m))
delta=2*(NLL-NLL.min())
pos=np.unravel_index(np.argmin(NLL),NLL.shape)
G_HAT,W_HAT=G_GRID[pos[1]],W_GRID[pos[0]]

fig,axs=plt.subplots(2,3,figsize=(11.4,7.0),layout='constrained');axs=axs.ravel()
extent=[N[0]-.5,N[-1]+.5,X[0]-.1,X[-1]+.1]
a=axs[0];im=a.imshow(q0,origin='lower',extent=extent,aspect='auto',cmap='magma')
a.set(xlabel='energy order $n$',ylabel=r'probe position $x/w_0$');fig.colorbar(im,ax=a,shrink=.88,label='ideal joint probability')
a=axs[1];im=a.imshow(mu0,origin='lower',extent=extent,aspect='auto',cmap='magma')
a.set(xlabel='energy order $n$',ylabel=r'probe position $x/w_0$');fig.colorbar(im,ax=a,shrink=.88,label='expected counts')
a=axs[2];im=a.imshow(y,origin='lower',extent=extent,aspect='auto',cmap='magma')
a.set(xlabel='energy order $n$',ylabel=r'probe position $x/w_0$');fig.colorbar(im,ax=a,shrink=.88,label='Poisson counts')
a=axs[3]
a.errorbar(N,y.sum(axis=0),yerr=np.sqrt(np.maximum(y.sum(axis=0),1)),fmt='o',markersize=3,capsize=2,label='observed')
a.plot(N,predicted(G_HAT,W_HAT).sum(axis=0),'-',label='fitted forward model')
a.set(xlabel='energy order $n$',ylabel='spatially integrated counts');a.legend(frameon=False)
a=axs[4];im=a.imshow(np.minimum(delta,26),origin='lower',extent=[G_GRID[0],G_GRID[-1],W_GRID[0],W_GRID[-1]],aspect='auto',cmap='viridis_r')
a.contour(G_GRID,W_GRID,delta,levels=[2.30,6.18],colors=['white','#f3bb51'],linewidths=[1.2,1.3])
a.plot(G_TRUE,W_TRUE,'x',ms=8,mew=2,color='#ed4760',label='true')
a.plot(G_HAT,W_HAT,'+',ms=9,mew=1.8,color='white',label='MLE')
a.set(xlabel=r'amplitude $g_0$',ylabel=r'near-field width $w/w_0$');a.legend(frameon=False,loc='upper right')
fig.colorbar(im,ax=a,shrink=.88,label=r'$2\Delta(-\ln\mathcal{L})$')
a=axs[5];spec=np.linspace(.12,1.22,35)
for spatial,legend in [(True,'resolved $x,n$'),(False,'energy-only')]:
    lam=[np.linalg.eigvalsh(fisher(G_TRUE,W_TRUE,s,spatial))[0]/N_COUNT for s in spec]
    a.plot(spec,lam,label=legend)
a.set(xlabel=r'energy blur $\sigma_E/(\hbar\omega)$',ylabel=r'$\lambda_{\min}(F)/N_{\mathrm{e}}$')
a.legend(frameon=False)
titles=['(a) Ideal joint PINEM distribution','(b) Detector-averaged expectation',
        '(c) Noisy measured events','(d) Spectral fit to the same counts',
        '(e) Full two-parameter likelihood','(f) Joint versus marginal information']
for ax,t in zip(axs,titles):ax.set_title(t,loc='left',pad=8,fontweight='bold')
book_save(fig,Path(__file__).with_suffix('.pdf'))
print('MLE g,width=',G_HAT,W_HAT,'signal total=',mu0.sum(),'data total=',y.sum())
