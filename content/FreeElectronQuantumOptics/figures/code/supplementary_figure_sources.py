from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, LINE_STYLES, figure_style, polish_axes, save_pdf_png_pair, add_legend  # noqa: E402

FIG = ROOT / 'figures'
GEN = ROOT / 'figures' / 'generated'

# 1) sm_higgs_potential_dp11
with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.6))
    x = np.linspace(-1.8, 1.8, 600)
    V = 0.35 * x**4 - x**2
    ax.plot(x, V, color=COLORS[0], linewidth=2.8)
    xmin = 1/np.sqrt(0.7)
    for s in (-xmin, xmin):
        ax.plot(s, 0.35*s**4 - s**2, marker='o', color=COLORS[1], markersize=8)
    ax.axvline(0.0, color='0.4', linestyle=':', linewidth=1.3)
    ax.axhline(0.0, color='0.4', linestyle=':', linewidth=1.0)
    ax.text(-1.48, 0.28, 'unstable symmetric point')
    ax.text(0.62, -0.50, 'degenerate minima', bbox=dict(facecolor='white', edgecolor='none', alpha=0.85))
    ax.set_xlabel(r'$h/v_E$')
    ax.set_ylabel(r'normalized potential $V/V_0$')
    ax.set_title('Higgs potential')
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'sm_higgs_potential_dp11', output_dir=GEN)

# 2) sm_gauge_running_dp11
with figure_style():
    fig, ax = plt.subplots(figsize=(8.5, 5.8))
    mu = np.logspace(2, 16, 500)
    t = np.log(mu / 91.1876)
    gY0, g20, g30 = 0.357, 0.652, 1.221
    bY, b2, b3 = 41/6, -19/6, -7
    def run(g0, b):
        inv = 1/g0**2 - b/(8*np.pi**2)*t
        return 1/np.sqrt(inv)
    ax.plot(mu, run(gY0,bY), label=r'$g_Y(\mu)$', color=COLORS[0], linestyle=LINE_STYLES[0])
    ax.plot(mu, run(g20,b2), label=r'$g(\mu)$', color=COLORS[1], linestyle=LINE_STYLES[1])
    ax.plot(mu, run(g30,b3), label=r'$g_s(\mu)$', color=COLORS[2], linestyle=LINE_STYLES[2])
    ax.set_xscale('log')
    ax.set_xlabel(r'$\mu$ [GeV]')
    ax.set_ylabel('one-loop coupling')
    ax.set_title('SM gauge running')
    ax.set_ylim(0.25, 1.35)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'sm_gauge_running_dp11', output_dir=GEN)

# 3) yukawa_decay_threshold.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    x = np.linspace(1.0, 4.0, 500)   # x = m_X/(2m_f)
    beta = np.sqrt(1.0 - 1.0/x**2)
    ax.plot(x, beta**3, label=r'scalar: $\beta^3$', color=COLORS[0], linestyle=LINE_STYLES[0])
    ax.plot(x, beta, label=r'pseudoscalar: $\beta$', color=COLORS[1], linestyle=LINE_STYLES[1])
    ax.set_xlabel(r'$m_X/(2m_f)$')
    ax.set_ylabel(r'normalized width factor')
    ax.set_title('Yukawa decay threshold')
    ax.set_xlim(1.0, 4.0)
    ax.set_ylim(0.0, 1.05)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'yukawa_decay_threshold', output_dir=FIG)

# 4) breit_wheeler_total.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    beta = np.linspace(1e-3, 0.995, 800)
    sigma = 0.5*(1-beta**2)*((3-beta**4)*np.log((1+beta)/(1-beta)) - 2*beta*(2-beta**2))
    ax.plot(beta, sigma, color=COLORS[0], linewidth=2.6)
    ax.set_xlabel(r'$\beta_{\rm pair}$')
    ax.set_ylabel(r'$\sigma_{\rm BW}/(\pi r_e^2)$')
    ax.set_title('Breit--Wheeler cross section')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, max(sigma)*1.08)
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'breit_wheeler_total', output_dir=FIG)

# 5) mott_rutherford_angular.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    th = np.linspace(np.deg2rad(5), np.deg2rad(175), 700)
    norm_idx = np.argmin(np.abs(th - np.deg2rad(30)))
    for beta_e, color, ls in zip([0.3, 0.6, 0.9], COLORS[:3], LINE_STYLES[:3]):
        y = 1 - beta_e**2 * np.sin(th/2)**2
        y = y / y[norm_idx]
        ax.plot(np.rad2deg(th), y, label=rf'$\beta_e={beta_e:.1f}$', color=color, linestyle=ls)
    ax.set_xlabel(r'$\theta$ [deg]')
    ax.set_ylabel('relative Mott factor')
    ax.set_title('Relativistic Rutherford factor')
    ax.set_xlim(0, 180)
    ax.set_ylim(0.1, 1.2)
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=True, framealpha=0.94)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'mott_rutherford_angular', output_dir=FIG)

# 6) recoil_two_level_selection.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(5.0, 6.6))
    ell = np.array([-1, 0, 1, 2])
    E = np.array([2.0, 0.0, 0.0, 2.0])
    labels = ['-1', '0', '1', '2']
    for lv, en, lab in zip(ell, E, labels):
        ax.hlines(en, lv-0.32, lv+0.32, linewidth=3.0, color=COLORS[0])
        ax.text(lv, en+0.12, rf'$\ell={lab}$', ha='center')
    ax.add_patch(FancyArrowPatch((0,0.08),(1,0.08), arrowstyle='<->', mutation_scale=18, linewidth=2.0, color=COLORS[1]))
    ax.text(0.5, 0.26, 'resonant', ha='center')
    ax.text(-1, 2.18, r'$\delta_{-1}\approx2\omega_r$', ha='center')
    ax.text(2, 2.18, r'$\delta_{2}\approx2\omega_r$', ha='center')
    ax.set_xlim(-1.8, 2.8)
    ax.set_ylim(-0.4, 2.8)
    ax.set_xlabel('momentum ladder index')
    ax.set_ylabel('effective detuning scale')
    ax.set_title('Recoil-selected two-level window')
    polish_axes(ax, grid=False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'recoil_two_level_selection', output_dir=FIG)

# 7) pinem_energy_ladder.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(5.4, 6.8))
    levels = np.arange(-3, 4)
    for l in levels:
        y = l
        ax.hlines(y, -0.6, 0.6, color=COLORS[0], linewidth=2.8)
        ax.text(0.72, y-0.08, rf'$E_0{l:+d}\hbar\omega$')
    ax.add_patch(FancyArrowPatch((-0.25,-2.4),(-0.25,2.4), arrowstyle='<->', mutation_scale=20, linewidth=2.0, color=COLORS[1]))
    ax.text(-0.92, 0.0, r'absorption / emission', rotation=90, va='center')
    ax.text(-0.1, -3.75, r'uniform spacing $\hbar\omega$')
    ax.set_xlim(-1.3, 2.6)
    ax.set_ylim(-3.9, 3.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Recoil-free PINEM ladder')
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'pinem_energy_ladder', output_dir=FIG)

# 8) pinem_experiment_geometry.pdf
with figure_style():
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    # electron beam
    ax.add_patch(FancyArrowPatch((0.8,3.0),(9.3,3.0), arrowstyle='->', mutation_scale=20, linewidth=2.6, color=COLORS[0]))
    ax.text(1.0, 3.35, 'electron beam')
    # nanostructure
    ax.add_patch(Rectangle((4.4,1.4), 0.45, 3.2, fill=False, linewidth=2.2, edgecolor=COLORS[1]))
    ax.text(4.1, 4.95, 'nanostructure')
    # optical near field waves
    xs = np.linspace(4.9, 7.6, 250)
    ys = 3.0 + 0.7*np.sin(5*(xs-4.9))*np.exp(-0.45*(xs-4.9))
    ax.plot(xs, ys, color=COLORS[2], linewidth=2.2)
    ax.text(6.3, 4.25, 'synchronous\nnear field', ha='center', va='bottom')
    # spectrometer box
    ax.add_patch(Rectangle((8.0,1.9),1.1,2.2, fill=False, linewidth=2.0, edgecolor=COLORS[3]))
    ax.text(8.55, 4.35, 'EELS', ha='center')
    ax.text(7.9, 1.35, 'sideband readout')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('PINEM geometry')
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'pinem_experiment_geometry', output_dir=FIG)
