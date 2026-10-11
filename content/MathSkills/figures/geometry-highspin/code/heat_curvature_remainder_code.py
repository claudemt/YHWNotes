"""Unit 2-sphere spectral heat trace and local geometric coefficients."""
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'preamble.py').exists())
sys.path.insert(0, str(ROOT))
from preamble import COLORS, REFERENCE_LINE_STYLE, figure_style, polish_axes, add_legend, save_pdf_png_pair
OUT = Path(__file__).resolve().parents[1]
with figure_style():
    t=np.linspace(.018,.42,300)
    ell=np.arange(0,180)
    traces=np.exp(-t[:,None]*(ell*(ell+1))[None,:])@(2*ell+1)
    quotient=(traces-1/t-1/3)/t
    assert abs(quotient[0]-1/15)<.002
    fig,ax=plt.subplots(figsize=(6.5,4.0))
    ax.plot(t,quotient,color=COLORS[0],label=r'exact spectrum: $(K-1/t-1/3)/t$')
    ax.axhline(1/15,**REFERENCE_LINE_STYLE,label=r'heat coefficient $1/15$')
    ax.set(xlabel=r'heat parameter $t/R^2$',ylabel='scaled remainder')
    ax.set_xlim(float(t.min()),float(t.max()))
    polish_axes(ax,grid=True)
    add_legend(ax,corner='upper left')
    fig.tight_layout(pad=1.05)
    save_pdf_png_pair(fig,'heat_curvature_remainder',OUT)
