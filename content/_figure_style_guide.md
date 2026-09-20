# Figure style guide — block-logic diagrams (and matplotlib)

Applies to every block / map / lattice / flow schematic in `content/*/figures`.
Feynman topologies (wiggly photons, coiled gluons, fermion lines, loops) are **not**
covered by this guide — keep those as freeform diagrams. This guide is for boxes
that represent objects/spaces/operations connected by arrows.

## Reuse the shared styles (do not invent new ones)

All defined in root `preamble.tex` and always loaded:

| Style        | Use for |
|--------------|---------|
| `lecturebox` | rounded-corner content box (the look to reuse) |
| `blockbox`   | a layer box = `lecturebox` + fixed `minimum height`; size a layer with `minimum width` |
| `lecturearrow` / `layerarrow` | `-{Stealth}` arrow, 0.75 pt; `layerarrow` is the orthogonal-only alias |
| `line-label` / `blocklabel`  | white-backed label so arrows never show through glyphs |
| `blockmatrix` | ready-made `matrix of nodes` grid with `nodes=blockbox` and 9 mm gaps |

`content/_figure_style_guide.tex` is the `\input`-able twin of this file; it only
tunes these shared styles, it does not redefine them.

## Checklist

### Boxes
- Same-layer boxes share **one** `minimum width`. Pick `w` per layer and pass
  `minimum width=<w>mm` to every box in that row (e.g. all bottom-layer boxes get
  `minimum width=48mm`). Short content is centred; tall content does not stretch
  neighbours.
- Use `blockbox` (which inherits `lecturebox`). Box edges are always horizontal /
  vertical — **never rotate a box**.
- Lay nodes on an explicit grid: prefer `matrix of nodes` (`blockmatrix`) or fixed
  x-coordinates. Same row ⇒ same `y`; same column ⇒ same `x`.

### Arrows
- Horizontal flow → horizontal arrows. Vertical flow → vertical arrows.
- Avoid diagonal `to[out=...,in=...]` curves between layers unless genuinely
  unavoidable.
- When a fan-out is unavoidable, route it **orthogonally (L-shaped)**:
  - `-|` = horizontal first, then vertical.
  - `|-` = vertical first, then horizontal.
- Use `layerarrow` (= `lecturearrow`) for every such arrow. The picture must read
  as a grid, not a scribble.

### Arrow labels
- Always use `line-label` / `blocklabel` (white backing).
- Place the label in the whitespace next to the arrow — **not** on the arrow root,
  not on a box edge.
  - Horizontal arrow: `[above]` or `[below]` with a small `yshift`.
  - Vertical arrow: `[left]` or `[right]`.
- On an L-shaped `-|` / `|-` path, put the label on the straight leg (`pos≈0.75`
  for the second leg), anchored to the side with whitespace.

### Spacing
- Adjacent boxes in a row: consistent gap, e.g. `column sep=9mm` in a matrix, or
  an explicit x-separation of 3–4 cm.
- Leave ≥ 1 cm padding around the bounding box. Never cram everything into the
  centre.

### Overall
- The finished figure must read **square and aligned**: row baselines flat, column
  edges vertical, arrow lines orthogonal.

## matplotlib side

Every matplotlib figure in the repo must go through `preamble.py`:
wrap plotting in `with figure_style():`, call `polish_axes(ax)` (full frame, outward
ticks, faint dashed grid), `add_legend(...)` if a legend is wanted, and save with
`save_pdf_png_pair(fig, stem, output_dir)` to emit the embedded PDF plus a 200-dpi
PNG preview. **No script may set `rcParams`, `font.size`, or `figsize` beyond the
per-figure `figsize` that the data itself requires** — fonts, sizes, spines, grid
and DPI are owned centrally by `figure_style()` / `polish_axes` / `save_pdf_png_pair`.
