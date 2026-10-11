# MathSkills — R17 深修状态与后续问题

最新有效要求与跨书后续任务见根目录 [待后续优化](../../待后续优化.md)；本文旧阶段的版数与章数只表示对应历史版本。

## 2026-10-11 综合例题续修

新增区间算子的定义域、谱、静态响应、演化与模态误差完整计算链，以及同一高斯趋势观测的概率、投影、估计、检验与区间计算链。后续分布/积分算子、几何和非线性部分的连续综合应用仍待补齐；全书数学审查不能由新增例题的局部审阅代替。

## 2026-10-09 概率基础的前后衔接续修

详细 ch18–20 的本次修订把概率空间、随机变量、期望和独立性放到第一次实际使用之前；条件期望按定义、存在唯一性、Jensen、投影、全方差重新展开，保留 Hilbert→L1 的替代构造于章末。收敛例题归位，Bernstein 补独立性及完整指数矩证明，高斯线性像和正交投影补特征函数论证。原相关引用标签保留。细节见 temp/worklogs/detailed-foundation-restoration-2026-10-09.md。ch19 其他高级渐近结论以及其余全书框体尚不能由此次基础续修判为全部审查完成。

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

- ch04 仍显著长于其他章。下一轮应检查重复定义和重复 Example，合并时保留独有细节；技术证明保留在相关正文，可按认知任务拆节或正常章节，不移入附录。必须保持 boundary triplet → spectral measure → resolvent/propagator 的主线不断裂。
- ch05 可进一步加入 wave-front/singular support 的最低完整框架，但只有在后续确实使用时才展开 microlocal language。
- ch06 可把 Picard criterion、spectral cutoff、Tikhonov 与一般 filter regularization 的误差/参数选择关系再做一次统一定理化。
- ch07 可继续深化 Sobolev 型局部适定性与 continuation criterion，但必须先声明函数空间与乘积估计，不能只写形式能量法。
- 几何部分下一层可选方向是 comparison geometry（Rauch/Bonnet--Myers）或 elliptic Hodge regularity/Dirichlet-to-Neumann；二者都应作为新母结构加入，而不是零散公式。
- 统计部分若继续推进，应从 semiparametric tangent space、efficient influence function 或二阶 LAN/BvM 建立统一框架，不继续堆彼此独立的渐近公式。

## 2026-09-15 merge 审计

- 修复未定义引用：ch05 中 `chap:math-pde-nonlinear` 改为实际 label `chap:nonlinear-pde`。
- 清除作者自我澄清与拟人化语句：删除“为避免…混淆/复用记号”“这里没有…”“在这里只需要记住”“它告诉我们/提醒我们”等；trivial 处的“显然”改为具体依据（如 `\dd^2=0`、由定义）。
- 编译验证：406 页，0 undefined reference。

## 2026-10-09 本轮续修

详细版 23 章保留，新稿 37 个专题归入相关理论章；定义域、PVM、闭形式等新稿材料与旧稿相应定义及证明衔接。统一内积约定，重写自伴谱理论、形式扰动、演化、Hodge 和 Clifford 相关论证。重要结论入定义／命题／定理框并配证明；具体修正见 temp/worklogs/other-books-deep-revision-2026-10-09.md。尚未逐框连续复核的几何、概率、统计章节仍需审查。


### 2026-10-09 统计三章的详细稿续修

详细 ch21–23 与相关章末推导已实质重写；短稿 ch30–37 的主要结论、简明证明和独有算例融入相关位置，原文件保留。旧详细稿中的 64 个标签全部保留。新增的确切修正、四组数据复算、局部正则性与 BvM 总变差证明见本轮 worklog。其余未逐框通读的章节仍待审查；不能将结构扫描通过视为全书数学审查完成。
