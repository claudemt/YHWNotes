"""Independent numerical, convention and include-graph checks for chapters 7–11."""
from pathlib import Path
from collections import Counter
import sys,json,re
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.linalg import expm
from scipy.special import jv,iv,ndtr,gammaln
from scipy.sparse import diags,kron
from scipy.sparse.linalg import expm_multiply
BOOK=Path(__file__).resolve().parents[1]
ROOT=BOOK.parents[1]
sys.path.insert(0,str(BOOK/'figures/code'))
from _electron_worked_models import v0,omega,hbar,e,photon_eV,kappa,recoil,lattice,density,spectrum,bins,reference
RESULTS={}
def check(name,actual,expected,rtol=2e-9,atol=2e-10):
    np.testing.assert_allclose(actual,expected,rtol=rtol,atol=atol,err_msg=name)
    RESULTS[name]={'max_abs_error':float(np.max(abs(np.asarray(actual)-expected)))}

# Wavepacket normalization and overlap from real integrals, not just the formula.
for shift in [1.,1.9375,7.75]:
    f=lambda p:np.exp(-p*p/4)/(2*np.pi)**.25
    overlap=quad(lambda p:f(p)*f(p-shift),-np.inf,np.inf)[0]
    check(f'packet_overlap_{shift}',overlap,np.exp(-shift*shift/8))
psi=np.array([[1,0],[.6,.8]],dtype=complex)/np.sqrt(2)
rho=psi@psi.conj().T
check('partial_trace_example',np.trace(rho@rho),.68)

# One finite-time amplitude with its phase; Lorentzian spectral integral vs closed form.
for delta in [0.,1.7,2*np.pi]:
    amp=quad(lambda t:np.cos(delta*t),0,1)[0]+1j*quad(lambda t:np.sin(delta*t),0,1)[0]
    check(f'window_amplitude_{delta}',amp,np.exp(.5j*delta)*np.sinc(delta/(2*np.pi)))
for T in [.2,2,20]:
    spectral=quad(lambda d:2/(1+d*d)*T*T*np.sinc(d*T/(2*np.pi))**2,0,500,epsabs=1e-9,limit=2000)[0]
    check(f'golden_rule_spectral_{T}',spectral,2*np.pi*(T-1+np.exp(-T)),atol=5e-8)

# Positive-frequency convention: integrate the real cosine's Fourier coefficient.
check('positive_frequency_half_amplitude',quad(lambda t:np.cos(t)**2,0,2*np.pi)[0]/(2*np.pi),.5)
for mismatch in [.0,1.,3.,8.]:
    integral=quad(lambda z:np.cos(mismatch*z),-.5,.5)[0]
    check(f'nearfield_spatial_integral_{mismatch}',integral,np.sinc(mismatch/(2*np.pi)))
ell=np.arange(-40,41); beta=1/photon_eV
prob=jv(ell,2*beta)**2
check('field_bessel_normalization',sum(prob),1.)
check('field_bessel_variance',prob@(ell**2),2*beta**2)
check('printed_field_P0',jv(0,2*beta)**2,.391,rtol=.001)

# Full electron–photon propagation of a coherent input, followed by a literal partial trace.
le=np.arange(-25,26); n=np.arange(75)
b=diags(np.ones(50),1,shape=(51,51),format='csr')
a=diags(np.sqrt(np.arange(1,75)),1,shape=(75,75),format='csr')
g=.3*np.exp(.7j); alpha=4*np.exp(.2j); beta=alpha*g; r=abs(g)**2
generator=g*kron(b.T,a)-g.conjugate()*kron(b,a.T)
coherent=np.exp(-abs(alpha)**2/2+n*np.log(alpha)-.5*gammaln(n+1))
initial=np.zeros(51*75,dtype=complex);initial[25*75:26*75]=coherent
joint=expm_multiply(generator,initial).reshape(51,75)
actual=joint@joint.conj().T
expected=np.zeros((51,51),dtype=complex)
for m in range(18):
    vec=jv(le+m,2*abs(beta))*np.exp(1j*(le+m)*np.angle(beta))
    weight=np.exp(-r+m*np.log(r)-gammaln(m+1))
    expected+=weight*np.outer(vec,vec.conj())
check('coherent_light_full_partial_trace',actual,expected,atol=2e-9)
check('coherent_light_purity',np.trace(actual@actual).real,np.exp(-2*r)*iv(0,2*r))
mean=(np.diag(actual).real@le)
check('coherent_light_mean',mean,-r)
check('coherent_light_variance',np.diag(actual).real@(le**2)-mean**2,2*abs(beta)**2+r)

# Thermal input: propagate a mixture of orthogonal Fock inputs through the full joint space.
nbar=.7
weights=(nbar/(1+nbar))**np.arange(32)/(1+nbar)
initials=np.zeros((51*75,32),dtype=complex)
initials[25*75+np.arange(32),np.arange(32)]=np.sqrt(weights)
joint_th=expm_multiply(generator,initials).reshape(51,75,32)
rho_th=np.einsum('lnk,mnk->lm',joint_th,joint_th.conj())
lam_plus=r*nbar;lam_minus=r*(nbar+1)
predicted=np.exp(-lam_plus-lam_minus)*(lam_plus/lam_minus)**(le/2)*iv(abs(le),2*np.sqrt(lam_plus*lam_minus))
check('thermal_full_joint_spectrum',np.diag(rho_th).real,predicted,atol=2e-11)
check('thermal_full_joint_off_diagonal',rho_th-np.diag(np.diag(rho_th)),0.,atol=2e-11)

# Full finite Gaussian wavepacket density integral versus envelope convolution.
for packet_width in [.4,3.]:
    aa,bb=.2,.1
    Z=1+2*aa*np.exp(-packet_width**2/2)
    env=lambda z:np.exp(-z*z/(2*packet_width**2))/(np.sqrt(2*np.pi)*packet_width)
    dens=lambda z:env(z)*(1+2*aa*np.cos(z)-2*bb*np.sin(z))/Z
    direct=quad(lambda z:dens(z)*np.cos(z),-np.inf,np.inf)[0]-1j*quad(lambda z:dens(z)*np.sin(z),-np.inf,np.inf)[0]
    F=lambda q:np.exp(-packet_width**2*q*q/2)
    check(f'finite_envelope_harmonic_{packet_width}',direct,(F(1)+(aa+1j*bb)*F(0)+(aa-1j*bb)*F(2))/Z)

# Lattice propagation: independent differential equation and enlarged cutoff.
for ratio in [.05,.2,1,5]:
    el,p=lattice(ratio,cutoff=25); el2,p2=lattice(ratio,cutoff=34)
    check(f'bragg_cutoff_{ratio}',p[:,0],p2[9:-9,0],atol=2e-9)
    check(f'bragg_norm_{ratio}',sum(p[:,0]),1.)
ratio=1.; cutoff=10; el=np.arange(-cutoff,cutoff+1)
H=np.diag(el*(el-1.)).astype(float)+np.diag(np.full(2*cutoff,.5),1)+np.diag(np.full(2*cutoff,.5),-1)
initial=np.zeros(2*cutoff+1,dtype=complex);initial[cutoff]=1
ode=solve_ivp(lambda t,y:-1j*H@y,(0,np.pi),initial,rtol=1e-9,atol=1e-11,method='DOP853').y[:,-1]
check('bragg_ode_probability',abs(ode)**2,lattice(1,cutoff=cutoff)[1][:,0],atol=2e-8)

# Direct sideband sums vs the harmonic closed form; Fourier sign at a fixed detector.
beta=1.2;phi=.37;el=np.arange(-45,46)
for order in [1,2,3]:
    for phase in [.1,.39366966546,1.2]:
        direct=np.sum(jv(el,2*beta)*jv(el-order,2*beta)*np.exp(-1j*(2*el*order-order**2)*phase))*np.exp(1j*order*phi)
        closed=(-1j)**order*np.exp(1j*order*phi)*jv(order,4*beta*np.sin(order*phase))
        check(f'bunching_harmonic_{order}_{phase}',direct,closed)
times=np.linspace(-2,2,40)
wave=np.exp(-1j*np.outer(times,el))@(jv(el,2*beta)*np.exp(1j*el*phi))
check('pinem_time_phase_sign',wave,np.exp(2j*beta*np.sin(phi-times)))
dt=1e-5
ph=lambda t:2*beta*np.sin(phi-t)
check('instantaneous_energy_sign',-(ph(times+dt)-ph(times-dt))/(2*dt),2*beta*np.cos(phi-times),atol=2e-9)
phase=.39366966546
theta=np.linspace(-np.pi,np.pi,5001)
check('density_normalization',np.trapezoid(density(theta,beta,phase),theta)/(2*np.pi),1.)
check('incoherent_density',sum(jv(el,2*beta)**2),1.)
RESULTS['physical_scales']={'v0_m_s':v0,'photon_eV':photon_eV,'recoil_rad_s':recoil,
                           'best_first_harmonic_m':phase*v0/recoil,'talbot_m':2*np.pi*v0/recoil}

# Reference tomography from the full two-input, one-output measurement row.
rho=np.array([[.65,.2+.15j],[.2-.15j,.35]])
phases=np.arange(4)*np.pi/2
u0,u1=jv(0,.8),jv(1,.8)
for phase in phases:
    row=np.array([u0,-u1*np.exp(-1j*phase)])
    check(f'tomography_effect_{phase}',row@rho@row.conj(),reference(phase))
p=reference(phases)
check('tomography_four_phase',[(p[2]-p[0])/(4*u0*u1),(p[1]-p[3])/(4*u0*u1)],[.2,.15])
check('tomography_purity',np.trace(rho@rho).real,.67)

# Gaussian source convolved with detector; bin edges and field quadratures.
sigma=np.hypot(.25,.15)
for output in [0,.2,.8]:
    integral=quad(lambda z:np.exp(-z*z/(2*.25**2)-(output-z)**2/(2*.15**2))/(2*np.pi*.25*.15),-3,3)[0]
    check(f'gaussian_convolution_{output}',integral,np.exp(-output**2/(2*sigma**2))/(np.sqrt(2*np.pi)*sigma))
edges=np.array([-np.inf,-2.5*photon_eV,-.5*photon_eV,.5*photon_eV,2.5*photon_eV,np.inf])
bp=bins(edges,1.2,sigma)
check('detector_all_bins',sum(bp),1.)
for j in range(1,4):
    numeric=quad(lambda x:spectrum([x],1.2,sigma)[0],edges[j],edges[j+1],epsabs=1e-11)[0]
    check(f'detector_bin_integral_{j}',numeric,bp[j])
q=abs(.6+.3j+.5*np.exp(1j*phases))**2
check('nearfield_quadrature_inputs',q,[1.3,1.,.1,.4])
check('nearfield_four_phase',[(q[0]-q[2])/2,(q[1]-q[3])/2],[.6,.3])
RESULTS['detector_examples']={'misassignment':2*ndtr(-photon_eV/(2*sigma)),
 'measured_variances_eV2':(.085+2*photon_eV**2*q).tolist()}

# Follow actual inputs, excluding historical or backup fragments.
visited=[]
def walk(path):
    assert path not in visited,('duplicate include',path)
    visited.append(path)
    text=path.read_text(encoding='utf-8')
    for value in re.findall(r'\\input\{([^}]+)\}',text):
        name=value if Path(value).suffix else value+'.tex'
        found=next((p for p in [ROOT/name,BOOK/name,path.parent/name] if p.is_file()),None)
        assert found is not None,(path,name)
        walk(found)
walk(BOOK/'FreeElectronQuantumOptics.tex')
texts=[p.read_text(encoding='utf-8') for p in visited]
for path,t in zip(visited,texts):
    if path.name.startswith('electron-'):
        assert not re.search(r'(?<!\\)\b(?:quad|qquad|frac|hbar|sqrt|mathrm|operatorname|Delta|sigma)\b',t),path
        assert 'S_RU_{\nm drift}' not in t,path
joined='\n'.join(texts)
labels=Counter(re.findall(r'\\label\{([^}]+)\}',joined))
assert all(count==1 for count in labels.values()),{k:v for k,v in labels.items() if v>1}
for path,t in zip(visited,texts):
    assert Counter(re.findall(r'\\begin\{([^}]+)\}',t))==Counter(re.findall(r'\\end\{([^}]+)\}',t)),path
keys=set(re.findall(r'@\w+\{([^,]+),',(BOOK/'references.bib').read_text(encoding='utf-8')))
cites={x.strip() for group in re.findall(r'\\cite\{([^}]+)\}',joined) for x in group.split(',')}
assert cites<=keys,cites-keys
aux=ROOT/'build/FreeElectronQuantumOptics/main.aux'
refs={x.strip() for group in re.findall(r'\\(?:eqnrefs|figref|tabref|secref|chapref|ref|eqref)\{([^}]+)\}',joined) for x in group.split(',')}
if aux.exists():
    auxlabels=set(re.findall(r'\\newlabel\{([^}]+)\}',aux.read_text(encoding='utf-8',errors='replace')))
    assert not (refs-set(labels)-auxlabels-{'LastPage'}),refs-set(labels)-auxlabels
RESULTS['structure']={'included_files':len(visited),'labels':len(labels),'references':len(refs),'citations':len(cites)}
(BOOK/'validation/electron-verification.json').write_text(json.dumps(RESULTS,indent=2),encoding='utf-8')
print(f'PASS: {len(RESULTS)} numerical and structural checks/outputs.')
print(json.dumps({k:v for k,v in RESULTS.items() if k in ['physical_scales','detector_examples','structure']},indent=2))
