# AdvancedPhysics — Issues

## R14 状态：六线程遗留 P0 已闭合

统计物理部分现在从有限 Gibbs 系统、图/同调、transfer matrix、Clifford/Jordan--Wigner 一路闭合到有限扇区、Onsager/Yang 与一般 cluster expansion。R14 新增 Feynman--Sherman 局部交叉消去的 Pfaffian/完美配对证明，不再只把 determinant cycle expansion 到 even-subgraph 权重之间的组合消去当作黑箱。Yang 磁化也不再以各向同性 symbol 冒充一般情形：对各向异性方格直接写出正确 diagonal Toeplitz symbol，再由 Fourier 系数和 strong Szegő 得到
\[
M=\left[1-(\sinh2K_h\sinh2K_v)^{-2}\right]^{1/8}.
\]

有限尺寸部分已经给出 NS/R 四个 fermionic spin structures 与算符 traces/Kaufman parity projection 的逐项字典。R14 又把临界 finite-size 系数从各向同性推广到整个各向异性临界线：若临界 transfer velocity 为 \(v_c=\sinh(2K_{h,c})\)，则 rapidity cusp 的 Fourier 尾和离散 Poisson 求和直接给出
\[
S_{\mathrm R}=N\bar\gamma-\frac{\pi v_c}{3N}+O(N^{-3}),
\qquad
S_{\mathrm{NS}}=N\bar\gamma+\frac{\pi v_c}{6N}+O(N^{-3}),
\]
从而主导 NS 条带的每格点自由能修正为 \(\pi v_c/(12N^2)\)。该系数由 lattice spectrum 推出，\(c=1/2\) 只作为一致性检查。

cluster/virial 部分补入精确三阶 canonical cumulant
\[
C_3=Q_3-Q_1Q_2+\frac13Q_1^3,
\qquad
b_3=\frac{\lambda_T^3}{\mathcal V}C_3,
\]
并把三体物理 Hilbert 空间分解为内部通道，明确内部简并度、束缚 trimer 简并度、spectator 二体 subtraction 与 connected three-body spectral shift 的计数。高维零能共振、一般维 effective-range expansion、自伴扩张参数与散射长度的对应已经在 ch14 完成；TCL4/NZ 逐阶对应、finite-coarse-graining Kossakowski Gram 正性已经在 ch15 完成；worldtube/Schott 的局域守恒律与 Schott 束缚四动量推导已在 ch13 完成；外力 Gaussian 脉冲的显式 Schott 能量算例在重构中删去，留待决定是否补回为独立 Example。因此这些旧清单项目均不再属于未完成 P0。

## 后续可选深化

以下是新扩展方向，不是本轮未完成项：

- 若要完全内部证明二维 Ising 自旋关联，可继续从 Kaufman spinor/Wick--Pfaffian 推到 Toeplitz determinant；当前 strong Szegő 与相关函数定理被明确标为独立数学输入。
- 三体统计若继续深化，应进入 Faddeev/AGS resolvent 或三体 S-matrix determinant，再把 connected spectral shift 与 Efimov 标度异常放进同一框架。
- 开放系统可继续讨论长期弱耦合极限中的重求和、非 CP-divisible time-local dynamics 与 memory-kernel reconstruction；不能把有限阶 TCL 的局部误差直接外推到 \(t\sim O(\lambda^{-2})\)。
- 辐射反作用若继续扩展，可比较不同 worldtube/regularization prescription 的有限部分，但必须保持总能动量守恒和质量重整化约定不变。

## 出版 QA 约束

正式编译源保持 0 `paragraph/subsubsection`、0 裸 `\ref/\eqref`、0 公式 `resizebox`。符号注册继续使用：统计粒子数密度 \(\varrho\)，薄板体质量密度 \(\rho_{\rm m}\)、面密度 \(\mu_A\)，电荷密度 \(\rho_{\rm e}\)，量子密度算符 \(\rho\)，频谱哑变量 \(\varpi\)，立体角 \(\dd\Omega\)。

## 2026-09-15 merge 审计

- 自 `PhysicsLectureNotes_FourBooks_R17_AdvancedPhysics_REFINED_20260915` 合并精修后的 28 章正文与 frontmatter。
- 清除作者自我澄清与拟人化语句：删除“为避免…混淆/误当/冲突”“必须先强调”“为了…而不是依靠读者…”“需要说明 convention”及“告诉我们/允许我们”等。
- 编译验证：287 页，0 undefined reference，0 hard error。

## 2026-09-24 refactor_0924 深度重构

- 全书由 28 章重组为 35 章，依次展开统计物理、连续介质与经典场、高维与开放系统、原子与量子光学、分子物理；场量子化已前置于原子—光相互作用。
- 开放系统部分补全双量子位偏迹、约化动力学、Kraus 表示、完备性与完全正性；分子部分把 Born--Oppenheimer/Born--Huang 理论写成谱子空间上的 Hermitian 向量丛与投影联络，并补入曲率、整体回转、量子几何张量和标量势。
- 微分几何部分重写 Gauss--Bonnet 推导，从 Levi--Civita 联络与 Cartan 曲率方程，经带角点边界公式和测地三角剖分得到整体结论，不再循环引用待证结论。
- 删除依赖图式的“主线”“路线图”“脉络提示”写法，重写总论和多章开头，使动机、定义、计算与物理解读在正文中连续展开。
- 最终构建：333 页；925 个标记、407 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 `\\boxed`。

## 2026-09-24 零前置数学重写

- 新增“数学预备：从线性空间到联络”，从集合、商空间、秩--零化度、谱分解讲到群表示、Schur 引理、Lie 代数、流形、切向量、微分形式、向量丛、联络与曲率；核心结论均配有证明。
- ch03 由 788 行重写为 478 行。图、链空间、圈秩、平面 Euler 公式、面边界独立性、同调与 Gauss--Bonnet 均改成“定义—定理—证明”，并删除与 Ising 任务无关的映射类群、Torelli 群等跳级内容。
- ch16、ch21、ch23、ch30、ch31、ch34 在首次使用处补入 \(SO(d)\)、\(SU(2)\)、Lorentz 群、Clifford 代数、有限群表示、Haar 测度、流形、切空间、向量丛和联络的局部定义与证明，不再要求读者先修群论或微分几何。
- 全书 141 个 derivation 长框全部改为无边框的“解/证明”格式；重复的 Clebsch--Gordan 构造与章末特征标理论被合并，旧有“分四步建立”“关键步骤”等提纲腔改成连续论证。
- 构建与引用审计：328 个 PDF 页面，924 个标记、390 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 missing character。

## 2026-09-24 本科基础读者扩写

- ch11 不再从 \(H^2\) 迹空间直接起步。新增一维 Euler--Bernoulli 梁的势能变分，两次分部积分同时推出体方程和固支、简支、自由边界；补入唯一性证明、均布载荷完整解和简支梁显式 Green 函数。
- ch17 从“微分表达式不等于算符”讲起，用边界型区分对称与自伴，证明 Robin 半直线哈密顿量自伴，并把边界参数算到束缚态能量、相移、散射长度和概率流。
- ch18 从测量平均值建立密度算符、纯度和张量积，操作性定义偏迹并证明基底无关；补全纠缠与经典相关的区别，以及振幅衰减 Kraus 映射的逐项矩阵计算。
- ch19 在一般 Nakajima--Zwanzig/GKSL 推导之前加入量子比特算例：短时相位翻转、有限时 Kraus 解、振幅衰减、\(T_1/T_2\) 关系，以及高斯有色噪声到白噪声极限的完整推导。
- ch21 从空间波函数的转动作用推出 \(\vb L=\vb r\times\vb p\) 和角动量对易关系；ch30 从球面曲线坐标推进到切余切空间、张量、度量、Levi--Civita 联络、Christoffel 符号、测地线和 Riemann 曲率；ch31 用水分子完成 \(C_{2v}\) 位移表示的全部特征标约化。
- 语言按 no-ai-slop 审校标准再次清理：删除残留的“旧主线”空标题和接口式总结，把定义、计算与解释改成连续讲述。
- 最终构建与结构审计：342 个 PDF 页面，970 个标记、643 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 missing character；新增关键页已逐页渲染抽查。

## 2026-09-24 多电子原子继续深化

- ch22 先把反对称化算符证明为正交投影，再由行列式展开证明正交轨道构成的 Slater 行列式已经归一化；Hartree--Fock 方程的变分步骤改为连续证明，不再依赖冗长推导框。
- 新增氦原子的单参数变分计算。从归一化指数轨道出发，逐项算出动能、核吸引能和电子间 Coulomb 积分 \(J=5\zeta/8\)，再极小化得到 \(\zeta_*=Z-5/16\) 与 \(E_{\rm He}=-2.84765625\) Hartree。算例同时说明屏蔽、变分上界和动态关联能分别从哪里出现。
- 最终构建与结构审计：343 个 PDF 页面，971 个标记、643 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 missing character；新增页面已逐页渲染抽查。
