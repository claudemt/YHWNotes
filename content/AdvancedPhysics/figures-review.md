# AdvancedPhysics 图形规范

## 共享视觉规范

- 数值图统一调用仓库根目录的 `preamble.py`：`figure_style`、`COLORS`、`COLORMAPS`、`REFERENCE_LINE_STYLE`、`polish_axes`、`add_legend` 与 `save_pdf_png_pair`。
- TikZ 图统一置于 `tikzfig` 环境中，使用根 `preamble.tex` 的 `wfA`、`lecturearrow`、`lecturebox`、`lecturelabel` 等公共样式。讲义章节和单图文件不另设 `tikzset`、线宽或私有图形调色板。
- 单图尺寸只按内容的长宽比调整；曲线颜色、虚实线和标记只表达数据类别，不改变字体、轴、图例、网格或线宽的全书规范。
- Python 图输出到 `figures/generated/`，由讲义引用的 PDF 与用于检查的 PNG 使用同一文件名。脚本以固定参数或随机种子重建图像。

## TikZ 图

| 文件 | 用途 | 共享样式 |
|---|---|---|
| `figures/tikz/frequency-regime-map.tex` | 频率与尺度区域 | `tikzfig`、`wfA`、`lecturearrow`、`lecturelabel` |
| `figures/tikz/worldtube-geometry.tex` | 世界管几何 | `tikzfig`、`wfA`、`lecturearrow`、`lecturelabel` |
| `figures/tikz/dirac-decomposition.tex` | 自力分解流程 | `tikzfig`、`lecturebox`、`lecturearrow`、`lecturelabel` |
| `figures/tikz/five-edge-graph.tex` | 有限图的顶点与边 | `tikzfig`、`wfA`、`lecturelabel` |

## Python 数值图

正文中的数值图由对应的 `figures/code/*_code.py` 生成：`biharmonic_square`、`biharmonic_disk_boundary`、`integral_equations`、`inverse_integral_regularization`、`plate_modal_response`、`plate_modal_shapes`、`ising_random_cluster`、`form_factor_shell`、`order_reduction_error`、`strong_field_return`、`doppler_limit`、`franck_condon`、`fano_lineshape` 与 `landau_zener`。

## 出版检查

在最终成书尺寸下检查每幅图的字号、线条、图例位置、节点间距、标签空隙、箭头方向和边界裁切。数值图还须核对坐标量纲、参数定义、收敛或残差断言；TikZ 图须核对几何关系与正文论断一致。构建检查包含图文件可找到、字体可用、引用有效以及图表未被缩放至难以阅读。
