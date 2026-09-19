"""Unified matplotlib style for the multi-book physics notes repository.

This mirrors the public LaTeX ``preamble.tex`` visual grammar: a serif body
font (Latin Modern Roman, matching the LaTeX engine), medium-large print
sizes, consistent line widths, outward ticks on a full frame, and a faint
dashed light-grey grid.  Figures are saved as a PDF/PNG pair; the PDF is the
vector figure actually embedded by XeLaTeX, the PNG is a raster QA preview.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams

# A colourblind-friendly qualitative palette (tab10 order kept so existing
# scripts that index COLORS[0..5] keep their current colours).
COLORS = [
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
    "#7f7f7f",  # grey
]

LINE_STYLES = ["-", "--", "-.", ":"]

_CORNER_LOC = {
    "upper left": "upper left",
    "upper right": "upper right",
    "lower left": "lower left",
    "lower right": "lower right",
    "center left": "center left",
    "center right": "center right",
}

# rcParams keys touched by figure_style(); saved/restored on exit.
_STYLE_KEYS = (
    "font.family", "font.serif", "font.size",
    "axes.titlesize", "axes.labelsize", "axes.linewidth",
    "axes.grid", "axes.axisbelow",
    "xtick.labelsize", "ytick.labelsize",
    "xtick.direction", "ytick.direction",
    "xtick.top", "ytick.right",
    "xtick.major.width", "ytick.major.width",
    "xtick.minor.visible", "ytick.minor.visible",
    "grid.color", "grid.linestyle", "grid.linewidth", "grid.alpha",
    "legend.fontsize", "legend.title_fontsize",
    "lines.linewidth", "lines.markersize",
    "mathtext.fontset", "mathtext.rm", "mathtext.it", "mathtext.bf",
    "savefig.dpi", "figure.dpi",
    "figure.facecolor", "axes.facecolor",
)


@contextmanager
def figure_style():
    """Context manager applying the shared publication style."""
    saved = {k: rcParams[k] for k in _STYLE_KEYS if k in rcParams}
    try:
        rcParams.update({
            # Font: serif matching the LaTeX body (Latin Modern Roman first).
            "font.family": "serif",
            "font.serif": ["Latin Modern Roman", "LM Roman 10",
                           "DejaVu Serif", "CMU Serif", "Times New Roman"],
            "font.size": 11.0,
            # Text sizes scaled so in-figure labels read at print size.
            "axes.titlesize": 16.0,
            "axes.labelsize": 13.0,
            "axes.linewidth": 1.0,
            "xtick.labelsize": 12.0,
            "ytick.labelsize": 12.0,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            # Outward ticks on a full four-sided frame; no minor ticks.
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.minor.visible": False,
            "ytick.minor.visible": False,
            # Faint dashed light-grey grid, drawn under the data.
            "axes.grid": False,
            "axes.axisbelow": True,
            "grid.color": "0.85",
            "grid.linestyle": "--",
            "grid.linewidth": 0.7,
            "grid.alpha": 1.0,
            # Lines / legend.
            "legend.fontsize": 11.0,
            "legend.title_fontsize": 11.0,
            "lines.linewidth": 1.6,
            "lines.markersize": 5.5,
            # Computer-Modern mathtext so in-figure math matches LaTeX.
            "mathtext.fontset": "cm",
            "mathtext.rm": "Latin Modern Roman",
            "mathtext.it": "Latin Modern Math:italic",
            "mathtext.bf": "Latin Modern Math:bold",
            # Save targets.
            "savefig.dpi": 200,
            "figure.dpi": 110,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        })
        yield
    finally:
        rcParams.update(saved)
        plt.close("all")


def polish_axes(ax, grid: bool = True, minor_ticks: bool = False) -> None:
    """Apply the shared spine/tick/grid polish to one Axes (or array).

    Keeps all four spines visible (full frame), outward major ticks, and the
    faint dashed grid under the data lines.  Minor ticks are off by default
    to match the historical figures.
    """
    for a in _iter_axes(ax):
        # Full frame: all four spines black, uniform weight.
        for side in ("top", "right", "bottom", "left"):
            a.spines[side].set_visible(True)
            a.spines[side].set_linewidth(1.0)
            a.spines[side].set_color("black")
        # Outward major ticks on all four sides; no minor ticks.
        a.tick_params(axis="both", which="major", direction="out",
                      top=True, right=True, length=4.0, width=1.0)
        a.tick_params(axis="both", which="minor", bottom=False, top=False,
                      left=False, right=False)
        if minor_ticks:
            a.minorticks_on()
            a.tick_params(axis="both", which="minor", direction="out",
                          length=2.0, width=0.8)
        else:
            try:
                a.minorticks_off()
            except Exception:
                pass
        if grid:
            a.grid(True, which="major", linestyle="--", linewidth=0.7,
                   color="0.85")
            a.set_axisbelow(True)
        else:
            a.grid(False)


def add_legend(ax, loc: Optional[str] = None, corner: Optional[str] = None,
               frameon: bool = True, ncol: int = 1, fontsize=None,
               framealpha: float = 0.95, edgecolor: str = "0.80",
               **kwargs):
    """Place the legend inside the axes in a chosen empty corner.

    Always drawn in-axes with a near-opaque white frame and a thin light-grey
    edge.  Callers should pass a corner that is actually empty for their
    data; ``"best"`` is only a fallback.
    """
    if corner is not None and loc is None:
        loc = _CORNER_LOC.get(corner, "best")
    if loc is None:
        loc = "best"
    leg = ax.legend(loc=loc, frameon=frameon, ncol=ncol, fontsize=fontsize,
                    framealpha=framealpha, edgecolor=edgecolor,
                    fancybox=True, borderpad=0.55, labelspacing=0.4,
                    **kwargs)
    if frameon and leg is not None:
        leg.get_frame().set_linewidth(0.9)
    return leg


def save_pdf_png_pair(fig, stem: str, output_dir) -> None:
    """Save ``<stem>.pdf`` and ``<stem>.png`` into ``output_dir``."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{stem}.pdf")
    fig.savefig(out / f"{stem}.png", dpi=200)


def _iter_axes(ax) -> Iterable:
    try:
        import numpy as np
        for a in np.atleast_1d(ax).ravel():
            yield a
    except Exception:
        yield ax
