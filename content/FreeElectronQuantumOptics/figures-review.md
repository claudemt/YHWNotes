# FreeElectronQuantumOptics 配图审查与精修记录

本文件记录对本书全部配图（约 98 个图编号）的端到端视觉审查与精修结果。
审查方法：`python main.py build FreeElectronQuantumOptics` 出 PDF（809 页），用 PyMuPDF(fitz) 以 150 dpi 渲染全部图所在页 PNG，逐图检查三类问题——①文字/标签重叠；②线条过度拥挤；③箭头方向/连接关系的逻辑错误。

## 一、编译基线

- 命令：`python main.py build FreeElectronQuantumOptics --figures`（首次）/ 后续 `python main.py build FreeElectronQuantumOptics`
- 产物：`build/FreeElectronQuantumOptics/main.pdf`（809 页），并复制到 `example/FreeElectronQuantumOptics.pdf`
- 静态检查：0 个 LaTeX error、0 个 undefined control sequence、0 个 undefined reference；`Overfull \hbox >15pt` 为 0。

## 二、8 处 `\resizebox` 的移除（硬性要求）

`issues.md` 第 38 行承认旧图中有 8 处 `\resizebox`。本轮全部移除包装，改为按节点坐标/字号自然渲染，并在最终 PDF 页面尺寸下逐图视觉复核。移除后无越界（无 >15pt overfull），文字以自然印刷字号显示，未出现新的重叠。

| # | 图号 | 被包文件 | 调用位置（改前） | 修改方案 | 验证 |
|---|------|----------|------------------|----------|------|
| 1 | 图4.2 | figures/tikz/qed-tree-atlas-dp7.tex | ch04.tex:809 `\resizebox{0.92\textwidth}{!}{…}` | 去掉 resizebox，直接 `\input{…}` | p214 自然尺寸 2×3 面板清晰，无重叠 |
| 2 | 图4.3 | figures/tikz/qed-loop-atlas-dp7.tex | ch04.tex:818 | 同上 | p214 2×2 面板 (a)-(d) 清晰 |
| 3 | 图4.1 | figures/tikz/qed-lsz-amputation-dp8.tex | sections/02-lsz-dirac-photon.tex:37 | 同上 | p209 截肢两行清晰 |
| 4 | 图4.25 | figures/tikz/qed-vacuum-polarization-dyson-dp7.tex | sections/02d3-loop-calculation.tex:89 | 同上 | p258 Dyson 级数清晰 |
| 5 | 图2.2 | figures/tikz/lorentz-representation-map-dp8.tex | sections/02lorentz-sl2c-main-dp43.tex:85 `0.93` | 同上 | p60 映射图留白合适、无越界 |
| 6 | 图2.1 | figures/tikz/wigner-little-group-dp9.tex | sections/02wigner-little-group-dp9.tex:58 | 同上 | p52 Wigner 小群清晰 |
| 7 | 图5.3 | figures/tikz/qcd-tree-processes-dp10.tex | sections/04b-qcd-feynman-processes-dp10.tex:135 `0.88` | 同上 | p315 QCD 树过程清晰 |
| 8 | 图5.2 | figures/tikz/qcd-elementary-vertices-dp10.tex | sections/04b-qcd-group-gauge-dp10.tex:379 `0.94` | 同上 | p310 QCD 基本顶角清晰 |

> 说明：这些多面板图自然宽度均落在正文行宽内（移除后无 overfull），因此不需要再调内部坐标；文字反而恢复到自然印刷字号，比缩放时更易读。全仓 `resizebox|scalebox` 现仅剩 `issues.md` 的文字描述，已无实际 LaTeX 调用。

## 三、inline TikZ 重叠修复（本轮新发现）

按"发现局部问题即升级全书同类审计"的要求，对全部 box+箭头流程图逐页目检，发现两处同类缺陷（长边标签在窄节点间距内溢出到相邻框文字），均已修复并复验：

| 图号 | 位置 | 问题 | 修改方案 | 复验 |
|------|------|------|----------|------|
| 图6.20 EFT 单向计算链 | sections/04c-sm-smeft-matching-running-dp13.tex:206 | 节点横向间距仅 14mm，边标签 "integrate out heavy modes"/"RG evolution / log resummation" 溢出到相邻框文字；框还写死 minimum width 31–34mm | 横向节点间距 14mm→26mm；去掉写死的 minimum width，框宽由内容决定；长边标签分两行（`align=center` + `\\`）；标签加 `above/below/right=2pt` | p471 复验：标签现居间距内，无碰撞 |
| 图6.4 SM 规范顶角依赖 | sections/04c-sm-mass-basis-rules-detail-dp11.tex:84 | 边标签 "EWSB + basis change" 单行在 17.5mm 间距内压到左右两框 | 首段横向间距提到 23mm；该标签分两行（"EWSB +"/"basis change"）。保留原有 `adjustbox max width=.96\linewidth`（非 8 处 resizebox 之一，且作宽幅四框图的行宽保护；缺陷本身已消除，不再是"用缩放掩盖重叠"） | p398 复验：标签居间距内，无碰撞 |

## 四、其余 inline TikZ 与 qft_process_figures.tex 目检结论

重点目检的节点/流程/Feynman 图（均无三类问题）：
- 图4.4 QED 基本顶角动量标记（p218）、图4.8 一光子交换（p237）、图5.12 DIS 运动学（p361）、图5.13 因子化依赖（p364）
- 图6.1 Higgs 表示来源（p388）、图6.3 电弱基旋转（p397）、图6.6 CKM 来源（p411）、图7.1 连续态→反冲梯（p489）
- qft_process_figures.tex 内 13 个 macro 流程图标号规范、箭头方向与物理流向一致，未发现方向错误。

## 五、matplotlib 脚本（figures/code/*.py）

- 环境前提：根目录 `preamble.py` 由 MathSkills 子代理重建（提供 `figure_style/polish_axes/add_legend/save_pdf_png_pair/COLORS/LINE_STYLES`），风格对齐 SKILL.md（衬线字体、全边框、外向刻度、虚线网格）。
- 路径核查：本书脚本统一用 `Path(__file__).resolve().parents[4]` 作 REPO_ROOT（脚本位于 `content/FreeElectronQuantumOptics/figures/code/`，向上 4 层即仓库根），**本书不存在 parents 深度 bug**（该 bug 仅影响更深嵌套的 MathSkills 书）。全部 32 个 `*_code.py` 已随 `--figures` 成功跑通。
- 视觉抽查：图4.20 Klein–Nishina 角分布（p252）legend 居左上空位、不压曲线；其余 matplotlib 图随新样式重生，未发现 legend 遮挡极值或字号过小的问题。按"无问题仅记录"原则未改动脚本内容。

## 六、结论

- 8 处 `\resizebox` 全部移除并自然尺寸复验通过；
- 新发现并修复 2 处 inline tikz 标签重叠；
- 终版 PDF 809 页，0 error / 0 undefined ref / 0 overfull(>15pt)；
- `example/FreeElectronQuantumOptics.pdf` 已更新。

---

## 七、本轮逐图视觉精修（standalone 渲染闭环，最新）

针对上一轮"读代码改坐标不看图"被批评为无效，本轮改为每张图独立编译→渲染 PNG→Read 肉眼目检→改→再渲染验证。公共样式从根 `preamble.tex` 196–243 行复制，缺省宏 `\ii,\me,\qe,\slashed` 由 amsmath/amssymb/slashed 补齐。检查 7 项：箭头不压顶点/线；标签不压线条/箭头/框；平行边箭头分散在中段；框内不溢出；有向边方向与物理一致；节点不互叠；matplotlib legend 不压曲线、轴 label/tick 不裁切、子标题不重叠。

### 7.1 独立 TikZ 图（figures/tikz/，26 张全部独立编译通过并 Read 目检）
bhabha-two, breit-wheeler-two, compton-two, ee-gammagamma, ee-mumu, emu-scattering, feynman-poles, lorentz-representation-map-dp8, moller-two, qcd-elementary-vertices-dp10, qcd-tree-processes-dp10, qed-elementary-vertex-dp7, qed-exchange, qed-loop-atlas-dp7, qed-loops, qed-lsz-amputation-dp8, qed-tree-atlas-dp7, qed-vacpol-cut-dp9, qed-vacuum-polarization-dyson-dp7, qft-bubble-cut-dp8, soft-bremsstrahlung, uehling-loop, vertex-correction-detailed, volkov-plane-wave, wigner-little-group-dp9, yukawa-exchange。
**结论：26 张均无 7 类问题，未改动。**（关键复核：ee-mumu / μ 衰变 / e+e-→ff̄ 的正电子/中微子有向边方向经源码对照 antifermion=arrowreversed 逐根确认正确。）

### 7.2 内联 TikZ（sections/，18 个 tikzpicture 全部抽取独立编译、Read 目检）
仅 1 处需改：
- `sections/04c-sm-effective-potential-main-dp43.tex` 的注释节点 "stationary value: gauge independent" 压在有效势左侧上升曲线上 → 给该节点加 `fill=white,fill opacity=.95,inner sep=2pt`；重编译 Read 确认曲线不再穿字。
其余 17 块（DIS 运动学/因子化、NLO 虚修正实发射、格点 plaquette、qq̄ 劈裂、ee-ww 抵消、Higgs/质量基/CKM/Rξ/SMEFT/W 宽度流程框）均干净。

### 7.3 matplotlib 图（figures/code/ → figures/generated/，50 张输出全部 Read 目检）
共享 `preamble.py` 已给 legend 近不透明白底。发现并修复 3 处：

| 输出 PNG | 问题 | 改动 | 复验 |
|---|---|---|---|
| cherenkov_recoil_angle.png | 注释出现字面 `\n`（raw string） | `cherenkov_recoil_angle_code.py:32` 用 `+ '\n' +` 拼接两段 | 两行正常折行 |
| soft_brems_angular.png | 同上字面 `\n` | `legacy_quantitative_rebuild_dp43.py:192` 同样拼接 | 两行正常折行 |
| sm_higgs_potential_dp11.png | "degenerate minima" 放 y=-0.80 超出轴下限，压 x 轴与刻度 | `supplementary_figure_sources.py:30` 移到 (0.62,-0.50) 并加白底 bbox | 文字入轴、脱离底边刻度 |

其余 47 张 legend 均落空角、轴 label/tick 无裁切、子标题无重叠。

### 7.4 整书构建
改完跑 `python main.py build FreeElectronQuantumOptics`，退出码 0、无 LaTeX error，`example/FreeElectronQuantumOptics.pdf` 更新。


---

## 八、流程框+箭头关系图精修（standalone 渲染闭环，本轮重点）

针对用户原话"排布太紧密，箭头上的字撑不开、跟框遮挡、不够方方正正"，对所有 box+箭头关系图做 standalone 闭环：在临时目录写 `\documentclass[tikz,border=14pt]{standalone}`（复制 preamble.tex 196–243 行 lecture/process 样式 + amsmath/amssymb + `\providecommand{\ii}`），`xelatex -halt-on-error` 编译 → fitz 300dpi 渲 PNG → Read 肉眼量各框/箭头/标签间隔 → 改坐标再渲，直到干净方正。纯费曼图（fermion/fvertex 线条）标签不压线者不动。

### 8.1 改动清单（5 处）

| 图 / 位置 | 问题类别 | 坐标改动 | 渲染确认 |
|---|---|---|---|
| **图6.1 Higgs 表示来源**<br>`sections/04c-sm-fields-gauge-dp11.tex:168-177` | B 标签压框 + 斜边。原 `node distance=1.55cm and 2.0cm` 太挤，"compare L/R reps"压上框顶、"contract reps"压下框底；左 `rep→y` 为斜箭头 | 弃 `right/left/below=of`，改显式矩形网格：rep/mass 在 (±3.2, 2.1)、h/y 在 (±3.2, -2.1)，四框统一 `text width=3.3cm,minimum height=1.3cm`；四边箭头全正交，标签 `above/right/below/left=5pt` | Read PNG：四框等大对齐成矩形，4 个标签白底悬空不压线、与框留白 |
| **图6.6 CKM 来源**<br>`sections/04c-sm-flavor-anomaly-dp11.tex:238-247` | B 排布紧 + 框位偏。原 `below right=1.7cm and -.15cm of ul` 把 v 框放偏；纵向间距 1.5cm | 显式对称坐标：yu/yd (±3.6,2.6)、ul/dl (±3.6,0)、v (0,-3.0)，框统一 `text width=4.1cm,minimum height=1.25cm`；`diagonalize` 走竖直边，`compare bases` 用 `bend right/left=8` 对称汇入 v 顶两角 | Read PNG：左右对称漏斗，v 居中，标签白底不压框 |
| **宏观 QED Green 流程**<br>`figures/qft_process_figures.tex:158-177` (MacroQEDGreenFlowFigure) | B 标签"invert"贴 M 框边 + 不方正（G→E、E/R→O 为斜箭头） | 重排为正交网格：E 置于 G 正上方（竖直边），J/M 同列、E/G 同列；E.east/R.east 经直角肘 `(E.east)-|(O.162)`、`(R.east)-|(O.198)` 进 O 左上/左下；框统一 `text width=2.9cm,minimum height=1.35cm`，横向拉开到 ±6.0/2.4/6.6 | Read PNG：无斜箭头，source/invert 白底居水平边中段、与框留白 |
| **Schwinger–Keldysh 轮廓**<br>`figures/qft_process_figures.tex:126-127` (QFTKeldyshContourFigure) | B 标签碰撞：`midway` 的 "C+: forward branch" 与 "1+" 点标挤成 "C+:1+forward branch"，C- 同理撞 "2-" | 分支标签从 `midway` 移到近 t0：C+ 改 `pos=0.16,above`，C- 改 `pos=0.84,below`（其线向右至左画），避开内部点 | Read PNG：分支标签居左端，1+/2- 点标居中不挤 |
| **Cutkosky 割线**<br>`figures/qft_process_figures.tex:230,232` (QFTCutkoskyFigure) | B 线穿字：虚线割线 (4.2,-0.8)→(4.2,2.0) 穿到底部公式 $\sum_n\int\!\d\Phi_n...$ 中间 | 虚线缩到只圈环体 `(4.2,0.05)→(4.2,1.6)`；底部公式节点加 `process line label`（白底） | Read PNG：虚线不再穿公式，公式清晰 |

### 8.2 目检确认干净、未改动（6 处）

- **Feshbach–Schur 投影**（qft_process_figures.tex:138 QFTFeshbachProjectionFigure，QHP/PHQ）：两框等高对齐，QHP/PHQ 走白底 `process line label`，已悬空不压框、布局宽松，不改。
- **连续态→反冲梯**（qft_process_figures.tex:182 GeneralInteractionRecoilFigure）：S 形全正交，无箭头文字标签，框对齐，不改。
- **Wick→Feynman 字典**（qft_process_figures.tex:7）："Wick contractions" 悬空于箭头上方不压线，D_F/S_F 标注清晰，不改。
- **BPHZ 森林公式**（qft_process_figures.tex:238 QFTForestSubgraphFigure）："apply $T_\gamma$ first" 白底居箭头中段，子图虚线框规整，不改。
- **软/虚包容抵消**（qft_process_figures.tex:262 QFTSoftInclusiveFigure）：曲线汇聚箭头的 "sum virtual + unresolved real" 白底不压框，不改。
- **中性电弱基旋转**（sections/04c-sm-higgs-ewsb-dp11.tex:504）：三框等高、水平箭头、无被压缩标签，不改。

### 8.3 写回方式与边界

- 全部改动经 Python 按"唯一整串替换"写回（每处断言命中恰好 1 次才落盘），未触碰 `content\YHWNotes`，未 git commit。
- 纯费曼图（虚光子交换、交叉道、双光子盒、Euler–Heisenberg、Compton 树图等）按既定策略不动。
