# YHWNotes

YHWNotes is a collection of LaTeX-based academic notes on physics.

The repository serves as a personal knowledge base for advanced theoretical concepts, research references, and study materials.

The unified narrative and physics-exposition standard is documented in
[LECTURE_STYLE.md](LECTURE_STYLE.md). It defines the common chapter structure,
approximation bookkeeping, derivation rhythm, example design, and
cross-disciplinary writing conventions.

The full advanced-content roadmap and chapter-by-chapter restructuring plan is
documented in [supplement.md](supplement.md).

## Repository Layout

The notes cover five main fields: mechanics, electrodynamics, statistics, optics, and mathematical tools. Each field contains several topic-level notes.

```text
YHWNotes/
├── main.tex                     # Main entry point of the book
├── preamble.tex                 # Shared packages, page style, counters, boxes, and math commands
├── compile.ps1                  # Regenerates main.tex from the chapters directory
├── chapters/
│   ├── Mechanics/
│   ├── Electrodynamics/
│   ├── Statistics/
│   ├── Optics/
│   └── MathTool/
│       └── TopicName/
│           ├── topic_name.tex                  # Main note body for this topic
│           ├── topic_name_fig/                 # Figures used by this topic
│           │   ├── figure_name.png
│           │   └── topic_name_fig_code/        # Source code for generated figures
│           │       └── figure_name_code.tex
│           ├── topic_name_calculate/           # Optional calculation / validation scripts
│           ├── topic_name_mma/                 # Optional Mathematica notebooks
│           └── supplement_material/            # Optional supplementary derivations or files
├── fig/
│   ├── fig_config.tex            # Shared TikZ / circuitikz configuration for figure source files
│   ├── fig_draw.tex              # Standalone figure-compilation entry point
│   ├── compile_fig.ps1           # Regenerates fig_draw.tex from *_code.tex files
│   └── draw_platform_mmacode.txt # Auxiliary drawing / plotting code notes
├── build/                        # Compiled main PDF and LaTeX auxiliary files
└── LICENSE
```

A standard topic should include at least:

```text
chapters/[Field]/[Topic]/
├── [topic].tex
└── [topic]_fig/
    ├── [figure_name].png
    └── [topic]_fig_code/
        └── [figure_name]_code.tex
```

## Editing Rules

### Topic Files

Topic files are written as LaTeX fragments, not standalone documents. **Do not** add `\documentclass`, `\begin{document}`, or `\end{document}` inside a topic file; these are provided by `main.tex`.

To add a new topic:

1. Create a directory under the appropriate field, for example `chapters/Optics/NewTopic/`.
2. Add the main note file, for example `new_topic.tex`.
3. Add figures under `new_topic_fig/` if needed.
4. Include the topic in `main.tex` with `\subimport`:

`update_main.ps1` can be used to regenerate a scaffold of `main.tex` from the `chapters/` directory. The generated imports are commented out, so uncomment only the chapters and topics that should be compiled.

Note that since `main.tex` uses `\subimport`, paths inside a topic file are relative to that topic directory. 

### Figure Files

Figure source files are managed separately from the main book. The project-level figure entry point is `fig/fig_draw.tex`

To add a generated figure:

1. Put the figure source in `[topic]_fig/[topic]_fig_code/[figure_name]_code.tex`.
2. Run or edit `fig/update_fig_draw.ps1` so the file is listed in `fig/fig_draw.tex`.
3. Uncomment the corresponding `\input{...}` line in `fig_draw.tex` when compiling that figure.
4. Export the compiled result to PNG/PDF and place it in `[topic]_fig/`.
5. Include the exported image from the topic `.tex` file.

## Special Commands

### Math Commands

`preamble.tex` customizes several common math commands:

| Command | Meaning | Example |
| --- | --- | --- |
| `\vb{x}` | Bold vector using `\bm` | `\vb{E}` |
| `\uv{x}` | Bold unit vector with a hat | `\uv{e}_r` |
| `\d` | Upright differential operator | `\int f(x)\,\d x` |
| `\diag` | `diag` operator | `\diag(a,b,c)` |
| `\sinc` | `sinc` operator | `\sinc x` |
| `\arsinh`, `\arcsinh` | inverse hyperbolic sine | `\arsinh x` |
| `\arcosh` | inverse hyperbolic cosine | `\arcosh x` |
| `\artanh` | inverse hyperbolic tangent | `\artanh x` |
| `\sn`, `\cn`, `\dn` | Jacobi elliptic functions | `\sn(u,k)` |
| `\crossdot` | stacked cross-dot binary symbol | `A \crossdot B` |
| `\dotdotdot` | vertical three-dot binary symbol | `A \dotdotdot B` |

### Typesetting Commands

The preamble redefines `equation*` so that its body is automatically wrapped in `split`, so multi-line unnumbered equations can use alignment marks `&` and line breaks `\\` directly inside `equation*`.

Two numbered `tcolorbox` environments are provided: `example` and `notes`. Both are numbered within each section, breakable across pages, use compact spacing, and restore paragraph indentation inside the box.

To render example title format: `例 <number>`, use:

```tex
\begin{example}
  This is an example.
\end{example}
```

To render note title format: `注 <number>`, use:
```tex
\begin{notes}
  This is a note.
\end{notes}
```

### Figure Commands

`fig_config.tex` loads the figure packages:

```tex
\usepackage{tikz,tikz-3dplot,circuitikz,bm}
\usetikzlibrary{calc,arrows.meta,decorations.markings,positioning}
```

It also defines shared TikZ styles:

| Style | Purpose |
| --- | --- |
| `mid arrow` | Draws a thick line with a `Stealth` arrow at the middle of the path. |
| `lens` | Small blue-tinted optical lens block. |
| `plane` | Small gray-tinted plane or screen block. |
| `filter` | Small red-tinted filter block. |
| `axes` | Thin arrow style for coordinate axes. |
| `wfA`, `wfB`, `wfC` | Thin line styles for wavefronts or grouped curves. |
| `lab` | Small label style with a white translucent background. |

Shared figure environments:

```tex
\begin{LegendCircuitFigure}[<extra options>]
  ... circuitikz code ...
\end{LegendCircuitFigure}
```

Uses `circuitikz` with a thick default line width, `Stealth` arrows, large labels, and rounded line caps/joins.

```tex
\begin{LegendTikZFigure}[<extra options>]
  ... tikz code ...
\end{LegendTikZFigure}
```

Uses a standard `tikzpicture` with `Stealth` arrows and rounded line caps/joins.

```tex
\tdplotsetmaincoords{68}{125}
\begin{LegendTDPlot}[<extra options>]
  ... tikz-3dplot code ...
\end{LegendTDPlot}
```

Uses a `tikzpicture` with `tdplot_main_coords`. Set the 3D view with `\tdplotsetmaincoords{<theta>}{<phi>}` before the environment.

Confocal quadric helper commands:

```tex
\DrawConfocalAxes{xmax}{ymax}{zmax}
```

Draws 3D coordinate axes labeled `$x$`, `$y$`, and `$z$`.

```tex
\DrawConfocalEllipsoid{a}{b}{c}{lambda}{style}
```

Draws a confocal ellipsoid using base parameters `a`, `b`, `c`, a parameter `lambda`, and a TikZ style such as `wfA`.

```tex
\DrawConfocalOneSheet{a}{b}{c}{lambda}{tmax}{style}
```

Draws a one-sheet confocal hyperboloid. `tmax` controls the plotted parameter range `[-tmax,tmax]`.

```tex
\DrawConfocalTwoSheet{a}{b}{c}{lambda}{tmin}{tmax}{style}
```

Draws a two-sheet confocal hyperboloid. `tmin` and `tmax` control the plotted parameter range.

Example:

```tex
\tdplotsetmaincoords{68}{125}
\begin{LegendTDPlot}
  \def\aF{2.4}\def\bF{1.8}\def\cF{1.2}
  \DrawConfocalAxes{4.0}{3.0}{2.5}
  \DrawConfocalEllipsoid{\aF}{\bF}{\cF}{1.0}{wfA}
  \node[lab, align=center] at (0,0,0) [below=66pt]
    {$\xi=\mathrm{const}$\\(confocal ellipsoid)};
\end{LegendTDPlot}
```

## License

This project is released under the CC BY-NC-ND 4.0 License. 
