from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, save_pdf_png_pair, add_legend

# Dimensionless y = Q/(m_e c). Plot -Pi_R(-Q^2)/alpha.
def direct(y):
    f = lambda x: x*(1-x)*np.log1p(y*y*x*(1-x))
    val, _ = quad(f, 0.0, 1.0, epsabs=2e-11, epsrel=2e-11, limit=200)
    return 2.0/np.pi * val

def dispersive(y):
    # -Pi/alpha = y^2/(3 pi) int_4^inf dt beta(t)(1+2/t)/[t(t+y^2)]
    def integrand(t):
        beta = np.sqrt(max(0.0, 1.0-4.0/t))
        return beta*(1.0+2.0/t)/(t*(t+y*y))
    val, _ = quad(integrand, 4.0, np.inf, epsabs=3e-10, epsrel=3e-10, limit=400)
    return y*y/(3.0*np.pi)*val

y = np.logspace(-2.0, 1.35, 90)
d = np.array([direct(v) for v in y])
s = np.array([dispersive(v) for v in y])

with figure_style():
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    ax.plot(y, d, linewidth=3.2, label='Feynman-parameter integral')
    ax.plot(y, s, '--', linewidth=2.5, label='cut + dispersion relation')
    ax.set_xscale('log')
    ax.set_xlabel(r'$Q/(m_e c)$')
    ax.set_ylabel(r'$-\Pi_R(-Q^2)/\alpha$')
    polish_axes(ax, grid=True)
    add_legend(ax, frameon=False)
    fig.subplots_adjust(left=0.18, bottom=0.18, right=0.98, top=0.97)
    save_pdf_png_pair(fig, 'qed_vacpol_dispersion_dp9', output_dir=ROOT/'figures'/'generated')

