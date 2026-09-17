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
并把三体物理 Hilbert 空间分解为内部通道，明确内部简并度、束缚 trimer 简并度、spectator 二体 subtraction 与 connected three-body spectral shift 的计数。高维零能共振、一般维 effective-range expansion、自伴扩张参数与散射长度的对应已经在 ch14 完成；TCL4/NZ 逐阶对应、finite-coarse-graining Kossakowski Gram 正性已经在 ch15 完成；worldtube/Schott 的局域守恒与外力脉冲算例已经在 ch13 完成。因此这些旧清单项目均不再属于未完成 P0。

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
