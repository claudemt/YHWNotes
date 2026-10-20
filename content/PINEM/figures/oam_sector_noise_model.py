"""Exact Gaussian phase-jitter ensemble for phase-only six-sector OAM PINEM.

Independent zero-mean Gaussian *sector* phases with variance sigma^2 damp
all inter-sector coherences by q=exp(-n^2 sigma^2), retaining diagonal terms.
One common global phase leaves all sector coherences exactly unaffected.
Detector probabilities include the mode window, efficiency and a null record.
"""
import numpy as np
from scipy.special import jv
from oam_higher_order_models import MASK_A,MASK_B,conditional_oam

MODES=np.arange(-120,121)
FW=1.1
EFF=.72
WINDOW=12


def sector_ensemble(mask, order, modes=MODES, sigma=0.,correlation=0.):
    """If all sector phases have equicorrelation rho, pairwise variance is
    2*sigma^2*(1-rho), hence q=exp(-n^2*sigma^2*(1-rho)).
    For rho in [0,1], covariance PSD; rho=1 is perfectly common drift.
    """
    if not 0<=correlation<=1:
        raise ValueError('Only equicorrelation 0<=rho<=1 in this teaching model')
    if sigma <0:
        raise ValueError('sigma must be nonnegative')
    modes=np.asarray(modes,int)
    coherent=conditional_oam(mask,order,modes)
    incoherent=np.sinc(modes/6.)**2/6.
    q=np.exp(-order*order*sigma*sigma*(1.-correlation))
    return q*coherent+(1-q)*incoherent


def blur_kernel(modes=MODES,fwhm=FW):
    modes=np.asarray(modes,int)
    if fwhm<=0: return np.eye(len(modes))
    s=fwhm/(2*np.sqrt(2*np.log(2)))
    matrix=np.exp(-.5*((modes[:,None]-modes[None,:])/s)**2)
    matrix/=matrix.sum(axis=0,keepdims=True)
    return matrix


# Precompute finite-window detection; rows outside the collected window
# still retain probability in the null outcome.
K=blur_kernel()
SELECT=np.abs(MODES)<=WINDOW


def detected_mode_weights(mask,n,sigma,rho):
    p=sector_ensemble(mask,n,MODES,sigma,rho)
    return EFF*(K@p)[SELECT]


def joint_record(mask,n,a,sigma,rho):
    obs=jv(n,2*a)**2 * detected_mode_weights(mask,n,sigma,rho)
    null=1.-obs.sum()
    if null<0: raise ValueError('Unphysical detection rate')
    return np.r_[null,obs]


def bhatt(p,q):
    return float(np.sum(np.sqrt(np.maximum(p,0)*np.maximum(q,0))))


def incident_rate(n,a,sigma,rho):
    x=joint_record(MASK_A,n,a,sigma,rho)
    y=joint_record(MASK_B,n,a,sigma,rho)
    return -np.log(np.clip(bhatt(x,y),1e-300,1.))


def conditional_tv(n,sigma,rho):
    a=detected_mode_weights(MASK_A,n,sigma,rho)
    b=detected_mode_weights(MASK_B,n,sigma,rho)
    a=a/a.sum();b=b/b.sum()
    return .5*np.abs(a-b).sum()


def self_check():
    from oam_higher_order_models import conditional_oam
    for n in [1,2,4,6]:
        p=sector_ensemble(MASK_A,n,sigma=0.)
        assert np.max(abs(p-conditional_oam(MASK_A,n,MODES)))<1e-14
        common=sector_ensemble(MASK_A,n,sigma=1.4,correlation=1.)
        assert np.max(abs(p-common))<1e-14
        pa=joint_record(MASK_A,n,.8,.35,0.)
        pb=joint_record(MASK_B,n,.8,.35,0.)
        assert abs(pa.sum()-1)<1e-12 and pa.min()>=0
        assert abs(pb.sum()-1)<1e-12 and pb.min()>=0
    assert conditional_tv(1,0,0)<1e-12
    assert conditional_tv(2,0,0)>.7
    assert conditional_tv(2,.7,0)<conditional_tv(2,.3,0)<conditional_tv(2,0,0)
    assert abs(conditional_tv(2,.9,1)-conditional_tv(2,0,0))<1e-12
    assert incident_rate(2,.8,.8,0)<incident_rate(2,.8,.2,0)
    # MC validation for the Gaussian dephasing factor of an offdiagonal entry.
    rng=np.random.default_rng(1305)
    delta=rng.normal(0,.35,size=(70000,6))
    measured=np.mean(np.exp(2j*(delta[:,0]-delta[:,1]))).real
    assert abs(measured-np.exp(-4*.35**2))<.01
    return dict(ideal_two_photon_tv=conditional_tv(2,0,0),
                jittered_two_photon_tv=conditional_tv(2,.5,0),
                protected_two_photon_tv=conditional_tv(2,.5,1))

if __name__=='__main__':print(self_check())
