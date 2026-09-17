"""Rebuild legacy quantitative figures from the formulas printed in the manuscript.

This file replaces PDF-only historical assets with reproducible PDF/PNG pairs.
All plots use the project-wide YHWNotes-compatible style helper.
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, m_e, e, epsilon_0, hbar
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fig"))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import (  # noqa: E402
    add_legend,    figure_style,
    polish_axes,
    COLORS,
    LINE_STYLES,
    save_pdf_png_pair,
)

OUT = ROOT / "figures" / "generated"
OUT.mkdir(parents=True, exist_ok=True)
alpha = e**2 / (4.0 * np.pi * epsilon_0 * hbar * c)


def save(fig, stem):
    fig.tight_layout()
    save_pdf_png_pair(fig, stem, output_dir=OUT)


# ---------------------------------------------------------------------------
# QED massless charged-fermion angular distributions, normalized at 90 deg.
# ---------------------------------------------------------------------------
theta = np.linspace(np.deg2rad(5.0), np.deg2rad(175.0), 800)
ct = np.cos(theta)
st2 = np.sin(theta) ** 2
angle_deg = np.rad2deg(theta)

with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    shape = (4.0 + (1.0 + ct) ** 2) / (1.0 - ct) ** 2
    ax.semilogy(angle_deg, shape / 5.0, color=COLORS[0])
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"relative distribution")
    ax.set_xlim(5, 175)
    polish_axes(ax, grid=True)
    save(fig, "emu_angular_distribution")

with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    shape = 1.0 + ct**2
    ax.plot(angle_deg, shape, color=COLORS[1])
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"$1+\cos^2\theta$")
    ax.set_xlim(5, 175)
    polish_axes(ax, grid=True)
    save(fig, "ee_mumu_angular_distribution")

with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    shape = (3.0 + ct**2) ** 2 / st2**2
    ax.semilogy(angle_deg, shape / 9.0, color=COLORS[2])
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"relative distribution")
    ax.set_xlim(5, 175)
    polish_axes(ax, grid=True)
    save(fig, "moller_angular_distribution")

with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    shape = (3.0 + ct**2) ** 2 / (1.0 - ct) ** 2
    ax.semilogy(angle_deg, shape / 9.0, color=COLORS[3])
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"relative distribution")
    ax.set_xlim(5, 175)
    polish_axes(ax, grid=True)
    save(fig, "bhabha_angular_distribution")


# ---------------------------------------------------------------------------
# Klein--Nishina angular kernel in units of r_e^2.
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    theta_kn = np.linspace(0.0, np.pi, 720)
    cth = np.cos(theta_kn)
    for i, x in enumerate([0.01, 0.5, 2.0]):
        ratio = 1.0 / (1.0 + x * (1.0 - cth))
        kernel = 0.5 * ratio**2 * (1.0 / ratio + ratio - np.sin(theta_kn) ** 2)
        ax.plot(np.rad2deg(theta_kn), kernel, color=COLORS[i], linestyle=LINE_STYLES[i], label=fr"$x={x:g}$")
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"$(1/r_e^2)\,d\sigma/d\Omega$")
    ax.set_xlim(0, 180)
    add_legend(ax, frameon=True)
    polish_axes(ax, grid=True)
    save(fig, "compton_klein_nishina")


# ---------------------------------------------------------------------------
# Exact relativistic dispersion and its local first/second-order expansions.
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    mc2 = m_e * c**2
    K0 = 200.0e3 * e
    E0 = mc2 + K0
    p0 = np.sqrt(E0**2 - mc2**2) / c
    v0 = c**2 * p0 / E0
    gamma0 = E0 / mc2
    mpar = gamma0**3 * m_e
    q = np.linspace(-0.38, 0.38, 700)
    dp = q * p0
    E_exact = np.sqrt(mc2**2 + c**2 * (p0 + dp) ** 2)
    y_exact = (E_exact - E0) / mc2
    y_lin = v0 * dp / mc2
    y_quad = (v0 * dp + dp**2 / (2.0 * mpar)) / mc2
    ax.plot(q, y_exact, color=COLORS[0], label="exact relativistic dispersion")
    ax.plot(q, y_lin, linestyle="--", color=COLORS[1], label="linear expansion")
    ax.plot(q, y_quad, linestyle="-.", color=COLORS[2], label="quadratic expansion")
    ax.set_xlabel(r"$\delta p/p_0$")
    ax.set_ylabel(r"$(E-E_0)/(m_ec^2)$")
    add_legend(ax, frameon=True)
    polish_axes(ax, grid=True)
    save(fig, "dispersion_control")


# ---------------------------------------------------------------------------
# One-loop Pauli form factor, normalized by F2(0).
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    q = np.logspace(-2.0, 1.6, 420)
    # Integral can be evaluated stably with Gauss-Legendre nodes.
    nodes, weights = np.polynomial.legendre.leggauss(180)
    u = 0.5 * (nodes + 1.0)
    w = 0.5 * weights
    ratio = np.array([np.sum(w / (1.0 + qq**2 * u * (1.0 - u))) for qq in q])
    ax.semilogx(q, ratio, color=COLORS[0])
    ax.set_xlabel(r"$Q/(m_ec)$")
    ax.set_ylabel(r"$F_2^{(1)}(-Q^2)/F_2^{(1)}(0)$")
    ax.set_ylim(0, 1.04)
    polish_axes(ax, grid=True)
    save(fig, "qed_pauli_form_factor_r14")


# ---------------------------------------------------------------------------
# Uehling correction relative to the Coulomb potential.
# ---------------------------------------------------------------------------
def uehling_ratio(x):
    def integrand(t):
        return np.exp(-2.0 * x * t) * (1.0 + 0.5 / t**2) * np.sqrt(t**2 - 1.0) / t**2
    val, _ = quad(integrand, 1.0, np.inf, epsabs=2e-11, epsrel=2e-9, limit=350)
    return 2.0 * alpha / (3.0 * np.pi) * val

with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    x = np.logspace(-1.5, 0.65, 180)
    y = np.array([uehling_ratio(xx) for xx in x])
    ax.loglog(x, y, color=COLORS[1])
    ax.set_xlabel(r"$r/\lambda_C$")
    ax.set_ylabel(r"$\delta V_U/V_C$")
    polish_axes(ax, grid=True)
    save(fig, "uehling_relative")


# ---------------------------------------------------------------------------
# Soft-bremsstrahlung angular geometry factor for one explicit deflection.
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    beta = 0.80
    deflection = np.deg2rad(25.0)
    beta_i = beta * np.array([0.0, 0.0, 1.0])
    beta_f = beta * np.array([np.sin(deflection), 0.0, np.cos(deflection)])
    th = np.linspace(0.0, np.pi, 800)
    geom = np.zeros_like(th)
    for j, tj in enumerate(th):
        n = np.array([np.sin(tj), 0.0, np.cos(tj)])
        def bperp(b):
            return b - n * np.dot(n, b)
        vec = bperp(beta_f) / (1.0 - np.dot(n, beta_f)) - bperp(beta_i) / (1.0 - np.dot(n, beta_i))
        geom[j] = np.dot(vec, vec)
    ax.plot(np.rad2deg(th), geom, color=COLORS[2])
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"soft-photon geometry factor")
    ax.text(0.04, 0.94, r"$\beta_i=\beta_f=0.8$\ndeflection $25^\circ$", transform=ax.transAxes, va="top")
    polish_axes(ax, grid=True)
    save(fig, "soft_brems_angular")


# ---------------------------------------------------------------------------
# Volkov effective mass for circular and linear polarization.
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    a0 = np.linspace(0.0, 4.0, 500)
    mcirc = np.sqrt(1.0 + a0**2)
    mlin = np.sqrt(1.0 + 0.5 * a0**2)
    ax.plot(a0, mcirc, color=COLORS[0], label="circular polarization")
    ax.plot(a0, mlin, linestyle="--", color=COLORS[1], label="linear polarization")
    ax.set_xlabel(r"$a_0$")
    ax.set_ylabel(r"$m_*/m_e$")
    add_legend(ax, frameon=True)
    polish_axes(ax, grid=True)
    save(fig, "volkov_effective_mass")


# ---------------------------------------------------------------------------
# Scalar-Yukawa elastic scattering, normalized at 90 deg.
# rho=mc/p is fixed; mu=m_Y c/p is varied.
# ---------------------------------------------------------------------------
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    theta_y = np.linspace(np.deg2rad(4.0), np.deg2rad(176.0), 800)
    cy = np.cos(theta_y)
    rho = 0.20
    for i, mu in enumerate([0.30, 1.0, 3.0]):
        def shape(cosv):
            return (4.0 * rho**2 + 2.0 * (1.0 - cosv))**2 / (mu**2 + 2.0 * (1.0 - cosv))**2
        y = shape(cy) / shape(0.0)
        ax.semilogy(np.rad2deg(theta_y), y, color=COLORS[i], linestyle=LINE_STYLES[i], label=fr"$m_Yc/p={mu:g}$")
    ax.set_xlabel(r"$\theta$ [deg]")
    ax.set_ylabel(r"Yukawa relative distribution")
    ax.text(0.04, 0.94, "mc/p = 0.20", transform=ax.transAxes, va="top")
    add_legend(ax, frameon=True)
    polish_axes(ax, grid=True)
    save(fig, "yukawa_angular_distribution")
