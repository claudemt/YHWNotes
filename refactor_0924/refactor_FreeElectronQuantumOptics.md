# FreeElectronQuantumOptics 深度重构方案

## 一、原件诊断：这本书已经被“前置理论”吞掉了

这是四本书中最需要做结构性手术的一本。

表面上全书只有 11 个 `chXX.tex`，但正文通过 `\input` 递归展开后约 57327 行，约 5587 个公式环境、434 个 Derivation、约 1284 个 `\boxed`。`sections/` 目录下有约 198 个片段文件，其中大量文件名带 `dpXX`、`detail`、`extra`、`worked`、`derivation`。这说明现在的源码不仅内容极大，而且已经明显带有多轮增量修补痕迹。

更关键的是内容重心失衡：

- ch01 展开约 2074 行：Fourier/分布、Hilbert/投影、Gaussian/Grassmann 路径积分、Lie 群、微分几何、散射积分；
- ch02 约 4182 行：Lorentz/Poincaré、Wigner 小群、Weyl/Dirac、自作用量/Noether、Maxwell–Dirac、Maxwell Green；
- ch03 约 6906 行：自由场量子化、Wick/LSZ、散射、谱表示、unitarity/cuts、renormalization/RG/OPE/heat kernel、BRST、SSB；
- ch04 约 7777 行：完整 QED，从 Dirac/Maxwell 场量子化一直到 Compton、Ward–Takahashi、单圈重整化、软辐射、Schwinger、macroscopic QED；
- ch05 约 5648 行：一整套 QCD；
- ch06 约 7507 行：一整套标准模型；
- ch07 才正式进入“自由电子与量子激发”。

ch01–06 合计约 34094 行，占全书递归展开源码约 **59.5%**。换句话说，读者要先读完整本书六成，才到书名里的主题。

这不是“基础讲得太详细”，而是**书的身份已经混乱**：前六章是一套场论百科，后五章才是一套自由电子量子光学教材。

后五章也存在巨章混合问题：

- ch07 约 6372 行、43 个 Derivation，把一般系统/正常模、有限时间跃迁、Green 张量、EELS 类损失、相位匹配、单模、反冲格放在一起；
- ch08 约 3608 行，把经典外场 PINEM、有限脉冲、空间平均、量子 PINEM、Fock/thermal 响应和有限反冲联合量子格放在一起；
- ch09 约 2663 行，同时讲 Bloch 纤维、Floquet、高频有效 Hamiltonian、Kapitza–Dirac/Bragg/反冲格；
- ch10 约 6038 行，把自由传播/阿秒聚束、开放系统、量子测量、QFI、层析、条件测量、统计反演全部压成一章；
- ch11 约 4604 行，把介质响应、辐射、周期介质、混合模式、EELS/CL/LDOS、Compton、整形电子、成像、实验反演和收集通道放在一起。

因此，本书不能继续沿 11 章框架精修。**必须先重新定义书名所承诺的主线，再把前置理论降为最小接口，把 ch07–11 拆成真正的自由电子量子光学课程。**

---

## 二、模范量子场论讲义对这本书最重要的启发

前面的量子场论模范教材有几个写法尤其适合本书。

### 1. 先让旧理论撞墙

模范教材不是开篇宣布“量子场论很重要”，而是把 Klein–Gordon 单粒子解释、Dirac 负能海等方案一步步走到困难，再让量子场出现。

自由电子量子光学也应如此。不要第一章先讲 Fourier、Grassmann、Poincaré。应该先把真正的问题摆出来：

- 经典电子光学会告诉我们轨迹、能量调制和辐射；
- 实验却看到以 \(\hbar\omega\) 为间隔的离散边带；
- 强场时边带人口会消失又复现；
- 量子光场还可能与电子纠缠；
- 自由传播可以把能量相位结构转成阿秒时间结构。

于是读者自然会问：**电子究竟应该用怎样的量子态描述？光/材料环境怎样与它交换能量和相位？哪些现象用经典场就够，哪些必须量子化？**

这才是本书第一章。

### 2. 先完整看一个物理问题，再抽象工具

模范教材讲辐射修正时，先拿 \(e^+e^-\to\mu^+\mu^-\) 展示顶角修正、自能、真空极化、箱图、实辐射，读者先知道“圈图到底给我们制造了什么困难”，然后才退回 \(\phi^4\) 系统讲正规化和重整化。

本书也应选 PINEM 或 EELS 作为“预演问题”。例如在导论中先用不完全推导但严格定义的方式展示：
\[
P_n=J_n^2(2|\beta|)
\]
意味着什么、实验看到什么、为什么这要求相干振幅而不只是跃迁概率。然后才在后面的章节真正从 Hamiltonian/Dirac/QED 推出它。

### 3. 定义后立即让对象做事

原稿很多高级对象定义后会继续补性质。重构后应像模范教材那样，定义能量平移算符后马上作用到 \(|n\rangle\)，定义 Green 张量后马上算一个电子电流的场或损失概率，定义 reduced density matrix 后马上算一次偏迹。

### 4. 每个核心公式后说“所以它到底告诉我们什么”

用户给出的 PINEM 论文讲解是本书最直接的风格样本：

- 写出 \(\hat S=\exp(g^*a-ga^\dagger)\) 后，不停在“这是幺正算符”，而是说**一个参数 \(g\) 同时控制整条能量梯**；
- 写出 \(J_n^2\) 后，马上说明零点意味着某个边带会被相干抽空再出现；
- 给电子束斑和近场尺度，不是做参数表，而是解释为什么时空平均不会洗掉振荡；
- 区分“实验直接看到”“理论预测”“数值模拟”。

整本书都应采用这种声线。

---

## 三、重新定义本书范围

这本书的正文主线只服务一个问题：

> 自由电子与经典/量子电磁环境发生有限时间相互作用以后，电子的能量、动量、相位、相干性、纠缠和辐射如何改变；这些改变怎样传播到探测面，并怎样从实验数据反演出来？

凡是不能直接服务这条主线的内容，不再因为“理论完整性”留在主先修链。

### 必须移出主线

- 完整 QCD；
- 完整标准模型；
- 一般 Higgs/CKM/PMNS/anomaly/RG/weak process；
- 与自由电子光学无直接关系的 OPE、heat kernel、BRST 全套、一般 SSB；
- 一般高阶 QED 辐射修正的完整专著式计算。

这些内容可以有三个归宿：

1. 移入独立的 `FieldTheoryCompanion`；
2. 作为不参与主先修关系的附录；
3. 若其他讲义已经覆盖，直接删除重复。

**QCD 和标准模型绝不能再位于读者进入自由电子量子光学前的必读链上。**

### 主线中只保留的 QFT/QED 最小接口

- relativistic electron states/Dirac current；
- minimal coupling；
- 正负能与正能投影在需要时的受控近似；
- Maxwell Green tensor；
- quantized EM normal modes/Fock/coherent states；
- interaction picture/Dyson 或等价有限时间演化；
- Fermi golden rule 作为长时间极限；
- 必要的 one-photon emission/absorption matrix element；
- 需要 macroscopic QED 时再引入 reservoir/Green tensor quantization。

不为“证明自己懂 QED”而保留 Compton、one-loop Ward、Schwinger 等完整推导，除非后面的自由电子问题真的调用它们。

---

## 四、建议的新主目录

### 第一部分：问题、电子与场

1. 自由电子量子光学在问什么
2. 相对论电子、波包与电磁最小耦合
3. Maxwell Green 张量与电子产生的场
4. 量子化电磁场与电子—光子相互作用

### 第二部分：从一般相互作用到可观测跃迁

5. 有限时间散射、相位匹配与能量交换
6. 电子电流、Green 张量与 EELS/CL 的一般表达
7. 单模投影、有效耦合与反冲能量格

### 第三部分：经典光驱动的自由电子

8. PINEM：外场相位调制与 Bessel 能量梳
9. 有限脉冲、空间平均、相位可见性与实验标定
10. 有限反冲：从均匀能量梯到 Bragg/Kapitza–Dirac 动力学
11. 周期驱动、Bloch/Floquet 与反冲格

### 第四部分：量子光驱动与量子交换

12. 量子 PINEM 的一般电子—光联合动力学
13. Fock、相干、热光场下的边带统计
14. 电子—光纠缠、条件测量与非经典态制备

### 第五部分：传播、退相干与测量

15. 自由传播、色散与能量相位到时间密度的转换
16. 阿秒聚束、Talbot 传播与时间透镜
17. 电子特定的开放系统与退相干
18. 电子能谱测量、相位读出与量子层析
19. 条件测量与统计反演

### 第六部分：介质、辐射与成像

20. 介质 Green 响应与电子能量损失
21. 阴极发光、界面辐射与混合模式
22. 周期介质、Cherenkov/Smith–Purcell 类运动学与结构化模式
23. 近场成像、收集通道与实验反演

### 附录/伴随材料

A. Fourier、分布和连续态归一化
B. 投影算符和有效 Hamiltonian
C. Dirac/Weyl 代数表
D. QFT/QED 更完整的背景（若坚持保留）
E. QCD/标准模型迁移说明或外部讲义引用

这个目录的关键变化不是章节数从 11 增到 23，而是读者在第 1 章就进入“自由电子量子光学”，而不是先读六章另一门课。

---

## 五、现 ch01：数学工具必须降为按需调用的附录

当前 ch01 约 2074 展开行，包含 Fourier/分布、Hilbert/投影、Gaussian/Grassmann、Lie 群、微分几何、散射积分。它已经是一章“数学物理方法速成”，但对自由电子主线的大部分内容不是即时依赖。

### 必须做的手术

- Fourier/分布保留最小约定，移到附录 A；
- Hilbert 连续态归一化和投影保留，分散到电子态与有效 Hamiltonian 真正使用处；
- Gaussian/Grassmann 路径积分从主线删除；
- Lie 群、微分几何从主线删除；
- loop integrals 从主线删除；
- sinc 长时间极限移到“有限时间跃迁 → FGR”章节，在那里从有限时间积分自然得到。

### 原则

“前置知识”不应该要求读者在不知道将来为什么用的情况下先学完。需要 Fourier 归一化时就说明 Fourier 约定；需要 delta 分布时再回指附录。

---

## 六、现 ch02：压缩为“相对论电子与经典电磁场”两章

当前 ch02 约 4182 行，Lorentz/Poincaré/Wigner/Weyl/Dirac/Noether/U(1)/Maxwell–Dirac/Green 全部齐全，远超本书入口所需。

### 新 ch02：相对论电子、波包与最小耦合

**章首问题**：自由电子在 keV–MeV 能区运动时，为什么不能一直用 \(p^2/2m\)，而又为什么很多实验最后仍能得到一个单向传播的有效 Schrödinger 方程？

顺序：

1. relativistic dispersion \(E(\mathbf p)\)；
2. Dirac equation 从最小耦合写起，明确 \(q=-e\)；
3. 自由正/负能解、归一化、完备性；
4. wave packet 与中心动量；
5. current \(j^\mu\)；
6. 外电磁场中的最小耦合；
7. 正能子空间投影与什么时候可以忽略 pair creation；
8. 沿主传播方向做窄带/旁轴/低反冲近似，明确小参数。

Poincaré 代数和 Wigner 分类只保留理解 Dirac 态标签所需最小内容，详细证明移到 MathSkills/GroupTheory。

### 新 ch03：Maxwell Green 张量

**章首问题**：电子沿一条轨迹经过复杂纳米结构时，每换一个源都重新解 Maxwell 方程太低效；怎样把环境响应封装成一个对象？

从 Maxwell 方程 → 频域算子 → Green 张量定义 → 边界条件 → 源场卷积。然后马上用一个点偶极或电子电流算场。

这里才解释 Im Green 与局域态密度/耗散通道的关系，不要提前铺 macroscopic QED 全套。

---

## 七、现 ch03–ch04：完整 QFT/QED 课程必须收缩成最小接口

### 新 ch04：量子化电磁场与电子—光子相互作用

这章可以借鉴模范 QFT 教材“标量场是无穷多个谐振子”的讲法，但更直接：

1. 先取一个腔模，经典能量就是一个谐振子；
2. 量子化得到 \(a,a^\dagger\)；
3. 推到多模场；
4. Fock 与 coherent states 在真正需要时定义；
5. 写 electron–field interaction Hamiltonian；
6. 算一次单光子吸收/发射矩阵元；
7. 再说明复杂介质可由正常模或 Green 张量表示。

无需先完整量子化标量场、证明 Wick、LSZ、renormalization、BRST。

### QFT 背景的处理

现 ch03 里以下内容从主线移出：

- scalar toy 全套；
- Wick theorem 的一般组合学；
- LSZ 一般证明；
- crossing/dispersion；
- spectral representation 全套；
- unitarity cuts；
- renormalization/RG/OPE/heat kernel；
- BRST；
- SSB/Higgs。

若需要散射语言，只在有限时间相互作用章节定义 \(S\)-matrix/interaction picture 所需最少形式。

### 现 ch04 QED

保留：Dirac 场/电子态归一化的必要部分、光子模式、顶角、树级电子—光子相互作用、Ward identity 若用于证明规范不变性、macroscopic QED 接口。

移出主线：Møller/Bhabha/Yukawa 大量对照算例、Compton 完整截面、one-loop renormalization、Schwinger \(g-2\)、soft inclusive 全套。

Compton 若后文 ch11 当前“Compton 前向模型”确实需要，应在那里按实验前向模型重新引入，而不是为了 QED 课程完整性提前讲。

---

## 八、现 ch05–ch06：QCD 与标准模型退出主线

这是 P0 级硬要求。

### ch05 QCD

完整内容可以迁移到 `AdvancedPhysics` 的粒子物理部分或独立场论讲义。自由电子量子光学的核心推导不依赖：

- non-Abelian ghost rules；
- running coupling；
- Sudakov；
- DIS/Drell–Yan；
- lattice topology；
- chiral condensate。

它们不应占本书五千多行。

### ch06 标准模型

同理，Higgs、Yukawa、CKM、GIM、anomaly、weak widths、neutrino scattering、MSW 等不属于自由电子量子光学必修依赖。

若某个具体自由电子过程涉及弱相互作用，可在应用章节局部引入，不应该让所有读者先读七千多行 SM。

### 迁移方式

不要简单删除文件导致历史成果丢失。建议：

- 在重构分支中先移动到 `content/FieldTheoryCompanion/`；
- 修正文中反向引用；
- FreeElectronQuantumOptics 正文只留一段“本书聚焦电磁相互作用，强弱相互作用另见……”；
- 完成迁移后再决定是否并入其他书。

---

## 九、现 ch07：必须拆成三章

ch07 目前是自由电子主线真正开始的地方，章首其实已经比前六章好：它会说“前面建立 QED，现在问电子出射能量分布和相位怎样改变”。这种声线要保留，但内容量太大。

### 新 ch05：有限时间相互作用与能量交换

**中心问题**：电子与一个时间有限的扰动相互作用时，能量守恒为什么不是一开始就是 delta 函数，而会有有限宽度？

顺序：

1. interaction picture 精确传播；
2. 一阶振幅的时间积分；
3. 有限窗口得到 sinc；
4. 长时间极限才得到 Fermi golden rule；
5. 定义精确 mass-shell mismatch；
6. 说明 \(|\Delta|T\lesssim1\) 才是有限时间可分辨条件；
7. 多量子过程再进入 Dyson/中间态 resolvent。

原稿中很好的“低反冲不等价于 \(\hbar\omega/E_0\ll1\)”应保留并突出，但不要框起来；用一段人话解释实际占据的多个通道失谐都要小。

### 新 ch06：电子电流、Green 张量与 EELS/CL

从一般跃迁振幅中识别电子跃迁电流，再把环境自由度通过 Green 张量消去。明确：

- EELS 测的是电子丢失能量的概率分布；
- CL 测的是其中耦合到可收集远场光子的部分；
- Im Green 张量组织所有环境模，但不同实验投影不同通道。

先做一个平面界面或简单局域模的完整算例，再推广 QNM/continuum branch cut。当前 QNM residue normalization 等高阶内容后移。

### 新 ch07：单模投影与反冲格

只有在一般 Green/continuum 理论建立后，才把环境投影到一个窄线宽模式。由单次能量/动量交换得到通道 \(|\ell\rangle\)，写精确 \(\mathcal E_\ell=E(p_\ell)\)，再说明什么时候可以近似成等间隔梯。

反冲格振幅链应从 Hamiltonian 的矩阵元直接得到，不要把“平移对称能量梯”先当默认模型。

---

## 十、现 ch08：拆成经典 PINEM 与量子 PINEM 至少四章

### 新 ch08：经典 PINEM——相位调制怎样产生 Bessel 边带

这是全书最应该“像演讲”的一章。

建议直接模仿用户提供的论文讲解节奏：

1. 先说实验现象：电子经过光学近场后出现 \(\hbar\omega\) 等间隔边带；
2. 问：为什么不是一次吸收/发射两个峰，而是无限梯？
3. 从 Dirac/正能包络方程在低反冲、单向传播条件下约化；
4. 沿经典轨迹积分得到无量纲复耦合 \(\beta\)；
5. 明确 \(|\beta|\) 和 \(\arg\beta\) 分别控制什么；
6. 相位因子展开，逐步得到 \(J_n(2|\beta|)\)；
7. 概率 \(J_n^2\) 后立即解释：所有边带由一个耦合锁定，零点意味着相干抽空和复现；
8. 做概率归一化、均值/方差等 Bessel 恒等式验证；
9. 最后才说这可以理解为“能量空间衍射/相位调制”。

不要在这章混入光场 Fock 态。

### 新 ch09：有限脉冲、空间平均与实验标定

中心问题：理想 \(J_n^2\) 为什么实验上会被洗浅？

按用户论文讲解的方式，把参数都变成“回答问题”的数字：电子束横向尺寸与近场衰减长度比较、电子脉冲与光脉冲时长比较、速度失配、焦斑等。先写单电子给定 \(\beta\) 的条件分布，再对实验 ensemble 的 \(\beta\) 分布平均。

相位可见性、双脉冲 Ramsey/PINEM reference 放这里，因为它们回答“只测概率如何读出相位”。

### 新 ch10：有限反冲与 Bragg/Kapitza–Dirac

中心问题：什么时候均匀能量梯失效？

从精确 relativistic dispersion 算每条边的 detuning，逐步出现 recoil energy/Bragg resonance。再分 Raman–Nath/薄光栅、Bragg/少态等不同极限，明确控制参数。

### 新 ch11：周期势与 Floquet

现 ch09 的 Bloch/Floquet 不应和经典 PINEM 主推导夹在一起。先讲空间周期导致准动量和 Bloch fiber，再讲时间周期导致 quasienergy/Floquet。若同时周期，再说明两者如何组合。

高频 Floquet effective Hamiltonian 必须由 \(\Omega\) 大于内部动力学尺度的展开得到，写清 micromotion 仍然存在。

---

## 十一、量子 PINEM 必须成为独立大块，而不是 ch08 后半

### 新 ch12：一般电子—光联合动力学

**章首问题**：把光当经典场时，电子只获得确定的相位调制；如果光场本身有量子涨落，电子交换一个量子后，光场也会改变。此时不能只演化电子态。

从联合 Hilbert 空间开始，写最一般模式耦合。先单模，再多模。明确能量平移算符与光子升降算符分别作用在哪个空间。

推导时必须区分：

- classical prescribed field；
- coherent state large-amplitude limit；
- exact quantum exchange。

不能把相干态替换成 c-number 当作定义。

### 新 ch13：Fock、相干、热光场响应

每种输入态只回答一个物理问题：

- Fock：固定光子数如何限制吸收/发射不对称？
- coherent：为什么恢复经典 Bessel 调制；量子修正是什么量级？
- thermal：光子数涨落怎样把相干结构平均掉？

每个分布至少推一次从联合振幅到电子边带概率，不能只报闭式公式。

### 新 ch14：纠缠与条件测量

从联合态
\[
|\Psi\rangle=\sum_{n,m}c_{nm}|n\rangle_e|m\rangle_\gamma
\]
说明为什么单独电子态变混合。做一次偏迹。然后问：如果我们反过来测光子，会把电子投影到什么条件态？由此自然进入 heralding、conditional electron shaping，而不是突然切到量子信息术语。

---

## 十二、现 ch10：必须拆成五章

这是另一处最严重的混章。

### 新 ch15：自由传播与色散

现 ch10 开场已经很好：离开相互作用区后，能谱不变但相位继续演化。保留这个入口。

先用精确 relativistic phase
\[
e^{-iE(\mathbf p)t/\hbar}
\]
再对窄带 wavepacket 做 Taylor 展开，推横纵有效质量。每次近似给 phase error，而不是只说 \(\delta p/p_0\ll1\)。

### 新 ch16：能量梳到阿秒时间结构

中心问题：PINEM 刚离开近场时主要改变能量/相位，为什么传播一段距离后会变成密度脉冲？

从离散能量格的相对相位出发，写时间密度干涉项。二次谱相位 → 聚束距离 → Talbot/revival。Wigner 图只在这里帮助展示相空间剪切，不画流程图。

时间透镜作为“先给时间相关能量调制，再让色散转换”的应用放末尾。

### 新 ch17：电子特定的开放系统

不要再教一整套一般 OQS。只问自由电子在传播/与材料耦合时哪些未观测自由度会毁掉相干。

从一个具体模型：电子与一个环境模式/连续 bath 纠缠，偏迹后 \(\rho_{nn'}\) 获得 decoherence factor。再推广到 Gaussian noise/FDT、colored noise。若需要 Markov master equation，只给本系统实际需要的生成元并说明近似条件。

一般 GKSL 证明已经在 AdvancedPhysics，不重复。

### 新 ch18：电子能谱测量与相位层析

先明确普通 EELS/PINEM spectrometer 测到的是能量 POVM，只给 diagonal populations；相位信息为什么丢失？然后加可控 reference interaction，把相位旋转成可测人口变化，由此得到 tomography。

Fisher/QFI 只在回答“给定前向模型，什么参数能被多精确估计”时出现。一般量子估计理论不在本书重讲。

### 新 ch19：条件测量与统计反演

把条件光场仪器、计数核、inversion 放到同一清晰问题里：探测器读数 \(y\) 不是理想光子数 \(n\)，已知响应矩阵 \(R_{y|n}\) 后怎样从数据估计真实分布/条件态？

先写 forward model，再谈 inversion。正则化/先验只在病态真正出现后引入。

---

## 十三、现 ch11：拆成四章

### 新 ch20：介质响应与 EELS

从电子电流产生的频域场和 work \(\int j\cdot E\) 出发，推 loss probability。然后用 Green tensor 表示任意线性介质。

平面 Drude 界面做完整算例：模式极点/continuum、impact parameter、速度依赖、损失峰。这样抽象 Green 张量真正落地。

### 新 ch21：CL、界面辐射与混合模式

中心问题：同样是电子激发环境，为什么有些能量进入吸收/非辐射模，有些变成远场光？

分清 total loss、radiative LDOS/collection、detector aperture。Hopfield diagonalization 只有在强耦合混合模真正需要时出现。

### 新 ch22：周期介质与运动学辐射

把 Cherenkov、Smith–Purcell/周期阵列、phase matching 放在同一运动学框架里：电子的 \((\omega,\mathbf q)\) 支持与介质色散/reciprocal lattice 怎样相交。先画色散几何，再算谱。

### 新 ch23：成像与实验反演

把近场 spectrum imaging、collection geometry、detector response、regularized inversion 放在最后，因为现在读者已经知道 forward model 的每一层。

章节应明确区分：

- 理论场/Green tensor；
- 电子实际耦合；
- 光学收集；
- 能谱/相机 detector response；
- 最后数据反演。

这样“实验反演”不是额外专题，而是把整本书的 forward chain 反过来。

---

## 十四、第一章应该彻底重写：给整本书定声线

建议新 ch01 不超过普通章节长度，但承担全书最重要的教学工作。

### 开头可以沿这样的认知顺序写

1. 一束高能电子经过没有光场的真空，能谱只有原来的峰；
2. 让它掠过被光照亮的纳米结构，会出现等间隔 \(\hbar\omega\) 边带；
3. 弱场时像吸收/发射少数光子，强场时却出现很多边带，甚至某一阶会消失后再回来；
4. 这说明不能把各边带当成彼此独立的跃迁概率；它们是同一个量子振幅演化的不同分量；
5. 若传播一段距离，能谱不变但相对相位改变，电子还会在时间上形成尖峰；
6. 若光场量子化，电子和光又会彼此纠缠；
7. 因此本书要解决的是“能量、相位、反冲、纠缠、传播、测量”这一整条链。

然后给一张**物理实验示意图**即可，不要画“全书逻辑流程框”。

### 导论只预览三个公式

可以预览但不完整证明：

- exact relativistic dispersion；
- classical PINEM \(P_n=J_n^2(2|\beta|)\)；
- Green tensor loss/radiation 的一般结构。

每个公式只回答“它最终会告诉我们什么”，正式推导留后文。

---

## 十五、叙述声线：以用户的 PINEM 论文讲解为直接范本

### 好的句子要有动作

原稿常写：

> 这一质量壳失谐把 PINEM、有限反冲格和少态共振统一成同一个运动学问题。

信息正确，但“统一成”仍像总结语。更适合正文的写法是：

> 当 \(\Delta_\ell\) 在实际占据的几个通道中都小到有限作用时间分辨不出来时，电子每向上或向下走一级几乎看到同样的共振条件，于是可以把这些通道看成均匀能量梯。反过来，一旦相邻 \(\Delta_\ell\) 的差别大到可以分辨，只有少数边仍接近共振，动力学就会自动收缩到有限几个通道。

先讲“发生什么”，最后一句再给术语。

### 数字必须回答一个问题

不要单列“典型参数”。例如写 120 keV、15 nm、90 nm、3.4 ps 时，必须告诉读者这些尺度比较为什么保证同一电子脉冲看到近似一致的 \(\beta\)。

### 实验、模拟、理论预测分开说

正文明确使用：

- “实验直接测到……”；
- “由模型拟合得到……”；
- “数值传播显示……”；
- “理论进一步预测……”。

不要把它们合成“结果表明”。

### 术语后置

先讲“不同能量分量传播后相位不同并在某处重新同相”，再说“这就是纵向聚束/时间焦点”。先讲“未探测光子携带了哪条路径信息”，再说“这导致退相干”。

---

## 十六、推导详实程度的硬要求

这本书最重要的数学链必须全部可复算。

### 必须算到底

- Dirac 正/负能自由解、归一化、current；
- 外场最小耦合到正能 envelope 的约化，所有近似条件逐一写；
- relativistic dispersion 到 longitudinal/transverse effective mass；
- finite-time integral 到 sinc 再到 FGR delta；
- exact recoil mismatch 与低反冲判据；
- Green tensor 从 Maxwell operator inverse 定义到电子 current 响应；
- EELS/CL probability 的 normalization 和单位；
- classical PINEM 从 trajectory phase 到 Jacobi–Anger/Bessel coefficients；
- Bessel normalization、moments、zero/oscillation 的物理读法；
- finite pulse/spatial averaging integral；
- quantum PINEM joint-state recursion 或 closed solution；
- coherent state classical limit；
- Fock/thermal response；
- recoil lattice → Bragg two-level reduction 的消元和误差；
- free propagation phase expansion and attosecond bunching；
- partial trace/decoherence factor；
- tomography forward model and identifiability；
- Green-response inversion 的 forward operator 与 regularization 条件。

### 可以引用而不机械展开

- 标准 Gaussian integral；
- 通用 group theorem；
- 已在 MathSkills 完整证明的 spectral theorem；
- 已在 AdvancedPhysics 完整证明的一般 GKSL theorem；
- 与主线无关的 QED loop integral。

### 每个近似必须有“精确式 → 小参数 → 截断后式 → 误差”

尤其检查：

- paraxial；
- eikonal；
- positive-energy projection；
- narrowband；
- low recoil；
- rotating wave；
- single-mode projection；
- Markov；
- Bragg/two-level；
- quadratic dispersion。

“高能电子”“弱耦合”“窄带”都不算数学条件，必须给无量纲量或 phase error。

---

## 十七、源码工程必须清除历史补丁结构

当前 `sections/` 的约 198 个片段中，大量名称含 `dp22`、`dp43`、`dp83`、`detail`、`extra`、`worked`、`derivations`。这种结构适合开发阶段，不适合正式出版源码。

### 重构后原则

- 正式正文优先直接放入 `chXX.tex`；
- 只有一个稳定章节确实过长时才拆到 `sections/semantic-name.tex`；
- 文件名必须描述物理内容，不记录历史轮次；
- 删除 `dpXX`、`extra`、`detail`、`r13` 等修订痕迹；
- 同一主题若由 4–6 个补丁文件拼成，应合并成一个经过重新编辑的连续源码文件，而不是机械 concatenate；
- validation 脚本可以保留，但不让它们决定正式章节结构。

这一步不仅是整洁问题。现在的片段化本身会鼓励“想到什么再 input 一个模块”，最终导致章节越来越像知识插件集合。

---

## 十八、排版与图形

- 不新增教学型 preamble 命令；
- 不增加“物理链条框”“条件框”“路线图框”；
- 现有约 1284 个 `\boxed` 必须大规模清理，目标不是设硬数量，而是默认不用；
- 只有真正需要读者隔页快速定位的最终主方程才考虑框，但普通编号公式足够；
- Derivation 保留给长数学，不要每个两行代数也开环境；
- 不为了“新手友好”新增大量 Note；解释直接写进正文；
- 图优先画真正的实验几何、色散关系、边带人口、相空间、Green 谱、辐射角分布；
- 不画“理论 A → 理论 B → 理论 C”的装饰流程图；
- 图内普通解释文字用中文，坐标轴以符号+单位为主；
- 同一 PINEM/反冲/传播图族保持统一尺度与符号。

---

## 十九、执行顺序

### P0：重新建立书的身份

1. 新写导论；
2. ch05 QCD/ch06 SM 移出主线；
3. ch01 数学工具降附录/按需调用；
4. ch03–04 压缩成 QFT/QED 最小接口；
5. 更新 dependency map。

### P1：拆真正的自由电子巨章

- ch07 → finite-time / Green-EELS / single-mode recoil；
- ch08 → classical PINEM / experimental averaging / quantum PINEM；
- ch09 → recoil/Bragg 与 Floquet；
- ch10 → propagation / attosecond / decoherence / measurement / inversion；
- ch11 → EELS / CL-hybrid / periodic radiation / imaging。

### P2：逐章重写章首和转场

全部删除“本章系统地”“母结构”“接下来考察”式报告语言。先不动公式，只把每个公式为什么出现写明白。

### P3：推导链审计

以“学生能否从上一行自己算到下一行”为标准，重点修 PINEM、quantum PINEM、recoil、propagation、Green response。

### P4：实验尺度和完整算例

至少完成：

- 一个 Feist-style PINEM 参数计算；
- 一个有限脉冲平均；
- 一个 recoil/Bragg 参数区间；
- 一个 attosecond bunching distance；
- 一个 planar-interface EELS；
- 一个 detector inversion。

这些直接写进连续正文，不新增 Example 命令。

### P5：源码去补丁化和视觉 QA

合并 sections，删 dpXX，清 boxed，统一语义 label，最终编译。

---

## 二十、最终验收否决项

出现以下任一情况，本书仍不算完成：

- 读者仍需先读 QCD/标准模型才能到自由电子；
- ch01 仍把 Grassmann/Lie/differential geometry/loop integrals 当共同先修；
- 主线开始前仍占全书接近一半以上篇幅；
- ch07–11 仍以原巨章形式存在；
- 经典 PINEM 和量子 PINEM 仍混在同一个 section 链里；
- 自由传播、开放系统、量子测量、反演仍塞在一章；
- 一般 OQS/QFT 内容与其他讲义重复讲一遍；
- `sections/` 仍充斥 `dpXX/detail/extra` 历史文件；
- 普通公式仍大量 `\boxed`；
- “低反冲”“高能”“Markov”等近似仍只有文字没有控制参数；
- 实验参数仍作为表格/列表出现，却不解释为什么这些尺度决定可见性；
- 读者看完 PINEM 只知道 \(J_n\) 公式，却不知道为什么所有边带由同一个相干振幅锁定；
- 读者看完整本书仍说不清“经典场驱动、量子光驱动、材料环境、自由传播、测量”这五层分别在哪一步进入。

---

## 二十一、逐原章动作清单：以当前递归展开后的真实内容为准

| 当前章 | 真实规模/病灶 | 必须保留 | 必须移动/删除 | 重写后落点 |
|---|---|---|---|---|
| ch01 数学工具 | 约 2074 展开行，Fourier/Hilbert/Grassmann/Lie/几何/散射积分齐聚 | Fourier 约定、连续态归一化、必要投影/Green 基础 | Grassmann、一般 Lie/微分几何、loop 技巧全部按需后移；不再共同先修 | 附录/按需盒外正文引用，不做主章 |
| ch02 时空/经典场 | 约 4178 行，Poincaré/Wigner/Weyl/Dirac/Noether/Maxwell/Green 混合 | relativistic dispersion、Dirac 正能态、最小耦合、Maxwell Green | Wigner 分类、完整群论、一般 Noether 细节移其他书 | 新 ch02–03 |
| ch03 QFT | 约 6577 行，完整 QFT 课程 | field quantization 的最小接口、interaction picture/Dyson、Wick/LSZ 若真正需要 | renormalization/RG/OPE/heat-kernel/BRST/SSB 主线删除或附录链接 | 新 ch04 的最小前置 |
| ch04 QED | 约 7870 行，完整 QED | Dirac+photon quantization、QED vertex、tree electron-photon interaction、macroscopic QED 接口 | loop renormalization/soft theorem/Schwinger/大量 scattering 退出主线 | 新 ch04 + 后文按需引用 |
| ch05 QCD | 约 1805 展开行，与书名主线无关 | 若需展示场论广度，转独立附录/AdvancedPhysics | 从主目录和先修链删除 | 非主线 |
| ch06 SM | 约 2046 展开行，与主线无关 | 最多保留一页“电子在标准模型中的位置” | gauge/SSB/flavor/anomaly/precision 全部移出 | 非主线 |
| ch07 自由电子与量子激发 | 约 6372 行，终于进入主题但含三四层理论 | continuous electron state、finite-time transition、environment modes/Green、EELS、single-mode/recoil | Feshbach/一般环境工具只在需要处；拆章 | 新 ch05–07 |
| ch08 外场/反冲/量子交换 | 约 3608 行，classical PINEM、pulse averaging、quantum PINEM、recoil 混合 | external-field PINEM、Bessel、finite pulse、quantum exchange | 经典与量子支路完全拆开；反冲独立 | 新 ch08–14 |
| ch09 周期势/反冲 | 约 2663 行，Bloch/Floquet/Bragg/KD 混合 | exact recoil lattice、Bragg/KD、Floquet 最小接口 | 与 PINEM 无关的一般周期驱动技术压缩 | 新 ch10–11 |
| ch10 传播/OQS/测量 | 约 6038 行，五个中心问题同章 | exact free propagation、attosecond bunching、decoherence、POVM/tomography、inversion | 一般 OQS theorem 引用 AdvancedPhysics；QFI 若非主线后移 | 新 ch15–19 |
| ch11 响应/辐射/反演 | 约 4604 行，EELS/CL/LDOS/hybrid/periodic/Compton/imaging 全塞 | Green response、EELS/CL、hybrid mode、collection/inversion | Compton/QED 百科移出；重复 measurement 合并 ch18–19 | 新 ch20–23 |

### 21.1 一个必须接受的结论

这本书完成后，主目录中的“前置基础”不能再超过自由电子主题本身。读者应在前两三章就开始计算自由电子，而不是读完整套 QFT/QCD/SM 后才进入书名主题。

---

## 二十二、建议最终主线进一步收紧为 23 章

前一版建议已给出拆分方向，这里把每章的“真正任务”进一步具体化。

### ch01 现象导论：自由电子为什么会出现量子光学问题

**章首要做的事**：从实验可见现象出发，不讲 Grassmann、不讲规范固定。依次让读者看到：

- 光学近场给自由电子产生 `hbar omega` 间隔边带；
- 强耦合时某些边带消失又复现；
- 真实反冲会打破均匀能量梯；
- 传播后能谱可不变，但时间密度会聚束；
- 若光量子化，电子与光可纠缠；
- 材料环境和探测器又会改变可见结果。

**只预览三个公式**：relativistic dispersion、`P_l=J_l^2(2|beta|)`、Green-response loss/radiation 的结构。每个只解释“它会回答什么”，不做正式证明。

**章末问题**：要把这些现象算出来，首先需要一个正确的自由电子态和它与电磁场的耦合。

### ch02 相对论自由电子、波包与最小耦合

从 Dirac 方程开始，但目标不是教完 relativistic QM，而是得到后文真实需要的：

- 正/负能平面波；
- `u_s(p), v_s(p)` 归一化；
- probability/current；
- 正能波包；
- exact dispersion/group velocity/Hessian；
- minimal coupling；
- 正能投影何时安全。

**A 级推导**：正能 spinor、归一化、current、`H_D^2`、投影算符、低能/窄带约化。

**人话解释点**：自由电子没有预先存在的离散能级；后面所有“边带/格点”都是相互作用选择出来的通道。

### ch03 Maxwell 场、Green 张量与材料响应

先给“给定电子电流，怎样算它在结构中激起的场”。

顺序：Maxwell operator → boundary condition → Green tensor → source field → spectral/modal representation → Im G 的物理意义。

不要先上 macroscopic QED。先把 classical linear response 算清楚，再在需要量子噪声时升级。

### ch04 量子化电磁场与电子—光子相互作用的最小接口

只保留本书必需 QED：

- field mode quantization；
- Fock/coherent/thermal；
- electron current coupling；
- interaction picture/Dyson；
- one-photon absorption/emission amplitude；
- coherent-state classical limit。

不讲 QCD/SM/loop renormalization。

### ch05 有限时间相互作用：为什么会出现谱选择

先从一个通道的一阶振幅积分开始，推矩形窗 `sinc`，再推广一般 envelope。

**必须推**：finite-time amplitude → probability → continuum final states → golden rule delta limit。

**关键人话**：有限时间意味着能量并不“精确守恒”，而是只能分辨到约 `hbar/T`；这正是为什么连续电子谱会被环境频率选出一组可分辨通道。

### ch06 电子电流与 Green 张量：EELS/CL 的共同起点

先写 classical trajectory/current，再由 `G` 算 induced field。EELS 从 electron work/energy loss 得到；CL 从 radiated flux/collection channel 得到。明确二者都由同一个 response kernel 控制，但测量的是不同通道。

### ch07 单模投影与真实反冲格

从 exact dispersion 计算第 `l` 个交换通道：

`p_l`, `E_l`, `Delta_l`, `G_l`。

只有当相邻边的失谐和耦合差别不可分辨时才得到 translation-invariant ladder。定义电子 shift operator 到这里才出现。

### ch08 经典 PINEM：从沿轨迹相位到 Bessel 边带

这是全书必须写得最像用户论文讲解的一章。

顺序：

1. 给定外场和入射电子；
2. 从最小耦合/程函近似得到沿轨迹相位；
3. 定义 `beta`；
4. Jacobi–Anger 展开；
5. 得到复振幅 `c_l` 和概率 `J_l^2`；
6. 解释所有边带被一个 `beta` 锁定；
7. 解释 Bessel 零点、人口消失/复现、多路径干涉；
8. 做 normalization/moments/classical limit。

### ch09 有限脉冲、空间平均与实验可见性

把“为什么理想 Bessel 振荡在实验中会被洗掉”独立出来。

完整计算：电子横向分布、时间包络、`beta(r,t)` 分布，最后对 `J_l^2(2|beta|)` 做 ensemble average。用 Feist-style 尺度比较解释束斑/近场/脉冲宽度的作用。

### ch10 有限反冲、Bragg 与 Kapitza–Dirac

从 ch07 exact recoil lattice 回来。定义 recoil energy/mismatch。低反冲极限→PINEM；反冲可分辨时→少通道共振；二态 Bragg reduction 要从完整格点通过 Feshbach/adiabatic elimination 得到，并给误差。

### ch11 Bloch/Floquet 只服务周期问题

空间周期先讲 Bloch，时间周期再讲 Floquet。只保留理解 periodic near field / driven recoil lattice 所需内容。高频 Magnus/van Vleck 不做百科。

### ch12 量子 PINEM：联合电子—光动力学

先问 classical `beta` 把光当给定数，如果光子数会涨落怎么办？

写 joint Hamiltonian，电子 shift operator 与 photon `a/a†` 同时出现。必须明确两种 ladder 的边界和物理不同。

### ch13 Fock、相干、热光场怎样映射到电子谱

逐类输入态计算 electron reduced distribution；相干态极限恢复 classical PINEM，但必须说明 `a†` 项为什么使有限振幅下仍有残余 entanglement correction。

### ch14 纠缠、条件测量与非经典光

从联合态 Schmidt/overlap 解释 electron coherence。先讲环境末态可区分性如何压低 off-diagonal，再讲 heralding/conditional measurement。

### ch15 自由传播：精确相位与色散展开

保留现 ch10 好开场。先 exact `exp(-iE(p)t/hbar)`，再做 controlled Taylor expansion。横向/纵向 effective mass 不是新的质量，而是 dispersion curvature。

### ch16 能量梳怎样变成阿秒时间结构

从 sideband amplitudes 带入 free propagation，相位包含 `l` 的线性/二次项；线性项只平移时间，相对二次相位造成 bunching。推 density/Bessel sum/Talbot-like scale。

### ch17 自由电子的退相干与噪声

不要重讲完整 OQS。先定义电子实际遇到的随机/量子环境，算 coherence factor。一般 GKSL/NZ 只引用 AdvancedPhysics。重点是 sideband coherence、phase noise、energy diffusion、which-path information。

### ch18 电子探测：能谱、相位和 POVM

先从真实探测器输出问“实验到底测什么”。Projective energy measurement 只是理想极限；有限分辨率写 effect operator/convolution。相位信息需要干涉/参考场/多设置。

### ch19 层析与反演

明确 forward map：未知近场/密度矩阵 → measurable counts。再问 identifiability、conditioning、regularization、uncertainty。QFI 只有在它真帮助实验设计时保留。

### ch20 EELS：从 Green response 到材料谱

完整做 planar interface/sphere 至少一个解析例。把 Mie/planar response 与通用 Green tensor 接起来。

### ch21 CL 与辐射收集通道

从 far-field channel projection 求 photon yield/angular distribution；解释 EELS 与 CL 不等价，因为能量损失可进入非辐射通道。

### ch22 混合模式、周期介质与动量选择

plasmon/polariton/cavity/photonic crystal 都放在“mode dispersion + electron phase matching”同一语言下，但每次先写可观测现象和 matching condition。

### ch23 实验前向模型与综合案例

最后不是再加新理论，而是完整贯穿：sample geometry → field/Green response → electron evolution → propagation → detector convolution → inversion。至少给一个端到端案例。

---

## 二十三、必须从原稿中明确移出的内容清单

### 主线删除/迁移

- ch05 全部 QCD 主课内容；
- ch06 全部标准模型主课内容；
- ch03 中 OPE、heat kernel、BRST、SSB、完整 RG/renormalization；
- ch04 中 QED loop renormalization、vacuum polarization 全套、soft theorem、Schwinger 等，除非后文某个实验结果真正需要；
- 与 `MathSkills` 重复的完整 Poincaré/group/differential geometry；
- 与 `AdvancedPhysics` 重复的一般开放系统定理。

### 可以留一句链接的位置

例如在 electron self-energy/dispersion correction 真需要 QED radiative correction 时，可以一句：

> “这些修正属于重整化 QED 的范畴，本书只把其已重整化参数作为输入；完整圈图推导见……”

而不是把整套课程放在这里。

---

## 二十四、原件中 `lecture-narrative-*.json` 已经暴露的叙述病灶，应全书推广修正

这些 before/after 记录非常有价值，说明旧稿的根本问题不是“不会解释”，而是**多轮扩写后抽象术语重新盖住了解释**。

### 24.1 多层记号一次性出现

旧稿曾在 classical PINEM 入口一次定义 `G_l(t)`、`upsilon(t)`、`g_q`、`beta`、`g_c`。这对作者很完整，对初学者是灾难。

硬规则：某个符号只有在未来 1–2 页内要实际参与方程时才定义。量子耦合 `g_q` 不得在 classical PINEM 章提前出现。

### 24.2 “母对象”式总结替代实际作用

旧稿称 propagator/resolvent 为“精确母对象”。重构后必须先让它作用：

- propagator 作用于初态得到末态；
- resolvent 作用于 eigenstate 得 `(z-E_n)^{-1}`；
- Green tensor 作用于 source 得 field。

只有读者已经会用以后，才可以一句概括其统一性。

### 24.3 术语先于物理过程

旧稿先说“质量壳失谐统一 PINEM/反冲格/少态共振”。应改成先比较

`E(p+hbar k)-E(p)` 与 `hbar Omega`

的差，再把这个差叫 detuning。术语是结果的名字。

### 24.4 过度提前说明例外

旧稿为了严格，经常在第一次定义时把连续谱、阈值、初始相关、非高斯等所有例外一次列完。重构后：

- 先在当前主问题的清晰条件下建立结果；
- 例外只在它会改变下一步时出现；
- 但近似条件和适用域不能省。

“后移例外”不等于“隐藏条件”。

---

## 二十五、全书最重要的 A 级推导链：必须逐行可复算

### 电子基础

- Dirac equation → plane-wave eigenspinors；
- spinor normalization/current/completeness；
- positive-energy projector；
- minimal coupling；
- exact relativistic dispersion derivatives；
- envelope/paraxial/eikonal reduction with phase-error control。

### 有限时间与通道形成

- Dyson first order → finite window integral；
- rectangular window → sinc；
- continuum → golden rule；
- exact mass-shell mismatch；
- channel overlap vs detector resolution distinction。

### Green response

- Maxwell operator inverse definition；
- mode expansion；
- retarded prescription；
- Im G spectral density；
- electron current → induced field → energy loss；
- radiative channel projection → CL。

### PINEM

- external-field Dirac/eikonal → accumulated phase；
- positive-frequency field convention and factor 2；
- `beta` trajectory integral；
- Jacobi–Anger → sideband amplitude；
- normalization/moments；
- finite pulse/spatial averaging；
- Bessel zero/Rabi-like population oscillation interpretation。

### recoil/Bragg

- exact channel energies/couplings；
- recoil mismatch；
- translation-invariant limit；
- Feshbach/elimination to two-level；
- error estimate/validity。

### quantum PINEM

- joint Hamiltonian；
- Fock input evolution；
- coherent-state limit；
- thermal mixture；
- partial trace/purity/coherence；
- entanglement/conditional state。

### propagation/attosecond

- exact free phase；
- Taylor/Hessian；
- phase-error bound；
- sideband phase sum → time density；
- bunching/Talbot scale；
- initial energy spread effect separated from comb phase structure。

### measurement/inversion

- ideal projective measurement → finite-resolution POVM/effect；
- forward convolution；
- multi-setting phase reconstruction；
- inverse problem conditioning；
- regularization and uncertainty。

---

## 二十六、必须补的六个端到端“像论文讲解一样”的完整案例

这些案例不做成彩框，不新增 Example 环境。每个案例就是正文中一段连续小作文+推导。

### 案例 1：Feist-style coherent PINEM

给定电子能量、束斑、近场衰减尺度、脉冲宽度，先解释为什么耦合近似均匀，再由 `beta` 求 `J_l^2`，找到零点，解释边带消失/复现。

### 案例 2：有限反冲从 PINEM 到 Bragg

固定 photon momentum transfer 和 interaction time，比较 recoil detuning 与 `1/T`，展示从多边 ladder 到 two-state resonance 的连续变化。

### 案例 3：quantum light imprint

比较 coherent/Fock/thermal input，给 electron output spectrum 和 purity。明确哪些差异来自 photon-number distribution，哪些来自 entanglement。

### 案例 4：attosecond bunching

从一个给定 Bessel comb 出发，自由传播到 time density，求首个强聚束距离和 pulse width；再加入 finite initial energy spread 比较。

### 案例 5：planar-interface EELS/CL

从 planar Green tensor 开始，沿 electron trajectory 积分得到 loss probability，再投到 radiative sector 得 CL，解释同一 mode 在两种测量中的差别。

### 案例 6：近场反演

未知参数设为一个简单 complex near-field amplitude/profile。写 forward model、detector convolution、noise，展示多设置测量如何恢复 amplitude/phase，并给 conditioning/uncertainty。

---

## 二十七、源码重构的具体落地规则

当前 `sections/` 大量历史片段不能只改名。执行顺序：

1. 为每个新章新建干净 `chXX.tex`；
2. 先写新的连续章首和 section 骨架；
3. 从旧文件中按数学内容迁移段落；
4. 每迁一块都重写前后过渡，禁止机械 concatenate；
5. 同一推导分散在 `detail/dpXX/derivations` 多文件时，合并成一处；
6. 已不在主线的文件移动到 `source_notes/` 或独立 archive，不参与编译；
7. 新 `sections/` 只有在单章确实需要稳定语义拆分时使用，文件名只写内容；
8. validation 脚本按新语义路径更新，不让旧路径反向绑架新章节结构。

`preamble.tex` 不因为重构新增任何“phase box”“approximation box”“logic chain”之类命令。

---

## 二十八、加严验收否决项

- 主目录中仍存在 QCD/标准模型作为必须阅读的 ch05/ch06；
- 第一个真正的自由电子计算仍晚于全书三分之一；
- ch03/ch04 仍保留完整 QFT/QED 百科规模；
- classical PINEM 一章开头一次出现 5 个以上耦合/失谐符号；
- PINEM Bessel 公式推完后没有解释同一个 `beta` 如何锁定全部边带和 Bessel 零点的物理意义；
- finite pulse/spatial averaging 仍只列公式，没有解释为什么实验均匀性决定可见振荡深度；
- exact recoil 与 low-recoil approximation 仍没有同一套符号直接比较；
- quantum PINEM 仍被塞在 classical PINEM 后半节；
- propagation/OQS/measurement/inversion 任意两项仍合成一个巨章；
- OQS 仍重复 AdvancedPhysics 的一般理论而没有 electron-specific observable；
- EELS/CL 仍作为两个孤立公式，而没有从同一个 Green response kernel 展开；
- `sections/` 正式输入链仍有大量 `dpXX/detail/extra`；
- 全书普通公式仍有数百个 `\\boxed`；
- 读者完成全书后仍不能清楚区分：经典场驱动、量子光交换、材料耗散、自由传播、探测器响应分别在哪一步进入。

---

## 二十九、第三版读者契约：从四大力学出发，不要求量子光学或场论先修

目标读者学过高等数学、线性代数、数学物理方法以及经典力学、电动力学、量子力学和统计力学。他知道 Schrödinger 方程、简单微扰论、Maxwell 方程和谐振子，但可以从未学过 Dirac 方程、量子场论、量子光学、开放系统、Green 张量、POVM 或逆问题。

这意味着本书可以调用本科课程里的基本结论，却不能用一句“由标准量子光学可知”跨过自由电子计算真正依赖的步骤。`AdvancedPhysics`、`MathSkills` 和 `GroupTheory` 只能作为延伸阅读；删除这些交叉引用后，本书的主线推导仍须闭合。

第一次出现一个新对象时，正文必须依次完成四件事：它描述什么实验过程；它在数学上是什么；怎样用它算出一个可观测量；在哪些尺度下这个描述失效。定义不能脱离可观测量，物理图像也不能代替数学定义。

本书不是自由电子相关主题的论文合集。它应当让读者从一个已知入射电子和一个已知光场或材料环境出发，独立算出末态电子谱、光子统计、时间密度、损失概率或探测器计数，并能说清每一步使用了哪种近似。

## 三十、四章基础入口必须真正从零建立

### 30.1 相对论电子不能从现成旋量公式开始

从相对论能量关系和 Schrödinger 描述的局限进入 Dirac 方程。至少完整展示一次：

1. Dirac Hamiltonian 的矩阵结构；
2. 平面波代入后得到的代数本征方程；
3. 正能量旋量的构造与归一化；
4. 概率密度和电流；
5. 正能量投影算符；
6. 窄带波包如何由平面波叠加；
7. 群速度与能量色散的关系；
8. 最小耦合怎样从经典四动量替换进入 Hamiltonian。

不能假定读者熟悉协变记号。四矢量、度规号差、上下指标、自然单位与 SI 单位第一次出现时都要说明。正文选定一套 Fourier、正频场和相位约定后，全书保持不变；若文献采用另一约定，要在转换处实际写出符号如何改变。

### 30.2 Maxwell Green 张量必须从波动方程推出来

不能把 \(\mathbf G\) 作为“材料响应母对象”直接交给读者。先从频域 Maxwell 方程消去磁场，得到电场波动算符；再把 Green 张量定义为该算符对点源的逆。随后完整检查：

- delta 源和单位张量的归一化；
- 推迟边界条件与 \(+i0\) 处方；
- 电流源经过卷积怎样产生电场；
- 真空 Green 张量或平面界面 Green 张量的一个可算例子；
- \(\operatorname{Im}\mathbf G\) 与模式密度或耗散通道的联系；
- reciprocity、causality 和 passivity 分别需要什么条件。

模式展开和 Green 表示必须在同一简单几何中核对一次。读者应看到二者是同一响应的两种表示，而不是两套互不相干的公式。

### 30.3 量子化电磁场必须从单个谐振子搭桥

读者只学过量子谐振子，因此先从单模开始：定义产生湮灭算符、Fock 态和数算符，证明对易关系，写出电场正负频部分，再推广到多模。随后才定义相干态、热态和非经典态。

相干态不能只给 \(a|\alpha\rangle=\alpha|\alpha\rangle\)。至少推导其 Fock 展开、归一化、光子数分布和平均场，并解释经典场极限来自哪里。热态要从 Gibbs 权重得到光子数分布。Fock、相干、热态第一次比较时，使用同一平均光子数和同一电子耦合，避免把能量不同造成的差异误认成统计差异。

场的连续模归一化、盒归一化和损耗介质量子化不可一次全部压给读者。主线先在一个离散单模中完成电子—光交换，再说明连续模极限增加了哪些积分、态密度和归一化因子。

### 30.4 密度算符、偏迹和测量必须在量子 PINEM 前补齐

从“不同制备可以给相同统计混合”进入密度算符，推导期望值公式、纯度和部分迹。至少对一个两能级电子与单模光场的联合态手算偏迹，让读者看到总态为纯态而电子约化态可以是混态。

随后从 Born 概率进入投影测量，再解释有限能量分辨率为什么对应一组正算符效应。POVM、量子操作和 Kraus 算符只讲后文实际需要的部分，但正性、归一化和条件态更新必须用一个小矩阵例子验证。

不能等到反演章节才第一次解释“实验记录的不是理想概率，而是理想分布经过探测响应后的计数”。这一层应在第一个电子能谱计算后立即出现一个最简单的卷积模型。

## 三十一、全书必须始终分清五层模型

每个推导开始前，正文要用自然语言交代当前处理的是哪一层；不需要做成框或流程图。

1. **制备层**：入射电子波包、光场态、材料温度和初始相关；
2. **相互作用层**：Hamiltonian、经典外场、量子交换或材料响应；
3. **传播层**：相互作用结束后的自由色散、环境噪声和退相干；
4. **测量层**：探测器分辨率、收集角、效率和 POVM；
5. **推断层**：从有限计数反演场、态或材料参数。

这五层的参数不得混用。电子初始能散不是探测器能量分辨率；相互作用区内的脉冲包络不是漂移后的时间响应；材料损耗造成的混态不是对未记录光子自由度求和以外的“额外退相干”同义词；正则化偏差也不是实验噪声。

每个最终可观测量都应能够沿这五层逆向追溯。若一条公式同时包含多层因素，要先给理想结果，再逐层加入卷积、平均或偏迹，使读者看见每一层怎样改变结果。

## 三十二、核心推导必须达到逐行可复算的程度

首次出现一种推导动作时，不能藏在长 `derivation` 框或一页公式墙中。正文应先说明当前已知量和待求量，再按数学动作分段。每个等号需要能够回答：用了哪个定义、换了什么变量、舍掉了哪一项、边界为何消失、近似误差由什么控制。

以下细节不得省略：

- 连续态归一化中的 \(2\pi\)、体积和 delta 函数；
- 从时间积分得到 sinc 的上下限、相位和长时 delta 极限；
- 从实电场提取正频振幅时的因子二；
- 从沿轨迹相位到 Jacobi--Anger 展开的符号与指标变换；
- Bessel 振幅的归一化和至少一个矩恒等式；
- 动量、能量与边带编号之间的 Jacobian；
- 对环境或光场求偏迹时，振幅求和与概率求和的区别；
- 从精确相对论色散到二阶展开的余项；
- Green 张量奇异部分、推迟处方和取虚部的顺序；
- 探测器卷积核的归一化以及计数模型的似然。

近似一律按“精确式—无量纲控制参数—展开—保留阶—余项或误差界—失效条件”的顺序写。`high energy`、`small recoil`、`long interaction`、`Markov`、`paraxial`、`narrow band` 不能单独充当推导理由。

若严格误差界超出本书范围，至少给相邻保留项与首个舍弃项的比值，并用一组现实尺度估计其数量级。只写“数值验证很好”不能替代误差判据。

## 三十三、八条主干必须各自从最简单模型讲到实验量

### 33.1 有限时间跃迁

先解一个常数矩阵元、有限矩形时间窗的两态或连续态跃迁，得到 sinc 线形；再讨论一般包络的 Fourier 变换。黄金律只能在峰宽远小于其他变化尺度、作用时间足够长时出现。必须区分有限时谱宽、初态能散和探测器分辨率。

### 33.2 经典 PINEM

从给定经典近场和电子轨迹出发，先求累积相位，再展开边带振幅。读者要能独立回答：\(\beta\) 的量纲是什么；改变场相位会改变什么；为什么概率只依赖 \(|\beta|\) 而相干演化仍保留 \(\arg\beta\)；为什么所有边带由同一个复数锁定；Bessel 零点为何表现为边带消失和复现。

有限脉冲、电子束横向尺寸和到达时间抖动应分别写成不同平均。至少选择一个解析包络，把平均做完，而不是只给三重积分。

### 33.3 有限反冲与 Bragg/Kapitza--Dirac

先保留精确相对论能量差，写出离散通道方程，再把低反冲 PINEM 作为极限推出。Bragg 两态近似要从消去非共振通道得到，并估计被消去通道的占据或能级修正。不能仅凭“接近共振”宣布只剩两个态。

纵向 PINEM 与横向 Kapitza--Dirac 的动量转移几何必须分别画清或用坐标明确说明，不能共用一个未定义的“反冲频率”。

### 33.4 量子 PINEM

先在单模、有限光子数截断下写联合 Hamiltonian 和守恒量，手算最小的 \(2\times2\) 或有限维块，再给一般结果。Fock、相干和热光输入使用同一符号体系逐个计算电子约化态、能谱与纯度。

相干态的经典极限要说明是怎样的极限：平均光子数增大时耦合如何缩放，哪些量保持不变，哪些量的相对涨落消失。不能只说“相干态最接近经典光”。

电子—光纠缠必须用约化态非纯、Schmidt 系数或互信息中的至少一种可计算量展示。若最终没有记录光，必须先形成联合密度算符再偏迹；不能对不同光子末态的振幅直接相加。

### 33.5 自由传播与阿秒聚束

从每个能量边带的精确传播相位开始，再做色散展开。必须把整体相位、线性平移和二次聚束三部分分开。Talbot 长度或最佳聚束距离应从相邻或二阶相位条件推出来，而不是直接给公式。

初始电子能散、边带相位噪声和漂移长度分布对时间密度的影响分别加入。至少给一个从能谱振幅到时域密度的完整 Fourier 和式，并检查总概率守恒。

### 33.6 EELS 与 CL

从同一电子电流和同一推迟 Green 张量出发推导能量损失，再把辐射到远场收集通道的部分投影出来。EELS 与 CL 的差别必须落在积分区域、边界通量或模式投影上，而不能只说“一个测损失，一个测光”。

至少完整计算真空、均匀介质或平面界面中的一个模型。所得概率要检查正性、量纲和无材料响应时的极限。若使用局域态密度类比，要明确电子轨迹的非局域采样为何不等同于点偶极子 LDOS。

### 33.7 开放系统与退相干

只讲影响自由电子可观测量的模型。每个 Lindblad 或随机噪声项都要从一种明确的环境相关函数或散射过程进入，并指出它衰减的是哪些边带相干。至少对一个纯退相干模型同时给时域解、能量基矩阵元和对聚束对比度的影响。

一般 CPTP、Nakajima--Zwanzig 或量子回归理论可以引用其他书，但这里必须完成电子特定的计算，不能用一般理论篇幅取代结果。

### 33.8 测量与反演

先写前向模型，再谈反演。参数到理想分布、理想分布到有限分辨计数、计数到似然的三步要分开。反演至少给一个可识别性失败例，说明单一能谱为何不能恢复全部相位，以及增加哪种相位扫描或传播距离后信息才足够。

正则化必须说明惩罚了什么、引入了什么偏差、超参数如何选择。误差条要来自计数统计、系统参数不确定度或后验/采样分布，不能把优化器收敛误差当作实验不确定度。

## 三十四、完整案例必须像论文讲解，但比论文更照顾初学者

前述六个端到端案例全部保留，并为每个案例补齐统一的教学要求：

1. 先画清或用文字定义几何、坐标和正方向；
2. 列出给定量与待求量，并说明每个量的单位；
3. 从一般方程化到该几何，不直接引用最终公式；
4. 在近似发生的那一行给尺度比较；
5. 解析计算能做多远就做多远，再使用数值；
6. 数值图必须对应正文中的明确问题；
7. 结果至少检查归一化、量纲、一个极限和一个数量级；
8. 最后说明实验真正记录什么，以及理论量如何经过探测器变成记录量。

每个大部分还要有一个“失败案例”：例如均匀耦合假设被束斑平均破坏、两态近似在强驱动下失效、单一能谱无法恢复相位、Markov 近似在长相关时间下失效。失败案例能阻止读者把适用条件误记成普遍规律。

数值参数不能作为装饰。每组数字至少支撑一个无量纲比值或可见性判断。若参数来自论文，区分论文报告值、由报告值推得的量和为了教学选择的示意值，并给出处或明确标注。

## 三十五、叙述必须像教授连续讲课，而不是研究笔记的注释层

正式正文删除“本书主线”“统一接口”“母对象”“脉络提示”“路线图”和“这一框架揭示”等施工语言。不要用粗体句、彩框或表格告诉读者某段重要；通过问题、计算和后果让重要性显现。

章首先承接一个具体实验现象或上一章留下的计算。新符号只在即将进入公式时定义。核心公式前说明为什么需要它，公式后解释各项、参数变化和下一步用途。章末停在自然产生的新问题，不复述目录。

缩写第一次出现时给中文名称和英文全称，之后只保留稳定缩写。PINEM、EELS、CL 等术语不能代替物理过程；在读者熟悉缩写以前，要继续说“电子交换一个光子能量后出现的边带”或“电子对材料的能量损失”。

推导环境只用于边界清楚、长度适中的局部论证。跨页的主干推导回到普通正文，按数学动作分段。公式之间若需要作者口头补一句才能看懂，那句话就应写进正文。

## 三十六、依赖、习题和读者任务

每章施工前写一份不进入成书的依赖清单：允许使用的本科知识；本章需要就地补齐的概念；本章输出给后文的公式。若一个章节依赖尚未建立的量子光学、Green 函数或统计概念，必须调整顺序，不能把定义塞进脚注。

每章至少安排一个逐步算例和一组短练习。每个部分至少安排一个综合问题，把制备、相互作用、传播和测量中的两层以上连起来。核心练习提供完整答案，答案写出中间步骤和近似条件。

全书完成时，目标读者应能在不查研究论文的情况下完成下列任务：

- 从给定近场沿电子轨迹算出 \(\beta\) 和边带概率；
- 判断一组参数属于低反冲 PINEM、多态反冲格还是 Bragg 两态区；
- 对 Fock、相干或热光输入求电子约化能谱；
- 从边带复振幅传播到给定距离的时间密度；
- 从电子电流与简单 Green 张量写出 EELS/CL 前向量；
- 把理想能谱与探测器响应卷积，并写出有限计数的似然；
- 指出上述每个结果最先在哪个近似失效。

只要其中任何任务仍需从别册补学一整章，本书就没有达到既定读者起点。

## 三十七、第三版最终否决项

除前述否决项外，出现以下任一情况也不得宣布完成：

- Dirac 旋量、Green 张量、相干态、偏迹或 POVM 第一次出现时直接引用现成公式；
- 四矢量、Fourier、正频场或连续态归一化约定在不同章节悄然改变；
- 量子 PINEM 没有先用有限维联合态演示偏迹和纠缠；
- PINEM 推导省略实场到正频振幅的因子二、相位符号或 Bessel 指标变换；
- 低反冲、两态、窄带、长时或 Markov 近似没有无量纲控制参数；
- EELS 与 CL 没有从同一 Green 响应推导，或没有至少一个完整几何算例；
- 阿秒聚束只给 Talbot 尺度，不从传播相位和边带和式推出；
- 探测器、初态平均、环境退相干和正则化被合并成一个模糊的“展宽”；
- 端到端案例只代入数值，没有一般推导、极限检查和误差判断；
- 正文仍以“主线提示”“统一框架”或长推导框代替连贯叙述；
- 读者能复述缩写和结论，却不能从输入态与相互作用写出一个可观测概率。
