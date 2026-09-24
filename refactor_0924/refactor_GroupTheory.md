# GroupTheory 深度重构方案

## 1. 原件诊断：前六章讲得太“满”，后两章讲得太“快”

当前 `GroupTheory` 共 8 章，约 14577 行，约 203 个主要公式环境、38 个 Derivation、99 个 Example。它的局部语言其实是四本中最接近“人讲课”的：ch01 会先解释“两个几何变换可以先后执行”，再告诉读者这就是二元运算；这种写法应作为全书声线样本。

真正的问题是结构失衡：

- ch01 约 3123 行、22 个 Example，从群公理一路讲到 Cauchy、Sylow、Jordan–Hölder、可解群、直积、半直积。第一次学群论的人还没建立“陪集/商群为什么需要”，就已经被带到有限群结构理论。
- ch02–ch06 每章约 1750–2636 行，99 个 Example 几乎都集中在前六章，正文经常被“定义—例子—定理—例子”切碎。很多两三行验证完全可以写在正文里，不需要独立环境。
- ch03 同时承担点群、空间群、晶体点群表示；ch04 又同时承担量子简并、微扰、投影、选择定则、红外/Raman、Bloch、小群、时间反演、破缺。应用层太密。
- ch05 把 SO(3)、SU(2)、二重覆盖、旋量、双群、CG、不约化张量全压一章。内容都重要，但二重覆盖和半整数角动量应比现在慢得多。
- ch07 只有约 263 行，却要讲 Minkowski、Lorentz 代数、有限维场表示、Clifford、Poincaré、Casimir、Wigner 分类。
- ch08 只有约 448 行，却要讲 Lie 代数、根、最高权、SU(3)、标准模型表示、Weyl 群、Yang–Mills 拓扑、SU(5)、seesaw。

这两个末章不是“写短了”，而是**章节边界本身错误**。它们必须废止并从头重建。

---

## 2. 新的认知主线

全书建议沿一条真正能讲出口的问题链推进：

> 可逆操作怎样复合？
> → 大群里怎样识别子结构？
> → 不同群之间怎样比较和压缩？
> → 群怎样作用在具体对象上？
> → 怎样把抽象群元变成矩阵？
> → 怎样把矩阵表示分成不可约块？
> → 不可约块怎样决定简并、选择定则和耦合？
> → 连续旋转为什么需要 SU(2) 而不只是 SO(3)？
> → 多粒子置换怎样组织全同粒子态？
> → 一般连续群怎样由 Lie 代数、根和权分类表示？
> → Lorentz/Poincaré 怎样分类相对论场和粒子？
> → 规范群怎样组织标准模型场？

“先一般后特殊”仍然成立，但一般理论的入口必须由一个具体困难打开。

---

## 3. 建议的新目录

### 第一部分 群的基本结构

1. 群、循环群与最初的对称操作
2. 子群、陪集与 Lagrange 定理
3. 同态、正规子群、商群与群作用
4. 共轭类、有限群结构、Sylow、直积与半直积

Jordan–Hölder、可解群视篇幅放 ch04 后半或附录。

### 第二部分 有限群表示

5. 线性表示、等价与不可约性
6. Schur 引理、Maschke 定理与特征标
7. 投影算符、正则表示与不可约分解
8. 张量积与 Clebsch–Gordan 分解

### 第三部分 空间对称与量子力学

9. 点群与 Schoenflies 符号
10. 空间群、Bloch 定理与小群
11. 对称性、简并、微扰与选择定则
12. 时间反演与对称性破缺

### 第四部分 旋转、角动量与置换

13. SO(3)、SU(2) 与二重覆盖
14. 旋量、自旋与双群
15. 角动量耦合与不可约张量
16. 置换群、Young 方法与全同粒子

### 第五部分 Lie 群与粒子物理

17. Lie 群、Lie 代数、指数映射与伴随表示
18. Cartan 子代数、根、权与最高权
19. SU(3) 表示与夸克模型
20. Lorentz 群与有限维场表示
21. Poincaré 群、Casimir 与 Wigner 分类
22. 规范群与标准模型表示结构

Weyl 特征标公式可以放 ch18 后半；Yang–Mills 拓扑、SU(5)、seesaw 退出主线，放附录或另册。

---

## 4. 原 ch01：必须拆开，保留它“说人话”的优点

### 新 ch01：群是什么

原稿这段应保留其精神：群的“乘法”不是普通数乘，而是操作复合。第一次定义群之前先拿整数加法、矩阵乘法、旋转复合对照，让读者知道抽象公理从哪里来。

本章只做到：

- 二元运算；
- 群四公理；
- 单位元与逆元；
- 元素阶；
- 循环群；
- 一个最简单几何对称群。

定义后立刻算，不要连续定义。比如定义元素阶后立即算 \(C_4\) 各元素的阶。

### 新 ch02：子群、陪集与 Lagrange

先问：“一个大群里只取某些操作，什么时候它们自己仍构成群？”由此进入子群。

接着问：“怎样按一个子群把整个群无重叠地分块？”由此出现左/右陪集。Lagrange 定理完整证明后立刻给三个后果：

- 子群阶整除群阶；
- 元素阶整除群阶；
- 素数阶群为什么必为循环群。

不要在同一章继续冲到 Sylow。

### 新 ch03：同态、正规子群、商群与群作用

同态从“两个看似不同的群是否有相同复合结构”进入。做一个模映射或符号映射，让核和像真的算出来。

然后自然解释：想把核中的元素看成“等价于单位元”，其陪集要能组成群，为什么需要正规性。商群和第一同构定理由此出现。

群作用放本章后半：群本身的乘法是一回事，群怎样移动一个集合中的对象是另一回事。轨道—稳定子由此推出。

### 新 ch04：有限群结构

有了共轭作用以后，类方程自然出现。Cauchy、Sylow 随后回答“群阶里含某个素因子时，群里必须有什么子群”。

这里可以完整处理 5 阶、6 阶等小群分类，让 Sylow 不只是三条背诵条件。

直积和半直积放最后。半直积不要只给符号 \(N\rtimes H\)，至少用一个二面体群说明“一个子群怎样作用在另一个正规子群上”。

Jordan–Hölder/可解群若保留，明确它们回答“群能否逐层拆成简单商”。

---

## 5. 原 ch02：表示论拆成四个台阶

### 新 ch05：为什么需要表示

知道抽象群怎样相乘，并不能直接算量子态、振动模式或坐标怎样变化。表示把群元送到线性变换，使抽象对称变成矩阵计算。

定义 \(D(g_1g_2)=D(g_1)D(g_2)\) 后立即用 \(C_3\) 或小点群做一个矩阵例子。等价表示由“换基不应改变物理内容”引入。

### 新 ch06：不可约表示、Schur、Maschke 与特征标

先给一个可约矩阵表示，实际找到不变子空间，然后才定义不可约。

Maschke 定理的平均内积构造应完整写；Schur 引理由“与所有群元对易的算符”引出。特征标回答“能否不携带整个矩阵也判断表示分解”，因此放在这些概念之后。

特征标正交关系的证明不要跳掉群平均和 Schur 这一步。

### 新 ch07：投影算符与正则表示

投影算符必须真正作用到一组基函数/振动坐标上，得到对称适配线性组合。然后再讲正则表示为何包含每个不可约表示若干次。

### 新 ch08：张量积与 CG

中心问题是组合系统。先写 \(D^{(1)}\otimes D^{(2)}\)，用特征标算不可约分解重数；再引入 CG 系数作为基变换系数。

至少完整做一个有限群例子，并在后面的 SU(2) 章节再做两个自旋 \(1/2\) 的例子。

---

## 6. 原 ch03–ch04：空间对称和量子应用重新排序

### 新 ch09：点群

从“把一个分子/物体旋转或反射以后是否与原结构完全重合”开始，而不是从 \(O(3)\) 子群分类开始。

顺序建议：恒等 → 旋转 → 镜面 → 反演 → 反旋转 → 主轴/副轴 → Schoenflies 命名。每介绍一种符号，都用一个真实几何结构判一次。

平面结构要把几个容易混淆点说清：分子平面是镜面对称候选；是否有反演中心取决于每个原子是否能映到同种原子；具有 \(C_4\) 自动含 \(C_2\) 子操作，但“属于哪个点群”取决于全部对称操作集合而不是只看最高阶轴。

### 新 ch10：空间群、Bloch 与小群

无限晶体多了平移。由 Bravais 平移群出发，说明非平凡点操作和分数平移怎样形成空间群。不要把 230 个空间群分类当主线。

Bloch 定理由平移表示直接推，随后 reciprocal lattice、Brillouin zone、小群。小群真正回答的是“固定某个 \(\mathbf k\) 后还有哪些对称保留这个波矢到等价类中”。

### 新 ch11：量子对称、简并、微扰和选择定则

从
\[
[H,U(g)]=0
\]
推 Hamiltonian 在不可约表示空间上分块，Schur 引理给简并。随后再问微扰保持的子群变小后，原不可约表示如何分裂。

选择定则从矩阵元在群下必须含平凡表示推出。红外、Raman、电子偶极等不要各自变成一串规则；选一两个把群论逻辑算完整，其余做表或习题。

### 新 ch12：时间反演与破缺

时间反演是反幺正，和普通酉表示不同，应该单独讲。Kramers 简并从 \(T^2=-1\) 推出。

对称性破缺只讲群—子群、简并极小值和序参量表示的最小框架；完整 Landau 理论可放 AdvancedPhysics。

---

## 7. 原 ch05：SO(3)/SU(2) 应拆三章

### 新 ch13：SO(3)、SU(2) 与二重覆盖

章首问：三维旋转矩阵已经描述所有空间旋转，为什么量子态还需要另一个群？

从 SO(3) 无穷小旋转推角动量代数，再构造 SU(2)
\[
U(\hat n,\theta)=\exp[-i\theta\hat n\cdot\sigma/2].
\]
实际算 \(2\pi\) 旋转得到负号、\(4\pi\) 回原态，然后才解释二重覆盖。

拓扑语言可以补充，但不应在读者还没看到符号变化前先讲 \(\pi_1(SO(3))\)。

### 新 ch14：旋量、自旋与双群

旋量由“矢量表示无法容纳半整数角动量”逼出。解释 Pauli spinor 怎样变换、为什么不能当普通空间矢量。

分子双群放这里最自然：点群有半整数自旋后，需要把 \(2\pi\) 旋转与恒等操作区分。

### 新 ch15：角动量耦合与不可约张量

两个自旋 \(1/2\) 完整构造 triplet/singlet，再抽象到 \(j_1\otimes j_2\)。CG 系数就是 uncoupled/coupled bases 的变换矩阵。

不可约张量算符随后进入，Wigner–Eckart 定理由群表示结构推出；选择定则说明是几何系数为零，而不是“神秘规则”。

---

## 8. 原 ch06：Young 方法保留，但不要被 Example 环境切碎

开场从全同粒子开始：交换粒子标签不应产生新的物理配置，那么多粒子 Hilbert 空间怎样组织交换对称性？这时才引入 \(S_N\)。

顺序：

1. 置换与循环分解；
2. 共轭类对应循环类型；
3. Young 图标记不可约表示；
4. Young symmetrizer；
5. \(S_3\) 做一个完整表示构造；
6. boson/fermion 是完全对称/完全反对称表示；
7. 自旋与轨道对称怎样组合成总反对称；
8. Frobenius characteristic / Littlewood–Richardson 放最后作为高级工具。

原章很多低阶变体移到习题。正文只保留能推动理解的例子。

---

## 9. 原 ch07–ch08：必须从头重建连续群与粒子物理

### 新 ch17：Lie 群与 Lie 代数

当前原 ch08 一上来就是“Lie 代数、根与最高权”，中间缺了最重要的桥。

先从一参数旋转
\[
R(\theta)=e^{\theta X}
\]
说起：连续群有无穷多个元素，但单位元附近的切向量是有限维的，生成元和它们的交换关系编码局域结构。

必须讲清：

- Lie group 的 tangent space at identity；
- left/right translation；
- Lie bracket；
- structure constants；
- exponential map；
- adjoint representation。

SO(3) 或 SU(2) 全程做具体参照。

### 新 ch18：Cartan、根、权与最高权

这是全书最需要降速的部分。

先问：一个高维半单 Lie 代数有很多不对易生成元，怎样系统标记不可约表示中的态？最大可交换生成元可以同时对角化，于是本征值组就是“权”。其余生成元会把权态搬到另一个权态，位移向量就是“根”。

顺序固定为：Cartan → weight → root operator → positive/simple roots → Cartan matrix/Dynkin → fundamental weights → highest weight → Weyl reflections。

每个一般概念先在 SU(2)/SU(3) 图上看见，再写一般定义；但一般结论必须独立证明，不能说“SU(3) 类似推广”。

### 新 ch19：SU(3) 表示与夸克模型

先算 \(\mathfrak{su}(3)\) 的 rank 2、simple roots、fundamental weights；画 \(\mathbf3,\bar{\mathbf3},\mathbf8\) 权图。然后完整求
\[
\mathbf3\otimes\mathbf3=\mathbf6\oplus\bar{\mathbf3},\qquad
\mathbf3\otimes\bar{\mathbf3}=\mathbf8\oplus\mathbf1.
\]

再解释 flavor SU(3) 与 color SU(3) 是两个物理角色不同的群，避免混淆。

### 新 ch20：Lorentz 群与有限维场表示

原 ch07 263 行必须扩成真正教材章。

从 Minkowski metric invariance 推 Lorentz condition，再无穷小展开得到 \(M^{\mu\nu}\)。定义
\[
J_i=\frac12\epsilon_{ijk}M^{jk},\qquad K_i=M^{0i}
\]
并完整推交换关系。

随后令
\[
A_i=\frac12(J_i+iK_i),\quad B_i=\frac12(J_i-iK_i),
\]
展示 complexified Lorentz algebra 分成两个 \(\mathfrak{su}(2)\)，于是有限维不可约表示标记 \((j_L,j_R)\)。

逐个解释：scalar \((0,0)\)、left/right Weyl spinors、vector \((1/2,1/2)\)、Dirac spinor 是直和。Clifford algebra 只作为构造 gamma matrices/Dirac spinor 的工具。

### 新 ch21：Poincaré 群与 Wigner 分类

必须先把两个问题分开：

- 场在 Lorentz 变换下属于哪个有限维表示；
- 单粒子 Hilbert 空间属于 Poincaré 的哪个不可约酉表示。

Poincaré 是 Lorentz 与 translation 的半直积。推 Casimir \(P^2,W^2\)，然后：

- massive：标准四动量 → little group SO(3)/SU(2) → spin；
- massless：标准 null momentum → little group → helicity；
- 连续自旋表示不进入主线。

Pauli–Lubanski 不能只报定义，必须说明它为什么与总角动量中“依赖原点的轨道部分”不同，能抽出内禀自旋。

### 新 ch22：规范群与标准模型表示

只回答“场怎样装进 \(SU(3)_C\times SU(2)_L\times U(1)_Y\) 表示”。

顺序：

1. global symmetry 到 local symmetry 为什么需要 gauge connection；
2. representation 决定 covariant derivative 中 generator 怎样作用；
3. 一代 fermions 的表示；
4. Higgs doublet；
5. \(Q=T_3+Y\)；
6. Yukawa invariant 怎样限制 hypercharge；
7. anomaly 若保留，只说明表示选择为什么受约束。

原 ch08 中 Yang–Mills topology、SU(5)、seesaw 全部移附录/其他书。

---

## 10. 99 个 Example 怎样处理

不要为了“新手友好”继续增加 Example。先把现有 99 个分三类：

**A. 保留为独立完整算例**：确实需要半页以上计算，且后文会引用。

**B. 融进正文**：刚定义完以后两三行验证、简单群表、简单矩阵表示。直接用自然文字和公式讲完。

**C. 移习题**：重复练习、同型低阶群、多个点群识别、类似字符表分解。

全书每章有 0–3 个真正显式 Example 就已经足够。目标不是数量，而是让主线不再像卡片集合。

---

## 11. 叙述风格的具体要求

### 开场

不要“本章介绍……”。例如 Lie 群章应先说：有限群可以逐个列元素，旋转群却有连续无穷多个元素；直接列群乘法几乎无从下手。我们需要把问题缩到单位元附近，看一条连续群曲线最初朝哪个方向走。这个切向信息就是 Lie algebra 的入口。

### 定义

先让对象解决问题，再给名字。定义后立即算。

### 定理

先说定理为什么值得证明。Sylow 不是因为“群论课程必须有”，而是因为只知道群阶时，它仍能强迫某些子群存在并限制子群数量。

### 章末

不要“本章建立了统一框架”。直接留下下一问。例如表示章末：现在会把一个群变成矩阵了，但一个给定矩阵表示仍可能包含重复的对称类型；下一章要解决怎样把它拆成不可约块。

---

## 12. 推导详实程度

必须完整或足够详细地给出：

- Lagrange theorem；
- first isomorphism theorem；
- class equation；
- Sylow 核心证明或明确引用边界；
- Maschke averaging；
- Schur lemma；
- character orthogonality；
- projection operator；
- SU(2) → SO(3) double cover；
- spin-1/2 tensor product；
- one Young symmetrizer construction；
- Lie bracket/exponential；
- SU(3) root/weight construction；
- Lorentz \((j_L,j_R)\) decomposition；
- Poincaré Casimir/little group；
- one Standard Model gauge invariant check。

成熟分类表和大量字符表不必逐项证明。

---

## 13. 语言、图形与工程

- 正文中文；人名/标准缩写/数学符号例外。
- `representation/little group/root/weight` 写“表示/小群/根/权”。
- 不新增 preamble 教学宏。
- 不做“群论知识地图”“逻辑流程框”。
- 定义/定理环境可以保留，但不要用它们切碎普通叙述。
- 普通公式不 `\boxed`。
- 图真正用于点群几何、晶体、权图、Dynkin 图、群作用轨道；不画抽象流程示意。
- 新章全部重做语义 label。

---

## 14. 执行顺序

### P0

拆 ch01/ch02/ch05；重排 ch03–04；废止 ch07–08 边界并新建 ch17–22。

### P1

以现 ch01 前几页“二元运算说人话”的语气作为样本，逐章重写入口和转场。

### P2

集中完成 Lie/root-weight/Lorentz/Poincaré/SM 六章，这是全书真正缺口。

### P3

清理 99 个 Example，分为保留/融入/移习题。

### P4

统一中文术语、图、引用、习题答案和编译。

---

## 15. 最终验收否决项

- ch01 仍一口气讲到 Sylow/Jordan–Hölder/半直积；
- ch07–08 仍保留 263/448 行式概览；
- 根和最高权在 Lie 群/Lie 代数尚未真正建立前出现；
- Lorentz 场表示与 Wigner 粒子分类仍混为一件事；
- 标准模型、Yang–Mills 拓扑、GUT、seesaw 仍挤在一个短章；
- Example 环境仍高密度打断正文；
- 定理名和术语比解释多；
- 读者会背 Schoenflies、CG、根系，却答不出它们分别解决了哪个物理问题。

---

## 十、逐原章动作清单：GroupTheory 的关键不是继续加内容，而是重新分配“第一次学”的速度

| 当前章 | 主要病灶 | 必须保留 | 必须移动/删除 | 重写后落点 |
|---|---|---|---|---|
| ch01 群基本概念 | 3123 行、9 section、22 Example，一章承担从群公理到 Jordan–Hölder/半直积 | 群、子群、陪集、正规子群、同态、群作用、D3 贯穿例 | Sylow/Jordan–Hölder/可解群后移；简单 Example 并入正文或习题 | 新 ch01–04 |
| ch02 表示论 | 1996 行、13 Example，正则表示/特征标/张量积都拥挤 | 表示、不可约、Schur/Maschke、character、projection、tensor product | 过多低阶群表格移习题/附录 | 新 ch05–08 |
| ch03 点群/空间群 | 点群分类、空间群、晶体表示混合 | Schoenflies、晶体点群、空间群最小接口 | 一般空间群技术与小群分开 | 新 ch09–10 |
| ch04 群论与量子 | 简并/微扰/选择定则/Bloch/时间反演/破缺全塞一章 | 简并、投影、选择定则；Bloch 与小群；时间反演 | 红外/Raman/和频细节按主线取舍；对称破缺另成段 | 新 ch11–12 |
| ch05 SO(3)/SU(2)/旋量/CG | 2637 行、24 Example，两个巨大认知转折同章 | SO(3) 几何、SU(2) 二重覆盖、旋量、CG、Wigner–Eckart | 重复低阶例并入正文；双群后置 | 新 ch13–15 |
| ch06 置换群/Young | 内容完整但例题过密 | 共轭类、Young 图、Specht/表示、全同粒子、LR | 低阶 S_n 表格减少；对称函数高级部分后移 | 新 ch16 |
| ch07 Lorentz/Poincaré | 264 行，严重欠展开 | Lorentz 代数、有限维场表示、Clifford、Poincaré Casimir、Wigner | 群上 Plancherel 若不服务粒子分类则移附录 | 新 ch20–21 |
| ch08 Lie/根/SM | 449 行，最难主题压成概览 | Lie algebra、Cartan、root/weight、highest weight、SU(3)、SM representation | Yang–Mills 拓扑、SU(5)、seesaw 若非主线移附录/AdvancedPhysics | 新 ch17–19、22 |

### 最重要的平衡动作

- 前六章总量不能原样保留再给 ch07–08 扩写，否则全书会膨胀成两倍但仍前重后轻。
- 必须从 ch01–06 **回收篇幅**：减少重复 Example、重复定义、低阶算表，把空间让给 Lie/Poincaré/根权。
- “例子多”不是新手友好的充分条件。99 个 Example 中很多只是定义的直接代入，应写回正文一句话，只有真正改变理解的例子才独立保留。

---

## 十一、前四章应该怎样慢下来，但不是变啰嗦

### 新 ch01：群是什么——先让操作复合起来

保留原稿最好的地方：从旋转/反射等操作的先后复合进入。第一章只完成：

- closure/associativity/identity/inverse 的必要性；
- cyclic group；
- 最简单的 D3/C3v；
- 子群的直观概念。

不要在第一章讲 Sylow、Jordan–Hölder、半直积。

完整算例：正三角形的六个对称操作，真正写出部分乘法表，解释为什么反射与旋转不对易。

章末问题：大群里一个子群占“多大”？这逼出陪集。

### 新 ch02：陪集和 Lagrange——为什么子群大小整除群阶

先把群元素按左陪集分块，让“每块大小都等于 |H|”从双射直接看出来，再给 Lagrange。

Cauchy 定理可在此作为应用，但不要马上进入完整 Sylow 理论。至少做一个“为什么 6 阶群必有 2/3 阶元素”的例子。

### 新 ch03：正规子群、商群、同态

问题入口：若想把群中的一批操作“视为同一种”，什么时候乘法仍然定义良好？这自然要求正规子群。

顺序：

- 同态先作为“保持乘法的压缩”；
- kernel 自动正规；
- cosets 形成 quotient；
- first isomorphism theorem；
- D3→C2 或其他明确例子。

不要先定义商群再解释为什么需要正规。

### 新 ch04：群作用、共轭与有限群结构

群作用从“群如何实际作用在对象集合上”进入。orbit/stabilizer 后再讲 conjugation action、class equation。Sylow 定理现在才有足够背景。

Jordan–Hölder/solvable 若保留，放本章最后作为“怎样逐层拆群”的高级出口，不作为初学主线核心。

---

## 十二、表示论必须从“抽象群怎样作用在线性态空间”进入

### 新 ch05：表示与不可约性

不要开篇列 homomorphism 定义。先回到群作用：量子态、振动位移、轨道基都是向量，群作用若保持线性，就由矩阵表示。然后才定义 representation `D(g)`。

定义后立即算 D3/C3v 的二维表示，验证乘法保持。

### 新 ch06：Schur、Maschke 与分块

问题：一个大矩阵表示能否分成互不混合的小块？先让一个可约表示实际出现，再定义 invariant subspace / irreducible。

Schur 引理不是孤立定理，要直接解释为什么与 Hamiltonian 对称性和简并有关。

### 新 ch07：特征标和投影

先指出“逐个求相似变换太麻烦，而 trace 在相似变换下不变”，由此引出 character。正交关系推完后立即做 projection operator，把一个具体振动/轨道空间投到 irreps。

### 新 ch08：张量积与 CG

问题：两个系统各自按表示变换，合在一起怎样变换？先写 tensor product representation，再问如何分解。CG 系数就是不同耦合基之间的变换矩阵。

---

## 十三、空间对称与量子应用：不要把“应用”写成第二本百科

### 点群/Schoenflies

先从一组具体三维分子/晶体结构识别对称操作；说明主轴、垂直 C2、镜面、反演分别怎样改变点。再给 C_n、D_n、C_nv、D_nh 等命名规则。

用户曾经问过“平面结构的 C2h 是否能同时有反演”“C4 是否也自动包含 C2/C1”，这些正是很好的教学问题，应在正文用群包含关系直接回答，而不是只列符号表。

### 空间群/Bloch

先从“平移群是无限离散群”进入；Bloch 定理的出现应由 Hamiltonian 与晶格平移对易逼出。小群要在“某个 k 点只有部分空间群保持它不变模倒格矢”时定义。

### 选择定则

不要先背“直积含全对称表示”。从矩阵元

`<f|O|i>`

在群变换下必须保持不变开始，推到 `Γ_f^*⊗Γ_O⊗Γ_i` 含平凡表示。然后再把红外/Raman 作为两个例子。

---

## 十四、SO(3)→SU(2)→自旋：全书最关键的“旧对象不够”之一

这一段必须像模范 QFT 那样把旧理论真的走到失败。

### 14.1 先讲 SO(3)

从三维旋转矩阵和角动量生成元开始，明确 SO(3) 的群结构和 Lie algebra。

### 14.2 再让半整数自旋制造困难

量子力学中自旋 1/2 态旋转 2π 后变号；这不是普通 SO(3) 的单值表示。不要一句“SU(2) 是 SO(3) 的 double cover”带过。

应实际写

`U(n,θ)=exp(-i θ n·σ/2)`

并比较 θ=2π 和 4π。读者看到 2π 给 -I、4π 才回 I 后，再引出覆盖映射 SU(2)→SO(3)。

### 14.3 旋量随后才是自然对象

先让 SU(2) 作用在二分量复向量上，再叫 spinor。不要先给“旋量是 Spin 群表示空间”的最高抽象定义。

### 14.4 CG/Wigner–Eckart 后接

多角动量耦合从 tensor product 出发；Wigner–Eckart 从旋转对矩阵元的约束出发。完整推导至少做一次 `1/2⊗1/2=1⊕0`。

---

## 十五、Lie 群与根权部分必须从头重建，不允许“扩写旧 ch08”

### 新 ch17：Lie 群和 Lie 代数

先从连续一参数群 `g(t)` 的切向量进入，得到 generator。说明 Lie algebra 是单位元附近的局部乘法信息，commutator 来自两个无穷小变换不对易。

必须推：

- exponential map；
- adjoint representation；
- structure constants；
- Killing form 至少解释用途；
- SU(2) 作为第一个完整例子。

### 新 ch18：Cartan、根与权

问题入口：多个生成元不对易，怎样同时给表示态贴标签？选 maximal commuting Cartan subalgebra。

然后：

- weight 是 Cartan generators 的共同本征值；
- root 是 adjoint representation 中 ladder operators 的 weight；
- 用 SU(2) 回看根；
- 再进入 SU(3) 的二维 root diagram。

不要第一页就画 Dynkin diagram。

### 新 ch19：最高权、Dynkin 标签与 SU(3)

先让 raising operators 把权格推到顶部，说明有限维 irreps 必须有 highest weight；再构造表示。

必须完整算：

- SU(3) fundamental `3`；
- conjugate `3bar`；
- `3⊗3=6⊕3bar`；
- `3⊗3bar=8⊕1`；
- 与夸克 flavor/color 的表示含义分开说明。

Weyl character formula 可以作为 B 级结果，不要喧宾夺主。

---

## 十六、Lorentz/Poincaré 部分必须达到“可以独立学会”的程度

当前 ch07 只有约 264 行，完全不够。

### 新 ch20：Lorentz 群与有限维场表示

叙述顺序：

1. Minkowski interval 为什么要求 `Λ^TηΛ=η`；
2. 连通分支和 proper orthochronous subgroup；
3. 无穷小变换得到 `M^{μν}` Lie algebra；
4. 定义 `J_i` 和 `K_i`；
5. 组合成 `A=(J+iK)/2, B=(J-iK)/2`，得到两个 su(2)；
6. 因此有限维复表示标记为 `(j_L,j_R)`；
7. Weyl spinor `(1/2,0)` 和 `(0,1/2)`；
8. vector `(1/2,1/2)`；
9. Dirac spinor 是左右手表示直和。

每一步都必须说明“这个分解解决了什么分类问题”。

### 新 ch21：Poincaré 群与粒子分类

先说明场的有限维表示和物理单粒子 Hilbert 空间不是一回事。Poincaré irreducible unitary representations 才分类粒子。

必须推：

- semidirect product；
- Poincaré algebra；
- `P²` 和 Pauli–Lubanski `W²`；
- massive little group SU(2)→spin；
- massless little group ISO(2)→helicity（平移部分平凡时）；
- 为什么 `(j_L,j_R)` 不能直接当粒子自旋标签。

群上的 Plancherel/harmonic analysis 若不服务这一主线，移附录。

### 新 ch22：规范群与标准模型表示只讲“表示结构”

本书不是标准模型教材。只回答：场怎样放进 SU(3)×SU(2)×U(1) 表示，张量积怎样决定允许的 gauge-invariant coupling，Higgs vev 怎样在表示层面留下 U(1)_em。

不展开 loop、anomaly、GUT、seesaw，除非作为两三页延伸阅读。

---

## 十七、Example 的治理：99 个不是优势，本轮目标是“少而有用”

建议把现有 Example 分成三类：

### A 类保留

能改变理解、后文会反复引用的贯穿例：

- D3/C3v；
- NH3 振动；
- SU(2) spin-1/2；
- `1/2⊗1/2`；
- S3 Young `[2,1]`；
- SU(3) `3⊗3bar`。

### B 类并入正文

只验证一个定义或做两三行矩阵乘法的例子，不需要独立框。直接写“例如……计算得……”。

### C 类移习题

同一技术的第二、第三个变体，尤其低阶群的重复 character table。

重构后不设硬数量，但每章通常 0–3 个真正独立 Example 已足够。

---

## 十八、GroupTheory 的详实度分级

### A 级必须证明/推导

- Lagrange theorem；
- first isomorphism theorem；
- orbit–stabilizer；
- class equation；
- Schur lemma；
- character orthogonality/projection；
- tensor product decomposition 的一般结构；
- Bloch theorem 的群论推导；
- selection rule criterion；
- SU(2) double cover 及 2π/4π；
- CG `1/2⊗1/2`；
- Young 方法的一个完整低阶表示；
- Lie algebra 从无穷小群乘法得到；
- root/weight/raising-lowering；
- SU(3) 基本 tensor products；
- Lorentz algebra→su(2)⊕su(2)；
- Poincaré Casimir/little group/Wigner classification。

### B 级可引用

- Sylow theorem 完整证明可根据篇幅压缩；
- Jordan–Hölder；
- Weyl character formula；
- 高阶 LR combinatorics；
- 空间群完整分类。

### C/D 级移出主线

- Yang–Mills topology；
- SU(5)/seesaw；
- 群上 Plancherel 主系列；
- 与 MathSkills/QFT 重复的 Clifford 大全。

---

## 十九、加严验收否决项

- ch01 仍从群公理一路讲到 Jordan–Hölder/半直积；
- ch07–08 只是在原 264/449 行基础上“扩写一点”，而没有重新分章；
- Lie algebra/root/weight/highest weight 仍在同一个 section 连续出现；
- Lorentz finite-dimensional field representations 与 Poincaré unitary particle representations 仍混为一层；
- SU(2) double cover 仍只写结论，没有 2π/4π 的显式演算；
- 点群章节仍主要靠表格背 Schoenflies，而不解释各符号对应什么几何操作；
- selection rules 仍作为口诀，没有从矩阵元不变性推出；
- 前六章 Example 数量不减、后六章仍无完整算例；
- 标准模型部分扩成粒子物理百科，偏离“群表示”主题。
