"""Exact angular PINEM Fourier masks and endpoint-history quantum walk.

Physical conventions:
  Angular phase-only PINEM: beta(phi)=a*s(phi), |s|=1, uniform input OAM 0.
  c(n,M)=J_n(2a) times the angular Fourier coefficient of s(phi)^n.
  Endpoint model: H_{destination,source}=g exp(+i theta) and U=exp(-i H tau).
All numerical examples are deliberately finite teaching models, not measured data.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm
from scipy.special import jv

SECTORS = 6
MASK_A = np.array([1, 1, 1, 1, 1, -1], dtype=complex)
MASK_B = np.array([1, 1, 1j, 1, 1, -1j], dtype=complex)
# A second exact family whose first and second order spectra coincide.
ROOTS = np.exp(2j*np.pi*np.arange(SECTORS)/SECTORS)
MASK_C = ROOTS[[0, 0, 4, 0, 4, 0]]
MASK_D = ROOTS[[0, 1, 0, 1, 0, 3]]


def angular_coefficients(mask: np.ndarray, order: int, modes: np.ndarray) -> np.ndarray:
    """Analytic integral over six equal angular sectors (no FFT interpolation)."""
    modes = np.asarray(modes, dtype=int)
    centers = 2*np.pi*(np.arange(SECTORS)+.5)/SECTORS
    phases = mask ** int(order)
    # Integral on each sector = exp(-i m center)*sinc(m/6)/6.
    return np.sinc(modes/SECTORS) * (np.exp(-1j*np.outer(modes, centers))@phases)/SECTORS


def conditional_oam(mask, order: int, modes):
    c = angular_coefficients(mask, order, modes)
    return abs(c)**2


def detector_blur(p, modes, fwhm=1.1):
    """Column-stochastic OAM sorter response; mode index is in units hbar."""
    sig=fwhm/(2*np.sqrt(2*np.log(2)))
    diff = np.asarray(modes)[:,None] - np.asarray(modes)[None,:]
    k=np.exp(-.5*(diff/sig)**2)
    k/=np.sum(k,axis=0,keepdims=True)
    return k@np.asarray(p)


def normalized_oam(mask, order, modes, fwhm=None):
    """Finite collection window renormalized *after* optional detector blur."""
    p=conditional_oam(mask,order,modes)
    if fwhm is not None:p=detector_blur(p,modes,fwhm=fwhm)
    return p/p.sum()


def total_variation(p,q):
    return 0.5*np.sum(abs(np.asarray(p)-np.asarray(q)))


def build_endpoint_hamiltonian(g1=.43,g2=.38,g3=.34,theta1=0.,theta2=0.,theta3=0.,graded=False):
    """Finite coherent walk with two exchange-order paths and one direct path.

    States of ungraded model: [origin,(1,+1),(1,-1),(2,0)].
    Graded model: [origin,(1,+1),(1,-1), direct endpoint, composite endpoint].
    The graded endpoints are orthogonal labels with the same measured (E,OAM).
    """
    H=np.zeros((5 if graded else 4,5 if graded else 4),dtype=complex)
    composite = 4 if graded else 3
    direct = 3
    hops=[(1,0,g1,theta1), (2,0,g2,theta2),
          (composite,1,g2,theta2),(composite,2,g1,theta1),
          (direct,0,g3,theta3)]
    for i,j,g,th in hops:
        H[i,j]=g*np.exp(1j*th)
        H[j,i]=np.conj(H[i,j])
    return H


def populations(theta3, g1=.43,g2=.38,g3=.34,tau=1., graded=False):
    H=build_endpoint_hamiltonian(g1,g2,g3,theta3=theta3,graded=graded)
    vec=expm(-1j*tau*H)[:,0]
    pop=np.abs(vec)**2
    if graded:
        return np.r_[pop[:3],pop[3]+pop[4]]
    return pop


def endpoint_signal(theta3, **kwargs):
    return populations(theta3,**kwargs)[-1]


def harmonic_coefficient(signal, harmonic=1):
    """Fourier component of uniformly sampled phase response (periodic)."""
    return np.mean(np.asarray(signal)*np.exp(-1j*int(harmonic)*2*np.pi*np.arange(len(signal))/len(signal)))


def self_check():
    modes=np.arange(-250,251)
    assert np.max(abs(conditional_oam(MASK_A,1,modes)-conditional_oam(MASK_B,1,modes))) <1e-13
    assert total_variation(normalized_oam(MASK_A,2,modes,1.1),normalized_oam(MASK_B,2,modes,1.1))>.79
    for n in (1,2):
        assert np.max(abs(conditional_oam(MASK_C,n,modes)-conditional_oam(MASK_D,n,modes)))<1e-13
    assert total_variation(normalized_oam(MASK_C,3,modes,1.1),normalized_oam(MASK_D,3,modes,1.1))>.02
    for s in (MASK_A,MASK_B,MASK_C,MASK_D):
        for n in (1,2,3):
            tail=1-sum(conditional_oam(s,n,modes))
            assert 0 <= tail < .007,(n,tail)
    theta=np.linspace(0,2*np.pi,97,endpoint=False)
    coherent=np.array([endpoint_signal(t) for t in theta])
    graded=np.array([endpoint_signal(t,graded=True) for t in theta])
    assert np.ptp(coherent)>0.025
    assert np.ptp(graded)<1e-13
    for th in theta[::11]:
        for grade in (False,True):
            h=build_endpoint_hamiltonian(theta3=th,graded=grade)
            assert np.max(abs(h-h.conj().T))<1e-14
            assert abs(populations(th,graded=grade).sum()-1)<2e-14
    assert np.ptp(np.array([endpoint_signal(t,g3=0.) for t in theta]))<1e-13
    return dict(homometry_two_photon=total_variation(normalized_oam(MASK_A,2,modes,1.1),normalized_oam(MASK_B,2,modes,1.1)),
                coherent_modulation=np.ptp(coherent), graded_modulation=np.ptp(graded))


if __name__=='__main__':
    print(self_check())


def angular_increment_correlation(mask, order, deltas, modes=None):
    """Circular phase-increment correlator computed from exact angular harmonics.

    C_n(Delta)=sum_M |tilde{s^n}_M|^2 exp(+i M Delta).
    The optional symmetric modal cutoff makes its omitted tail explicit.
    """
    if modes is None:
        modes=np.arange(-250,251)
    modes=np.asarray(modes,dtype=int)
    delta=np.asarray(deltas,dtype=float)
    probabilities=conditional_oam(mask,order,modes)
    return np.exp(1j*np.outer(delta,modes)) @ probabilities


def bhattacharyya(p,q):
    """Classical overlap after all declared readout blur and collection cuts."""
    p=np.maximum(np.asarray(p,dtype=float),0.)
    q=np.maximum(np.asarray(q,dtype=float),0.)
    assert p.shape==q.shape
    assert abs(p.sum()-1.)<1e-9 and abs(q.sum()-1.)<1e-9
    return float(np.clip(np.sum(np.sqrt(p*q)),0.,1.))


def order_overlap(mask_a,mask_b,order,modes,fwhm=1.1):
    """B_n for the *normalized, detector-resolved* order-conditioned spectra."""
    p=normalized_oam(mask_a,order,modes,fwhm)
    q=normalized_oam(mask_b,order,modes,fwhm)
    return bhattacharyya(p,q)


def per_electron_exponent(amplitude,orders,overlaps,both_signs=True):
    """Bhattacharyya discrimination rate for one incident electron.

    Only selected observed energy orders retain their OAM readout; all other
    outcomes are collected into a nondiscriminating bin. If both energy signs
    are collected, the pair shares the same B_n in a phase-only PINEM model.
    The returned rate is *not* the optimal Chernoff exponent.
    """
    orders=np.atleast_1d(orders).astype(int)
    overlaps=np.atleast_1d(overlaps).astype(float)
    assert len(orders)==len(overlaps) and np.all(orders>0)
    assert len(set(map(int,orders)))==len(orders)
    weight=(2.0 if both_signs else 1.0)*jv(orders,2*amplitude)**2
    deficit=float(np.dot(weight,np.maximum(0,1.-overlaps)))
    assert -1e-12<=deficit<1.+1e-12,(weight,deficit)
    return float(-np.log1p(-min(max(deficit,0.),1.-1e-14)))


def error_probability_bound(rate,dose):
    """Equal-prior Bayes error upper bound: Pe <= (1/2)exp(-N rate)."""
    return .5*np.exp(-np.asarray(dose,dtype=float)*rate)


def information_budget_check():
    modes=np.arange(-250,251)
    overlap={n:order_overlap(MASK_A,MASK_B,n,modes,1.1) for n in range(1,8)}
    for n in (1,3,4,5,7):
        assert abs(1-overlap[n])<1e-10, (n,overlap[n])
    assert 1-overlap[2]>.50 and 1-overlap[6]>.50
    for n in (2,6):
        ideal=order_overlap(MASK_A,MASK_B,n,modes,None)
        blur=overlap[n]
        assert blur+1e-11>=ideal,(n,ideal,blur)
    for a in (.8,2.,3.):
        rates=np.array([per_electron_exponent(a,[n],[overlap[n]]) for n in (2,6)])
        joint=per_electron_exponent(a,[2,6],[overlap[2],overlap[6]])
        assert joint+1e-13 >=rates.max()
        assert 0<=error_probability_bound(joint,50)<=.5
    return overlap
