# 叙述风格与重构方案

## A. 统一叙述规范（原 LECTURE_STYLE.md）

# YHWNotes 讲义统一叙述规范

## 0. 总原则

这套讲义的目标不是把公式尽可能多地写下来，而是让读者能够沿着一条稳定的物理链条完成以下过程：

> 观察现象 -> 提出模型 -> 明确假设 -> 建立方程 -> 得到可检查的闭式结果 -> 取近似或极限 -> 用实例解释结果 -> 说明适用范围。

全库统一的是这条推理节奏，而不是每章的篇幅、公式数量或数学技巧。不同主题可以使用不同语言，但都应回答同一组问题：

1. 我们要解释什么物理现象？
2. 为什么选择这个模型？
3. 哪些量是输入，哪些量是未知量，哪些量是可观测量？
4. 近似参数是什么？近似在哪一步进入？
5. 闭式结果说明了什么，而不是只说明“算出来了什么”？
6. 结果在哪些极限下退化为熟知结论？
7. 这个模型什么时候失效？

## 1. 每章的固定骨架

每章开头尽量按以下顺序组织，篇幅可以根据主题压缩：

### 1.1 物理动机

用一段话说明：

- 研究对象是什么；
- 它来自哪个实验、现象或理论问题；
- 本章最终想得到什么可计算结果；
- 结果会在哪些后续问题中使用。

示例句式：

> 本章研究的是……。困难在于……。在……近似下，问题可以化为……。我们将先建立……，再求出……，最后用……极限检查结果。

不要从定义或公式直接开始，也不要只写“下面讨论某某方程”。

### 1.2 预备知识与路线图

只列出本章真正会用到的工具，并说明用途：

- 作用量或守恒量：用来消去时间或降低阶数；
- Green 函数：用来把点源响应叠加成一般源的解；
- VSH：用来分离角向自由度；
- ABCD 矩阵：用来把连续光学系统压缩为线性变换；
- Bethe 变分自由能：用来在局部概率上求热力学平衡。

路线图最好不超过四句。路线图不是目录重复，而是告诉读者每一节在整个问题中承担什么作用。

### 1.3 模型、约定与适用范围

在第一次出现主方程之前，集中说明：

- 坐标系、符号约定、时间/频率约定；
- 单位制；
- 边界条件与初始条件；
- 材料、几何、对称性假设；
- 小参数及其量级；
- 忽略哪些效应，以及忽略的物理理由。

每个近似都写成“参数 + 条件 + 后果”的形式：

> 设 \(\epsilon\ll1\)。我们保留 \(O(1)\) 与 \(O(\epsilon)\) 项，舍弃 \(O(\epsilon^2)\) 项；因此该结果只适用于……，并不描述……。

### 1.4 基准模型

先给出最简单、最可检查的情形。基准模型的作用是：

- 固定符号；
- 给出尺度；
- 让读者先看到问题的物理结构；
- 为后面的修正提供比较对象。

例如：

- 力学先给无扰动轨道，再加相对论修正；
- 电磁学先给静态或偶极场，再进入辐射；
- 光学先给各向同性介质，再进入各向异性或双各向异性；
- 统计力学先给无场或高温极限，再引入相互作用和临界性。

### 1.5 核心推导

核心推导不追求逐行展开，但必须显式交代每个关键转折：

1. 从哪一个方程出发；
2. 采用了什么代换或守恒量；
3. 为什么可以分离变量或截断；
4. 中间结果如何导向下一个公式；
5. 闭式结果的分支、定义域和积分常数是什么。

“代入可得”“整理得”“不难证明”“显然”“解得”只能用于真正不影响理解的局部代数。凡是改变物理结构的步骤，都至少补一句原因。

### 1.6 结果解释

每个核心公式后至少回答一个问题：

- 它控制哪个可观测量？
- 哪个参数决定共振、衰减、发散、临界或截止？
- 公式中的每一项分别来自哪个物理机制？
- 符号改变时，物理图像如何改变？

公式不是段落终点，而是物理解释的起点。

### 1.7 极限与近似模型

每节至少安排两个检查：

- 一个熟知极限，例如 \(k\to0\)、\(B\to0\)、\(q\to2\)、\(T\to\infty\)；
- 一个非平凡极限，例如临界点、共振、远场、碰撞、截止或强耦合边界。

说明“精确模型”和“近似模型”的关系：

> 精确式保留了……；当……时，它退化为……。近似式的误差阶为……，所以它只能用于……。

### 1.8 实例与总结

每个主要章节至少有一个完整实例。实例必须包含：

1. 参数和物理场景；
2. 要求解的问题；
3. 代入闭式公式的过程；
4. 数值或量纲检查；
5. 结果的物理解释；
6. 与基准模型的比较。

章节结尾用三到五句话总结：

- 本章建立了什么；
- 最重要的闭式结果是什么；
- 哪个极限最值得记住；
- 下一章接着解决什么问题。

## 2. 公式段落的统一写法

一组公式建议使用以下五步：

### 2.1 目标句

先说要算什么：

> 现在求远场能流，而不是先求完整近场。

### 2.2 输入句

指出使用的方程和边界条件：

> 代入时谐 Maxwell 方程，并取源外区域的 outgoing 边界条件。

### 2.3 关键步骤句

说明最重要的变换：

> 用 VSH 的角向正交性消去不同 \((l,m)\) 之间的交叉项。

### 2.4 结果句

给出闭式公式，并标明条件：

> 因而在 \(kr\gg1\) 时，得到……

### 2.5 解释与检查句

说明尺度、极限和物理意义：

> 该式显示功率由 \(1/r^2\) 能流乘以球面积抵消，因而与观察半径无关；令 \(l=1\) 即退化为偶极辐射。

## 3. 近似模型的统一记账

全库采用“近似台账”，任何一节只要引入小参数，就在附近明确写出：

| 项目 | 必须说明 |
|---|---|
| 小参数 | 例如 \(ka\)、\(\epsilon\)、\(1/\gamma\)、\(k\lambda_D\) |
| 物理条件 | 长波、弱非线性、稀薄、远场、低温等 |
| 保留阶数 | \(O(1)\)、\(O(\epsilon)\)、\(O((ka)^3)\) |
| 舍弃项 | 明确指出被舍弃项及原因 |
| 适用范围 | 参数区间、边界条件、是否靠近奇异点 |
| 检查方式 | 量纲、极限、守恒、数值或与标准结果比较 |

特别注意：不要把“\(\zeta=O(\epsilon)\)”和“公式中删除 \(\zeta/\epsilon\)”混为一谈。前者是阶数声明，后者会改变物理阻尼的实际大小。正文应区分“形式阶数参数”和“物理参数”。

## 4. 各学科的专用叙事骨架

### 4.1 力学

统一采用：

> 几何与势能 -> 守恒量 -> 一维有效运动 -> 轨道/相图 -> 闭式解 -> 极限与稳定性 -> 实例。

必须交代：

- 角度零点和积分常数；
- 物理解域；
- 有限近日点、渐近线、碰撞点或转向点；
- 稳定平衡与不稳定平衡的区别；
- “精确初值是平衡点”与“异宿/同宿轨道”不能混写。

力学实例不要只报数值，应先说明它属于哪一类运动，再解释参数改变会导致什么轨道拓扑变化。

### 4.2 电动力学

统一采用：

> 源与约定 -> Maxwell 方程 -> 对称性/模态分解 -> 场的闭式表达 -> 能流或辐射功率 -> 多极/远场近似 -> 极限。

每次进入远场、散射或辐射时，说明：

- 为什么只保留 \(1/r\) 项；
- \(E\)、\(H\) 的横向关系；
- 功率如何由 Poynting 向量得到；
- 模式系数如何对应电偶极、磁偶极和更高多极矩。

不要把“场的展开”“系数的求法”“功率公式”混成一段；它们分别回答表示、求解、观测三个问题。

### 4.3 光学

统一采用：

> 几何与材料 -> 本征波/传播方向 -> 边界条件 -> 振幅系数 -> 能量与互易关系 -> 极限/器件实例。

对于各向异性介质，先解释 \(D\)、\(E\)、\(S\)、波矢之间的几何关系，再给折射率和振幅公式。数值表后必须检查：

- 反射率与透射率的能量守恒；
- 互易或 Stokes 关系；
- 各向同性、正入射、轴向传播等极限。

Fourier optics 和 Matrix optics 要明确分工：

- Fourier optics 解释“场分布如何变成频谱、空间滤波如何工作”；
- Matrix optics 解释“光线和 Gaussian beam 参数如何经过光具组变换”。

两者在 4f 系统处交叉引用，不要分别讲成互不相干的公式集合。

### 4.4 统计力学

统一采用：

> 微观状态 -> 配分函数/自由能 -> 变分或求和 -> 序参量 -> 稳定性/临界性 -> 热力学量 -> 极限。

每个近似模型必须说明它保留和丢弃了什么关联：

- Bethe：树图上保留局部关联；
- Bragg-Williams：因子化并忽略关联；
- 平均场：以自洽有效场代替邻居涨落。

临界现象不能只列出指数。至少展示一条链：

> 自洽方程 -> 线性系数变号 -> 响应函数发散 -> 序参量非解析行为。

### 4.5 数学工具

数学工具章节必须从物理问题开头，而不是从恒等式开头。每组公式说明：

- 它服务于哪个章节；
- 变换约定和分支是什么；
- 适用域是什么；
- 可以用哪个低阶或数值例子检查。

推荐顺序：

> 物理需求 -> 数学对象 -> 恒等式/闭式 -> 推导或引用 -> 数值检查 -> 在正文中的使用位置。

## 5. 统一例题体系

全库例题分成三种，标题中明确类型：

### 类型 A：基准例

展示最简单极限，固定符号和尺度。

### 类型 B：机制例

突出一个新物理机制，例如辐射阻尼、色散、各向异性、关联或临界涨落。

### 类型 C：边界例

展示近似失效、分支切换、共振、碰撞、截止或临界点。

一个完整例题采用：

> 场景 -> 参数 -> 目标 -> 公式 -> 代入 -> 检查 -> 解释。

禁止只给“代入可得 \(x=...\)”而没有说明这个数值是否合理。

## 6. 统一语言风格

### 6.1 推荐用语

- “这里的目标是……”
- “这一近似把……忽略，因此只适用于……”
- “该项来自……”
- “用……代换后，问题变成……”
- “在……极限下，式子退化为……”
- “这说明……”
- “这一结果与……守恒/对称性一致。”

### 6.2 谨慎使用

- “显然”
- “不难证明”
- “易知”
- “容易得到”
- “解得”
- “综合以上”

这些词不是禁用，而是必须在后面补充“为什么这一步不会改变物理结构”。例如：

> 由树的无环性，联合概率可按父子条件概率分解；代入边缘化关系后得到……

比“显然可分解”更好。

### 6.3 术语一致性

同一物理量在全章保持一个名字和一个符号。若必须切换无量纲变量，先写：

> 以下用 \(s=\omega/\omega_0\) 代替 \(\omega\)，因此 \(s\) 是无量纲频率，而不是新的物理频率。

“精确解”“闭式解”“渐近式”“数值解”“模型假设”不要混用。

## 7. 章节自检清单

每章完成后逐项检查：

- [ ] 开头说明了研究对象、物理动机和最终目标。
- [ ] 首次出现主方程前写明了坐标、符号、单位和边界条件。
- [ ] 每个小参数都有条件、保留阶数和适用范围。
- [ ] 至少一个核心公式给出了关键推导链。
- [ ] 闭式公式的分支、定义域和积分常数已说明。
- [ ] 每个主要公式后都有物理解释。
- [ ] 至少检查两个极限，其中一个是熟知极限。
- [ ] 至少有一个完整数值实例，并检查量纲、守恒或对称性。
- [ ] 标准结果若未推导，已注明来源或说明采用的约定。
- [ ] 本章结尾说明了结论和下一章的关系。
- [ ] 与相邻章节存在必要的交叉引用。

## 8. 当前讲义的改造顺序

不建议一次性重写全部章节。优先按“主线收益/改写成本”排序：

1. `matrix_optics.tex`：先补傍轴模型、高斯光束目标，再把三/四透镜矩阵乘法移为验证例。
2. `fourier_optics_4f.tex`：补菲涅尔积分到焦平面 Fourier 变换的主推导，明确变换约定。
3. `ising_model.tex`：补 Bethe 熵的树图逻辑、自洽方程和临界判据。
4. `bose_fermi_gas.tex`：重排“散射前置 -> 统计展开 -> 相互作用修正 -> 低温磁性”顺序。
5. `crystal_optics.tex`：先画清 \(D,E,S,k\) 几何，再做边界条件和能量检查。
6. `green_function.tex`：以“点源响应”开篇，统一静电、扩散、波动 Green 函数的主线。
7. 其余章节按同一模板补齐开头、近似台账、实例和章末总结。

改造时优先重排段落和补关键转折，不要一开始大规模改公式。公式正确性、符号约定和物理叙事应分轮检查。

## 9. 一句话版本

每个物理问题都按同一节奏讲：

> 先说为什么研究，再说模型保留了什么；先做一个可检查的基准解，再引入新机制；每个近似都记账，每个闭式结果都取极限；最后用一个具体实例说明公式到底改变了什么物理图像。

---

## B. 全库重构方案（原 supplement.md）

# YHWNotes 进阶讲义全库重构方案

## 0. 文件定位

本文档是 YHWNotes 的内容重构总方案。它回答四个问题：

1. 这套讲义面向什么层次的读者；
2. 各章节应该讲到什么深度；
3. 现有章节哪些只需补强，哪些需要大幅重排或拆分；
4. 如何把闭式计算、近似模型、一般解法和物理实例组织成统一体系。

本方案不把讲义改造成从定义开始的入门教材。它应当保留专题讲义的密度和数学强度，但必须让读者清楚地知道：

> 当前问题是什么，为什么采用这个模型，闭式结果依赖哪些假设，近似模型从哪里来，更一般的解法是什么，以及结果如何回到物理。

## 1. 读者定位

### 1.1 默认先修背景

读者默认已经学习过以下内容：

- 经典力学：拉格朗日/哈密顿形式、中心力、刚体、线性振动；
- 电动力学：Maxwell 方程、势函数、边界条件、平面波、基本辐射；
- 量子力学：Hilbert 空间、角动量、微扰、散射和基本谱理论；
- 统计力学：配分函数、系综、热力学极限、平均场；
- 数学物理：常微分方程、偏微分方程、Fourier 变换、复分析基础、特殊函数；
- 数值方法：基本线性代数、数值积分、非线性方程和绘图。

因此，正文不必重新解释“什么是梯度”“什么是配分函数”，但必须在专题内说明：

- 本章采用的符号和约定；
- 本章与先修知识的接口；
- 为什么标准理论在这里需要推广；
- 当前闭式公式的适用范围。

### 1.2 本讲义不追求的目标

本讲义不追求：

- 覆盖所有基础定义；
- 把每个代数步骤都写成初等教材；
- 汇总尽可能多的公式；
- 用大量历史背景替代数学推导；
- 把所有高级主题都写成完整专著。

它追求的是专题问题中的“第二层理解”：

- 从标准方程进入非标准几何或非标准边界；
- 从形式解进入可计算闭式；
- 从精确模型进入受控近似；
- 从一个特殊例子推广到一般结构；
- 从不同方法的结果比较其物理假设。

### 1.3 章节深度比例

每个主题建议采用如下比例：

- 60%：核心问题、主推导和闭式结果；
- 25%：近似、极限、数值验证和典型实例；
- 15%：一般化、替代方法和进阶延伸。

进阶内容不能只是“列出更高级名词”。每个高级方向必须回答：

1. 它解决了当前基本模型的哪个限制；
2. 它改变了哪一条方程或边界条件；
3. 它保留了哪些旧结果；
4. 它在什么参数区间下才值得使用。

## 2. 统一叙述目标

### 2.1 每个专题的核心链条

所有章节都采用下面的主链：

> 物理问题  
> -> 模型与假设  
> -> 对称性、守恒量或算子结构  
> -> 基准解  
> -> 一般闭式或谱解  
> -> 近似模型  
> -> 极限与一致性检查  
> -> 实例与更一般方法。

这不是固定的章节标题，而是固定的思考顺序。

### 2.2 每个重要公式的七个问题

任何核心公式都应能够回答：

1. 它从哪个方程来；
2. 它使用了哪个假设；
3. 它的未知量是什么；
4. 它是精确式、渐近式还是数值式；
5. 它的定义域和分支是什么；
6. 它在熟知极限下变成什么；
7. 它改变了哪个可观测量或物理图像。

正文不需要机械地逐条列出，但关键转折必须完整体现。

### 2.3 “入门说明”与“进阶说明”的区别

针对当前读者，开头不需要写：

> “导数表示函数变化率，积分表示求和。”

但需要写：

> “本章真正困难的地方不是写出 Maxwell 方程，而是有界各向异性介质中 \(D\)、\(E\)、\(S\) 与波矢方向不再共线；因此必须先求本征波，再处理边界条件。”

也就是说，讲义应减少基础定义，增加专题困难的定位。

## 3. 全库组织结构

### 3.1 建议的学科主线

五大领域内部应形成如下方法关系。

#### 力学

```text
中心力与守恒量
    -> Lorentz 协变和相对论动力学
    -> 刚体与非线性系统
    -> 稳定性、分岔和渐近方法
```

#### 电动力学

```text
静态边值问题
    -> 波导、谐振腔和模式
    -> 散射与辐射
    -> 多极展开
    -> 等离子体和色散介质
```

#### 光学

```text
Maxwell 平面波
    -> 各向异性晶体
    -> 薄膜和边界矩阵
    -> Fourier 光学和空间滤波
    -> ABCD 与 Gaussian beam
```

#### 统计力学

```text
系综和配分函数
    -> 理想量子气体
    -> 弱相互作用修正
    -> 磁场和低温奇异性
    -> 格点模型、Bethe 与平均场
```

#### 数学工具

```text
Fourier、Green、谱分解
    -> 特殊函数与本征问题
    -> 反问题和正则化
    -> 在电磁、光学和统计章节中反复调用
```

### 3.2 MathTool 不应只是公式仓库

数学工具章节应明确注明“服务对象”。例如：

- Green 函数：服务于静电、热核、波动和边值问题；
- VSH：服务于散射、辐射和多极展开；
- Mathieu 函数：服务于椭圆边界、周期系统和稳定性；
- 椭球坐标：服务于椭球边界上的 Laplace/Helmholtz 分离；
- 解谱与 GLS：服务于实验数据反演和不确定度传播。

数学工具正文可以较抽象，但每一节至少有一个“物理调用点”。

## 4. 章节统一模板

每个主题文件建议按以下结构重排。

### 4.1 章节开头

包含三段：

1. **问题段**：研究什么物理对象；
2. **困难段**：标准方法在哪一步失效或不足；
3. **路线段**：本章将用哪些方法解决。

模板：

```text
本章研究……

在最简单的……模型中，问题可以由……解决。
但当……时，……不再成立，困难集中在……。

我们先建立……的基准解，再引入……，
最后用……极限和……实例检查结果。
```

### 4.2 模型与约定

在主方程之前集中说明：

- 坐标和方向；
- 时间/频率约定；
- 单位制；
- 边界和初始条件；
- 无量纲变量；
- 小参数；
- 保留和忽略的物理机制。

### 4.3 基准问题

先选一个读者熟悉的基准：

- 真空、各向同性、无耗散；
- 无外场、无扰动；
- 无限大、平面或球对称；
- 线性、低频或长波极限。

基准问题的作用是确认符号和尺度，而不是浪费篇幅重复教材内容。

### 4.4 核心推导

只展开改变物理结构的步骤：

- 分离变量；
- 守恒量消元；
- 变分得到自洽方程；
- 边界条件得到矩阵；
- 渐近展开；
- 模式正交；
- 闭式积分；
- 稳定性判据。

标准代数可以简写，但要注明“这里使用了什么恒等式或结构”。

### 4.5 结果、极限与实例

每个大节至少包括：

- 一个闭式结果；
- 一个熟知极限；
- 一个边界或失效极限；
- 一个完整实例。

实例不只给数值，还要说明：

- 该参数属于哪种物理区域；
- 哪个项主导；
- 结果是否满足守恒；
- 改变一个参数会发生什么。

## 5. 力学部分重构方案

## 5.1 一次反比势场中的运动

文件：

[inverse_square_motion.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Mechanics/InverseSquareMotion/inverse_square_motion.tex)

### 当前定位

这章已有“相对论精确解 -> 吸引/排斥 -> 非相对论微扰”的主线，属于可以保留骨架、重点加强解释的章节。

### 建议结构

#### 第一节：相对论中心力的统一形式

先从哈密顿-雅可比方程说明：

- 为什么 \(S=-Et+L\phi+f(r)\) 可以分离；
- \(E,L\) 分别对应时间和平移/旋转对称；
- 径向问题如何化为关于 \(u=1/r\) 的一维问题。

引入统一参数：

\[
\Delta=\alpha^2-c^2L^2,\qquad
\mathcal{E}=E^2-m^2c^4.
\]

然后按 \(\Delta>0,\Delta=0,\Delta<0\) 分类，而不是一开始分别堆三条公式。

#### 第二节：轨道几何分类

对每个分支明确解释：

- \(\Delta>0\)：临界吸引/捕获结构；
- \(\Delta=0\)：无有限近日点的临界轨道；
- \(\Delta<0\)：有界或散射型角向结构。

给出：

- \(r(\phi)\)；
- 物理解域；
- 渐近线；
- 转向点；
- 碰撞条件。

#### 第三节：时间参数

将 \(t(r)\) 视为独立问题说明：

- 为什么角度闭式和时间闭式的积分类型不同；
- \(\arcosh\)、\(\arccos\) 分支分别对应什么能量区域；
- 相撞时间为何有限或发散。

#### 第四节：散射与非相对论极限

建立：

\[
\chi_{\mathrm{rel}}
\longrightarrow
\chi_{\mathrm{Newton}}
\]

并把 \(\beta_0^2\) 修正解释为速度效应，而不是孤立的展开系数。

#### 第五节：弱扰动进动

统一处理：

- Schwarzschild 型 \(1/r^3\) 修正；
- 椭球体四极矩修正；
- 一般摄动势 \(\varepsilon(r,\phi)\)。

给出通用公式：

\[
\Delta\phi
=\frac{\partial}{\partial L}
\left(\text{一周期平均扰动作用量}\right),
\]

然后说明 GR 和四极矩只是这个公式的两个实例。

### 高级补充

- Runge-Lenz 向量与轨道闭合；
- action-angle 变量；
- 一般中心势中的进动判据；
- 相对论散射的弱场极限；
- 捕获轨道和临界冲击参数；
- 数值积分与闭式解的误差比较。

## 5.2 Lorentz 变换、Wigner 转动与 BMT

文件：

[lorentz_transformation.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Mechanics/LorentzTransformation/lorentz_transformation.tex)

### 建议重构为五个逻辑单元

1. Lorentz 群和四维速度；
2. 四维加速度与加速度变换；
3. 二阶张量和电磁场张量；
4. 非共线 Boost、Wigner 转动和 Thomas 进动；
5. BMT 自旋进动。

### 重点补充

- 用矩阵表示一次 Boost，并明确度规；
- 展示 \(A^\mu A_\mu\) 不变量如何约束空间分量；
- 先从两个有限 Boost 得 Wigner 转动，再取无穷小极限；
- 说明 Thomas 进动是“连续非共线 Boost 的几何效应”；
- 在 BMT 前说明自旋四矢量的正交条件 \(S\cdot U=0\)；
- 分别给出 \(g=2\) 和异常磁矩的极限。

### 高级补充

- Lie algebra 中的旋转生成元与 Boost 生成元；
- \(SO(1,3)\) 的生成元对易关系；
- Pauli-Lubanski 四矢量；
- BMT 方程在实验室系与瞬时共动系的比较；
- 电场、磁场同时存在时的协变形式。

## 5.3 刚体转动

文件：

[rigid_body.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Mechanics/RigidBody/rigid_body.tex)

### 保留主线

惯量张量 -> 欧拉角 -> 自由刚体 -> Euler top -> 定点转动。

### 需要补强

- 用 Poinsot 图像解释 \(E,L\) 两个椭球面的交线；
- 将三种主轴转动分别解释为稳定、稳定、不稳定；
- 明确 Jacobi 椭圆函数只是精确参数化，不是物理机制本身；
- 在异宿轨道处画出相空间连接关系；
- 将心形刚体算例分成“几何积分”和“稳定进动”两部分。

### 高级补充

- Euler top 的 separatrix；
- 稳定性与能量-角动量椭球；
- Routh reduction；
- 对称陀螺的有效势；
- 陀螺进动的快速进动和慢进动近似；
- 带电刚体和磁场耦合的 Hamilton 结构。

## 5.4 非线性振动

文件：

[nonlinear_oscillation.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Mechanics/NonlinearOscillation/nonlinear_oscillation.tex)

### 建议主线

```text
线性基准
    -> 弱非线性和阻尼的阶数
    -> 多尺度法
    -> 自由振动慢流
    -> 近共振受迫振动
    -> Duffing 响应
    -> 超谐/亚谐
    -> 稳定性和分岔
```

### 必须明确

- \(\epsilon\) 是形式展开参数；
- \(\zeta\) 是物理阻尼参数，且可满足 \(\zeta=O(\epsilon)\)；
- \(\zeta/\epsilon\) 是阶数记账后的系数，不代表物理阻尼变大；
- \(\sigma\) 是失谐量；
- \(\Phi,\Psi\) 分别对应慢振幅和慢相位。

### 高级补充

- averaging method 与 multiple scales 的等价性；
- Floquet 乘子与周期解稳定性；
- normal form；
- 参数共振和 Mathieu 方程；
- saddle-node、跳跃和滞回；
- Melnikov 方法作为远离弱扰动极限的延伸。

## 6. 电动力学部分重构方案

## 6.1 静态边值问题

文件：

[electrostatics.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/Electrostatics/electrostatics.tex)

### 当前问题

电阻网络、椭球、圆孔、磁扩散虽然都涉及线性边值问题，但物理主线不够集中。

### 建议改名或拆分

建议将其定位为：

> 静态场与扩散类边值问题专题。

按算子和边界组织：

1. 离散 Laplace 问题：电阻网络；
2. 连续 Laplace 问题：椭球和圆孔；
3. 轴对称扩散：磁场扩散；
4. 几何对称、Green 函数和特殊函数的共同结构。

高级补充：

- Dirichlet-to-Neumann map；
- 电阻网络与离散 Laplacian；
- 椭球坐标分离；
- 磁扩散的 skin depth；
- 静态问题与耗散问题的数学类比。

## 6.2 波导与谐振腔

文件：

[waveguide.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/Waveguide/waveguide.tex)

这是电动力学中叙述基础较好的章节之一，应作为风格示范。

### 建议补充

- 先说明波导的工程/物理问题：为什么自由空间波不能被简单引导；
- 由纵向场决定横向场的逻辑；
- TE/TM 分解的本征值意义；
- cutoff、相速度、群速度和能流之间的关系；
- 非理想边界导致的衰减和 \(Q\) 因子。

### 高级补充

- Sturm-Liouville 正交性；
- 开放波导和辐射模；
- scattering matrix；
- coupled-mode theory；
- 弱形变波导的微扰；
- 介质波导中的模式泄漏与复传播常数。

## 6.3 散射问题

文件：

[scattering.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/Scattering/scattering.tex)

### 建议主线

```text
远场观测量
    -> VSH 展开
    -> S 矩阵/相移
    -> 球对称 Mie 散射
    -> Rayleigh 与高频极限
    -> 圆柱散射
```

不要先给一长组系数，再告诉读者它们是什么。应先说明：

- \(a_{lm},b_{lm}\) 是哪些模式振幅；
- 相移如何反映散射体对入射模的响应；
- 总功率、角分布、光学定理如何从系数得到。

### 高级补充

- S 矩阵的幺正性与无耗散条件；
- optical theorem；
- resonant poles 和 quasi-normal modes；
- T-matrix 方法；
- 吸收介质中的非幺正散射；
- 高频渐近、几何光学和 creeping waves；
- 圆柱 \(m=0\) 分支的特殊处理。

## 6.4 辐射

文件：

[radiation.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/Radiation/radiation.tex)

### 建议拆成四层

1. 一般时谐源和 VSH；
2. 点电荷与推迟势；
3. 局域源的多极辐射；
4. 介质中的 Cherenkov、穿越和过渡辐射。

### 每层必须回答不同问题

- 一般时谐源：如何表示；
- 点电荷：如何处理运动源；
- 多极展开：哪些源矩主导；
- 介质辐射：色散和边界如何改变辐射条件。

### 高级补充

- gauge choice 与辐射场不变量；
- formation length；
- 介质色散中的因果性和 Kramers-Kronig；
- radiation reaction；
- synchrotron 的 Airy/Bessel 渐近；
- transition radiation 的边界匹配；
- multipole origin dependence 与 toroidal moments。

## 6.5 等离子体

文件：

[plasma.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/Plasma/plasma.tex)

### 建议结构

1. 冷流体模型；
2. 无磁场的纵波和横波；
3. 外磁场下的介电张量；
4. 垂直/平行传播模式；
5. 动理学修正与 Landau 阻尼；
6. 非均匀或弱碰撞延伸。

每一种模式都用同一表格说明：

| 项目 | 内容 |
|---|---|
| 极化 | \(E\) 的方向 |
| 色散 | \(\omega(k)\) |
| 主要恢复力 | 电场、磁场、压力或回旋 |
| 阻尼/增长 | 是否存在虚部 |
| 适用模型 | 冷流体、温流体或 Vlasov |

### 高级补充

- Stix dielectric tensor；
- Bernstein modes；
- warm plasma；
- drift kinetic 和 gyrokinetic 近似；
- Landau contour；
- two-stream instability；
- nonlinear wave-particle trapping。

## 6.6 STF 多极展开

文件：

[stf_multipole_expansion.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Electrodynamics/STFMultipoleExpansion/stf_multipole_expansion.tex)

建议作为辐射章节后的高级专题，而不是完全独立的第一入口。

### 建议顺序

1. 普通 Cartesian multipole；
2. 为什么 trace 部分会和低阶多极混合；
3. 二阶 STF 的完整手算；
4. 一般 \(n\) 阶 STF；
5. 场和功率；
6. toroidal moments；
7. 与 VSH 多极系数的对应。

### 高级补充

- 规范变换和原点平移；
- irreducible representation of \(SO(3)\)；
- Cartesian 与 spherical multipole 的转换；
- toroidal/electric/anapole cancellation；
- 高阶多极的辐射选择规则。

## 7. 光学部分重构方案

## 7.1 晶体光学

文件：

[crystal_optics.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Optics/CrystalOptics/crystal_optics.tex)

### 建议主线

```text
本构关系
    -> Maxwell 本征问题
    -> 波面、光线面和能流面
    -> 单轴/双轴晶体
    -> 边界条件
    -> Fresnel 系数
    -> 偏振器件和锥形折射
```

必须区分：

- 波矢方向；
- 相速度方向；
- 群速度或能流方向；
- \(D\) 与 \(E\) 的夹角。

### 高级补充

- Jones 与 Mueller 矩阵；
- complex dielectric tensor；
- circular birefringence；
- magnetoelectric coupling；
- 非厄米晶体和 exceptional points；
- conical refraction 的局部展开；
- 各向异性介质中的 reciprocity。

## 7.2 Fourier 光学 4f

文件：

[fourier_optics_4f.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Optics/FourierOptics4F/fourier_optics_4f.tex)

### 建议主线

```text
Huygens/Fresnel
    -> 薄透镜相位
    -> 后焦平面 Fourier 变换
    -> 两透镜 4f 系统
    -> 空间频率滤波
    -> 孔径、晶格和采样
```

### 高级补充

- finite aperture 和 transfer function；
- sampling、aliasing 和 discrete Fourier transform；
- coherent 与 incoherent imaging；
- optical transfer function；
- phase contrast；
- lattice diffraction 和 reciprocal lattice；
- 4f 系统与 ABCD 矩阵的连接。

## 7.3 矩阵光学

文件：

[matrix_optics.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Optics/MatrixOptics/matrix_optics.tex)

### 建议主线

1. 傍轴光线的状态空间；
2. 元件矩阵的推导；
3. 矩阵复合；
4. 主面、节点、焦点；
5. Gaussian beam 的复曲率；
6. 光腔稳定性；
7. 真实光具组实例。

### 高级补充

- \(Sp(2,\mathbb{R})\) 结构；
- ABCD 与 symplectic geometry；
- resonator stability criterion；
- Gouy phase；
- astigmatic Gaussian beam；
- ABCD 矩阵和 Fourier optics 的统一；
- 非理想透镜与复矩阵元。

三/四透镜乘法不应占据主叙事，应放入“矩阵复合练习”。

## 8. 统计力学部分重构方案

## 8.1 Bose-Fermi gas

文件：

[bose_fermi_gas.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Statistics/BoseFermiGas/bose_fermi_gas.tex)

这是全库最需要拆分或大幅重排的文件。

### 推荐拆成三篇

#### A. 低能散射与弱相互作用

- 分波和散射长度；
- 硬球边界；
- 赝势；
- 二阶巨配分函数；
- 自旋对称性和交换项；
- 相互作用能修正。

#### B. 理想 Bose/Fermi 气体

- 巨正则系综；
- \(g_\nu(z),f_\nu(z)\)；
- 占据数和涨落；
- 热力学量；
- Sommerfeld 展开；
- 零温和低温极限。

#### C. 磁场与量子统计相变

- Landau 能级；
- 磁化率；
- 低温临界条件；
- 奇异自由能；
- 磁化率和热容的非解析性。

### 高级补充

- Beth-Uhlenbeck 公式；
- virial expansion；
- Fermi liquid correction；
- BCS/BEC crossover；
- spin susceptibility；
- density of states engineering；
- quantum critical scaling。

高级内容应按“当前模型的哪一项假设被放宽”来组织，不要直接变成文献综述。

## 8.2 Ising 模型

文件：

[ising_model.tex](E:/OneDrive/Desktop/YHWNotes/chapters/Statistics/IsingModel/ising_model.tex)

### 建议主线

```text
格点模型与序参量
    -> 树图概率分解
    -> Bethe 自由能
    -> 自洽方程
    -> 临界点和响应函数
    -> Bragg-Williams 对比
```

### 必须突出的方法差异

- Bethe：树图上局部关联保留；
- Bragg-Williams：完全因子化；
- 一维 transfer matrix：无有限温度相变；
- 无限维极限：平均场成为合理近似。

### 高级补充

- cavity method；
- belief propagation；
- correlation length；
- finite-size scaling；
- transfer matrix；
- cluster variational method；
- renormalization-group viewpoint。

## 9. 数学工具部分重构方案

## 9.1 Green 函数

文件：

[green_function.tex](E:/OneDrive/Desktop/YHWNotes/chapters/MathTool/BasicAlgebra/green_function.tex)

### 统一主线

```text
线性算子的点源响应
    -> 静态 Green 函数
    -> 边界条件和谱展开
    -> 热核
    -> 推迟 Green 函数
    -> 统一维数表达
```

### 高级补充

- distributional derivative；
- resolvent；
- spectral theorem；
- heat kernel expansion；
- image method 的适用条件；
- Robin-to-Dirichlet map；
- retarded/advanced/Feynman Green function 的区别。

## 9.2 无穷级数与积分

文件：

[infinite_integrals.tex](E:/OneDrive/Desktop/YHWNotes/chapters/MathTool/BasicAlgebra/infinite_integrals.tex)

这是目前较适合保留主体的数学章节。

建议新增一个“物理中的积分”部分：

- Fourier 和 Laplace 变换；
- 振荡积分；
- stationary phase；
- steepest descent；
- Bessel/Hankel 积分；
- Green 函数中的谱积分；
- 辐射和散射中的大参数极限。

这样它不再只是分析学工具，也能成为全库的渐近方法基础。

## 9.3 参数估计与解谱

文件：

[parameter_estimation.tex](E:/OneDrive/Desktop/YHWNotes/chapters/MathTool/BasicAlgebra/parameter_estimation.tex)

[spectral_deconvolution.tex](E:/OneDrive/Desktop/YHWNotes/chapters/MathTool/BasicAlgebra/spectral_deconvolution.tex)

建议形成“线性反问题”专题：

1. GLS 的几何；
2. 误差传播；
3. 白化；
4. SVD；
5. 病态性；
6. Tikhonov；
7. 约束、正则化和 Bayesian 解释。

### 高级补充

- Fisher information；
- Cramér-Rao bound；
- generalized cross-validation；
- L-curve；
- positivity-constrained inverse problem；
- Bayesian posterior covariance；
- model discrepancy。

## 9.4 椭球坐标、Mathieu、VSH

这些章节应作为“特殊几何与特殊函数”组：

### 椭球坐标

- 从椭球边界问题开始；
- 再引入椭圆积分；
- 之后给坐标、度量、Laplacian；
- 最后讨论分离变量和物理应用。

### Mathieu 函数

- 从椭圆柱或参数激励振子开始；
- 用 Floquet 理论说明周期解；
- 再讲特征值、稳定舌和级数；
- 最后与非线性振动、波导或椭圆边界连接。

### VSH

- 从角动量算符和球面标量谐函数开始；
- 构造 \(\vb{X}_{lm},\vb{M}_{lm},\vb{N}_{lm}\)；
- 给正交性和旋度；
- 再进入散射和辐射。

## 9.5 supplementary_formulas

文件：

[supplementary_formulas.tex](E:/OneDrive/Desktop/YHWNotes/chapters/MathTool/SpecialFunctions/supplementary_formulas.tex)

该文件不宜继续作为独立叙述章节，而应重构为“公式附录”：

- 按服务章节分组；
- 每组公式标注用途；
- 写清变换约定和适用域；
- 给出来源或一句推导提示；
- 关键公式链接回正文；
- 将未使用或完全孤立的公式移入独立附录。

## 10. 全库需要统一的高级方法

### 10.1 守恒量与对称性

所有章节尽量先寻找：

- 平移对称 -> 动量；
- 时间平移 -> 能量；
- 旋转对称 -> 角动量；
- 规范对称 -> 电荷守恒；
- 周期性 -> Bloch/Floquet；
- 线性平移不变 -> Fourier；
- 自伴算子 -> 正交谱。

这会把不同主题连接起来，而不是让每章都是孤立技巧。

### 10.2 谱方法

需要在不同章节反复强调同一个结构：

> 选择本征基，把耦合的微分问题变成模式系数问题。

它在以下章节中分别表现为：

- VSH；
- 波导横向本征函数；
- Green 函数谱展开；
- Mathieu/Floquet 模式；
- Ising transfer matrix；
- SVD 解谱。

### 10.3 响应函数

把响应函数作为跨学科主线：

- 电磁介电张量；
- Green 函数；
- 散射 \(S\) 矩阵；
- GLS 协方差；
- 统计力学磁化率；
- 线性振动的频率响应。

每次出现“响应”，都应明确：

- 外部驱动是什么；
- 响应变量是什么；
- 极点、零点和虚部的物理意义是什么。

### 10.4 精确解与近似解的层级

每章区分三类结果：

1. **结构精确**：由对称性或算子结构严格成立；
2. **模型精确**：在给定模型内精确，但模型本身有近似；
3. **渐近近似**：只在某个小参数区域成立。

例如：

- Mie 系数对球形边界是模型精确；
- Rayleigh 散射是 \(kR\ll1\) 渐近式；
- 几何光学是短波极限；
- 冷等离子体模型忽略热速度，但不等于完全精确。

## 11. 章节重构优先级

### 第一优先级：大幅重构

1. `bose_fermi_gas.tex`
2. `matrix_optics.tex`
3. `fourier_optics_4f.tex`
4. `green_function.tex`
5. `radiation.tex`
6. `crystal_optics.tex`

这些章节的主要问题是主线和内容边界，而不仅是解释不足。

### 第二优先级：中等重构

1. `ising_model.tex`
2. `lorentz_transformation.tex`
3. `plasma.tex`
4. `scattering.tex`
5. `vector_spherical_harmonics.tex`
6. `stf_multipole_expansion.tex`
7. `mathieu_functions.tex`

这些章节已有主体结构，但需要补动机、方法比较和高级延伸。

### 第三优先级：局部补强

1. `infinite_integrals.tex`
2. `parameter_estimation.tex`
3. `spectral_deconvolution.tex`
4. `waveguide.tex`
5. `thin_film.tex`
6. `inverse_square_motion.tex`
7. `rigid_body.tex`
8. `nonlinear_oscillation.tex`

这些章节可作为统一风格示范，不建议先推倒重写。

## 12. 分阶段执行方案

### Phase 0：统一记号和文件边界

目标：

- 固定时间因子、Fourier 约定、度规、单位制；
- 给主题文件标记“核心/附录/工具”；
- 处理明显的跨章符号冲突；
- 建立章节依赖表。

交付物：

- 全库 notation table；
- MathTool 使用关系；
- 每章一段研究范围说明。

### Phase 1：重构三类样板

先完成三个风格完全不同的样板：

1. `waveguide.tex`：电动力学本征问题；
2. `matrix_optics.tex`：矩阵与 Gaussian beam；
3. `ising_model.tex`：统计力学自洽与临界性。

这三章分别验证：

- 模式方法；
- 传输矩阵方法；
- 变分/自洽方法。

### Phase 2：处理主干章节

顺序建议：

1. Green 函数；
2. Fourier 光学；
3. Bose-Fermi gas；
4. 辐射；
5. 晶体光学；
6. 等离子体。

这些章节重构后，会成为全库的知识主干。

### Phase 3：补充高级专题

加入或完善：

- action-angle 和一般中心力；
- Wigner/Thomas/BMT；
- Floquet、normal form、Melnikov；
- S 矩阵、optical theorem、T-matrix；
- STF、toroidal moments；
- gyrokinetic 和 Landau contour；
- OTF、coherent imaging；
- cavity method、finite-size scaling；
- resolvent、heat kernel 和 Bayesian inverse problem。

### Phase 4：统一实例与验证

每章补：

- 一个基准例；
- 一个机制例；
- 一个边界/失效例。

同时进行：

- 量纲检查；
- 极限检查；
- 守恒检查；
- 数值与闭式互校；
- 图像与公式对照。

### Phase 5：全库编辑审查

检查：

- 是否有章节动机；
- 是否有路线图；
- 是否明确模型边界；
- 是否把精确和近似分开；
- 是否解释闭式公式；
- 是否说明失败条件；
- 是否和前后章节衔接。

## 13. 每个高级内容的纳入标准

高级内容只有满足以下至少两条才进入正文：

- 直接解释当前公式的来源；
- 放宽当前模型的一个关键假设；
- 提供一个更一般的闭式或谱解；
- 解释当前近似何时失效；
- 与其他章节建立重要联系；
- 能通过一个完整实例验证。

只满足“这个主题很高级”而没有连接当前主线的内容，应放入：

- notes；
- supplement；
- appendix；
- reference list。

## 14. 新增正文环境的建议

现有 `example` 和 `notes` 环境可以继续使用。后续可在 `preamble.tex` 增加以下可选环境：

- `motivation`：本节研究什么；
- `model`：假设和适用范围；
- `approximation`：近似台账；
- `check`：极限、守恒、数值检查；
- `advanced`：进阶延伸；
- `summary`：本节结论。

这些环境不是为了增加装饰，而是帮助读者快速识别：

- 哪些是物理问题；
- 哪些是数学推导；
- 哪些是近似；
- 哪些是验证；
- 哪些是可选延伸。

## 15. 完成标准

一个章节完成重构后，应满足：

- 读者不看公式，也能说出本章研究的问题；
- 读者能指出模型的主要假设；
- 读者能区分精确结果和渐近结果；
- 至少一个闭式结果有完整来源；
- 至少一个结果有极限检查；
- 至少一个实例解释了物理含义；
- 高级内容不是孤立名词，而是从基本模型自然生长出来；
- 下一章为什么接着出现是清楚的。

## 16. 最终目标

这套讲义最终不应只是“很多专题的集合”，而应成为一套以数学物理方法组织起来的进阶讲义：

```text
对称性与守恒
    -> 本征问题与谱分解
    -> Green/响应函数
    -> 闭式解与特殊函数
    -> 渐近展开和有效模型
    -> 稳定性、散射和临界性
    -> 数值验证与实验可观测量
```

读者已经知道基础理论，因此讲义最有价值的部分不是再次介绍定义，而是展示：

> 一个熟悉的基础方程，如何在特殊几何、复杂边界、色散介质、弱扰动、临界区域或逆问题中，发展出更一般的数学结构和更丰富的物理图像。

