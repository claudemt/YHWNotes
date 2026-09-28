#!/usr/bin/env python3
"""Finite-graph Ising correlation equals random-cluster connectivity."""
from itertools import product
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "preamble.py").exists())
sys.path.insert(0, str(ROOT))
from preamble import figure_style, polish_axes, add_legend, save_pdf_png_pair

OUT = Path(__file__).resolve().parents[1] / "generated"
EDGES = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))
SPINS = np.array(list(product((-1, 1), repeat=4)))
MASKS = range(1 << len(EDGES))


def components(mask):
    parent = list(range(4))

    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v

    for e, (a, b) in enumerate(EDGES):
        if mask & (1 << e):
            parent[root(a)] = root(b)
    return len({root(v) for v in range(4)}), root(0) == root(2)


component_counts = np.array([components(mask)[0] for mask in MASKS])
connected = np.array([components(mask)[1] for mask in MASKS])
edge_counts = np.array([mask.bit_count() for mask in MASKS])
spin_energy = sum(SPINS[:, a] * SPINS[:, b] for a, b in EDGES)


def observables(J):
    spin_weights = np.exp(J * spin_energy)
    spin_correlation = np.dot(spin_weights, SPINS[:, 0] * SPINS[:, 2]) / sum(
        spin_weights)
    p = 1 - np.exp(-2 * J)
    cluster_weights = 2.0**component_counts * p**edge_counts * (
        1 - p)**(len(EDGES) - edge_counts)
    cluster_probability = np.dot(cluster_weights, connected) / sum(cluster_weights)
    return spin_correlation, cluster_probability


couplings = np.linspace(0.0, 1.2, 81)
values = np.array([observables(J) for J in couplings])
assert np.max(np.abs(values[:, 0] - values[:, 1])) < 2e-14

with figure_style():
    fig, ax = plt.subplots()
    ax.plot(couplings, values[:, 0], "k-", label="Ising correlation")
    ax.plot(couplings[::8], values[::8, 1], "o", ms=4,
                 label="cluster connectivity")
    ax.set(xlabel="coupling $J$", ylabel="correlation / probability")
    polish_axes(ax, grid=True)
    add_legend(ax, corner="lower right")
    fig.tight_layout()
    save_pdf_png_pair(fig, "ising_random_cluster", OUT)
    plt.close(fig)

print("maximum identity residual:", np.max(np.abs(values[:, 0] - values[:, 1])))
