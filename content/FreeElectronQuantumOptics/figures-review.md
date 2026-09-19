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
