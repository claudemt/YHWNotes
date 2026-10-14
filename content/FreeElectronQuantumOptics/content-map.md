# 自由电子量子光学内容迁移记录

## 2026-10-14：重构之后的计算链续修

以重构提交 `7e9c50d` 为基线，章节路线仍为下表的三部十七章，续修成品为 389 页。此次继续深化有限时间、外场与量子交换、反冲传播、开放动力学和测量反演，旧标签全部保留；改写错误论断时登记正确替代与复算依据。逐文件基线/当前哈希、新增标签、更正范围与最终验收见 [continuation-audit-20261014.json](continuation-audit-20261014.json)。下文迁移阶段的“最终源稿”和 379 页均指 `7e9c50d` 的重构快照，不是续修后的版本。

## 2026-10-13 至 2026-10-14：聚焦电子传播、测量与成像

本轮先将已有四书更改提交为 `8efe635`，并核实 GitHub 主分支 `1beb2ee`。重构以该提交为保留基线。完整 QFT、QED、QCD、标准模型及几何共形量子态理论迁入《高等物理》的十八个正常章节；本册保留独立阅读所需的最小电子前置及连续电子与环境理论，最终三部十七章、379 页。完整逐文件、逐框、逐图哈希及原标签去向见 [高等物理迁移账本](../AdvancedPhysics/field-theory/content-map.json)，说明见 [内容分工记录](../AdvancedPhysics/field-theory/content-map.md)。

### 当前十七章阅读顺序

| 部分 | 章节 | 正文根文件 |
| --- | --- | --- |
| 入射电子与量子交换 | 1．入射电子、量子态与因果响应 | electron-foundations.tex |
| 入射电子与量子交换 | 2．连续电子、辅助系统与模式耦合 | electron-environment.tex |
| 入射电子与量子交换 | 3．自由电子传播与有限时间跃迁 | electron-finite-time.tex |
| 入射电子与量子交换 | 4．外场散射与有限脉冲 | external-field-scattering.tex |
| 入射电子与量子交换 | 5．电子与光子的量子交换 | quantum-electron-photon-exchange.tex |
| 反冲、束流与波包传播 | 6．单模选择与电子反冲通道 | electron-recoil-channels.tex |
| 反冲、束流与波包传播 | 7．周期势与电子传播 | periodic-electron-propagation.tex |
| 反冲、束流与波包传播 | 8．有限反冲与 Bragg 通道 | recoil-bragg-channels.tex |
| 反冲、束流与波包传播 | 9．电子碰撞、束流统计与费米关联 | electron-collision-dynamics.tex |
| 反冲、束流与波包传播 | 10．电子波包传播与时间结构 | electron-wavepacket-propagation.tex |
| 反冲、束流与波包传播 | 11．电子约化动力学与环境记忆 | electron-open-dynamics.tex |
| 量子测量与辐射成像 | 12．电子量子测量与可辨识性 | electron-quantum-measurement.tex |
| 量子测量与辐射成像 | 13．条件制备、计数与统计反演 | conditional-electron-inference.tex |
| 量子测量与辐射成像 | 14．跃迁电流与材料的因果响应 | electron-current-response.tex |
| 量子测量与辐射成像 | 15．材料响应与辐射运动学 | material-radiation-response.tex |
| 量子测量与辐射成像 | 16．混合模式与辐射通道 | hybrid-radiation-channels.tex |
| 量子测量与辐射成像 | 17．电子成像、收集与参数反演 | electron-imaging-inversion.tex |

### 原长章的拆分

| 基线位置 | 当前去向 |
| --- | --- |
| detailed/ch08.tex | external-field-scattering.tex；quantum-electron-photon-exchange.tex |
| detailed/ch09.tex | periodic-electron-propagation.tex；recoil-bragg-channels.tex |
| detailed/ch10.tex | electron-wavepacket-propagation.tex；electron-open-dynamics.tex；electron-quantum-measurement.tex；conditional-electron-inference.tex |
| detailed/ch11.tex | material-radiation-response.tex；hybrid-radiation-channels.tex；electron-imaging-inversion.tex |

原 ch07 的五个语义章节保留，材料电流响应调整到辐射成像部分；该章上一轮的详细拆分见下方历史记录。各实际章节末尾放置对应具体物理计算；开放单模线宽与协作参数归入开放动力学章。旧根删除属于移迁，原独有正文、例题和计算均有对应去向。

最小前置章新增量子态、旋量电流、色散反冲、传播与 Maxwell 因果响应，使本册不必以前六章的完整基本相互作用课程开篇。材料响应补本地 Maxwell T 算符与条件，混合辐射补完整 KN 微观输入；一般场论背景通过明确书名和主题连接高等物理。176 个兼容别名均落到本册真实标签，跨章范围引用按实际主题修复。耦合图复用原宏后改用中文节点与共享 TikZ 样式，原完整图宏仍保存在高等物理。

两册拆章审计合计保留 157 个物理计算框和 96 个数学结果/独立证明框原文；55 个移迁图资产字节不变。原公共参考文献字节不变地移至 `references/field-and-electron-physics.bib`。迁入场论的唯一 Dirac 标签改名、原高等物理横向 Green 函数修正及精确部分分式修正均在共同账本明示。最终源稿输入、引用、别名、图片、参考文献和章末位置检查通过；保留审计和选页排版检查不等于本轮逐条重证整书公式。

## 历史记录：2026-10-12 长章拆分

2026-10-12 续修以 GitHub 主分支 `1beb2ee` 为基线，保留工作区已有深化修改。下列原行号对应拆章前的当前详细稿，不是主分支的行号；原 `detailed/ch07.tex` 的 SHA256 为 `47e0ae0e532878f5eb2346ca9df83262d7fb687f1cb79fd23f86fff2e9b19819`。源码只保留新的语义结构，本文件记录内容去向。

| 原位置 | 新正文 | 中心问题 |
| --- | --- | --- |
| detailed/ch07.tex，1–1314 行 | electron-environment.tex | 连续电子怎样与辅助系统和环境模式耦合 |
| detailed/ch07.tex，1315–2562 行 | electron-finite-time.tex | 自由传播及有限作用时间怎样决定跃迁幅 |
| detailed/ch07.tex，2563–3701 行 | electron-current-response.tex | 跃迁电流怎样激发有因果响应的材料 |
| detailed/ch07.tex，3702–4379 行 | electron-recoil-channels.tex | 单模选择和反冲怎样改变通道结构 |
| detailed/ch07.tex，4380–5189 行 | electron-collision-dynamics.tex | 联合碰撞怎样产生靶信道及束流关联 |

原章与原章末计算的 127 个标签全部保留。`chap:general-interaction` 保留在第一章；有限时间、材料响应、反冲通道、碰撞动力学各有新的章标签。兼容别名、全书概览、依赖路径和声子跃迁的引用已按实际内容调整。旧两个文件在全部内容迁入后退出正式输入链。

| 原章末计算主题 | 新位置 |
| --- | --- |
| 模态谱、完备性及场归一化 | electron-environment.tex，横向 Maxwell 算符的命题与独立证明 |
| 盒态与连续态的模式耦合归一化 | chapter-end/electron-environment-calculations.tex |
| 一量子发射概率、两次发射的时间排序、Lorentz 线形的有限时间积分 | chapter-end/electron-finite-time-calculations.tex |
| 反冲与 Cherenkov 条件、偶极衰变、吸收储库与涨落关系、环境激发率、诱导场做功 | chapter-end/electron-current-response-calculations.tex |
| 单模发射与吸收的有限时间谱核 | chapter-end/electron-recoil-channels-calculations.tex |

一般模态论证移入正文时，修正全空间单位算符与横向投影的混同，并从闭二次型确定自伴实现；分部积分仅用于验证对称性。其余十段具体物理计算保留必要细节，分别置于所属实际章节末尾。

碰撞章中的错误论证直接由正确结果替代：小波包内积不足以控制交换项，改为实际交叉电流或核矩阵元条件，并给出正交平面波的完整反例；一体熵的纯态关联解释限定于归一化两费米子纯态，补同一一体密度矩阵的纯态与混态反例。转移核余项补量纲与窗口范数，Magnus 余项补充分条件及常数。新增随机到达的精确生成元、周期信道收敛证明、同一二能级靶的条件读出与稳态计算，以及弱碰撞传播误差界，均放在所用一般结果之后。

此表覆盖本次长章迁移，不代表更早历史稿与整书所有内容的保留审计已经完成。
