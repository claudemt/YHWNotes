from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from preamble import COLORS, figure_style, polish_axes, save_pdf_png_pair  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "generated"
OUT.mkdir(parents=True, exist_ok=True)

with figure_style():
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    # electron beam
    ax.add_patch(FancyArrowPatch((0.8, 3.0), (9.3, 3.0), arrowstyle='->', mutation_scale=20, linewidth=2.6, color=COLORS[0]))
    ax.text(1.0, 3.35, 'electron beam')
    # nanostructure
    ax.add_patch(Rectangle((4.4, 1.4), 0.45, 3.2, fill=False, linewidth=2.2, edgecolor=COLORS[1]))
    ax.text(4.1, 4.95, 'nanostructure')
    # optical near field waves
    xs = np.linspace(4.9, 7.6, 250)
    ys = 3.0 + 0.7*np.sin(5*(xs-4.9))*np.exp(-0.45*(xs-4.9))
    ax.plot(xs, ys, color=COLORS[2], linewidth=2.2)
    ax.text(6.3, 4.25, 'synchronous\nnear field', ha='center', va='bottom')
    # spectrometer box
    ax.add_patch(Rectangle((8.0, 1.9), 1.1, 2.2, fill=False, linewidth=2.0, edgecolor=COLORS[3]))
    ax.text(8.55, 4.35, 'EELS', ha='center')
    ax.text(7.9, 1.35, 'sideband readout')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('PINEM geometry')
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    save_pdf_png_pair(fig, 'pinem_experiment_geometry', output_dir=OUT)
