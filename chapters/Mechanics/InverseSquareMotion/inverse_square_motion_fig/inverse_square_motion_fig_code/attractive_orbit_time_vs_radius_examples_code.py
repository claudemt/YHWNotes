import numpy as np
import matplotlib.pyplot as plt
from fig_style_python import figure_style, polish_axes, save_figure, add_legend, COLORS

PARAMS=[(3.8,1.5),(0.48,0.95),(0.30,1.10),(1.10,0.85)]
LABELS=[rf"$\tilde{{\alpha}}={a:.2f},\ \tilde{{E}}={b:.2f}$" for a,b in PARAMS]

def disc(a,b): return a*a*b*b-(b*b-1)*(a*a-1)

def r_curve(index,phi):
    a,b=PARAMS[index]; D=np.sqrt(disc(a,b))
    if index==0:
        den=-a*b+D*np.cosh(np.sqrt(a*a-1)*phi)
        return (a*a-1)/np.sqrt(np.where(den>0,den,np.nan))
    if index==1:
        return (1-a*a)/(a*b+D*np.cos(np.sqrt(1-a*a)*phi))
    if index==2:
        e=np.sqrt(1-((b*b-1)*(a*a-1))/(a*a*b*b))
        return (1-a*a)/(1+e*np.cos(np.sqrt(1-a*a)*phi))
    return (a*a-1)/(-a*b+D*np.cosh(np.sqrt(a*a-1)*phi))

def t_curve(index,r):
    a,b=PARAMS[index]
    D=np.sqrt(disc(a,b))
    rad=(b*b-1)*r*r+2*a*b*r+a*a-1
    first=b/(b*b-1)*np.sqrt(np.where(rad>=0,rad,np.nan))
    arg=(a*b+r*(b*b-1))/D
    if b>1:
        second=a/(b*b-1)**1.5*np.arccosh(np.where(arg>=1,arg,np.nan))
        return first-second
    second=a/(1-b*b)**1.5*np.arccos(np.clip(arg,-1,1))
    valid=(arg>=-1)&(arg<=1)&(rad>=0)
    return np.where(valid,first+second,np.nan)


def main():
    r=np.linspace(0,8.5,4000)
    with figure_style():
        fig,ax=plt.subplots(figsize=(13.0,8.0))
        for i in range(4): ax.plot(r,t_curve(i,r),color=COLORS[i],label=LABELS[i])
        ax.set(xlabel=r"$\tilde{r}$",ylabel=r"$\tilde{t}$")
        ax.set_xlim(0,8.7); ax.set_ylim(0,52)
        polish_axes(ax); add_legend(ax, outside=False, loc="upper left")
        save_figure(fig,"attractive_orbit_time_vs_radius_examples.png")
if __name__=="__main__": main()
