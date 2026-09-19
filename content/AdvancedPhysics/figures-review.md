# AdvancedPhysics 配图审查与精修记录

审查基线：`python main.py build AdvancedPhysics`（无 --figures）生成 `build/AdvancedPhysics/main.pdf`，共 421 页。
视觉 QA：PyMuPDF (fitz) 150 dpi 渲染图页，300 dpi 局部放大。
全书 PDF 共 10 张配图（ch13 五张：3 个 TikZ + 2 个 matplotlib；ch19/21/24 各 1 张；ch28 两张）。
注：`rabi_dynamics_code.py` 未被任何 `\includegraphics` 引用，为孤儿脚本，不进 PDF，不做视觉 QA。

---

## 问题总览（初查）

| 图编号 | 文件 | 页 | 问题类别 | 严重度 |
|---|---|---|---|---|
| 13.1 | tikz/radiation-reaction/frequency-regime-map.tex | p164 | 竖直虚线穿标签 | 中 |
| 13.2 | code/radiation-reaction/form_factor_shell_code.py | p170 | 无 | — |
| 13.3 | tikz/radiation-reaction/worldtube-geometry.tex | p176 | 标签拥挤粘连 | 中 |
| 13.4 | tikz/radiation-reaction/dirac-decomposition.tex | p179 | 两框边框重叠 | 高 |
| 13.5 | code/radiation-reaction/order_reduction_error_code.py | p190 | 无 | — |
| 19.1 | atomic-molecular/code/strong_field_return_code.py | p304 | 无 | — |
| 21.1 | atomic-molecular/code/doppler_limit_code.py | p327 | annotation 字面 `\n` | 高 |
| 24.1 | atomic-molecular/code/franck_condon_code.py | p363 | 无 | — |
| 28.1 | atomic-molecular/code/fano_lineshape_code.py | p414 | 无 | — |
| 28.2 | atomic-molecular/code/landau_zener_code.py | p417 | legend 压曲线 | 中 |

---

## 图 13.1 frequency-regime-map（参数平面四象限图）

**问题**：竖直虚线分隔线 `x=1.65` 穿过左列多行标签——"long-wave region" 末尾的 "on"、"multipole expansion" 末尾的 "on" 被虚线切过；底部 "overlap / soft multipole limit" 第二行也被虚线压住。根因：左列宽仅 1.65 绘图单位（x 比例 1.25cm/单位），装不下 `\small` 宽英文标签，而标签仍居中于左列中心 x≈0.8。

**修改方案**：
1. 竖直分隔虚线由 `x=1.65` 右移到 `x=2.4`，拓宽左列；
2. 左列两个标签（long-wave、overlap）中心由 x≈0.8 重定位于新列中心 `x≈1.25`，使其完全落在虚线左侧；
3. 右列标签（general-frequency、soft-frequency、exact parent box）保持原位，仍在新分隔线右侧；
4. 不改动任何文字内容、坐标轴与箭头语义。

**验证方式**：单图 harness 渲染 → 重排后 PDF p164 复核：虚线不再压任何文字，四象限标签各自居区。

## 图 13.2 form_factor_shell（形状因子曲线）

**结论**：legend 右上、frameon，5 条曲线在左侧/中部衰减，右上为空白区，不遮挡；坐标轴与标注正常。无修改。

## 图 13.3 worldtube-geometry（Fermi 世界管几何）

**问题**：中心区标签拥挤粘连。`u^\mu` 竖直箭头标签置于世界线右侧顶部 `(0.09,0.55)`，与水平半径 `\ell` 箭头的上方标签 `(0.55,0.25)` 距离过近，渲染成粘连的 "u^μℓ"。

**修改方案**：把 `u^\mu` 标签从世界线右侧顶部移到世界线左侧中段空白处（左管壁与世界线之间、Σ1/Σ2 之间的空区），用 `anchor=east` 右对齐到世界线左侧；`\ell`、`n^\mu` 标签保持不变。箭头本身（u 沿世界线、n 横向法向、ℓ 横向半径）物理方向正确，不改动。

**验证方式**：单图 harness 渲染 → 重排后 PDF p176 复核：u^μ 与 ℓ 标签不再粘连，三向量标签互不重叠。

## 图 13.4 dirac-decomposition（两支路流程图）

**问题**：`dirac` 框（中心 x=1.35）与 `tube` 框（中心 x=4.95）水平间距 3.60cm 不足以容纳两个宽文本框，左框右边框与右框左边框重合约 55px，边框线切穿 "decomposition" 末尾字母与 "F_adv)" 括号。

**修改方案**：拉开水平间距——`dirac` 中心由 x=1.35 左移到 x=0.3，`tube` 中心由 x=4.95 右移到 x=5.7，使两框间留出明显间隙；`self`、`ll` 仍居中 x=3.15（恰为新两框中点 ~3.0），两支汇聚箭头自然收束。全部箭头语义（分叉→两支独立→汇聚到同一 ALD→LL 降阶）保持不变。

**验证方式**：单图 harness 渲染 → 重排后 PDF p179 复核：两框边框分明、无文字被边框切穿。

## 图 13.5 order_reduction_error（log-log 误差标度）

**结论**：两条线（数值误差 / O[(τ/T)²]）重合展示二次标度，legend 左上不遮挡，无修改。

## 图 19.1 strong_field_return（强场回碰截止）

**结论**：两曲线极值点标注 3.17/10.01 清晰，legend 右上空白区，无修改。

## 图 21.1 doppler_limit（Doppler 极限）

**问题**：annotation 用原始字符串 `r'$\Delta=-\Gamma/2$\n$T_D=...$'`，`\n` 在 raw string 中不被解释为换行，mathtext 也不把它当换行，导致图中直接显示字面量 `\n`（读作 "Δ=−Γ/2\nT_D=…"）。

**修改方案**：把 annotation 文本改为 `r'$\Delta=-\Gamma/2$' + '\n' + r'$T_D=\hbar\Gamma/(2k_B)$'`，用真实换行连接两个 raw 数学段。annotation 位置、箭头、legend 不变。

**验证方式**：重生成 png/pdf → PDF p327 复核：annotation 分两行、无字面 `\n`。

## 图 24.1 franck_condon（Franck–Condon 因子）

**结论**：三条 Poisson 分布，legend 右上不压曲线，无修改。

## 图 28.1 fano_lineshape（Fano 线型）

**结论**：四条 q 曲线，legend 左上两列、红峰在中部，不遮挡，无修改。

## 图 28.2 landau_zener（Landau–Zener 能级）

**问题**：legend 位于 `loc='upper left'`，但绿色绝热线从左上 (-4,2.25) 下行，从 "Adiabatic" legend 文字旁擦过（曲线紧贴文字顶部）；该角并非真空白。

**修改方案**：legend 改 `loc='center left'`。左中竖直通道（y≈0，x=−4…−2）在四条 X 型曲线之间为真正空白（上下对角斜线分别在 y≈±1），legend 不压任何曲线。

**验证方式**：重生成 png/pdf → PDF p417 复核：legend 落于左中空区，不与绿线/蓝线相交。

---

## 附：构建基础设施修复（非视觉，必要修复）

- 6 个 atomic-molecular 脚本原写 `ROOT = Path(__file__).resolve().parents[4]`，实测 parents[4]=`content/` 而非仓库根，导致 `from preamble import ...` 报 `ModuleNotFoundError`。已统一改为 `parents[5]`（=仓库根 YHWNotes/）。涉及：doppler_limit / fano_lineshape / franck_condon / landau_zener / rabi_dynamics / strong_field_return 六个 `_code.py` 的路径行。
- 两个 radiation-reaction 脚本用向上搜索 `preamble.py` 的方式定位仓库根，路径正确，无需改。
- 根目录 `preamble.py` 已由构建方提供（figure_style / polish_axes / add_legend / save_pdf_png_pair），未改动。

## 重编译与最终视觉复核结果

最终命令：`python main.py build AdvancedPhysics --figures`（在仓库根执行）。
结果：退出码 0；`build/AdvancedPhysics/main.pdf` 421 页、2,701,020 字节；`example/AdvancedPhysics.pdf` 同步更新；日志无 `^!`/`LaTeX Error`/`Undefined control`/`undefined references`。

逐图最终复核（fitz 150 dpi 重新渲染新 PDF）：

| 图 | 页 | 复核结果 |
|---|---|---|
| 13.1 | p164 | ✅ 竖直虚线已右移，左列三行标签均不被穿过，四象限各居其区 |
| 13.3 | p176 | ✅ u^μ 移至世界线左侧，与 ℓ、n^μ 三标签分离、不粘连 |
| 13.4 | p179 | ✅ Dirac/Fermi 两框间距清晰，边框不再切穿文字；箭头逻辑不变 |
| 21.1 | p327 | ✅ annotation 分两行，字面 `\n` 已消除 |
| 28.2 | p417 | ✅ legend 移至左中空区，不再压绿色绝热线 |
| 13.2/13.5/19.1/24.1/28.1 | — | 初查即无问题，本次未改，重编译后保持正常 |

同类审计：①全书仅这 3 个 tikzpicture（无章节内联），已全部覆盖；②其余 `_code.py` 无第二处 raw-string 字面 `\n`；③未引用的 rabi_dynamics 脚本不进 PDF。

剩余未解决问题：无。
