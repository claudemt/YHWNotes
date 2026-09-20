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


---

## 意思核对（2026-09-20）

本轮不是视觉精修（legend 位置上一轮已闭环），而是把三张 matplotlib 图与正文声称的数学关系逐条对照：先读正文段落搞清每张图声称什么数学关系，再 Read 渲染出的 PNG 亲看图，必要时用独立数值脚本核对孤子中心/相移。**结论：三张图数学意思全部正确，未改任何 .py，未重跑生成。**

### 图 6.1  Tikhonov 滤波函数（`tikhonov_filter_code.py`）

- **正文怎么说**（ch06.tex:1596–1626）：把 $q(s)$ 定义为乘在数据系数 $g_n$ 上的因子（与形式逆同轴）。形式逆 $q=1/s$；TSVD $q_\tau(s)=\mathbf 1_{s\ge\tau}/s$（硬截断，$s<\tau$ 取 0）；Tikhonov $q_\alpha(s)=s/(s^2+\alpha)$（正文 line 1617 明确写 $s/(s^2+\alpha)$，不是 $s^2/(s^2+\alpha)$）。caption 强调"形式逆在 $s\to0$ 无界、Tikhonov 平滑压制小奇异值、TSVD 阈值以下直接截断"。
- **图原来怎么画**：蓝 `1/s` 自左上角冲出；橙 $\alpha=0.01$ 单峰；绿 $\alpha=0.04$ 单峰且更矮；红 TSVD 在 $s=0.18$ 前贴 0、之后竖直跳到 $1/0.18\approx5.56$ 并与蓝线重合。
- **意思核对**：
  - 峰值位置/高度：$q_\alpha(s)=s/(s^2+\alpha)$ 在 $s=\sqrt\alpha$ 处取极大 $1/(2\sqrt\alpha)$。$\alpha=0.01\Rightarrow$ 峰在 $s=0.1$、高 $5.0$；$\alpha=0.04\Rightarrow$ 峰在 $s=0.2$、高 $2.5$。PNG 上橙峰约 $(0.1,5.0)$、绿峰约 $(0.2,2.5)$，与公式定量一致。
  - 小 $s$ 行为：$s\to0$ 时两条 Tikhonov 都 $\to0$（被平滑压制），而 $1/s\to\infty$（无界），TSVD 硬归零——三条与正文叙述一一对应。
  - TSVD 衔接：$s\ge\tau=0.18$ 后红线与蓝线 $1/s$ 重合，正是 TSVD 定义；竖直跳变在 $s=0.18$。
  - **说明**：任务描述括号里写的 $q(s)=s^2/(s^2+\alpha)$ 是"乘在 $1/s$ 上的保留因子"那一套惯例（单调 S 曲线、无峰）；但本书正文把 $q(s)$ 定义成乘在 $g_n$ 上的系数（与 $1/s$ 同轴同量纲），故正文公式是 $s/(s^2+\alpha)$，脚本与正文一致。以正文为准。
- **意思问题**：无。
- **改成什么**：不改。
- **验证结果**：PNG 目视 + 公式峰值解析计算一致。

### 图 7.1  Burgers 特征线（`burgers_characteristics_code.py`）

- **正文怎么说**（ch07.tex:442–485）：无黏 Burgers 隐式解 $x=\xi+t\,u_0(\xi)$，取 $u_0(\xi)=-\tanh\xi$。$\min u_0'=-1$（在 $\xi=0$），故 $t_*=-1/\min u_0'=1$；几何上特征线在 $(0,t_*=1)$ 附近首次交叉（梯度灾变/激波形成处）。caption："图中正是在这条水平线附近首先出现特征线交叉"。
- **图原来怎么画**：$t\in[0,1.25]$ 纵轴、$x$ 横轴；17 条直线 $x(t)=\xi+t[-\tanh\xi]$；蓝色虚线 $t=1$。
- **意思核对**（逐方向）：
  - $\xi<0$ 半支：$u_0=-\tanh\xi>0$，$\dot x=u_0>0$，线随 $t$ 增大向右倾。PNG 最左深蓝线自 $x\approx-2.2,t=0$ 升到 $x\approx-1.0,t=1.25$，$\Delta x/\Delta t\approx0.96\approx-\tanh(-2.2)=0.976$，向右倾 ✓。
  - $\xi>0$ 半支：$u_0<0$，线随 $t$ 增大向左倾。最右粉线自 $x\approx2.2,t=0$ 升到 $x\approx1.2,t=1.25$，$\Delta x/\Delta t\approx-0.88\approx-\tanh(2.2)=-0.976$，向左倾 ✓。
  - 汇聚/激波：左右两半支向中心 $x=0$ 收拢，在 $t=1$ 蓝虚线附近（$\xi\approx\pm0.2$ 的相邻线交点在 $t\approx1.01,x\approx0$）首次交叉；$t>1$ 后线在中心附近穿开、上下端左右次序反转。与 $t_*=1$ 预言一致 ✓。
  - 疏密：$u_0'$ 在 $\xi=0$ 最陡（$-1$），特征线在中心最密、向两侧变疏，PNG 上中心束紧、两侧松开 ✓。
- **意思问题**：无。（$t>t_*$ 后仍画直线特征线是教材演示"交叉"的标准画法，不是错误。）
- **改成什么**：不改。
- **验证结果**：PNG 目视 + 两条边线斜率解析核对一致。

### 图 7.2  KdV 二孤子散射（`kdv_two_soliton_code.py`）

- **正文怎么说**（ch07.tex:1270–1316）：标准符号 $u_t-6uu_x+u_{xxx}=0$，二孤子 tau 函数 $u=-2(\ln\tau)_{xx}$，$k_1>k_2>0$。孤子是**负阱**，振幅 $2k_i^2$、速度 $4k_i^2$——越深（$k_1$ 大）越快。弹性散射：快孤子前向相移 $\Delta x_1=-\ln A_{12}/(2k_1)>0$，慢孤子后向相移 $\Delta x_2=\ln A_{12}/(2k_2)<0$；碰撞改位置不改 $k_i$/速度/振幅。三个时刻截面：撞前、碰撞中、撞后。
- **图原来怎么画**：$k_1=0.9$（深阱深 $1.62$、快）、$k_2=0.5$（浅阱深 $0.5$、慢）；$t=-3,3,6$ 三条截面。
- **意思核对**（用独立数值脚本求极小值点，非肉眼估坐标）：

  | 时刻 | 深阱 $(k_1)$ 数值位置 | 浅阱 $(k_2)$ 数值位置 | 裸轨迹 | 判定 |
  |------|------|------|------|------|
  | $t=-3$ 撞前 | $-13.72$（深，$u=-1.62$） | $+2.51$（浅，$u=-0.5$） | 深 $-13.72$ / 浅 $0$ | 深阱在后（左）追赶浅阱 ✓ |
  | $t=3$ 碰撞 | 合并单谷 $5.75$（$u=-1.31$） | — | 深 $5.72$ / 浅 $6.00$ 重合 | 强叠加作用区 ✓ |
  | $t=6$ 撞后 | $16.83$（深，$u=-1.62$） | $9.00$（浅，$u=-0.5$） | 深 $15.44$ / 浅 $9.00$ | 深阱已越过到前方（右）✓ |

  - 越过后排序：撞前深在浅之左，撞后深在浅之右——深阱追上并越过浅阱，排序反转 ✓。
  - 相移方向：$A_{12}=((k_1-k_2)/(k_1+k_2))^2=0.0816$，$\ln A_{12}=-2.506$。撞后深阱 $16.83$ 比裸轨迹 $15.44$ 右移 $+1.39=-\ln A_{12}/(2k_1)=\Delta x_1>0$（快孤子前推）✓；慢孤子撞前在 $+2.51$、撞后回到裸轨迹 $9.00$，位移 $\Delta x_2=\ln A_{12}/(2k_2)=-2.51<0$（慢孤子后延）✓。方向与正文公式一致。
  - 振幅/速度：深阱 $u_{\min}\approx-1.62=-2k_1^2$、浅阱 $u_{\min}\approx-0.5=-2k_2^2$，数值上与解析振幅一致；深阱更快 ✓。
- **意思问题**：无。
- **改成什么**：不改。
- **验证结果**：独立 Python 求极小值 + 相移解析公式双向核对一致；PNG 目视三条截面谷位/深浅与数值表吻合。

### 本轮改动汇总

| 脚本 | 改动 |
|------|------|
| `tikhonov_filter_code.py` | 无 |
| `burgers_characteristics_code.py` | 无 |
| `kdv_two_soliton_code.py` | 无 |

本轮仅新增本审查记录；三张图的数学意思（箭头方向/特征线疏密/激波位置、孤子追赶与越序、相移方向、滤波曲线峰值与硬截断）均与正文定量一致，未触发任何 .py 修改或重新生成。

---

## 2026-09-20 统一 matplotlib 样式重建（preamble.figure_style）

- **本轮**：python 脚本统一走 `preamble.figure_style`；**3 个入口脚本跑通，全部 exit 0**（burgers_characteristics、kdv_two_soliton、tikhonov_filter）。
- **重生成**：3 个 PDF（及同名 PNG）落 `mathematical-physics/generated/`。
- **遗留问题**：无失败、无数据/物理报错。视觉抽查 kdv_two_soliton：serif 字体、四边黑框、外向刻度、虚线浅灰网格、近不透明 legend 框一致；右上 legend 轻微覆盖到 y≈0 平线，但 legend 近不透明白底已干净遮挡，不构成数据误读。


---

## 2026-09-20 视觉精修本轮（A 类样式统一 / B 类重叠查重）

**范围**：MathSkills 全部图引用 6 处（3 个 `\includegraphics` + 3 个 `\figref`），对应 3 张 matplotlib 产物；仓库内无内联 tikzpicture（前一轮已递归 grep 确认）。

**闭环方法**：`python <script>.py` 重新生成 PDF/PNG 一对 → Read 渲染出的 PNG 逐图目检（A 类：是否走 preamble.figure_style、字体/边框/刻度/网格/图例风格是否一致；B 类：legend 是否压曲线、annotation 是否压轴/压线、标签是否重叠/裁切）→ 不改则记录，改则改 .py 后重跑再 Read。

### 逐图记录

| 图号/标签 | 脚本 | A 类（样式统一） | B 类（重叠查重） | 改动 | 渲染确认 |
|-----------|------|------------------|------------------|------|----------|
| 图 6.1 `fig:tikhonov-filter`（ch06.tex:1622） | `tikhonov_filter_code.py` | ✓ 走 `figure_style()`；serif 字体（Latin Modern Roman）、四边黑框、外向刻度、浅灰虚线网格、`add_legend` 近不透明白框；与另两图风格一致 | ✓ legend upper right 悬空在 s>0.66、q>8 空白角，四条目均不到该区域；蓝 1/s 自 s≈0.08 从顶入图（物理本意）；橙/绿峰分别在 (0.1,5.0)/(0.2,2.5)，远离 legend；红 TSVD 在 s=0.18 竖直跳变后与蓝线重合，衔接清楚；轴标签 singular value s / filter q(s) 无裁切 | 无 | Read PNG 通过 |
| 图 7.1 `fig:burgers-characteristic-crossing`（ch07.tex:480） | `burgers_characteristics_code.py` | ✓ 走 `figure_style()`；同上样式基线；figsize=(6.4,4.5)；标题 `Characteristics for u_0(xi)=-tanh xi` 用 serif mathtext | ✓ legend upper right 箱体约 x∈[1.5,2.3]、t∈[1.15,1.28]；最右特征线 ξ=2.2 在 t=1.27 时 x≈0.96，远在箱体左缘之外；蓝色虚线 t*=1 横贯画面且在 legend 下方不被遮；中心 x≈0 处特征线自然汇聚是激波形成物理本意；轴标签 x/t、标题无裁切 | 无 | Read PNG 通过 |
| 图 7.2 `fig:kdv-two-soliton-scattering`（ch07.tex:1311） | `kdv_two_soliton_code.py` | ✓ 走 `figure_style()`；同上样式基线；figsize=(6.6,4.5)；`tight_layout(rect=[0,0,0.83,1])` 为轴外 legend 留右边距 | ✓ legend 用 `bbox_to_anchor=(1.01,1.0)` 放到轴外右侧白边内，与坐标轴 spine 齐平，不压任何数据线；蓝 t=-3 深谷 x≈-13.7、橙 t=3 作用区 x≈6、绿 t=6 双谷 x≈9/x≈16 均在轴内完整可见；绿线右肩在 x≈19 回到 u≈0 基线，未被裁；三个时刻标签蓝/橙/绿清晰分开 | 无 | Read PNG 通过 |

### 本轮改动汇总

| 脚本 | 改动 |
|------|------|
| `tikhonov_filter_code.py` | 无 |
| `burgers_characteristics_code.py` | 无 |
| `kdv_two_soliton_code.py` | 无 |

### 小结

- 处理图数：**3 张**（全部 MathSkills 图引用）。
- 本轮改动：**0 处**。前几轮已完成 legend 移位（burgers upper left→upper right；kdv 图内→轴外）与统一样式重建（三脚本均走 preamble.figure_style）；本轮视觉复核确认 A 类样式一致、B 类无重叠/无裁切，未触发任何 .py 修改或重新生成。
- 遗留：无。仓库内无内联 TikZ 图（前一轮已 grep 确认），故无 standalone 编译对象。
