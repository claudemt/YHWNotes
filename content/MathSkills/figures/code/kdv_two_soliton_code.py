from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

k1, k2 = 0.9, 0.5
x10, x20 = -4.0, 3.0
A = ((k1-k2)/(k1+k2))**2
x = np.linspace(-18, 20, 1900)
def u_two(x, t):
    eta1 = 2*k1*(x - 4*k1**2*t - x10)
    eta2 = 2*k2*(x - 4*k2**2*t - x20)
    e1, e2 = np.exp(eta1), np.exp(eta2)
    e12 = A*np.exp(eta1+eta2)
    tau = 1.0 + e1 + e2 + e12
    tau_x = 2*k1*e1 + 2*k2*e2 + 2*(k1+k2)*e12
    tau_xx = (2*k1)**2*e1 + (2*k2)**2*e2 + (2*(k1+k2))**2*e12
    return -2.0*(tau*tau_xx - tau_x**2)/tau**2

with figure_style():
    fig, ax = plt.subplots()
    for t in (-3.0, 3.0, 6.0):
        ax.plot(x, u_two(x, t), label=rf'$t={t:g}$')
    ax.set_xlim(-21, 20)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$u(x,t)$')
    add_legend(ax)
    polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'kdv_two_soliton', Path(__file__).resolve().parents[1] / 'generated')
