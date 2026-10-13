# 自由电子长章的内容迁移记录

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
