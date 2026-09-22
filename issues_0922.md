# YHWNotes 深度审计报告（2026-09-22）

**审计对象**：PR #1 `refactor: streamline derivations across three lecture notes`（commit `327dd74`，已 squash 合并入 `main`），改动 `content/AdvancedPhysics`(28 章) + `content/GroupTheory`(8 章) + `content/MathSkills`(23 章) 共 59 个章节文件，+3277 / −9198。

**审计方法**：`SKILL.md` §6 的六层流程（静态搜索 → 符号审计 → 逐式数学审计 → 结构审计 → 图形审计 → 最终 PDF QA），叠加：
- 行级 / hunk 级 diff 量化（区分"真删内容"与"改框边界"）；
- 三路逐章深审（每本书一个独立审计员，逐个 Derivation 读 diff）；
- 对深审结论的关键项做独立复核（下文标 ✅ 者为复核为真，❌ 为复核为假，无标记者属深审报告原文、未逐条复核）。

---

## 0. 结论摘要

1. **三本书用了三种不同手法，不是一个"压缩"动作**：AdvancedPhysics = 拆解 + 删节 + 压缩；GroupTheory ch01–06 压缩、**ch07–08 是重写（删数学）**；MathSkills **几乎只挪推导框边界，数学一字未动**。
2. **PR 自述的"推导框体量"指标在 MathSkills 上不成立**：`推导框平均 102.2 → 51.3 行、>100 行 = 0` 是把 `\end{derivation}` 提前造成的，正文那部分数学原地保留、逐字节未改。
3. **没有产生破坏性引用错误**：三本书 0 悬空 label、0 重复 label、0 undefined reference；AP 的 35 条跨章引用全部可解析，被引用的 28 个公式块前后逐字节相同。编译 0 error、0 overfull。
4. **主要风险集中在"结论代替推导"**：AP ch13 主线（Dirac 正则场 → 自伴性 → Schott 动量 → Liénard 功率）与 GT ch08（Killing 形式非退化、异常抵消、Goldstone 计数）被压成断言，违反 SKILL §1「重要结论必须真正算出来」。
5. **一批机械替换残留**：AP 新增 278 处「先讨论/随后讨论」模板句与中英空格丢失；MS 因删掉步骤标签产生 24 处悬空「第 N 步」；GT ch07/ch08 编号公式密度飙到 9.5–11.1 条/百行（其余章 0.66–2.12），45/47 条从未被引用。
6. 深审报告有一处**误报已排除**（GT ch02:1612 的因式分解实为正确），处置时不要按误报改动。

---

## 1. 事实层：重构到底做了什么

### 1.1 行数分解（推导框内 vs 框外）

| 书 | 推导框内行 | 框外正文行 | 总行数 | ≥20 行的大块删除 | 最大连续删除 |
|---|---:|---:|---:|---:|---:|
| AdvancedPhysics | 9189 → 7183（−22%） | 14866 → 14967 | 24055 → 22150 | 27 块 / 1280 行 | 153 行 |
| GroupTheory | 4136 → 1003（−76%） | 15411 → 14800 | 19547 → 15803 | 71 块 / 3236 行（新增大块 **0**） | 139 行 |
| MathSkills | 14723 → 7484（−49%） | 17808 → **24777** | 32531 → 32261 | **6 块 / 191 行** | 57 行 |

### 1.2 三本三种手法

- **AdvancedPhysics = 拆解 + 删节 + 压缩**
  ch13 推导框 6 → 12 个（长推导切开重写）；`物理意义`块 143 → 11；`\boxed` 334 → 320；删除整节（如 ch11 `薄板振动的材料参数与实验数值`）。ch13 行数 1881 → 1013。
- **GroupTheory = ch01–06 压缩，ch07–08 重写**
  ch07 1054 → 273 行、ch08 1874 → 422 行。ch08 删掉 7 个 `definition`、6 个 `proposition`、6 个 `theorem`、4 个 `example`、1 个 `corollary`、2 个 `proof`、2 个 `remark`、149 个 `equation*` 与唯一一张 TikZ 根图（旧值/新值均经复核 ✅），只留 45 个编号公式。ch01–06 则是删伪标题、删分点、简化证明，骨架（定义/定理/例）基本保留。
- **MathSkills = 只挪框边界**
  ch04 与父提交**行级相同率 98.3%**，最长连续未改动块 **592 行**；全部 75 个 hunk 都是单行编辑（`\end{derivation}` 上移 + 重写 `\begin{derivation}[标题]`）。ch21 最大删除块仅 7 行。**数学内容原地保留，只是不再被算作"推导"**——这正是 §2「Derivation 只负责草稿纸层面的复杂数学」被反向执行的地方：原本该留在框里的 Cauchy 数据、变参数积分方程、$AC_{\rm loc}$ 论证现在渲染为正文。

### 1.3 结构体计数（三本书合计）

| | 重构前 | 重构后 |
|---|---:|---:|
| `\textbf` | 1146 | 233 |
| `\item` | 532 | 386 |
| `\subsubsection` / `\paragraph` | 0 / 0 | 0 / 0 |
| `derivation` | 334 | 341 |
| `equation`（编号） | 1888 | 1873 |
| `equation*`（不编号） | 1157 | 843 |
| `显然 / 容易得到 / 类似可得` | 12 | **0** |
| `值得注意的是` | 1 | **0** |

被删的 `\textbf` 正是 `物理意义。`(46)、`实例。`(16)、`第一步：…`、`总结。`、`(i)/(ii)/(iii)` 一类伪标题。

---

## 2. 符合 SKILL 的部分

- **§4 引用完整性**：三本书 0 悬空 label、0 重复 label、0 undefined reference；AP 跨章引用 35 条全部可解析，被跨章引用的 28 个公式块**逐字节相同**——「引用了被删公式」这一最危险的破坏没有发生。
- **§2 去伪标题**：`\textbf{第N步}`、`\paragraph`、`\subsubsection` 归零；`\emph/`\textbf 外壳剥离（MS ch04 57 → 6、ch16 52 → 1、ch21 48 → 3）。
- **§1 去手挥短语**：三本书 `显然/容易得到/类似可得/推广可得/不难验证` 全为 0。
- **§4 Derivation 标题简短**：由百科式（「自伴扩张的完整理论：从微分表达式经 deficiency indices 到边界条件分类」）改为短语式（「Lagrange 恒等式与最小算子的伴随」）。
- **确有物理修正**：GT ch07 Haar 测度由错误的 `sinh η dη dμ dμ` 改为 Helgason 形式 `sinh²ζ dζ dμ_SU(2) dμ_SU(2)`；GT ch05 Ponzano–Regge 与 6j 修正；GT ch06 hook-content / 轴向距离修正。
- **编译结果**：AdvancedPhysics 344 页、GroupTheory 268 页、MathSkills 494 页、FreeElectronQuantumOptics 815 页；0 LaTeX error、0 undefined reference、0 significant overfull。

---

## 3. 缺陷清单

### P0 — 确定性错误（✅ 均已独立复核为真，可直接修）

| # | 位置 | 问题 | 修法 |
|---|---|---|---|
| 1 | `content/GroupTheory/ch03.tex:1569` | `这正是 eqnrefs{thm:neumann}；` **缺反斜杠**，编译不报错但照排成字面文字 | 改为 `\eqnrefs{thm:neumann}` |
| 2 | `content/MathSkills/ch17.tex:229,233`（共 5 处） | `ADM 贪` 系批量替换事故 | 全部改为 `ADM 质量` |
| 3 | `content/MathSkills/ch16.tex`、`ch17.tex` | 全章 **0 个 `\dd`**；ch17 有 **19 处裸 `d^dx`**（ch16 3 处）；同书其他章 `\dd` 用了 300+ 次 | `d^dx → \dd^dx`、`dx^\mu → \dd x^\mu`、`ds^2 → \dd s^2` |
| 4 | `content/AdvancedPhysics/ch19.tex:312` | `K(t)=\frac{v^2}{2}=\frac{2U_p}{1}(\cdots)^2` —— 空分母 `1` | 直接写 `2U_p`（$U_p=E_0^2/4\omega^2$，该式正确） |
| 5 | `content/AdvancedPhysics/ch24.tex:666` | `\sqrt{\frac{v!v'!}{}}` —— 空分母 | 补回分母（Huang–Rhys 因子归一化常数） |
| 6 | `content/AdvancedPhysics/ch20.tex:308` vs `ch20.tex:723` | 同一参数（800 nm, $10^{14}$ W/cm²）给 $U_p\approx9.3$ eV 与 $5.97$ eV 两值；308 行 $γ_K\approx0.81$ | **5.97 eV 正确**（$U_p=9.337\times10^{-14}I\lambda^2$），$γ_K$ 应为 ≈1.0；`ch20.tex:960` 的 9.3 eV 亦应为 ≈8.4 eV（该处 $1.4\times10^{14}$ W/cm²） |
| 7 | `content/AdvancedPhysics/ch23.tex:563` | `\chi=y^\varepsilon e^{-y/2}w(y)` —— `\ee` 被改回斜体 `e`（§4 记号回归） | 改回 `\ee` |
| 8 | MathSkills 12 个文件 24 处 | 悬空「第 N 步」：步骤标签已全删（全书 0 处 `第一步：` 定义），引用仍在。如 `ch01:260`「每个轨道对第三步总和的贡献」、`ch01:271`、`ch04:2500`、`ch05:1923`、`ch10:566`、`ch12:35/614`、`ch14:441/459`、`ch16:132`、`ch17:465`、`ch21:98/298/418` 等 | 按 §6 一次清完，改为内容性指代（「由上面建立的 form norm 等价」） |
| 9 | `content/AdvancedPhysics/ch13.tex:789` | `P_{\rm rad}=\frac{q^2\gamma^6}{6\pi\varepsilon_0c^3}[\cdots]` —— $\gamma$ 在 ch13 全章**从未定义**（全章 `gamma` 只出现 2 次：390 行的 $\gamma_A\gamma_B$ 与 789 行） | 定义 $\gamma$（或改写为 $1/\sqrt{1-v^2/c^2}$） |

### P1 — 违反 §1「重要结论必须真正算出来」

**AdvancedPhysics ch13（本次损失最重）**：主线推导链被压成断言——
1. `ch13:196-200` 旋转对称性 + 对 $z$ 两次求导直接给出 $\int\dd\Omega\,n_in_je^{-\ii z\vb n\cdot\hat{\vb r}}$ 的 $j_0''/j_2$ 关系，中间整段被删。
2. `ch13:450-481` 多极展开跳过 $k$ 阶展开与 $\vb\Pi_\perp\cdot(\vb I\cdot\vb n)=\frac13\vb\Pi_\perp\cdot(\vb{\mathcal Q}\cdot\vb n)$ 消元；四极角因子 $4\pi/5$ 全靠断言（值与结论经审计员验算正确，但正文无此步）。
3. `ch13:703-725` **循环论证**：用 $\frac12(\vb E_{\rm ret}-\vb E_{\rm adv})$ 去"校准"同一推导正在求的系数；旧文的协变局域喷流分类与"$O(\ell^3)$ 根修正不能省略"警告均被删。
4. `ch13:810-816` Fermi 世界管 $P_{\rm bound}^\mu$ 的系数直接断言（显式匹配被删）。
5. 符号首现无定义（除 P0#9 的 $\gamma$）：`ch13:215` $\vb J=\sum_aq_ac\boldsymbol\beta_a$ 中 $\boldsymbol\beta_a$ 无定义；`ch13:428` $\vb w$ 的定义式已删（且 876 行 $w$ 另作标量 $\dot\psi$）；`ch13:800` $L_{\rm loc}$、`ch13:898/916/929/938` $\mathcal F_\star$ 从未定义。
- 另：ch13 删除了全部多极物理（禁戒/选择定则/宇称/$(ka)^{2L}$）、硬频尾小节、$\omega\ln\omega$ 的 note、Schott 能量的 Gaussian 脉冲 Example。

**GroupTheory ch08（重写导致的数学缺失）**：
1. `ch08:19`「Killing 形式在单李代数上非退化，因此可作为内积」——直接断言，全书无一处验证。这是 Cartan 矩阵、根内积、Dynkin 标签的地基。
2. `ch08:46-52` 与 `ch08:61-68`：Freudenthal 递归的 Derivation 与正文公式**逐字相同**，没有任何一步递推计算。
3. `ch08:261` Weyl 维数公式靠「令 $H\to0$ … 比较最低非零阶」一句带过。
4. `ch08:158-177` 异常抵消、`ch08:151-156` Goldstone 计数均为断言（迹贡献表缺失）。
5. 全章**无一个具体根/权数值**（旧版 TikZ 根六边形与权图已删）：出现 SU(3) 维数公式却未列 $\alpha_1,\alpha_2$ 与 $\Lambda_1,\Lambda_2$。
6. `ch08:275-280` 与 `82-84`：`eq:3x3x3-decomposition` 与 `eq:baryon-decomposition` 内容完全相同，同一分解被编号两次。

**其余同类（深审报告，未逐条复核）**：
- `content/AdvancedPhysics/ch05.tex:290-298`：$T_n=\frac{1}{2\pi}\int_0^{2\pi}\phi\ee^{-\ii n\theta}\dd\theta$ 与 $\phi(\theta)=[1-k^2\sin^2(\theta/2)]^{1/2}$ 的**定义句被删**，`T_{i-j}`、`\phi` 首现即用；strong Szegő → $(1-k^2)^{1/4}=m^2$ 的中间式被"代入…并计算 Fourier 系数，得到"顶替（这两条在 ch08 已有，可搬回）。
- `content/AdvancedPhysics/ch11.tex:463-466`：声称"对四阶刚度算子直接做相空间计数"，实际只算 $p_4=|\boldsymbol\xi|^4$ 各向同性特例；一般结论在 `ch11:425` 仅以断言出现。
- `content/AdvancedPhysics/ch14.tex:1531-1543`：$SO(d+1)$ 隐对称性整块塞进推导框，Runge–Lenz 的 $[A_i,H]$、$[A_i,A_j]$ 全无；`ch14:1526-1528` 精确 Stark 能级 $E_{n,k}$ 被删（全书 `grep E_{n,k}` 无命中）。
- `content/AdvancedPhysics/ch21.tex:666-718`：$U_0,\Omega$、裸 $\Gamma$ 全章仅此一次出现且无定义（正文用 $U_+,C,\Gamma_{\rm sp}$）；`ch21:675` 由 $J_g=1/2\to J_e=3/2$ 特例反推一般（明违 §1）；亚多普勒标度只剩未定系数 $C_T=O(1)$。
- `content/AdvancedPhysics/ch27.tex:615-628`：Wang 变换对角化只剩"直接展开矩阵元 $\propto\delta_{\sigma\sigma'}$"，连比例系数都没有。
- MathSkills：**29 条带编号的重要公式只出现在 Derivation 内部且全文从未被引用**，删掉框即消失（§2 违反）。代表：`ch20:196-211` `eq:math-stat-gaussian-conditional` 与 `eq:math-stat-gaussian-schur-complement`（该节核心结论，正文没有）；`ch17:220` `eq:ms-curved-T-conservation`（$\nabla_\mu T^{\mu\nu}=0$）；`ch16:716/719/729/733`（角动量流/自旋流/总角动量/守恒律四条定义式）。

### P2 — 机械替换残留

1. **「先讨论/随后讨论/再讨论/接着讨论/进一步讨论/最后讨论」共 278 处**（AdvancedPhysics，重构前 0）：`先讨论`67、`随后讨论`67、`再讨论`66、`接着讨论`56、`进一步讨论`18、`最后讨论`4。把显式编号换成隐性编号，句法同构，反而更像提纲（§2）。例：`ch18:61`「先讨论Dyson 级数。」`ch16:481`「随后讨论6j 符号的定义与对称性。」`ch26:536`。
2. **中英间距丢失 +74 处**（AP 38 → 112）：`ch28:825`「先讨论Fano 模型。」`ch15:3671`「先讨论Zeno 效应」`ch15:3712`「随后讨论GKLS 表示」`ch01:552`「先讨论Griffiths」。另有英文词残留正文：`ch01:550` `monotonicity`、`ch01:439` `presuppose`。
3. **伪标题残迹「短语。 」（8 处，AP）**：`ch25:874`「推导要点。 对 Fock 态」`ch26:166`「实例。 水分子」`ch12:1309`「全息干涉法。 用激光全息术」等——粗体被删成纯文本，问题未解决还多了半角空格。
4. **元叙述残留（AP，4 处）**：`ch01:79`「而不需要把某个理想气体实例拼接进证明」；`ch02:330`「不再重复一套彼此矛盾的本征值计算」；`ch12:801`「因此该 Example 不依赖任何隐藏在 Derivation 中才定义的 Green 核符号」；`ch23:131`「这一步没有使用振动小振幅、刚性键长或慢转动等近似」。
5. **MathSkills「名词短语+句号」段落头 84 处**（✅ 复核计数）：`实例。`/`物理意义。`/`总结。`/`尾声。`/`后记。`/`推广方向。`/`推广与物理建模。` 等。最密集：`ch02:764/773/775`（同一推导框内连挂三段）、`ch02:1137/1143/1145/1147`（四连）、`ch08` 有 7 段 `推广与物理建模。`（95/365/420/502/665/733/851），每段都罗列 5–6 个物理领域。`ch03:601` 与 `ch03:603` 是近重复。
6. **MathSkills 元叙述互指「正文」9 处**：`ch06:1839/1841`、`ch20:757`、`ch21:1218`、`ch22:826` 等（「得到正文中的精确公式」「这正是正文\eqnrefs{…}」）。
7. **GroupTheory 提纲碎片**：`ch03:1495/1509`、`ch05:1434/1442/1471/1593`、`ch06:1603/1610/1621/1713/1784/1877`；`ch01:720`「这里故意没有把 $G/C_G(x)$ 当成商群来使用。」；MS 的 `ch16:534-576`（`高阶导数 Lagrangian.\enspace` 等四连）、`ch17:193-234`（五连 `.enspace` 伪标题）在 Derivation 框内。

### P3 — 结构与一致性

1. **GT ch07/ch08 编号公式泛滥**：ch07 26 条 `eq:`（22 条从未被引用）、ch08 47 条（45 条从未被引用），密度 9.52 / 11.14 条每百行，而 ch01–ch06 只有 0.66–2.12。违反 §1「只给重要公式编号；推导步骤用不编号的 `align*`/`equation*`」。
2. **GT ch08 环境全清空**：0 个 `definition`/`theorem`/`example`（旧版 24 个）。「Cartan 子代数」「单根/基本权」「Dynkin 标签」至少应恢复为 `definition`，GMO 质量公式应为 `theorem`。
3. **GT 证明环境两套并存**：98 处手搓 `\par\smallskip\noindent\textbf{证明.}` 与 27 个 `proof` 环境并行（重构前 36 个）。本次动了 GT 全部 8 章却未统一。
4. **GT 图未被引用**：25 个图 label 中 **19 个从未被 `\cref` 引用**（AP 10 个中 4 个）。重构前后完全相同，属"重写了每一章却没把图接进正文"（§6 要求局部问题升级为全局不变量）。
5. **MathSkills 环境不统一**：`ch04` 用 7 个 `\begin{example}`，其余 15 章全用 `\begin{exbox}`；`\section*{本章小结}` 只出现在 `ch16:828`、`ch17:630`。
6. **MathSkills 行内公式风格混用**：同一文件内 `$…$` 与 `\(…\)` 并存（`ch01` 356/436、`ch04` 3804/71、`ch16` 112/455）。
7. **MathSkills 引用宏混用**：19 处裸 `\cref{}`（`ch02:4`、`ch03:2`、`ch04:1`、`ch05:2`、`ch06:2`、`ch07:8`）应统一为 `\eqnrefs{}`。
8. **MathSkills 三处 `\\figref{}` 多一个 `\\`**：`ch06:1624`、`ch07:476`、`ch07:1308`（正文中制造硬换行）。
9. **MathSkills 图形缺口**：全 23 章只有 3 张图，且 ch18–ch23（统计推断，最易给定量图）为 0 张；`ch19`（CLT）、`ch20`（$\chi^2$/Wishart）、`ch23`（ridge 谱收缩、lasso soft-threshold）都是现成素材。
10. **AP 排版问题**：`ch16:88-113` 用 `&\hspace{8em}{}` 在等式内手工缩进凑对齐（§4 明令禁止用非关系符断行）；`ch16:500-508` 9 行连续空行；`ch03:253-263`、`ch05:310-319/535-540`、`ch06:409-419`、`ch07:380-388/433-439/466-475`、`ch09:375-384`、`ch17:249-253` 均有删改残留的连续空行。
11. **AP 孤 label（删掉引用句造成）**：`ch11:433/459`、`ch16:516`（与 ch18 引用的 `eq:wigner-eckart` 重复编号）、`ch21:669/673`、`ch22:608/620/639`、`ch23:555`、`ch27:613/623`、`ch28:305/777/830`（后者与 `ch28:745` 重复编号）。
12. **AP Derivation 被当主题倾倒场**：`ch07:347-389` 标题「临界自反模与宇称投影」下塞入任意子熔接、编织矩阵、拓扑码、实验候选等 8 个无关主题；`ch24:659-669`、`ch26:531-541`、`ch28:822-837`、`ch25:1060-1065` 四个新建 Derivation **整框复述正文**、无一行推导（违 §6）；`ch12:223-271` 与正文 38-124 高度重复；`ch25:974` 标题承诺的结论出现在下一框（1024）。
13. **AP ch03/ch04 结构**：`ch03:229-256` Matrix–Tree 的完整 Cauchy–Binet 证明裸露在正文、无小节无环境；`ch04:346-368` 闭曲面 $\pi_1/\mathrm H_1$ 三步推导同样裸在正文。

### P4 — 逐式审计发现（深审报告原文，未逐条复核）

**AdvancedPhysics**
- `ch14:263` 与 `ch14:271` 对 limit-point/limit-circle 给出**不一致阈值**（$0<\nu_l<1$ vs $0\le\nu_l<1$；$\nu_l=0$ 时两支可积，应为 limit-circle，263 行错）。
- `ch23:548` $D_e$ 在推导内是井深，`ch23:379` 编号式 $D_e$ 是离心畸变常数，`ch23:455` 表格用 $\tilde D_e$ —— 同一符号三重身份。
- `ch24:666` $S$ 与 `eq:huang-rhys` 的 $S_{\rm HR}$、`ch24:552` 的 $S$ 三种定义；`ch26:247` $\Gamma_{\rm total}$ vs `ch26:534` $\Gamma_{\rm tot}$；`ch01:56` Derivation 内裸 $Z,H$ 与正文 $Z_\Lambda,H_\Lambda$ 不一致；`ch21:721` 用 $\delta,\Gamma$ 而全章用 $\Delta,\Gamma_{\rm sp}$；`ch28` Feshbach 段 $\delta\mu$ 未定义。
- `ch27:580-581` 水分子 $K=\pm1$ 块：代入 $A=27.877$、$B=14.512$ 得 27.877/14.512，与文中 23.398 不符（非对角元被当 0）；末句"与实验值完全吻合"是把同一组数与自己比较——**本次重构恰好删掉了能定非对角元的推导**。
- `ch20:960` ATI 算例：$U_p\approx9.3$ eV 与 $\gamma_K\approx1.0$ 互斥（由 $U_p=I_p/(2\gamma_K^2)$ 应为 6.05 eV）；$E_n=(n+s)\hbar\omega-2U_p$ 也算不出 $E_8\approx-4.5$ eV。
- `ch05:544`「分四步建立。」其后只有三段；`ch04:370`「分四步建立。」其后只剩两步（计数未同步）。
- `ch10:195-198` 引出句被删、公式块前只剩两个空行；`ch10:807` 段落以裸「（1）（2）（3）」开头；`ch06:408` 留下裸 `(i)(ii)(iii)(iv)` 枚举。
- `ch11` 删除 `\section{薄板振动的材料参数与实验数值}` 后，全书 `Seeley`/`亏指数`/`碳纤维`/`听鼓声` 零命中，`ch12:1305-1311` 的 Chladni 小节再无材料与几何参数可查；`content/AdvancedPhysics/issues.md` 仍声称 worldtube/Schott 的算例"已经在 ch13 完成"，与现状不符。

**GroupTheory**
- `ch02:1612` 的因式分解 —— ❌ **深审报告误报**：$x^3-2x^2-x+2=(x-2)(x^2-1)=(x-2)(x-1)(x+1)$ **正确**，不要改动。
- `ch07:142` $\omega_{\mu\nu}$ 首次出现无定义（conventions.tex 亦未登记）；`ch07:148` $S^{-1}\gamma^\mu S=\Lambda^\mu{}_\nu\gamma^\nu$ 直接断言；`ch07:152` Majorana 表示未定义即使用；`ch07:31` 非幺正性断言无证明；`ch07:187-195` Pauli–Lubanski 符号约定未给（$W^2=-m^2j(j+1)$ 依赖 $\epsilon^{0123}$ 约定，conventions.tex 未登记）；`ch08:201-206` Jarlskog 不变量符号约定未声明。
- `ch03:1569` 缺反斜杠（已列 P0#1）；`ch03:843` 用 `d^3r` 而非 `\dd^3r`；`ch07:10/12/190/210/226-233` 用 `\mathbf` 而非全书统一的 `\vb`（conventions.tex:52 规定拉丁向量用直立粗体宏 `\vb`）；`ch07:164` 表格塞进 `equation` 环境；`ch08:382` 用 `ln` 而非 `\ln`。
- `ch04:177/216` 未编号的 `\[…\]` 挂了 `\label`，`\eqnrefs` 引用后打印出的编号指向定理 4.3（`main.aux` 中 `\newlabel{eq:commutant-block-form}{{4.1}{115}…{theorem.4.3}}`）——**编号显示错误**；`ch04:1025` vs `1064` 磁多极算符宇称前后矛盾。
- `ch01:2188/2198` 两处并列小标题都写成 `(iii)`，`ch01:2204`「再由 (ii) 的扩张性质」在旧版指向 (iii)，改动后**指错条目**。
- `ch02:1229` 裸文本「定理（特征标的列正交关系）。」（旧有 7 处 `\textbf{定理（…）}`，清尾只清到剩 1 处）；`ch02:260` 重复给「简称不可约表示」；`ch02:1225/1227` 相邻整句重复；`ch02:736-738` 投影算子前后不一致；Peter–Weyl 定理陈述被删导致 $\hat f_\alpha^{ij}$、$\pi_\alpha^{ij}$、$\|\cdot\|_{HS}$ 主文中首现无定义；`ch02:1661` H2O/D3 群判定错误。
- `ch05:958-962` 因子 2 错误（与其自身证明矛盾）；`ch05:974-978` $O^D$ 类结构颠倒（36≠48）；`ch05:1002-1008` 双群特征标积应为 $(4,-1,0,0,0)$ 且夹着草稿式自纠「等等——实际上」；`ch05:2254-2263` 伪 3j 恒等式 $=1/3$，$\hbar\sqrt{3j(j+1)}$ 应为 $\hbar\sqrt{(2j+1)j(j+1)}$；`ch05:2118-2124` 保留草稿自纠。
- `ch06:1554-1560` 分支规则显示式 $[3]\downarrow=[2]\oplus[1,1]$ 与其下一行结论矛盾；`ch06:1741/1749` 幂和公式错误；`ch06:1171-1173` 与 `1371-1373` 整句重复；`ch06` hook-length 证明把关键一步外推给 `app:young-proofs`（附录存在，但主文因此缺一步）。
- `ch07:238-268` 结构与动机倒置：Haar/Plancherel 公式先给、动机与适用条件说明在后（违 §4/§5）。
- ✅ 已排除：悬空引用 0、重复标签 0、未定义控制序列 0、overfull 0、`第 N 步` 伪标题 0（ch07/ch08 从 86/194 清零）、ch07/ch08 裸 `i`/`d` 微分 0。

**MathSkills**
- D1 「第 N 步」悬空引用 24 处（已列 P0#8）。
- D2 `标题.\enspace` 伪标题：`ch16` 8 处、`ch17` 11 处、`ch21` 5 处。
- D3 重复推导：`ch01:203-207` 与 `ch01:278-296` 把 $p$-群中心定理推了两遍（巨型推导拆散后未合并）。
- D4 重要结论藏在框内 29 条（已列 P1）。
- D6 微分记号：`ch16/ch17` 全章 0 个 `\dd`（已列 P0#3）；另 `ch07` 3 处、`ch03` 3 处、`ch05` 2 处、`ch02` 1 处零星裸 `d`。
- D8 符号首现无定义：`ch01:209-213` 在有限群章节插入 Weyl 积分公式并用到 maximal torus / Weyl 群 / Weyl 分母，而本书直到 `ch01:1318` 才首现 maximal torus；`ch02:771` 直接使用 maximal torus、$N_G(T)$、$w_2(TM)=0$、$\widehat A$ 类。
- 543 个编号公式从未被任何 `\eqnrefs` 引用（`ch04:82`、`ch05:40`、`ch07:43`…）——按 §1 宜抽检是否降为 `equation*`，不宜机械全改。
- 模板句「接下来考察X。」235 处（`ch17` 23、`ch02` 22、`ch04` 21、`ch16` 20），重构前后完全一致，非本次引入。
- `ch01:120-175` 把 orbit–stabilizer 的证明放在正文已使用该公式（`131`、`132-150`）之后，属"先用后证"。

---

## 4. 2026-09-22 标题与排版改动（本次新增，已编译验证）

**`preamble.tex`**
- 章标题改为**一行**：`第N章 标题`，三号（16pt）粗体居中（原 `\Huge` 两行）。
- 部分页：独页两行，「第N部分」二号（22pt）/ 部分标题一号（26pt），居中；`part/break = \clearpage`、`part/hang = false`。

**章标题精简**：4 本书 70 章全部 ≤8 汉字（外文术语按 1 词计），62 章改写。

| 书 | 新标题 |
|---|---|
| AdvancedPhysics（28） | 配分函数的解析性 / Lee--Yang 零点 / 图的边界与圈空间 / 平面对偶与同调 / 高低温展开与对偶 / 转移算子的谱 / Clifford 线性化 / Onsager 精确解 / Yang 自发磁化 / 维里展开 / 自伴边界与 Green 谱 / 薄板振动 / 辐射反作用 / 中心势问题 / 开放系统动力学 / 角动量与张量算符 / Dirac 精细结构 / 原子光相互作用 / 强场经典动力学 / 强场量子动力学 / 激光冷却与磁阱 / 几何规范势 / 双原子分子谱 / Franck--Condon 原理 / 相干态与压缩态 / 分子对称性 / 激光诱导排列 / Fano 共振 |
| GroupTheory（8） | 群的基本概念 / 群表示理论 / 点群与空间群 / 群论与量子力学 / 转动群与旋量 / Young 方法与全同粒子 / 洛伦兹群 / 李群与李代数 |
| MathSkills（23） | 群作用与表示论 / Clifford 代数 / 闭算子与紧算子 / 自伴扩张与谱测度 / 广义函数 / Fredholm 理论 / 守恒律与可积性 / 流与 Lie 导数 / 标架与非完整性 / 联络与曲率 / 度量与联络 / Killing 对称 / Frobenius 定理 / 输运与度量变分 / 活动标架法 / Noether 定理 / 弯曲时空场论 / 经验分布与抽样 / 中心极限定理 / 正态样本几何 / 估计与 Bayes 推断 / 假设检验 / 一般线性模型 |
| FreeElectronQuantumOptics（11） | 数学与物理约定 / 经典规范场 / 量子场论基础 / 量子电动力学 / 量子色动力学 / 标准模型 / 量子激发 / 外场与量子交换 / 周期势与反冲 / 开放系统与测量 / 介质响应与反演 |

**编译结果**（改造后，全部 0 error / 0 undefined reference / 0 overfull）：

| 书 | 页数 | 变化 |
|---|---:|---|
| AdvancedPhysics | 344 | 348 → 344 |
| GroupTheory | 268 | 269 → 268 |
| MathSkills | 494 | 499 → 494 |
| FreeElectronQuantumOptics | 815 | — |

信息损失最明显的三个：`Cluster、Mayer、virial 与相互作用量子气体` → **维里展开**；`Born--Huang 展开、Born--Oppenheimer 近似与几何规范势` → **几何规范势**；`Moving frame 与 Gauss--Codazzi--Ricci 方程` → **活动标架法**。

---

## 5. 建议处置顺序

1. **P0 全部 9 项**（确定性错误，其中 8 项可脚本化 + 2 处手改）——最高性价比。
2. **P2 的 1/2 项**（278 处「先讨论」类模板与中英空格）可与 P0 一起做一次全局清理，顺带处理 8 处「短语。 」残留。
3. **决定 AP ch13 主线的处置方式**：补回中间等式（工作量最大）还是改写为「结论 + 指路」并在正文明确标注省略了哪些步骤。
4. **GT ch08 补齐最小可自学集**：Killing 形式非退化（$su(3)$ 上验算 3–5 行）、Freudenthal 在 $(1,1)$ 上递推一次、一张 TikZ 根图、恢复 definition/theorem 环境、把 45 条未被引用的编号公式降级。
5. **P3 的结构一致性**（GT 证明环境统一、图接进正文；MS example/exbox 与引用宏统一）。
6. **P4 列表按章抽检**（尤其 AP ch14:263 阈值矛盾、ch23 $D_e$ 三重身份、ch27:580 数值自比、GT ch02:1661 群判定、MS ch01 Weyl 公式前向引用）。

---

## 6. 复现命令

```bash
# 结构与行数量化
git diff --unified=0 327dd74^ 327dd74 -- content/MathSkills/ch04.tex | grep -E "^@@"
git diff --stat 327dd74^ 327dd74 -- content/

# 静态审计（三本书范围）
grep -rn "subsubsection\|paragraph" content/AdvancedPhysics content/GroupTheory content/MathSkills
grep -rnE "显然|容易得到|容易验证|类似地?可得|推广可得|不难看出" content/AdvancedPhysics content/GroupTheory content/MathSkills
grep -rn "^.chapter{" content/*/ch*.tex

# 编译
python main.py build AdvancedPhysics     # 单本
python main.py build --all               # 全部
pdfinfo example/AdvancedPhysics.pdf | grep Pages
```
