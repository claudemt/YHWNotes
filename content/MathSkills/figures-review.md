# MathSkills 配图视觉审查记录

审查对象：三张 matplotlib 图（脚本在 `figures/mathematical-physics/code/`，产物在 `figures/mathematical-physics/generated/` 的 pdf/png 一对）。

审查方法（本轮，视觉闭环）：`python <script>.py` 重新生成 → 直接 Read 渲染出的 PNG 逐图目检 → 量坐标判断是否压曲线 → 改 `.py` → 再生成再 Read，直到干净。**不看渲染图不改坐标。**

| 图号 | 脚本 | 产物 | 主题 |
|------|------|------|------|
| 图 6.1 | `tikhonov_filter_code.py` | `tikhonov_filter.{pdf,png}` | 形式逆 / Tikhonov / TSVD 滤波函数比较 |
| 图 7.1 | `burgers_characteristics_code.py` | `burgers_characteristics.{pdf,png}` | Burgers 特征线（$u_0(\xi)=-\tanh\xi$） |
| 图 7.2 | `kdv_two_soliton_code.py` | `kdv_two_soliton.{pdf,png}` | KdV 二孤子散射（三个时刻截面） |

## 0. 基础设施（前一轮已完成）

- 仓库根 `preamble.py` 提供 `figure_style / polish_axes / add_legend / save_pdf_png_pair`；三个脚本 `ROOT = parents[5]` 指向仓库根。本轮未再动基础设施。

## 1. 图 6.1  Tikhonov 滤波函数（`tikhonov_filter_code.py`）

**本轮目检结论：通过，未改动。**

- legend 位于右上角 `loc='upper right'`，四条目在 $s>0.6$ 处均已回落到 $q(s)<2$，legend 箱体约 $q(s)\in[8.4,11.8]$、$s\in[0.66,0.98]$，**完全悬空**，不压任何曲线。
- 形式逆 $1/s$ 蓝线在 $s\to0$ 处冲出上边界（$s\approx0.08$ 从顶入图），属物理本意；TSVD 红竖线在 $s=\tau=0.18$ 硬截断，$s\ge\tau$ 后与 $1/s$ 重合（TSVD 定义使然），衔接清楚。
- 橙 $\alpha=0.01$ 峰值 $\approx5.0$、绿 $\alpha=0.04$ 峰值 $\approx2.5$，均远离右上角 legend；四条目颜色（蓝/橙/绿/红）清晰区分，公式 label $1/s,\alpha,\tau$ 渲染正常。
- 轴标签 `singular value $s$` / `filter $q(s)$`、刻度均无裁切（`tight_layout`）；无标题、无 annotation。

## 2. 图 7.1  Burgers 特征线（`burgers_characteristics_code.py`）

**本轮目检结论：前一轮"通过、未改动"判断有误——legend 实际压住左起第一条特征线，已修复。**

- **问题**：原 `add_legend(ax, loc='upper left')`。目检 PNG：legend 白框约落在 $x\in[-2.3,-1.0]$、$t\in[1.15,1.3]$。最左侧特征线 $\xi=-2.2$，$u_0=-\tanh(-2.2)=+0.976$，$x(t)=-2.2+0.976\,t$；在 legend 竖向高度内它位于 $t=1.15\Rightarrow x\approx-1.08$，$t=1.30\Rightarrow x\approx-0.93$，**正穿过 legend 箱体右缘，被不透明白框遮去一段**。上一轮记录"legend 右缘约 $x\approx-1.4$、不相交"是没看图的估坐标，与渲染不符。
- **改法**：`add_legend(ax, loc='upper left')` → `loc='upper right'`。右上区 $x>1.5,\ t>1.15$ 为空：最右侧特征线 $\xi=2.2$ 在该高度仅到 $x\approx1.08\to0.93$，在箱体左缘之外。
- **改后复验（Read PNG）**：legend 移到右上，箱体约 $x\in[1.5,2.4]$，最右粉线不再入框；左起深蓝线完整露出、不再被遮；$t_*=1$ 蓝色虚线横贯画面且在 legend 下方，不被遮。中心 $(0,t\approx1.25)$ 处特征线自然汇聚是激波形成的物理本意，非缺陷。轴标签 $x,t$、标题无裁切。

## 3. 图 7.2  KdV 二孤子散射（`kdv_two_soliton_code.py`）

**本轮目检结论：前一轮"upper left + xlim=-21"仍压曲线——蓝色 $t=-3$ 孤子左肩穿过 legend 箱体，已改为轴外 legend。**

- **问题**：上一轮把 legend 从 `lower left` 挪到 `upper left` 并把左边界外推到 $-21$。本轮目检 PNG：legend 箱体仍约落在 $x\in[-20,-12.5]$、$u\in[-0.35,0.05]$。蓝色 $t=-3$ 曲线在 $x\lesssim-15.5$ 处从 $u\approx0$ 陡降，在 $x\approx-14.2$ 处穿过 $u=-0.35$，**即蓝色左肩下降沿从箱体下缘进入 legend 区**；上一轮称"左肩 $u\approx-0.5$ 在下缘之下、无重叠"同样与渲染不符。
- **改法**：图内四角均被孤子占据（左下蓝谷 $x\approx-13.7$、右下绿谷 $x\approx16$、左上蓝肩、右上绿肩擦边），无干净图内角。改为把 legend 放到轴外右侧：
  - `add_legend(ax, loc='upper left', bbox_to_anchor=(1.01, 1.0), borderaxespad=0.0)`
  - `fig.tight_layout(rect=[0, 0, 0.83, 1])` 给右侧 legend 留出画布宽度。
- **改后复验（Read PNG）**：legend 落在轴外右侧白边内，与坐标轴 spine 齐平、不压任何数据线；三条孤子在轴内全部完整可见——蓝 $t=-3$ 深谷 $x\approx-13.7$、橙 $t=3$ 相互作用区 $x\approx6$、绿 $t=6$ 双谷 $x\approx9$ 与 $x\approx16$，均无遮挡；三个时刻标签蓝/橙/绿清晰分开。轴标签 $u(x,t)$、$x$、标题 `KdV two-soliton scattering` 无裁切。

## 4. 本轮改动汇总

| 脚本 | 改动 |
|------|------|
| `burgers_characteristics_code.py` | legend `loc='upper left'` → `'upper right'` |
| `kdv_two_soliton_code.py` | legend 改轴外：`bbox_to_anchor=(1.01,1.0), borderaxespad=0.0`；`tight_layout(rect=[0,0,0.83,1])` |
| `tikhonov_filter_code.py` | 无（已干净） |

## 5. 旁注（非本次任务范围，仅记录）

- 正文交叉引用 `figreffig:tikhonov-filter` 之类字面量属 LaTeX 宏/引用问题，与三张 matplotlib 图本身无关，本轮不处理。


---

## 6. TikZ 内联图专项审计（本轮，A/B 类标准）

**任务**：复查 content/MathSkills/ 各章节 .tex 内联的 	ikzpicture，按 A 类（标注标签几何图：标签不压线、留 5-8pt）、B 类（流程框+箭头：框方正、网格对齐、箭头标签白底不压框）逐图 standalone 编译→渲染→Read 目检→修→复验。

**结论：MathSkills 不存在任何内联 TikZ 图，A/B 类对象为空，本轮无图可修。**

证据（均为本轮实际执行，非推断）：

| 检查 | 命令/方式 | 结果 |
|------|-----------|------|
| 顶层章节内联图 | `Select-String -Path content\MathSkills\*.tex -Pattern 'begin\{tikzpicture\}'` | **0 命中** |
| 全书递归（含 frontmatter、settings、main） | Grep 	ikzpicture over content/MathSkills（29 个 .tex） | **0 命中** |
| 其他 TikZ 环境 | 	ikzcd / \begin{tikz | **0 命中** |
| 图引用 | 全文 igures 关键字 | 仅 3 处 \includegraphics，均指向 matplotlib 产物（见下） |
| igures/tikz/{differential-geometry,mathematical-statistics,sturm-liouville}/ | 列目录 | **空目录** |
| igures/code/{differential-geometry,mathematical-statistics,sturm-liouville}/ | 列目录 | **空目录** |

MathSkills 实际图形资产（非 TikZ，不属本轮 A/B 审查范围）：

| 位置 | 文件 | 类型 |
|------|------|------|
| ch06.tex:1624 | igures/mathematical-physics/generated/tikhonov_filter.pdf | matplotlib |
| ch07.tex:482 | igures/mathematical-physics/generated/burgers_characteristics.pdf | matplotlib |
| ch07.tex:1313 | igures/mathematical-physics/generated/kdv_two_soliton.pdf | matplotlib |

> 说明：本轮指令的描述（"MathSkills 的 TikZ 图内联在各章节 .tex、无独立 figures 子目录"）与本仓库现状不符——MathSkills 既无内联 tikzpicture，又确实存在（但为空的）igures/tikz/ 子目录。该描述更贴合同仓库的 GroupTheory / AdvancedPhysics / FreeElectronQuantumOptics（这三本书确有内联 tikzpicture，本轮未触碰）。按任务边界，未改动 content/YHWNotes/，未做 git commit。

**改动文件**：无（章节 .tex 零改动）。**Standalone 编译迭代**：无对象，未生成临时 fig.pdf/fig.png。
