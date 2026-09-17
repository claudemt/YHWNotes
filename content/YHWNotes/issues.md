# YHWNotes — Issues

YHWNotes 已作为独立综合笔记接入统一出版工程。R08 只完成章节规范、公共样式迁移和少量机械规范化，正文尚未达到 `SKILL.md` 的最终出版标准。

## P0：数学与物理主线
- `ch01` 中相对论逆平方势、Lorentz 群、非线性振动和刚体动力学目前更像独立专题笔记，后续需要在每个 section 开头补足问题动机、定义域和从一般结构到具体模型的单向推导。
- 电动力学部分包含静电网络、等离子体、辐射、散射、STF 多极、薄膜和波导，覆盖面很广，但部分专题直接从特殊几何或已知公式开始。后续应逐节检查 Maxwell 方程、Green 函数、边界条件和介质本构是否先于具体模型建立。
- 弱相互作用 Bose/Fermi 气体和 Ising 模型需要与 `AdvancedPhysics` 的严格版本交叉核对，避免两本书出现彼此不一致的公式、符号或假设。
- Green 函数、无穷积分、参数估计、特殊函数等数学工具必须从统一算子/概率模型出发，避免只堆积公式表。

## P1：结构与叙述
- 原稿仍保留较多 `subsubsection`、短标题、`显然/不难证明` 等跳步语言；R08 已把旧工程依赖 preamble 自动拆分的 `equation*` 显式迁为 `align*`，后续还需逐式检查真正的对齐点。后续按 Skill 逐节改成连续正文，并把真正复杂计算移入 `Derivation`。
- 所有新符号首次出现位置需要重新审计；不同专题之间的 `I, D, M, k, a` 等常用符号尤其容易发生跨章复用。
- 原稿的 section 编号原先跨 chapter 手动连续；R08 已恢复标准 `chapter → section → subsection` 编号，后续不得再用 `\setcounter` 模拟旧编号。

## P2：图形与文件
- 原图和图源已经随 section 模块保留，但 27 个 Python 脚本需要继续统一到根目录 `preamble.py`；本轮已迁移 import 层，后续逐图检查 legend、字体、裁切和物理标注。
- TikZ 允许保留 YHWNotes 专用 style，但基础字号、线宽和箭头视觉应与公共 `preamble.tex` 一致。
- 旧的中文 label 和非语义化 label 尚未全量改名；后续应统一为 `fig:/eq:/sec:` + 英文语义名。

## R08 回归状态
- 统一公共 preamble 后，YHWNotes 已完成 265 页 XeLaTeX 多遍回归；当前 0 undefined reference、0 duplicate label、0 hard LaTeX error。
- 仍有 54 个 overfull box，主要来自旧稿的长公式。这些位置必须后续逐式改用 `align/aligned/split/multlined`，禁止用整体缩放掩盖。
- 旧工程依赖隐式 `equation* -> split` 魔改的公式已经显式迁移；其中 1659 个旧无编号显示环境已按源码语义重构，后续继续核对每一个 `&` 的真正数学对齐点。
- 27 个 Python 图脚本已经全部迁到根目录唯一 `preamble.py` 并逐个执行通过；旧脚本中把 legend 推到图外的调用已改为公共图内 legend 规则。
- 正式正文仍有 85 个 `\subsubsection`、5 个裸 `\eqref`、36 个裸 `\ref` 和 21 处“显然/不难证明/容易得到”等高风险跳步语言，作为下一轮语义精修的优先搜索项。
