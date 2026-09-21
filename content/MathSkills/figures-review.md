# MathSkills 配图精修记录（2026-09-20）

范围：仅 `content/MathSkills/`。递归 `Get-ChildItem -Recurse -Include *.tex` 后 grep `\begin{figure}` / `\includegraphics` / `\begin{tikzpicture}` / `\input{`，确认正文仅 3 处 `\includegraphics`（ch06.tex 1 处、ch07.tex 2 处），全部指向 matplotlib 生成的 PDF；无内联 tikzpicture；`figures/tikz/` 各子目录为空；`figures/code/`、`figures/generated/`（differential-geometry、mathematical-statistics、sturm-liouville）均无被引用的 PDF。未触碰 `content/YHWNotes`，未运行整书 build，未做 git 操作。

## 逐图清单

### content/MathSkills/figures/mathematical-physics/generated/tikhonov_filter.pdf 正则化滤波因子 q(s) 对比
- 检查结果：通过。图例位于 upper right 空白区，框内无任何曲线；蓝色 formal inverse 1/s 在 s≈0.12 处冲出图顶为该函数固有发散（ylim=12 为既定展示口径，非布局缺陷）；红色 TSVD 竖线 τ=0.18 与阈值线无文字标注压线；轴标签/刻度贴轴正常。
- 改动：无。
- 渲染确认：原始 PDF 已渲染 300dpi PNG 并 Read 复核（含图例区 2x 放大核对），5 项标准均干净。

### content/MathSkills/figures/mathematical-physics/generated/burgers_characteristics.pdf Burgers 方程 u0=-tanh ξ 特征线
- 检查结果：通过。图例（t*=1）位于 upper right，蓝色虚线 t*=1 在图例框下方留有间隙，未被图例框压住；右侧品红特征线斜率向上收束，在图例纵向高度处已位于框左侧，未穿框；17 条特征线在图顶 x≈±1.0 范围内收束，右上 x>1.5 区域为空，无元素重叠；标题、轴标签正常。
- 改动：无。
- 渲染确认：原始 PDF 已渲染 300dpi PNG 并 Read 复核（含图例区 2.2x 放大核对），5 项标准均干净。

### content/MathSkills/figures/mathematical-physics/generated/kdv_two_soliton.pdf KdV 双孤子散射三时刻叠加
- 检查结果：初查不合格。原脚本 `bbox_to_anchor=(1.01,1.0)` 使外置图例左边框紧贴右侧轴脊，绿色 t=6 曲线在 x≈20 处回升至 u=0 的顶端直接顶在图例左上角，蓝色/橙色零值平线亦顶到脊线——按"图例离曲线 <3pt 算贴/压线"标准判为贴线。
- 改动：仅改布局参数（未动数据与物理内容）——`kdv_two_soliton_code.py` 中 `bbox_to_anchor` 由 `(1.01, 1.0)` 改为 `(1.06, 1.0)`，`tight_layout(rect=...)` 右边界由 `0.83` 改为 `0.80`，使图例右移并与轴脊留出可见白缝；重跑脚本覆盖同名 PDF。
- 渲染确认：重生成 PDF 已渲染 300dpi PNG 并 Read 复核（含图例区放大核对），图例与右侧轴脊之间出现清晰白缝，绿曲线顶端不再顶图例，图例不溢出图边，5 项标准均干净。

## 小结
- 共审：3 张。
- 修改：1 张（kdv_two_soliton）；其余 2 张初查即合规，未改。

## 2026-09-21 — style unification pass
- 仅处理 `content/MathSkills/figures/mathematical-physics/code/` 下 3 个脚本（burgers_characteristics、kdv_two_soliton、tikhonov_filter），未触碰其他书，未 git commit，未跑整书 build。
- 改动：
  - 三脚本均删除 `plt.subplots(...)` 中硬编码 `figsize=(...)`，改用 preamble 默认 8x5。
  - burgers 删除 `ax.set_title(...)`；kdv 删除 `ax.set_title(...)`。
  - kdv 由外置图例（`loc='upper left', bbox_to_anchor=(1.06,1.0), borderaxespad=0.0` + `tight_layout(rect=[0,0,0.80,1])`）改为轴内默认 `add_legend(ax)`（best、frameon=True），tight_layout 去掉 rect；重渲染后 matplotlib 自动选到左下空白角，曲线无明显重叠，无需指定 corner。
  - 三脚本均删除 add_legend 显式 `loc=`，统一走默认 best。
  - 标签、数据、save 路径均未改。
- 运行确认：3 个脚本均 `python` 重跑，退出码 0，无报错；kdv PNG 已 Read 复核，图例位于左下空白区，不压数据。
