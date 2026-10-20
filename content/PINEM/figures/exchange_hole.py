from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import pubfig, clean, safe_panel, finish_pub

fig, axs = plt.subplots(2,3,figsize=(10.6,7.9),constrained_layout=True)
axs=axs.ravel()
x=np.linspace(-4,4,260); X,Y=np.meshgrid(x,x); ds=[.35,.8,1.6,2.8,4.0,6.0]
for j,d in enumerate(ds):
 aX=np.exp(-(X-d/2)**2/2); bX=np.exp(-(X+d/2)**2/2); aY=np.exp(-(Y-d/2)**2/2); bY=np.exp(-(Y+d/2)**2/2); P=(aX*bY-bX*aY)**2; P/=P.max()+1e-12; im=axs[j].imshow(P,origin='lower',extent=[-4,4,-4,4],vmin=0,vmax=1); axs[j].plot(x,x,'w--',lw=.8); axs[j].set_title(f'separation $d={d}$'); axs[j].set_xlabel('$x_1$'); axs[j].set_ylabel('$x_2$')
fig.colorbar(im,ax=axs.ravel().tolist(),shrink=.8,label='pair density')
for i,ax in enumerate(axs):
    clean(ax); safe_panel(ax,chr(97+i))
finish_pub(fig,Path(__file__).with_suffix('.pdf'))
