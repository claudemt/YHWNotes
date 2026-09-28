# GroupTheory 图形规范

## 共享视觉规范

- 数值图统一调用根目录 `preamble.py` 的 `figure_style`、`COLORS`、`COLORMAPS`、`REFERENCE_LINE_STYLE`、`polish_axes`、`add_legend` 与 `save_pdf_png_pair`。
- 几何图和结构图统一使用根目录 `preamble.tex` 的 `tikzfig` 环境及公共 `wfA`、`lecturearrow`、`lecturebox`、`lecturelabel` 样式。章节文件不自行定义 `tikzset`，不覆盖共享线宽。
- 图内的形状、颜色和线型服务于群作用、表示空间、能级或几何对象的区分；字体、基础线宽、箭头尺寸、坐标轴与图例规则保持共享。
- Python 图以同名 PDF/PNG 配对输出至 `figures/generated/`；正文排版引用 PDF，PNG 用于视觉检查。

## 结构图目录

| 源文件 | 图示标签 |
|---|---|
| `ch01.tex` | `d3-symmetry`、`d3-cayley-graph` |
| `ch02.tex` | `d3-subgroup-lattice` |
| `ch05.tex` | `representation-homomorphism`、`intertwiner-diagram` |
| `ch06.tex` | `left-regular-action` |
| `ch09.tex` | `cube-axes`、`improper-rotation`、`proper-point-group-classification`、`sigma-hvd`、`schoenflies-family-tree` |
| `ch10.tex` | `screw-glide`、`stereographic-projection`、`bz-wigner-seitz`、`irreducible-bz` |
| `ch11.tex` | `irrep-degeneracy`、`d-orbital-splitting`、`c3v-three-sites`、`ir-raman-schematic` |
| `ch12.tex` | `tr-kramers-bands` |
| `ch13.tex` | `euler-axis-angle`、`su2-double-cover` |
| `ch14.tex` | `crystal-spin-orbit-branching` |
| `ch16.tex` | `s4-young-diagrams`、`three-spin-s3` |
| `ch18.tex` | `su3-roots-defining-weights` |

每幅结构图均由章内语义标签定位；TikZ 源码位于相应章节，根与权图单独存于 `figures/tikz/su3-roots-weights.tex`。连续旋转的数值图为 `rotation_commutator`，由 `figures/code/rotation_commutator_code.py` 生成。

## 出版检查

在最终 PDF 的印刷尺寸下检查图意、标签、节点、箭头、线条交叉、留白和裁切。表示图必须与相邻正文中的映射或分解一致；坐标图须核对轴、点、轨道和群作用的含义；数值图须核对参考渐近式和误差尺度。发现局部样式差异时，修正共享样式或调用方式，不在单图中另建视觉规范。
