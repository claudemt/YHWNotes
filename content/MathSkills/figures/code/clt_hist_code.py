from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

rng = np.random.default_rng(2024)
n_unif, n_exp = 12, 12
N = 200000
with figure_style():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    # Uniform(0,1): mean .5, var 1/12 -> standardized sum
    U = rng.random((N, n_unif)).sum(axis=1)
    zU = (U - n_unif * 0.5) / (np.sqrt(n_unif / 12.0))
    # Exp(1): mean 1, var 1
    E = rng.exponential(1.0, size=(N, n_exp)).sum(axis=1)
    zE = (E - n_exp) / np.sqrt(n_exp)
    x = np.linspace(-4, 4, 400)
    pdf = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    for ax, z, title in [(axes[0], zU, r'$\mathrm{Uniform}(0,1)$, $n=12$'),
                        (axes[1], zE, r'$\mathrm{Exp}(1)$, $n=12$')]:
        ax.hist(z, bins=80, density=True, color="#9ecae1",
                edgecolor="0.5", linewidth=0.4, label="standardized sum")
        ax.plot(x, pdf, color="#d62728", linewidth=1.8,
                label=r'$N(0,1)$ density')
        ax.set_xlim(-4, 4); ax.set_ylim(0, 0.55)
        ax.set_xlabel("standardized sum"); ax.set_ylabel("density")
        ax.set_title(title)
        add_legend(ax, loc="upper right")
        polish_axes(ax, grid=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'clt_hist', Path(__file__).resolve().parents[1] / 'generated')
print('clt_hist done')
