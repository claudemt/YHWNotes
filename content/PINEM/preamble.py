"""Unified publication plotting style for every textbook figure.

Latin Modern typography, mathematical labels, axes and export are defined here.
All figure scripts must reuse these helpers; model code stays in figures/common.py.
"""
import sys, types
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Use the system Latin Modern installation when available.
try:
    from matplotlib import font_manager
    for _fp in [
        '/usr/share/texmf/fonts/opentype/public/lm/lmroman10-regular.otf',
        '/usr/share/texmf/fonts/opentype/public/lm/lmroman10-bold.otf',
        '/usr/share/texmf/fonts/opentype/public/lm/lmroman10-italic.otf',
        '/usr/share/texmf/fonts/opentype/public/lm-math/latinmodern-math.otf',
    ]:
        if Path(_fp).exists():
            font_manager.fontManager.addfont(_fp)
except Exception:
    pass

mpl.rcParams.update({
    'figure.dpi': 160,
    'savefig.dpi': 220,
    'font.family': 'serif',
    'font.serif': ['Latin Modern Roman', 'Computer Modern Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',
    'mathtext.rm': 'Latin Modern Math',
    'mathtext.it': 'Latin Modern Math:italic',
    'mathtext.bf': 'Latin Modern Math:bold',
    'mathtext.cal': 'Latin Modern Math',
    'mathtext.sf': 'Latin Modern Math',
    'mathtext.tt': 'Latin Modern Math',
    'mathtext.fallback': None,
    'font.size': 11.0,
    'axes.labelsize': 11.0,
    'axes.titlesize': 12.0,
    'xtick.labelsize': 9.8,
    'ytick.labelsize': 9.8,
    'legend.fontsize': 9.8,
    'axes.linewidth': 0.75,
    'xtick.major.width': 0.65,
    'ytick.major.width': 0.65,
    'lines.linewidth': 1.35,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

COLORS = {'blue':'#2677a8', 'orange':'#c77641', 'green':'#258676', 'purple':'#8463ac'}

def paper_figure(width=9.8, height=6.85):
    return plt.figure(figsize=(width, height), constrained_layout=False)

def panel(ax, label, x=-0.12, y=1.05):
    fn=getattr(ax,'text2D',ax.text)
    fn(x,y,label,transform=ax.transAxes,ha='left',va='bottom',fontweight='bold',fontsize=11.0,
       bbox=dict(boxstyle='square,pad=0.08',fc='white',ec='none',alpha=0.96),zorder=20,clip_on=False)

def clean(ax):
    ax.tick_params(direction='out',length=3,pad=2)
    for s in ax.spines.values(): s.set_linewidth(0.75)

STANDARD_FIGSIZE=(9.8, 6.85)  # 3:2 landscape, shared by every retained figure

import re
# Figure-wide mathematical typography policy (used at export by save()).
# Math symbols/variables are MathText; prose and physical units remain upright.
_MATH_EXACT = {
    'kx': r'$k_x$', 'ky': r'$k_y$', 'kz': r'$k_z$',
    'g1': r'$g_1$', 'g2': r'$g_2$',
    'phi2': r'$\phi_2$', 'phi3': r'$\phi_3$',
    'sigma_n': r'$\sigma_n$', 'Omega': r'$\Omega$',
    'Re E': r'$\operatorname{Re} E$',
    'Im E': r'$\operatorname{Im} E$',
    'Re $E/J$': r'$\operatorname{Re}(E/J)$',
    'Tr g': r'$\operatorname{Tr} g$',
    '|Omega| / Tr g': r'$|\Omega|/\operatorname{Tr} g$',
    '|beta|': r'$|\beta|$', '|beta_hat|': r'$|\hat{\beta}|$',
    '<n>': r'$\langle n\rangle$', 'P(+1)': r'$P(+1)$',
    'P(n,n)': r'$P(n,n)$', 'P(n|Nph)': r'$P(n\mid N_{\mathrm{ph}})$',
    'conditional g2': r'conditional $g^{(2)}$',
    'phase / pi': r'phase / $\pi$',
    r'd\chi/dT':r'$\mathrm{d}\chi/\mathrm{d}T$',
}
_TOKEN_PATTERN = re.compile(r'(?<![A-Za-z0-9_\\])(?:sigma_n|phi2|phi3|gamma|alpha|theta|omega|beta|eta|rho|k[xyz]|g[123]|[NnmgGTCFPEJKSVRLQxyztp])(?!(?:[A-Za-z0-9_]))')
_GREEK = {'gamma':r'\gamma','alpha':r'\alpha','theta':r'\theta',
          'omega':r'\omega','beta':r'\beta','eta':r'\eta','rho':r'\rho',
          'sigma_n':r'\sigma_n','phi2':r'\phi_2','phi3':r'\phi_3'}


def _upright_differentials(math):
    """Roman d only for differentials, preserving any variable named d."""
    math=re.sub(r'(?<![A-Za-z])d(?=\\(?:chi|theta|omega|phi|alpha|beta|tau|xi|rho)|[TtxyzqspEnm]|\s*\^\s*[12])',lambda m:r'\mathrm{d}',math)
    return math.replace(r'\dd',r'\mathrm{d}')


def normalize_math_label(label):
    """Convert unformatted physical symbols while leaving explanatory text as text."""
    if not isinstance(label,str) or not label or label.startswith('_'):
        return label
    if label in _MATH_EXACT:
        return _MATH_EXACT[label]
    spans=re.split(r'(\$[^$]*\$)',label)
    out=[]
    for fragment in spans:
        if fragment.startswith('$') and fragment.endswith('$'):
            out.append('$'+_upright_differentials(fragment[1:-1])+'$')
            continue
        fragment=re.sub(r'(?<![A-Za-z])\b(Re|Im|Tr)\s+(?=[A-Z])',
                        lambda m:'$'+{'Re':r'\operatorname{Re}','Im':r'\operatorname{Im}','Tr':r'\operatorname{Tr}'}[m.group(1)]+'$ ',fragment)
        # Input strings containing bare TeX Greek commands are invalid otherwise.
        def bare_greek(m):
            sub=m.group(2)
            return '$'+chr(92)+m.group(1)+(('_'+('{' + sub + '}' if len(sub)>1 else sub)) if sub else '')+'$'
        fragment=re.sub(r'\\(sigma|theta|phi|gamma|omega|eta|alpha|beta)(?:_\{?([0-9a-zA-Z]+)\}?)?',bare_greek,fragment)
        def token(m):
            key=m.group(0)
            rep=_GREEK.get(key)
            if rep is None and key in ('kx','ky','kz'):rep='k_'+key[-1]
            if rep is None and re.fullmatch('g[123]',key):rep='g_'+key[-1]
            if rep is None:rep=key
            return '$'+rep+'$'
        out.append(_TOKEN_PATTERN.sub(token,fragment))
    return ''.join(out)

def _normalize_figure(fig):
    """Normalize *typography*, never geometry or scientific data.

    Retain authored aspect ratios, panel order and spacing. Only text styling
    is normalized; scientific data and plotted geometry are unchanged.
    """
    from matplotlib.text import Text
    for obj in fig.findobj(match=Text):
        try:
            raw=obj.get_text()
            obj.set_text(normalize_math_label(raw))
            obj.set_fontfamily('Latin Modern Roman')
        except Exception:
            pass
    for ax in fig.axes:
        try:
            ax.xaxis.label.set_fontsize(9.3)
            ax.yaxis.label.set_fontsize(9.3)
            for tick in ax.get_xticklabels()+ax.get_yticklabels():
                tick.set_fontsize(8.6)
            leg=ax.get_legend()
            if leg is not None:
                for v in leg.get_texts(): v.set_fontsize(8.7)
                if leg.get_title(): leg.get_title().set_fontsize(8.7)
        except Exception:
            pass



# Six-panel figures are placed as three rows of TWO panels at their true
# A4 print width. The old fixed three-column grid scaled every 10 pt label
# to roughly 6 pt and placed colorbars inside neighbouring axis gutters.
# The six panel meanings and order are preserved: no scientific arrays are
# altered by the layout operation.
FIGURE_WIDTH_IN = 6.72
FIGURE_HEIGHT_IN = 8.34
_SLOTS = [(0.125,0.713,0.325,0.213), (0.612,0.713,0.325,0.213),
          (0.125,0.407,0.325,0.213), (0.612,0.407,0.325,0.213),
          (0.125,0.101,0.325,0.213), (0.612,0.101,0.325,0.213)]

def _is_colorbar_axis(ax):
    return ax.get_label() == '<colorbar>' or getattr(ax, '_colorbar', None) is not None

def _line_occupancy(ax, leg, renderer):
    """Measure actual display-space line/annotation collisions for a candidate legend."""
    from matplotlib.transforms import Bbox
    bbox = leg.get_window_extent(renderer)
    if bbox.width <= 0 or bbox.height <= 0: return float('inf')
    score=0.0
    for line in ax.lines:
        xy=line.get_xydata()
        if len(xy)<2:continue
        xy=xy[np.all(np.isfinite(xy),axis=1)]
        if len(xy)<2:continue
        if len(xy)>1600:xy=xy[np.linspace(0,len(xy)-1,1600,dtype=int)]
        try: pixels=ax.transData.transform(xy)
        except Exception:continue
        inside=(pixels[:,0]>bbox.x0-2)&(pixels[:,0]<bbox.x1+2)&(pixels[:,1]>bbox.y0-2)&(pixels[:,1]<bbox.y1+2)
        score+=float(inside.sum())/len(xy)
    for artist in ax.texts:
        if not artist.get_visible() or artist.get_text().strip() in 'abcdef':continue
        try:
            txtbox=artist.get_window_extent(renderer)
            if txtbox.overlaps(bbox):score+=10
        except Exception:pass
    # A line plot legend placed over a background image generally erases data.
    if ax.images or ax.collections and any(hasattr(c,'get_array') and c.get_array() is not None for c in ax.collections):
        score+=0.25
    return score

def _position_legends(fig, primaries):
    # Anchor legends to one of four *inside* corners. This minimizes actual
    # curve/annotation overlap rather than trusting matplotlib 'best' heuristics.
    for ax in primaries:
        leg=ax.get_legend()
        if leg is None:continue
        try:
            leg.set_bbox_to_anchor(None)
            best=None
            for loc in ('upper left','upper right','lower left','lower right'):
                leg.set_loc(loc)
                fig.canvas.draw()
                score=_line_occupancy(ax,leg,fig.canvas.get_renderer())
                if best is None or score<best[0]:best=(score,loc)
            leg.set_loc(best[1])
            leg.set_frame_on(True)
            leg.get_frame().set_facecolor('white')
            leg.get_frame().set_edgecolor('none')
            leg.get_frame().set_alpha(.89)
            for txt in leg.get_texts():txt.set_fontsize(8.7)
        except Exception as err:
            print('LEGEND_LAYOUT_WARNING',err)

def canonical_six_panel_layout(fig):
    """Reflow data boxes and colorbars, retaining each mathematical plot unchanged."""
    allaxes=list(fig.axes)
    primary=[ax for ax in allaxes if not _is_colorbar_axis(ax)]
    bars=[ax for ax in allaxes if _is_colorbar_axis(ax)]
    if len(primary)!=6:
        # Other source figures, if any, use their authored layout.
        return fig
    old={a:a.get_position().bounds for a in allaxes}
    def label_index(ax):
        for item in ax.texts:
            s=item.get_text().strip().lower().strip('()')
            if s in 'abcdef' and len(s)==1:return 'abcdef'.index(s)
        return None
    indexed={label_index(ax):ax for ax in primary}
    if len(indexed)==6 and set(indexed)==set(range(6)):
        ordered=[indexed[j] for j in range(6)]
    else:
        ordered=sorted(primary,key=lambda a:(-round(old[a][1]+old[a][3]/2,1),old[a][0]))
    fig.set_size_inches(FIGURE_WIDTH_IN,FIGURE_HEIGHT_IN,forward=True)
    for j,ax in enumerate(ordered):
        slot=_SLOTS[j]
        try:ax.set_axes_locator(None)
        except Exception:pass
        ax.set_position(slot,which='both')
        # Matplotlib maintains separate left/center/right title artists.
        # Clearing only the centered title leaves legacy long left titles
        # overlapping adjacent panels after the new page-width reflow.
        for title_loc in ('left','center','right'):
            ax.set_title('',loc=title_loc)
        ax.tick_params(direction='out',labelsize=8.6,pad=2.6)
        ax.xaxis.label.set_fontsize(9.3)
        ax.yaxis.label.set_fontsize(9.3)
        # A single visible panel label; stored in an independent top gutter.
        for artist in list(ax.texts):
            tx=artist.get_text().strip()
            if tx.lower() in ('a','b','c','d','e','f','(a)','(b)','(c)','(d)','(e)','(f)'):
                artist.set_visible(False)
        fn=getattr(ax,'text2D',ax.text)
        fn(-.115,1.11,chr(97+j),transform=ax.transAxes,
           ha='left',va='bottom',fontsize=10.5,fontweight='bold',
           color='.15',clip_on=False,zorder=20)
    # For each colorbar use its Matplotlib mappable, not proximity alone.
    for cb in bars:
        original=old[cb]
        source=getattr(getattr(cb,'_colorbar',None),'mappable',None)
        target=getattr(source,'axes',None)
        if target not in ordered:
            target=min(ordered,key=lambda ax:
               abs((old[ax][0]+old[ax][2])-original[0]) +
               abs((old[ax][1]+old[ax][3]/2)-(original[1]+original[3]/2)))
        x,y,w,h=_SLOTS[ordered.index(target)]
        try:cb.set_axes_locator(None)
        except Exception:pass
        cb.set_position((x+w+.014,y,.015,h),which='both')
        cb.tick_params(labelsize=7.5,pad=1)
        cb.yaxis.label.set_text('')
        cb.yaxis.label.set_visible(False)
    _position_legends(fig,ordered)
    return fig

def save(fig,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    _normalize_figure(fig)
    canonical_six_panel_layout(fig)
    fig.savefig(path,facecolor='white',bbox_inches=None,pad_inches=.015)
    plt.close(fig)

# --- Shared figure helpers ---
def hero_figure(width=9.8, height=6.85):
    return plt.figure(figsize=(width, height), constrained_layout=False)

def hero_panel(ax, label, x=-0.115, y=1.13):
    # One unobtrusive panel marker system for all original figures.
    fn=getattr(ax,'text2D',ax.text)
    fn(x,max(float(y),1.13),label,transform=ax.transAxes,ha='left',va='bottom',
       fontweight='bold',fontsize=11.0,color='0.08',zorder=30,clip_on=False)

def hero_title(ax, title, subtitle=None):
    # Panel identity belongs to the (a)-(f) marker and physical axis labels.
    # All explanations are typeset in the LaTeX caption, at actual print size.
    return ax

def style_3d(ax, elev=28, azim=-52):
    ax.view_init(elev=elev,azim=azim)
    ax.grid(False)
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        try: axis.pane.set_facecolor((1,1,1,0)); axis.pane.set_edgecolor((0.86,0.86,0.86,1))
        except Exception: pass
    ax.tick_params(pad=0,labelsize=7.0)

# --- Collision-safe publication helpers ---
def pubfig(width=9.8, height=6.85, top=0.90, bottom=0.09, left=0.07, right=0.97):
    fig=plt.figure(figsize=(width,height),constrained_layout=False)
    fig.subplots_adjust(left=left,right=right,bottom=bottom,top=top)
    return fig

def safe_panel(ax,label,x=-0.115,y=1.13):
    fn=getattr(ax,'text2D',ax.text)
    fn(x,y,label,transform=ax.transAxes,ha='left',va='bottom',fontweight='bold',fontsize=11.0,
       color='0.08',zorder=100,clip_on=False)

def safe_title(ax,title,subtitle=None):
    # Suppress inconsistent floating panel headings; use one caption per figure.
    # Does not change axes, plotted data, line styling or panel markers.
    return ax

def safe_colorbar(fig,mappable,ax,label='',side='right',size='3.2%',pad=0.025):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    div=make_axes_locatable(ax)
    cax=div.append_axes(side,size=size,pad=pad)
    cb=fig.colorbar(mappable,cax=cax)
    if label: cb.set_label(label,labelpad=3)
    cb.ax.tick_params(labelsize=7.0,pad=1.5)
    return cb

def finish_pub(fig,path,suptitle=None):
    # The LaTeX figure caption carries the title and panel explanations.
    save(fig,path)



# --- Typography normalization for all active and embedded figure builders ---
# This layer changes presentation only. It does not alter data, equations, labels, or geometry.
def _norm_fs(value, role='body'):
    try:
        x=float(value)
    except Exception:
        return value
    if role == 'title':
        return 12.5 if x < 12.5 else min(x, 13.5)
    if role == 'panel':
        return 12.5
    if role == 'tick':
        return 10.5
    if role == 'legend':
        return 10.0
    # labels / annotations / general text
    if x < 9.0: return 10.0
    if x < 10.5: return 11.0
    if x < 12.0: return 12.0
    return min(x, 13.5)

def _install_typography_guard():
    from matplotlib.axes import Axes
    from matplotlib.legend import Legend
    if getattr(Axes, '_pinem_typography_guard', False):
        return
    Axes._pinem_typography_guard=True

    _text=Axes.text
    def text_guard(self,*args,**kwargs):
        if 'fontsize' in kwargs: kwargs['fontsize']=_norm_fs(kwargs['fontsize'],'body')
        if 'size' in kwargs: kwargs['size']=_norm_fs(kwargs['size'],'body')
        return _text(self,*args,**kwargs)
    Axes.text=text_guard

    _title=Axes.set_title
    def title_guard(self,label,*args,**kwargs):
        if 'fontsize' in kwargs: kwargs['fontsize']=_norm_fs(kwargs['fontsize'],'title')
        elif 'size' in kwargs: kwargs['size']=_norm_fs(kwargs['size'],'title')
        return _title(self,label,*args,**kwargs)
    Axes.set_title=title_guard

    _xlabel=Axes.set_xlabel; _ylabel=Axes.set_ylabel
    def xlabel_guard(self,xlabel,*args,**kwargs):
        if 'fontsize' in kwargs: kwargs['fontsize']=_norm_fs(kwargs['fontsize'],'body')
        return _xlabel(self,xlabel,*args,**kwargs)
    def ylabel_guard(self,ylabel,*args,**kwargs):
        if 'fontsize' in kwargs: kwargs['fontsize']=_norm_fs(kwargs['fontsize'],'body')
        return _ylabel(self,ylabel,*args,**kwargs)
    Axes.set_xlabel=xlabel_guard; Axes.set_ylabel=ylabel_guard

    _tick=Axes.tick_params
    def tick_guard(self,*args,**kwargs):
        if 'labelsize' in kwargs: kwargs['labelsize']=_norm_fs(kwargs['labelsize'],'tick')
        return _tick(self,*args,**kwargs)
    Axes.tick_params=tick_guard

    _legend=Axes.legend
    def legend_guard(self,*args,**kwargs):
        if 'fontsize' in kwargs: kwargs['fontsize']=_norm_fs(kwargs['fontsize'],'legend')
        if 'prop' not in kwargs and 'fontsize' not in kwargs:
            kwargs['fontsize']=10.0
        return _legend(self,*args,**kwargs)
    Axes.legend=legend_guard

# Local scientific data and axes geometry remain untouched by typography normalization.

# Backward-compatible virtual module used by legacy figure source.


