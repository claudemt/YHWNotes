"""Gaussian noise on endpoint-relation phases, computed from the exact four-state
energy-OAM Hamiltonian in oam_higher_order_models.

All positions in the 3D plot are *laser phase errors*, not 3D synthetic space.
No phenomenological reduction of the Hamiltonian is used. Gaussian averaging of
P_f(Phi) is exactly diagonal in the relation-harmonic Fourier basis.
"""
import numpy as np
from oam_higher_order_models import endpoint_signal, build_endpoint_hamiltonian

U = np.array([1., 1., -1.])
TAU = 2.5
G = (0.43, 0.38, 0.34)


def exact_endpoint(phase, tau=TAU):
    """P_f with loop phase Phi=theta1+theta2-theta3, theta3=-Phi."""
    return float(endpoint_signal(-float(phase), g1=G[0],g2=G[1],g3=G[2],tau=tau))


def phase_signal(n=512, tau=TAU):
    phi = np.arange(n)*2*np.pi/n
    values = np.array([exact_endpoint(x,tau) for x in phi])
    coefficients = np.fft.fft(values)/n
    return phi, values, coefficients


def relation_variance(covariance, u=U):
    matrix = np.asarray(covariance,float)
    assert matrix.shape == (len(u),len(u))
    if np.linalg.eigvalsh(matrix).min() < -1e-11:
        raise ValueError('Covariance must be positive semidefinite')
    return float(np.asarray(u)@matrix@np.asarray(u))


def independent_covariance(sigma):
    return (sigma*sigma)*np.eye(3)


def locked_covariance(sigma, lam=1.0, residual=.12):
    """theta1=x,theta2=y,theta3=lambda(x+y)+epsilon*z, independent unit Gaussians."""
    M=np.array([[1.,0.,0.],[0.,1.,0.],[lam,lam,residual/max(sigma,1e-50)]])
    if sigma == 0:
        return np.diag([0.,0.,residual*residual])
    return sigma*sigma*(M@M.T)


def closed_relation_variance(sigma, lam=1., residual=.12):
    return 2*(1-lam)**2*sigma**2+residual**2


def averaged_coefficients(coefs, v):
    indices=np.fft.fftfreq(len(coefs),d=1./len(coefs))
    return coefs*np.exp(-.5*v*indices**2)


def signal_at(phases, coefs, variance=0.0, derivative=False):
    """Exact Gaussian shot-noise average, using Fourier coefficients from expm.

    The discrete coefficient grid is spectrally converged for the smooth signal.
    """
    m=np.fft.fftfreq(len(coefs),d=1./len(coefs))
    y=averaged_coefficients(coefs,variance)
    if derivative:
        y=1j*m*y
    phases=np.atleast_1d(np.asarray(phases,float))
    val=np.exp(1j*np.outer(phases,m))@y
    if np.max(abs(val.imag)) > 2e-10:
        raise ValueError('Imaginary reconstruction beyond numerical tolerance')
    return val.real


def fisher_binary(phi, coeffs, variance):
    p=signal_at([phi],coeffs,variance)[0]
    dp=signal_at([phi],coeffs,variance,derivative=True)[0]
    if not 0<p<1: return 0.
    return float(dp*dp/(p*(1-p)))


def self_check():
    from scipy.linalg import expm
    phi,y,c=phase_signal(n=256)
    assert np.max(abs(signal_at(phi,c)-y)) <1e-12
    assert abs(c[1])>.1 and abs(c[2])>.005
    assert y.min()>=0 and y.max()<=1
    assert relation_variance(independent_covariance(.8))==np.dot(U,U)*.8**2
    for sigma,lam,eps in [(.8,1.,.12),(.8,.6,.12),(2.0,.1,.32),(0.,1.,.12)]:
        assert abs(relation_variance(locked_covariance(sigma,lam,eps))-closed_relation_variance(sigma,lam,eps)) <2e-13
    # Gauge invariance: only Phi matters, even for finite tau.
    phi0=.37
    from oam_higher_order_models import build_endpoint_hamiltonian
    for t1,t2 in [(.25,-.1),(.92,-.8),(1.0,.30)]:
        t3=t1+t2-phi0
        h=build_endpoint_hamiltonian(g1=G[0],g2=G[1],g3=G[2],theta1=t1,theta2=t2,theta3=t3)
        exact=abs(expm(-1j*TAU*h)[3,0])**2
        assert abs(exact-exact_endpoint(phi0))<1e-13,(exact,exact_endpoint(phi0))
    # Averages with sampled Gaussian phase jitter reproduce Fourier attenuation.
    rng=np.random.default_rng(2701)
    phase_noise=rng.normal(0,.8,size=(40000,3))
    phi_noise=phase_noise@U
    phigrid=np.linspace(0,2*np.pi,256,endpoint=False)
    pvals=y
    # Evaluate arbitrary phases via Fourier; direct expm for each MC draw isn't needed.
    draws=signal_at(phi0+phi_noise,c)
    target=signal_at([phi0],c,relation_variance(independent_covariance(.8)))[0]
    assert abs(draws.mean()-target)<.003,(draws.mean(),target)
    # Correlated jitter with theta3=theta1+theta2+residual z leaves only residual.
    xyz=rng.normal(size=(40000,3))
    errors=np.stack([.8*xyz[:,0],.8*xyz[:,1],.8*(xyz[:,0]+xyz[:,1])+.12*xyz[:,2]],axis=-1)
    assert abs(np.std(errors@U)-.12)<.003
    assert abs(np.mean(signal_at(phi0+errors@U,c)) - signal_at([phi0],c,.12**2)[0])<.002
    # The phase-noise factor for Fourier harmonic m is exp(-m^2 V/2).
    blurred=averaged_coefficients(c,.72)
    for m in [1,2,3]:
        assert abs(blurred[m]/c[m] - np.exp(-.36*m*m))<1e-9
    # Quantum unitary and physical probability, plus Fisher nonnegativity.
    assert fisher_binary(phi0,c,.72)>=0
    return dict(first_harmonic=float(abs(c[1])),second_harmonic=float(abs(c[2])),
                protected_variance=.12**2,independent_variance=3*.8**2,
                max_endpoint_probability=float(y.max()))

if __name__=='__main__':
    print(self_check())
