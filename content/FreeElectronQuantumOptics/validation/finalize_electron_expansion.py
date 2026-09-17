from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
p = BOOK / 'ch09.tex'
t = p.read_text(encoding='utf-8')
head, tail = t.split(r'\subsection{Bloch--Floquet 纤维}', 1)
head = head.replace(r'\mathbf p_0', r'\mathbf p_{\rm B}')
p.write_text(head + r'\subsection{Bloch--Floquet 纤维}' + tail, encoding='utf-8')

p = BOOK / 'issues.md'
t = p.read_text(encoding='utf-8')
t += '''
## 2026-09-16：第七至第十一章教学扩充

新增八个小节、十二道数值例题、八组局部推导及五幅定量图：波包重叠与偏迹、有限作用窗与黄金律误差、实场到 PINEM 边带的标定、相干光输入下的电子纯度、完整反冲格与 Bragg 两态近似、自由漂移脉冲列、四相位电子相干重建、有限探测窗口与近场复振幅反演。新概念在正文首次使用处给出对象定义、量纲和物理作用，再给一般公式、近似条件和可复算输入。

修正 Feshbach 投影中离开与返回子空间的算符方向；统一时间 Fourier 相位与瞬时能移的正负号；显式区分原始耦合矩阵元与量子交换 Hamiltonian 的相位约定。Bloch 准动量统一为 p_B，入射束中心动量保留 p_0；在位失谐 delta 与相邻交换边失谐 Delta 分开。相对周期密度与物理密度分开，谐波调制幅度与 Michelson 可见度分开，实场峰值与正频振幅的因子二明确保留。修正纵向 PINEM 判据误用横向 Kapitza–Dirac 反冲频率的问题；补足弱量子交换中光子数增强的适用条件。

本轮验证入口为 `python content/FreeElectronQuantumOptics/validation/verify_electron_expansion.py`，结果为同目录 `electron-verification.json`。解析结果分别与波包积分、有限时谱积分、完整电子—光子矩阵指数及偏迹、反冲格矩阵指数及独立微分方程、Bessel 级数、探测卷积积分和测量效应矩阵交叉验证。结构检查沿实际输入链检查标签、引用、文献和环境配对。

本轮构建日志保存在 `validation/electron-build.log`；渲染入口为 `validation/render_electron_expansion.py`，新增内容页面与整书文本边界检查保存至 `validation/render/`。此前条目中根目录 tools 与 tmp 的记录属于历史验证路径；当前交付以本书目录内的验证结果为准。
'''
p.write_text(t, encoding='utf-8')
print('Updated Bloch notation and maintenance record.')
