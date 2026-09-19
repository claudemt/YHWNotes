from pathlib import Path
import sys, math
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[5]; sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair
with figure_style():
    n=np.arange(0,16); fig,ax=plt.subplots()
    for S in [0.5,2.0,5.0]:
        P=np.array([math.exp(-S)*S**int(k)/math.factorial(int(k)) for k in n]); ax.plot(n,P,marker='o',label=rf'$S_{{\rm HR}}={S:g}$')
    ax.set_xlabel(r'Final vibrational quantum number $n$'); ax.set_ylabel('Franck--Condon factor'); ax.set_xticks(np.arange(0,16,2))
    add_legend(ax,loc='upper right',frameon=False); polish_axes(ax,grid=True); fig.tight_layout(); save_pdf_png_pair(fig,'franck_condon',Path(__file__).resolve().parents[1]/'generated')
