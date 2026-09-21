import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import figure_style, polish_axes, save_figure, COLORS, add_dual_legend
from matplotlib.lines import Line2D

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

def finite_or_zero(value):
    return value if np.isfinite(value) else 0.0


def main():
    T=np.linspace(0,5.5,1000)
    with figure_style():
        fig,ax=plt.subplots()
        for i,q in enumerate((3,4,5)):
            mb=np.array([finite_or_zero(abs(bethe_values(max(t,5e-2),q)[3])) for t in T])
            mw=np.array([finite_or_zero(abs(bw_values(max(t,5e-2),q)[0])) for t in T])
            ax.plot(T,mb,color=COLORS[i],ls="-",label=rf"$q={q}$"); ax.plot(T,mw,color=COLORS[i],ls="--")
        add_dual_legend(ax,
            handles1=[Line2D([0],[0],color="black",ls="-",label="Bethe"),
                      Line2D([0],[0],color="black",ls="--",label="B--W")],
            handles2=[Line2D([0],[0],color=COLORS[i],ls="-",label=rf"$q={q}$") for i,q in enumerate((3,4,5))],
            kw1=dict(loc="upper right"), kw2=dict(loc="lower left"))
        ax.set(xlabel=r"$kT/J$",ylabel=r"$m$",xlim=(0,5.5),ylim=(0,1.03)); polish_axes(ax)
        save_figure(fig, "order_parameter.png", output_dir=pathlib.Path(__file__).resolve().parent.parent)
if __name__=="__main__": main()
