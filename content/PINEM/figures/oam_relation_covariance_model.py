"""Two-loop energy-OAM relation model; finite Fourier exact noise tomography.

This is a calibrated effective four-history endpoint measurement, not a claimed
Maxwell-validated implementation or a new microscopic free-electron Hamiltonian.
"""
import numpy as np
from scipy.linalg import null_space

A=np.array([[1,1,2,0],[1,-1,0,2]],dtype=int)
U=np.array([[1,1],[1,-1],[-1,0],[0,-1]],dtype=int) # columns u,v
H0=np.array([0,1,1,1],dtype=int)
HISTORIES=np.array([H0,H0+U[:,0],H0+U[:,1],H0+U[:,0]+U[:,1]],dtype=int)
# Relative relation phases (0,u,v,u+v)
WINDINGS=np.array([[0,0],[1,0],[0,1],[1,1]],dtype=int)
AMPS=np.array([.24,.18,.16,.20*np.exp(.35j)],dtype=complex)
G_TRUE=np.array([[.36,.12],[.12,.25]])
BASIS=null_space(U.T)
assert np.array_equal(A@U,np.zeros((2,2),dtype=int))
assert (HISTORIES>=0).all()
assert np.array_equal((A@HISTORIES.T).T,np.tile(np.array([3,1]),(4,1)))

def covariance_from_projection(G,blind=0.):
    """Return a PSD 4x4 covariance with U.T Sigma U=G."""
    G=np.asarray(G,dtype=float)
    D=U@np.linalg.inv(U.T@U)
    return D@G@D.T+blind**2*(BASIS@BASIS.T)

def coeffs(G=None):
    """Four-history exact probability Fourier coefficients for relation angles."""
    if G is None:G=np.zeros((2,2))
    ans={}
    for j,kj in enumerate(WINDINGS):
        for l,kl in enumerate(WINDINGS):
            h=tuple((kj-kl).tolist())
            d=np.array(h,dtype=float)
            ans[h]=ans.get(h,0j)+AMPS[j]*np.conj(AMPS[l])*np.exp(-.5*d@G@d)
    return ans

def probability(phi_u,phi_v,G=None):
    z=np.asarray(phi_u);w=np.asarray(phi_v)
    ans=np.zeros(np.broadcast_shapes(z.shape,w.shape),dtype=complex)
    for (m,n),c in coeffs(G).items():ans=ans+c*np.exp(1j*(m*z+n*w))
    return ans.real

def fisher_grid(G,grid=24):
    """Per-electron Bernoulli Fisher for three entries [G11,G22,G12]."""
    p=np.arange(grid)*2*np.pi/grid
    X,Y=np.meshgrid(p,p,indexing='ij')
    P=probability(X,Y,G)
    d=np.zeros((3,grid,grid),float)
    for (m,n),c in coeffs(G).items():
        osc=c*np.exp(1j*(m*X+n*Y))
        d[0]+=-.5*m*m*osc.real
        d[1]+=-.5*n*n*osc.real
        d[2]+=-m*n*osc.real
    D=d.reshape(3,-1)
    return (D/np.sqrt((P*(1-P)).ravel())).dot((D/np.sqrt((P*(1-P)).ravel())).T)/P.size

def reconstruct_G(freq,initial=0.):
    """Four calibrated harmonic amplitudes; method-of-moments projection."""
    clean=coeffs()
    def attenuation(h):
        return np.clip(np.abs(freq[h])/abs(clean[h]),1.e-8,1.)
    V10=-2*np.log(attenuation((1,0)))
    V01=-2*np.log(attenuation((0,1)))
    V11=-2*np.log(attenuation((1,1)))
    V1m=-2*np.log(attenuation((1,-1)))
    return np.array([[V10,(V11-V1m)/4],[(V11-V1m)/4,V01]])

def estimate_fourier(counts,nshot):
    """Measured 2D Bernoulli frequency coefficients on a uniformly sampled phase torus."""
    q=np.asarray(counts)/nshot
    z=np.fft.fft2(q)/(q.shape[0]*q.shape[1])
    return {(1,0):z[1,0],(0,1):z[0,1],(1,1):z[1,1],(1,-1):z[1,-1]}

def trial_estimates(nshot,trials=80,seed=2407,grid=24,G=G_TRUE):
    rng=np.random.default_rng(seed)
    phases=np.arange(grid)*2*np.pi/grid
    X,Y=np.meshgrid(phases,phases,indexing='ij')
    pp=probability(X,Y,G)
    q=rng.binomial(nshot,pp,size=(trials,grid,grid))
    return np.array([reconstruct_G(estimate_fourier(a,nshot)) for a in q])

if __name__=='__main__':
    print(A@HISTORIES.T)
    print('unblurred population range',probability(*np.meshgrid(np.linspace(0,2*np.pi,24),np.linspace(0,2*np.pi,24))).min())
    print('Fisher',fisher_grid(G_TRUE))
