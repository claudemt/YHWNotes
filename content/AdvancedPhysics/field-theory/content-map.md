# 场论内容迁移与两册分工记录

2026-10-16 已按仓库 Skill 继续纠正记号、例题及基础错误，并整理正式文件名；当前路径、移动时哈希和验收见[本轮审计账本](../../../lecture-skill-audit-20261016.json)。下文原路径与哈希属于各自注明的历史快照，保留作为内容来源证据。

本次重构于 2026-10-13 开始，2026-10-14 收尾。开始时核实的 GitHub 主分支为 `1beb2ee`，已有四书润色先提交为 `8efe635`，以下保留审计以该提交为基线。完整的量子场论、量子电动力学、量子色动力学、标准模型、几何背景与共形量子态内容归入《高等物理》；《自由电子量子光学》以入射电子、量子交换、反冲、传播、测量和成像为主线。

机器账本见 [content-map.json](content-map.json)。其中逐文件记录基线 Git 字节哈希、纯迁移阶段字节哈希、原标签和最终去向；逐框记录原文哈希及最终文件位置；逐图记录原路径、目标路径和字节哈希。所有路径均相对于仓库根目录。拆章行号对应纯迁移中间稿，不是最终源稿行号。

这里的最终源稿哈希和输入链验收属于重构快照 `7e9c50d`。其后自由电子正文的更正与补充另记于 [续修账本](../../FreeElectronQuantumOptics/continuation-audit-20261014.json)，不覆盖迁移阶段的原文保留证据。

## 原八个理论根的归属

| 基线中的自由电子源稿 | 高等物理正常章节根（均在 field-theory 下） |
| --- | --- |
| detailed/ch01.tex | mathematical-tools.tex |
| detailed/ch02.tex | spacetime-and-spinors.tex；classical-gauge-response.tex |
| detailed/ch03.tex | free-quantum-fields.tex；interacting-field-propagation.tex；relativistic-scattering.tex；quantum-radiative-structure.tex |
| detailed/ch04.tex | quantized-electromagnetic-fields.tex；electromagnetic-scattering.tex；quantum-electromagnetic-media.tex |
| detailed/ch05.tex | color-gauge-fields.tex；quark-gluon-scattering.tex；strong-coupling-and-hadrons.tex |
| detailed/ch06.tex | electroweak-fields-and-higgs.tex；flavor-and-anomalies.tex；electroweak-processes.tex |
| detailed/geometric-free-states.tex | geometric-field-states.tex |
| detailed/radial-highspin-states.tex | conformal-high-spin.tex |

旧八个根的正式输入闭包共 211 个源文件；完整 TikZ 图宏文件另计一个，共 212 个迁移记录。纯迁移阶段逆转路径与唯一的标签改名后，212 个文件文本全部相等；随后按物理主题拆成 18 个正常章节。旧文件退出输入链并删除属于迁移，不能解读为其内容被删除。高等物理保留原五部十三章，再增加“相对论量子场与基本相互作用”十六章和“几何背景与共形量子态”两章，最终七部三十一章，966 页。

## 论证、计算与图表的保留

157 个具体物理计算框和 96 个数学结果/独立证明框的原文哈希均在最终输入链中找到，未压缩框内步骤。具体物理计算放在所属实际章节末尾；原 ch02 章末的 48 个数学结果及其 48 个独立证明改放正文数学模块。Euler–Lagrange 与 Noether 的结果/证明放在作用量定义之后；Lorentz、旋量与手征论证归入时空旋量章，规范响应论证归入经典规范响应章。原 ch01 的数学模块全文移入 `sections/mathematical-tool-results.tex`，规范化文本完全相等。

二体阈值相空间计算归入相对论散射，Abel Higgs 矢量质量计算归入量子辐射结构；自由电子的开放单模线宽与协作参数计算归入开放动力学。逐框位置以 JSON 为准。

55 个被引用的图资产复制到高等物理场论图目录，全部字节哈希与基线相等，原图资产也保留。原 13 个完整 TikZ 图宏保存于 `figures/tikz/process-figures.tex`。自由电子只复用电子耦合示意图，中文标注及共享样式的调整不影响高等物理保存的原宏。原 bibliography 字节不变地迁入仓库公共文件 `references/field-and-electron-physics.bib`，两册共同读取。

## 标签、依赖与必要修正

全局基线标签没有遗漏。唯一改名为迁入场论的 `eq:dirac-hamiltonian-em` → `eq:field-dirac-hamiltonian-em`，以保留高等物理原章已有的同名锚点；相应引用同时改写。自由电子的 176 个兼容别名均指向本册真实标签，不依赖另一册编译辅助文件。

自由电子新增最小前置章，给出态与连续谱约定、正能旋量与电流、精确色散和反冲、耦合顶点、时间排序传播以及因果 Maxwell 逆算符；补明上下旋量块和归一化系数。材料响应章补 Maxwell 散射方程与 T 算符及其成立条件，混合辐射章补带适用条件的完整 Klein–Nishina 输入。完整微观场论计算仍在高等物理。

高等物理原 ch24 的横向模态谱表示改为 `G_T`，原近共振分母写法改为精确部分分式恒等式；原偶极辐射应用保留。三处旧显示公式的文字形式因此被完整公式或正确公式替代，不属于无替代删减。章首引入、前后章措辞、范围引用和输入顺序按新章节归属调整，详细变化及阶段说明记录在 JSON 中。

## 核查范围

最终输入链检查未发现缺失输入、未定义引用、重复标签、失效别名、缺图、缺参考文献、环境不配对或章末计算之后仍有正文的问题。上述哈希核对证明迁移内容有去向；最终编译与选页视觉检查验证结构和排版。本次记录不声称重新证明了所有迁入公式，也不将纯迁移阶段的哈希当成润色后最终源稿的哈希。
