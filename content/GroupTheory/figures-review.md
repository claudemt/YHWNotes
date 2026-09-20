# GroupTheory 配图视觉精修记录

审查日期：2026-09-19（第二轮，逐图视觉闭环）
方法：每张图复制到 `C:\Users\Administrator\AppData\Local\Temp\figfine\` 下的 standalone 文件，`xelatex` 单图编译 → PyMuPDF 渲染 PNG(dpi=300) → Read 亲眼看图量坐标 → 改 → 再渲染确认 → 用 Python 脚本按精确字符串写回源文件。
公共样式来自根 `preamble.tex`（lecturebox / lecturearrow / lecturelabel / axes / mid arrow 等），standalone 测试时复制所需样式并加 `\usepackage{ctex}` 渲染中文。

---

## 逐图记录

### ch01

#### 图1.1 fig:d3-symmetry（ch01.tex，旋转 r 三角形 + 反射 s 三角形）【基准图，重改】
发现问题：
- 左三角三条蓝弧用 `lecturearrow`（箭头在路径终点），三个箭头尖正压在 B1/C1/A1 顶点黑点上，方向看不清（7项之①）。
- `r` 标签在 (0,-0.35)，正好压在 B1→C1 底弧上，且把底弧中点箭头遮住（②）。
- 顶点标签 2、3 用 below left/right=6pt，离底边黑线偏近（②）。
- 右三角两条红双向弧仍用 `lecturearrow`，箭头尖压在顶点黑点上；`s` 标签 (0.18,0) 压在红色虚反射轴上（①②）。
修改：
- 三条蓝弧与两条红弧全部改用 `mid arrow`（`postaction={decorate, markings, mark=at position 0.5}`），箭头落在各边中点，不再压顶点。
- `r` 标签移到三角内部中心空白 (0,0.05)，离三条内弧均 ≥10pt。
- 顶点黑点 2pt→1.6pt；标签 2、3 的 below left/right 由 6pt→13pt，外移约 7pt。
- `s` 标签移到虚轴右侧 (0.34,0.20)，离线≥5pt。
验证：standalone 渲染 PNG 亲看，5 个有向边箭头均在各自边中点，r/s 标签均在空白处，顶点标签离底边清晰。

#### 图1.2 fig:d3-cayley-graph（ch01.tex，D3 Cayley 图）
- 六节点圆上，蓝边右乘 r：e→r→r²→e、s→sr→sr²→s，方向验算正确；红虚边右乘 s：e-s、r-sr²、r²-sr 连接正确。
- 箭头指向大圆圈边框为有向图标准画法，标签 r/s 不压线不压点。
- 结论：无需修改，通过。

#### 图1.3 fig:d3-subgroup-lattice（ch01.tex，D3 子群格）
发现问题：中间宽标签 `⟨r⟩≅C₃`（位于 (0,1.6)）被 D₃→⟨sr⟩、D₃→⟨sr²⟩ 两条陡斜线穿过（②，斜线从字中穿过）。
修改：在所有 draw 之后补一句 `\node[fill=white,inner sep=1.5pt] at (r) {$\cyclic{r}\cong C_3$};`，白底重绘遮住穿线。
验证：渲染亲看，两条斜线止于白底标签边缘，文字干净。

### ch02

#### 图2.1 fig:representation-homomorphism（表示同态框图）
- G→GL(V) 标 ρ、GL(V)→D(g) 标"选定基"，框与标签均无重叠。通过。

#### 图2.2 fig:intertwiner-diagram（2×2 交换图）
- 标准交换图，T、ρ(g)、ρ'(g) 标签清晰。通过。

#### 图2.3 fig:left-regular-action（左正则表示）
- 基→左乘重排箭头，说明文字居中无重叠。通过。

### ch03

#### 图3.1 fig:cube-axes（立方体三类转轴）
发现问题：C₃ 对角线从原点到 (1.75,1.55)，`C₃` 标签原用 midway above，被对角线穿过"3"（②）。
修改：C₃ 箭头只画线，标签独立放在 (1.1,1.45)，位于对角线上方空白、且与中心 C₄ 标签分开。
验证：渲染亲看，C₃ 标签离线、不与 C₄ 重叠。

#### 图3.2 fig:improper-rotation（转动反射 S_n）
发现问题：`reflect` 标签在 (-2.0,-0.1)，正压在 x 横轴线上（②）。
修改：移到 (-2.0,-0.38)，落在 x 轴与 σ_h 虚线之间的空白带。
验证：渲染亲看，reflect 离线。

#### 图3.3 fig:proper-point-group-classification（五种旋转群并排）
发现问题：五个 lecturebox 中心 x=-5.4,-2.7,0,2.7,5.4，间距 2.7cm 小于盒宽，相邻盒边框互相重叠（⑥盒重叠、④文字压邻盒）。
修改：间距拉到 3.6cm，中心改为 -7.2,-3.6,0,3.6,7.2，下方 (n,n) 等标注同步对齐。
验证：渲染亲看，五盒之间留白清晰，标注正对上方盒中心。

#### 图3.4 fig:sigma-hvd（三类镜面）
发现问题：`σ_d` 标签在 (2.25,1.35)，贴在 σ_d 虚线端点上（②）。
修改：移到 (2.55,1.55)，在虚线端点右侧。
验证：渲染亲看，σ_d 离线。

#### 图3.5 fig:schoenflies-family-tree（识别逻辑树）
- start→cyc/dih→各叶子，扇形展开无重叠，箭头方向正确。通过。

#### 图3.6 fig:screw-glide（螺旋轴 + 滑移面，两 minipage）
- 左（螺旋轴）：发现 `{C₆|c/6}` 左花括号贴着弯曲箭头（②）。标签从 (1.55,-1.15) 右移到 (2.05,-1.05)。
- 右（滑移面）：σ 虚线、上下两排点、箭头均无重叠。通过。

#### 图3.7 fig:stereographic-projection（极射赤面投影）
发现问题：P' 点 (0.89,0) 下方标签压在透视椭圆线上（②）。
修改：P' 标签加 `fill=white,inner sep=1pt`，白底遮住椭圆线。
验证：渲染亲看，P' 标签清晰、椭圆线在字后被白底遮断。

### ch04

#### 图4.1 fig:irrep-degeneracy（不可约表示维数示意）
- 三条能级线与基态短线、右侧标注均无重叠。通过。

#### 图4.2 fig:d-orbital-splitting（d 轨道劈裂树）
发现问题：中间列 E_g、T_{2g} 标签用 `node[right]` 放在 (5.1,...)，而右侧分叉箭头从 (5.35,...) 出发，标签子脚本正好压在分叉箭头起点上（②⑥）。
修改：两标签改为 `node[midway,below=2pt]`，放到能级线下方中点，右侧分叉点空出。
验证：渲染亲看，E_g/T_{2g} 在线下，分叉箭头干净出发。

#### 图4.3 fig:c3v-three-sites（C₃ᵥ 三位置）
发现问题：σ_v 虚轴顶端 `node[above]` 与顶点 |1〉标签叠在同一竖线上、后又紧贴 |1〉（②）。
修改：σ_v 标签从轴上移到右上空白 (0.35,2.55)，与 |1〉分开。
验证：渲染亲看，|1〉、σ_v 分开清晰。

#### 图4.4 fig:ir-raman-schematic（IR/Raman 能级）
- IR 单光子箭头、Raman 双光子路径方向正确，标签无重叠。通过。

#### 图4.5 fig:bz-wigner-seitz（Wigner-Seitz 原胞）
- 点阵、灰原胞、虚线边界、"1st BZ" 居中，无重叠。通过。

#### 图4.6 fig:irreducible-bz（不可约 BZ 楔形）
发现问题："irreducible wedge" 文字被 Γ-M 对角线穿过（②）。
修改：标签加 `fill=white,inner sep=1pt` 并移到 (1.7,0.6)，白底遮住对角线。
验证：渲染亲看，对角线在字后被白底遮断。

#### 图4.7 fig:tr-kramers-bands（Kramers 能带）
发现问题："Kramers point" 标签 (0.75,0.8) 贴在两支抛物线下方附近（②）。
修改：下移到 (0.85,0.55)，离线。
验证：渲染亲看，标签离线。

### ch05

#### 图5.1 fig:euler-axis-angle（轴角/Euler 角）
- 三轴、n̂ 轴、β/α 弧线、右侧说明文字均清晰。通过。

#### 图5.2 fig:su2-double-cover（SU(2)→SO(3) 二重覆盖）
- U、-U 各经 π 映到 R_U，箭头方向正确，框与说明文字无重叠。通过。

#### 图5.3 fig:crystal-spin-orbit-branching（晶场+自旋轨道约化）
- SO(3)→O_h→O_h^D 三框横排，箭头标签与下方说明无重叠。通过。

### ch06

#### 图6.1 fig:s4-young-diagrams（S₄ 五个 Young 图）
- 五个分拆形状正确，标签对齐。通过。

#### 图6.2 fig:three-spin-s3（自旋+置换分类）
发现问题：右侧 lecturewidebox（宽 74mm）中心原在 x=10.0，左边缘与 SU(2)/S₃ 两框右边缘几乎相贴，净距不足（⑥）。
修改：宽框中心右移到 x=11.8，箭头变为清晰斜向连线。
验证：渲染亲看，两列框之间留白充足。

### ch08

#### SU(3) 根图（ch08.tex 内联 tikzpicture）
- 正六边形、α₁(1,0)、α₂(-0.5,0.866)、α₁+α₂(0.5,0.866) 位置正确，T₃/T₈ 轴与标签不压根点。通过。

---

## 修复汇总（本轮实际改动）

| 图 | 位置 | 问题（7项编号） | 改动 |
|----|------|------------------|------|
| 1.1 | ch01 | ①箭头压黑点 ②r/s 压线 | 蓝/红弧改 mid arrow；r 移中心；s 移开虚轴；黑点缩小；顶点标签外移 |
| 1.3 | ch01 | ②斜线穿宽标签 | 白底细标签重绘 |
| 3.1 | ch03 | ②C₃ 标签穿线 | 标签移到对角线上方 (1.1,1.45) |
| 3.2 | ch03 | ②reflect 压横轴 | 移到轴与 σ_h 之间 |
| 3.3 | ch03 | ④⑥盒重叠 | 盒距 2.7→3.6cm |
| 3.4 | ch03 | ②σ_d 贴虚线端点 | 右移到 (2.55,1.55) |
| 3.6a | ch03 | ②花括号贴箭头 | 标签右移 |
| 3.7 | ch03 | ②P' 压椭圆 | 白底标签 |
| 4.2 | ch04 | ②⑥中间列标签压分叉 | 标签改 midway below |
| 4.3 | ch04 | ②σ_v 叠顶点标签 | 移到右上空白 |
| 4.6 | ch04 | ②对角线穿文字 | 白底标签 |
| 4.7 | ch04 | ②Kramers 贴曲线 | 标签下移 |
| 6.2 | ch06 | ⑥宽框净距不足 | 宽框右移到 11.8 |

未改动（经 standalone 渲染亲看确认无 7 类问题）：1.2、2.1、2.2、2.3、3.5、3.6b、4.1、4.4、4.5、5.1、5.2、5.3、6.1、ch08 SU(3)。

---

## 2026-09-20 第三轮：轴次/投影标签压线专项（质量标准 A：标签不压任何线、落空白区、彼此分开、离线≥5–8pt）

方法同前：standalone（`\documentclass[tikz,border=12pt]{standalone}` + preamble.tex 196–243 行所需样式 + `\providecommand{\ii}{\mathrm{i}}`）→ `xelatex` → PyMuPDF 渲染 PNG → Read 亲看量坐标 → 改 → 再渲染 → 确认后用 Python 按精确字符串写回。

### 图3.1 fig:cube-axes（立方体纯转动群 O 三类转轴）——必修
- 问题类别：A 压线 / 贴线 / 挤在一起。
- Read 原 PNG 观察：`C4` 用 `midway,right`，竖直线（z 轴）穿过 "C4" 字形并紧贴立方体顶面前边；`C3` 在 (1.1,1.45) 紧贴立方体顶面前边；`C2` 用 `midway,above` 落在立方体正面矩形内部。三个轴次标签挤在立方体顶部，与透视线、z 轴交叉重叠。
- 坐标改动：
  - C4：删去箭头上的 `midway,right` 标签；箭头仍画 `(0,0)--(0,2.0)`，标签独立放到 **(1.0,2.05)**（z 轴右侧、立方体顶面上方空白）。
  - C3：标签 (1.1,1.45) → **(2.35,1.55)**（C3 箭头尖端右侧空白，离开立方体顶面）。
  - C2：删去箭头上的 `midway,above` 标签；箭头仍画 `(0,0)--(-2.1,.85)`，标签独立放到 **(-2.5,1.3)**（箭头尖端左上方空白，离开立方体正面）。
- 渲染确认（改后 Read PNG 亲看）：C4 在 z 轴右侧，与竖直线、立方体顶面前边均有清晰间隙；C3 在箭头尖端右侧空白；C2 在箭头左上方空白；三标签彼此分开，无立方体边/坐标轴/透视线穿过或贴线。干净。

### 图3.7 fig:stereographic-projection（极射赤面投影基本几何）——必修
- 问题类别：A 压线。
- Read 原 PNG 观察：`equator` 在 (2.45,0.25) 压在赤道虚线右端与圆周右缘交点上；`P'` 标签挂在 (0.89,0) 正下方，紧贴赤道虚线并与 S–P 构造线（半径线）挤在一起。
- 坐标改动：
  - equator：(2.45,0.25) → **(-1.2,-0.62)**（圆内左下方空白，离开虚线右端与圆周）。
  - P'：把原来挂在 `\fill (Pp) circle` 上的 `below=1pt` 标签拆成独立节点 **(0.89,-0.62)**（投影椭圆下弧下方空白，离开赤道虚线与 S–P 半径线）。
  - P 标签保留 `above right`（原本即离线）。
- 渲染确认（改后 Read PNG 亲看）：equator 在左下方空白，与赤道虚线、椭圆下弧均有间隙；P' 在椭圆下弧下方，避开虚线与 S–P 半径线；P 在右上空白。干净。

### 举一反三：其余 ch03 几何图 standalone 复看
- 图3.2 fig:improper-rotation（S_n）：σ_h、r、R_{n̂}(θ)r、S_n r、rotate、reflect 均在空白，离线。无需改。
- 图3.4 fig:sigma-hvd（三类镜面）：σ_d 标签 (2.55,1.55) 仍贴 σ_d 虚线右端点（间隙约 4pt），微调 → **(2.75,1.75)**；σ_v、σ_h、principal axis C_n 本就离线。改后 Read PNG 亲看：σ_d 移到虚线端点右上方空白，间隙充足。
- 图3.6a 螺旋轴 `{C₆|c/6}`、图3.6b 滑移面 `{σ|a/2}`：标签均在空白，离线。无需改。

### 本轮改动汇总
| 图 | 位置 | 问题类别 | 坐标改动 |
|----|------|----------|----------|
| 3.1 | ch03 L80–85 | A 标签压线/挤 | C4→(1.0,2.05)；C3→(2.35,1.55)；C2→(-2.5,1.3) |
| 3.7 | ch03 L1372/L1379–1380 | A equator/P' 压线 | equator→(-1.2,-0.62)；P'→独立节点 (0.89,-0.62) |
| 3.4 | ch03 L610 | A σ_d 贴虚线端点 | σ_d (2.55,1.55)→(2.75,1.75) |

---

## 第四轮：意思核对（2026-09-20）

本轮不做视觉精修（视觉前两轮已闭环），逐图核对**数学含义**：箭头方向 vs 正文叙述的映射/演化、元素连接与包含关系、标注对应、节点/层数、实虚/颜色约定。方法：standalone（模板同第三轮，补 `amsmath`、`positioning` 库、`\GL/\vb/\uv/\cyclic/\ket` 等宏占位）→ `xelatex` → PyMuPDF 300dpi PNG → Read 亲看，并对照正文逐句验算。26 张内联 TikZ（另 1 张 `tikzcd` 交换图 2.2）全部渲图核对。

**结论先行：全部图意思正确，无箭头反向、无连接错误、无标注错配，本轮未改动任何源 .tex。** 逐图记录如下。

### ch01

#### 图1.1 fig:d3-symmetry
- 正文：$r$ 把顶点 $1\to2\to3\to1$ 循环置换；$s$ 固定 $1$ 交换 $2\leftrightarrow3$。
- 原图：左三角三条蓝中箭头 $1\to2$、$2\to3$、$3\to1$（CCW）；右三角红虚轴过 $1$，底边红双向弧 $2\leftrightarrow3$。
- 核对：蓝弧方向与 $r$ 的 CCW 置换一致；红轴过顶点 $1$、双向弧交换 $2,3$，与 $s$ 一致。✅ 不改。

#### 图1.2 fig:d3-cayley-graph（重点）
- 正文：蓝有向边右乘 $r$（$e\to r\to r^2\to e$、$s\to sr\to sr^2\to s$）；红虚边右乘 $s$（$e$-$s$、$r$-$sr^2$、$r^2$-$sr$，用 $rs=sr^2$ 而非 $sr$）。
- 原图节点按 $90^\circ,150^\circ,210^\circ,270^\circ,330^\circ,30^\circ$ 排为 $e,r,r^2,sr^2,sr,s$。
- 核对（逐边验乘法表 eq:d3-multiplication-table）：
  - 蓝：$e\to r$（$er=r$）、$r\to r^2$、$r^2\to e$（$r^2r=e$）；$s\to sr$、$sr\to sr^2$、$sr^2\to s$（$sr^2r=s$）。inner/outer 两个三角方向均与"右乘 $r$"一致。✅
  - 红虚：$e$-$s$（$\{e,s\}=\langle s\rangle$）、$r$-$sr^2$（$rs=sr^2$）、$r^2$-$sr$（$r^2s=sr$）。三处连接正是正文强调的 $rs=sr^2$ 关系，无一处画成 $r$-$sr$。✅
- Read PNG 亲看：蓝箭头尖均在目标节点；红虚边三条位置正确。✅ 不改。

#### 图1.3 fig:d3-subgroup-lattice
- 正文：顶 $D_3$ 含一 $C_3$（正规）与三 $C_2$；$\langle r\rangle$ 与三 $C_2$ 无包含关系、交集均 $\{e\}$。
- 原图：$D_3$(上)—$\langle r\rangle\cong C_3$(中)、三 $C_2$(下排)—$\{e\}$(底)。
- 核对：顶 $D_3$ 连四个子群，四子群各连底 $\{e\}$；**$\langle r\rangle$ 与三 $C_2$ 之间无连线**（正确反映"无包含"）。Hasse 方向大群在上小群在下，符合包含约定。✅ 不改。

### ch02

#### 图2.1 fig:representation-homomorphism（重点：表示层次映射）
- 正文：先 $\rho:G\to\mathrm{GL}(V)$，再选定基得矩阵表示 $D(g)$。
- 原图：$G$(抽象群) $\xrightarrow{\rho}$ $\mathrm{GL}(V)$(线性变换群) $\xrightarrow{\text{选定基}}$ $D(g)$(固定基后矩阵群)。
- 核对：映射方向 群→线性变换群→矩阵群，箭头指向与正文叙述一致；旁注 $\rho(gh)=\rho(g)\rho(h),\rho(e)=I_V$。✅ 不改。

#### 图2.2 fig:intertwiner-diagram（tikzcd）
- 正文：交织关系 $T\rho(g)=\rho'(g)T$。
- 原图：$2\times2$ 交换方 $V\xrightarrow{\rho(g)}V$、$V'\xrightarrow{\rho'(g)}V'$，竖边 $T$。
- 核对：右-下路径 $T\circ\rho(g)$ 与下-右路径 $\rho'(g)\circ T$ 闭合，正是 $T\rho(g)=\rho'(g)T$。✅ 不改。

#### 图2.3 fig:left-regular-action
- 正文：固定 $h$，$L(h)e_g=e_{hg}$ 只是左乘重排（置换矩阵）。
- 原图：基 $\{e_g\}$ $\xrightarrow{\text{左乘重排}}$ 固定 $h$ 框。
- 核对：箭头方向与"基→左乘作用后基"一致。✅ 不改。

### ch03

#### 图3.1 fig:cube-axes（重点：三类转轴位置）
- 正文：$C_4$ 过面心、$C_3$ 过顶点、$C_2$ 过相对棱中点。
- 原图：$C_4$ 竖直沿 $z$ 过前面中心；$C_3$ 斜上右指向前右上顶点；$C_2$ 斜上左指向左侧棱区域。
- Read PNG 亲看：$C_4$ 线穿前面正方形中心（面心✅）；$C_3$ 箭头尖落在立方体前右上顶点方向（顶点✅）；$C_2$ 箭头落在左侧棱而非角点/面心（棱中点区域✅，2D 透视下指向侧边）。三类轴位置与正文一一对应。✅ 不改。

#### 图3.2 fig:improper-rotation
- 正文：$S_n$ 先绕主轴转 $2\pi/n$，再关于垂直主轴的 $\sigma_h$ 反射。
- 原图：$\vb r$ 经弧 $R_{\hat n}(\theta)\vb r$（CCW，箭头在左上），再竖直下落到 $S_n\vb r$（穿过 $\sigma_h$ 虚线）。
- 核对：反射验算 $y'=2(-0.7)-1.63=-3.03$，与 $S_n\vb r$ 坐标一致；先转后反顺序正确。✅ 不改。

#### 图3.3 fig:proper-point-group-classification
- 正文：五族解 $(n,n),(2,2,n),(2,3,3),(2,3,4),(2,3,5)$ 对应 $C_n,D_n,T,O,I$。
- 原图：五框横排，下方标注逐一对应。
- 核对：$T=(2,3,3)$、$O=(2,3,4)$、$I=(2,3,5)$ 与轨道方程解一致。✅ 不改。

#### 图3.4 fig:sigma-hvd
- 正文：$\sigma_v$ 与 $\sigma_d$ 均含主轴，$\sigma_d$ 平分相邻横向 $C_2$ 夹角；$\sigma_h$ 垂直主轴。
- 原图：$C_n$ 竖直主轴；$\sigma_h$ 水平平行四边形；$\sigma_v$ 竖直矩形含轴；$\sigma_d$ 对角虚线含轴。
- 核对：三镜面相对主轴的位置关系正确。✅ 不改。

#### 图3.5 fig:schoenflies-family-tree
- 正文：判断顺序 主轴结构→横向 $C_2$→镜面/反演/转动反射。
- 原图：`highest-order axis` 分 `no perpendicular C2`/`perpendicular C2 axes`，再分 $C_n,C_{nv},C_{nh}/S_{2n}$ 与 $D_n,D_{nh}/D_{nd}$。
- 核对：分叉方向与判断流程一致。✅ 不改。

#### 图3.6a fig:screw-glide（螺旋轴）
- 正文：$\{C_6\mid c/6\}$ 转 $60^\circ$ 并轴向平移。
- 原图：六点绕 $z$ 螺旋上升（角度 $60^\circ k$、$y$ 等差），弯箭头表转动。
- 核对：相邻点角度差 $60^\circ$、高度递增，螺旋关系正确。✅ 不改。

#### 图3.6b fig:screw-glide（滑移面）
- 正文：$\{\sigma\mid \vb a/2\}$ 反射加半格平移。
- 原图：$\sigma$ 水平虚线，上下两排点错位半格，箭头由上排反射平移到下排。
- 核对：上下排 $x$ 错位 $0.6\approx$ 半周期，箭头含反射+半移。✅ 不改。

#### 图3.7 fig:stereographic-projection（重点：极射投影）
- 正文：从球极（南极）向赤道面立体投影；北半球点投影到赤道面。
- 原图：$S$(底/南极)—$P$(右上，北半球)—$P'$(赤道椭圆上) 一线连。
- 核对（几何验算）：$S=(0,-2.2)$、$P=(1.4,1.25)$，直线交赤道面 $y=0$ 处 $t=2.2/3.45=0.638$，$x=1.4\cdot0.638=0.89=P'$，**连线确实过南极投影中心**；$P$ 在赤道线上方（北半球）、$P'$ 落在透视赤道椭圆上。✅ 不改。

### ch04

#### 图4.1 fig:irrep-degeneracy
- 正文：irrep 维数 = 对称性强制最小简并。
- 原图：$T$-type $d=3$（3 条短线）、$E$-type $d=2$（2 条）、$A$-type $d=1$（1 条）。
- 核对：右侧 basis 短线数 = 维数。✅ 不改。

#### 图4.2 fig:d-orbital-splitting
- 正文：$l=2$($SO(3)$) 在 $O_h$ 裂为 $E_g\oplus T_{2g}$；在 $D_{4h}$ 再裂为 $1+1+1+2$。
- 原图：$E_g\to A_{1g}+B_{1g}$，$T_{2g}\to B_{2g}+E_g$。
- 核对：终态 $A_{1g}(1)+B_{1g}(1)+B_{2g}(1)+E_g(2)=5$，与 $d$ 轨道数一致；分叉数正确。✅ 不改。

#### 图4.3 fig:c3v-three-sites
- 正文：三等价位 $|1\rangle,|2\rangle,|3\rangle$ 承载 $C_{3v}$，$C_3$ 循环、$\sigma_v$ 过 $|1\rangle$。
- 原图：三角 $|1\rangle$ 顶、$|2\rangle$ 左下、$|3\rangle$ 右下；中心 CCW 圆弧 $C_3$；竖直虚轴过 $|1\rangle$ 与对边中点。
- 核对：CCW 弧对应 $1\to2\to3$；$\sigma_v$ 过顶点 $1$。✅ 不改。

#### 图4.4 fig:ir-raman-schematic
- 正文：IR 单光子 $v=0\to v=1$；Raman 双光子经虚态（$\omega_L$ 上、$\omega_L-\omega_v$ 下）。
- 原图：IR 直箭 $v=0\to v=1$；Raman 折箭 $\omega_L$ 升至虚态再 $\omega_L-\omega_v$ 降至 $v=1$。
- 核对：两过程方向与光子能量标注正确。✅ 不改。

#### 图4.5 fig:bz-wigner-seitz
- 正文：方格倒格的 WS 原胞 = 第一 BZ。
- 原图：格点间距 $1.5$，中心灰方 $[-0.75,0.75]^2$，虚线为中垂线。
- 核对：灰方边长半周期 $0.75$，正是原点 Voronoi 胞。✅ 不改。

#### 图4.6 fig:irreducible-bz
- 正文：$D_4$ 对称下不可约 BZ 楔形为 $\Gamma$-$X$-$M$ 三角。
- 原图：$\Gamma(0,0)$、$X$(右边中点)、$M$(角)，阴影直角三角。
- 核对：$X$ 在边中、$M$ 在角，楔形占 $1/8$ BZ。✅ 不改。

#### 图4.7 fig:tr-kramers-bands
- 正文：保时间反演缺空间反演时一般 $k$ 两支分裂，TRIM 处交成 Kramers 对；$E_+(k)=E_-(-k)$。
- 原图：两支抛物线在 $k=0$ 相切（Kramers point），线性项 $\pm0.42k$ 使其分开。
- 核对：$E_1(k)=1.15+0.28k^2+0.42k$、$E_2(-k)=E_1(k)$，等式成立；$k=0$ 处相切。✅ 不改。

### ch05

#### 图5.1 fig:euler-axis-angle
- 正文：轴角 $\hat n$ 与 $z$ 夹角 $\beta$、方位角 $\alpha$。
- 原图：$x,z,y$ 三轴；$\hat n$ 在 $x$-$z$ 面；$\beta$ 弧在 $z$ 与 $\hat n$ 间；$\alpha$ 椭圆弧在 $x$ 轴附近。
- 核对：$\beta$ 标在 $z$-$\hat n$ 夹角，$\alpha$ 标在方位向。✅ 不改。

#### 图5.2 fig:su2-double-cover
- 正文：$SU(2)$ 二重覆盖 $SO(3)$，$U$ 与 $-U$ 映到同一 $R_U$。
- 原图：$U$、$-U$ 各经 $\pi$ 箭头到同一 $R_U$。
- 核对：双入单出，覆盖关系正确。✅ 不改。

#### 图5.3 fig:crystal-spin-orbit-branching
- 正文：$SO(3)\,d:\ell=2$ $\xrightarrow{\text{晶场降对称}$ $O_h\,E_g\oplus T_{2g}$ $\xrightarrow{\text{乘}\Gamma_{1/2}\text{约化}$ $O_h^D\,\Gamma_8\oplus\Gamma_7\oplus\Gamma_8$。
- 原图：三框横排，箭头与标注逐一对应。
- 核对：约化链方向正确。✅ 不改。

### ch06

#### 图6.1 fig:s4-young-diagrams
- 正文：$4$ 的五个分拆 $[4],[3,1],[2,2],[2,1,1],[1^4]$。
- 原图：五框形状 4 横、3+1、2+2、2+1+1、4 竖。
- 核对：每个 Young 图行/列长度与分拆一致。✅ 不改。

#### 图6.2 fig:three-spin-s3
- 正文：三自旋 $1/2$ 的 $2^3=8$ 维同时受 $SU(2)$（$4\oplus2\oplus2$）与 $S_3$（$4[3]\oplus2[2,1]$）分类，得 $V_{3/2}\otimes[3]\oplus V_{1/2}\otimes[2,1]$。
- 原图：$8$ 维框分两支到 $SU(2)$/$S_3$ 框，再汇合到右侧组合框。
- 核对：$4\cdot1+2\cdot2=8$，维数闭合；箭头分叉/汇合方向正确。✅ 不改。

### ch08

#### SU(3) 根图
- 正文：正六边形，正根 $\alpha_1,\alpha_2,\alpha_1+\alpha_2$。
- 原图：$\alpha_1=(1,0)$ 右顶点、$\alpha_2=(-0.5,0.866)$ 左上顶点、$\alpha_1+\alpha_2=(0.5,0.866)$ 右上顶点，$T_3$ 水平 $T_8$ 竖直。
- 核对：三根位置与标准 $SU(3)$ 根六边形一致。✅ 不改。

### 本轮小结
| 项 | 结果 |
|----|------|
| 渲图核对 | 26 张内联 TikZ + 1 张 tikzcd 全部 standalone 渲 PNG 亲看 |
| 箭头方向 | 全部与正文映射/演化一致（含重点 1.2 Cayley、2.1 层次映射、3.7 投影） |
| 元素/包含连接 | 1.2 右乘边、1.3 子群包含、4.2 劈裂、6.2 维数闭合均正确 |
| 标注对应 | 3.1 三类转轴、3.4 三镜面、4.6 高对称点、SU(3) 根均落在正确对象上 |
| 改动 | **无**（源 .tex 未动；本轮只记录） |

---

## 2026-09-20 统一 matplotlib 样式重建（preamble.figure_style）

- **本轮**：跨书统一 matplotlib 样式重建范围为 AdvancedPhysics / FreeElectronQuantumOptics / MathSkills 三本。
- **GroupTheory 本轮**：本书配图为 TikZ / `preamble.tex` 体系，无 in-scope 的 `.py` 图脚本，故本轮未重跑、未改动任何源文件，仅登记此范围说明。


---

## 2026-09-20 第五轮：A 同类样式统一 + B 图例/标记重叠 逐图视觉闭环（复渲染全部 27 张内联 TikZ）

方法同前：standalone（`\documentclass[tikz,border=12pt]{standalone}` + 复制 preamble.tex 195–249/225–238 全部共享 tikz 样式 + settings.tex 数学宏占位 + `\providecommand{\ii,\ket,\bra}`）→ `xelatex` → PyMuPDF 300dpi PNG → Read 亲眼逐张核对。本轮把 ch01–ch08 全部 27 个 tikzpicture/tikzfig/tikzcd 块重新抽块、重编译、重渲染、亲看。

### A 类（同类样式统一）核查结论
- **Feynman 类**：全书 27 张图中**无任何** fermion/antifermion/photon/fvertex/momentumlabel 用法（Grep 全文无命中），该类基线 N/A，无需统一。
- **流程/板块逻辑图**（ch02 两张、ch03 树图、ch05 两张、ch06 一张，共 6 张）：Grep 确认全部框用 `lecturebox`、全部箭头用 `lecturearrow`、箭头旁注用 `lecturelabel`；**无一处**自写 `draw, rounded corners` / `draw, rectangle` 框或内联 `line width=` 箭头。同层框同宽、圆角 2pt、内边距一致，内部自洽。
  - 备注（不改）：箭头标签用 `lecturelabel`（无白底）而非 `line-label`/`blocklabel`（白底）。逐张亲看确认所有箭头标签均放在箭头**空白侧**（above/below/right），没有任何线穿过字形，故白底不带来可见收益、反而会在干净空白处加白框，本轮保持现状不批量替换。
- **几何/根图/Young 图**：线宽统一 0.75pt；节点黑点大小一致（1.6–2pt）；字体统一 `font=\small`。ch08 SU(3) 根图用 `thick`（≈0.8pt）与基线 0.75pt 差 0.05pt，目视无差别，且属独立几何图，不改。

### B 类（图例/标记逐个查重叠）逐图记录

| 图号/标签 | A 类 | B 类（穿线/挤压/压框边） | 改动 | 渲染确认 |
|-----------|------|--------------------------|------|----------|
| 1.1 fig:d3-symmetry | mid arrow 共用 | 三蓝/两红中箭头在边中点不压顶点黑点；r 在中心空白、s 在虚轴右侧；顶点 1/2/3 标签离线分开 | 无 | f1_1.png 亲看干净 |
| 1.2 fig:d3-cayley-graph | lecturearrow 共用 | r/s 旁注在空白；六节点圆排开、蓝红边不穿字 | 无 | f1_2.png 亲看干净 |
| 1.3 fig:d3-subgroup-lattice | 正交 bus 走线 | D3/⟨s⟩/⟨sr⟩/⟨r⟩≅C3/⟨sr²⟩/​{e} 在上下两条水平 bus 之间空白，竖线止于标签南北缘，无穿字 | 无 | f1_3.png 亲看干净 |
| 2.1 fig:representation-homomorphism | lecturebox+lecturearrow | ρ 在水平箭头上空白、"选定基"在竖箭头右侧空白，不穿线 | 无 | f2_1.png 亲看干净 |
| 2.2 fig:intertwiner-diagram | tikzcd 标准 | ρ(g)/ρ'(g)/T 标签均在边侧空白，交换方闭合 | 无 | f2_2.png 亲看干净 |
| 2.3 fig:left-regular-action | lecturebox+lecturearrow | "左乘重排"在箭头上空白，下方说明文字不压线 | 无 | f2_3.png 亲看干净 |
| 3.1 fig:cube-axes | lecturearrow | C4 在 z 轴右侧空白、C3 在对角箭头尖右侧空白、C2 在左对角尖左上空白；三轴次标签彼此分开不压立方体边 | 无 | f3_1.png 亲看干净 |
| 3.2 fig:improper-rotation | lecturearrow | reflect 在 x 轴与 σ_h 之间空白、rotate 在右侧空白、σ_h 在虚线右端空白；R r / S_n r / r 标签离线 | 无 | f3_2.png 亲看干净 |
| 3.3 fig:proper-point-group-classification | lecturebox 同层同宽 | 五框间距 3.6cm 不重叠；下方 (n,n)…(2,3,5) 逐一正对框中心 | 无 | f3_3.png 亲看干净 |
| 3.4 fig:sigma-hvd | — | σ_d 在对角虚线端点右上方空白、σ_v 在竖矩形右侧空白、σ_h 在水平平行四边形右侧空白；"principal axis Cn"在顶端 | 无 | f3_4.png 亲看干净 |
| 3.5 fig:schoenflies-family-tree | lecturebox+lecturearrow | 树图两叉扇形展开，叶子 Cn/Cnv/Cnh/S2n/Dn/Dnh/Dnd 彼此分开，箭头不穿字 | 无 | f3_5.png 亲看干净 |
| 3.6a fig:screw-glide（螺旋轴） | lecturearrow | {C6\|c/6} 在弯曲箭头右侧空白；六点螺旋绕 z 排开 | 无 | f3_6a.png 亲看干净 |
| 3.6b fig:screw-glide（滑移面） | lecturearrow | {σ\|a/2} 在 σ 虚线上方空白；上下两排点错位半格，箭头不压标签 | 无 | f3_6b.png 亲看干净 |
| 3.7 fig:stereographic-projection | — | equator 在圆内左下空白、P' 在椭圆下弧下方空白、P 在右上空白；S–P 半径线不穿标签 | 无 | f3_7.png 亲看干净 |
| 4.1 fig:irrep-degeneracy | — | T/E/A 三能级线与右侧 3/2/1 基态短划线对齐，标签不压线 | 无 | f4_1.png 亲看干净 |
| 4.2 fig:d-orbital-splitting | lecturearrow | Eg/T2g 在线下空白，右侧分叉箭头从能级右端空白出发，不压标签 | 无 | f4_2.png 亲看干净 |
| 4.3 fig:c3v-three-sites | lecturearrow | \|1〉在顶点正上、σ_v 在其右上空白、C3 在中心弧右侧空白；\|2〉\|3〉在底角外 | 无 | f4_3.png 亲看干净 |
| 4.4 fig:ir-raman-schematic | lecturearrow | IR 直箭、Raman ωL 上/ωL−ωv 下折箭标签均在箭头侧空白 | 无 | f4_4.png 亲看干净 |
| 4.5 fig:bz-wigner-seitz | — | 点阵+虚线中垂线+中央灰方"1st BZ"居中，无穿字 | 无 | f4_5.png 亲看干净 |
| 4.6 fig:irreducible-bz | — | Γ/X/M 高对称点标签在点外空白；"irreducible wedge"白底细遮 Γ–M 对角线，文字干净 | 无 | f4_6.png 亲看干净 |
| 4.7 fig:tr-kramers-bands | — | Kramers point 标签在原点下方空白；E+(k)=E−(−k) 在两抛物臂之间空白 | 无 | f4_7.png 亲看干净 |
| 5.1 fig:euler-axis-angle | axes/mid arrow | β 在 z–n̂ 弧间空白、α 在 x 轴附近弧下空白、n̂ 在箭头尖上；右侧说明块与图分开 | 无 | f5_1.png 亲看干净 |
| 5.2 fig:su2-double-cover | lecturebox+lecturearrow | 双 π 入单出，π 标签分别在上/下箭身空白；下方说明文字不压线 | 无 | f5_2.png 亲看干净 |
| 5.3 fig:crystal-spin-orbit-branching | lecturebox+lecturearrow | 三框横排，"晶场降对称"/"乘 Γ1/2 并约化"在箭头上方空白；下方说明不压线 | 无 | f5_3.png 亲看干净 |
| 6.1 fig:s4-young-diagrams | — | 五个分拆 [4][3,1][2,2][2,1,1][1⁴] 形状正确、下方标签对齐分开 | 无 | f6_1.png 亲看干净 |
| 6.2 fig:three-spin-s3 | lecturebox+lecturearrow | 左 8 维框分两支到 SU(2)/S3 框再汇到右侧宽框；右框与左列留白充足，箭头斜向连线干净 | 无 | f6_2.png 亲看干净 |
| ch08 SU(3) 根图 | thick≈0.8pt（不改） | α1 在右顶点右下空白、α2 在左上顶点左上空白、α1+α2 在右上顶点右上空白；T3/T8 轴标签不压根点 | 无 | f8_1.png 亲看干净 |

### 本轮小结
| 项 | 结果 |
|----|------|
| 渲图数 | **27 张**内联 TikZ 全部 standalone 重编译 → 300dpi PNG → Read 亲看（ch01×3, ch02×3, ch03×8, ch04×7, ch05×3, ch06×2, ch08×1；ch07/backmatter/frontmatter 无 tikz 块） |
| A 类改动 | **0**（板块图已全部共用 lecturebox/lecturearrow/lecturelabel；本书无 Feynman 图；无自写框样式） |
| B 类改动 | **0**（前四轮修复在新渲染中全部成立：无穿字、无挤压、无压框边/节点） |
| 源 .tex 改动 | **无**（本轮只复渲染核对并记录） |
| 未改动图清单 | 全部 27 张：1.1 1.2 1.3 2.1 2.2 2.3 3.1 3.2 3.3 3.4 3.5 3.6a 3.6b 3.7 4.1 4.2 4.3 4.4 4.5 4.6 4.7 5.1 5.2 5.3 6.1 6.2 ch08 根图 |


---

## 2026-09-20 第六轮：「挪标签不遮线」新原则专项（ch01×3 + ch08×1，4 个内联 tikzpicture）

原则：尽量靠挪元素位置防重叠，而非用 `fill=white` 白底遮线。该留 lecturebox/blockbox/节点圆本身的白底框；不批量删 `fill=white`。
方法：逐块抽出到 agent workspace `figreview/` 下 standalone（`\documentclass[tikz,border=12pt]{standalone}` + preamble.tex 196–238 用到的 mid arrow/lecturearrow + `\providecommand{\ii}{\mathrm{i}}`、`\cyclic` 占位）→ `xelatex` → PyMuPDF 300/600dpi PNG → Read 亲看。

### 图1.1 fig:d3-symmetry（ch01.tex L242–269）
- 用法：mid arrow（箭头落边中点）；r 标签在左三角中心 (0,0.05)；s 标签在右三角虚轴右侧 (0.34,0.20)；顶点 1/2/3 用 above/below left/right=7–13pt。
- Grep + 渲染亲看：全图无 `line-label`/`lab`/`fill=white` 文字标签；r/s 与顶点标签均在空白处，无任何坐标轴/边线/箭头穿字。
- 结论：**无需改动**。（前几轮已把 r 从底弧移到中心、s 从虚轴移到右侧，本就符合新原则。）

### 图1.2 fig:d3-cayley-graph（ch01.tex L345–360）
- 用法：六节点 `circle,draw,fill=white`（节点圆白底，属"该留"的节点框背景）；边标签 r 蓝色 (-1.7,0.9)、s 红色 (3.05,0) 均为裸 `\node`（无 fill）。
- 渲染亲看：边 r 在内三角蓝边与 n1–n3 红虚边之间的空白带；s 在右节点圆右侧空白；边均止于节点圆边框，无穿字。
- 结论：**无需改动**。节点圆 `fill=white` 保留（节点框背景，非遮线补丁）。

### 图1.3 fig:d3-subgroup-lattice（ch01.tex L451–464）——重点排查①
- 现状：正交总线扇形走线（top→(0,2.3) 横 bus→`-|` 下引四孩子；孩子 `|-` 收束到 bot.north）。六个节点全为裸 `\node`（无 fill）。
- Grep + 600dpi 渲染亲看：**已无**第二轮"白底重绘遮穿线"的 `\node[fill=white]` 补丁（该补丁在重写为正交 bus 走线时随陡斜线一并移除）；D3/⟨s⟩/⟨sr⟩/⟨r⟩≅C3/⟨sr²⟩/{e} 全部落在上下两条水平 bus 之间的空白带，竖线止于各标签 .north/.south 缘，无穿字、无白底遮线。
- 结论：**无需改动**。当前正交走线本身就是"挪位置防重叠"的正解，不依赖白底。

### 图ch08 SU(3) 根图（ch08.tex L410–419）——重点排查②
- 用法：`scale=0.65`；T3 横轴 `node[right]`、T8 纵轴 `node[above]`；α1 在 (1,0) `below right`、α2 在 (-0.5,0.866) `above left`、α1+α2 在 (0.5,0.866) `above right`，全为裸 node（无 fill）。
- 600dpi 渲染亲看：α1 在 T3 轴下方空白、α2 在左上顶点左上空白、α1+α2 在右上顶点右上空白；T3/T8 轴标签在箭头尖外；无任何根线/坐标轴穿字，无白底遮线。
- 结论：**无需改动**。

### 本轮小结
| 图 | 位置 | 白底遮线? | 改动 | 渲染确认 |
|----|------|-----------|------|----------|
| 1.1 d3-symmetry | ch01 L242–269 | 无 | 无 | 300dpi PNG 亲看，r/s/顶点标签均在空白 |
| 1.2 d3-cayley | ch01 L345–360 | 无（节点圆 fill=white 属该留） | 无 | 300dpi PNG 亲看，边标签空白、边止圆框 |
| 1.3 子群格 | ch01 L451–464 | 无（旧白底补丁已随正交走线重写移除） | 无 | 600dpi PNG 亲看，竖线止标签南北缘、无穿字 |
| ch08 SU(3) 根图 | ch08 L410–419 | 无 | 无 | 600dpi PNG 亲看，α1/α2/α1+α2/T3/T8 均在空白 |

- 源 .tex 改动：**0**（四张图本就符合"挪标签不遮线"新原则；唯一 `fill=white` 是 Cayley 节点圆，按原则保留）。
- 临时 standalone/编译产物：agent workspace `figreview/`（fig1–fig4.tex/.pdf/.png，含 fig3_hi/fig4_hi 600dpi 放大）。

---

## 2026-09-20 第七轮：5 项硬标准专项（压线/重叠/贴线/穿线/不规整；ch01×3 + ch08×1）

判定标准（任一命中即改）：①文字压任何线（含擦边）；②元素重叠/节点叠/箭头交叉/标签叠/框叠；③标签离线 <3pt；④线穿标签；⑤布局不规整（不对齐、不横平竖直、画歪、过挤）。方法：每图抽到 agent workspace `figreview/` 下 standalone（`\documentclass[tikz,border=12pt]{standalone}` + preamble.tex 196–219、225–238 两个 `\tikzset` 原样 + `\providecommand{\ii}`、`\cyclic` 占位）→ `pdflatex` → PyMuPDF 300dpi PNG → Read 亲看（必要时 4–6× 局部放大）→ 改 → 再渲染确认。

### ch01.tex:242 正三角形 D3 生成元图（r 旋转 / s 反射）
- 检查结果：通过。顶点 1/2/3 标签离线；左三角蓝 `r` 与三条内弯蓝弧均有可见间隙；右三角红 `s` 与红虚反射轴、上方红弧、右边线均有间隙；无节点叠、无箭头交叉。已 4× 左右局部放大复核。
- 改动：无需改动。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，5 项标准均干净。

### ch01.tex:345 D3 Cayley 图
- 检查结果：发现问题。原 6 节点同圆周（半径 2.8）画法致蓝 r 弧边与红虚 s 边真实交叉两处（左蓝弧跨 r–sr² 红虚对角、右蓝弧跨 r²–sr 红虚水平），命中②箭头交叉；且与 caption「内三角为 ⟨r⟩、外三角为三个反射」的双三角意图不符。
- 改动：重排为同心双三角形——内三角 {e,r,r²}（半径 1.7，CCW 三箭头），外三角 {s,sr,sr²}（半径 3.3，CW 三箭头），s 边改三条径向虚线（e—s、r—sr²、r²—sr），消除全部交叉；蓝 `r` 标签移到 (2.15,0.55) 外侧空白，红 `s` 标签移到 (0.55,2.45)（竖直径向虚线右侧）。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，无交叉、无压线、节点不重叠、双三角对齐，5 项标准均干净。

### ch01.tex:451 D3 子群格
- 检查结果：通过。顶 D3、底 {e} 居中；中间四子群标签等距横排（x=-4,-1.33,1.33,4）；正交 L 形横平竖直；竖线止于各文本节点南北锚点（标准节点连线，未穿入字形）；标签横向间距充足。已 5× 中行局部放大复核。
- 改动：无需改动。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，5 项标准均干净。

### ch08.tex:410 SU(3) 根六边形（scale=0.65）
- 检查结果：发现问题。α₁ 黑球在 (1,0) 落在 T₃ 横轴上，原 `node[below right]{$\alpha_1$}` 使 α₁ 标签与 T₃ 轴箭头头部相擦（③贴线）。
- 改动：T₃ 横轴右端 1.6→2.0 把箭头让开；α₁ 黑球不再挂标签，改独立节点 `\node at (1.28,-0.34) {$\alpha_1$};`，落到箭头右下方并避开六边形右下斜边；α₂、α₁+α₂ 不动。
- 渲染确认：standalone 300dpi PNG 已 Read 复核，α₁ 与 T₃ 箭头/横轴/六边形边分离，三根标签与坐标轴均离线，5 项标准均干净。

### 本轮小结
| 图 | 位置 | 命中项 | 改动 |
|----|------|--------|------|
| D3 生成元 | ch01 L242 | 无 | 无 |
| D3 Cayley | ch01 L345 | ②箭头交叉 | 同圆周→同心双三角+径向 s 边；边标签外移 |
| D3 子群格 | ch01 L451 | 无 | 无 |
| SU(3) 根图 | ch08 L410 | ③α₁ 贴 T₃ 箭头 | 横轴延到 2.0；α₁ 独立节点移到 (1.28,-0.34) |
