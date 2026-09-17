# MathSkills — R17 深修状态与后续问题

## 当前已闭合的结构性问题

R17 当前正式正文为 21 章，主线已经统一为：代数与表示 → Clifford/Spin → Hilbert/算子 → 自伴谱理论 → 分布/Fourier → Fredholm/逆问题 → 非线性 PDE → 微分几何 → 概率统计。正式编译源保持 `chapter → section → subsection`，不使用 `subsubsection` 或 `paragraph` 作为正文层级。

代数部分已将群作用、商群、Schur/Maschke、character 正交、投影算符、张量积、Lie 群/代数与 Casimir 放在 SU(2)、Clifford、Dirac 矩阵等特例之前。Clifford 部分已经从二次型的普适性质进入 Pin/Spin 与旋量表示，不再由低维例子反推一般结构。

分析部分已补齐 Hilbert tensor product、分布局部阶数、tempered distribution 的 Fourier 延拓、Fredholm alternative 的算子证明、Tikhonov 谱滤波，以及半线性演化的 Duhamel 公式、局部压缩映射、最大解与 blow-up alternative、能量闭合。可积系统按照一般 Hamiltonian PDE/Poisson 结构 → KdV → Lax 等谱 → 逆散射 → NLS 的顺序组织。

几何部分已补齐 frame bundle 与 solder form、一般向量丛联络和协变外微分、`D^2=\Omega\wedge`、Jacobi 场、Hopf--Rinow、能量第一/第二变分与 index form、有边界 Hodge 自伴结构、foliation/holonomy、一般度量与曲率变分、Ricci--DeTurck，以及一般余维 Gauss--Codazzi--Ricci。子流形基本定理现在从扩展平坦联络的可积性直接重构 Euclidean 等距浸入。

统计部分维持模型族/样本 → LLN/CLT → 正态投影 → sufficiency/completeness → likelihood/Fisher/Bayes → LR/Wald/Score/Pearson → 一般线性模型的单向主线；GLM、LAN/BvM 与线性模型中的 Hilbert 投影语言已经与前面的分析框架兼容。

## 当前出版 QA 不变量

正式编译源应持续满足：

- 0 `subsubsection` / `paragraph` 正文层级；
- 0 裸 `\ref` / `\eqref`，全部使用统一语义引用宏；
- 0 公式 `resizebox` / `scalebox` 式粗暴缩放；
- 0 undefined reference、duplicate compiled label、overfull box 与 hard LaTeX error；
- MathSkills 之外的文件不得因为本书精修发生字节变化。

`source_notes/` 仅保存不参与编译的旧材料，不把其中历史层级、旧 label 或旧措辞计入正式书目 QA。

## 下一轮真正值得继续深化的内容

当前剩余工作已从“补缺”转为理论深度和篇幅均衡：

- ch04 仍显著长于其他章。下一轮应优先检查重复定义、重复 Example 和可移入附录的技术证明，而不是继续增加同类型结论；必须保持 boundary triplet → spectral measure → resolvent/propagator 的主线不断裂。
- ch05 可进一步加入 wave-front/singular support 的最低完整框架，但只有在后续确实使用时才展开 microlocal language。
- ch06 可把 Picard criterion、spectral cutoff、Tikhonov 与一般 filter regularization 的误差/参数选择关系再做一次统一定理化。
- ch07 可继续深化 Sobolev 型局部适定性与 continuation criterion，但必须先声明函数空间与乘积估计，不能只写形式能量法。
- 几何部分下一层可选方向是 comparison geometry（Rauch/Bonnet--Myers）或 elliptic Hodge regularity/Dirichlet-to-Neumann；二者都应作为新母结构加入，而不是零散公式。
- 统计部分若继续推进，应从 semiparametric tangent space、efficient influence function 或二阶 LAN/BvM 建立统一框架，不继续堆彼此独立的渐近公式。

## 2026-09-15 merge 审计

- 修复未定义引用：ch05 中 `chap:math-pde-nonlinear` 改为实际 label `chap:nonlinear-pde`。
- 清除作者自我澄清与拟人化语句：删除“为避免…混淆/复用记号”“这里没有…”“在这里只需要记住”“它告诉我们/提醒我们”等；trivial 处的“显然”改为具体依据（如 `\dd^2=0`、由定义）。
- 编译验证：406 页，0 undefined reference。
