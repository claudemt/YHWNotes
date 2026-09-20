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

---

## 第二轮视觉精修（standalone 渲染 → Read 亲眼看图 → 改 → 再渲染验证）

本轮方法：每张 TikZ 用 `standalone + xelatex + fitz(220dpi)` 单独编译成 PNG 后 `Read` 逐像素核对 7 项；matplotlib 先 `python *_code.py` 重生成 PNG 再 `Read`。绝不只看代码。公共样式取自 `preamble.tex` 196–243 行。

| # | 文件 | 本轮问题（对应 7 类） | 改了什么 | 修复后确认 |
|---|---|---|---|---|
| T1 | tikz/radiation-reaction/dirac-decomposition.tex | 无（重渲染核对：两框间距足够、汇聚箭头分落 self 顶边两点、无文字压线、方向全部向下） | 不改 | ✅ Read PNG：Dirac/Fermi 框无重叠，8 条箭头干净 |
| T2 | tikz/radiation-reaction/frequency-regime-map.tex | 类 2/4：右上"exact parent formula"圆角框无底色，其左边框压在 x=2.50 竖直虚线右侧，虚线穿框（框内公式背后透出虚线） | 节点加 `fill=white`，中心由 (4.15,4.45) 右移到 (4.45,4.45) | ✅ Read freq2.png：虚线止于框底，白底盖线，框与 general-frequency 标签留白 |
| T3 | tikz/radiation-reaction/worldtube-geometry.tex | 类 2：`u^μ` 标签离竖直切向量箭头仅 ~3pt 偏挤；`n^μ, n·u=0` 标签右缘贴近右管壁虚线 | `u^μ` 标签由 (-0.05,0.05) 左移到 (-0.20,0.05)；n 水平箭头由 0.78 缩短到 0.62；n 标签中心由 (0.52,-0.45) 移到 (0.36,-0.45) | ✅ Read worldtube2.png：u 标签离箭头 6pt+，n 标签右缘离右墙留白 |
| M1 | atomic-molecular/code/doppler_limit_code.py | 类 7：annotation 两行文字压在下降段蓝曲线上（xytext=(-95,28) 落点正落在曲线 y≈0.77 处） | xytext 由 (-95,28) 上移到 (-90,52)，文字抬到曲线上方空区，引导箭头全程在曲线上方 | ✅ 重生成 PNG：文字位于 y≈0.95，曲线在其下，箭头不压曲线 |
| M2 | atomic-molecular/code/fano_lineshape_code.py | 无（legend 左上两列，红峰在中部，不遮挡；轴标签不裁切） | 不改 | ✅ Read PNG 确认 |
| M3 | atomic-molecular/code/franck_condon_code.py | 无（legend 右上，S=0.5 峰在 n=0 左上，legend 在右上空白） | 不改 | ✅ Read PNG 确认 |
| M4 | atomic-molecular/code/landau_zener_code.py | 无（legend 已为 center left，落于四曲线间 y≈0 真空白；2\|V\| 标注箭头不压绝热线） | 不改 | ✅ Read PNG 确认 |
| M5 | atomic-molecular/code/rabi_dynamics_code.py | 类 7：legend 在 upper right，Δ/Ω=0 蓝曲线从 x≈9.5 峰下穿过 legend 框（frameon=False，文字直接压在蓝线上） | legend loc 由 'upper right' 改为 'upper center'，落到两蓝峰之间的低谷空区（y≈0.9，x≈6–8） | ✅ 重生成 PNG：legend 在两峰之间空白，不压任何曲线 |
| M6 | atomic-molecular/code/strong_field_return_code.py | 无（legend 右上，此时橙曲线已降到近 0；3.17/10.01 极值标注不压线） | 不改 | ✅ Read PNG 确认 |
| M7 | code/radiation-reaction/form_factor_shell_code.py | 无（legend 右上带框，5 条曲线在左上衰减，右上空白） | 不改 | ✅ Read PNG 确认 |
| M8 | code/radiation-reaction/order_reduction_error_code.py | 无（log-log 双线重合，legend 左上，曲线从左下上升，不压 legend） | 不改 | ✅ Read PNG 确认 |

本轮实际修改 4 张：T2、T3、M1、M5；其余 7 张重渲染核对后保持原样。

---

## 第三轮 TikZ 复查（standalone → xelatex → fitz 300–400dpi → Read 逐图量距）

本轮范围严格限于 AdvancedPhysics 的 3 个内联 tikzpicture（`content/AdvancedPhysics/figures/tikz/radiation-reaction/`，均由 ch13 `\input`）。方法：standalone 复制 preamble.tex 196–243 行公共样式，xelatex 编译后 fitz 300/400dpi 渲染 PNG 并裁切可疑区域 Read 目测量间距，只改确实压线/压框/未对齐的图。

| # | 文件 | 类别 | 本轮问题（实测） | 坐标改动 | 渲染确认干净 |
|---|---|---|---|---|---|
| F1 | tikz/radiation-reaction/frequency-regime-map.tex | A | 坐标轴/四象限标签/虚线。复检：竖直虚线 x=2.50 已在前两轮右移到位；"general-frequency region" 与竖直虚线留白 ~8pt；左列 "overlap/soft multipole limit" 右缘距竖直虚线略紧但仍有可见白隙、未接触；公式框已 fill=white | 不改 | ✅ Read 全图+裁切：无标签压线/压框 |
| F2 | tikz/radiation-reaction/worldtube-geometry.tex | A | 第二轮 T3 把 n 标签移到 (0.36,-0.45) 后，400dpi 裁切确认其右端 `0` 仍与右管壁虚线 $\partial\mathcal W$ 相切（贴线，未达 5–8pt 留白） | 第 24 行 n 标签中心 `(0.36,-0.45)` → `(0.08,-0.53)` | ✅ Read chk0/chk1：`0` 离右壁留白 ≳8pt；中央世界线从 "n^μ," 与 "n·u=0" 词间空隙穿过、不压字形；左缘离左壁留白充足 |
| F3 | tikz/radiation-reaction/dirac-decomposition.tex | B | 第三层左框 `memory` 中心 `y=-3.10`，同行 `dirac`/`tube` 在 `y=-3.20`，左框上下边比同行高 1mm，未对齐成网格 | 第 12 行 `(memory) at (-3.15,-3.10)` → `(-3.15,-3.20)`（节点箭头自动连接，无需动箭头） | ✅ Read 全图：第三层三框上下边水平对齐；框边横平竖直；树状斜向连接符落点在框边、不压字；无箭头上文字标签 |

本轮实际修改 2 张：F2（worldtube 标签压线）、F3（dirac 框网格对齐）；F1 复检后保持原样。
本轮未触碰 `content/YHWNotes/`，未执行 git commit。

---

## 意思核对（2026-09-20）

本轮只核对"图的物理意思是否和正文一致"，不做视觉精修（视觉轮已在前 1–3 轮完成）。方法：先读 `.tex` 中 `\input`/`\includegraphics` 前后 3–5 段正文，弄清正文声称的关系；TikZ 图按 standalone 模板（复制 preamble.tex 196–207/213–226 公共样式块 + `\providecommand{\ii,\ee,\dd,\vb}`）xelatex 300 dpi 渲 PNG 后 `Read`；matplotlib 图直接 `Read` 现有 `generated/*.png` 并对照 `*_code.py` 与正文公式。重点核对 5 类：箭头/轴方向 vs 正文演化/因果；元素连接（谁连谁/包含/映射）；标签-对象对应；节点/分支数 vs 正文；实线/虚线/箭头/颜色 vs legend。

**范围勘误**：任务说"在 ch*.tex 里 grep `begin{tikzpicture}` 还有 3 张内联图"，但实测 `grep -n "begin{tikzpicture}" content/AdvancedPhysics` 只命中 3 个 `\input` 独立文件（frequency-regime-map / worldtube-geometry / dirac-decomposition），在 `ch*.tex` 内联搜 `tikzpicture|tikzfig|circuitfig` 为 **0**。即全书 TikZ 就是这 3 个，无内联图，前几轮"①全书仅这 3 个 tikzpicture"的结论不变。`rabi_dynamics_code.py` 仍为孤儿脚本，跳过。实际核对 10 张图（3 TikZ + 7 matplotlib）。

逐图记录：

### 图 13.1 frequency-regime-map（参数平面四象限）

- **正文怎么说**（ch13 caption line 123；正文 line 86/96/116）：ε_soft=ωT_sc 控制时间软展开（散射历史），κ_src=ωa_src/c 控制源内空间相位的多极展开；两个小参数相互独立，整个参数平面由精确母式覆盖。
- **图原来怎么画**：x 轴 κ_src=ωa_src/c（向右增大），y 轴 ε_soft=ωT_sc（向上增大）；竖直虚线 x=2.50，水平虚线 y=1.35。四象限：左上"long-wave region, κ_src≪1, multipole expansion"；左下"overlap, soft multipole limit"；右下"soft-frequency region, ε_soft≪1, asymptotic-state control"；右上"general-frequency region, full spatial phase and trajectory history"；精确母式框在右上。
- **意思问题**：无。左列=κ 小（长波/多极），底行=ε 小（软频），左下=两近似同时成立（overlap），右上=两者都不展开（general）。轴方向、边界位置、四象限命名与正文"两个独立方向"完全自洽。
- **改成什么**：不改。
- **验证**：standalone 渲 freq PNG 300dpi Read：x 向右、y 向上，四象限各居其区，母式框在 general 区，无方向反转。

### 图 13.2 form_factor_shell（形状因子）

- **正文怎么说**（caption line 494；exbox line 142–148）：薄球壳精确强度比 = sinc²κ_src，Gaussian 云 = e^{−κ_src²/2}；虚线是各自低 κ 展开。
- **图原来怎么画**：shell=(sinκ/κ)²（实线），gaussian=e^{−κ²/2}（实线），shell LW=1−κ²/3（虚线），gaussian LW=1−κ²/2（虚线），竖点线 κ=1；x=κ_src，y=I/I_point。
- **意思问题**：无。sinc²κ 小 κ 展开 1−κ²/3、e^{−κ²/2} 展开 1−κ²/2，与脚本一致；shell 在 κ=π≈3.14 过零后小回升，Gaussian 单调衰减，均符合。
- **改成什么**：不改。
- **验证**：Read generated/form_factor_shell.png：两条实线衰减、两条虚线小 κ 贴合、shell 在 ~3.14 处过零，坐标轴与 legend 对应正确。

### 图 13.3 worldtube-geometry（Fermi 世界管）

- **正文怎么说**（line 861；caption line 868）：在固有时 τ 端面上取单位类空径向量 n^μ，满足 n·u=0、n²=−1；ℓ>0 是沿该端面的局域空间半径；u^μ 是世界线切矢（时间方向）。
- **图原来怎么画**：世界线 z^μ(τ) 竖直蜿蜒；两虚线管壁平行世界线（竖直）；Σ1/Σ2 水平横截（垂直世界线）；ℓ 箭头水平向右（横向）；u^μ 箭头沿世界线向上（时间方向）；n^μ 箭头水平向右（横向，n·u=0）；T_self dΣ_μ 从右壁径向向外。
- **意思问题**：无。世界管横向延展方向（ℓ，水平）确实垂直于世界线切方向（u，竖直），管壁平行世界线、端面横截世界线——几何朝向正确，没有反。u 沿世界线向上（τ 增大/未来向），n 与 ℓ 都横向，符合 Fermi 局部标架。
- **改成什么**：不改。
- **验证**：standalone 渲 worldtube PNG 300dpi Read：u 箭头沿竖直线向上，ℓ/n 箭头水平，管壁平行竖线，Σ1/Σ2 水平，径向箭头出壁。

### 图 13.4 dirac-decomposition（两支路流程）

- **正文怎么说**（caption line 1034；正文 line 999–1025）：父式 Maxwell+守恒分出有限尺寸支路（保留因果记忆）与点粒子极限支路；点极限中 Dirac 正则分解（F_S=½(F_ret+F_adv)，F_R=½(F_ret−F_adv)）与 Fermi 世界管守恒是两种独立组织，汇聚到同一有限 ALD 自力；LL 是后文的受控降阶。
- **图原来怎么画**：parent（顶）→ smooth（左）+ point（右）；smooth → memory（左列"history-dependent memory"）；point → dirac + tube；dirac 和 tube 都 → self（ALD）；self → ll（Landau–Lifshitz）。共 8 条箭头，全部向下。
- **意思问题**：无。分支/汇聚结构与正文"两支独立组织、汇聚同一 ALD"完全一致；dirac 框内 F_S/F_R 公式与正文式(1000)一致；memory 挂在有限尺寸支而非点粒子支，正确。
- **改成什么**：不改。
- **验证**：standalone 渲 dirac PNG 300dpi Read：树状连接、汇聚、降阶三级层次清楚，箭头方向全部向下（因果）。

### 图 13.5 order_reduction_error（降阶误差标度）

- **正文怎么说**（caption line 1834；line 1827）：ε_grad=τ_rr/T 的截断误差从二阶 O(ε_LL²) 起。
- **图原来怎么画**：log-log，"numerical error" 实线 vs O[(τ_rr/T)²] 虚线参考线；x=τ_rr/T，y=relative L² error。
- **意思问题**：无。两线在 log-log 上几乎重合、斜率=2，证实二次标度。
- **改成什么**：不改。
- **验证**：Read generated/order_reduction_error.png：双线平行重合于斜率 2 直线。

### 图 19.1 strong_field_return（强场回碰截止）

- **正文怎么说**（ch19 line 191–212）：K_r/U_p=2(sinφ_r−sinφ_0)²，极值 3.17 U_p（HHG 截止）；回碰后反向弹性散射 K_rescatt/U_p=2[2sinφ_r−sinφ_0]²，极值 10 U_p。
- **图原来怎么画**：脚本 Kret=2(sinφr−sinφ0)²、Kresc=2(2sinφr−sinφ0)²，brentq 解第一返回支 F=0；标注极值 3.17 / 10.01；x=电离相位 φ_0。
- **意思问题**：无。两曲线表达式、极值位置、rescatter 曲线恒在 ret 之上均与正文一致。
- **改成什么**：不改。
- **验证**：Read generated/strong_field_return.png：蓝(K_ret)峰 3.17、橙(K_resc)峰 10.01，rescatter 包络 ret。

### 图 21.1 doppler_limit（Doppler 冷却极限）

- **正文怎么说**（ch21 line 265–275；caption line 283）：记 x=|2Δ|/Γ_sp，k_BT=(ℏΓ_sp/4)(x+1/x)；AM–GM 不等式最小在 x=1（即 Δ=−Γ_sp/2，红失谐侧），k_BT_D=ℏΓ_sp/2。
- **图原来怎么画**：脚本 T=0.25(1+(2ξ)²)/|2ξ|，ξ=Δ/Γ；x 轴只画负失谐（红失谐）；散点+注释标在 (ξ=−0.5, T=0.5)，文字 "Δ=−Γ/2, T_D=ℏΓ/(2k_B)"。
- **意思问题**：无。把脚本式 0.125(1+4ξ²)/|ξ| 代入 x=2|ξ| 恰为 (1/4)(x+1/x)，与正文式严格等价；求导最小在 |ξ|=0.5，T_min=0.5=ℏΓ/(2k_B)，注释位置/表达式全对；只画红失谐（冷却侧）物理正确。
- **改成什么**：不改。
- **验证**：Read generated/doppler_limit.png：U 形谷底在 Δ/Γ=−0.5、k_BT/(ℏΓ)=0.5，注释两行、箭头指谷底。

### 图 24.1 franck_condon（Franck–Condon 因子）

- **正文怎么说**（ch24 line 258–275）：|⟨n_e|0_g⟩|²=e^{−S_HR}S_HR^n/n!（Poisson），均值=方差=S_HR；S≪1 零声子线主导，S≫1 分布移到 n~S。
- **图原来怎么画**：脚本 P(n)=e^{−S}S^n/n!，S∈{0.5,2,5}；x=末振动量子数 n。
- **意思问题**：无。S=0.5 峰在 n=0（e^{−0.5}=0.607）、S=2 峰在 n≈1–2、S=5 峰在 n≈4–5，均值=S 一致。
- **改成什么**：不改。
- **验证**：Read generated/franck_condon.png：三条 Poisson 峰位置随 S 右移、归一化总和合理。

### 图 28.1 fano_lineshape（Fano 线型）

- **正文怎么说**（ch28 line 374–386）：σ/σ_bg=(q+ε)²/(1+ε²)；|q|→∞ 退 Lorentzian，q=0 在 ε=0 反共振零点，q=±1 零点在 ε=∓1 最不对称。
- **图原来怎么画**：脚本 (q+ε)²/(1+ε²)，q∈{−1,0,1,3}；x=约化失谐 ε。
- **意思问题**：无。q=0 在 ε=0 为零、q=1 在 ε=−1 为零、q=−1 在 ε=+1 为零、q=3 在 ε=0 处峰≈9（Lorentzian），零点/峰位置与正文 line 380 逐项一致。
- **改成什么**：不改。
- **验证**：Read generated/fano_lineshape.png：四条曲线零点与峰位正确，legend 两列对应 q 值。

### 图 28.2 landau_zener（Landau–Zener 能级）

- **正文怎么说**（ch28 line 505–528；caption line 528）：diabatic H=diag(s t/2, −s t/2) 被常数 V 耦合，瞬时绝热能 E_±=±√((s t/2)²+|V|²)，最小间隙 2|V|；图只画 diabatic 与 adiabatic 能级。
- **图原来怎么画**：脚本 diabatic 虚线 ±a t/2（过原点相交），adiabatic 实线 ±√((a t/2)²+V²)；legend 虚线=Diabatic、实线=Adiabatic；"2|V|" 注释指向中心上方绝热支。
- **意思问题**：无。两条绝热支在交叉点 **不接触**（中心在 ±V，间隙 2V=2|V|）——正是 avoid crossing，若接触反而错；diabatic 虚线在 (0,0) 相交；label 挂线正确（虚线→Diabatic，实线→Adiabatic）。本图按 caption 仅含能级图、无"非绝热跃迁概率曲线"，任务该项 N/A。
- **改成什么**：不改。
- **验证**：Read generated/landau_zener.png：虚线 X 型交于原点，实线 U 型/∩型在中心分开留 2|V| 缺口，legend 落左中空区。

---

**本轮结论**：10 张图的物理意思与正文全部自洽，**未发现需要改源的意思错误**，故未改动任何 `.tikz`/`.py` 源，无需重渲染。唯一需要记录的范围勘误：任务所述"3 张内联 tikzpicture"在 ch*.tex 中实测为 0，全书 TikZ 即 3 个 `\input` 文件。本轮未触碰 `content/YHWNotes/`，未执行 git commit。
