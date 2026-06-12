import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS

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

def finite_or_zero(values):
    values=np.asarray(values,dtype=float)
    return np.where(np.isfinite(values),values,0.0)


def main():
    T=np.linspace(0,4,900); styles=["-","--",":"]; names=[r"$p_{+-}$",r"$p_{++}$",r"$p_+$"]
    with figure_style():
        fig,ax=plt.subplots(figsize=(12.8,7.4))
        for i,q in enumerate((3,4,5)):
            vals=finite_or_zero([bethe_values(max(t,5e-2),q)[:3] for t in T])
            for j in range(3): ax.plot(T,vals[:,j],color=COLORS[i],ls=styles[j],label=rf"$q={q}$" if j==0 else None)
        from matplotlib.lines import Line2D
        l1=ax.legend(
            handles=[Line2D([0],[0],color="black",ls=s,label=n) for s,n in zip(styles,names)],
            loc="lower left",
            bbox_to_anchor=(0.0, 0.36),
            frameon=False,
        ); ax.add_artist(l1)
        add_legend(ax, outside=False, loc="lower left"); ax.set(xlabel=r"$kT/J$",ylabel="probability",xlim=(0,4),ylim=(0,1.03)); polish_axes(ax)
        save_figure(fig,"state_probability.png")
if __name__=="__main__": main()
