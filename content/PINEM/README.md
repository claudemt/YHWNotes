# PINEM R19 — One Master Equation, Then Applications

本版把正文压缩为五章。前两章完成并只完成电子动力学；后三章全部是同一个主方程的应用，不再把有限脉冲、Rayleigh、实验平均等内容包装成彼此并列的理论。

## 唯一电子输入--输出关系

1. Dirac 最小耦合约化到一阶/eikonal PINEM 主方程；
2. 沿特征线积分；
3. 单色场只留下复耦合 `beta`；
4. `c_n = exp[i n arg(-beta)] J_n(2|beta|)`，`P_n = J_n^2(2|beta|)`。

到这里电子理论结束。

## 正文五章

- `ch01`：Dirac → 正能一阶 PINEM 主方程；
- `ch02`：只解一次主方程，得到 `beta` 与 Bessel 边带；
- `ch03`：直接给定场时如何应用主方程：Gaussian、有限长度 sinc 相位匹配、指数近场、光锥失配、多区干涉、偏振、OAM、有限脉冲；
- `ch04`：场未知时先解 Maxwell：Green/T、精确 Mie，并在同一章内取 Rayleigh 极限；
- `ch05`：最后一步实验读出：时间平均、空间/孔径平均、PINEM 图像、相位灵敏读出与相干平均边界。

原 `ch06` 有限脉冲章和 `ch07` 实验平均章不再独立存在；有限脉冲并入 `ch03`，统计读出统一并入 `ch05`。原独立 Rayleigh 章并入 Maxwell/Mie 章，因为它只是精确场的长波极限。

## 新增的主方程应用

- 有限长度相互作用区：`beta` 的 sinc 相位匹配；
- 指数局域场：Lorentz 型空间谱；
- 两段相干作用区：`beta_total = beta_1 + exp(i Phi) beta_2`；
- 偏振控制：线性组合直接在线性 `beta` 上完成；
- OAM/角向谐波：`beta ~ exp(i ell phi)` 导致第 `n` 个边带获得 `n ell` 的角向相位，在轴对称条件下给出 `Delta L_z = n ell hbar`；
- 弱耦合 PINEM 图像：`I_PINEM ≈ |beta|^2`；
- 参考耦合干涉：把 `arg beta` 转成能谱强度振荡。

## 附录

A--D 保留推导复核、Green 谱表示、几何扩展和多频推广；E 只作为 Bessel 平均的矩展开工具；F 仍明确标为另一条 Poisson--Skellam 随机动力学分支。

入口为 `main.tex`，使用 XeLaTeX 编译。

R19 后续精简中，弱耦合也从主方程章移出，归入直接应用；附录 E 被压成一个矩命题和两个解析矩算例。周期/多中心结构新增结构因子 `beta_N`，用于直接描述阵列相干增强与准相位匹配。
