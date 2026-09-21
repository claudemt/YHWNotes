import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt
import scienceplots
from pathlib import Path

# =========================================================
# SciencePlots style
# =========================================================
plt.style.use(["science", "grid", "ieee"])
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "legend.frameon": True,
    "lines.linewidth": 1.8,
    "figure.dpi": 180,
    "savefig.dpi": 300,
})

# =========================================================
# User configuration
# =========================================================
# Modify s values here:
s_list = [1.2, 1.5, 2.0, 3.0]

# Temperature range in units of T/T_s
t_min = 0.0
t_max = 1.5
n_t = 320

# Only mu uses symlog; all others are linear
use_symlog_mu = True

# Small positive floor to avoid evaluating exactly at t=0
t_eval_floor = 1e-6

# Automatic plot-range tuning
# More aggressive than before so singular spikes are suppressed better
auto_range_quantiles = {
    "mu": (0.03, 0.97),
    "cv": (0.03, 0.97),
    "p": (0.02, 0.98),
    "gamma": (0.05, 0.95),
}

# Extra padding around the visible envelope
auto_range_padding = {
    "mu": 0.04,
    "cv": 0.05,
    "p": 0.04,
    "gamma": 0.05,
}

# Manual override for y-limits if desired
manual_ylim = {
    "mu": None,
    "cv": None,
    "p": None,
    "gamma": None,
}

# Manual override for x-limits if desired
manual_xlim = {
    "mu": None,
    "cv": None,
    "p": None,
    "gamma": None,
}

# Small padding on x-range after auto-detection
auto_x_padding_frac = 0.01

# Output directory: same folder as this script
OUTDIR = Path(__file__).resolve().parent

# Numerical precision
mp.mp.dps = 30

# =========================================================
# Definitions
# =========================================================
def g(nu, eta):
    return float(mp.re(mp.polylog(nu, mp.e**eta)))

def f(nu, eta):
    return float(-mp.re(mp.polylog(nu, -mp.e**eta)))

def tc_over_ts(s):
    return float(mp.zeta(s) ** (-1 / s))

ylabel_map = {
    "mu": r"$\mu/(kT_s)$",
    "cv": r"$C_V/(Nk)$",
    "p": r"$P/(n k T_s)$",
    "gamma": r"$C_P/C_V$",
}

t_grid = np.linspace(t_min, t_max, n_t)
bose_data = {}
fermi_data = {}

# =========================================================
# Utility functions for robust auto-range
# =========================================================
def finite_values(arr):
    arr = np.asarray(arr, dtype=float)
    return arr[np.isfinite(arr)]

def robust_window(v, qlo, qhi):
    """
    Robust window for one curve:
    use quantiles to ignore singular spikes / extreme tails.
    """
    v = finite_values(v)
    if v.size == 0:
        return None

    if v.size < 8:
        return float(v.min()), float(v.max())

    lo, hi = np.quantile(v, [qlo, qhi])

    if (not np.isfinite(lo)) or (not np.isfinite(hi)) or (hi <= lo):
        lo, hi = float(v.min()), float(v.max())

    return float(lo), float(hi)

def automatic_ylim(curves, quantity):
    """
    Determine y-range from the visible envelope of the curves,
    while suppressing singular spikes.
    """
    if manual_ylim[quantity] is not None:
        return manual_ylim[quantity]

    qlo, qhi = auto_range_quantiles[quantity]
    pad = auto_range_padding[quantity]

    clipped_vals = []

    for y in curves:
        v = finite_values(y)
        if v.size == 0:
            continue

        win = robust_window(v, qlo, qhi)
        if win is None:
            continue

        lo_i, hi_i = win
        clipped_vals.append(np.clip(v, lo_i, hi_i))

    if not clipped_vals:
        return None

    vals = np.concatenate(clipped_vals)
    lo = float(np.min(vals))
    hi = float(np.max(vals))

    if (not np.isfinite(lo)) or (not np.isfinite(hi)):
        return None

    if hi <= lo:
        c = 0.5 * (lo + hi)
        d = max(abs(c), 1.0) * 0.1
        return (c - d, c + d)

    span = hi - lo
    y0 = lo - pad * span
    y1 = hi + pad * span

    # Snap to zero only if zero is naturally close
    if lo >= 0.0 and y0 < 0.0 and abs(y0) < 0.15 * span:
        y0 = 0.0
    if hi <= 0.0 and y1 > 0.0 and abs(y1) < 0.15 * span:
        y1 = 0.0

    # Important fix:
    # for mu + symlog, do NOT force symmetry around zero
    if quantity == "mu" and use_symlog_mu and (y0 < 0 < y1):
        eps = max(1e-8, 1e-6 * max(abs(y0), abs(y1), 1.0))
        if abs(y0) < eps:
            y0 = -eps
        if abs(y1) < eps:
            y1 = eps

    if y1 <= y0:
        c = 0.5 * (lo + hi)
        d = max(span, 1.0) * 0.5
        y0, y1 = c - d, c + d

    return (y0, y1)

def automatic_xlim(x, curves, quantity):
    """
    Determine x-range from the domain where curves are actually defined/finite.
    This removes blank regions such as Bose gamma below Tc.
    """
    if manual_xlim[quantity] is not None:
        return manual_xlim[quantity]

    x = np.asarray(x, dtype=float)
    lefts, rights = [], []

    for y in curves:
        y = np.asarray(y, dtype=float)
        mask = np.isfinite(y)
        if np.any(mask):
            xv = x[mask]
            lefts.append(float(xv[0]))
            rights.append(float(xv[-1]))

    if not lefts:
        return (float(x[0]), float(x[-1]))

    x0 = min(lefts)
    x1 = max(rights)

    if x1 <= x0:
        return (float(x[0]), float(x[-1]))

    span = x1 - x0
    pad = auto_x_padding_frac * span
    x0 = max(float(x[0]), x0 - pad)
    x1 = min(float(x[-1]), x1 + pad)

    return (x0, x1)

def clip_for_display(y, ylim):
    """
    Clip only for display: huge singular tails are truncated visually,
    but do not dominate the frame.
    """
    y = np.asarray(y, dtype=float).copy()
    if ylim is None:
        return y

    m = np.isfinite(y)
    y[m] = np.clip(y[m], ylim[0], ylim[1])
    return y

def setup_axis(ax, quantity, ylim, xlim):
    ax.set_xlabel(r"$T/T_s$")
    ax.set_ylabel(ylabel_map[quantity])

    if quantity == "mu" and use_symlog_mu:
        ax.set_yscale("symlog", linthresh=1e-2)

    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)

    ax.minorticks_on()
    ax.margins(x=0.0, y=0.0)

# =========================================================
# Build data using eta = ln z interpolation
# =========================================================
for s in s_list:
    # ----------------- Bose -----------------
    tc = tc_over_ts(s)
    eta_b = np.linspace(-12.0, -1e-5, 700)

    gb_s   = np.array([g(s,     e) for e in eta_b])
    gb_sm1 = np.array([g(s - 1, e) for e in eta_b])
    gb_sp1 = np.array([g(s + 1, e) for e in eta_b])

    t_b = gb_s ** (-1 / s)
    idx = np.argsort(t_b)

    t_b    = t_b[idx]
    eta_b  = eta_b[idx]
    gb_s   = gb_s[idx]
    gb_sm1 = gb_sm1[idx]
    gb_sp1 = gb_sp1[idx]

    mu_arr, cv_arr, p_arr, gamma_arr = [], [], [], []

    for t in t_grid:
        te = max(float(t), t_eval_floor)

        if te <= tc:
            zeta_sp1 = float(mp.zeta(s + 1))
            mu_arr.append(0.0)
            cv_arr.append(s * (s + 1) * (te ** s) * zeta_sp1)
            p_arr.append((te ** (s + 1)) * zeta_sp1)
            gamma_arr.append(np.nan)
        else:
            eta  = np.interp(te, t_b, eta_b)
            gs   = np.interp(te, t_b, gb_s)
            gsm1 = np.interp(te, t_b, gb_sm1)
            gsp1 = np.interp(te, t_b, gb_sp1)

            mu_arr.append(te * eta)
            cv_arr.append(s * ((s + 1) * gsp1 / gs - s * gs / gsm1))
            p_arr.append(te * gsp1 / gs)
            gamma_arr.append(((s + 1) / s) * gsp1 * gsm1 / (gs ** 2))

    bose_data[s] = {
        "t": t_grid.copy(),
        "mu": np.array(mu_arr),
        "cv": np.array(cv_arr),
        "p": np.array(p_arr),
        "gamma": np.array(gamma_arr),
        "tc": tc,
    }

    # ----------------- Fermi -----------------
    eta_f = np.linspace(-12.0, 30.0, 900)

    ff_s   = np.array([f(s,     e) for e in eta_f])
    ff_sm1 = np.array([f(s - 1, e) for e in eta_f])
    ff_sp1 = np.array([f(s + 1, e) for e in eta_f])

    t_f = ff_s ** (-1 / s)
    idx = np.argsort(t_f)

    t_f    = t_f[idx]
    eta_f  = eta_f[idx]
    ff_s   = ff_s[idx]
    ff_sm1 = ff_sm1[idx]
    ff_sp1 = ff_sp1[idx]

    mu_arr, cv_arr, p_arr, gamma_arr = [], [], [], []

    for t in t_grid:
        te = max(float(t), t_eval_floor)
        tt = np.clip(te, t_f.min(), t_f.max())

        eta  = np.interp(tt, t_f, eta_f)
        fs   = np.interp(tt, t_f, ff_s)
        fsm1 = np.interp(tt, t_f, ff_sm1)
        fsp1 = np.interp(tt, t_f, ff_sp1)

        mu_arr.append(tt * eta)
        cv_arr.append(s * ((s + 1) * fsp1 / fs - s * fs / fsm1))
        p_arr.append(tt * fsp1 / fs)
        gamma_arr.append(((s + 1) / s) * fsp1 * fsm1 / (fs ** 2))

    fermi_data[s] = {
        "t": t_grid.copy(),
        "mu": np.array(mu_arr),
        "cv": np.array(cv_arr),
        "p": np.array(p_arr),
        "gamma": np.array(gamma_arr),
    }

# =========================================================
# Plot helpers
# =========================================================
def make_two_panel(quantity, filename):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2), constrained_layout=True)
    ax_b, ax_f = axes

    bose_curves = [bose_data[s][quantity] for s in s_list]
    fermi_curves = [fermi_data[s][quantity] for s in s_list]

    x_b = bose_data[s_list[0]]["t"]
    x_f = fermi_data[s_list[0]]["t"]

    ylim_b = automatic_ylim(bose_curves, quantity)
    ylim_f = automatic_ylim(fermi_curves, quantity)

    xlim_b = automatic_xlim(x_b, bose_curves, quantity)
    xlim_f = automatic_xlim(x_f, fermi_curves, quantity)

    for s in s_list:
        yb = clip_for_display(bose_data[s][quantity], ylim_b)
        yf = clip_for_display(fermi_data[s][quantity], ylim_f)

        ax_b.plot(
            bose_data[s]["t"], yb,
            linestyle="-", label=fr"$s={s:g}$"
        )
        ax_f.plot(
            fermi_data[s]["t"], yf,
            linestyle="-", label=fr"$s={s:g}$"
        )

    ax_b.set_title(r"\textbf{Bose gas}")
    setup_axis(ax_b, quantity, ylim_b, xlim_b)
    ax_b.legend(loc="best")

    ax_f.set_title(r"\textbf{Fermi gas}")
    setup_axis(ax_f, quantity, ylim_f, xlim_f)
    ax_f.legend(loc="best")

    path = OUTDIR / filename
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

# =========================================================
# Generate single two-panel PNGs
# =========================================================
make_two_panel("mu",    "mu_T.png")
make_two_panel("cv",    "Cv_T.png")
make_two_panel("p",     "P_T.png")
make_two_panel("gamma", "gamma_T.png")

# =========================================================
# Generate all-panels summary figure
# =========================================================
fig, axes = plt.subplots(2, 4, figsize=(16, 7), constrained_layout=True)
quantities = ["mu", "cv", "p", "gamma"]

for col, q in enumerate(quantities):
    axb = axes[0, col]
    axf = axes[1, col]

    bose_curves = [bose_data[s][q] for s in s_list]
    fermi_curves = [fermi_data[s][q] for s in s_list]

    ylim_b = automatic_ylim(bose_curves, q)
    ylim_f = automatic_ylim(fermi_curves, q)

    x_b = bose_data[s_list[0]]["t"]
    x_f = fermi_data[s_list[0]]["t"]

    xlim_b = automatic_xlim(x_b, bose_curves, q)
    xlim_f = automatic_xlim(x_f, fermi_curves, q)

    for s in s_list:
        yb = clip_for_display(bose_data[s][q], ylim_b)
        yf = clip_for_display(fermi_data[s][q], ylim_f)

        axb.plot(
            bose_data[s]["t"], yb,
            linestyle="-", label=fr"$s={s:g}$"
        )
        axf.plot(
            fermi_data[s]["t"], yf,
            linestyle="-", label=fr"$s={s:g}$"
        )

    axb.set_title(r"\textbf{Bose}: " + q)
    axf.set_title(r"\textbf{Fermi}: " + q)

    setup_axis(axb, q, ylim_b, xlim_b)
    setup_axis(axf, q, ylim_f, xlim_f)

    axb.legend(loc="best")
    axf.legend(loc="best")

fig.savefig(OUTDIR / "all_panels.png", bbox_inches="tight")
plt.close(fig)
