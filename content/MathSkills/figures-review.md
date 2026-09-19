# MathSkills 配图视觉审查记录

审查对象：`build/MathSkills/main.pdf` 中三张 matplotlib 图（PDF 150 dpi 渲染逐图目检）。

| 图号 | 文件 | PDF 页码 | 主题 |
|------|------|----------|------|
| 图 6.1 | `tikhonov_filter.pdf` | 210 | 形式逆 / Tikhonov / TSVD 滤波函数比较 |
| 图 7.1 | `burgers_characteristics.pdf` | 226 | Burgers 特征线（$u_0(\xi)=-\tanh\xi$） |
| 图 7.2 | `kdv_two_soliton.pdf` | 237 | KdV 二孤子散射（三个时刻截面） |

## 0. 基础设施修复

- 仓库根 `preamble.py` 原本缺失（脚本 `from preamble import ...` 报 `ModuleNotFoundError`）。
- 三个脚本统一 `ROOT = Path(__file__).resolve().parents[4]`，实测该层级解析到 `content/` 而非仓库根，导致即便在根放 `preamble.py` 也无法导入。
- 处理：
  1. 在仓库根新建 `preamble.py`，提供 `figure_style / polish_axes / add_legend / save_pdf_png_pair` 四个函数，风格对齐 `generated/` 历史产物（Latin Modern Roman 衬线、CM mathtext、全框线、外向主刻度、浅灰虚线网格、图内带框 legend）。
  2. 把三个 `*_code.py` 的 `parents[4]` 改为 `parents[5]`，使 `sys.path` 指向仓库根。
- 验证：三个脚本均可独立运行，`generated/` 下 pdf/png 重新生成，与历史产物视觉一致。

## 1. 图 6.1  Tikhonov 滤波函数（`tikhonov_filter_code.py`）

**目检结论：通过。**

- legend 位于右上角，四条目在 $s>0.6$ 区域均已回落到 $q(s)<2$，legend 箱体（$q(s)\in[8.5,11.5]$）完全悬空，不遮挡任何曲线。
- 形式逆 $1/s$ 蓝线在 $s\to0$ 处冲出上边界，属物理本意；TSVD 红色竖线在 $s=\tau=0.18$ 处硬截断，与蓝线断点衔接清楚。
- 四条曲线颜色（蓝/橙/绿/红）与 tab10 一致，线宽统一；横轴 $s\in[0,1]$、纵轴 $q(s)\in[0,12]$ 范围合理。
- 无 annotation 压字；标题、轴标签、刻度字号一致、可读。

**未改动。**

## 2. 图 7.1  Burgers 特征线（`burgers_characteristics_code.py`）

**目检结论：通过。**

- legend（$t_*=1$ 蓝色虚线）位于左上角。特征线全部从中心 $(0,\,t_*)$ 向左右扇形发散，最左侧蓝/橙线在 $t=1.2$ 时已落到 $x\gtrsim-1.1$，legend 箱体右缘约 $x\approx-1.4$，二者不相交；虚线 $t=1.0$ 横贯画面但位于 legend 下方，不遮挡。
- 17 条特征线数量适中：左右两侧平坦区稀疏、中心激波形成区（$x\approx0,\ t\approx1.25$）自然汇聚，恰好直观展示“光滑初值有限时间爆破”，不显拥挤。
- 无 annotation；标题 `Characteristics for $u_0(\xi)=-\tanh\xi$` 居中，轴标签 $x,t$ 字号一致。

**未改动。**

## 3. 图 7.2  KdV 二孤子散射（`kdv_two_soliton_code.py`）

**目检结论：不通过 —— legend 遮挡曲线极值。**

- 当前 legend 位于 `loc='lower left'`，箱体覆盖 $x\in[-17,-11]$、$u\in[-1.62,-1.25]$。
- $t=-3$ 蓝色孤子谷底位于 $x\approx-13.5$、$u\approx-1.62$，谷底及其两侧下降沿正好落在 legend 箱体后方，**极值点被 legend 压住**。这违反“legend 不得遮挡曲线极值”的硬性要求。
- 四角检查：
  - 左下：蓝色孤子谷底（现位置，遮挡）。
  - 右下：绿色 $t=6$ 孤子谷底（$x\approx17$，同样遮挡）。
  - 左上：蓝色孤子左肩（$x\approx-15.5$，$u$ 从 0 跌至 $-0.5$）会擦到 legend 下缘。
  - 右上：绿色孤子右肩（$x\approx14.5$）同理。
- 由于三个孤子谷底分别占据两个底角，两个顶角也被孤子肩部擦边，**没有天然空角**。

**修改方案：**
1. legend 从 `'lower left'` 改为 `'upper left'`；
2. 把左边界从数据默认的 $-18$ 外推到 $-21$（`ax.set_xlim(-21, 20)`），在左上角腾出一段 $x\in[-21,-16]$ 的平坦基线区（三条曲线在 $x<-16$ 均 $u\approx0$），使 legend 箱体完全坐在平坦基线上，不碰任何孤子肩部。

**已应用并复验：** 改后重跑 `kdv_two_soliton_code.py` → 重编译 PDF（525 页，无 `!` 错误，三个 `fig:*` label 均已解析）→ 重新渲染第 237 页 PNG。新 legend 位于左上角 $x\in[-20,-13]$、$u\in[0,-0.35]$，蓝色 $t=-3$ 孤子谷底（$x\approx-13.5,\ u\approx-1.6$）完全露出在 legend 下方，不再被遮挡；蓝色左肩在 $x\approx-15.5$ 处 $u\approx-0.5$，恰在 legend 下缘之下，无重叠。

## 4. 旁注（非本次配图任务范围，仅记录）

- 第 210 页正文出现字面量 `figreffig:tikhonov-filter`，即 `\figref{fig:tikhonov-filter}` 宏未正常展开为蓝色链接。此为 LaTeX 宏 / 交叉引用问题，与三张 matplotlib 图本身无关，且按硬边界不得改动正文与 label，故仅记录、不处理。
- 全文编译无 `!` 错误、无 undefined reference；存在的 underfull hbox 与 rsfs 字号替换为既有警告，与本次改动无关。
