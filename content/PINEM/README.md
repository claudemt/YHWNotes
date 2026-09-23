# PINEM R16 — Derivation Rebuild

本版以 R15 深度重构为唯一基线，重点不是继续调整目录，而是把主线中的关键推导逐式闭环：明确每一步从哪条精确方程开始、代入了什么定义、采用了什么近似、舍弃项的控制参数是什么，以及近似失效后应退回哪一级理论。

## 正文唯一主线

1. Dirac 最小耦合与自由正负能结构；
2. 精确载波剥离与 P/Q 分块；
3. Feshbach–Schur 精确消元；
4. 二阶虚跃迁与相对论质量张量；
5. 规范协变正能包络方程与 eikonal/PINEM 一阶极限；
6. 任意外场特征线解 → 单色轨迹 Fourier 投影 → beta → Jacobi–Anger → Bessel 边带；
7. Maxwell 算符 → Green 张量 → T 算符 → 可计算近场；
8. 复杂 VSH/VSWF → 单球精确 Mie → 轨迹投影；
9. 精确 Mie → Rayleigh 长波极限；
10. 有限脉冲 → 延迟依赖边带；
11. 从单轨迹到实验统计与可观测谱。

## 正文结构

- `content/ch01.tex`：从 Dirac 方程到正能一阶输运方程；
- `content/ch02.tex`：PINEM 核心——轨迹相位、相位匹配与 Bessel 边带；
- `content/ch03.tex`：一般 Maxwell/Green/T 响应；
- `content/ch04.tex`：球形 VSH/VSWF 与精确 Mie 近场；
- `content/ch05.tex`：Mie 的 Rayleigh 受控极限；
- `content/ch06.tex`：有限脉冲；
- `content/ch07.tex`：实验平均、可观测量与适用范围。

## 附录

平方 Dirac、自旋修正、固定自旋双带逐分量复核、非相对论与 FW 复核、Green 谱表示、多层/多球/圆柱、一般椭球、多频驱动、解析级数以及完全失相干模型均保留在 `appendices/`，但不参与第一次阅读的主推导。

## 全局约定

- SI 单位制，显式保留 `c`、`\hbar`、`\epsilon_0`、`\mu_0`；
- 正基本电荷 `e>0`，电子电荷 `q_e=-e`；
- phasor convention 为 `\exp(-i\omega t)`；
- 真实电子通道能量与无反冲等间隔有效梯使用不同符号；
- 所有近似只在真正删项/截断处声明，并给出控制参数；
- 具体几何和命名模型只建立在一般理论之后。

## 构建

入口为 `main.tex`，使用 XeLaTeX 编译。交付包包含已编译 `main.pdf`，不包含编译中间文件。
