# AdvancedPhysics、GroupTheory 与 MathSkills 总体重构方案

> 本文是结构设计稿，不是逐句修订清单。目标不是在现有章节上继续“减几段、拆几个框”，而是重新确定三本书各自负责什么、读者沿什么知识链前进、哪些内容属于正文、哪些内容属于推导、哪些内容应迁移到附录或其他讲义。实施时允许调章、合章、拆章、降级为选读、移入附录以及删除无法服务主线的材料。

## 一、结论先行

当前问题的根源不是个别推导框仍然偏长，而是三本书的**叙事层级、学科边界和内容所有权没有真正确定**。

1. 三本书共 59 章、68,221 行正文，源码中没有一个 `subsection`。许多 `section` 实际长达 500--2,000 行，只能依靠公式、定理环境和推导框临时充当导航，结果是正文看似连续，认知上却频繁跳题。
2. AdvancedPhysics 在一本书内同时容纳二维 Ising 的专著级路线、连续介质、辐射反作用、开放系统、原子分子和强场物理，各部分深度严重失衡。二维 Ising 占十章，而开放系统一章达到 3,722 行；量子化电磁场却晚于已经使用它的原子--光相互作用。
3. GroupTheory 前六章极度膨胀，定义、结构定理、物理应用、习题解答和高级表示论混在同一章；后两章又突然压缩成概论。一般 Lie 理论放在 Lorentz/Poincaré 之后，依赖顺序倒置。
4. MathSkills 既像数学物理方法教材，又像微分几何专著、场论附录和高等数理统计教材。它与 GroupTheory 重复群表示、与 AdvancedPhysics 重复 Clifford/Dirac、Poincaré、自旋分类和若干物理推导；同时第 4 章单章 4,543 行，第 21 章一个 section 长 1,316 行。
5. 目前不少推导框已经变短，但仍承担了四种互不相容的任务：证明定理、补正文缺口、罗列推广、存放高级旁枝。只缩短框并不能修复阅读链；必须先重写“删除全部 Derivation 后仍可读”的正文骨架，再重新决定哪些计算值得成为推导。

因此建议采用一次**跨书架构重置**：

- GroupTheory 拥有“对称群、表示及其物理后果”的母理论；
- MathSkills 拥有“分析、几何、概率统计工具”的可复用数学结构；
- AdvancedPhysics 只在必要处回顾接口，重点讲这些结构如何产生具体物理模型、近似和可观测量；
- 自由电子量子光学作为叙事结构参考，而不是内容长度参考。

## 二、审计依据

### 2.1 当前体量

| 讲义 | 章数 | 章文件总行数 | section | subsection | Derivation | 定理类环境 | 例题类环境 |
|---|---:|---:|---:|---:|---:|---:|---:|
| AdvancedPhysics | 28 | 21,895 | 123 | 0 | 158 | 8 | 36 |
| GroupTheory | 8 | 14,416 | 58 | 0 | 37 | 158 | 98 |
| MathSkills | 23 | 31,910 | 105 | 0 | 146 | 24 | 40 |
| FreeElectronQuantumOptics（参照） | 11 | 24,165 | 33 | 103 | 148 | 0 | 26 |

“零 subsection”不是排版偏好，而是结构缺陷。当前最长的若干 section 包括：

- AdvancedPhysics ch15“应用：环境谱、微观跃迁率与腔 QED”，1,979 行；
- MathSkills ch04“闭二次型、Friedrichs 扩张与谱稳定性”，1,870 行；
- MathSkills ch21“Likelihood、Fisher 信息与局部二次实验”，1,316 行；
- MathSkills ch06“Fredholm 型方程”，1,226 行；
- MathSkills ch19“经验平均、大数律与统一收敛”，1,154 行；
- GroupTheory ch05“Clebsch--Gordan 分解与角动量耦合”，942 行。

这些单元已经超过正常章节长度，读者无法从目录判断其中的概念边界，作者也难以安排“动机—定义—结论—证明—应用”的次序。

### 2.2 自由电子量子光学可借鉴的结构

该讲义最值得复用的不是“也有很多推导框”，而是以下组织原则：

1. 一章回答一个物理层面的母问题，section 表示问题阶段，subsection 表示可以独立复述的认知单元。
2. 每个新对象先由上一个理论的不足引出，再给数学定义；随后先写形式精确结构，再加入尺度与近似。
3. 具体装置、参数和反演位于母理论之后，不用熟悉模型代替一般理论。
4. 正文明确给出实验真正读出的量；推导只补关键代数、指标或积分，不负责告诉读者“这节在做什么”。
5. 前置概论和理论脉络说明依赖关系，但不会替正文代讲。

三本书不应照搬它的超长章节。新的目标是保留其依赖逻辑，同时把 subsection 控制为更短、更稳定的教学单元。

## 三、三本书共同遵守的新结构规范

### 3.1 叙事单元

每个 chapter 只回答一个母问题。每个 section 只完成母问题的一个阶段。一个 subsection 应能用一句话回答“读完以后会多会什么”。建议尺度为：

- chapter 通常 400--900 行；超过 1,200 行原则上拆章；
- section 通常 100--300 行；超过 400 行必须说明为何不能拆；
- subsection 通常 40--140 行，每节以 2--5 个为宜；
- 不使用 `subsubsection`、`paragraph` 或行首粗体短语补层级；
- 章节末不再堆放“进一步推广”“更多联系”式百科尾巴。

subsection 不是越多越好。只有当概念有独立输入、输出和后续用途时才设标题；短过渡仍写成自然段。

### 3.2 正文闭合规则

暂时删除全部 Derivation 后，正文仍必须包含：

1. 为什么需要新对象；
2. 对象的数学类型、物理意义、单位和所在空间；
3. 核心方程及其假设；
4. 结论描述了什么、何时失效；
5. 下一单元为什么自然出现。

重要结论先在正文陈述，再以推导框验证。推导结束后只用一两句解释所得结论如何接回主线，不重复整个公式链。

### 3.3 推导分级

所有现有推导先归入四类，再决定去留：

- **A 类：正文内联计算。** 少于约 8 行，只是代入、一次积分或标准恒等式，直接并入正文。
- **B 类：核心 Derivation。** 约 15--60 行，解决一个明确困难，例如指标缩并、自伴边界型、投影消元或受控渐近。
- **C 类：定理证明。** 若是本书主线定理，放在定理后用普通 proof 或短 Derivation；若只提供数学完备性，移至本章技术附录。
- **D 类：高级旁枝。** 超过 80 行、需要新理论或后文不再使用，移至附录/专题阅读，或删除。

一个框只回答一个问题。标题用“为什么……”“怎样从……得到……”等语义标题，不把多个公式编号塞进标题。正文与推导不得前后复制同一串公式。

目标不是机械减少框数，但可用以下范围作为报警线：AdvancedPhysics 约 90--115 个核心框，GroupTheory 约 25--40 个，MathSkills 约 95--120 个；超过范围时优先检查是否把正文或附录内容误塞进框内。

### 3.4 跨书内容所有权

| 主题 | 主讲义 | 其他讲义的处理 |
|---|---|---|
| 有限群、特征标、投影、Young 方法 | GroupTheory | MathSkills 只保留工具摘要；AdvancedPhysics 直接引用并展示物理输入输出 |
| Lie 群、根权、$SU(2)/SU(3)$ 表示 | GroupTheory | MathSkills 保留 Lie 代数/几何接口；AdvancedPhysics 不重复证明 |
| Clifford/Spin 的代数构造 | MathSkills | GroupTheory 讲表示意义；AdvancedPhysics 只用 Dirac/FW 物理 |
| Hilbert 空间、自伴性、谱测度、Green/Fredholm | MathSkills | AdvancedPhysics 给模型域、边界和可观测量，不重建一般定理 |
| Lorentz/Poincaré 表示 | GroupTheory | MathSkills 只保留 Noether 与微分几何接口；AdvancedPhysics 只取原子/场论所需结果 |
| 开放系统、原子分子、强场、统计模型 | AdvancedPhysics | 另两书只提供数学工具，不重复物理章节 |
| 概率与统计推断 | MathSkills | AdvancedPhysics 只在实验反演时引用 |

实施中应建立“唯一主定义 + 跨书接口段”。接口段最多两三页，说明采用的约定和需要的结论，然后链接主讲义，不再复刻整套证明。

## 四、AdvancedPhysics 重构

### 4.1 新定位

AdvancedPhysics 应成为“高级物理模型怎样从一般结构下降到可计算量”的课程，而不是若干小专著的合集。全书统一问题是：

> 给定状态空间、动力学与尺度，怎样从精确母理论得到受控近似，并连接到谱、响应、散射率或实验信号？

统计、经典场、量子动力学、原子分子不必深度完全相同，但每部分都应遵循“母方程—谱/Green 结构—控制参数—近似—可观测量”。二维 Ising 保留为完整案例，但不再占用十章才能进入其他物理。

### 4.2 建议目录：28 章重组为约 24 章

#### 第一部　平衡统计、相变与可解模型

1. **有限 Gibbs 系统、响应与热力学极限**：整合现 ch01 的 Gibbs、Kubo--Mori、凸性与极限存在性。
2. **配分函数零点与相变非解析性**：整合现 ch01 末部与 ch02；区分一般解析性命题、Lee--Yang 专门条件和一维反例。
3. **图展开、轮廓与平面对偶**：合并现 ch03、ch04 的 Ising 必需内容和 ch05 前半；同调只讲到处理边界扇区所需深度。
4. **转移算子、费米子化与有限扇区**：重排现 ch06--ch08；只保留一次 Jordan--Wigner 与一次 NS/R 扇区构造。
5. **二维 Ising 的精确热力学与临界行为**：现 ch08 结果与 ch09；把 Toeplitz、Yang 磁化和临界指数放在统一观测量链上。
6. **Cluster、virial 与二体散射数据**：现 ch10；把多组分、Beth--Uhlenbeck、零程极限按一般到特殊排列。

#### 第二部　连续介质、Green 算子与辐射

7. **变分算子、自伴边界与 Green 表示**：现 ch11，作为本部工具章。
8. **弹性薄板：三维约化、谱与受迫响应**：现 ch12 核心；特殊几何算例移入章末案例或附录。
9. **Maxwell 源问题与辐射谱**：现 ch13 前半，只讲给定守恒源到谱、角分布和多极展开。
10. **自场、辐射反作用与有效降阶**：现 ch13 后半；从因果 Green 函数、世界管平衡到 ALD/LL，并明确有效理论尺度。

#### 第三部　量子谱、约化动力学与量子场

11. **中心势、自伴径向问题与阈值散射**：现 ch14 主线；高维延拓和特殊函数目录降为选读。
12. **精确约化动力学与记忆核**：现 ch15 的联合幺正、动力学映射、NZ/TCL 和非 Markov 判据。
13. **Markov 极限、GKSL 与环境谱**：现 ch15 的 Born--Markov--secular、详细平衡、jump 与典型环境；腔 QED 只保留一条完整算例。
14. **量子化电磁场、相干态与 Gaussian 光场**：把现 ch25 前移到这里，为后续原子--光相互作用提供先修。

#### 第四部　原子、光场操控与强场动力学

15. **角动量、不可约张量与多电子原子**：现 ch16，删去 GroupTheory 已证明的一般表示论，集中于物理矩阵元、反对称空间和 Hartree--Fock。
16. **Dirac 低能展开与原子精细结构**：现 ch17，Clifford/Lorentz 只作接口，主线从 Dirac 最小耦合到 FW、Breit--Pauli 与实验尺度。
17. **含时传播、弱场响应与近共振动力学**：现 ch18，保留 Dyson/Magnus、黄金法则、RWA/Rabi/Bloch；移除 Landau--Zener 的重复完整推导。
18. **激光冷却、Ramsey 计量与俘获**：现 ch21；先内部态响应，再质心随机动力学，再进入钟和阱。
19. **强场经典尺度与回碰**：现 ch19，负责 $U_p$、Keldysh 参数的经典意义与 cutoff。
20. **Volkov、SFA、复时间与 Floquet**：现 ch20，引用上一章尺度，不再重复定义；清楚区分精确 Volkov、SFA 假设和鞍点近似。

#### 第五部　分子通道、光谱与非绝热过程

21. **Born--Huang 多通道与几何耦合**：现 ch22。
22. **分子振动、转动与对称分块**：重组现 ch23、ch26、ch27 的结构内容；正常模、分子转子和有限群分块形成一条链，激光 alignment 放章末应用。
23. **Franck--Condon、Duschinsky 与振电光谱**：现 ch24；删去已在量子光学章证明的相干态/Gaussian 通用代数，只保留分子参数化。
24. **Fano--Feshbach、非绝热交叉与 Landau--Zener**：现 ch28；定态消元和含时交叉分成两个清楚单元，最后再说明共同的投影结构。

### 4.3 现有各章的具体处理

#### ch01 有限 Gibbs 系统与配分函数解析性

- 保留：经典/量子 Gibbs 对象、自由能凸性、Kubo--Mori 响应、有限体积解析性、热力学极限的最小充分论证。
- 迁移：Lee--Yang 零点禁区移到新第 2 章；FKG、Griffiths 与 Peierls 只在新第 5 章需要时出现。
- 删除或降级：末尾把 FKG、临界指数不等式、Fisher 零点、Hausdorff 维数、自然边界猜想串成一个推导的做法。这里包含若干未经充分限定的概括，应拆成“严格结论”“启发式标度”“开放问题”三类。
- 推导：Duhamel 与 Kubo--Mori 可以合并；一般 $n$ 阶响应和 FDT 分开；次可加性证明保留；Jensen 零点计数若后文不用则入附录。

#### ch02 Lee--Yang 零点

- 章首直接承接新第 1 章“有限体积解析而极限可失去解析”的问题。
- 保留 Asano--Ruelle、均匀场圆定理、零点测度到磁化跳跃、一维链禁区。
- 把 Sokhotski--Plemelj 作为数学工具短引，不在这里重建复分析课程。
- “适用域”应提前散入各结论附近；章末只总结哪些假设不可删除。

#### ch03 图与 cycle space

- 不再作为独立数学章。将 boundary/cycle/cut 的最少定义并入新第 3 章。
- 图 Laplacian 谱若后文没有实际使用，应删除或转到 MathSkills；不要因为结构漂亮而保留。
- 简单回路分解是高温展开真正需要的关键证明，应保留。

#### ch04 平面对偶与曲面同调

- 保留胞腔嵌入、对偶边、球面边界与环面四扇区。
- Dehn twist、映射类群辛表示、完整 Poincaré 对偶和 Gauss--Bonnet 不属于 Ising 主线；移到 MathSkills 几何附录或删除。
- 同调语言只服务“局部轮廓不足以描述环面全局扇区”，不要展开成拓扑学小专著。

#### ch05 高低温展开与 Kac--Ward

- 与 ch03/ch04 合并后，正文按“任意图高温展开—平面低温轮廓—对偶临界条件—行列式表示”推进。
- “Transfer matrix 与 Onsager 精确解”不得在正式建立转移算子前预演完整结果，移至新第 4/5 章。
- Kac--Ward、Feynman--Sherman 可选一条完整证明，另一条给定理与参考。
- 星--三角到 Yang--Baxter 的尾段若不发展可积系统，不应留下未经使用的公式链；降为两页选读或删除。

#### ch06--ch08 转移算子、Clifford 与 Onsager 谱

- 三章改成“通用 transfer 谱”“一次完整费米子化”“有限扇区到自由能”三层，不在 ch06 和 ch07 重复 Jordan--Wigner。
- 在 ch06 正文明确 transfer Hilbert 空间只是经典配置编码，以及相关长度依赖 observable selection rule。
- ch07 统一 Majorana、边界宇称、NS/R 扇区；Pfaffian/Kac--Ward 的联系放选读。
- ch08 先列四个 traces 的物理边界条件，再给 Nambu 块和乘积；临界有限尺寸修正放在精确自由能之后。

#### ch09 Yang 磁化与临界行为

- 以“自由能不能给出磁化，必须计算长程关联”为动机。
- Toeplitz 符号、Szegő/Fisher--Hartwig 输入与最终 $1/8$ 指数分层写，不把所有高级渐近塞进同一框。
- Painlevé 只作为相关函数超越结构的选读，不与主线临界指数并列。
- 实验段应解释二维 Ising 普适性如何被测量，而不只是罗列数值。

#### ch10 Cluster、virial 与量子气体

- 先固定经典/量子、canonical/grand canonical、单组分/多组分的 convention，避免中途更换 $b_n,c_n$ 意义。
- “为什么 $log\Xi$ 只含连通图”是核心；前三阶 cumulant 只算到足以建立规则，不要逐项百科展开。
- Beth--Uhlenbeck 前先写一般二体谱移公式，再特化分波、低能和零程。
- 三体 connected 信息用于说明二体系数边界即可；完整三体 EFT 不在本章展开。

#### ch11 四阶变分算子

- 作为连续场方法章保留，但减少“式号驱动”的推导标题。
- 正文先给算子、定义域、边界 Green 配对和谱问题；闭二次型、pseudoinverse、Weyl 计数各自成为 subsection。
- 与 MathSkills 谱理论建立明确接口：这里证明模型特有的边界型和主符号，不重复一般紧 resolvent 定理。

#### ch12 薄板与 Chladni

- 先用 $h/L$ 说明三维弹性到 Kirchhoff--Love 的控制；一般 $A$--$B$--$D$ 板与各向同性板分层。
- 环板、矩形板、均匀载荷、八维匹配不应全部占据主线。保留一个展示边界矩阵法、一个展示 Green 响应，其余进入算例附录。
- Chladni 节线只讲 Courant 上界和实验读图；Pleijel 完整证明为选读。

#### ch13 辐射与辐射反作用

- 拆为两章。给定源的辐射问题与带自洽自力的粒子问题具有不同输入，不应只用 section 区分。
- 辐射章保留守恒流、横向投影、世界线谱、多极和软极限。
- 自力章保留 retarded/advanced 分解、质量重整化、ALD 病态和 LL 降阶；世界管两种算法只留一套主证明。

#### ch14 高维中心势

- 主章集中于 $SO(d)$ 分解、径向酉变换、自伴端点、短程散射与阈值律。
- Maxwell--Poisson 的真实维数依赖与固定 $1/r$ 数学延拓必须明确分开。
- 可解势和 Kramers--Pasternack 递推移入算例附录；点相互作用只保留与低能散射相连的维数结论。

#### ch15 开放量子系统

- 必须拆成至少两章。当前四个 section 中有三个超过 500 行，应用 section 达 1,979 行。
- 第一章：联合幺正、CPTP 映射、Kraus/Stinespring、NZ/TCL、记忆核。
- 第二章：Born、Markov、coarse graining、secular、GKSL、KMS/详细平衡、Liouvillian 与 trajectories。
- 腔 QED、自由空间辐射、热浴、Zeno 只保留两条互补算例；其余成为习题或应用附录。
- TCL4 若后文无实际使用，降为技术附录；不能让高阶展开阻断主线。

#### ch16 角动量与多电子原子

- CG、Wigner--Eckart、6j 的一般证明归 GroupTheory；本章只用统一 convention，展示如何计算原子矩阵元。
- 正文主线改为“单电子角动量—多电子反对称空间—中心场/HF—LS/jj 与光谱”。
- Hartree--Fock 是本章动力学核心，应获得比第二套 CG 递推更多篇幅。

#### ch17 Dirac 与精细结构

- 不重复 Clifford 和 Lorentz 表示的普遍构造；用两页接口固定 gamma、度规和最小耦合。
- FW 推导保留一步一步的 even/odd 计数；Darwin、自旋轨道和动能修正紧接物理解释。
- Bethe 兰姆移位不是同一近似层次，作为“Breit--Pauli 之外”的独立选读，避免让读者误以为 FW 已包含 QED 辐射修正。

#### ch18 含时量子动力学

- 形式精确传播、Dyson/Magnus、有限时间谱、黄金法则、RWA/Rabi、Bloch 是连贯链。
- Landau--Zener 完整推导移到新第 24 章；这里只在讨论一般二能级近似失效时前引。
- 开放驱动两能级只调用新第 13 章的 GKSL，不重新讲主方程来源。

#### ch19--ch20 强场动力学

- ch19 只负责经典尺度、质动力和回碰几何；ADK 公式作为连接量子理论的结尾，不在经典章假装推完。
- ch20 从规范协变的精确传播进入 Volkov，再明确列出 SFA 丢掉了什么；复时间是 SFA 振幅的渐近，不是独立母理论。
- $U_p$、$gamma_K$、cutoff 只定义一次；实验参数统一放 ch20 末作为 regime map。
- Floquet 若保留，应说明它处理周期传播的普适结构，并与 MathSkills/FEQO 的 Floquet 约定一致。

#### ch21 冷却、钟与磁阱

- 先从 ch18 的内部态响应导出散射力，再加入质心与反冲噪声；不要从多普勒公式直接跳到 Fokker--Planck。
- Sisyphus 冷却需要先说明内部简并和位置依赖 dressed states。
- Ramsey/原子钟与磁阱不是同一动力学问题，以两个 subsection 收束；合成规范场只作下一层方向，不展开成新专题。

#### ch22 Born--Huang

- 保持“完整通道展开—有限子空间协变—绝热近似—diabatic/两态”主线。
- 明确完整基中的规范变换与截断子空间的几何标量势不是同一件事。
- Chern 数只有在后文真正使用全局拓扑时保留，否则降为选读。

#### ch23、ch26、ch27 分子振动、对称与转动

- 重新分工：先一般多原子质量加权 Hessian 与零模，再用群投影分块；随后讲双原子振转与一般转子。
- 当前 ch23 和 ch26 都证明平移/转动是 Hessian 零模，只保留一次。
- 群投影、特征标正交的证明引用 GroupTheory，不在分子章再证明 Burnside。
- ch27 的左右生成元、不对称陀螺和 Wang 基保留；alignment/revival 是应用 subsection。

#### ch24 Franck--Condon

- 单模位移作为最小模型，一般 Duschinsky--Doktorov 为母结果，有限温关联函数为可观测接口。
- 位移算符、squeezing 的通用代数引用新第 14 章；本章只推分子矩阵和生成函数。
- 多模热关联表示与递推若功能重复，选一个作主算法，另一个进入实现附录。

#### ch25 量子化电磁场

- 前移到第三部。Maxwell 加权自伴性—模式量子化—Green dyadic—光场状态的顺序合理。
- 当前“单模压缩态 Wigner 函数”有两次相邻推导，应合并为一次。
- 连续变量信息量不应突然成为尾部新主题；若没有后续测量章，缩成 note 或移到 MathSkills/FEQO。

#### ch28 Fano--Feshbach 与 Landau--Zener

- 章内明确分成定态和含时两条线：Schur complement/resolvent 产生自能与线型；局部线性交叉/Weber 方程产生跃迁指数与 Stokes 相位。
- 共同点只在“保留/消去子空间及解析延拓”，不能把定态共振和动力学跃迁写成同一个公式的两个记号。
- 实验段分别给冷原子磁场共振和 Stückelberg 干涉的控制参数。

## 五、GroupTheory 重构

### 5.1 新定位

GroupTheory 应是一门“从对称操作到物理选择规则”的课程。它既不能退化为抽象代数大全，也不能成为特征标表和角动量公式手册。全书主线固定为：

\[
\text{群作用}
\longrightarrow \text{线性表示}
\longrightarrow \text{不可约分解}
\longrightarrow \text{算符与状态的对称约束}
\longrightarrow \text{空间、交换与内部对称应用}.
\]

当前前六章平均约 2,287 行，后两章合计只有 693 行，难度与体量倒挂。建议把 8 个巨章重组为 13 个较均衡章节，把习题解答移出章正文，并让一般 Lie 理论先于 Lorentz 与标准模型。

### 5.2 建议目录：8 章重组为 13 章

#### 第一部　群作用与有限群表示

1. **群、子群、商与群作用**：定义、陪集、同态、轨道--稳定子、共轭类。
2. **有限群结构与构造**：直积/半直积、Cauchy/Sylow；Jordan--Hölder 与可解群作为选读。
3. **表示、不可约性与完全可约**：等价、酉化、Schur、Maschke、正则表示。
4. **特征标、投影与表示构造**：正交关系、分解重数、张量积、限制/诱导；Clifford 定理与 Frobenius 互反放高阶 subsection。

#### 第二部　空间对称与量子约束

5. **点群、分子对称与晶体点群**：从 $O(3)$ 有限子群到 Schoenflies 与特征标表。
6. **晶格、空间群、Bloch 表示与小群**：Seitz 乘法、倒格子、非点式操作、Bloch 定理、Brillouin 区和能带小群。
7. **量子哈密顿量的对称分块与选择定则**：简并、微扰、投影、矩阵元、IR/Raman 与反幺正对称。

#### 第三部　连续转动与交换对称

8. **$SO(3)$、$SU(2)$ 与自旋表示**：几何、二重覆盖、不可约表示、双群。
9. **角动量耦合与不可约张量**：CG、3j/6j、重耦合、Wigner--Eckart；高级恒等式入附录。
10. **置换群、Young 方法与全同粒子**：共轭类、Specht 模、hook length、对称化与费米/玻色多体态。

#### 第四部　Lie 群、时空与内部对称

11. **半单 Lie 代数、根、权与最高权**：一般框架，$SU(2)$ 与 $SU(3)$ 作为贯穿例子。
12. **Lorentz 与 Poincaré 表示**：有限维场表示和幺正粒子表示严格分开。
13. **规范表示与标准模型群**：场内容、Higgs 破缺、反常与味；Yang--Mills 拓扑、GUT、seesaw 作为选读尾章或独立附录。

### 5.3 现有各章的具体处理

#### ch01 群的基本概念

- 拆成新第 1、2 章。当前 3,080 行、53 个定理类环境和 22 个例题，既是入门章又包含研究生抽象代数后半程，认知负担过大。
- 第 1 章只保留后续表示论必需的群、子群、陪集、正规子群、商、同态、共轭与群作用。每个概念使用同一两个例子贯穿，而不是每个定义另起新例。
- Cauchy/Sylow、合成列、Jordan--Hölder、可解群进入第 2 章，并标出“核心/选读”。物理主线不依赖 Jordan--Hölder 的完整证明，不应阻塞表示论入口。
- 乘法表逐格推导不值得用 Derivation；Burnside 双重计数值得保留。$D_n$ 展示应服务半直积，而不是另起百科尾段。
- 习题与解答移到 `backmatter/exercises-ch01.tex` 等独立文件，正文不再被几十页答案截断。

#### ch02 群表示理论

- 拆成新第 3、4 章。先完成表示、子表示、不可约、酉化、Schur、Maschke，再进入特征标与构造。
- 群代数和正则表示只讲到证明维数平方和与 character 正交所需深度。
- Frobenius 互反、Plancherel、Clifford 定理属于“从已有表示构造新表示”的高级层，不应与第一次定义表示处在同一层级。
- character table 的算法应由一个完整群例子贯穿，避免在多个小群上重复同一流程。
- 张量积、对称幂、外幂给出统一 character 生成函数；不要把错误或仅适用于特殊本征值的乘积式当一般公式。

#### ch03 点群与空间群

- 拆成新第 5、6 章。有限转动群、Schoenflies 和分子点群属于点群章；Bravais/倒格子/Seitz/非点式群属于空间群章。
- 当前先讲空间群再回到晶体点群不可约表示，应用顺序来回跳；新结构应先完成点群 character，再以平移正规子群构造空间群表示。
- 晶体制约定理的证明保留；晶面法向和面间距属于几何工具，可内联或移至附录。
- 特征标表不能只出现结果，应示范如何用类、基函数和正交关系读表；但完整表格放附录。

#### ch04 群论与量子力学

- 将 Bloch、Brillouin 区、空间群小群迁到新第 6 章，避免点群理论和能带理论被拆开。
- 新第 7 章集中回答：对称性怎样分块 Hilbert 空间、怎样强制简并、怎样约束有效 Hamiltonian 和矩阵元。
- Wigner--Eckart 的一般证明只在新第 9 章出现一次；本章用有限群矩阵元定理和群平均投影。
- IR、Raman、和频只保留一套统一张量判据和少量互补例子，不逐种光谱重复“直积含全对称表示”。
- 时间反演与 Frobenius--Schur 指标要先区分反幺正算符、实/复/四元数型表示，再讲 Kramers；当前两个相关推导可合并。
- 对称性破缺与序参量若不建立 Landau 表示空间，只作下一课程接口，不在章末另开大主题。

#### ch05 转动群、旋量与角动量耦合

- 拆成新第 8、9 章。$SO(3)$ 几何、$SU(2)$ 覆盖、不可约表示和双群是一章；CG、不可约张量和重耦合是下一章。
- 当前 CG section 942 行，不具备可导航性。至少拆为“张量积分解”“递推与相位约定”“3j/6j 与重耦合”“矩阵元定理”。
- Racah 公式、正交关系保留核心证明；Biedenharn--Elliott、Ponzano--Regge、Regge 对称性移到“高级重耦合”附录，除非后文实际使用。
- 不在同一本书的 ch04 和 ch05 各证明一次 Wigner--Eckart。
- 公式表与相位约定集中到附录，正文强调表示映射和选择规则。

#### ch06 置换群、Young 方法与全同粒子

- 保留为新第 10 章，但把 2,123 行分成清晰 subsection：循环/分拆、Specht 构造、维数与字符、Schur--Weyl/对称函数、全同粒子。
- 物理应用应在基本 Young 对称化之后立即出现，不要先堆完所有对称函数理论。
- Young--Yamanouchi 给出可计算算法；Frobenius characteristic、Littlewood--Richardson、诱导表示选一条主线，其余入附录。
- $S_n$ 的抽象表示和电子自旋耦合要区分 $S_n\times SU(2)$ 的两个作用，避免把“同一个二维空间”误写成同一个表示。

#### ch07 Lorentz 与 Poincaré

- 移到一般 Lie 理论之后。当前 272 行试图同时覆盖非紧群、Clifford、Wigner 分类和 Plancherel，深度远低于前六章。
- 扩写“有限维非幺正场表示”和“无限维幺正粒子表示”的区别，这是全章核心。
- Clifford 代数构造引用 MathSkills；本章只说明 $(j_L,j_R)$、Weyl/Dirac 组合和宇称。
- 主系列与 $L^2(SL(2,\mathbb C))$ 的 Plancherel 若后文不用，移到选读，避免突然从粒子分类跳到调和分析。

#### ch08 Lie 群、李代数与标准模型

- 必须拆成新第 11、13 章。根权最高权的母理论不能与标准模型、拓扑荷、GUT、seesaw 压在 421 行内。
- Lie 章补齐 Cartan 子代数、简单根、基本权、Weyl 群、维数/character 公式之间的依赖；$SU(3)$ 权图作为完整例子。
- 标准模型章先列一代场表示与 $Q=T_3+Y$，再讲 Yukawa/Higgs、反常抵消和味混合。
- Yang--Mills 拓扑需要纤维丛、有限作用量边界和 winding 的先修；若只给结论，降为选读接口。
- $SU(5)$、$SO(10)$、seesaw 不属于标准模型群论的必要闭环。保留时应明确“超出标准模型的表示组织示例”，不能和已验证结论混写。

### 5.4 GroupTheory 的深度边界

- 主线证明：陪集分割、商群良定义、Schur、Maschke、矩阵元/character 正交、投影算符、$SU(2)$ irreps、CG 分解、Young 对称化。
- 讲结论并给证明思路：Sylow、Frobenius 互反、Weyl character、Wigner 分类。
- 技术附录：Jordan--Hölder、Clifford 定理、Ponzano--Regge、完整 LR、Lorentz 主系列、GUT 分支规则。
- 查表附录：点群/双群 character、CG/3j/6j convention、空间群记号。

## 六、MathSkills 重构

### 6.1 新定位

MathSkills 应是“物理中反复复用的数学结构”教材，而不是把所有高级数学和统计学放在一个文件序列中。每个主题必须回答三个问题：对象是什么；保证结论成立的假设是什么；物理计算中怎样调用。具体物理模型只作验证接口，不能发展成第二套 AdvancedPhysics。

建议把 23 章重组为约 29 个较短章节；若将 likelihood/Bayes 或线性模型/回归继续拆分，最终可在 29--31 章之间。章数增加不是扩张内容，而是把当前数千行巨章拆成有稳定先修关系的单元，并删除跨书重复。

### 6.2 建议目录

#### 第一部　代数、Hilbert 空间与算子

1. **线性、张量与群作用的共同语言**：保留最少群表示接口，深层群论链接 GroupTheory。
2. **结合代数、Clifford 代数与 Spin**。
3. **Banach/Hilbert 空间、投影与对偶**。
4. **闭算子、伴随与自伴扩张**。
5. **谱测度、函数演算与含时传播**。
6. **紧算子、SVD、Schmidt 与 rigged Hilbert space**。

#### 第二部　分布、Green 方法与演化方程

7. **分布、Fourier 与 Sobolev 空间**。
8. **椭圆算子、基本解与伪微分观点**。
9. **Fredholm、积分方程与逆问题**。
10. **半群、弱解与非线性演化**。
11. **色散、孤子与可积模型（选读案例）**。

#### 第三部　微分几何

12. **流形、切余切、微分形式与流**。
13. **标架、向量丛与主丛**。
14. **联络、挠率、曲率与 holonomy**。
15. **Riemann 几何、测地线与 Jacobi 场**。
16. **Hodge 理论、上同调与边界条件**。
17. **分布、Frobenius、contact 与叶空间**。
18. **子流形与 Gauss--Codazzi--Ricci**。
19. **几何变分与 Ricci flow**。

#### 第四部　变分、时空与场

20. **作用量、Noether 定理与能动量张量**。
21. **Poincaré 几何和场表示接口**：只保留 MathSkills 所需的生成元与 Casimir，不重复 GroupTheory 的分类证明。
22. **曲率时空中的场与局域 Lorentz 结构**：vielbein、spin connection、协变作用量；高自旋目录降为附录。

#### 第五部　概率与统计推断

23. **概率空间、条件期望、随机样本与经验测度**。
24. **大数律、集中、CLT 与渐近线性化**。
25. **Gaussian 投影与精确抽样分布**。
26. **充分性、风险与有限样本估计**。
27. **Likelihood、Fisher、LAN、MLE 与 Bayes**：必要时再拆为频率/Bayes 两章。
28. **假设检验与局部似然几何**。
29. **一般线性模型、ANOVA 与回归**：若篇幅仍大，拆成“线性模型”和“回归/正则化”。

### 6.3 现有各章的具体处理

#### ch01 群、群作用与表示论

- 大幅收缩。第一同构、轨道--稳定子、Schur/Maschke、character 投影只保留后续数学章节会直接调用的版本。
- CG 与物理选择定则迁回 GroupTheory；MathSkills 只讲张量积和 intertwiner 的一般语言。
- Lie 代数、伴随表示和 Casimir 可保留为几何/场论接口，但 $SU(3)$ 具体生成元不应在章尾另起小专题。

#### ch02 结合代数、Clifford 与旋量

- composition algebra 作为动机或选读，不让复数--四元数--八元数目录阻塞 Clifford 主线。
- 核心链：universal property—PBW/维数—正交反射—Pin/Spin—旋量模—chirality。
- gamma 矩阵、Dirac current 只是表示实例；Dirac 动力学留给 AdvancedPhysics。
- 八周期证明和 maximal isotropic polarization 可分“实分类/复旋量”两条阅读路径。

#### ch03 Hilbert 空间、闭算子与紧算子

- 拆为新第 3 和第 6 章；无界算子基础移到新第 4 章。
- Banach 泛函分析基本定理不必都长证：开映射/闭图像/一致有界给清楚依赖，Banach--Alaoglu 的完整拓扑证明可入附录。
- SVD、polar、Schmidt 放在同一紧算子应用章；rigged Hilbert space 在分布章之后回看更自然。

#### ch04 谱理论与算子方法

- 必须拆成至少三章。当前 4,543 行并存 Sturm--Liouville、自伴扩张、谱测度、二次型、稳定性、传播和可解模型。
- 新第 4 章：闭对称算子、deficiency、boundary triplet、Krein。
- 新第 5 章：谱测度、函数演算、resolvent、Stone 与传播。
- 二次型/Friedrichs/min--max 可作为第 5 章后半或独立短章。
- Sturm--Liouville 是贯穿实例，不应在抽象理论前占 1,147 行。
- 当前章尾出现 Schmidt 分解，应迁到紧算子章，说明现有章节已发生主题泄漏。

#### ch05 广义函数

- 改名为“分布、Fourier 与 Sobolev”，先固定检验函数空间与拓扑，再讲分布运算和 tempered Fourier。
- 奇异核、基本解、Sobolev/伪微分应按后续 PDE 所需组织，不作公式目录。
- 当前尾部 Gauss 周期、正十七边形等代数数论内容与本章无关，移入独立选读附录或删除。

#### ch06 积分方程、Fredholm 与逆问题

- 初等分类压缩成短入口，立刻用算子 $I-\lambda K$ 统一。
- Fredholm alternative、analytic Fredholm、谱滤波和 Tikhonov 是核心链。
- 卷积、Hilbert 变换和奇异积分迁到分布/Fourier 章；Euler 型形式变换若缺乏路径、分支和逆公式，不应保留在主教材。
- 反问题必须明确噪声模型、源条件、正则参数和误差率，而不只列滤波函数。

#### ch07 非线性 PDE

- 拆为“演化方程方法”和“非线性波/可积案例”。
- 第一章：半群/Duhamel、局部适定、blow-up alternative、特征线、弱解、熵条件、能量法。
- 第二章只选择 Burgers、KdV、NLS 中两条互补案例，展示耗散与色散；Lax/反散射作为高级路线。
- 从一般方程到长波/NLS 约化必须写出尺度和余项，不能只给形式多尺度展开。

#### ch08 切空间、流与 Lie 导数

- 结构基本合理，改成稳定 subsection：切向量、映射与横截、流/Lie bracket、拉回与 Lie 导数。
- Poincaré 引理需要先说明局部星形域；Cartan calculus 的两次相似推导合并。

#### ch09 标架、余标架与非完整性

- 与向量丛/主丛入口整合成新第 13 章。
- Maurer--Cartan 是 Lie 群标架的核心例子；不要在联络尚未定义时提前展开 holonomy。
- 章末“structure group reduction—connection—holonomy”只作路线预告，具体结论后移。

#### ch10 联络、挠率与曲率

- 区分向量丛联络、切丛 affine connection、principal connection 三层，给出明确映射关系。
- gauge 换标架律只推一次；曲率扰动、Bianchi、Chern--Weil、path ordering 分成 subsection。
- Chern--Weil 若保留，需要先给不变量多项式与 de Rham class 的必要背景；否则移入高级附录。

#### ch11 度量与 Levi--Civita

- 拆分“局部 Riemann 几何”和“全局比较几何”。Koszul、曲率收缩、测地线、指数映射、Jacobi 为核心。
- Bonnet--Myers、Bishop--Gromov 依赖完备性与比较工具，可作为选读，不应和第一次定义度量同章等量齐观。

#### ch12 Killing、体积与 Hodge

- Killing 场可放入 Riemann 几何章结尾；Hodge 星、余微分、Laplacian、分解与 Poincaré 对偶形成独立章。
- 边界 Hodge 自伴域应明确引用算子章，不重新证明全部闭算子理论。
- “Killing 流与 Hodge 相容性”适合作为章末综合命题，不另成大节。

#### ch13 Frobenius

- 核心章讲分布、involutivity、Pfaff 与积分叶。
- contact 作为最大非可积对照；symplectization 是应用。
- Ehresmann、主丛水平分布、曲率与 holonomy 迁回联络章，避免相同概念在 ch10/ch13 双重建立。

#### ch14 几何演化 与 ch15 子流形

- 调换顺序：先讲子流形、第二基本形式、Gauss--Codazzi--Ricci 和面积变分，再讲一般度量变分与 Ricci flow。
- ch15 的三维曲面只是任意余维理论的特例；保留一个完整曲面算例，删除公式百科。
- ch14 区分纯 diffeomorphism 变化、真正 metric variation 和 gauge fixing；soliton 在 Ricci flow 之后。

#### ch16 Poincaré 与 Noether

- 拆成 Noether 主章和 Poincaré 接口章。当前 11 个 section 把群论、场表示、变分与能动量放在一起。
- MathSkills 的核心是作用量变分、Noether、canonical/Hilbert/Belinfante 能动量之间的关系。
- Wigner 分类迁回 GroupTheory；这里只给 Casimir 结果供场论调用。
- “记号与约定”移入 frontmatter，不作为 section。

#### ch17 曲率时空场论与自旋分类

- 核心保留 vielbein、spin connection、协变作用量、Hilbert 张量、Einstein--Hilbert 变分。
- 再次出现的 Wigner 分类删除，避免与 ch16 和 GroupTheory 三重重复。
- 自旋 $0,1/2,1$ 可作协变导数实例；$3/2,2$、Fronsdal、helicity amplitude 是另一门高自旋/QFT 课程，移入高级附录。
- 明确“曲率时空局域 Lorentz 表示”与“平直时空全局单粒子表示”不是同一分类问题。

#### ch18 概率模型、样本与经验分布

- 先补齐概率空间、随机变量、分布、积分和条件期望的最小基础，再进入统计模型。
- martingale、disintegration 若要保留，必须先建立 filtration/regular conditional probability；否则降为选读。
- 常用分布按生成机制和参数约定组织，数值例子只保留能检验量纲或参数化的少数。

#### ch19 大数律、CLT 与渐近线性化

- 当前第二 section 1,154 行，拆为“LLN/集中/统一律”“CLT/Delta/M-estimation”“经验过程/分位数”至少三个单元。
- 区分点态 LLN、uniform LLN、Donsker 与 martingale 结果的假设；不能用“统一收敛”统称。
- 数值验证不替代理论；保留一个均值、一个分位数案例即可。

#### ch20 正态样本投影

- 母结构很好，保留 Gaussian whitening、正交投影、Cochran、Wishart、$\chi^2/t/F$。
- 单样本/两样本区间与检验不要在 ch20 和 ch22 重复；ch20 负责分布，ch22 负责决策。
- Satterthwaite 明确是矩匹配近似，不与精确投影定理并列。

#### ch21 充分性、估计、似然与 Bayes

- 必须拆分。当前把有限样本决策、局部渐近、MLE、错设、Bayes/BvM 全压入三节。
- 新第 26 章：充分/完备、Rao--Blackwell、Lehmann--Scheffé、风险、Cramér--Rao 与 James--Stein。
- 新第 27 章：QMD、Fisher、LAN、MLE、错设 sandwich；Bayes posterior 和 BvM 作为后半或独立章。
- 明确支持集依赖参数、边界、不可识别与高维时哪些定理失效。

#### ch22 假设检验

- 保持“检验决策—NP/Karlin--Rubin—LAN 几何—Pearson—精确正态”链。
- permutation/randomization test 在给定群不变性后出现，不能只凭“交换标签”默认精确。
- LR/Wald/Score 先写共同法向投影，再比较有限样本差异，避免三次重复推导。

#### ch23 一般线性模型

- 若仍超过约 1,000 行，拆成“GLS/ANOVA/嵌套模型”和“回归/诊断/正则化”。
- 先固定设计与随机设计的条件语义，再讲 Gauss--Markov；正态性只用于精确 $t/F$。
- ridge/lasso 放在估计目标和损失之后。预测/估计误差的 RE/compatibility 条件与精确 support recovery 的 irrepresentable + beta-min 条件严格区分。
- 例题减少手算数字，优先展示设计矩阵、投影、自由度和诊断图怎样对应。

### 6.4 附录重组

- 当前“微分几何常用公式”和“微分几何练习”应成为明确命名的附录，而不是在主入口中临时写两个 `chapter`。
- 建议附录：A 记号与线性代数恒等式；B 技术泛函分析证明；C 微分几何公式表；D 概率分布与渐近记号；E 分部习题与提示。
- 任何正文删除的高级材料先进入“候选附录池”，二次审查后再决定保留，避免把附录变成垃圾场。

## 七、跨书去重与接口设计

### 7.1 必须消除的重复链

1. **CG/Wigner--Eckart**：GroupTheory 主讲；AdvancedPhysics ch16 应用；MathSkills 只保留 intertwiner 语言。
2. **Clifford/Dirac**：MathSkills 主讲代数；GroupTheory 讲 Lorentz 表示；AdvancedPhysics 从最小耦合和 FW 开始。
3. **Poincaré/Wigner 分类**：GroupTheory 主讲；MathSkills Noether 章只引用 Casimir；曲率时空章不再重复。
4. **自伴与 Green**：MathSkills 主讲一般理论；AdvancedPhysics ch11/ch14 只证明模型特有定义域、跳跃和可观测量。
5. **群投影与分子振动**：GroupTheory 给投影公式；AdvancedPhysics 展示 Hessian 怎样分块，不再证明 Schur/Burnside。
6. **Landau--Zener**：只在 AdvancedPhysics 非绝热章完整推导；含时微扰章只前引。
7. **Gaussian/压缩代数**：AdvancedPhysics 量子光学章主讲；Franck--Condon 章只调用 Duschinsky 参数化。

### 7.2 接口段模板

跨书调用时使用固定四段式：

1. 本章需要的外部结论是什么；
2. 本书采用什么记号和归一化；
3. 在当前系统中对象具体对应什么；
4. 哪个新物理结论由此产生。

接口段禁止重新证明主讲义已有定理，也禁止只写“由群论可知”而不给映射关系。

## 八、重写执行顺序

### 阶段 0：冻结现状与建立迁移表

- 为所有现有 chapter/section/derivation 生成清单，标记 keep / rewrite / move / appendix / delete。
- 建立旧 label 到新 label 的迁移表；重构期间可暂留兼容 alias，最终清除重复标签。
- 建立三本书共同 symbol registry 和内容所有权表。

### 阶段 1：先改目录，不改公式

- 创建新 chapter/section/subsection 骨架。
- 只移动现有段落，暂不润色，确保没有内容在搬迁中丢失。
- 每章顶部写“输入—输出—后续用途”三句内部说明，待正文闭合后改成自然导言。

### 阶段 2：只写正文骨架

- 暂时隐藏所有 Derivation、Example、Note 和习题答案。
- 重写连续正文，使定义、核心方程、假设、结论与过渡完整。
- 若删除推导后某结论消失，先把结论移回正文；若删除例题后理论不闭合，说明例题承担了母理论职责，必须修正。

### 阶段 3：逐个重建推导

- 对每个旧框问：正文是否已陈述结论；是否有不可省略的困难步骤；后文是否使用；能否拆成一个问题。
- A 类内联，B 类重写，C/D 类移附录或删除。
- 推导中只编号后文引用的结果；中间步骤用无编号环境。

### 阶段 4：例题、图和习题

- 每个核心结构配一个代表性例题，不用五个近同例子堆覆盖率。
- 图必须对应“结构、参数区间或可观测量”，不是装饰。
- GroupTheory 习题解答从正文分离；MathSkills 和 AdvancedPhysics 建立分部习题，不在章尾突然加入新理论。

### 阶段 5：跨书回归

- 检查所有跨书引用、符号、Fourier/度规/单位/内积 convention。
- 同一结论只保留一个主证明；其他位置的接口段必须与主版本完全一致。
- 三本书和 FreeElectronQuantumOptics 一起编译，防止公共 preamble 或宏调整造成回归。

## 九、建议实施批次

1. **结构先导 PR**：只加入新目录、迁移表和 frontmatter，不大改公式。
2. **GroupTheory 基础 PR**：现 ch01--ch04 拆章，建立跨书表示论接口。
3. **MathSkills 分析 PR**：现 ch03--ch07 拆章，为 AdvancedPhysics 的谱/Green/演化提供稳定引用。
4. **AdvancedPhysics 统计 PR**：现 ch01--ch10 压缩为六章。
5. **MathSkills 几何 PR**：现 ch08--ch15 重排，先子流形后几何演化。
6. **AdvancedPhysics 场与开放系统 PR**：现 ch11--ch15，重点拆 ch13/ch15。
7. **GroupTheory 连续群 PR**：现 ch05--ch08 重排为转动、Young、Lie、Lorentz、标准模型。
8. **AdvancedPhysics 原子分子 PR**：移动 ch25，去重 ch16--ch28。
9. **MathSkills 统计 PR**：现 ch18--ch23 拆章并统一有限样本/渐近/决策层次。
10. **全书编辑 PR**：符号、交叉引用、习题、图形与 PDF 版面最终统一。

每个 PR 都应是可独立编译、可独立审阅的叙事闭环；不要一次提交三本书的全部搬迁和全部公式改写。

## 十、验收标准

### 10.1 结构

- 不存在超过 1,200 行而未给出拆分理由的章。
- 不存在超过 400 行且内部包含多个独立问题的 section。
- 不使用 `paragraph`、`subsubsection` 或行首粗体充当导航。
- 每章开头说明前置问题与本章输出，结尾只总结已建立结果和下一依赖。

### 10.2 正文与推导

- 隐藏全部 Derivation 后连续阅读，核心概念、公式、假设和结论仍完整。
- 每个推导框只有一个明确目标；正文不复制框内整段计算。
- 主线框原则上不超过 60 行，超过 80 行必须拆分或移入技术附录。
- 不以“显然、容易得到、类似可得、推广可得”跳过关键步骤。

### 10.3 数学与物理

- 一般理论先于特殊模型；形式精确表达先于近似。
- 每个近似写出起始方程、控制参数、截断阶、误差量级和失效条件。
- 第一次出现的重要符号说明类型、空间、单位和物理意义。
- 全量审计量纲、指标、共轭、符号、积分测度、$2\pi$、$\hbar$、$c$、Jacobian、简并度和归一化。

### 10.4 跨书一致性

- CG/Wigner、Clifford、Poincaré、自伴谱理论等主题只有一个主证明版本。
- 跨书接口明确映射当前变量，不使用无内容的“参见某章”。
- Fourier、Minkowski 度规、内积线性变量、连续态归一化、Green 边界条件和 SI/自然单位切换全书统一。

### 10.5 出版质量

- 三本书完整编译，无 LaTeX error、undefined control sequence、undefined reference、重复 label 和明显 overfull。
- 每次结构改动抽查目录、章首页、长公式页、推导框跨页和习题页。
- 生成 PDF 后按每章至少一页正文、一页公式密集页、一页推导/例题页做视觉 QA。

## 十一、第一轮实际开工建议

不要从最容易润色的短章开始。第一轮应选择最能验证新架构的三个“压力测试”：

1. AdvancedPhysics ch15：拆成“精确约化”和“Markov/GKSL”，验证正文闭合与应用降级规则；
2. GroupTheory ch05：拆成“$SO(3)/SU(2)$”和“角动量耦合”，验证一般理论、公式表和高级附录的边界；
3. MathSkills ch04：拆成“自伴扩张”“谱测度/传播”“二次型/稳定性”，验证超长数学章的重建流程。

这三个样板通过后，再按相同规则批量处理其余章节。否则直接全面搬迁，很容易只把旧内容换一个目录位置，而没有真正改变正文与推导的职责。
