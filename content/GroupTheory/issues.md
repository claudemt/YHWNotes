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
