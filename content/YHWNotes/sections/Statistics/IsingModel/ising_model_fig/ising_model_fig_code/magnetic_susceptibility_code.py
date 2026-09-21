import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, add_legend, COLORS

def gamma_c(q): return 0.5*np.log(q/(q-2))
def a_order(g,q):
    if g<=gamma_c(q): return 0.0
    def f(a): return np.exp(2*a/(q-1))*np.cosh(a-g)-np.cosh(a+g)
    lo=1e-9; hi=max(1.0,2.0*g)
    while f(hi)<=0 and hi<128:
        hi*=2.0
    if f(hi)<=0: return np.nan
    return brentq(f,lo,hi,maxiter=160)
def mp_order(g,q):
    if g<=1/q: return 0.0
    f=lambda m:m-np.tanh(q*g*m)
    return brentq(f,1e-8,1.0,maxiter=200)
def bethe_values(T,q):
    g=1/T; a=a_order(g,q); den=np.cosh(2*a)+np.exp(-2*g)
    pmp=np.exp(-2*g)/(2*den); ppp=np.exp(2*a)/(2*den); pp=(np.exp(-2*g)+np.exp(2*a))/(2*den)
    m=np.sinh(2*a)/den
    chi=(8*g*(1+np.exp(-2*g)*np.cosh(2*a))/den**2)/np.log(q/(q-2))*(2-(q-1)*(np.tanh(a+g)-np.tanh(a-g)))
    d2=np.cosh(2*a)+np.cosh(2*g)-(q-1)*np.sinh(2*g)
    C=g*g*(2*q*np.exp(-2*g)/den**2)*(np.cosh(2*a)+(q-1)*np.sinh(2*a)**2/d2)
    return pmp,ppp,pp,m,chi,C
def bw_values(T,q):
    g=1/T; m=mp_order(g,q)
    den=1-q*g*(1-m*m)
    C=0.0 if g<=1/q else g*g*q*q*m*m*(1-m*m)/den
    return m,C

def finite_or_zero(value, limit=3):
    return value if np.isfinite(value) and abs(value) <= limit else 0.0


def main():
    T=np.linspace(0,8,1000)
    with figure_style():
        fig,ax=plt.subplots()
        for i,q in enumerate((3,4,5)):
            y=np.array([finite_or_zero(bethe_values(max(t,5e-2),q)[4]) for t in T])
            ax.plot(T,y,color=COLORS[i],label=rf"$q={q}$")
        ax.set(xlabel=r"$kT/J$",ylabel=r"$\chi$",xlim=(0,8),ylim=(0,1.3)); polish_axes(ax); add_legend(ax, loc="lower right")
        save_figure(fig, "magnetic_susceptibility.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
