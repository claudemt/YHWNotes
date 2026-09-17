"""Exact SymPy checks for parameterized exercises; no numerical substitution."""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
results={}

def identity(name,actual,expected=0):
    residual=s.simplify(s.expand_func(actual-expected))
    if isinstance(residual,s.MatrixBase):
        assert residual==s.zeros(*residual.shape),(name,residual)
    else:
        assert residual==0,(name,residual)
    results[name]={'residual':str(residual)}
    print('PASS',name,flush=True)

p,a,b,q=s.symbols('p a b q',real=True)
sigma,tau=s.symbols('sigma tau',positive=True)
identity('Gaussian completing square',(p-a)**2+(p-b)**2,
         2*(p-(a+b)/2)**2+(a-b)**2/2)
overlap=s.integrate(s.exp(-(p-q/2)**2/(2*sigma**2)-q*q/(8*sigma**2))/(s.sqrt(2*s.pi)*sigma),(p,-s.oo,s.oo))
identity('Gaussian packet overlap integral',overlap,s.exp(-q*q/(8*sigma**2)))
w,mx,my,phi,theta=s.symbols('w mx my phi theta',real=True)
mu=mx+s.I*my
rho=s.Matrix([[w,s.sqrt(w*(1-w))*s.exp(-s.I*phi)*mu],
              [s.sqrt(w*(1-w))*s.exp(s.I*phi)*s.conjugate(mu),1-w]])
identity('Unequal path purity',s.trace(rho*rho),1-2*w*(1-w)*(1-mx*mx-my*my))
row=s.Matrix([[1,s.exp(-s.I*theta)]])/s.sqrt(2)
identity('Unequal path fringe',(row*rho*row.conjugate().T)[0],
         s.Rational(1,2)+s.sqrt(w*(1-w))*(s.exp(s.I*(theta-phi))*mu+s.exp(-s.I*(theta-phi))*s.conjugate(mu))/2)

t,D=s.symbols('t D',real=True)
ft=2*s.integrate(s.exp(-t*t/(2*tau*tau))*s.cos(D*t),(t,0,s.oo))
identity('Gaussian switching Fourier integral',ft,s.sqrt(2*s.pi)*tau*s.exp(-D*D*tau*tau/2))
identity('Gaussian spectral half maximum',s.exp(-D*D*tau*tau).subs(D,s.sqrt(s.log(2))/tau),s.Rational(1,2))
x,T,Gamma=s.symbols('x T Gamma',positive=True)
u=s.symbols('u',nonnegative=True)
P=Gamma/tau*s.integrate((T-u)*s.exp(-u/tau),(u,0,T))
identity('Lorentz spectrum time integral',P,Gamma*(T-tau*(1-s.exp(-T/tau))))
R=1-(1-s.exp(-x))/x
identity('Golden rule ratio derivative',s.diff(R,x),(1-(1+x)*s.exp(-x))/x**2)
identity('Golden rule short time series',s.series(R,x,0,4).removeO(),x/2-x*x/6+x**3/24)

beta=s.symbols('beta',real=True)
j=[s.series(s.besselj(n,2*beta),beta,0,6).removeO() for n in range(3)]
prob=[s.series(v*v,beta,0,6).removeO() for v in j]
identity('Bessel central probability through fourth order',prob[0],1-2*beta**2+s.Rational(3,2)*beta**4)
identity('Bessel first probability through fourth order',prob[1],beta**2-beta**4)
identity('Bessel second probability through fourth order',prob[2],beta**4/4)
identity('Bessel normalization through fourth order',prob[0]+2*prob[1]+2*prob[2],1)
identity('Bessel variance through fourth order',2*prob[1]+8*prob[2],2*beta**2)
chi=s.symbols('chi',real=True)
char=s.besselj(0,4*beta*s.sin(chi/2))
identity('Exact Bessel characteristic variance',-s.diff(char,chi,2).subs(chi,0),2*beta**2)

r=s.symbols('r',positive=True)
m=s.symbols('m',integer=True,nonnegative=True)
weights=s.exp(-r)*r**m/s.factorial(m)
identity('Poisson eigenvalue normalization',s.summation(weights,(m,0,s.oo)),1)
identity('Pure reference trace distance',(1-s.exp(-r)+s.summation(weights,(m,1,s.oo)))/2,1-s.exp(-r))
identity('Purity small coupling expansion',s.series(s.exp(-2*r)*s.besseli(0,2*r),r,0,3).removeO(),1-2*r+3*r*r)
eps=s.symbols('eps',positive=True)
identity('Trace distance tolerance at boundary',(1-s.exp(-r)).subs(r,-s.log(1-eps)),eps)

ox,oy,delta=s.symbols('ox oy delta',real=True)
Om=ox+s.I*oy
H=s.Matrix([[-delta,s.conjugate(Om)],[Om,delta]])/2
R2=ox*ox+oy*oy+delta*delta
identity('Detuned two-state Hamiltonian square',H*H,R2*s.eye(2)/4)
angle=s.symbols('angle',real=True)
norm=s.symbols('norm',positive=True)
U=s.cos(angle)*s.eye(2)-2*s.I*H/norm*s.sin(angle)
unit=s.expand(U.conjugate().T*U).subs(norm**2,R2)
identity('Detuned two-state propagator unitarity',unit,s.eye(2))
transfer=s.expand(U[1,0]*s.conjugate(U[1,0])).subs(norm**2,R2)
identity('Detuned two-state transfer probability',transfer,(ox*ox+oy*oy)/R2*s.sin(angle)**2)
ratio,eta=s.symbols('ratio eta',positive=True)
identity('Detuning tolerance at boundary',(1/(1+ratio**2)).subs(ratio,s.sqrt(eta/(1-eta))),1-eta)

z=s.symbols('z',real=True)
identity('Bessel first derivative recurrence',s.diff(s.besselj(1,z),z),(s.besselj(0,z)-s.besselj(2,z))/2)
d,omega,sj,sd=s.symbols('d omega sj sd',positive=True)
identity('Gaussian jitter and detector composition',s.exp(-d*d*omega*omega*sj*sj/2)*s.exp(-d*d*omega*omega*sd*sd/2),s.exp(-d*d*omega*omega*(sj*sj+sd*sd)/2))
identity('Harmonic retention at tolerance',s.exp(-d*d*omega*omega*sj*sj/2).subs(sj,s.sqrt(2*s.log(1/eta))/(d*omega)),eta)

p0,u0,u1,cx,cy,phase=s.symbols('p0 u0 u1 cx cy phase',real=True)
rr=s.Matrix([[p0,cx+s.I*cy],[cx-s.I*cy,1-p0]])
v=s.Matrix([[u0,-u1*s.exp(-s.I*phase)]])
fringe=(v*rr*v.conjugate().T)[0]
A=u0*u0*p0+u1*u1*(1-p0)
identity('Full-ladder reference effect on two input states',s.expand_complex(fringe),A-2*u0*u1*cx*s.cos(phase)+2*u0*u1*cy*s.sin(phase))
phase4=[0,s.pi/2,s.pi,3*s.pi/2]
pf=[s.simplify(fringe.subs(phase,a)) for a in phase4]
identity('Four-phase electron real part',(pf[2]-pf[0])/(4*u0*u1),cx)
identity('Four-phase electron imaginary part',(pf[1]-pf[3])/(4*u0*u1),cy)
identity('Four-phase electron background sum',pf[0]+pf[2]-pf[1]-pf[3])
identity('Electron positive determinant',rr.det(),p0*(1-p0)-cx*cx-cy*cy)
C,S,N=s.symbols('C S N',real=True)
identity('Binomial difference variance numerator',(A-C)*(1-A+C)+(A+C)*(1-A-C),2*A*(1-A)-2*C*C)

energy,width=s.symbols('energy width',positive=True)
x=s.symbols('x',real=True)
inside=s.integrate(s.exp(-x*x/(2*width*width))/(s.sqrt(2*s.pi)*width),(x,-energy/2,energy/2))
identity('Gaussian midpoint misassignment integral',1-inside,s.erfc(energy/(2*s.sqrt(2)*width)))
u=s.symbols('u',positive=True)
tail_bound=s.integrate(u*s.exp(-u*u/2),(u,energy/(2*width),s.oo))*2/(s.sqrt(2*s.pi)*(energy/(2*width)))
identity('Gaussian tail bound coefficient',tail_bound,s.sqrt(8/s.pi)*width/energy*s.exp(-energy*energy/(8*width*width)))

br=s.symbols('br',positive=True)
xs,ys=s.symbols('xs ys',real=True)
qfun=xs*xs+ys*ys+br*br+2*br*(xs*s.cos(phase)+ys*s.sin(phase))
q4=[qfun.subs(phase,a) for a in phase4]
identity('Four-phase field real part',(q4[0]-q4[2])/(4*br),xs)
identity('Four-phase field imaginary part',(q4[1]-q4[3])/(4*br),ys)
identity('Field background sum',q4[0]+q4[2]-q4[1]-q4[3])
identity('Field intensity and quadrature consistency',((q4[0]-q4[2])**2+(q4[1]-q4[3])**2)/(16*br*br),sum(q4)/4-br*br)
sq=s.symbols('sq',positive=True)
identity('Field quadrature equal-error variance',2*sq*sq/(4*br)**2,sq*sq/(8*br*br))

# Finite Gaussian envelope: normalized Fourier convolution and long-packet limit.
L,k=s.symbols('L k',positive=True)
u,v,q=s.symbols('u v q',real=True)
f=lambda q:s.exp(-L*L*q*q/2)
Z=1+2*u*f(k)
Ie=(f(q)+(u+s.I*v)*f(q-k)+(u-s.I*v)*f(q+k))/Z
identity('Finite envelope normalization',Ie.subs(q,0),1)
identity('Finite envelope integer harmonic limit',s.limit(Ie.subs(q,k),L,s.oo),u+s.I*v)

# Added general analytic cases: chirp, Ramsey interference, thermal input, Gaussian TDSE.
C,dp,z0=s.symbols('C dp z0',real=True)
hbar,mass=s.symbols('hbar mass',positive=True)
x=s.symbols('x',real=True)
chirp=2*s.integrate(s.exp(-x*x/(2*sigma*sigma))*s.cos(C*dp*x/(2*sigma*sigma)),(x,0,s.oo))/(s.sqrt(2*s.pi)*sigma)
identity('Chirped packet overlap modulus',chirp*s.exp(-dp*dp/(8*sigma*sigma)),s.exp(-(1+C*C)*dp*dp/(8*sigma*sigma)))
taup,delay=s.symbols('taup delay',positive=True)
det,ph=s.symbols('det ph',real=True)
ramsey=s.exp(-s.I*det*delay/2)+s.exp(s.I*ph+s.I*det*delay/2)
identity('Ramsey amplitude factorization',s.expand_complex(ramsey),s.expand_complex(2*s.exp(s.I*ph/2)*s.cos((det*delay+ph)/2)))
identity('Ramsey coherent probability factor',s.trigsimp(s.expand_complex(ramsey*s.conjugate(ramsey))),4*s.cos((det*delay+ph)/2)**2)

nbar,r=s.symbols('nbar r',positive=True)
th=s.symbols('th',real=True)
logchi=r*nbar*(s.exp(s.I*th)-1)+r*(nbar+1)*(s.exp(-s.I*th)-1)
identity('Thermal characteristic real and imaginary terms',s.expand_complex(logchi),-s.I*r*s.sin(th)-r*(2*nbar+1)*(1-s.cos(th)))
identity('Thermal mean',s.diff(logchi,th).subs(th,0)/s.I,-r)
identity('Thermal variance',-s.diff(logchi,th,2).subs(th,0),r*(2*nbar+1))
identity('Thermal fourth cumulant',s.diff(logchi,th,4).subs(th,0),r*(2*nbar+1))
charcoh=s.series(s.besselj(0,4*beta*s.sin(th/2)),th,0,6).removeO()
logcoh=s.series(s.log(charcoh),th,0,6).removeO()+r*(s.exp(-s.I*th)-1)
identity('Coherent fourth cumulant',s.diff(logcoh,th,4).subs(th,0),r+2*beta**2-6*beta**4)
identity('Equal-intensity fourth cumulant difference',r*(2*nbar+1)-(r+2*beta**2-6*beta**4).subs(beta**2,r*nbar),6*r*r*nbar*nbar)

z,t=s.symbols('z t',real=True)
a0=s.symbols('a0')
dd=1+2*s.I*hbar*a0*t/mass
psi=s.exp(-a0*z*z/dd)/s.sqrt(dd)
identity('Exact Gaussian TDSE residual',(s.I*hbar*s.diff(psi,t)+hbar*hbar/(2*mass)*s.diff(psi,z,2))/psi)
AA=a0-s.I*mass/(2*hbar*t)
BB=-s.I*mass*z/(hbar*t)
CC=s.I*mass*z*z/(2*hbar*t)
identity('Gaussian propagator integral exponent',CC+BB*BB/(4*AA),-a0*z*z/dd)
identity('Gaussian propagator squared prefactor',mass/(2*s.I*hbar*t*AA),1/dd)
ar=s.symbols('ar',positive=True)
ai=s.symbols('ai',real=True)
complex_a=ar+s.I*ai
complex_d=dd.subs(a0,complex_a)
identity('Gaussian TDSE normalization real exponent',s.re(complex_a/complex_d),ar/(s.re(complex_d)**2+s.im(complex_d)**2))
ut=s.symbols('ut',real=True)
width=(1+C*ut)**2+ut*ut
identity('Gaussian width completing square',width,(1+C*C)*(ut+C/(1+C*C))**2+1/(1+C*C))
focus=-C/(1+C*C)
identity('Gaussian focal time stationary condition',s.diff(width,ut).subs(ut,focus))
identity('Gaussian minimal width',width.subs(ut,focus),1/(1+C*C))
sig=s.symbols('sig',positive=True)
varp=hbar*hbar*(1+C*C)/(4*sig*sig)
cov=hbar*C/2
identity('Gaussian covariance uncertainty determinant',sig*sig*varp-cov*cov,hbar*hbar/4)
tf=focus*2*mass*sig*sig/hbar
identity('Gaussian zero covariance at focus',cov+tf*varp/mass)
identity('Gaussian minimum width momentum product squared',sig*sig/(1+C*C)*varp,hbar*hbar/4)

# Algebra introduced to explain the lecture's representations and noise example.
zw,pw=s.symbols('zw pw',real=True)
star_zp=zw*pw+s.I*hbar/2
star_pz=pw*zw-s.I*hbar/2
identity('Weyl canonical star commutator',star_zp-star_pz,s.I*hbar)
prob0,prob1=s.symbols('prob0 prob1',real=True)
chi=prob0+prob1*s.exp(s.I*th)+(1-prob0-prob1)*s.exp(-s.I*th)
mean=prob1-(1-prob0-prob1)
moment2=1-prob0
identity('Characteristic function first derivative',-s.I*s.diff(chi,th).subs(th,0),mean)
identity('Characteristic function second derivative',-s.diff(chi,th,2).subs(th,0),moment2)
identity('Log characteristic function variance',-s.diff(s.log(chi),th,2).subs(th,0),moment2-mean**2)
xx,anoise=s.symbols('xx anoise',positive=True)
free=anoise**2*(xx-1+s.exp(-xx))
echo=anoise**2*(xx-3+4*s.exp(-xx/2)-s.exp(-xx))
identity('Analytic noise echo improvement',free-echo,2*anoise**2*(1-s.exp(-xx/2))**2)
epsnoise=s.symbols('epsnoise',positive=True)
limit2=-s.log(1-epsnoise)/(anoise**2*(1-s.exp(-xx)))
identity('Noise error threshold exponent',-limit2*anoise**2*(1-s.exp(-xx)),s.log(1-epsnoise))
identity('Gaussian diffraction time width ratio',width.subs({C:0,ut:1}),2)

report={'symbolic_checks':len(results),'engine':'SymPy '+s.__version__,'checks':results}
(OUT/'electron-symbolic-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(results),'exact symbolic identities.')
