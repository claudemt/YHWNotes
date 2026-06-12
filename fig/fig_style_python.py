from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

try:
    import scienceplots  # noqa: F401
    _STYLE = ["science", "nature", "no-latex"]
except Exception:
    _STYLE = ["default"]

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "build"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 24,
    "axes.labelsize": 30,
    "axes.titlesize": 30,
    "xtick.labelsize": 26,
    "ytick.labelsize": 26,
    "legend.fontsize": 24,
    "legend.title_fontsize": 24,
    "axes.unicode_minus": False,
    "lines.linewidth": 2.8,
    "figure.dpi": 180,
    "savefig.dpi": 500,
    "savefig.bbox": "tight",
})

FONT_OVERRIDES = {
    "font.family": "DejaVu Serif",
    "font.size": 24,
    "axes.labelsize": 30,
    "axes.titlesize": 30,
    "xtick.labelsize": 26,
    "ytick.labelsize": 26,
    "legend.fontsize": 24,
    "legend.title_fontsize": 24,
    "axes.unicode_minus": False,
    "lines.linewidth": 2.8,
    "figure.dpi": 180,
    "savefig.dpi": 500,
    "savefig.bbox": "tight",
}

PLT_STYLE = _STYLE + [FONT_OVERRIDES]

COLORS = [
    "#C0392B",
    "#1A5276",
    "#2E7D32",
    "#8E44AD",
    "#D68910",
    "#566573",
    "#148F77",
    "#7D3C98",
]
LIGHT_BLUE = "#D9ECFF"
THREE_COLORS = COLORS[:3]
FOUR_COLORS = COLORS[:4]
LINE_STYLES = ["-", "--", "-.", ":"]


def use_style():
    return plt.style.context(PLT_STYLE)


@contextmanager
def figure_style():
    with use_style():
        yield


def style_axes(ax, *, grid=True, minor_ticks=True):
    if minor_ticks:
        ax.minorticks_on()
    ax.tick_params(which="both", direction="in", top=True, right=True, pad=8)
    if grid:
        ax.grid(True, alpha=0.22, linewidth=0.8)
    else:
        ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)


def polish_axes(ax, *, grid=False, minor_ticks=True):
    style_axes(ax, grid=grid, minor_ticks=minor_ticks)


def polish_polar_axes(ax, *, radial_grid=True, radial_labels=True, theta_offset=0.0):
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    if theta_offset:
        ax.set_theta_offset(theta_offset)
    ax.spines["polar"].set_linewidth(1.5)
    ax.spines["polar"].set_color("0.18")
    ax.grid(radial_grid, alpha=0.24, linewidth=0.9)
    ax.set_rlabel_position(22.5)
    if not radial_labels:
        ax.set_yticklabels([])
    else:
        ticks = ax.get_yticks()
        labels = [label.get_text() for label in ax.get_yticklabels()]
        if len(labels) > 2:
            ax.set_yticks(ticks)
            ax.set_yticklabels([""] * (len(labels) - 2) + labels[-2:])
    ax.set_thetagrids(
        np.arange(0, 360, 90),
        labels=[
            r"$0$",
            r"$\pi/2$",
            r"$\pi$",
            r"$3\pi/2$",
        ],
    )
    ax.tick_params(axis="x", pad=20)
    ax.tick_params(axis="y", pad=8)


def add_legend(ax, *, outside=True, **kwargs):
    kw = dict(frameon=True, framealpha=0.94)
    if outside:
        kw.setdefault("loc", "center left")
        kw.setdefault("bbox_to_anchor", (1.02, 0.5))
    kw.update(kwargs)
    return ax.legend(**kw)


def _is_zero(value):
    return abs(float(value)) <= 1.0e-10


def _hide_lower_left_duplicate_zero(fig):
    fig.canvas.draw()
    for ax in fig.axes:
        if getattr(ax, "name", "") == "polar":
            continue
        x_labels = {
            round(float(tick.get_loc()), 12): tick.label1.get_text()
            for tick in ax.xaxis.get_major_ticks()
        }
        y_labels = {
            round(float(tick.get_loc()), 12): tick.label1.get_text()
            for tick in ax.yaxis.get_major_ticks()
        }
        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda value, pos, labels=x_labels: "0" if _is_zero(value) else labels.get(round(float(value), 12), f"{value:g}"))
        )
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda value, pos, labels=y_labels: "0" if _is_zero(value) else labels.get(round(float(value), 12), f"{value:g}"))
        )
    fig.canvas.draw()
    for ax in fig.axes:
        if getattr(ax, "name", "") == "polar":
            continue
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        if not (_is_zero(xlim[0]) and _is_zero(ylim[0])):
            continue
        x_has_zero = any(_is_zero(tick) for tick in ax.get_xticks())
        y_has_zero = any(_is_zero(tick) for tick in ax.get_yticks())
        if not (x_has_zero and y_has_zero):
            continue
        for tick in ax.yaxis.get_major_ticks():
            if _is_zero(tick.get_loc()):
                tick.label1.set_visible(False)
                tick.label2.set_visible(False)


def save_fig(fig, filename):
    path = OUTPUT_DIR / filename
    _hide_lower_left_duplicate_zero(fig)
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path


def save_figure(fig, filename, *, dpi=None, close=True):
    path = OUTPUT_DIR / filename
    kwargs = {"facecolor": "white"}
    if dpi is not None:
        kwargs["dpi"] = dpi
    _hide_lower_left_duplicate_zero(fig)
    fig.savefig(path, **kwargs)
    if close:
        plt.close(fig)
    return path
