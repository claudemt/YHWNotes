import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from fig_style_python import figure_style, polish_axes, save_figure

LAM_MIN, LAM_MAX = -2.0, 34.0
Q_MIN, Q_MAX = 0.0, 17.5
N_MAX = 6
BASIS_SIZE = 48

def _lowest_eigenvalues(diagonal, off_diagonal, count):
    return eigh_tridiagonal(
        diagonal, off_diagonal,
        eigvals_only=True, select="i",
        select_range=(0, count - 1), check_finite=False,
    )

def _characteristic_values_at(q_value):
    q_value = float(q_value)
    k = np.arange(BASIS_SIZE, dtype=float)

    diag_ce_even = (2.0 * k) ** 2
    off_ce_even = np.full(BASIS_SIZE - 1, q_value, dtype=float)
    off_ce_even[0] = np.sqrt(2.0) * q_value
    ce_even = _lowest_eigenvalues(diag_ce_even, off_ce_even, 4)

    diag_ce_odd = (2.0 * k + 1.0) ** 2
    diag_ce_odd[0] += q_value
    off_odd = np.full(BASIS_SIZE - 1, q_value, dtype=float)
    ce_odd = _lowest_eigenvalues(diag_ce_odd, off_odd, 3)

    diag_se_odd = (2.0 * k + 1.0) ** 2
    diag_se_odd[0] -= q_value
    se_odd = _lowest_eigenvalues(diag_se_odd, off_odd, 3)

    diag_se_even = (2.0 * k + 2.0) ** 2
    off_even = np.full(BASIS_SIZE - 1, q_value, dtype=float)
    se_even = _lowest_eigenvalues(diag_se_even, off_even, 3)

    a = np.empty(N_MAX + 1, dtype=float)
    b = np.full(N_MAX + 1, np.nan, dtype=float)
    a[0::2] = ce_even
    a[1::2] = ce_odd
    b[1::2] = se_odd
    b[2::2] = se_even
    return a, b

def _characteristic_curves(q):
    a_curves = np.empty((N_MAX + 1, q.size), dtype=float)
    b_curves = np.full((N_MAX + 1, q.size), np.nan, dtype=float)
    for index, q_value in enumerate(q):
        a_curves[:, index], b_curves[:, index] = _characteristic_values_at(q_value)

    if not np.all(np.isfinite(a_curves)) or not np.all(np.isfinite(b_curves[1:])):
        raise RuntimeError("Non-finite Mathieu characteristic value encountered")

    largest_jump = max(
        float(np.max(np.abs(np.diff(curve))))
        for curve in [*a_curves, *b_curves[1:]]
    )
    if largest_jump > 0.25:
        raise RuntimeError(f"Characteristic branch continuity check failed: jump={largest_jump:.3g}")
    return a_curves, b_curves

def main():
    u = np.linspace(0.0, 1.0, 1400)
    q = Q_MAX * u ** 1.55
    curves_a, curves_b = _characteristic_curves(q)

    with figure_style():
        fig, ax = plt.subplots(figsize=(12.8, 8.3))

        ax.fill_betweenx(
            q, LAM_MIN, curves_a[0],
            facecolor="0.93", edgecolor="0.45", hatch="////", linewidth=0.0,
            label="unstable",
        )
        for n in range(1, N_MAX + 1):
            lo = np.minimum(curves_a[n], curves_b[n])
            hi = np.maximum(curves_a[n], curves_b[n])
            ax.fill_betweenx(
                q, lo, hi,
                facecolor="0.93", edgecolor="0.45", hatch="////", linewidth=0.0,
            )

        for n in range(N_MAX + 1):
            ax.plot(curves_a[n], q, color="black", lw=2.0, solid_capstyle="round")
            if n > 0:
                ax.plot(curves_b[n], q, color="black", lw=2.0, solid_capstyle="round")

        ax.set_xlabel(r"$\lambda$")
        ax.set_ylabel(r"$q$")
        ax.set_title(r"Mathieu stability chart (instability shaded)")
        ax.set_xlim(LAM_MIN, LAM_MAX)
        ax.set_ylim(Q_MIN, Q_MAX)
        ax.set_xticks(np.arange(-2, 35, 2))
        ax.set_yticks(np.arange(0, 18, 2))
        polish_axes(ax, minor_ticks=False)
        save_figure(fig, "eigenvalue_curve_shaded_region_stable.png")

if __name__ == "__main__":
    main()
