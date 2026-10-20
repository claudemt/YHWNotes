"""Phase-referenced angular PINEM: exact six-sector Bessel amplitudes.

Effective model only: same normalized radial mode for a phase-only sample field
and a coherent OAM-zero reference. Electron initially has uniform angle and OAM 0.
No claim about a realizable sample or state-of-the-art uniqueness.
"""
import numpy as np
from scipy.special import jv
from oam_higher_order_models import MASK_A, MASK_B

CENTERS = (np.arange(6)+0.5)*np.pi/3

def sector_amplitudes(mask, a, r, chi, n=1):
    beta = a*np.asarray(mask,dtype=complex) + r*np.exp(1j*chi)
    # J_n exp(i n arg(-beta)); n=0 admits beta=0 unambiguously.
    out = jv(n,2*np.abs(beta))*np.exp(1j*n*np.angle(-beta))
    return out

def angular_amplitudes(mask, a, r, chi, modes, n=1):
    vals=sector_amplitudes(mask,a,r,chi,n)
    modes=np.asarray(modes,dtype=int)
    return np.sinc(modes/6) * (np.exp(-1j*np.outer(modes,CENTERS))@vals)/6

def observation(mask, a, r, chi, modes, fwhm=1.1, efficiency=0.72,n=1):
    """One-electron record: detected mode outcomes plus one null/other record.

    Mode truncation is treated as a *lost event*, never renormalized away.
    Gaussian OAM response stochastic on retained mode index set; any angular
    Fourier power outside modes belongs to the null record.
    """
    modes=np.asarray(modes,dtype=int)
    if efficiency < 0 or efficiency > 1:raise ValueError('efficiency outside [0,1]')
    power=np.abs(angular_amplitudes(mask,a,r,chi,modes,n))**2
    d=modes[:,None]-modes[None,:]
    if fwhm>0:
        sig=fwhm/(2*np.sqrt(2*np.log(2)))
        K=np.exp(-0.5*(d/sig)**2)
        K/=K.sum(axis=0,keepdims=True)
        detected=efficiency*(K@power)
    else:
        detected=efficiency*power
    rest=1-detected.sum()
    if rest < -1e-10:raise ValueError('mode event mass larger than 1')
    return np.r_[np.maximum(rest,0),detected]

def bhattacharyya(p,q):
    return float(np.sum(np.sqrt(np.maximum(p,0)*np.maximum(q,0))))

def gamma(mask_a,mask_b,a,r,chi,modes,fwhm=1.1,efficiency=.72,n=1):
    p=observation(mask_a,a,r,chi,modes,fwhm,efficiency,n)
    q=observation(mask_b,a,r,chi,modes,fwhm,efficiency,n)
    return -np.log(np.clip(bhattacharyya(p,q),1e-300,1))

def tv(p,q):
    return .5*np.sum(np.abs(p-q))
