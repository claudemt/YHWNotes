from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, epsilon_0, mu_0, hbar, e, physical_constants

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend

eV = physical_constants['electron volt-joule relationship'][0]
hbar_omega_p_eV = 9.0
hbar_gamma_eV = 0.08
omega_p = hbar_omega_p_eV * eV / hbar
gamma = hbar_gamma_eV * eV / hbar
beta = 0.70
v = beta*c
b = 20e-9

energies = np.linspace(2.0, 7.5, 260) # eV
y = np.linspace(0.0, 14.0, 5000)     # y = k_y b
ky = y/b
spectrum = np.zeros_like(energies)


def kz_ret(kj2, kp2):
    z = np.sqrt((kj2-kp2)+0j)
    # retarded/outgoing branch: Im kz >= 0; if purely real choose Re kz >=0
    flip = (np.imag(z) < 0) | ((np.abs(np.imag(z)) < 1e-14) & (np.real(z) < 0))
    return np.where(flip, -z, z)

for i, Eev in enumerate(energies):
    omega = Eev*eV/hbar
    k0 = omega/c
    kx = omega/v
    kp2 = kx*kx + ky*ky
    kp = np.sqrt(kp2)
    eps1 = 1.0+0j
    eps2 = 1.0 - omega_p**2/(omega*(omega+1j*gamma))
    kz1 = kz_ret((eps1*k0*k0), kp2)
    kz2 = kz_ret((eps2*k0*k0), kp2)
    rp = (eps2*kz1-eps1*kz2)/(eps2*kz1+eps1*kz2)
    rs = (kz1-kz2)/(kz1+kz2)
    # For beta<1 and kx=omega/v, all sampled vacuum components are evanescent.
    kappa = np.imag(kz1)
    expfac = np.exp(-2*kappa*b)
    # Explicit x-x component of the Weyl scattering dyadic.
    Gxx_p = (kappa/(2*k0*k0))*(kx*kx/kp2)*rp*expfac
    Gxx_s = (1/(2*kappa))*(ky*ky/kp2)*rs*expfac
    integrand = np.imag(Gxx_p + Gxx_s)
    integral_ky = 2*np.trapezoid(integrand, ky)
    dP_domega_dL = mu_0*e**2/(2*np.pi**2*hbar) * integral_ky
    spectrum[i] = dP_domega_dL * (eV/hbar) * 1e-9  # per eV per nm

# Lossless synchronous surface-plasmon crossing for comparison.
eps_sync = 1.0/(beta**2-1.0)
omega_sync_over_wp = 1.0/np.sqrt(1.0-eps_sync)
E_sync = hbar_omega_p_eV*omega_sync_over_wp

with figure_style():
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(energies, spectrum, linewidth=2.0, label='full Weyl integral')
    ax.axvline(E_sync, linestyle='--', linewidth=1.5, label='lossless pole')
    ax.set_xlabel(r'$\hbar\omega$ [eV]')
    ax.set_ylabel(r'$(dP/dE)/L$ [eV$^{-1}$ nm$^{-1}$]')
    ax.set_xlim(energies[0], energies[-1])
    ax.set_ylim(bottom=0)
    polish_axes(ax, grid=True, minor_ticks=True)
    add_legend(ax, frameon=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'planar_drude_eels', output_dir=ROOT/'figures'/'generated')

print('E_sync_eV', E_sync)
print('peak_eV', energies[np.argmax(spectrum)])
print('peak_value_per_eV_nm', spectrum.max())
