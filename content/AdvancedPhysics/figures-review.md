# AdvancedPhysics 配图精修记录（2026-09-20）

审查范围：`content\AdvancedPhysics\` 下全部 TikZ 配图。
定位方式：对 `content\AdvancedPhysics` 递归 `Get-ChildItem -Filter *.tex` 后全量 grep `\begin{tikzpicture}`、`\includegraphics`、`\input{`。
结果：全仓共 3 个 TikZ 配图，全部位于 `figures\tikz\radiation-reaction\`，均由 `ch13.tex` 通过 `\input{...}` 引入（第 121、866、1032 行）；章节正文内无内联 `tikzpicture`，无 `\includegraphics` 位图。无遗漏。
审查口径：standalone 预编译（`\documentclass[tikz,border=12pt]{standalone}`，粘贴 preamble.tex 第 196–219、225–238 两个 `\tikzset` 块，`\providecommand{\ii}{\mathrm{i}}`），`pdflatex` 出 PDF，PyMuPDF 300dpi 出 PNG，Read 亲眼复核 5 项不合格标准。

## 逐图清单

### figures\tikz\radiation-reaction\dirac-decomposition.tex — Dirac 分解/自力推导流程图（ch13 第 1032 行 input）
- 检查结果：通过。7 个 `lecturebox`/`lecturewidebox` 节点分层排布（parent→smooth/point→memory/dirac/tube→self→ll），同层框等高对齐；箭头全部正交（`|-`/`--` 直角走线）；所有文字均在框内，无文字压线、无框重叠、无箭头穿字、无标签贴线（箭头只落在节点边框锚点上）。
- 改动：无需改动。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，5 项标准均干净。

### figures\tikz\radiation-reaction\frequency-regime-map.tex — 频率/尺度区域划分图（ch13 第 121 行 input）
- 检查结果：初版不合格。竖直虚线分界原位于 x=2.50，左上象限 "long-wave region / multipole expansion" 标签（原中心 x=1.25）最宽行右缘已压到/贴到该竖直虚线（间隙 <3pt）；左下 "overlap / soft multipole limit"、右上 "general-frequency region"、右下 "soft-frequency region" 三组标签同样因象限偏窄而贴线偏挤。
- 改动：将竖直虚线分界由 x=2.50 右移至 x=2.85（`(2.50,0)--(2.50,4.75)` → `(2.85,0)--(2.85,4.75)`）；四个区域标签中心横坐标相应重排——左上 (1.25,3.75)→(1.35,3.75)、左下 (1.25,0.63)→(1.35,0.63)、右上 (4.05,3.25)→(4.45,3.25)、右下 (4.05,0.64)→(4.45,0.64)。水平虚线 (y=1.35)、坐标轴、"exact parent formula" 圆角框与底部说明文字坐标未动；重排后框左缘与新分界仍留有清晰间隙，框下缘与 "general-frequency region" 标签仍留有清晰间隙。
- 渲染确认：改后 standalone 300dpi PNG 已 Read 复核，四组标签与竖直分界、水平虚线、坐标轴、公式框之间均无压线/贴线/穿字/重叠，5 项标准均干净。

### figures\tikz\radiation-reaction\worldtube-geometry.tex — Fermi 世界管几何示意图（ch13 第 866 行 input）
- 检查结果：初版不合格。左世界管壁为左右两条虚线世界管边界；"Σ2" 标签原锚点 (-0.92,1.55)（`left` 锚）右缘距左侧虚线管壁仅约 1pt，"Σ1" 标签原锚点 (-1.0,-1.55) 距管壁约 2.8pt，均 <3pt，属标签贴线/疑似线穿标签右缘。
- 改动：将 "Σ1"、"Σ2" 两个 `left` 锚标签横坐标同步左移至边距中——(-1.0,-1.55)→(-1.35,-1.55)、(-0.92,1.55)→(-1.35,1.55)。两条水平截面线端点 (-1.0,-1.55)、(-0.92,1.55) 及世界线、管壁、`ℓ`/`u^μ`/`n^μ`/`T_self`/`timelike wall` 各箭头与标签坐标未动。
- 渲染确认：改后 standalone 300dpi PNG 已 Read 复核，Σ1/Σ2 与左侧虚线管壁留有清晰间隙，其余标签（z^μ(τ)、u^μ、ℓ、timelike wall ∂W、n^μ、T_self dΣ_μ）与世界线/管壁/箭头均无压线、穿字、重叠，5 项标准均干净。

## 2026-09-21 — style unification pass（matplotlib 脚本）

将 8 个 AdvancedPhysics 配图脚本的硬编码 matplotlib 样式统一为继承 `preamble.py` 的共享样式。

- 改动范围：
  - 移除 `plt.subplots(...)` 中的硬编码 `figsize=`：仅 `form_factor_shell_code.py`（原 `(6.6, 4.1)`）与 `order_reduction_error_code.py`（原 `(6.4, 4.2)`）存在；其余 6 个 atomic-molecular 脚本本就是裸 `plt.subplots()`，未动。全部改用 preamble 默认 `figure.figsize=[8.0, 5.0]`。
  - 移除全部 `add_legend(...)` 调用中的 `frameon=False`（preamble 默认 `frameon=True`）。
  - 移除全部 `add_legend(...)` 中的显式 `loc=`，改用默认 `"best"` 自动定位。
  - 未发现任何 `ax.set_title(...)`，无需处理。
  - 其余标签、注释、数据、保存路径均未改动。
- 逐脚本：
  - `atomic-molecular\code\doppler_limit_code.py`：`add_legend(ax,loc='upper left',frameon=False)` → `add_legend(ax)`。
  - `atomic-molecular\code\fano_lineshape_code.py`：`add_legend(ax,loc='upper left',frameon=False,ncol=2)` → `add_legend(ax,ncol=2)`。
  - `atomic-molecular\code\franck_condon_code.py`：`add_legend(ax,loc='upper right',frameon=False)` → `add_legend(ax)`。
  - `atomic-molecular\code\landau_zener_code.py`：`add_legend(ax,loc='center left',frameon=False)` → `add_legend(ax)`。
  - `atomic-molecular\code\rabi_dynamics_code.py`：`add_legend(ax,loc='upper center',frameon=False)` → `add_legend(ax)`。
  - `atomic-molecular\code\strong_field_return_code.py`：`add_legend(ax,loc='upper right',frameon=False)` → `add_legend(ax)`。
  - `code\radiation-reaction\form_factor_shell_code.py`：`plt.subplots(figsize=(6.6,4.1))` → `plt.subplots()`；`add_legend(ax, loc="upper right", frameon=False)` → `add_legend(ax)`。
  - `code\radiation-reaction\order_reduction_error_code.py`：`plt.subplots(figsize=(6.4,4.2))` → `plt.subplots()`；`add_legend(ax, loc="upper left", frameon=False)` → `add_legend(ax)`。
- 渲染确认：8 个脚本全部 `python` 重跑退出码 0、无报错，PDF/PNG 已通过 `save_pdf_png_pair` 重新生成；Read 逐一复核 PNG，`"best"` 自动定位的图例均落在数据空白区，无图例压线/穿数据，无需为任一脚本回加显式 `loc=`。

