from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, trapezoid
from scipy.linalg import eigh_tridiagonal

import sys, pathlib
_repo_root = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(_repo_root))
from preamble import COLORS, figure_style, polish_axes, save_figure, Line2D, add_dual_legend

Q = 0.2
X_MAX = 4.0 * np.pi
N_POINTS = 5001
RTOL = 2.0e-12
ATOL = 2.0e-14
BASIS_SIZE = 48


def _characteristic_value(order: int, family: str, q_value: float) -> float:
    k = np.arange(BASIS_SIZE, dtype=float)
    q_value = float(q_value)
    mode_index = order // 2

    if family == "ce" and order % 2 == 0:
        diagonal = (2.0 * k) ** 2
        off_diagonal = np.full(BASIS_SIZE - 1, q_value, dtype=float)
        off_diagonal[0] = np.sqrt(2.0) * q_value
    elif family == "ce":
        diagonal = (2.0 * k + 1.0) ** 2
        diagonal[0] += q_value
        off_diagonal = np.full(BASIS_SIZE - 1, q_value, dtype=float)
    elif family == "se" and order > 0 and order % 2 == 1:
        diagonal = (2.0 * k + 1.0) ** 2
        diagonal[0] -= q_value
        off_diagonal = np.full(BASIS_SIZE - 1, q_value, dtype=float)
    elif family == "se" and order > 0:
        diagonal = (2.0 * k + 2.0) ** 2
        off_diagonal = np.full(BASIS_SIZE - 1, q_value, dtype=float)
        mode_index -= 1
    else:
        raise ValueError("se_0 is not a non-trivial Mathieu mode")

    value = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        eigvals_only=True,
        select="i",
        select_range=(mode_index, mode_index),
        check_finite=False,
    )[0]
    return float(value)


def _integrate_mode(order: int, family: str, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    characteristic = _characteristic_value(order, family, Q)
    if family == "ce":
        initial = (1.0, 0.0)
    elif family == "se" and order > 0:
        initial = (0.0, 1.0)
    else:
        raise ValueError("se_0 is not a non-trivial Mathieu mode")

    def rhs(t: float, state: np.ndarray) -> tuple[float, float]:
        y, yp = state
        return yp, -(characteristic - 2.0 * Q * np.cos(2.0 * t)) * y

    sol = solve_ivp(
        rhs,
        (float(x[0]), float(x[-1])),
        initial,
        method="DOP853",
        t_eval=x,
        rtol=RTOL,
        atol=ATOL,
        max_step=np.pi / 80.0,
    )
    if not sol.success or not np.all(np.isfinite(sol.y)):
        raise RuntimeError(f"Mathieu integration failed for {family}_{order}: {sol.message}")

    y, yp = sol.y
    period_end = int(np.argmin(np.abs(x - 2.0 * np.pi)))
    x_period = x[:period_end + 1]
    y_period = y[:period_end + 1]
    norm_sq = float(trapezoid(y_period ** 2, x_period))
    if not np.isfinite(norm_sq) or norm_sq <= 0.0:
        raise RuntimeError(f"Invalid normalization integral for {family}_{order}: {norm_sq}")
    scale = np.sqrt(np.pi / norm_sq)
    return scale * y, scale * yp


def _periodicity_error(y: np.ndarray, yp: np.ndarray, x: np.ndarray) -> float:
    idx = int(np.argmin(np.abs(x - 2.0 * np.pi)))
    reference = max(np.hypot(y[0], yp[0]), 1.0)
    return float(np.hypot(y[idx] - y[0], yp[idx] - yp[0]) / reference)


def main() -> None:
    x = np.linspace(0.0, X_MAX, N_POINTS)
    modes: dict[tuple[str, int], tuple[np.ndarray, np.ndarray]] = {}
    for order in range(4):
        modes[("ce", order)] = _integrate_mode(order, "ce", x)
        if order > 0:
            modes[("se", order)] = _integrate_mode(order, "se", x)

    max_closure_error = max(
        _periodicity_error(y, yp, x) for y, yp in modes.values()
    )
    if max_closure_error > 5.0e-8:
        raise RuntimeError(
            f"Periodic closure check failed: max relative mismatch={max_closure_error:.3e}"
        )

    with figure_style():
        fig, ax = plt.subplots(figsize=(13.4, 7.8))
        for order in range(4):
            ce_y, _ = modes[("ce", order)]
            ax.plot(x, ce_y, color=COLORS[order], linestyle="-", label=rf"$m={order}$")
            if order > 0:
                se_y, _ = modes[("se", order)]
                ax.plot(x, se_y, color=COLORS[order], linestyle="--")

        for boundary in (2.0 * np.pi, 4.0 * np.pi):
            ax.axvline(boundary, color="0.55", linewidth=1.0, linestyle=":", zorder=0)
        ax.axhline(0.0, color="0.35", linewidth=0.9, zorder=0)

        style_handles = [
            Line2D([0], [0], color="black", lw=2.7, ls="-", label=r"$\mathrm{ce}_m$"),
            Line2D([0], [0], color="black", lw=2.7, ls="--", label=r"$\mathrm{se}_m$"),
        ]
        add_dual_legend(ax,
            handles1=style_handles,
            handles2=[Line2D([0], [0], color=COLORS[o], lw=2.7, ls="-", label=rf"$m={o}$")
                      for o in range(4)],
            kw2=dict(loc="center left", bbox_to_anchor=(1.02, 0.42), title=r"mode"))

        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"normalized amplitude")
        ax.set_title(rf"Mathieu functions, $q={Q}$")
        ax.set_xlim(0.0, X_MAX)
        ax.set_xticks(
            np.arange(0.0, X_MAX + 0.1, np.pi),
            [r"$0$", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"],
        )
        polish_axes(ax, grid=False)
        save_figure(fig, "mathieu_function.png")

    print(f"Mathieu periodic closure max error: {max_closure_error:.3e}")


if __name__ == "__main__":
    main()
