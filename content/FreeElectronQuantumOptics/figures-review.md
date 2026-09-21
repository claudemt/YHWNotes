# FEQO 配图精修记录（2026-09-20）

审查范围：`content/FreeElectronQuantumOptics/` 下全部 TikZ 配图。逐图流程：standalone 包裹（含 preamble 第 196-219、225-238 两个 `\tikzset` 块原文 + `\providecommand{\ii}{\mathrm{i}}`）-> `pdflatex -interaction=nonstopmode` 编译 -> PyMuPDF 300 dpi 渲染 PNG -> Read 肉眼逐条对照 5 项标准（压字/重叠/贴线/穿字/不规整）。每张改动后二次渲染复核。未运行整书 build。

共审 TikZ 图 **58** 张（A 26 + B 13 + C 19），外部 `\includegraphics` 引用 **56** 处。实际修改 **3** 张。

---

## A. 独立 Feynman 图（`figures/tikz/`，26 张）

### bhabha-two.tex  Bhabha s/t 两图
- 检查结果：通过。s、t 标签在波浪线上方留隙，节点/箭头无重叠。
- 改动：无需改动。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，5 项标准均干净。

### breit-wheeler-two.tex  Breit-Wheeler 两图
- 检查结果：内段费米子动量标签 `$p_1-k_1$` / `$p_1-k_2$` 原以 `above=3pt,fill=white` 直接压在 y=0 水平内段线上（白底盖住，违反标准 #4）。
- 改动：两处标签锚点由 `(0,0)` 上移到 `(0,0.62)`（`above=2pt`），使标签真正离开内段线。
- 渲染确认：二次渲染 PNG 已 Read，两标签均悬空、线不再穿字。

### compton-two.tex  Compton s/u 两图
- 检查结果：通过。`$p+k$`、`$p-k'$` 在内外段上方留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### ee-gammagamma.tex  e-e+ -> gamma gamma
- 检查结果：通过。无标签，线/顶点规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### ee-mumu.tex  e-e+ -> mu- mu+
- 检查结果：通过。`$q^2=s$` 在交换光子上方留隙，外围 e/mu 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### emu-scattering.tex  e-mu 散射 t 道
- 检查结果：通过。`$q^2=t$` 在垂直波浪线右侧留隙，p1-p4 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### feynman-poles.tex  p^0 复平面极点
- 检查结果：通过。两极点黑点 + 竖虚线，极点标签与坐标轴标签均不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### lorentz-representation-map-dp8.tex  Lorentz 表示层级框图
- 检查结果：`2:1 covering map` 标签原 `above` 默认紧贴 SL<->SO 短连线，白底压线。
- 改动：改为 `above=4pt`，标签在两框间隙内抬离连线，且不压两框顶边框。
- 渲染确认：二次渲染 PNG 已 Read，标签悬空、不压框。

### moller-two.tex  Moller t/u 两图
- 检查结果：通过。t、u 标签在波浪线上方留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qcd-elementary-vertices-dp10.tex  QCD 基本顶点 (a)-(e)
- 检查结果：通过。a,mu / a,b,c 及 ghost 标签均在波浪线/虚线侧留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qcd-tree-processes-dp10.tex  QCD 树图 (a)(b)
- 检查结果：通过。g^a、t/u/s 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-elementary-vertex-dp7.tex  QED 三端顶点
- 检查结果：通过。q,lambda / p,s / p',s' / p+q=p' 均在各自线侧留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-exchange.tex  单光子交换
- 检查结果：通过。p/p'/k/k'/q 及传播子式均不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-loop-atlas-dp7.tex  一圈图集合 (a)-(d)
- 检查结果：通过。无标签压线，环结构规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-loops.tex  四基本环图
- 检查结果：通过。标签在图下方，不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-lsz-amputation-dp8.tex  LSZ 截肢框图
- 检查结果：通过。Z2^{...}/Z3^{...} 箭头标签在水平箭头上方留隙，框等高。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-tree-atlas-dp7.tex  树图集 (a)-(f)
- 检查结果：通过。s/u、p3<->p4 等标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-vacpol-cut-dp9.tex  真空极化 cut
- 检查结果：通过。q / p- / p+ 标签及右侧两式均不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qed-vacuum-polarization-dyson-dp7.tex  Dyson 级数
- 检查结果：通过。Pi 标签在环下方，级数规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### qft-bubble-cut-dp8.tex  标量气泡 cut
- 检查结果：通过。P/k/(P-k) 标签及右侧两式清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### soft-bremsstrahlung.tex  软轫致辐射
- 检查结果：通过。outgoing/incoming 标签在水平线下留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### uehling-loop.tex  Uehling 环
- 检查结果：通过。Ze/e- 圈、q^0=0 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### vertex-correction-detailed.tex  详细顶点修正
- 检查结果：通过。ell、q=p'-p 标签在环上下方留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### volkov-plane-wave.tex  Volkov 平面波
- 检查结果：通过。p^mu/pbar^mu 在对角线两端，背景波浪线为设计性交叉。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### wigner-little-group-dp9.tex  Wigner 小群框图
- 检查结果：通过。框对齐、箭头正交，各标签不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### yukawa-exchange.tex  Yukawa 交换
- 检查结果：通过。q 虚线及 p1/p1'/p2/p2'、传播子式清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

---

## B. 流程/关系框图（`figures/qft_process_figures.tex`，13 张）

### QFTWickContractionFigure  Wick 收缩字典
- 检查结果：通过。Wick contractions 箭头标签、S_F/D_F 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTVirtualPhotonExchangeFigure  单虚光子交换
- 检查结果：通过。p1/p1'/p2/p2'、q=p1-p1' 及右侧三行说明均不压线。
- 改动：无需改动（节点内全角冒号为书中正文标点，书籍 XeLaTeX 可编译，非几何缺陷）。
- 渲染确认：已 Read 复核，干净。

### QFTCrossingChannelsFigure  交叉三过程
- 检查结果：通过。湮灭/对产生/外场轫致辐射三图标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTTwoPhotonExchangeFigure  盒图与交叉盒图
- 检查结果：通过。无标签，线/顶点规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTEulerHeisenbergFigure  四光子环
- 检查结果：通过。右侧四行说明与环分离。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTKeldyshContourFigure  Keldysh 闭合围道
- 检查结果：通过。C+/C- 支标签、1+/2- 点、t0/tmax 虚线、括号说明均不交叉。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTFeshbachProjectionFigure  Feshbach 投影
- 检查结果：通过。P/Q 框等高，QHP/PHQ 弯曲箭头标签在弧顶/底留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### MacroQEDGreenFlowFigure  宏观 QED Green 流
- 检查结果：通过。6 框对齐，source/invert 标签在间隙，E/R->O 用 -| 正交走线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### GeneralInteractionRecoilFigure  连续态->反冲梯
- 检查结果：通过。同行框等高，箭头正交。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTCutkoskyFigure  Cutkosky cut
- 检查结果：通过。Cutkosky cut 箭头标签、左右环下方两式清晰，cut 竖虚线规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTForestSubgraphFigure  BPHZ 森林公式
- 检查结果：通过。子图虚线框、apply T_gamma first 箭头、local counterterm 框均不重叠。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTSoftInclusiveFigure  软共线 KLN 抵消
- 检查结果：通过。hard kernel 灰团、虚线求和弧与 inclusive observable 框分离。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### QFTComptonTreeFigure  Compton s/u 树图
- 检查结果：通过。p_gi/p_gf/p+p_gi/p-p_gf 均不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

---

## C. 章节内联 TikZ（19 张）

### ch03.tex:1312  phi^4 四点 Green 函数
- 检查结果：中心相互作用点标签 `$z$` 原 `above right` 压在指向 x3 的斜线上。
- 改动：改为 `above=5pt`，z 落于 x1/x3 两线之间的正上方空档，与四条斜线及中心黑点均分离。
- 渲染确认：二次渲染 PNG 已 Read，z 悬空、不压任何线。

### 02a-scattering-kinematics.tex:289  相空间三角形
- 检查结果：通过。x+y=1 沿线旋转标签、physical region、坐标轴 0/1 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04b-qcd-dis-factorization-dp13.tex:41  DIS 示意
- 检查结果：通过。k/k'/q/P/X 标签均在各自线侧留隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04b-qcd-dis-factorization-dp13.tex:305  DIS 因子化流程
- 检查结果：通过。框等高对齐，箭头正交。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04b-qcd-nlo-inclusive-dp12.tex:32  虚修正/实发射
- 检查结果：通过。两图标签在下方，线/顶点规整。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04b-qcd-nonperturbative-dp11.tex:50  格点 link/plaquette
- 检查结果：通过。方格网与四向箭头、右侧三行说明不交叉。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04b-qcd-running-ir-dp10.tex:298  gamma* -> q qbar g
- 检查结果：通过。q/g/qbar 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-ee-ww-cancellation-detail-dp11.tex:86  e-e+ -> WW 三图
- 检查结果：通过。e/e+/nu_e/W+/W-/gamma/Z 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-effective-potential-main-dp43.tex:113  V_eff 势曲线
- 检查结果：通过。极值点虚线、说明箭头、phi_star(xi) 标签均不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-fields-gauge-dp11.tex:168  手征表示->Yukawa
- 检查结果：通过。4 框对齐，箭头旁标签不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-flavor-anomaly-dp11.tex:238  CKM 构造
- 检查结果：通过。框对齐，diagonalize/compare bases 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-higgs-ewsb-dp11.tex:506  Weinberg 旋转
- 检查结果：通过。三框等高，箭头正交。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-mass-basis-rules-detail-dp11.tex:84  质量基规则依赖
- 检查结果：通过。6 框对齐，EWSB+basis change 等标签在间隙。
- 改动：无需改动（外层 adjustbox 仅缩放，standalone 验证时剥离，不影响仓库内容）。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-processes-rg-eft-dp11.tex:102  mu 衰变
- 检查结果：通过。mu-/nu_mu/W-/e-/nu_bar_e 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-processes-rg-eft-dp11.tex:196  e-e+ -> gamma/Z
- 检查结果：通过。e/e+/f/fbar/gamma/Z 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-processes-rg-eft-dp11.tex:301  h -> gamma gamma 两环
- 检查结果：通过。h/gamma/charged-fermion loop/W loop 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-rxi-quantization-detail-dp11.tex:134  Rxi 量子化流程
- 检查结果：通过。框对齐，identity constraints 等箭头标签不压线。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-smeft-matching-running-dp13.tex:206  SMEFT 匹配/RG
- 检查结果：通过。框对齐，各阶段标签在间隙。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

### 04c-sm-weak-widths-detail-dp11.tex:116  W/Z 衰变
- 检查结果：通过。W-/Z/ell/nu_bar/f/fbar 标签清晰。
- 改动：无需改动。
- 渲染确认：已 Read 复核，干净。

---

## D. 外部图片引用确认（`\includegraphics`，56 处）

- 55 张 PNG/PDF（含 `figures/generated/` 下 11 张 `content/...` 前缀图与 45 张裸文件名图）均在仓库中找到对应文件，路径有效。
- **1 张缺失**：`sections/sm-neutrino-matter-applications.tex:79` 引用 `neutrino_matter.pdf`，全仓库递归搜索无此文件（同族 `neutrino_electron_recoil.pdf` 存在）。属外部 raster 图（matplotlib 产物），非 TikZ 配图，本任务范围内不重建；建议后续补齐该 PDF 或修正引用名。

---

## 改动汇总

| 文件 | 位置 | 问题 | 改法 |
|---|---|---|---|
| `figures/tikz/breit-wheeler-two.tex` | 两 scope 内动量标签 | 白底压内段线 | 标签锚点 `(0,0)`->`(0,0.62)` |
| `figures/tikz/lorentz-representation-map-dp8.tex` | 第 15 行 covering map 标签 | 白底压短连线 | `above`->`above=4pt` |
| `ch03.tex` | 第 1318 行 z 标签 | above-right 压 x3 斜线 | `above right`->`above=5pt` |

未触碰 `content/YHWNotes`，未运行整书 build，未 git commit。

---

## 2026-09-21 — matplotlib 样式统一 pass（继承 `preamble.py`）

范围：`figures/code/` 下 FEQO 全部 32 张 matplotlib 配图脚本（任务清单所列）。未触碰其他 book，未 git commit，未运行整书 LaTeX build。

- **移除单轴脚本的硬编码 `figsize=(...)`**：25 张单轴脚本改为 `plt.subplots()`，继承 `preamble.figure_style()` 的默认 `figure.figsize=[8.0,5.0]`。
- **保留 1x2 子图脚本的 `figsize=(...)`**：`electron_bragg_convergence`、`electron_bunching_worked`、`electron_colored_noise`、`electron_detector_forward`、`electron_field_calibration`、`recoil_regime_map`、`sm_neutrino_matter`（需更宽画布）。
- **移除冗余 `frameon=`**：`add_legend(...)` 中的 `frameon=False` 与 `frameon=True` 一律删除（默认现为 `True`）；`ncol`/`fontsize`/`corner=` 等其余参数保留。
- **移除显式 `loc=`**：`add_legend(...)` 中的 `loc='...'` 一律删除，改用默认 `'best'`；`corner=` 保留。
- **移除 `ax.set_title(...)`**：按规则删除；保留两处例外——`hopfield_avoided_crossing` 的 `'RWA avoided crossing'`（图核心信息）与 `recoil_regime_map` 的两个子图标题（标注两个物理区间）。`electron_colored_noise` 子图用 `ax.set(..., title=...)` 标注 `|ℓ-m|` 区间，未改动。
- **未改动脚本**：`electron_field_calibration`、`recoil_regime_map`（仅需保留子图 figsize / 子图标题，无 frameon/loc/set_title 待清）。
- 全部 32 个脚本已逐一运行，退出码 0、无报错，PDF/PNG 已重新生成。
