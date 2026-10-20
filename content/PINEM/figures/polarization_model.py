"""Rayleigh sphere PINEM: one phasor convention and both dipolar channels.

Physical model (SI): E(t)=Re[E_omega exp(-i omega t)].
E_z is the quasistatic induced dipole field and the electron is a straight
trajectory r=(b cos phi,b sin phi,z), z=vt. Permittivity is phenomenological
and wavelength-independent for this pedagogical example.
"""
from __future__ import annotations
import numpy as np
from scipy.constants import c, epsilon_0, elementary_charge, hbar
from scipy.integrate import simpson
from scipy.special import kv, jv

radius = 30e-9
wavelength = 800e-9
velocity = .60 * c
omega = 2 * np.pi * c / wavelength
kappa = omega / velocity
relative_epsilon = 3.0 + .10j
incident_field = 1.0e9
chi = (relative_epsilon - 1) / (relative_epsilon + 2)
reference_dipole = 4*np.pi*epsilon_0*radius**3*chi*incident_field
beta_scale = -elementary_charge*kappa**2*reference_dipole/(4*np.pi*epsilon_0*hbar*omega)


def beta_parts(impact):
    """Complex electron sideband couplings for p_b=p0 and p_z=p0."""
    y = kappa*np.asarray(impact)
    return 1j*beta_scale*kv(1,y), beta_scale*kv(0,y)


def beta(impact, mixing=0., relative_phase=0., azimuth=0.):
    transverse, longitudinal = beta_parts(impact)
    return (transverse*np.cos(mixing)*np.cos(azimuth)
            + longitudinal*np.sin(mixing)*np.exp(1j*relative_phase))


def field_z(z, impact, channel):
    """The signed longitudinal phasor E_{omega,z}, for a transverse or z dipole."""
    r2 = impact**2 + np.asarray(z)**2
    if channel == 'transverse':
        numerator = 3*reference_dipole*impact*np.asarray(z)
    elif channel == 'longitudinal':
        numerator = reference_dipole*(2*np.asarray(z)**2-impact**2)
    else:
        raise ValueError(channel)
    return numerator/(4*np.pi*epsilon_0*r2**2.5)


def integrate_beta(impact, channel, n=20001, cutoff=350.):
    z=np.linspace(-cutoff*radius,cutoff*radius,n)
    integral=simpson(field_z(z,impact,channel)*np.exp(-1j*kappa*z),x=z)
    return elementary_charge*integral/(2*hbar*omega)


def sideband(orders, coupling):
    return jv(orders,2*np.abs(coupling))**2


def inelastic(coupling):
    return 1-jv(0,2*np.abs(coupling))**2


def cancellation_angle(impact):
    return np.arctan(kv(1,kappa*impact)/kv(0,kappa*impact))


def check():
    for impact in (1.2*radius,2*radius,4.4*radius):
        for channel,exact in zip(('transverse','longitudinal'),beta_parts(impact)):
            actual=integrate_beta(impact,channel)
            relative=abs(actual-exact)/max(abs(exact),1e-15)
            assert relative < 1.2e-3,(impact,channel,relative)
    impact=2*radius
    assert abs(beta(impact,cancellation_angle(impact),-np.pi/2))<1e-12
    theta=np.linspace(-np.pi,np.pi,241)
    g=beta(impact,cancellation_angle(impact),theta)
    n=np.arange(-30,31)[:,None]
    assert np.max(abs(sideband(n,g[None,:]).sum(axis=0)-1)) < 1e-12
    # Coherent classical PINEM must obey P(+n)=P(-n).
    assert np.max(abs(sideband(1,g)-sideband(-1,g)))<1e-13
    return True

if __name__=='__main__':
    check()
    print('PASS: Rayleigh K0/K1 quadrature, coherent extinction and Bessel normalization')
