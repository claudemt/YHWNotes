# GroupTheory issues

## 2026-09-16 结构对齐
- 已从独立 main.tex/preamble.tex 迁移到项目统一构建（`python main.py build GroupTheory`）。
- 定理色块已上提到根 preamble.tex，本书不再保留独立 preamble。
- 章节文件从嵌套 content/GroupTheory/content/GroupTheory/ 提升到 content/GroupTheory/。
- preamble.tex 补 `\appref` 宏和中文 `\crefname`；补 `\DeclareSIUnit{\fm}{fm}` 和 `\DeclareSIUnit{\barn}{barn}` 修复 AdvancedPhysics 预存问题。

## 2026-09-16 内容充实（ch01-ch02）
- ch01: D₃ 系统分析（几何定义、乘法表、Cayley 图、子群格、Derivation）
- ch01: 共轭类几何解读、类方程应用、群作用物理应用、正规子群几何解释
- ch01: 半直积 D₃≅C₃⋊C₂ 用几何语言重写（反射如何"扭转"旋转）
- ch02: D₃ 显式矩阵+Derivation、几何特征标表、NH₃ 振动分析、Maschke 物理意义

## 2026-09-16 跨章节 D₃ 线索连接（ch03-ch06）
- ch03: NH₃ 的 C₃ᵥ 连接回 ch01 D₃；C₃ᵥ 特征标表连接回 ch02 D₃ 特征标表
- ch04: 三等价位置 C₃ᵥ 例子连接回 ch01 D₃ 作用在正三角形顶点上；补 NH₃ 振动模引用
- ch05: j=1 表示限制到 D₃ 分解为 A₂⊕E 的 branching 例子
- ch06: S₃ [2,1] 表示连接回 ch01/ch02 D₃ E 表示，明确 S₃≅D₃≅C₃ᵥ 三重同构

## 2026-09-16 Derivation 环境补充
- ch03: 晶体制约定理加 Derivation 环境（整数迹约束三步推导）
- ch04: Bloch 定理加 Derivation 环境（同时对角化→位置表象→提取周期因子）

## 构建状态
- GroupTheory: 195 页，0 undefined，0 error ✅
- MathSkills: 476 页 ✅（回归测试）
- AdvancedPhysics: 344 页 ✅（回归测试）

## 2026-09-24 refactor_0924 深度重构

- 全书重组为 22 章：群与群作用、表示论、点群与空间群、旋转与角动量、Lie 群与粒子物理五部分分层展开；基础群论与表示论不再挤在同一章，Lorentz 群与 Poincaré 群也各自独立成章。
- 重建 Lie 理论核心：从单参数子群、指数映射、BCH 公式和伴随表示，推进到根、权、最高权与 Weyl 群；随后以 SU(3) 张量积分解、Lorentz 有限维场表示、Wigner 粒子分类和标准模型表示闭合应用链条。
- 重写导论与多个章首，以具体对称操作和物理问题引出抽象结构；压缩“主线”“路线”“接下来做什么”等报告式提示，把例题和说明融入连续讲述。
- 旧的 Yang--Mills、拓扑缺陷、SU(5) 与 seesaw 材料移入附录，避免抢占正文主层级；全书示例环境压缩到约每章一个，同时保留必要推导。
- 最终构建：281 页；544 个标记、176 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 missing character、0 `\\boxed`。

## 2026-09-24 Lie 理论与粒子物理继续深化

- ch17 从闭矩阵群的定义和切向量独立性起步，证明线性化约束给出 Lie 代数、单参数子群与生成元一一对应、Lie 括号封闭，并完整证明 \(SU(2)\to SO(3)\) 是核为 \(\{\pm I\}\) 的二重覆盖。
- ch18 补入根串定理及其 \(\mathfrak{sl}_2\) 证明，由此推出 Cartan 整数与最高权的整性条件；同时区分复化代数 \(\mathfrak{sl}(3,\mathbb C)\) 的 Killing 形式和紧实实形式 \(\mathfrak{su}(3)\) 上的负定形式。
- ch19--ch22 逐步推导 Gell--Mann--Okubo 质量关系、颜色单态、有限维 Lorentz 幺正表示的平凡性、Poincaré Casimir 算符和 little group；标准模型一章由局域对称性推出规范联络与场强，再算出电弱真空稳定子、规范玻色子质量和一代费米子的全部局域与整体反常抵消。
- 最终构建与结构审计：289 个 PDF 页面，553 个标记、362 个引用，0 失效引用、0 重复标记、0 hard error、0 overfull、0 missing character；新增关键页已逐页渲染抽查。
