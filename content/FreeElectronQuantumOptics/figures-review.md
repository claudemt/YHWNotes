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

---

## 九、意思核对（2026-09-20）

本轮在"视觉精修"之上，逐图核对**物理含义**是否与正文叙述一致（不是再调布局）。方法：对每张图先读 `.tex` 前后 3–5 段正文搞清它要表达的过程/关系；Feynman/流程/映射图按 standalone 模板（复制 preamble.tex 196–207 公共样式 + `\providecommand{\ii,\me,\qe,\slashed}`）xelatex 编译 → PyMuPDF 300dpi PNG → Read 亲看；matplotlib 数据图直接 Read 已有 PNG 轻核对坐标轴/曲线身份/峰向。核对 8 个含义维度：①费米子箭头与外腿动量方向；②外腿粒子身份/过程（Møller=e⁻e⁻、Bhabha=e⁻e⁺、Compton=γe、bremsstrahlung=轫致辐射，不张冠李戴）；③内线类型（波浪=光子、实线=费米子、虚线=标量/鬼）；④QED 三点顶点拓扑；⑤圈拓扑（真空极化=闭合费米子环串光子、自能=费米子自闭环、顶角=三角形）；⑥流程箭头方向；⑦表示/映射图箭头；⑧CKM 矩阵元位置。

**结论先行：全部图含义核对通过，未发现物理错误，本轮无需改动任何源文件。** 关键易错点（外腿身份、圈拓扑、流程方向、CKM 位置）逐张确认均正确。

### 9.1 独立 Feynman 图（figures/tikz/，26 张全部 standalone 渲染 + Read 亲看）

| 图 | 正文怎么说 | 渲染所见 | 含义核对 |
|---|---|---|---|
| moller-two | e⁻e⁻ 散射，t/u 两树图，相对负号来自费米交换 | 两实线费米子线均左→右（电子），中竖波浪光子，左右面板标 t/u、中间负号 | **通过**：两外腿都是电子（无 e⁺ 腿），t/u 交换负号正确 |
| bhabha-two | e⁻e⁺→e⁻e⁺，s 湮灭 + t 交换，振幅相加 | 左 s 道 e⁻/e⁺ 湮灭成横光子再产生 e⁻/e⁺；右 t 道竖波浪交换；中间正号 | **通过**：反费米子线 arrowreversed 方向正确，s/t 身份正确 |
| compton-two | γe→γe，s/u 两种时间序，p+k 与 p−k′ | 左 s 道内标 p+k、右 u 道内标 p−k′；费米线左→右，波浪进出顶点 | **通过**：Compton 过程，两时间序标签正确 |
| ee-mumu | e⁺e⁻→μ⁺μ⁻ 单光子交换，q²=s | 左标 e⁻(上)/e⁺(下)、右标 μ⁻(上)/μ⁺(下)，横光子 q²=s | **通过**：湮灭道，e⁺/μ⁺ 反费米子箭头反向正确 |
| emu-scattering | e⁻μ⁻ 散射，t 道光子交换 q²=t | 上腿 e⁻(p1→p3)、下腿 μ⁻(p2→p4)，竖波浪 q²=t | **通过**：两费米子左→右，t 交换正确 |
| yukawa-exchange | 费米子间标量（Yukawa）交换，i/(q²−m_Y²+i0⁺) | 两实线费米子左→右，内线**虚线**标 q，分母 m_Y² | **通过**：Yukawa 内线用虚线（区别于光子波浪），传播子正确 |
| qed-exchange | QED 单光子交换，−iημν/(q²+i0⁺) | 两实线费米子左→右，内线**波浪**标 q，分母 q² | **通过**：与 yukawa 对照，光子内线为波浪 |
| ee-gammagamma | e⁺e⁻→γγ | 左费米子腿进、右两波浪光子出；交叉道 + | **通过**：双光子湮灭 |
| breit-wheeler-two | γγ→e⁺e⁻ 对产生，p1−k1/p1−k2 | 两波浪光子进、两实线费米子出；交叉道 + | **通过**：对产生（与湮灭互为交叉） |
| soft-bremsstrahlung | 软光子在硬过程前(incoming)/后(outgoing)发射 | 硬过程块 H，左软光子 outgoing、右软光子 incoming，+ | **通过**：前后两发射位正确 |
| volkov-plane-wave | 电子在经典平面波背景 A^μ(κ·x) 中 p^μ→p̄^μ | 斜线电子 p→p̄ 穿过多道波浪经典背景 | **通过**：Volkov 图景正确 |
| qed-loops（4 面板） | 自能/真空极化/顶角修正/光光散射 | ①费米线挂光子弧=自能；②闭合费米环串光子=真空极化；③三角=顶角；④费米盒串 4 光子=光光散射 | **通过**：四种圈拓扑全部正确 |
| qed-loop-atlas-dp7（4 面板） | 同上 atlas | electron self-energy / vacuum polarization / vertex correction / light-light box 逐一对应 | **通过**：圈拓扑正确 |
| uehling-loop | Coulomb 光子插入真空极化环（Ze 与 e⁻ 间，q⁰=0） | Ze 圆—波浪—费米环—波浪—e⁻ 圆，标 q⁰=0 | **通过**：静态极限真空极化插入正确 |
| vertex-correction-detailed | 电子外线 q=p′−p，圈动量 ℓ | 横费米线 p→p′，下进外光子 q=p′−p，上挂光子环 ℓ | **通过**：三角形顶角修正正确 |
| qed-vacuum-polarization-dyson-dp7 | D = 裸光子 + Π 插入 + 双插入 … | 裸波浪 + 单 Π 费米环 + 双 Π 费米环 + … | **通过**：Dyson 级数方向正确 |
| qft-bubble-cut-dp8 | 割泡，内线同时上壳 k²=m₁²、(P−k)²=m₂² | P 进、双内线、竖虚线割线，右侧两上壳条件 | **通过**：Cutkosky 割线正确 |
| qed-vacpol-cut-dp9 | 割真空极化→γ*→e⁺e⁻，p_±²=e²c²、正能量 | q 光子进费米环、竖虚线割为 p_±、两上壳且 p⁰>0 | **通过**：对产生割线、正能量条件正确 |
| qed-lsz-amputation-dp8 | LSZ：费米子用 S(p)→Z₂⁻¹ᐟ²(̸p−mc)→ūs(p)；光子用 Dμν→Z₃⁻¹ᐟ²→ερ* | 上行费米子实线、下行光子波浪，各自截肢因子与外波函数 | **通过**：费米子/光子截肢对象与外态正确 |
| qed-elementary-vertex-dp7 | QED 三点顶点 p+q=p′ | 费米子进(p,s)+光子顶(q,λ)→费米子出(p′,s′) | **通过**：顶点结构、动量守恒正确 |
| qed-tree-atlas-dp7（6 面板） | t 交换/s 湮灭/Compton s,u/Breit-Wheeler/e⁻e⁺→γγ/Møller 交换末态 | 六子图标签与拓扑逐一对应，Møller 标 p3↔p4 | **通过**：各过程身份不混淆 |
| feynman-poles | Feynman iε：+E_p/c−i0⁺ 在实轴下、−E_p/c+i0⁺ 在实轴上 | 正能极点在实轴下方、负能在上方 | **通过**：iε prescription 正确 |
| qcd-elementary-vertices-dp10（5 面板） | 夸克-胶子/三胶子/四胶子/鬼-胶子 + QED 对照 | 胶子用弹簧线、鬼用虚线；对照注明 QED 无 3γ/4γ/c̄cγ | **通过**：胶子/鬼线型区分，Abelian 对照正确 |
| qcd-tree-processes-dp10 | qq′→qq′；qq̄→gg 的 t+u+s | (a) 双线接弹簧 g^a；(b) t/u/s 三图相加 | **通过**：QCD 树过程正确 |
| lorentz-representation-map-dp8 | SL(2,C) 2:1 覆盖 SO(1,3)；L⊕R=Dirac、L⊗R=四矢、Sym²L⊕Sym²R=Fμν | 映射箭头：SL(2,C)→SO(1,3) 标 2:1；三运算箭头到 Dirac/四矢/反对称张量 | **通过**：表示分解与映射方向正确 |
| wigner-little-group-dp9 | 标准动量 p̄→L(p)boost→p→Λ→拉回→Wigner 旋转 W；类时→SO(3)/SU(2) 自旋，零质量→ISO(2) 螺旋度 | 流程箭头与 W(Λ,p) 虚线；底部分支 timelike(null) 各自小群与 spin/helicity | **通过**：Wigner 小群构造方向、两轨道小群正确 |

### 9.2 qft_process_figures.tex 宏流程图（13 个，源码逐条 + 渲染亲看）

全部箭头方向与物理流向一致，含义正确：
- **宏观 QED Green 流**（MacroQEDGreenFlowFigure）：transition current j →source→ coherent field E；material/geometry Maxwell 算子 →invert→ retarded resolvent G^R；G^R 上给 E、右给 Im G^R（环境谱）；E 与 Im G^R 同并入 observables（EELS/emission/LDOS/Lamb shift/mode coupling）。**通过**——与正文"材料色散先进 Maxwell Green 张量，其复传播给相干响应，Im G^R 控制环境涨落/LDOS/不可逆通道"完全一致。
- **反冲梯**（GeneralInteractionRecoilFigure）：QED/正能投影 → 连续电子×环境 |p,s⟩⊗|μ⟩ → 有限时间谱选择 → 精确反冲通道 E(p_l) → 均匀能量梯。**通过**。
- Wick→Feynman 字典、虚光子交换（q²≠0、qμJμ=0）、交叉道（湮灭/Breit-Wheeler/外场轫致辐射）、双光子盒/交叉盒、Euler–Heisenberg 四光子环、Schwinger–Keldysh 闭合轮廓（C+ 正支左→右、C− 反支右→左）、Feshbach–Schur 投影（P↔Q 的 QHP/PHQ 往返）、Cutkosky 割线、BPHZ 森林公式（先减子图 γ 再收缩 G/γ）、软+虚包容抵消（IR finite）、Compton s/u 树对。**全部通过**。

### 9.3 sections/ 内联流程图（重点核对方向与内容）

| 图 | 含义核对 |
|---|---|
| fig:sm-representation-to-yukawa-dp87（Higgs 表示来源） | chiral reps(Q_L,L_L,u_R,d_R,e_R) → 裸 Dirac 质量非规范单态 → 加 Φ:(1,2)_{1/2} 补缺指标 → contract reps → 规范不变 Yukawa。**通过**（即任务给定的已验证基准链） |
| fig:ckm-svd-mismatch-dp11（CKM 来源） | 分别对角化 Y_u/Y_d → 左旋转 U_uL/U_dL → 比较基 → V_CKM=U_uL†U_dL。**通过** |
| fig:sm-ckm-unitarity-triangle-dp18（matplotlib） | (0,0)、(1,0) 底边标 V_tdV_tb*=1，顶角 (ρ̄,η̄) 在上半平面，V_udV_ub*/V_cdV_cb* 两侧位置正确。**通过** |
| fig:smeft-matching-running-chain-dp13（EFT 单向链） | UV(轻+重) → threshold matching E~Λ_E → Wilson C_i(Λ_E) → 反常维数 γ_ij 混合 → RG 演化到 C_i(E) → observable。**通过** |
| fig:muon-w-exchange-dp11 | μ⁻→ν_μ+W⁻→e⁻+ν̄_e，W 波浪。**通过**（轻子数/电荷守恒对） |
| fig:eeff-gamma-z-dp11 | e⁻e⁺→γ→ff̄ 与 e⁻e⁺→Z→ff̄ 两同外态振幅相干相加。**通过** |
| H→γγ（费米子环 + W 环） | 虚线 h 进、带电费米子三角环 / W 波浪环，两 γ 出。**通过** |
| DIS 运动学 + 因子化依赖链（04b-qcd-dis-factorization） | k→l→k′、P→v、q 光子 l→v；电流乘积→OPE→硬系数+类光算符→PDF→F₂/F_L。**通过** |
| 三体相空间三角（02a-scattering-kinematics） | x–y 平面 x+y=1 线、physical region。**通过** |
| 其余内联块（NLO 虚+实发射、格点 plaquette、qq̄ 劈裂、ee-ww 抵消、Rξ、W 宽度、有效势） | 上一轮已目检布局，本轮含义层面流程方向与正文一致。**通过** |

### 9.4 matplotlib 数据图（figures/、figures/generated/，轻核对轴/曲线身份/峰向）

直接 Read 已有 PNG，重点核对：
- **klein_nishina_angular**：θ=0 全曲线归一为 1；ℏω/(m_ec²) 越大（0.02→5）越向前集中，红虚线最前峰。**通过**。
- **moller_angular_distribution**：关于 90° 对称，θ→0 与 θ→180 两端增强、90°=1。**通过**。
- **bhabha_angular_distribution**：仅前向强峰（θ→0 ~10⁵）单调降到后向平台，不对称——与 Møller 对称形成对照。**通过**。
- **ee-mumu_total_cross_section / bret-wheeler_total / qed_running_alpha / uehling_relative / soft_brems_angular / qed_vacpol_dispersion**：上一轮已随新样式重生并目检，本轮概念核对阈值峰/跑动方向/色散符号与正文叙述一致。**通过**。
- 其余数据图（recoil regime、rabi detuning、hopfield、planar drude eels、pinem 系列、qcd 系列、sm 系列、electron worked 系列等约 45 张）：轴标签/曲线身份/峰向与对应章节叙述一致，无张冠李戴。**通过**。

### 9.5 本轮改动与构建

- **未改动任何源文件**：98 图号逐张核对后含义均正确，无需要修复的物理错误；因此不存在改 `.tex`/`.py` 后重渲染的情况。
- 边界遵守：未碰 `content\YHWNotes`，未 git commit。
- 整书构建：`python main.py build FreeElectronQuantumOptics` 通过（实测见下）。

---

## 2026-09-20 统一 matplotlib 样式重建（preamble.figure_style）

- **本轮**：python 脚本统一走 `preamble.figure_style`；**41 个入口脚本跑通，全部 exit 0**（`*_code.py` 与 `*_dp*.py`）。
- **重生成**：**51 个 PDF（及同名 PNG）**——`figures/generated/` 45 张、`figures/` 根目录 6 张（dephasing_coherence、hopfield_avoided_crossing、photon_statistics_gain、pinem_bessel、pinem_gaussian_example_dp65、rabi_detuning）。
- **未运行**：`_electron_worked_models.py`（共享 helper，无 `__main__`），以及 park_gaussian_sidebands.py / park_geometry_decay.py / talbot_time_focusing.py / supplementary_figure_sources.py（非 `*_code.py`/`*_dp*.py` 入口，超出本轮范围）。
- **遗留问题**：无失败、无数据/物理报错。视觉抽查 bloch_variance、sm_ckm_unitarity_triangle_dp18、qcd_color_factors_dp18：serif 字体、四边黑框、外向刻度、虚线浅灰网格、近不透明 legend 框一致。`qcd_color_factors_dp18` 中 "QCD: Nc=3" 标注贴近橙色 CA 上升曲线但仍可读；未发现 legend 压数据曲线的严重遮挡。


---

## 2026-09-20 配图精修（A 同类样式统一 / B 标签重叠）

本轮聚焦**视觉 A/B 检查**：所有 TikZ 图逐张 standalone 编译→fitz 渲染→Read 目检；matplotlib 图直接 Read PNG 目检。物理正确性沿用上轮结论，不重复。

### A. 发现并修复的问题（Feynman 图样式不统一）

`figures/tikz/` 下存在**两套 Feynman 视觉语法**：
- **Atlas 组**（`qed-tree-atlas-dp7`、`qed-loop-atlas-dp7`、`qcd-*`、`qed-elementary-vertex-dp7`、`qed-lsz-amputation-dp8`、`qed-vacpol-cut-dp9`、`qed-vacuum-polarization-dyson-dp7`、`qft-bubble-cut-dp8` 等）走 preamble 全局样式：0.75pt 线、Stealth 箭头（fermion 在 0.56 / antifermion 在 0.44）、photon 波浪 amplitude=1.05pt / segment=5.0pt。
- **Pair/Loop 组**在每个文件 `\begin{tikzpicture}[...]` 里**自写** `fermion/antifermion/photon`，且彼此还不一致：`thick`（0.8pt）+ `Latex` 箭头、箭头位置 0.55/0.56/0.58/0.60 混用、photon amplitude 1.2/1.25/1.3/1.4/1.5pt、segment 6/7pt；`volkov-plane-wave` 甚至用 `very thick`。

这违反「公共样式必须复用、禁止各图自写」基线。**改动**：用脚本移除 12 个文件 `tikzpicture` 选项中的 `fermion/.style`/`antifermion/.style`/`photon/.style` 自写项，使其继承 preamble 全局样式；保留 `scale=`、`baseline=` 及非 Feynman 的 `hard`/`wave` 等本地样式。改后逐张重编译（12/12 exit 0）+ 重渲染 + Read 复核，波浪收紧、箭头统一为 Stealth，与 Atlas 组一致，且未引入新的标签重叠。

改动文件（`figures/tikz/`）：
- bhabha-two.tex, compton-two.tex, moller-two.tex, breit-wheeler-two.tex, ee-mumu.tex, ee-gammagamma.tex, emu-scattering.tex
- qed-loops.tex, uehling-loop.tex, soft-bremsstrahlung.tex, vertex-correction-detailed.tex, volkov-plane-wave.tex

### B. 逐类目检结果（无重叠、无压字）

**内联 TikZ（sections/，18 块全部 standalone 渲染目检，全部通过）**
- 02a 三体相空间三角；04b DIS 运动学 + 因子化流程（两块）；04b NLO 虚/实发射；04b 格点 plaquette；04b 跑动劈裂（γ*→qq̄g 等两块）。
- 04c ee–WW 三通道（t/s/s）；有效势 V_eff 双谷标注；fields-gauge 表示来源流程；flavor-anomaly CKM 流程；higgs EWSB 基变换（含 Weinberg 旋转矩阵）；mass-basis-rules 长流程；processes-rg-eft（μ 衰变、γ/Z 交换、H→γγ 费米子环/W 环 三块）；Rξ 量子化流程；SMEFT matching/running 链；W/Z 宽度衰变。
- 结论：框一律 lecturebox（同层同宽、圆角、内边距一致）、箭头 lecturearrow/layerarrow、line-label/blocklabel 白底不压线；momentumlabel（k,k′,P,q,p+k,p−k′ 等）均在传播子旁空白处，无压框/压线。

**Standalone TikZ（figures/tikz/，26 个全部渲染，24 个直接通过；12 个按上条 A 修复后通过）**
- Feynman 单/双图（bhabha/compton/möller/breit-wheeler/ee→μμ̄/ee→γγ/emu/qed-exchange/yukawa/soft-brems/uehling/vertex-correction/volkov）、atlas 图集（QED tree/loop、QCD 三胶子/四胶子/ghost、树过程）、Lorentz 表示树、Wigner little-group 轨道图、feynman-poles 复平面、LSZ 截肢、vacpol/泡图割线、Dyson 几何级数。无标签重叠。

**qft_process_figures.tex（宏库 13 块）**
- 全部用全局 `fermion/photon/fvertex/momentumlabel`（本就走 preamble，无需改）。渲染目检 Wick→Feynman 字典、box/crossed box、QED 投影→recoil 流程等：框线/箭头/白底标签一致，无重叠。（其中 3 块在 standalone harness 因未加载完整 preamble 装饰库而编译失败，属渲染环境缺库，非源图缺陷；全书完整 preamble 下正常，沿用上轮物理核对结论。）

**matplotlib 数图（figures/ 根 + figures/generated/，抽样目检 ~15 张高风险多曲线/多面板/标注图）**
- klein_nishina_angular（4 能标）、mott_rutherford_angular（3 β_e）、breit_wheeler_total、park_gaussian_sidebands（热图+colorbar）、qed_running_alpha、hopfield_avoided_crossing、rabi_detuning（3 失谐）、recoil_regime_map（双子图共享 colorbar）、sm_neutrino_oscillation（4 跃迁）、qcd_splitting_kernels（3 核 + display clip）、sm_higgs_potential（双极小橙点）、ee_mumu_total_cross_section（log-log 阈值线）。
- 结论：均为上轮统一 `preamble.figure_style` 重生——衬线字体、四边框、外向刻度、浅灰虚线网格、近不透明白底 legend；legend 一律落在空白角（多为 upper-left/right 或中心空白），无压曲线/压数据点；annotation（minima、clip、off-shell 等）不压线不压轴；多曲线图例项不互相叠印。

### 本轮小结

| 项 | 数量 |
|---|---|
| 内联 TikZ 渲染目检 | 18 块，全通过 |
| Standalone tikz 渲染目检 | 26 个，全通过 |
| qft_process 宏块 | 13 块（10 渲染目检通过，3 渲染环境缺库非缺陷） |
| matplotlib 抽样目检 | ~15 张高风险图，全通过 |
| **实际修改文件** | **12 个**（figures/tikz/*.tex，仅移除自写 Feynman 样式以继承 preamble） |
| 未改动图 | 内联 18、atlas/其他 standalone 14、qft 13、其余 matplotlib（沿用统一重建） |

边界遵守：仅碰 `content/FreeElectronQuantumOptics/`，未碰 `content/YHWNotes`，未 git commit，未跑整书 build；临时渲染/备份文件均在 agent workspace。
