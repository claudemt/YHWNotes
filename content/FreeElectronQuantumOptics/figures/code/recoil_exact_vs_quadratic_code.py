from pathlib import Path
import sys, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'fig'))

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import figure_style, polish_axes, COLORS, save_pdf_png_pair, add_legend

hbar=1.054571817e-34
m=9.1093837139e-31
c=299792458.0
eV=1.602176634e-19
lam=800e-9
omega=2*np.pi*c/lam
K=20e3*eV
gamma=1+K/(m*c*c)
v=c*np.sqrt(1-gamma**-2)
p=gamma*m*v
kappa=omega/v
ell=np.arange(-12,13)
def E(pp):
    return np.sqrt((m*c*c)**2+(c*pp)**2)
exact=(E(p+(ell+1)*hbar*kappa)-E(p+ell*hbar*kappa))/hbar
quad=v*kappa+(2*ell+1)*hbar*kappa*kappa/(2*gamma**3*m)
shift_exact=(exact-v*kappa)/(2*np.pi*1e9)
shift_quad=(quad-v*kappa)/(2*np.pi*1e9)
with figure_style():
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(ell,shift_exact,marker='o',label='exact relativistic dispersion',color=COLORS[0])
    ax.plot(ell,shift_quad,linestyle='--',label='quadratic recoil',color=COLORS[1])
    ax.set_xlabel(r'edge index $\ell$')
    ax.set_ylabel(r'$\delta f_\ell$ (GHz)')
    polish_axes(ax,grid=True,minor_ticks=False)
    add_legend(ax, frameon=True)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'recoil_exact_vs_quadratic', output_dir=ROOT/'figures'/'generated')
