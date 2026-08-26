# 最近两次提交变更要点

本文按 `git log -2` 总结最近两个 commit，供逐条核实。这里只总结提交历史本身，不把当前工作区未提交改动额外计入。

---

## 1. `81ded3c` - `fix: physics issues`

提交时间：2026-08-05 08:41:08 +0800

总体范围：
- 修改正文：`radiation.tex`、`scattering.tex`、`rigid_body.tex`、`matrix_optics.tex`、`bose_fermi_gas.tex`、`ising_model.tex`、`preamble.tex`
- 新增编译产物：`build_verify/main.aux`、`main.log`、`main.pdf`、`main.toc`
- 规模：11 个文件，约 5398 行新增、1012 行删除；其中大量新增来自 `build_verify/` 编译输出。

### 编译与 LaTeX 环境

- `preamble.tex`
  - 在重定义 `equation*` 环境后，补回
    `\renewcommand{\[}{\orig@equationstar}` 与
    `\renewcommand{\]}{\orig@endequationstar}`。
  - 目的：避免 `\[...\]` 被 `equation*` 的 `environ` 包装破坏，修复整本编译报错。

### 电动力学

- `chapters/Electrodynamics/Radiation/radiation.tex`
  - 将多处含多行对齐的 `equation*` 改为 `align*`，主要是 LaTeX 结构修复。
  - 在 VSH 辐射远场处补充 Hankel 函数远场渐近：
    \(h_l^{(1)}(kr)\sim(-i)^{l+1}e^{ikr}/(kr)\)。
  - 显式写出远区横向场：
    \(\vb E_{\rm rad}\)、\(\vb H_{\rm rad}\) 的 \((-i)^{l+1}\) 相位。
  - 修改微分辐射功率角分布，在模平方求和中加入每个多极的 \((-i)^{l+1}\) 相位。总功率公式不变。
  - 该修正影响不同 \(l\) 多极之间的角向干涉项。

- `chapters/Electrodynamics/Scattering/scattering.tex`
  - 散射远场微分功率中，同样补入每个球多极的 \((-i)^{l+1}\) 相位。
  - 总散射功率 \(\sum_{lm}(|a_{lm}|^2+|b_{lm}|^2)\) 不变。

### 力学

- `chapters/Mechanics/RigidBody/rigid_body.tex`
  - 定点转动无磁场例子中，将
    `\omega_p^2=\sqrt{...}` 改为 `\omega_p=\sqrt{...}`。
  - 依据：原式左右量纲不一致，根号内已经是频率平方量。

### 矩阵光学

- `chapters/Optics/MatrixOptics/matrix_optics.tex`
  - 大幅重写矩阵光学正文结构，新增或明确：
    - 几何角状态 \((y,\alpha)\) 与约化角状态 \((y,u=n\alpha)\) 的关系；
    - 跨介质系统中 \(\det M=n_1/n_2\)，约化角矩阵中 \(\det\widetilde M=1\)；
    - 球面折射矩阵、球面镜矩阵、薄透镜矩阵的约定；
    - 复合系统的主面、节点、焦点、无焦条件；
    - Gaussian beam 的 \(q\) 参数 ABCD 变换；
    - 光腔稳定条件和两透镜 relay 示例。
  - 核实时重点注意：该提交属于大幅正文重写，需检查是否有过度叙述或与原章节风格不一致处。

### 统计物理

- `chapters/Statistics/BoseFermiGas/bose_fermi_gas.tex`
  - 硬球赝势部分：
    - 明确 \(a\) 是硬球半径，并在最低阶 \(s\) 波近似中充当散射长度；
    - 说明零程近似条件 \(ka\ll1\)、多体热力学条件 \(a/\lambda\ll1\)。
  - 部分波投影算符：
    - 将投影积分中的 \(Y_{lm}\) 改为 \(Y_{lm}^{*}\)，适配复球谐函数正交归一。
  - 接触相互作用哈密顿量：
    - 将有序对求和从 \(\sum_{i,j}\) 改为 \(\sum_{i\ne j}\)，排除自相互作用。
  - 大幅新增理想玻色/费米气体基准、一般态密度 \(\Sigma(\varepsilon)=BV\varepsilon^s\)、热力学闭式公式、BEC 与费米低温展开、占据数统计、自旋简并度拆分等内容。
  - 修正或说明强简并展开余项：按 Sommerfeld 型偶次幂 \((\ln z)^{-2}\) 组织，余项写入括号内。
  - 核实时重点注意：该提交既有明确公式修正，也包含大段内容扩写。

- `chapters/Statistics/IsingModel/ising_model.tex`
  - 将章节从原先 “伊辛模型的 Bethe 解” 扩展为 “Bethe 与 Bragg--Williams 描述”。
  - 重新组织并扩写：
    - 模型、假设与记号；
    - 树图概率分解；
    - Bethe 熵；
    - Bethe 自由能与自洽方程；
    - 腔场变量；
    - 临界性、响应函数与 Landau 展开；
    - \(q=2\) 一维链严格基准；
    - Bragg--Williams 近似。
  - \(q=2\) 一维链相关闭式中出现如下重点公式：
    - 磁化强度 \(m=\sinh\widetilde h/\sqrt{e^{-4\gamma}+\sinh^2\widetilde h}\)；
    - 磁化率与 \(p_\pm\) 分母使用同一平方根结构；
    - 强调 \(T_c=0\)，不存在有限温度自发磁化。
  - 核实时重点注意：该提交为章节级重写，建议逐式检查 Bethe 自由能、热容、临界展开和 Bragg--Williams 温标是否前后一致。

### 非正文/产物

- `build_verify/`
  - 提交中新增了 `main.pdf`、`main.log`、`main.aux`、`main.toc`。
  - 这些是编译验证产物，不属于正文源文件。若希望仓库保持干净，可考虑后续从版本历史或下一次提交中移除。

---

## 2. `be5c15a` - `fix: physics issues`

提交时间：2026-08-04 21:25:29 +0800

总体范围：
- 新增审核记录与方案：已整理为 `docs/change.md` 与 `docs/refactory.md`
- 修改主入口与说明：`main.tex`、`README.md`
- 修改大量章节源码与配套图片：力学、电动力学、数学工具、统计/光学章节
- 新增 `script_rewrite/` 多个拆分/合并稿件文件
- 规模：64 个文件，约 14896 行新增、196 行删除；新增行主要来自 `script_rewrite/`、`supplement.md`、`issues.md`

### 审核文档与重构方案

- `docs/change.md`（合并原 `issues.md`）
  - 新增全库物理/数学审核记录。
  - 内容包括：
    - 力学章节已修改 30 处；
    - 电动力学核心章节已修改 11 处；
    - 电学其余章节、热学光学、数学工具章节的已修正项与存疑项；
    - 二次核实结论；
    - 叙述与体系问题建议。
  - 这是核查本提交最重要的索引文件。

- `docs/refactory.md`（合并原 `supplement.md` 与 `LECTURE_STYLE.md`）
  - 新增一套较完整的后续补充与系统重构方案。
  - 内容偏计划性/体系性，并非全部已经落入正文。

- 讲义风格规范与重构方法论已并入 `docs/refactory.md`。

- `script_rewrite/`
  - 新增 `original_script.tex`、`merged.tex`、`part1.tex` 至 `part5.tex`。
  - 这些看起来是拆分/重写过程产物，需判断是否应纳入正式仓库。

### 力学章节

- `inverse_square_motion.tex`
  - 修正相对论反平方运动中 \(t(r)\) 积分第一项缺少的 \(E/c\) 因子。
  - 修正吸引/排斥散射角 \(\beta_0^2\) 展开系数。
  - 修正 GR 修正势与径向扰动力符号。
  - 修正椭球四极矩修正势缺少质量因子 \(m\)。
  - 修正双曲线附加偏转角中 \((1-e^2)^{5/2}\) 在 \(e>1\) 区域导致虚数的问题，改为 \((e^2-1)^{5/2}\)。
  - 新增或更新相关轨道示意图。

- `lorentz_transformation.tex`
  - 修正四维加速度空间分量。
  - 修正加速度变换公式。
  - 修正四维加速度不变量。
  - 修正垂直 boost 的 Wigner 转角公式为 \(\tan(\theta/2)\)。
  - 修正电子自旋-轨道进动符号。

- `nonlinear_oscillation.tex`
  - 修正多尺度法中阻尼项 \(\zeta\) 与 \(\epsilon\) 的记账问题。
  - 修正驱动项中 \(\sigma\) 符号。
  - 修正稳态响应式中缺失的 \(1/\epsilon\) 因子。
  - 修正亚谐波响应中若干 \(\zeta^2/\epsilon^2\) 系数问题。
  - 更新 Duffing 相关相图/响应图。

- `rigid_body.tex`
  - 修正自由刚体椭圆函数解中的若干符号、分母与模变换错误。
  - 修正定点转动 \(\theta\) 运动方程符号。
  - 修正心形刚体 \(I_3\) 量纲为 \(R^5\)。
  - 二次核实后将心形刚体参数改为 \(\alpha=7/10\)，并同步更新数值。
  - 改写中间轴不稳定分界轨道的表述。

### 电动力学章节

- `radiation.tex`
  - 修正若干 VSH/辐射源方程中的源项或类型错误。
  - 修正角动量辐射功率系数量纲。
  - 修正圆周运动频域电场缺少 \(\beta\) 因子。
  - 修正简谐运动频域电场相位。
  - 修正二体辐射中椭圆轨道演化闭式的 \(e_i^2\) 分母与时间组合。
  - 将一般四极矩定义改为 STF 形式，使四极功率 \(1/(720\pi\varepsilon_0c^5)\) 与实例自洽。
  - 更新多张辐射图。

- `scattering.tex`
  - 修正表面阻抗球长波近似系数。
  - 修正长波散射场中 \(\alpha,\beta\) 配对、缺 \(1/r\) 等问题。
  - 修正 \(\kappa_e,\kappa_m\) 与 \(\alpha,\beta\) 的对应。
  - 修正相移分式中的 \(\mu_r/\varepsilon_r\) 笔误。
  - 二次核实后修正远场微分功率交叉项符号、无损高频介质球相位项，以及圆柱散射实场共轭条件。

- `plasma.tex`
  - 修正垂直传播横向耦合关系：两个横向因子之积等于耦合项平方。
  - 保留普通波关系。

- `electrostatics.tex`
  - 有少量公式/叙述修正，并更新磁场扩散相关图片。

- `thin_film.tex`
  - 少量介质膜/弹性膜叙述或公式修正。
  - 需重点核对矩阵 \(P,Q\) 与能流守恒相关表述。

- `waveguide.tex`
  - 少量波导/谐振腔公式或表述修正。
  - 更新群速度、角频率、特征位移关系图。

### 数学工具章节

- `green_function.tex`
  - 修正 Legendre 级数恒等式闭式。
  - 增补/改写若干 Green 函数推导内容。

- `infinite_integrals.tex`
  - 大幅增补或调整振荡积分/级数相关推导内容。

- `ellipsoidal_coordinates.tex`
  - 修正椭圆积分解析延拓中 \(k^2>1\) 分支的前导系数和 arcsin 参数。
  - 修正坐标恒等式缺项。

- `mathieu_functions.tex`
  - 修正 \(se_{2n+2}\) 级数展开指数。
  - 修正特征值 \(q=0\) 极限。
  - 修正标签错误。

- `supplementary_formulas.tex`
  - 修正玻色/费米积分第二种形式的 Gamma 因子。
  - 修正 Helmholtz 方程符号与 Fourier 表示一致性。
  - 修正平面周期运动积分中 Bessel 恒等式的系数/相位。
  - 修正 \(\varphi\) 积分恒等式的 \(\pi\) 因子。
  - 修正离散余弦和恒等式的正负号。
  - 定义 \(f_m(U)\)、\(g_m(W)\) 以消除前述存疑。

- `vector_spherical_harmonics.tex`
  - 修正 \(Y_{lm}\) 超几何表示缺少 Condon-Shortley 相位。
  - 修正球基矢到直角基矢转换矩阵前两行角因子互换问题。
  - 修正 \(\vb X_{lm}\) 分量公式中的 \(i\) 因子和整体符号。

### 统计与光学章节

- `bose_fermi_gas.tex`
  - 修正磁化率/磁响应中缺少的 \(1/3\) 因子。

- `ising_model.tex`
  - 修正 \(q=2\) 链能量公式缺项。
  - 更新 Ising 相关图。

- `crystal_optics.tex`
  - 修正 \(i=0\) 特殊情形中 \(\theta_r\) 的 \((n_o/n_e)^2\) 因子。
  - 修正相关 \(t_R,t_R',T_R,T_R'\)。
  - 二次核实后修正 \(r_L'\) 关系和 \(R_L'\) 标签。
  - 新增晶体干涉装置示意图，并重命名对应绘图源码文件。

- `fourier_optics_4f.tex`
  - 修正频谱公式中多出的 \((2\pi)^2\) 因子。
  - 修正立方密排/六角密排峰值位置中的 \(\pi\) 与下标组合。

- `matrix_optics.tex`
  - 修正 Gaussian beam 中 \(q_0=1/(2k\omega_0^2)\) 的量纲问题。
  - 修正 \(z_{02}/q_{02}\) 的 \(f,h\) 形式漏掉主面位移 \(h,h'\) 的问题。
  - 删除或修正“牛顿关系对 Gaussian beam 精确成立”的结论。

### 主文件与图片/工具

- `main.tex`
  - 新增较多章节入口或结构调整。

- `README.md`
  - 少量说明更新。

- `fig/fig_style_python.py`
  - 更新绘图样式脚本。
  - 同时提交了 `fig/__pycache__/...pyc`，这是 Python 缓存产物，通常不建议纳入版本控制。

- 多个 `.png`
  - 大量图像重新生成或更新，主要分布在力学、电动力学、数学工具、统计、光学章节。
  - 核实时建议只检查对应正文公式是否确实需要更新图，不必逐像素比较。

---

## 建议核查顺序

1. 先看 `docs/change.md` 中后半部分的详细错误清单，它是 `be5c15a` 的详细错误清单与二次核实记录。
2. 再核查 `81ded3c` 中的三类高风险内容：
   - `matrix_optics.tex` 章节级重写；
   - `bose_fermi_gas.tex` 大段新增热力学内容；
   - `ising_model.tex` Bethe/BW 章节级重写。
3. 单独决定是否保留提交进历史的产物：
   - `build_verify/`
   - `fig/__pycache__/...pyc`
   - `script_rewrite/`
4. 对正文公式优先核查：
   - VSH 远场相位与辐射/散射角分布；
   - 刚体定点转动无磁场例子的 \(\omega_p\)；
   - Bose-Fermi 中 \(Y_{lm}^{*}\)、\(\sum_{i\ne j}\)、自旋简并度；
   - Ising 的 \(q=2\) 链与 Bethe 临界展开。

---

# 详细审核清单（原 issues.md）

# YHWNotes 章节审核问题汇总(2026-08-04)

全库 24 个章节文件完成系数/物理错误审核与叙述完整性审核。已修正的错误直接改入原文件;存疑项与叙述建议记录如下。
统计:已修改 72 处(力学 30、电学核心 11、电学其余 15、热学光学 8、数学工具 16,部分为同一处多符号);存疑 25+ 项;叙述与体系建议 140+ 条。

---
# 力学章节审核问题清单(inverse_square_motion / lorentz_transformation / nonlinear_oscillation / rigid_body)

审核方法:对每个关键公式先做量纲分析,再用 Python(sympy/numpy/scipy/mpmath)数值验证(代入数值检验恒等式、极限行为、闭合形式与原积分的互推、数值积分对照封闭公式)。以下按"已修改"、"未修改存疑项"、"叙述与体系问题"三节列出。

---

## 一、已修改(共 30 处)

### inverse_square_motion.tex(8 处)

【inverse_square_motion.tex:28】t(r) 积分第一项被积函数缺因子 E/c
- 原文:`t &= \int \dfrac{r + \alpha E / (E^2 - m^2 c^4)}{\sqrt{(E^2 - m^2 c^4) r^2 + 2 \alpha E r + \alpha^2 - c^2 L^2}} \, \d r - \dfrac{\alpha m^2 c^3}{E^2 - m^2 c^4} \int ...`
- 改后:第一项前加 `\dfrac{E}{c}`,即 `t = \dfrac{E}{c}\int \dfrac{r + \alpha E/(E^2-m^2c^4)}{\sqrt{...}}\d r - \dfrac{\alpha m^2 c^3}{E^2-m^2c^4}\int ...`
- 类型:量纲/系数
- 理由:由 ∂S/∂E 得精确被积函数 dt/dr = (Er+α)/(c√X)。数值验证:E=10,m=1,c=3,α=2,L=1,r=7 时,精确值 0.69109,原文 0.15004,改后与精确值完全一致。原文第一项量纲为 1/能量而非时间/长度。
- 严重程度:主要(后续 t(r) 封闭式(63 行)本身正确,此式为中间步骤)

【inverse_square_motion.tex:236】未定义符号 ζ₀
- 原文:`\dfrac{2 \pi}{\sqrt{1 - \beta_0^2 (1 - \beta_0^2) \zeta_0^2}}`
- 改后:ζ₀ → ζ
- 类型:记号
- 理由:ζ₀ 从未定义;由 α²/(c²L²) = ζ²β₀²(1−β₀²) 知应为 ζ。数值验证:用 ζ 代入后与精确 χ 一致。
- 严重程度:次要

【inverse_square_motion.tex:241】吸引双曲线偏转角 χ 的 β₀² 展开系数错误
- 原文:`\chi = 2 \arctan\zeta + \left(\pi \zeta^2 + \dfrac{\zeta (-1 + \zeta^2)}{1 + \zeta^2} - \zeta^2 \arctan\zeta\right) \beta_0^2 + \mathcal{O}(\beta_0^4)`
- 改后:`\chi = 2 \arctan\zeta + \left( \dfrac{\zeta (\zeta^2 - 1)}{1 + \zeta^2} + \zeta^2 \left( \dfrac{\pi}{2} + \arctan\zeta \right) \right) \beta_0^2 + \mathcal{O}(\beta_0^4)`
- 类型:系数/推导
- 理由:对精确式 χ = −π + 2cL/√(c²L²−α²)[π − arctan(√((E²−m²c⁴)(c²L²−α²))/(αE))] 做 β₀→0 展开,得到 β₀² 系数 C = ζ(ζ²−1)/(1+ζ²) + ζ²(π/2 + arctanζ)。数值拟合(ζ=0.5,1,2 外推 β₀→0)确认:ζ=0.5 时真值 0.2096 vs 原文 0.3695;ζ=2 时真值 11.88 vs 原文 9.34(ζ=1 恰好巧合相等)。
- 严重程度:主要

【inverse_square_motion.tex:272】排斥势 t(r) 积分第一项同样缺因子 E/c
- 原文:`t &= \int \dfrac{r - \alpha E / (E^2 - m^2 c^4)}{\sqrt{(E^2 - m^2 c^4) r^2 - 2 \alpha E r + \alpha^2 - c^2 L^2}} \, \d r + ...`
- 改后:第一项前加 `\dfrac{E}{c}`(与吸引情形对称)
- 类型:量纲/系数
- 理由:排斥情形 dt/dr = (Er−α)/(c√X);数值验证(同上参数)精确 0.89181,原文 0.34582,改后一致。
- 严重程度:主要

【inverse_square_motion.tex:324】排斥散射 χ 的 β₀² 展开系数错误
- 原文:`\chi = 2 \arctan\zeta + \left( \dfrac{\zeta (-1 + \zeta^2)}{1 + \zeta^2} - \zeta^2 \arctan (\zeta) \right) \beta_0^2 + \mathcal{O}(\beta_0^4)`
- 改后:`\chi = 2 \arctan\zeta + \left( \dfrac{\zeta (\zeta^2 - 1)}{1 + \zeta^2} + \zeta^2 \left( \arctan \zeta - \dfrac{\pi}{2} \right) \right) \beta_0^2 + \mathcal{O}(\beta_0^4)`
- 类型:系数/推导
- 理由:对精确式 χ = π − 2cL/√(c²L²−α²)arctan(...) 展开得 C = ζ(ζ²−1)/(1+ζ²) + ζ²(arctanζ − π/2)。数值拟合:ζ=0.5 真值 −0.5767 vs 原文 −0.4159;ζ=2 真值 −0.654 vs 原文 −3.229。
- 严重程度:主要

【inverse_square_motion.tex:395-397】GR 修正势 ε 与 f_r 的符号错误
- 原文:`\varepsilon (r, \theta) = \frac{\alpha L^2}{m^2 c^2 r^3}, \quad f_r = ... = \frac{3 \alpha L^2}{m^2 c^2 r^4} = \frac{3 \alpha^2}{m p^3 c^2} (1 + e \cos \theta)^4`
- 改后:ε = −αL²/(m²c²r³),f_r = −3αL²/(m²c²r⁴) = −3α²(1+ecosθ)⁴/(mp³c²)
- 类型:符号/结论
- 理由:Schwarzschild 有效势修正项为 ΔV = −GML²/(mc²r³) = −αL²/(m²c²r³)(吸引修正)。数值积分验证:按原文 f_r 符号得 Δφ_pr = −6πα/(mc²p)(负进动),与文末声称的 +6πα/(mc²p) 及水星 5.02×10⁻⁷ rad 矛盾;符号改正后精确得到 +6πα/(mc²p)。
- 严重程度:主要(不改则与文末结论直接矛盾)

【inverse_square_motion.tex:428】椭球四极矩修正势 ε 缺质量因子 m
- 原文:`\varepsilon (r, \theta) = \frac{-GM (a^2 - b^2)}{10 r^3} \left(3 \cos^2 (\theta - \alpha) - 1\right)`
- 改后:GM → GmM(ε 应为势能,与 V = −α/r、α = GMm 一致)
- 类型:量纲/系数
- 理由:扰动理论中 ε 是势能微扰。缺 m 时代入 Δφ = (p²/αe)∫... 得到的 Δφ 含 1/m 因子(量纲错误),且与文中结果 (3π/10)(a²−b²)/p² 不符;补上 m 后 m 恰好消去,数值积分给出 (3π/10)(a²−b²)/p²,与文末结果一致。
- 严重程度:主要

【inverse_square_motion.tex:433-437】双曲线附加偏转角 Δχ 公式中 (1−e²)^{5/2} 对 e>1 为虚数
- 原文:`+ \frac{2 (1 - e^2)^{5/2} \cos (2 \alpha)}{3 e^4}`
- 改后:`+ \frac{2 (e^2 - 1)^{5/2} \cos (2 \alpha)}{3 e^4}`
- 类型:符号/定义域
- 理由:Δχ 用于双曲线轨道(e>1),(1−e²)^{5/2} = i(e²−1)^{5/2} 使公式为复数,必然错误。数值积分(e=2,a²−b²=3,p=1)得 Δχ(α) = A + Bcos2α,A = 3.0541(与文中"π+√(e²−1)(1+2e²)/(3e²)−arccos(1/e)"部分一致),B = 0.5846 = (3/10)(a²−b²)/p²·2(e²−1)^{5/2}/(3e⁴),即 (e²−1)^{5/2} 且取正号。
- 严重程度:主要

### lorentz_transformation.tex(5 处)

【lorentz_transformation.tex:166】四维加速度空间分量错误
- 原文:`A^\mu = ( \gamma_u^4 \vb{a} \cdot \vb{\beta}_u, \gamma_u^4 ( \vb{a} + \vb{\beta}_u (\vb{\beta}_u \cdot \vb{a}) ) )`
- 改后:`A^\mu = ( \gamma_u^4 \vb{a} \cdot \vb{\beta}_u, \gamma_u^4 ( (1 - \beta_u^2) \vb{a} + \vb{\beta}_u (\vb{\beta}_u \cdot \vb{a}) ) )`(即 γ_u⁴[a − β_u×(β_u×a)] 或 γ_u⁴[(1−β_u²)a + β_u(a·β_u)])
- 类型:系数
- 理由:由 A = dU/dτ = γ d(γβc)/dt 直接求导得 A = γ⁴[(1−β²)a + β(a·β)]。数值:β_u=(0.2,0.1),a=(0.5,0.2):正确 (0.5529,0.2238) vs 原文 (0.5806,0.2349)。原文缺 −β_u²a 项。
- 严重程度:主要

【lorentz_transformation.tex:168】加速度变换公式 a' 错误
- 原文:`\vb{a}' = \dfrac{ \vb{a} (1 - \vb{\beta} \cdot \vb{\beta}_u) + (\vb{a} \cdot \vb{\beta}) (\vb{\beta}_u - \dfrac{\gamma}{\gamma+1} \vb{\beta}) }{ \gamma^2 (1 - \vb{\beta} \cdot \vb{\beta}_u) }`
- 改后:`\vb{a}' = \dfrac{ \vb{a} + \dfrac{(\vb{a} \cdot \vb{\beta})(\vb{\beta}_u - \dfrac{\gamma}{\gamma+1} \vb{\beta})}{1 - \vb{\beta} \cdot \vb{\beta}_u} }{ \gamma^2 (1 - \vb{\beta} \cdot \vb{\beta}_u)^2 }`
- 类型:推导
- 理由:用正确 A^μ 经洛伦兹变换并利用 a' = (A'−β_{u'}A'⁰)/γ_{u'}² 化简得上式(其中 (a·β_u) 项全部抵消)。数值:β=(0.2,0.1),β_u=(0.15,0.05),a=(1,0) 时正确 (1.0305,−0.000136) vs 原文 (0.9596,−0.000126)。并满足标准极限 a'∥ = a∥/[γ³(1−β·β_u)³]。原文公式系由错误的 A^μ 推出。
- 严重程度:主要

【lorentz_transformation.tex:170】四维加速度不变量错误
- 原文:`A^\mu A_\mu = \gamma_u^6 ( a^2 - (\vb{a} \cdot \vb{\beta}_u)^2 )`
- 改后:`A^\mu A_\mu = \gamma_u^6 ( a^2 - |\vb{a} \times \vb{\beta}_u|^2 )`
- 类型:推导
- 理由:−(A⁰)²+|A|² = γ_u⁸(1−β_u²)(a²−|a×β_u|²) = γ_u⁶(a²−|a×β_u|²);|a×β_u|² = a²β_u²−(a·β_u)² 与原文相差 a²β_u² 项。
- 严重程度:主要

【lorentz_transformation.tex:422】垂直 Boost 情形 Wigner 转角公式缺 1/2
- 原文:`\tan\theta = \tanh\left( \dfrac{\phi_1}{2} \right) \tanh\left( \dfrac{\phi_2}{2} \right)`
- 改后:`\tan\dfrac{\theta}{2} = \tanh\left( \dfrac{\phi_1}{2} \right) \tanh\left( \dfrac{\phi_2}{2} \right)`
- 类型:系数
- 理由:标准结果 tan(θ/2) = γ₁γ₂|β₁×β₂|/(1+γ₁+γ₂+γ) = tanh(φ₁/2)tanh(φ₂/2)(垂直情形)。数值:β₁=0.4,β₂=0.6:tan(θ/2)=0.06957 = tanh(φ₁/2)tanh(φ₂/2),而 tanθ=0.1398。
- 严重程度:主要

【lorentz_transformation.tex:575】电子自旋-轨道进动符号错误(且中间表达式乱)
- 原文:`\dfrac{\d \vb{s}}{\d t} = \left( \dfrac{-e\vb{B}_\text{eff}}{m_e} \cdot \dfrac{-\vb{\beta} \times \vb{E}}{2c} \right) \times \vb{s} = -\dfrac{e^2 \vb{L}}{8\pi\varepsilon_0 m_e^2 c^2 r^3} \times \vb{s}`
- 改后:`\dfrac{\d \vb{s}}{\d t} = \dfrac{e \vb{B}_\text{eff}}{m_e} \times \vb{s} = \dfrac{e^2 \vb{L}}{8\pi\varepsilon_0 m_e^2 c^2 r^3} \times \vb{s}`
- 类型:符号
- 理由:由已验证的 559 行公式(g_s=2,γ=1,B=0)得 ds/dt = (q/m)s×[−(1/2c)β×E] = −(e/2m_ec)s×(β×E);β×E = −eL/(4πε₀m_ecr³),故 ds/dt = +e²L×s/(8πε₀m_e²c²r³)。原式 -(e²L×s) 符号相反,且中间把 B_eff 与 β×E/(2c) 重复相乘(量纲混乱)。ΔU_SL(584 行)符号正确,未动。
- 严重程度:主要

### nonlinear_oscillation.tex(11 处)

说明:本文多处存在 ε/ω₀ 记账不一致。最终结果(79 行 ȧ = −ω₀ζa − εω₀Φ、134 行、180 行等)经核对与精确谐波平衡一致,故只修正中间被积式与明显错项。

【nonlinear_oscillation.tex:53、66】久期条件中 ζa 项缺因子 ω₀/ε(量纲错误)
- 原文:`2 \omega_0 (D_1 a + \zeta a) \sin\psi`、`2 \omega_0 (D_1 a + \zeta a) + d_1 = 0`
- 改后:`2 \omega_0 \left( D_1 a + \dfrac{\omega_0 \zeta a}{\epsilon} \right) \sin\psi`、`2 \omega_0 \left( D_1 a + \dfrac{\omega_0 \zeta a}{\epsilon} \right) + d_1 = 0`
- 类型:系数/量纲
- 理由:阻尼项 2ζω₀ẋ 在 O(ε) 层给出 sinψ 系数 2ζω₀²a,而阻尼系数 ζ ~ ε 应写成 ζ = εζ̃,故该项 = 2ω₀·(ω₀ζa/ε)。原式 D₁a + ζa 量纲混乱(D₁a ~ a/t,ζa ~ a)。改后恰给出 79 行 ȧ = −ω₀ζa − εω₀Φ(与精确自由衰减 ȧ = −ζω₀a 一致)。
- 严重程度:主要

【nonlinear_oscillation.tex:114】驱动情形 RHS:ζa 缺因子 ω₀/ε,且 σ 项符号错误
- 原文:`... + 2 \omega (D_1 a + \zeta a) \sin\psi + ... + \omega_0^2 B \cos(\psi - \theta) - \omega_0^2 \sigma a \cos\psi`
- 改后:ζ 项加 ω₀/ε;`- \omega_0^2 \sigma a \cos\psi` → `+ \omega_0^2 \sigma a \cos\psi`
- 类型:系数/符号
- 理由:由 O(ε) 方程(104 行,含 −ω₀²σx₀)移项,RHS 应为 +ω₀²σx₀ = +ω₀²σa cosψ。改后与 135 行 θ̇ = (ω₀/2s)(1−s²−εBcosθ/a−2εΨ/a)(已核对正确)自洽。
- 严重程度:主要

【nonlinear_oscillation.tex:119】ζa 缺因子 ω₀/ε
- 原文:`2 \omega (D_1 a + \zeta a) + \omega_0^2 B \sin\theta + 2 \omega_0^2 \Phi(s, a) = 0`
- 改后:`2 \omega \left( D_1 a + \dfrac{\omega_0 \zeta a}{\epsilon} \right) + ...`
- 类型:系数/量纲
- 理由:同 53/66 行;改后经 ȧ = εD₁a 恰给出 134 行正确形式。
- 严重程度:主要

【nonlinear_oscillation.tex:122】σ 项符号错误
- 原文:`2 \omega a (D_1 \theta) + \omega_0^2 B \cos\theta - \omega_0^2 \sigma a + 2 \omega_0^2 \Psi(s, a) = 0`
- 改后:`... + \omega_0^2 \sigma a ...`
- 类型:符号
- 理由:与 114 行修正对应;改后给出 135 行 θ̇ 与 141 行 Bcosθ_s = a_s(1−s²)/ε − 2Ψ_s。
- 严重程度:主要

【nonlinear_oscillation.tex:140】稳态 Bsinθ_s 缺 1/ε
- 原文:`B \sin\theta_{\mathrm{s}} = -2 \zeta s a_{\mathrm{s}} - 2 \epsilon \Phi(s, a_{\mathrm{s}})`
- 改后:`B \sin\theta_{\mathrm{s}} = -\dfrac{2 \zeta s a_{\mathrm{s}}}{\epsilon} - 2 \Phi(s, a_{\mathrm{s}})`
- 类型:系数
- 理由:精确谐波平衡:−2ζω₀ωa − εd₁ = εω₀²Bsinθ ⇒ Bsinθ = −2ζsa/ε − 2Φ。原文与其自身 134 行(2ζsa+εBsinθ+2εΦ=0)也不自洽(缺除以 ε)。改后与 180 行 Duffing 响应 (2ζs)² + (s²−1−3εa²/4)² = ε²B²/a² 一致。
- 严重程度:主要

【nonlinear_oscillation.tex:145】响应曲线第一项缺 1/ε
- 原文:`\left( \Phi_s + \zeta s a_{\mathrm{s}} \right)^2 + \left( \Psi_s + \dfrac{a_{\mathrm{s}} (s^2 - 1)}{2 \epsilon} \right)^2 = \dfrac{B^2}{4}`
- 改后:第一项 `\left( \Phi_s + \dfrac{\zeta s a_{\mathrm{s}}}{\epsilon} \right)^2`
- 类型:系数
- 理由:由修正后的 140/141 行平方相加即得;改后 Duffing 极限与 180 行一致。
- 严重程度:主要

【nonlinear_oscillation.tex:387】亚谐波振幅方程缺 ε(与超谐波情形 336 行约定不一致)
- 原文:`\dot{a} = -\omega_0 \zeta a + \dfrac{3 \omega_0 a^2 A}{8} \sin\gamma,\quad \dot{\gamma} = \dfrac{9 \omega_0}{8} (a^2 + 2A^2 + aA \cos\gamma) - \omega_0 \sigma`
- 改后:`\dot{a} = \omega_0 \epsilon \left( -\zeta a + \dfrac{3 a^2 A}{8} \sin\gamma \right),\quad \dot{\gamma} = \omega_0 \epsilon \left( \dfrac{9}{8} (a^2 + 2A^2 + aA \cos\gamma) - \sigma \right)`
- 类型:系数
- 理由:与超谐波情形 336 行 ȧ = ω₀ε(−ζa + A³sinγ/8) 结构应一致(稳态方程 391 行不受影响,ε 在稳态中消去)。
- 严重程度:次要

【nonlinear_oscillation.tex:401、407、411】亚谐波 q 及其导出稳定性条件中 ζ² 项多乘了 1/ε²
- 原文(401):`q = \dfrac{64}{81} \left( \dfrac{9\zeta^2}{\epsilon^2} + \left( \sigma - \dfrac{9A^2}{4} \right)^2 \right)`;407 行 `... + 8 (1 - s^2)^4 \dfrac{\zeta^2}{\epsilon^2} \leq 0`;411 行 `... \sqrt{\left( \dfrac{s-3}{\epsilon} \right)^2 - \dfrac{63\zeta^2}{\epsilon^2}}`
- 改后:三处 ζ²/ε² → ζ²(401 行为 `9\zeta^2`、407 行为 `8(1-s²)^4\zeta²`、411 行为 `63\zeta²`)
- 类型:系数
- 理由:由 391 行稳态方程 (8ζ/3)² + (8σ/9−a_s²−2A²)² = A²a_s² 得 u=a_s² 满足 u²−2pu+const=0,const = (8σ/9−2A²)²+64ζ²/9,即 q = (64/81)(σ−9A²/4)² + 64ζ²/9,ζ² 项无 1/ε²。数值:σ=5,A=1,ζ=0.1,ε=0.1 时原文 q=13.086 使 p²−q<0(判无实根),而稳态方程确有实根 u=4.564,1.325;正确 q=6.046 给出 p±√(p²−q)=4.564,1.325 完全吻合。407/411 行由 q 导出,随之修正。
- 严重程度:主要

### rigid_body.tex(6 处)

【rigid_body.tex:157】ω₃² 表达式分母符号错误
- 原文:`\omega_3^2 = \frac{1}{I_3(I_1-I_3)}\left[(L^2 - 2EI_1) - I_2(I_2-I_1)\omega_2^2\right]`
- 改后:`I_3(I_1-I_3)` → `I_3(I_3-I_1)`
- 类型:符号
- 理由:由 2EI₁ − L² = I₂(I₁−I₂)ω₂² + I₃(I₁−I₃)ω₃² 解出 ω₃² = [(L²−2EI₁)−I₂(I₂−I₁)ω₂²]/[I₃(I₃−I₁)]。原文分母为负,给出负的 ω₃²。
- 严重程度:主要

【rigid_body.tex:186】情况一变量 s 定义中分母符号错误
- 原文:`s = \omega_2\sqrt{\frac{I_2(I_2-I_1)}{2EI_1-L^2}}`
- 改后:`s = \omega_2\sqrt{\frac{I_2(I_2-I_1)}{L^2-2EI_1}}`
- 类型:符号
- 理由:情况一 L² ≥ 2EI₁ 恒成立,2EI₁−L² ≤ 0,原文 s 为虚数。改正后验证 (ds/dτ)² = (1−s²)(1−k²s²) 严格成立,并给出 198-200 行 ω₁,ω₂,ω₃ 的 dn/sn/cn 解。
- 严重程度:主要

【rigid_body.tex:203】情况一 φ̇ 缺因子 L
- 原文:`\dot{\varphi} = \frac{(2EI_3-L^2)+(L^2-2EI_1)\sn^2(\tau,k)}{I_1(2EI_3-L^2)+I_3(L^2-2EI_1)\sn^2(\tau,k)}`
- 改后:分子前加 `L`
- 类型:系数/量纲
- 理由:由 172 行一般公式 φ̇ = L(I₁ω₁²+I₂ω₂²)/(I₁²ω₁²+I₂²ω₂²) 代入 ω₁²,ω₂² 化简得含 L 的形式。数值验证(I₁=1,I₂=2,I₃=3,E=10,L²=25,s²=0.3):一般公式 4.6203 = L×0.9240。原文量纲为 1/(I)(错误),应为 1/时间。注意情况二(237 行)已有 L,原文两情形不一致。
- 严重程度:主要

【rigid_body.tex:307】Jacobi 椭圆函数倒数模变换第三式错误
- 原文:`\dn(\tau,k)=\dn(k\tau,\frac{1}{k})`
- 改后:`\dn(\tau,k)=\cn(k\tau,\frac{1}{k})`
- 类型:系数
- 理由:标准倒数模变换:sn(u,k)=(1/k)sn(ku,1/k)、cn(u,k)=dn(ku,1/k)、dn(u,k)=cn(ku,1/k)。数值(mpmath,参数 m=k²):dn(1,0.5)=0.91149 = cn(0.5,1/k)=0.91149,而 dn(0.5,1/k)=0.56857 ≠ 0.91149。
- 严重程度:次要

【rigid_body.tex:376】定点转动 θ 运动方程三项符号全部相反
- 原文:`I_1 \ddot{\theta} = -M g a \sin \theta - \Omega^2 (I_3 - I_1) \sin \theta \cos \theta + \frac{(p_\phi - p_\psi \cos \theta)(p_\psi - p_\phi \cos \theta)}{I_1 \sin^3 \theta}`
- 改后:`I_1 \ddot{\theta} = M g a \sin \theta + \Omega^2 (I_3 - I_1) \sin \theta \cos \theta - \frac{(p_\phi - p_\psi \cos \theta)(p_\psi - p_\phi \cos \theta)}{I_1 \sin^3 \theta}`
- 类型:符号
- 理由:哈密顿方程 ṗ_θ = −∂H/∂θ(sympy 符号验证:正确结果恰为原文的相反数)。修正后:Ω=0 极限退化为陀螺标准方程 I₁θ̈ = Mgasinθ + (p_φ−p_ψcθ)(p_ψ−p_φcθ)/(I₁s³θ);且与文末 392/401 行 ω_p 公式一致(数值:ω_p/Ω = 8.640,用修正后方程线性化得到相同值)。
- 严重程度:主要

【rigid_body.tex:408】心形刚体 I₃ 幂次错误
- 原文:`I_3 = \frac{64}{35} \pi \rho R^3`
- 改后:`I_3 = \frac{64}{35} \pi \rho R^5`
- 类型:量纲/系数
- 理由:I₃ = ∫s²dm 量纲必为 ρR⁵;数值积分(旋转心形,r(θ)=R(1−cosθ))得 I₃ = 64πρR⁵/35(注意薄圆盘对轴惯量为 (1/2)dm·y²)。其余量已核对无误:M = 8πρR³/3 ✓,I₁(P) = 192πρR⁵/35 ✓,a = 6R/5 ✓(三维质心 x̄ = −4R/5 精确解析),γ = 1/3 ✓(64/192)。
- 严重程度:主要

---

## 二、未修改的存疑项

【rigid_body.tex:409、412-415】心形例题 α = 7/12 与给定输入不自洽
- 原文:`\alpha = \frac{7}{12}` 且 `g/R\,\Omega^2=1.2`,计算得 ψ̇₀/Ω = 1.926、ω_p/Ω = 8.640
- 存疑理由:由文中 a=6R/5、M=8πρR³/3、I₁=192πρR⁵/35、g/(RΩ²)=1.2 得 α = (35/72)(a/R)(g/(RΩ²)) = (7/12)(g/RΩ²) = 0.7,而非 7/12;α=7/12 需 (a/R)(g/RΩ²)=6/5(即 g/RΩ²=1 或 a=R)。文末数值 1.926、8.640 确由 (α,γ)=(7/12,1/3) 算出(已验证),即作者实际使用了 α=7/12。因无法确定作者意图(a、g/RΩ²、α 三者哪一项需改),未改动,仅记录。

【rigid_body.tex:261-268】情况三"若初始时刻角速度仅有 2 轴分量 ω₀,则系统达到稳态时 ω₁=…,ω₂=0,ω₃=…"表述混乱
- 存疑理由:(0, ω₀, 0) 是欧拉方程的不动点(ω̇=0),以此为初值系统将停留不动;而 ω₁*, 0, ω₃* 实际是分界轨迹在 t=0 时刻的值(时间反演对称性的正确表述应为:t→−∞ 时 ω→(0,−ω₀,0),t=0 时 (ω₁*,0,ω₃*),t→+∞ 时 ω→(0,+ω₀,0),即角速度渐近地回到中间轴)。文中"角速度会从 2 轴转移到 1、3 轴"作为长期结论不严谨。因语义可作多种解读,未改。

【lorentz_transformation.tex:527-528】"S_ν" 的指标约定与度规降指标相差一个负号
- 原文:`S_{\nu}\dfrac{\d U^\nu}{\d \tau} = \left( \vb{\beta} \cdot \vb{S} \right) \dfrac{\d(\gamma c)}{\d \tau} - \vb{S} \cdot \dfrac{\d(\gamma \vb{\beta} c)}{\d \tau} = -\gamma c \, \vb{S} \cdot \dfrac{\d \vb{\beta}}{\d \tau}`
- 存疑理由:按度规降指标 S_ν = (−β·S, S),正确结果为 +γc S·dβ/dτ;文中按 "S_ν = (β·S, −S)" 处理,前后(531-532 行及 559 行标准公式)自洽且最终结果正确,属记号约定问题而非结果错误。因整套推导一致,未改,建议加注说明。

【inverse_square_motion.tex:53】α = cL 情形的角度零点与其他情形不同
- 存疑理由:该式在 φ 取"从入射渐近线方向起算"时成立(φ→∞ 处 r=∞ 对应 |φ|=√(E²−m²c⁴)/E = |φ|min 极限),与 cosh/cos 情形(转角在近日点/坠心点为 0)零点不同;公式仅对 |φ| ≥ |φ|min 有效。公式本身数值验证正确,属角度约定未加说明的问题,未改。

【nonlinear_oscillation.tex:79、134 vs 336】ε 记账约定前后不统一(ζ 项带不带 ε)
- 原文:79 行 ȧ = −ω₀ζa − εω₀Φ(ζ 不带 ε);336 行 ȧ = ω₀ε(−ζa + A³sinγ/8)(ζ 带 ε);134 行(ζ 不带 ε)
- 存疑理由:79、134 行与精确结果一致,336 行按 ȧ=εD₁a 约定;两处约定互相矛盾。因 336 行稳态(342-343 行)不受影响,且不确定作者意图,未改 336 行,仅记录(若统一约定,336 行应改为 ȧ = −ω₀ζa + εω₀A³sinγ/8)。

---

## 三、叙述与体系问题(仅建议,未修改)

### inverse_square_motion.tex
- 【1-10 行】知识点跳跃:开篇直接给出相对论哈密顿-雅可比方程(V = −α/r 的库仑/开普勒问题),未说明该问题来源(如相对论性开普勒、氢原子)、为何在 SI 制引入 c,缺引入段。建议:加一段动机(相对论修正、精细结构)。
- 【21-29 行】推导跳跃:从 f(r) 到 φ(r)、t(r)(∂S/∂L、∂S/∂E 求导及被积函数变形)一步带过,且正是此处出现系数错误。建议:补充 ∂S/∂L、∂S/∂E 的求导过程。
- 【64 行】E = mc² 特例的 t(r) 直接给出,未说明是 E > mc² 情形的极限;建议注明。
- 【168-215 行】玻尔-索末菲量子化条件(∮p_r dr = 2πn_rħ)突然引入,未说明半经典量子化背景;结合能展开(203-215 行)结果直接给出未推导。建议补充。
- 【218-244 行】"记 ζ = α/(mc²bβ₀²),可以化简得"——从 (E,L) 到 ζ 的代入化简全部跳过;且展开系数恰在此处出错。建议补充化简与展开步骤。
- 【228 行】"设物体在无穷远处速率为 β₀c,入射半径为 b"——β₀、b 的几何意义应配图说明。
- 【329-390 行】微扰理论部分推导较完整,但 Δφ 公式(371 行)前应说明 ΔA_eff 与轨道长轴进动角的关系。
- 【392-423 行】GR 例子中"平均进动角速度"的 T 用了开普勒周期但中间式 (Δφ/2π)√(α/(mp³)) 缺 (1−e²)^{3/2} 因子(最终结果正确),建议修正中间式以免读者困惑。

### lorentz_transformation.tex
- 【165-171 行】四维加速度例:各项结果直接给出,无推导;且此处公式有误(已修)。建议补充 dU^μ/dτ 的推导。
- 【209-236 行】二阶张量变换的 w', S', G', Σ' 四个分块公式直接给出,未展示矩阵乘法过程,是全章最大的推导缺口;建议补充或加注(分块矩阵乘法)。
- 【298-308 行】电磁场张量例中混合指标与双上指标两种约定(w=0, Σ=−ε·B, S=G=E/c 与 S=−G=E/c)未解释两者关系及为何不变量相同。
- 【366-384 行】Wigner 转动推导中"代入…给出关系式"两步之间的大量矩阵代数被跳过;建议至少注明利用了 β₂⊕β₁ 与 β₁⊕β₂ 的 γ 相等关系。
- 【455-461 行】δφ 展开与对易子恒等式 [L^{2n−1},δL]、[L^{2n},δL] 直接给出,未推导。
- 【509-517 行】BMT 协变形式"可确定各项系数"——系数确定过程完全跳过,建议补充(利用 U_μS^μ=0 与退化形式)。
- 【527 行】"S_ν" 指标约定特殊(见存疑项),建议加注说明,否则读者按度规降指标会得到相反符号。
- 章节之间衔接:EM 场张量例(298 行)与 Wigner 转动(331 行)之间缺过渡段说明为何研究 Wigner 转动(加速系/托马斯进动动机)。

### nonlinear_oscillation.tex
- 【3-10 行】缺引入:为何研究单自由度非线性振动(杜芬、自激等),ε 展开的适用条件(弱非线性)未说明。
- 【8 行】"阻尼项量级规定为 ζ ~ ε"与后续公式中 ζ 的 ε 记账(见存疑项)易让读者困惑;建议明确约定"ζ = εζ̃"并统一。
- 【17-29 行】m=2 展开式给出但全文未使用(m=1 足够),建议删去或注明"仅作示意"。
- 【99-104 行】驱动情形把齐次项从 ω₀² 换成 ω² 并引入 σ 的技巧未解释(为何能这样替换、σ 的物理意义=失谐)。
- 【283-326 行】远共振情形:Duffing 代入后"最后一步仅保留…"的截断(321→322 行)未说明丢弃项的判据(3ψ、Φ+2ψ 等非久期);建议加一句说明。
- 【328-353 行】超谐波:3ω = ω₀(1+εσ) 与 γ = θ−σω₀T₁ 的引入较突兀;345-353 行"三次方程至少有一个实根"结论与响应曲线图之间缺解释。
- 【380-424 行】亚谐波:Φ = 3ψ−γ 的相位关系未配图说明;415-418 行 ψ 的化简(γ_s+σω₀εt 的代入)略跳。

### rigid_body.tex
- 【36-50 行】欧拉角几何:图给出但三次旋转"绕 z 轴→绕 x' 轴→绕 z'' 轴"的几何意义与角速度 ω = θ̇û_ON + φ̇ẑ + ψ̇x₃ 的物理(各分量的转轴)可再解释。
- 【143-159 行】"选取如下三个独立方程"——为何选 L²、2E 与第二欧拉方程;2EI₁ ≤ L² ≤ 2EI₃ 的推导未给出。
- 【177-209 行】情况一的变量代换(τ、s、k)直接引入,未说明如何从 (dω₂/dt)² 化为 (ds/dτ)²=(1−s²)(1−k²s²);k² 的物理意义(两种情形的判别)建议说明。
- 【245-268 行】情况三的表述(见存疑项)与"时间反演对称性"的论证过于简略,建议重写。
- 【327-346 行】定点转动例题:磁项 ∫A·v dq = Ω·L 的推导(Ω = QB/2M、L 为绕 P 的角动量)未展开;例中 I₁、I₃ 已含"过 P"的下标省略说明,但 L 用的是 I_P·ω 这一点宜明示。
- 【404-416 行】心形例题:a、M、I₁、I₃ 的数值直接给出(未给积分过程);且 I₃ 出错(已修)、α 与给定输入不自洽(见存疑项),建议补推导并核对数值。

---

## 总结

共发现并修正 30 处错误:致命 0,主要 24,次要 6(另 5 项存疑未改)。错误类型分布:系数/量纲类 16 处、符号类 8 处、推导类 4 处、记号类 2 处。所有修改均经量纲分析与数值验证。

---

# 电动力学三章检查报告(radiation / scattering / STF)

检查日期:2026-08-04。检查方式:量纲分析 + 手工推导 + Python(scipy/mpmath)数值验证。
已按用户授权修改确认的错误(修改后未重新编译,建议编译验证)。

---

## 一、已修改清单(共 11 处)

### radiation.tex(6 处)

**1.【radiation.tex L27】∇×E' 方程源项缺旋度**
- 原文:`\nabla \times \vb{E}' - i k Z_0 \vb{H}' = \frac{i}{\omega \epsilon_0} \vb{J}`
- 改后:`\nabla \times \vb{E}' - i k Z_0 \vb{H}' = \frac{i}{\omega \epsilon_0} \nabla \times \vb{J}`
- 理由:由 ∇×E' = ∇×E + (i/ωε0)∇×J = ikZ0H' + (i/ωε0)∇×J 直接得出;且 L32 的 (∇²+k²)E' 公式(含 ∇×(∇×J)/k²)要求源项为 ∇×J。原文缺 ∇× 无法推出 L32。
- 严重程度:次要(中间公式笔误,L32 起已用正确形式)。

**2.【radiation.tex L37】r·H' 方程右端类型错误**
- 原文:`(\nabla^2 + k^2)(\vb{r} \cdot \vb{H}') = -i \vb{L} \cdot \vb{J} + \nabla \times \vb{M}`
- 改后:`(\nabla^2 + k^2)(\vb{r} \cdot \vb{H}') = -i \vb{L} \cdot \left( \vb{J} + \nabla \times \vb{M} \right)`
- 理由:左端是标量,右端 ∇×M 是矢量,类型不符。由 L33 的 (∇²+k²)H' = -∇×(J+∇×M) 取 r· 并利用 r·(∇×f) = iL·f 得 -iL·(J+∇×M)。
- 严重程度:次要。

**3.【radiation.tex L95】角动量辐射功率系数量纲错误(差 1/c)**
- 原文:`\frac{Z_0}{2k^3 c^2}`
- 改后:`\frac{Z_0}{2k^3 c}`
- 理由:与散射问题(scattering.tex L59)的同类公式 Z0/(2k0²ω) 比较:Z0/(2k²ω) = Z0/(2k³c)(因 kc=ω),原文多一个 1/c。量纲检查:Z0/(k³c²)·|a|² 给出 kg·m/s(非 J),改正后给出 J ✓。数值验证:dL/dt = P/ω 对圆偏振偶极成立。
- 严重程度:主要(量纲错误)。

**4.【radiation.tex L363】频谱公式积分核应为 r̂×(r̂×β)**
- 原文:`\left| \int_{-\infty}^{\infty} e^{i\omega \left( t_{s} - \uv{R} \cdot \vb{r}_{q}(t_{s})/c \right)} \uv{R} \times \vb{\beta} \, \d t_{s} \right|^{2}`
- 改后:`\left| \int_{-\infty}^{\infty} e^{i\omega \left( t_{s} - \uv{R} \cdot \vb{r}_{q}(t_{s})/c \right)} \uv{R} \times \left( \uv{R} \times \vb{\beta} \right) \, \d t_{s} \right|^{2}`
- 理由:L354 部分积分后的 E(r,ω) 含 r̂×(r̂×β),L363 由此推出却写 r̂×β。数值验证:二者模对圆周运动巧合相等(|∫r̂×β| = |∫r̂×(r̂×β)| = 0.3949),但偏振分辨不同;L387 的 e_b 分量 J'_m 结构来自 r̂×(r̂×β) 版本,故 L363 应为后者。对后续功率公式无数值影响。
- 严重程度:次要(形式笔误,结果不受影响)。

**5.【radiation.tex L386】圆周运动频域电场缺 β 因子(确认用户提示)**
- 原文:`-\frac{i q \omega e^{i\omega r/c}}{2\sqrt{2\pi} \varepsilon_{0} c r}`
- 改后:`-\frac{i q \omega \beta e^{i\omega r/c}}{2\sqrt{2\pi} \varepsilon_{0} c r}`
- 理由:从 L353-354 出发完整推导(含部分积分与周期 δ 归一化)得 E(r,ω) = -iqωβe^{iωr/c}/(2√(2π)ε0cr)·δ(ω-mβc/a)·[e_a·m sinθJ_m(x)/x - i e_b J'_m(x)],x=ωa cosθ/c。mpmath 高精度数值(推迟时间精确处理)逐项确认:β 因子必须存在(L386 缺),且 e_a 分量除 m sinθJ_m/x 外**无**额外 J'_m 项(用户提示的"缺 β"确认;"icosθJ'_m 项"不存在,初查时误判,已排除)。
- 严重程度:主要。注意:L387(L388-L390)已含 β² 因子,正确,未改。

**6.【radiation.tex L424】简谐运动频域电场相位错误(缺 i 因子)**
- 原文:`-i^{-m} \uv{e}_{a}`
- 改后:`-i^{1-m} \uv{e}_{a}`
- 理由:由 L423 直接积分(δ 归一化)得 δ 系数应为 -(-1)^m i^{m+1}·qωtanθJ_m/(2√(2π)ε0cr),即 L424 缺一个 i 因子。数值验证(m=1,2,3,β0=0.6,θ=0.9):mpmath 精确积分给出 δ 系数 -0.02764(实)、+0.02002j(虚)、+0.01220(实),与 -i^{1-m} 版本逐一吻合(比值 1.000),与 -i^{-m} 版本不符(相位+大小均错)。L425-L427(平方量)不受影响,正确。
- 严重程度:主要。

### scattering.tex(5 处)

**7.【scattering.tex L250-251】表面阻抗球的 α_l/β_l 小 kR 近似系数错误(差 (2l+1) 因子)**
- 原文:`-\dfrac{2i(kR)^{2l+1}}{[(2l+1)(2l-1)!!]^2}\dfrac{kR-i z_s(l+1)}{kR+i z_s l}`(β 同构)
- 改后:`-\dfrac{2i(kR)^{2l+1}}{(2l+1)!!\,(2l-1)!!}\dfrac{kR-i z_s(l+1)}{kR+i z_s l}`
- 理由:由 α = -1-(H*kR-iz_sH'*)/(HkR-iz_sH') 用 j_l≈x^l/(2l+1)!!, n_l≈-(2l-1)!!/x^{l+1} 小宗量展开,得 α_l = -2i(kR)^{2l+1}(kR-iz_s(l+1))/[(2l+1)!!(2l-1)!!(kR+iz_sl)]。数值验证(kR=0.01, δ/R=0.1, z_s=kδ(1-i)/2):精确 α_1 = -9.05e-8-5.67e-7i;原文公式(÷3)误差 67%;修正后误差 1.7%(剩余为高阶项)。l=1 时 (2l+1)!!(2l-1)!! = 3,原文 (2l+1)²(2l-1)!!² = 9,差 3 倍。
- 严重程度:主要。

**8.【scattering.tex L308】长波长散射场 α、β 配对位置交换 + 缺 1/r**
- 原文:`-\dfrac{3}{4}i E_{\rm inc} \dfrac{e^{ikr}}{kr}\bigl(\alpha(\uv{n}_s\times\uv{e}_i)\times\uv{n}_s + \beta(\uv{n}_i\times\uv{e}_i)\times\uv{n}_s\bigr) = \dfrac{k^2 e^{ikr}}{4 \pi\varepsilon_0} E_{\rm inc}\bigl(\kappa_e (\uv{n}_s\times\uv{e}_i)\times\uv{n}_s + \kappa_m (\uv{n}_i\times\uv{e}_i)\times\uv{n}_s\bigr)`
- 改后:`-\dfrac{3}{4}i E_{\rm inc} \dfrac{e^{ikr}}{kr}\bigl(\beta(\uv{n}_s\times\uv{e}_i)\times\uv{n}_s + \alpha(\uv{n}_i\times\uv{e}_i)\times\uv{n}_s\bigr) = \dfrac{k^2 e^{ikr}}{4 \pi\varepsilon_0 r} E_{\rm inc}\bigl(\kappa_e (\uv{n}_s\times\uv{e}_i)\times\uv{n}_s + \kappa_m (\uv{n}_i\times\uv{e}_i)\times\uv{n}_s\bigr)`
- 理由:(a) 从 L269-271 的 E_sc = √(3π/2)E_inc e^{ikr}/(kr)ΣA_±(±β r̂×X - iαX) 与 L300-304 恒等式严格推导,得 -(3/4)iE_inc e^{ikr}/(kr)[β(n̂_s×ê_i)×n̂_s + α(n̂_i×ê_i)×n̂_s],原文 α/β 位置交换;(b) 电偶极散射场 ∝ κ_e(n̂_s×ê_i)×n̂_s(与 L325 一致),非磁性介电球(μr=1)电极化率应 ∝ (εr-1),修正后 β(∝εr)配电模式,物理正确(原文 α(∝μr)配电模式导致 μr=1 时电散射为零,荒谬);(c) 系数核对:-(3/4)iβ/(kr) = k²κ_e/(4πε0r)(κ_e=3πε0β/(ik³)),第二式必须含 1/r 分母。
- 严重程度:主要。

**9.【scattering.tex L313】κ_e、κ_m 与 α、β 的对应交换**
- 原文:`\kappa_e = \dfrac{3 \pi\varepsilon_0}{i k^3}\alpha, \quad \kappa_m = \dfrac{3 \pi\varepsilon_0}{i k^3}\beta`
- 改后:`\kappa_e = \dfrac{3 \pi\varepsilon_0}{i k^3}\beta, \quad \kappa_m = \dfrac{3 \pi\varepsilon_0}{i k^3}\alpha`
- 理由:与 L308 修正配套。修正后 κ_e = 4πε0R³(εr-1)/(εr+2)(介电球极化率 ✓)、κ_m = 4πε0R³(μr-1)/(μr+2) ✓;且 L345 的经典结论(修正后)与 L346 的 α=i(4/3)(μr-1)/(μr+2)(kR)³、β=i(4/3)(εr-1)/(εr+2)(kR)³ 自洽:α↔κ_m↔μr,β↔κ_e↔εr。瑞利截面 L353 数值与标准一致(εr 项配 (1+cos²θ))。
- 严重程度:主要。

**10.【scattering.tex L340】β 的相移角分式分子笔误(μr → εr)**
- 原文:`\exp\Bigl[2i\arctan\Bigl(\dfrac{J_1\Pi_1'- \mu_r \Pi_1 J_1'}{N_1\Pi_1'- \varepsilon_r \Pi_1 N_1'}\Bigr)\Bigr]`
- 改后:`\exp\Bigl[2i\arctan\Bigl(\dfrac{J_1\Pi_1'- \varepsilon_r \Pi_1 J_1'}{N_1\Pi_1'- \varepsilon_r \Pi_1 N_1'}\Bigr)\Bigr]`
- 理由:L173 定义 Δ = arctan((JΠ'-εrΠJ')/(NΠ'-εrΠN'))(分子分母均 εr);L163 的 β 公式含 εr。原文分子误用 μr。
- 严重程度:次要(笔误)。

**11.【scattering.tex L345】κ_m、κ_e 的经典公式配对交换**
- 原文:`\kappa_m = 4\pi \varepsilon_0 R^3 \dfrac{\varepsilon_r-1}{\varepsilon_r+2}, \quad \kappa_e = 4\pi \varepsilon_0 R^3 \dfrac{\mu_r-1}{\mu_r+2}`
- 改后:`\kappa_e = 4\pi \varepsilon_0 R^3 \dfrac{\varepsilon_r-1}{\varepsilon_r+2}, \quad \kappa_m = 4\pi \varepsilon_0 R^3 \dfrac{\mu_r-1}{\mu_r+2}`
- 理由:电极化率必须 ∝ (εr-1)(非磁性介质球 p = κ_eE_inc ≠ 0 的物理要求);与 L313/L346 修正后自洽。
- 严重程度:主要。

---

## 二、存疑/未修改项

1.【radiation.tex L59-70】球坐标展开的 a_lm、b_lm 积分公式(L68-69)与 Jackson 标准结果(9.178-9.186 附近)一致,但中间推导(L55-L69)个别步骤未逐项重推,未发现错误。
2.【radiation.tex L423-427】简谐运动:L423 正确;L425-L427 经数值验证正确(L426 与 L453 一致)。
3.【radiation.tex L404-406】同步辐射连续化:L404 与 L405 系数解析精确一致;L405 与精确求和(L388,β=0.99)逐点一致(θ=0.02 处 9% 内,θ=0.2 处 1% 内);L405 与 L406 的积分关系 2π∫_{-∞}^{∞}dθ(每单位 θ 密度约定)数值一致(3% 内)。未发现错误。
4.【radiation.tex L561-755】二体辐射算例:L588、L599-601、L614、L743-752 均手工验证正确(与 Peters-Mathews 引力波公式一致)。L619 的轨道演化闭式、L624 的相撞时刻未重推,存疑。
5.【radiation.tex L757-1057】Cherenkov 部分:L845 的 d²W/dzdω = μ0q²ω/(4π)(1-1/(β²ε)) 与标准一致;其余(磁矩场、时空解)未数值验证,存疑。
6.【radiation.tex L1059-1189】穿越辐射:L1153-1154 的电荷部分结构与标准一致,磁矩部分(L1168, L1173, L1183)系数未独立验证,存疑。
7.【radiation.tex L539】四极辐射功率 1/(720πε0c⁵) 系数正确(标准);但 D 定义为非无迹(L513),公式直接用 (∂³D:∂³D) 隐含 D 无迹,与定义不一致(例子里 D 无迹)。存疑(约定问题)。
8.【scattering.tex L58】dP/dΩ = Z0/(2k0²)|Σ(aX + br̂×X)|² 与 L56 的远场 -a r̂×X + bX 的交叉项符号不一致(对角项相同、总功率正确);但 L116(含 iβ 的结构)经验证与标准瑞利一致。L58 作为"一般公式"的交叉项符号存疑,未改。
9.【scattering.tex L184-206】介质球 kR≫1 的近似(kR≫1 分支含 arctan(z_r tan(...)))未验证,存疑。
10.【scattering.tex L603-613】圆柱 z_s 小球近似的 m=0 分支(含 ln 项)未验证,存疑。
11.【stf_multipole_expansion.tex】L267-275 的 P^{(n)}/M^{(n)} 高阶修正系数(1/42, 1/60, 1/1680 等)为专业文献结果,未独立验证,存疑;L256-257 的 STF 积分形式系数 ((2n-1)!!, (n+1)) 与标准一致。L385-386 已验证与通用公式(L293, L302)自洽,正确。L402 环形电偶极矩 -π/2·NIR₁R₂² 已手工推导验证,正确。本章未发现确认错误。
12.【radiation.tex L369 与 L250】L369(良导体球 α=-(2i/3)(kR)³(1-(3/2)(1+i)δ_c/R))经数值验证正确(误差 1.7%),与修正后的 L250-251 一致。

---

## 三、叙述与体系问题(仅建议,未修改)

1.【radiation.tex L366-369】δ 平方积分约定 ∫(δ(ω-mΩ))²f dω = fT/(2π) 突然引入,无任何解释(δ 函数平方本无意义,这是周期能量归一化的非常规约定)。建议补一段说明其来源与适用范围。
2.【radiation.tex L393-401】连续化近似(Σ_m f(m)δ(ω-mΩ) → (1/Ω)f(ω/Ω),即 L399-401)缺少推导,建议说明 δ 峰间距 Ω 的物理与"单周期能量"的关系。
3.【radiation.tex L1059】穿越辐射小节开头直接"将上面求出的电荷电场记为 E",缺少"为什么研究穿越辐射/物理动机"的引入段。
4.【radiation.tex L558】二体辐射三个算例前缺少过渡(为何讨论经典开普勒辐射、与天体物理的联系),虽有 notes 提及引力波,建议在开头加动机。
5.【scattering.tex L424】"由于电磁场是实数,必然有 a_m = a_{-m},b_m = b_{-m}"——物理陈述错误:实场要求 a_{-m} = a_m*(共轭),除非系数全实。该条件后文未使用,建议修正表述或删除。
6.【scattering.tex L63】Mie 散射入射平面波的 VSH 展开(L79-81)前缺动机(为何能这样展开、A_+/A_- 参数化的意义),建议补充。
7.【scattering.tex L419】圆柱部分"令 k_{z,n}=0"后直接给出展开式,缺"TE/TM 解耦"的证明性说明(仅有断言)。
8.【stf_multipole_expansion.tex L6-41】指标分配符号/Λ 算符体系非常抽象,无一个完整的小例子演示 STF 化的具体操作(如对二阶张量完整算一遍),可读性受影响。
9.【stf_multipole_expansion.tex L180-244】STF 化步骤的"求和重排"(L222 的恒等式)缺少动机说明,读者难以跟上。
10.【radiation.tex L461-555】局域电荷体系部分双点乘/叉点乘在 L463-467 定义,但后续公式密集无中间解释,建议在 L504-505(电磁势)与 L519-525(电磁场)之间加"各项来源"的注释。
11.【radiation.tex L87-97】由 VSH 展开到功率公式(L89-95)之间缺一步"远场近似说明"(为何 (1/r) 项主导、E 与 H 关系),建议补充。

---

## 四、检查结论

- radiation.tex:修改 6 处(主要 3:缺 β、缺 i、角动量量纲;次要 3);存疑 7 项。
- scattering.tex:修改 5 处(主要 4:系数 3 倍、α/β 配对、κ_e/κ_m、经典公式;次要 1);存疑 3 项。
- stf_multipole_expansion.tex:未修改(未发现确认错误);存疑 2 项;关键系数(L385-386, L402)已数值/推导验证正确。

建议:修改后运行 xelatex 编译验证无语法错误。

---

# 电学其余四章审核结果(亲自审核)

审核方式:逐章通读 + 量纲分析 + Python(scipy/mpmath)数值验证关键公式。
修改原则:明确错误直接修改;能确定正确形式的也修改;存疑项记录不改。

## electrostatics.tex(静电学)

### 已修改
- [L552] 磁偶极矩系数错误:文本"等效磁偶极矩为 4πa³B₀/μ"→ 2πa³B₀/μ。
  理由:球面电流 K = (3B₀/2μ)sinθ û_φ 的磁偶极 m = ½∫r×K dS = 2πa³B₀/μ(与 A_φ = B₀a²r_</r_>² 的偶极远场 A_φ = μ₀m/(4πr²) 一致);均匀磁化球 m = 2πB₀a³/μ 交叉验证。原文差 2 倍。
- [L614] 磁场能量公式缺 r² 因子:W_m = (4π/3)∫J_φA_φ dr → (4π/3)∫J_φA_φ r² dr。
  理由:W = ½∫J·A dV = ½·2π·(4/3)∫J_φA_φr²dr(∫sin³θdθ = 4/3),r²dr 才使量纲正确;数值验证:带 r² 的积分与 L615 闭式完全一致(4 位小数)。

### 已验证正确(数值/解析)
- 有限/无限立方电阻网公式(L24-L137):1D R(0,1)=r 精确;2D 有限网与直接解节点方程一致(比 0.999-1.000);无限网 R(1,0)=r/2、R(1,1)=2r/π 等标准值全部吻合。
- 导体椭球电容(L198):椭圆积分形式与数值积分一致(需用 F(模数,幅角) 约定)。
- 椭球四极矩(L204):数值验证 ⟨x²⟩=a²/3 型加权,公式精确。
- 圆孔电场/磁场(L325-458):Jackson 标准结果,偶极 4ε₀a³E₀/3、磁偶极 8a³H₀/3 全部正确。
- 磁场扩散例(L549-619):A_φ 闭式(L566)与积分一致(比 1.0000);J_φ(L602)、W_m(L615)闭式全部数值吻合;erf 闭式(L587-589)解析验证;一维扩散(L645-649)正确。
  注:L566 的级数在 νt 很小时不收敛(r=0.8,νt=0.1 时级数发散),属收敛域问题,非错误。

## plasma.tex(等离子体)

### 已修改
- [L270] b̂·ε 矩阵表示错误:[[0,i,0],[-i,0,0],[0,0,0]] → [[0,1,0],[-1,0,0],[0,0,0]]。
  理由:与 L40 定义(û_b·ε = û_e1û_e2-û_e2û_e1)一致;原文带 i 使 ε_xy 为实数,违反无耗散 Hermitian 要求(ε_xy 必须纯虚);L102 的 ε_r 结构经 L97 数值验证正确。
- [L478] λ_De 关系颠倒:λ_De = √(ZT_i/T_e)·λ_Di → √(ZT_e/T_i)·λ_Di。
  理由:λ_De²/λ_Di² = (T_e/n_ee²)·(n_eZe²/T_i) = ZT_e/T_i。
- [L487] Langmuir 色散虚部:符号反 + 缺 ω 因子:-i·2√πω_pe²/(k³v_the³) → +i·2√πω_pe²·ω/(k³v_the³)。
  理由:从 Z 函数渐近 1+ζZ ≈ -1/(2ζ²)+i√πζe^{-ζ²} 推导,虚部必须带 ω;符号由标准阻尼率 γ = -√πω_p⁴/(k³v³)e^{-...} 交叉验证。
- [L491] Langmuir 频移系数:3k²v_the²/(2ω_pe²) → 3k²v_the²/(4ω_pe²)。
  理由:ω = ω_p√(1+3k²v²/(2ω²)) → ω/ω_p ≈ 1+3k²v²/(4ω_p²);数值:根 ωr = 42.93047,文中形式给出 42.9807,修正形式 42.9303 ✓。
- [L497] 离子声波色散虚部缺 ω 因子:+i·2√πω_pi²/(k³v_thi³) → +i·2√πω_pi²·ω/(k³v_thi³)。
- [L501] 离子声波阻尼 1/2 因子多余:删除 -i√π/2 → -i√π。
  理由:数值解复数色散方程:根 ω = 0.33899-0.004081i;无 1/2 版本阻尼 = 0.01225ω₀(误差 0.3%),带 1/2 版本差 2 倍。

### 存疑(未修改)
- [L341] 垂直传播色散 1-k²c²/ω²-∑(ω_p²e^{-κ}/ω)∑I_n/(ω-nΩ) = 0:纵波(ε_zz = 0)与横波(ε_yy = n²)的结构混淆。正确纵波无 k²c²/ω² 项;正确普通波(ε_yy = n²)分子应为 n²I_n+2κ²(I_n-I'_n) 且带 1/κ 系数。数值验证两个恒等式均不成立。
- [L345] 两个括号相乘 = ±∑... 形式:ε_xz 在 k∥=0 时 ∝ k∥ → 0,右侧 ± 项应为零;且 ε_xx·(ε_yy-n²) ≠ ±(...)²(数值验证)。建议改为 ε_xx(ε_yy-n²)ε_zz = 0 的因式分解。

## thin_film.tex(介质膜)

### 未发现问题
- 光学部分:转移矩阵(L48-76)、四分之一波长闭式(L183-243,含 N 奇偶、!! 记号)、菲涅尔公式(N=0)、FP 腔(N=1)全部解析验证正确。
- 弹性部分:应力张量、P/SV/SH 波矩阵、能量守恒(L462/L467)、流体端闭式解(L624-627)数值验证与直接解方程组完全一致,能量守恒精确为 1。

## waveguide.tex(波导与谐振腔)

### 已修改
- [L153] 圆孔等效电偶极积分元缺 ρ:∫(û_ρ·E)ρdρdφ → ∫(û_ρ·E)ρ²dρdφ。
  理由:积分结果 πE₀a²/2 与声称值 4a³E₀/3 量纲都不一致;带 ρ² 时 ∫E_ρρ²dρdφ = 4E₀a³/3(∫₀^aρ³/√(a²-ρ²)dρ = 2a³/3)✓。
- [L156] 同上,磁偶极积分元:m_a = 2∫û_ρ(ẑ·H)ρdρdφ → ρ²dρdφ。验证:m_y = 8H₀a³/3 ✓。
- [L310] 谐振腔能量系数错误:(1+2(pπ/(dγ))²) → (1+(pπ/(dγ))²)。
  理由:TE101 立方腔(a=b=d=1)直接积分 U = μ/4,文中形式给 3μ/8,修正形式 μ/4 ✓;TM 的 (1+δ_p0) 处理 p=0 的 ∫cos² 积分,保留。
- [L373] 谐振腔本征值修正系数错误:-i(4Z_s/(dωε)) → -i(4εωZ_s/d)。
  理由:从 L366 微扰公式严格推导(1/f = -iγ²Z_s/(ωμ),γ²/(ωμ) = εω/(1+(pπ/(dγ))²));与能量法 α = 2Re(Z_s)/(μd)B 交叉验证:γ²-γ⁰² = -2iμεωα = -4iεωZ_sB/d;原文缺 (εω)² 因子。L381 的 α 与能量法一致,故 L373 错。
- [L862/L863/L864] 介质波导 H_t 展开符号错误(4 处):
  - x>a:x̂ 项 -(i/β)k(...) → +(i/β)k(...)
  - |x|<a:ŷ 项 +(ω/c)n₁²(...) → -(ω/c)n₁²(...)
  - x<-a:x̂ 项 +(i/β)k(...) → -(i/β)k(...);ŷ 项 +(ω/c)n₂²(...) → -(ω/c)n₂²(...)
  理由:从 H_t = (1/γ²)(∇_t∂_zH_z + iε₀n²ωẑ×∇_tE_z) 严格推导;修正后四个边界连续方程均给出 B/A = (-1)^{m+1},与 L869/L870 的 TE/TM 本征方程精确一致;原文符号给出非 ±1 的相位因子(仅模为 1),与 L869/L870 矛盾。E_t 展开(L850-853)经验证全部正确,未改动。

### 已验证正确
- 横向-纵向分解、边界条件、TM/TE 场与归一化(L32-L98)、圆孔 notes(L146-148,与静电章节一致)、非理想边界微扰结构(L204-L250 的 ξ/η 结构因子)、矩形/三角/圆柱截面结构因子(L471-L569,数值抽查)、球形谐振腔(L591-641,含薄腔极限)、Schumann 共振(L662-667)、相/群速度公式(L753-775)、平板波导功率 L875/L880(用 TE 本征方程化简后与推导一致)。

---

# 物理审核报告:统计力学与光学五章(系数/物理错误)

审核范围(SI 单位制):bose_fermi_gas.tex、ising_model.tex、crystal_optics.tex、fourier_optics_4f.tex、matrix_optics.tex。
方法:量纲分析 + Python(scipy/sympy)数值验证(恒等式、高温/低温极限、边界条件、直接积分 vs 级数)。
已按要求直接修改明确错误;**存疑项未修改**。

---

## 一、已修改清单(7 处,全部经数值验证)

### 1. bose_fermi_gas.tex 行 622-624 — χ_m 缺因子 1/3(系数)
- 原文: `\chi_{m} = \frac{n\mu_{q}^{2}}{kT} \left(J(J+1)g_{J}^{2}-1\right) \frac{\Phi_{d/2-1}(z)}{\Phi_{d/2}(z)}`
- 改后: `\chi_{m} = \frac{n\mu_{q}^{2}}{3kT} \left(J(J+1)g_{J}^{2}-1\right) \frac{\Phi_{d/2-1}(z)}{\Phi_{d/2}(z)}`
- 理由: 由前式 M = (2J+1)/(3λ^d)(J(J+1)g_J²−1)βμ_q²B Φ_{d/2−1}(z)(该式含 1/3 且正确),χ = ∂M/∂B = (n/3)(J(J+1)g_J²−1)βμ_q²Φ_{d/2−1}/Φ_{d/2}。经典极限检验:z→0 时 Φ_{d/2−1}/Φ_{d/2}→1,对 J=1/2, g_J=2 应为 χ = (2/3)nμ_q²/kT(Curie 顺磁 nμ_q²/kT 与 Landau 抗磁 −(1/3)nμ_q²/kT 之和),原文给出 3 倍于此的 2nμ_q²/kT。
- 严重程度: 主要

### 2. ising_model.tex 行 233 — q=2 链能量公式缺 2e^{−4γ}/S 项(系数)
- 原文: `\frac{E}{NJ} = \frac{\sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \left( -\cosh\tilde{h} + \sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \right)}{\sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \left( \cosh\tilde{h} + \sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \right)}`
- 改后: `\frac{E}{NJ} = -\frac{\sqrt{e^{-4\gamma}+\sinh^2\tilde{h}}\,\cosh\tilde{h} + \sinh^2\tilde{h} - e^{-4\gamma}}{\sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \left( \cosh\tilde{h} + \sqrt{e^{-4\gamma}+\sinh^2\tilde{h}} \right)}`
- 理由: E/NJ = −(p_++ + p_−− − 2p_+−),代入本文 p_++/p_−−/p_+− 公式得 −(S cosh h̃ + sinh²h̃ − e^{−4γ})/(S(cosh h̃+S))。数值检验(γ=0.5, h̃=0.3):原文 −0.3728,正确值 −0.62783(与传递矩阵精确 ⟨σ_iσ_{i+1}⟩ = 1 − 2e^{−4γ}/(S(cosh h̃+S)) 一致)。两者仅在 h̃=0 时相同(均 = −tanhγ),h̃≠0 时原文漏掉 2e^{−4γ}/S 项。
- 严重程度: 主要

### 3. crystal_optics.tex 行 660-666 — i=0 特殊情形 θ_r 的 (n_o/n_e) 应为 (n_o/n_e)²,并连带修正 t_R、t_R'、T_R、T_R'(系数)
- 原文(行 660): `\theta_r' = -\theta_r = -\xi + \arctan\left( \dfrac{n_o}{n_e} \tan\xi \right)`
- 改后(行 660): `\theta_r' = -\theta_r = -\xi + \arctan\left( \dfrac{n_o^2}{n_e^2} \tan\xi \right)`
- 行 662-663 原文 t_R = 2n(n_e²cos²ξ+n_o²sin²ξ)/((n_ecos²ξ+n_osin²ξ)(n_on_e+n√(...))) 等改后为(以 √A = √(n_e²cos²ξ+n_o²sin²ξ), √B = √(n_e⁴cos²ξ+n_o⁴sin²ξ)):
  - t_R = t_L = 2n√A·√B/((n_e²cos²ξ+n_o²sin²ξ)(n_on_e+n√A))
  - t_R' = t_L' = 2n_on_e(n_e²cos²ξ+n_o²sin²ξ)/(√B(n_on_e+n√A))
  - T_R = T_L = 4n_on_en·√A·√B/((n_e²cos²ξ+n_o²sin²ξ)(n√A+n_on_e)²)
  - T_R' = T_L' = 4n_on_en·√A(n_e²cos²ξ+n_o²sin²ξ)/(√B(n√A+n_on_e)²)
  (行 661、664 的 r_R、R_R 原本正确,未动)
- 理由: 精确 e 光能流方向给出 tanθ_r = (v₁²−v₃²)sinξcosξ/(v₃²+(v₁²−v₃²)cos²ξ)(θ_N=0 时),即 θ_r = ξ − arctan((n_o²/n_e²)tanξ);原文用 (n_o/n_e) 得 2.02° 而正确值为 3.82°(数值:θ_N=0 时 S 矢量计算 0.0668 rad)。边界条件 (E_i−E_r)cos i = E_t cosθ_r、n(E_i+E_r) = n_N E_t cos(θ_r−θ_N) 在 i=0 给出 t_R = 2n√A/(cosθ_r(n_on_e+n√A)) 等,代入 cosθ_r = (n_e²cos²ξ+n_o²sin²ξ)/√B 即得上式。数值验证(n=1, ξ=17°, n_o=1.4, n_e=1.6):改后 t_R=0.83027(原文 0.8289)、t_R'=1.16897(原文 1.1709)、T_R=0.97273(原文 0.9712)、T_R'=0.96840(原文 0.9700),与边界条件精确解一致。注意:ξ=0、ξ=π/2 两个特殊情形已逐项数值验证,全部正确,未修改。
- 严重程度: 主要(数值差约 0.16%,但为系统错误)

### 4. fourier_optics_4f.tex 行 163、174、191、205 — 频谱公式多出 (2π)² 因子(系数)
- 行 163 原文: `\sum_{h,l} \frac{(2\pi)^2}{A_c} \tilde{W}(\vb{\kappa} - \vb{G}_{hl})` 改后: `\frac{1}{A_c} \tilde{W}(\vb{\kappa} - \vb{G}_{hl})`
- 行 174 原文: `\frac{L_1 L_2}{A_c} \sum (2\pi)^2 \sinc(...)\sinc(...)` 改后去掉 `(2\pi)^2`
- 行 191 原文: `\frac{(2\pi L)^2}{d^2}` 改后: `\frac{L^2}{d^2}`
- 行 205 原文: `\frac{2 (2\pi L)^2}{\sqrt{3} d^2}` 改后: `\frac{2 L^2}{\sqrt{3} d^2}`
- 理由: U_o = u_o*(W·amalg),amalg = Σδ(r−R_mn) = (1/A_c)Σe^{iG·r}(该傅里叶级数展开不含 2π 因子),故 Ũ_f = Ũ_f^unit·(1/A_c)ΣW̃(κ−G)。泊松求和公式 Σ_{mn}f(R_mn) = (1/A_c)Σ_hl f̂(G_hl) 在 f̂(κ) = ∫f e^{−iκ·r}dr 约定下也不含 (2π)²。数值验证:点孔 + 10×10 窗口在任意离轴 κ 处直接求和 Σe^{−iκ·R} 与 (1/A_c)ΣW̃(κ−G) 一致(比值 1.002,截断误差),与 (2π)²/A_c 版差 39.5 倍(=(2π)²)。
- 严重程度: 致命(整体缩放因子错误)

### 5. fourier_optics_4f.tex 行 195 — 立方密排峰值位置缺 π(系数)
- 原文: `\kappa_x=\frac{2h}{d},\quad \kappa_y=\frac{2l}{d}` 改后: `\kappa_x=\frac{2\pi h}{d},\quad \kappa_y=\frac{2\pi l}{d}`
- 理由: 峰值处 sinc 自变量为零:κ_xL₁/2 = πhL₁/d → κ_x = 2πh/d,即 κ = G_hl = (2π/d)(h,l);原文的 2h/d 与自身的 sinc 表达式(行 191)矛盾。
- 严重程度: 主要

### 6. fourier_optics_4f.tex 行 209 — 六角密排峰值位置缺 π 且下标组合错误(系数/上下标)
- 原文: `\kappa_x=\frac{2h}{d},\quad \kappa_y=\frac{2(-l+2h)}{\sqrt{3}d}`
- 改后: `\kappa_x=\frac{2\pi h}{d},\quad \kappa_y=\frac{2\pi(-h+2l)}{\sqrt{3}d}`
- 理由: 峰值 κ = G_hl,由行 202 的 G_hl = (2π/d)(h, (−h+2l)/√3) 得 κ_y = 2π(−h+2l)/(√3d)。原文 (a) 缺 π;(b) (−l+2h) 与 (−h+2l) 不同(仅 h=l 时相等),为抄写/推导错误。
- 严重程度: 主要

### 7. matrix_optics.tex 行 236 — q₀ = 1/(2kω₀²) 量纲错误(量纲)
- 原文: `q_0=\dfrac{1}{2\,k\,\omega_0^2}` 改后: `q_0=\dfrac{k\,\omega_0^2}{2}`
- 理由: 由 1/ρ = 1/R + 2i/(kω²) 与 ρ = z − iq₀:Im(1/ρ) = q₀/(z²+q₀²) = 2/(kω(z)²),ω(z)² = ω₀²(1+z²/q₀²) ⇒ q₀ = kω₀²/2(Rayleigh 距离,z_R)。量纲:kω₀²/2 为长度;原文 1/(2kω₀²) 为 m⁻¹,量纲错误。数值例:k=2π/0.5μm, ω₀=1mm:正确 q₀ = 6.28 m,原文给出 0.04 m⁻¹。
- 严重程度: 致命(量纲错误,影响其后所有高斯光束公式)

### 8. matrix_optics.tex 行 375-377 — z₀₂/q₀₂ 的 f,h 形式漏掉主面位移 h、h';牛顿关系对高斯光束不精确成立(系数/结论)
- 原文: `z_{02}=\dfrac{f'\,(q_{01}^2 - z_{01}(f - z_{01}))}{q_{01}^2+(f - z_{01})^2},\quad q_{02}=\dfrac{q_{01}\,f\,f'}{q_{01}^2+(f - z_{01})^2}, \quad (z_{02}-f'-h')(z_{01}-f-h)=f\,f'`
- 改后: `z_{02}=h'+\dfrac{f'\,(q_{01}^2 - (z_{01}-h)(f - z_{01}+h))}{q_{01}^2+(f - z_{01}+h)^2},\quad q_{02}=\dfrac{q_{01}\,f\,f'}{q_{01}^2+(f - z_{01}+h)^2}` 及 `(z_{02}-f'-h')(z_{01}-f-h)=f\,f'\,\dfrac{(z_{01}-f-h)^2}{q_{01}^2+(z_{01}-f-h)^2}`;正文改为"满足修正的牛顿成像关系,在几何光学极限 q₀₁→0 下退化为牛顿成像定律"。
- 理由: 总矩阵 T(z₂)MT(z₀₁) = T(z₂−h')·M_HH'·T(z₀₁−h),故 Z₁ = z₀₁−h、Z₂ = z₀₂−h' 代入复曲率变换得 Z₂ = f'(q₀₁²−Z₁(f−Z₁))/(q₀₁²+(f−Z₁)²)。数值验证(a=1.5,b=2,c=−0.1,d=0.8,q₀₁=3,z₀₁=4):改后 z₀₂=−7.4、q₀₂=16.8 与直接 ABCD 计算完全一致;原文给 −2.844、3.853。且 (Z₂−f')(Z₁−f) = ff'(Z₁−f)²/(q₀₁²+(Z₁−f)²),牛顿定律仅当 q₀₁→0 时成立(数值:89.6 vs ff'=140)。
- 严重程度: 主要

---

## 二、存疑项(未修改)

### A. crystal_optics.tex 行 609-611 — 数值表中 "R_L" 标注疑为 R_L' 之误,且 t_L 数值与行 584 公式不自洽(上下标/结论)
- 行 609: "r_L' = −0.16785, **R_L** = 0.028432, t_L' = 1.1675, T_L' = 0.96970" — 0.028432 恰为 R_L'(由 r_L'²·n_N'cos(θ_r'−θ_N')/(n_Ncos(θ_r−θ_N)) 算得),该组量的正确标签应为 R_L'。
- 行 610: t_L = 0.82442;而行 584 公式 t_L = (cosθ_r/cosθ_r')t_R 给出 0.82880。0.82442 与 T_L = 0.96407(已验证正确)按能流关系 T_L = t_L²·n_N'cos(θ_r'−θ_N')/n 自洽(0.96433),而 0.82880 不自洽;但行 584 的推导(i→−i 替换)又似乎给出 0.82880。两者矛盾,无法确定哪一个是笔误,未修改。
- 其余 12 个数值(R_R、T_R、R_L、T_L、R_L'、T_L'、R_R'、T_R' 及所有振幅)均与公式精确一致。

### B. bose_fermi_gas.tex 行 292-293 — 零温 μ、E 的 T² 项系数 (7ln2−1)(存疑)
- μ 的 T² 修正 −(π²/12)(kT)²/ε_F·(16J/5π²)(7ln2−1)(k_Fa)² 与 E 的 T² 修正 (16J/15π²)(7ln2−1) 经代数链(主公式→ln z 展开→Sommerfeld 展开)与 F(z) 渐近(行 298)自洽,且 (7ln2−1) 组合与文献一致;但行 298 的次领头系数 (35/8)(2ln2−1)/(11−2ln2) 未能独立数值验证(级数在 z>1 发散,需解析延拓),故整条链的次领头项未完全独立确认。

### C. ising_model.tex 行 147-149 — E、C 公式(存疑度低,倾向正确)
- E/NkT_c 与 C/Nk 表达式与数值导数一致(t=±0.01 处 C 公式与数值微分精确吻合),自由能展开系数 a₂、b₁、c₀ 与精确 Φ 数值展开一致(0.05% 内),判为正确,未修改。

---

## 三、已检查确认正确的重点内容(数值验证)

- bose_fermi_gas.tex:行 90 恒等式、行 198 sinh 积分恒等式(4 组参数比值 1.000000)、G(z)/F(z) 的 (1,1,1) 系数(976.673 = (8π)^{3/2}π³/4,与级数一致)、(k+l)(j+l) 与 (j+k)(j+l) 分母等价(j↔l 换标号)、F(z) 零温领头系数 (16/105)(11−2ln2)/π^{3/2}(经链式推导与文献 μ 系数 4(11−2ln2)/15π² 互证)、零温 μ/E 系数与文献一致、Landau 能级巨势闭式与直接求和逐项一致、E 与 ln z 的二阶展开代数正确。
- ising_model.tex:Bethe 自洽解、p₁₂ 变分公式、χ、E/C、自由能展开、q=2 精确解(m、χ̃、p 全部)、平均场 Q 矩阵与 p 公式(自洽条件下)、B-W 部分全部正确。
- crystal_optics.tex:双轴光轴、单轴 o/e 波全部公式、Fresnel 一般公式及行 605-612 数值、Δφ 两种形式、小 δ 展开、ξ=0 与 ξ=π/2 特殊情形全部正确。
- fourier_optics_4f.tex:卷积定理、多边形/三角形孔公式、倒格矢、窗函数、挡零级滤波全部正确。
- matrix_optics.tex:主面/节点公式、双/三/四透镜矩阵元(sympy 精确验证)全部正确;R₂/ω₂² 变换与 q₀₂/z₀₂ 直接形式正确。

---

## 四、总结

共发现 **8 处问题(已修改 8 处)**,其中:致命 2(傅里叶 (2π)² 因子、q₀ 量纲),主要 5(χ_m 1/3、Ising E、晶体 i=0、傅里叶峰值 ×2),另有 2 处存疑(晶体数值表标注、F(z) 次领头项)。全部修改经 xelatex 编译通过(45 页,无错误),且每处修改均经数值复核与原文公式一致。

---

## 五、叙述与体系问题(建议,未修改)

> 说明:以下为叙述完整性/知识体系审查结果,只记录建议,未修改文件。严重程度分为"影响理解主线"(缺一步推导读者就无法继续)与"小瑕疵"(可读性/过渡问题)。

### bose_fermi_gas.tex

1. 【bose_fermi_gas.tex 行 5-21】缺少散射理论前置:开头直接给出硬球散射的分波解 ψ_lm = C_lm(j_l − tanδ_l·n_l)Y_lm 与相移 δ_l,默认读者熟悉分波展开、相移概念及低能散射长度关系(ka≪1 时 tanδ₀≈−ka)。建议:开头补一段"硬球势与赝势的动机"(为何低能 s 波主导、为何用赝势替代硬球势),或补出 ka≪1 极限 δ_l 的推导。——影响理解主线

2. 【bose_fermi_gas.tex 行 28-30】"不难证明"的积分 ∫_{Vε} r^l(∇²−l(l+1)/r²)n_l(kr)d³r = 4π(2l+1)!!/k^{l+1} 决定赝势强度,是关键一步,直接给出结果。建议:补出分部积分/边界项论证。——影响理解主线

3. 【bose_fermi_gas.tex 行 84-98】配分函数二阶微扰展开(Q_N^{(2)}、Ξ^{(2)}、R 算符)直接出现:一阶(平均场)与二阶(关联修正)的物理意义未说明,Σ_{p,q,s} H₀^p H₁ H₀^q H₁ H₀^s 的组合计数也未解释。建议:补一段"为何需要二阶"的动机,并解释 R 算符 = (1−δ_rs)/(E_r−E_s) 即能量分母的由来。——影响理解主线

4. 【bose_fermi_gas.tex 行 131-149】自旋简并因子 g(g+1)、g(g−1)、g(g+1)²、2g(g+1) 等结论直接列出,只给一句"s 波空间波函数对称"的推理。建议:补出两粒子自旋对称/反对称态的计数(对称态 g(g+1)/2 个、反对称态 g(g−1)/2 个)推导。——影响理解主线

5. 【bose_fermi_gas.tex 行 172-177】二体碰撞三类((1,2)→(3,4)、(1,1)→(2,3)、(1,2)→(3,3))的划分与"四个及两个 ⟨n⟩ 项的求和为零"的对称性论证只有一句。建议:补出对称性论证(交换初末态、1/(q²−p²) 的奇性/主值),或至少提示可验证。——影响理解主线

6. 【bose_fermi_gas.tex 行 268-280】E、ln z 的二阶展开结果突然出现,中间过程("按照 a/λ 的幂次展开,保留到二阶项")未展开;z₀ 的定义(行 282-288)在结果之后。建议:先定义 z₀,再补出由 N = z∂lnΞ/∂z 固定粒子数消去 z 的一两步提示。——影响理解主线

7. 【bose_fermi_gas.tex 行 290-299】零温极限:F(z) 的 Sommerfeld 渐近直接给出,未说明级数 Σ(−1)^{j+k+l−1}z^{j+k+l}/D 在 z>1 发散、须取解析延拓(本节最易误解处);μ、E 修正公式也是直接列出。建议:补一句"此处 F(z) 取级数的解析延拓",并说明 Sommerfeld 代入的要点。——影响理解主线

8. 【bose_fermi_gas.tex 行 462-532】"占据数平均值的计算"一节放在硬球修正计算之后,但行 163、169 已用到 Σ(⟨n²⟩−⟨n⟩²) ≈ (V/λ³)g_{1/2}(z) 等结果(工具先于推导使用)。建议:将该节前移,或在行 163 处加交叉引用。——小瑕疵

9. 【bose_fermi_gas.tex 行 565-590】Landau 能级巨势密度闭式:从定义式到 (sβμ_qB/sinh(sβμ_qB))·[sinh(sβg_Jμ_qB(J+1/2))/sinh(sβg_Jμ_qB/2)] 的 j、m_J 几何级数求和被省略。建议:补出 Σ_j e^{−sβμ_qB(2j+1)} = 1/(2sinh sβμ_qB) 与 Σ_{m_J} e^{sβg_Jμ_qBm_J} 的结果。——小瑕疵

10. 【bose_fermi_gas.tex 行 630-884】低温磁场相变分析(η、t、ν、ξ_l、S_α、B_c、f_sing、M_sing、χ_sing)是全篇最密集处:"不难给出"出现多次(行 733、759、815),η(t) 分段解、自由能奇异项、磁化率跃变等关键结论直接列出。建议:至少补出 η(t) 推导(粒子数方程在 B_c 附近展开)与 f_sing 的 (1/2)(∂²ω_R/∂μ̄²)(η−t)² 展开的中间步骤,或注明"推导较长,可另文/附录"。——影响理解主线

11. 【bose_fermi_gas.tex 行 2】章节标题"弱相互作用玻色费米气体"与内容(硬球强排斥势)表面矛盾,未解释"弱"指稀薄气体条件 a/λ≪1。建议:开头一句交代稀薄条件。——小瑕疵

12. 【bose_fermi_gas.tex 全文】公式密集且几乎全用无编号 equation* 环境,正文以"如上所求""综合以上各项"指代,读者无法定位公式;公式之间普遍缺少解释性文字。建议:关键公式改编号环境,公式后加一两句物理说明。——小瑕疵(可读性)

### ising_model.tex

13. 【ising_model.tex 行 1-4】缺少引入:直接进入"数图的熵",未说明为什么研究 Ising 模型、为什么用 Bethe 方法(精确求解困难时树图可严格解)、Bethe 近似何时成立。建议:开头补动机段落。——影响理解主线

14. 【ising_model.tex 行 5-8】树图联合分布分解 P({σ}) = Π P(σ_i|σ_π(i)) 是后续所有推导的基础,直接给出,未利用树无环性证明。建议:补一句"树上删去一条边即把图分成两个连通分量"的论证。——影响理解主线

15. 【ising_model.tex 行 93-104】自由能 Φ 的构造与稳态解:p₁₂(m,t) 与 h(m) 直接"解得",∂Φ/∂p₁₂ = 0、∂Φ/∂m = 0 的代数被省略;随后 a、γ 参数化(行 107-111)突然引入,未说明动机(化简 h 与 p 的双曲函数形式)。建议:补出 ∂Φ/∂p₁₂ = 0 的一步结果(ln[p₁₂²/(p₁₁p₂₂)] 条件),并说明"引入 a 以对角化双曲函数"。——影响理解主线

16. 【ising_model.tex 行 120】χ 公式直接给出,无推导(∂m/∂a 与 ∂h/∂a 之比)。建议:补一行推导或注明可验证。——小瑕疵

17. 【ising_model.tex 行 82-84、129-133】T_c 引入时说"后文将证明",但证明只有 (q−1)tanhγ = 1 ⟹ t = 0 一行,且"临界点对应磁化率发散"的判据未解释。建议:补一句"χ⁻¹ ∝ 1−(q−1)tanhγ,发散处即临界点"。——小瑕疵

18. 【ising_model.tex 行 147-149】C 最终表达式中分母 [cosh(2a) + (q−1)sinh²(2a)/(cosh(2a)+cosh(2γ)−(q−1)sinh(2γ))] 来源未交代(来自隐函数求导 da/dγ)。建议:补出 dE/dγ 中 da/dγ 的求导步骤。——影响理解主线

19. 【ising_model.tex 行 178-190】自由能展开系数 a₀、a₁、a₂、b₁、c₀ 直接"展开得",无过程。建议:补出 Φ 对 m 展开的一两步,或至少给出 a₂、b₁、c₀ 各自来源的提示。——影响理解主线

20. 【ising_model.tex 行 220-234】q=2 极限:ln(q/(q−2)) → ∞ 的处理、arcsinh 公式与 p_++ 等表达式的来源未说明。建议:补一句"q=2 时 T_c=0,以 γ=J/kT 为参数直接解自洽方程"。——小瑕疵

21. 【ising_model.tex 行 238-239】"Bethe 方法与平均场方法给出等价的结果"只有一句,未解释(给定中心自旋后邻居独立 ⟹ 有效场图像)。建议:补一句论证。——小瑕疵

22. 【ising_model.tex 行 308-316】Bragg-Williams 近似引入 p_σσ' = p_σ p_σ' 因子化,但未说明与 Bethe 近似的本质区别(忽略关联 vs 树图精确关联)、失效条件。建议:补一句适用范围对比。——小瑕疵

### crystal_optics.tex

23. 【crystal_optics.tex 行 1-2】缺少章节动机:晶体光学的研究对象(双折射、偏振器件)未引入;双各向异性(手性/磁电介质)缺少物理例子。建议:开头补"为什么研究"与典型材料例子。——小瑕疵

24. 【crystal_optics.tex 行 28-33】损耗功率密度 p_abs 的矩阵形式直接给出,(ε†−ε) 等组合的来源未说明。建议:补出 (H*·B − E·D*) 代入本构关系的展开。——小瑕疵

25. 【crystal_optics.tex 行 156-158】w_e = (1/2)(D·E+B·H) = μH² = D·E 的两个等号都未推导(需用平面波关系 D = −k/ω×H、H = k/(ωμ)×E 与 k·S 的恒等式)。建议:补出 D·E = (1/ω)k·S = μH² 的推导。——小瑕疵

26. 【crystal_optics.tex 行 268-292】双轴晶体光轴方向上的 D、E、H、S 矢量公式(行 275-286)与 δ = ∠(E,D) 公式(行 286)直接给出,无推导;锥形折射叙述(行 289-294)较概念化。建议:补出 E 表达式由 E_i = k̂_i v_i²/(v²−v_i²)(k̂·E) 代入光轴条件得出的一两步,δ 公式给一句来源。——影响理解主线

27. 【crystal_optics.tex 行 307-309】单轴晶体 v'、v'' 公式"通过 δ 取极限得"含糊(ε₂→ε₁ 的取极限过程未写)。建议:明确写出取极限步骤,或直接给无 δ 的推导。——小瑕疵

28. 【crystal_optics.tex 行 419-451】θ_N 显式解与 r_R、t_R 解都是"解得",代数完全省略(折射定律二次方程求解、边界条件联立)。建议:补出关键一步(如 n_N 代入 Snell 定律后的化简),或注明代数细节。——影响理解主线

29. 【crystal_optics.tex 行 509-512】"计算中用到关系式"的恒等式(cosθ_r sinθ_N/cos(θ_r−θ_N) = ...)直接给出,无推导。建议:补出由折射定律与 tanξ 关系推出的步骤。——小瑕疵

30. 【crystal_optics.tex 行 534-563】斯托克斯关系消光论证较简略:"该情形可消光,则 r_R r_L + t_R t_L' = 1" 的物理含义(消光 ⟹ 反向入射无反射)未解释。建议:用一两句说明消光条件如何导出方程。——小瑕疵

31. 【crystal_optics.tex 行 605-612】算例数值表后无任何讨论(读者无法判断数值合理性及量间关系)。建议:加一句验证说明(能量守恒、斯托克斯关系)。——小瑕疵(可读性)

### fourier_optics_4f.tex

32. 【fourier_optics_4f.tex 行 5-25】数学概念部分与 4f 系统未建立联系(为何定义矩形/圆孔特征函数);傅里叶变换正/逆约定未统一给出(e^{ikx} 与 e^{−i2πfx} 两种形式并存)。建议:先给出本章统一变换定义(含 1/(2π) 约定),再列矩形/圆孔结果。——影响理解主线

33. 【fourier_optics_4f.tex 行 57-61】全章最重要的知识跳跃:核心公式 U_f = (1/λf)∫∫U_o e^{−i(2π/λf)(xx_f+yy_f)} 直接给出,"对球面波因子进行傍轴近似、忽略轴向传播因子"一句带过,透镜焦平面的傅里叶变换性质未推导。建议:补出从菲涅尔衍射积分到焦平面变换的推导,或至少给参考。——影响理解主线

34. 【fourier_optics_4f.tex 行 122-125】N 边形孔公式"用二维高斯定理不难证明"跳步,且两种等价形式(L_j·x̂/κ·ŷ 与 L_j·ŷ/κ·x̂)的等价性未说明。建议:补出格林定理一步 ∫∫e^{−iκ·r}d²r = (i/κ²)∮e^{−iκ·r}κ·n̂ dl。——影响理解主线

35. 【fourier_optics_4f.tex 行 147-150】梳状函数傅里叶展开 Σδ(r−R_mn) = (1/A_c)Σe^{iG·r} 直接给出,无推导。建议:补一句"由倒格矢定义可验证(泊松求和)"。——小瑕疵

36. 【fourier_optics_4f.tex 行 214-236】频谱模拟部分:几何参数列表与模拟图之间没有说明离散傅里叶变换与连续公式的对应(采样、窗口、混叠),也未与理论公式(行 191、205)数值对比。建议:补一段模拟设置说明。——小瑕疵

37. 【fourier_optics_4f.tex 行 346-366】挡零级滤波:h(x,y) 中 δ 函数项的来源直接给出;滤波后"边界外仍有较暗光场"解释较简略。建议:补一句 δ 项来源(1 的傅里叶变换)与卷积展宽的说明。——小瑕疵

### matrix_optics.tex

38. 【matrix_optics.tex 行 3-19】核心假设"任意理想光具组可由 2×2 矩阵表示"直接给出,未说明傍轴近似的来源与矩阵元意义(a 放大率、b 与焦距联系等预告)。建议:开头补一句"傍轴下光线坐标线性演化"的动机,并与行 56-121 主面/节点定理呼应。——影响理解主线

39. 【matrix_optics.tex 行 30-51】球面折射矩阵、薄透镜矩阵直接给出,无推导。建议:补出球面折射的几何推导或注明结果来源。——小瑕疵

40. 【matrix_optics.tex 行 128-221】双/三/四薄透镜矩阵元:三、四透镜的 a、b、c、d 元素直接列出,无推导过程,属纯公式堆砌;且未说明这些结果的用途(后续高斯光束变换只用一般 a,b,c,d)。建议:补出三透镜矩阵乘法的推导或移入附录,并说明"此节为矩阵乘法练习,后文只需一般形式"。——影响理解主线(可读性)

41. 【matrix_optics.tex 行 223-237】高斯光束 U(r,z)、ω(z)、R(z)、φ(z) 直接给出,无推导(傍轴波动方程 → 高斯解);q₀ 的物理意义(瑞利距离,束腰到 ω=√2ω₀ 处)未说明。建议:补一段"从傍轴亥姆霍兹方程到高斯解"概述,并解释 q₀ 物理意义。——影响理解主线

42. 【matrix_optics.tex 行 296-317】"代入得到"R₂、ω₂² 公式:从 1/ρ₂ = (c'ρ₁+d')/(a'ρ₁+b') 分离实虚部的代数被跳过。建议:补出分离实虚部的一两步。——小瑕疵

43. 【matrix_optics.tex 行 350-362】q₀₂、z₀₂ 的引入("注意到,若记...则")未说明如何从 R₂、ω₂² 反解。建议:补一句"比较 ω₂² 与 R₂ 对 z₂ 的依赖即可反解"。——小瑕疵

44. 【matrix_optics.tex 行 366-378】f,h 形式一节动机不足:引入焦距/主面的目的(联系光具组参量)未说明。建议:补一句"这些量可由矩阵元直接读出,便于物理解释"。——小瑕疵

### 跨章衔接

45. 【Statistics 章】BoseFermiGas 与 IsingModel 两文件间无交叉引用或顺序说明(量子统计 vs 经典格点统计,方法完全不同)。建议:在章首或两文件开头加导言说明关系。——小瑕疵

46. 【Optics 章】CrystalOptics、FourierOptics4F、MatrixOptics 三文件相互独立,无交叉引用(如 MatrixOptics 的 ABCD 方法可给出 4f 系统透镜矩阵;FourierOptics 的透镜变换与 MatrixOptics 薄透镜矩阵同源)。建议:在文件开头加一句衔接。——小瑕疵

---

## 六、总结(叙述与体系)

叙述完整性方面:**matrix_optics 透镜矩阵元部分(行 128-221)与 bose_fermi_gas 低温磁场相变部分(行 630-884)是公式堆砌/跳步最严重的两处**;fourier_optics 的 4f 核心变换公式缺少推导(行 57-61)是最大的单点知识跳跃;crystal_optics 与 ising_model 的代数跳步("解得""不难证明")较多但主线推导基本完整。所有章节普遍缺少"为什么研究这个问题"的引入,公式后缺少解释性文字。上述 46 条均为建议,未修改文件。

---

# MathTool 数学审核报告(2026-08-04)

范围:chapters/MathTool/ 下 8 个 TeX 文件全部通读;关键公式用 mpmath/scipy 数值验证。
结论:**共发现 16 处错误,全部已直接修改文件(主要 15 处、次要 1 处);存疑未修改 1 处。**
修改后 8 个文件经 xelatex 编译通过(48 页,无语法错误;仅测试环境图片路径警告)。

---

## 一、已修改清单

### 1. green_function.tex 行 324 — Legendre 级数恒等式闭式错误【主要】
- 原公式:`\sum_{l=1}^\infty\frac{t^{l+1}}{l}P_l(\mu)=\ln\frac{t-\mu+\sqrt{1-2\mu t+t^2}}{1-\mu}`
- 改后:`\sum_{l=1}^\infty\frac{t^{l+1}}{l}P_l(\mu)=t\ln\frac{2}{1-\mu t+\sqrt{1-2\mu t+t^2}}`
- 错误类型:系数/闭式错误
- 证据:t=0.5, μ=0.3 时级数和=0.045871;原 RHS=0.51767;改后 RHS=0.045871 ✓(级数=t×第二式)。原式是第二式(Σt^l/l·P_l)的错误改写。
- 修改理由:正确闭式即第二式乘以 t。

### 2. ellipsoidal_coordinates.tex 行 41 — ∫√(1+k²sinh²θ)dθ 前导系数(k²>1 分支)【主要】
- 原公式:`\dfrac{\sinh\varphi\cosh\varphi}{\sqrt{1+k^2\sinh^2\varphi}}`
- 改后:`\dfrac{k^2\sinh\varphi\cosh\varphi}{\sqrt{1+k^2\sinh^2\varphi}}`
- 错误类型:系数
- 证据:φ=0.5, k=2 直接积分=0.577155;原公式=−0.792239;补 k² 后=0.577155 ✓。另一检验点(k=1.5, φ=0.9)亦匹配。
- 修改理由:由 k²≤1 分支经虚模变换 E(iκ,·) 解析延拓,k² 因子来自前导项 tanhφ√(1+k²sinh²φ)+k'²tanhφ/√(...) 的合并。

### 3. ellipsoidal_coordinates.tex 行 43/46 — ∫√(1+k²sinh²θ)dθ 的 arcsin 参数(k²>1 分支)【主要】
- 原公式:`\arcsin\!\dfrac{k\,\tanh\varphi}{\sqrt{1+\tanh^2\varphi}}`
- 改后:`\arcsin\!\dfrac{k\,\tanh\varphi}{\sqrt{1+(k^2-1)\tanh^2\varphi}}`
- 错误类型:符号/参数
- 证据:同上(与第 2 条同式,数值验证见上)。√(1+(k²−1)tanh²φ)=√(1+k²sinh²φ)/coshφ,与 F(iκ) 虚模变换一致。
- 修改理由:解析延拓 F(ik', asin(tanhφ)) 时应为 √(1+k'²tanh²φ),k'²=k²−1。

### 4. ellipsoidal_coordinates.tex 行 189-191 — 坐标恒等式缺项【主要】
- 原公式:`\xi\eta+\eta\zeta+\zeta\xi = a^{2}b^{2}c^{2}\bigl(\frac{x^{2}}{a^{4}}+\frac{y^{2}}{b^{4}}+\frac{z^{2}}{c^{4}}\bigr)`
- 改后:`a^{2}b^{2}c^{2}\bigl(\frac{x^{2}}{a^{4}}+\frac{y^{2}}{b^{4}}+\frac{z^{2}}{c^{4}}\bigr) = \xi\eta+\eta\zeta+\zeta\xi+\frac{\xi\eta\zeta(a^{2}b^{2}+b^{2}c^{2}+c^{2}a^{2})}{a^{2}b^{2}c^{2}}`
- 错误类型:系数/缺项
- 证据:a=3,b=2,c=1,ξ=0.8,η=−1.3,ζ=−3.2:LHS=5.0897,原 RHS=0.56;补项后 0.56+3.328×49/36=5.09 ✓。另一检验点亦匹配。
- 修改理由:由二阶差商展开 x²/a⁴+y²/b⁴+z²/c⁴ = (ξη+ηζ+ζξ)/(a²b²c²) + ξηζ(a²b²+b²c²+c²a²)/(a⁴b⁴c⁴) 导出。

### 5. mathieu_functions.tex 行 47 — se_{2n+2} 级数展开指数错误【主要】
- 原公式:`y = \mathrm{se}_{2n+2}(z) = \sum_{s=-\infty}^{\infty} c_{s-n} e^{2isz} = -2i \sum_{s=0}^{\infty} c_{s-n-1} \sin((2s + 2)z)`
- 改后:`y = \mathrm{se}_{2n+2}(z) = \sum_{s=-\infty}^{\infty} c_{s-n} e^{2isz} = 2i \sum_{s=0}^{\infty} c_{s+1-n} \sin((2s + 2)z)`
- 错误类型:上下标/符号
- 证据:由 y=Σ_s c_{s−n}e^{2isz} 与反对称 c_{−n−l}=−c_{−n+l} 直接展开得 2iΣ_{l≥1}c_{l−n}sin(2lz);q=0 时 se_4 应退化为 sin4z:原式系数(∝c_{−1}=0)为 0,改后系数(∝c_1=1/(2i))为 1 ✓。
- 修改理由:原式指数错位(s−n−1)且符号反;n=0 时因 c_{−1}=−c_1 恰好巧合成立,n≥1 时必错。

### 6. mathieu_functions.tex 行 96 — 特征值 q=0 极限错误【主要】
- 原公式:`a_{2n+1}(0) = b_{2n}(0) = (2n)^2`
- 改后:`a_{2n+1}(0) = b_{2n+1}(0) = (2n+1)^2`
- 错误类型:系数/下标
- 证据:a_1(0)=1(文件自身行 111 用 a_1=1+q+...);(2n)² 对 n=0 给出 a_1(0)=0,矛盾;b_{2n}(0)=(2n+2)² 已在本行前句给出,不可能又等于 (2n)²。
- 修改理由:标准结果 a_{2n+1}(0)=b_{2n+1}(0)=(2n+1)²。

### 7. mathieu_functions.tex 行 117 — 标签错误【次要】
- 原公式:`a_2 = 16 + \frac{1}{30}q^2 + \frac{433}{86400}q^4 + \mathcal{O}(q^6)`
- 改后:`a_4 = 16 + \frac{1}{30}q^2 + \frac{433}{86400}q^4 + \mathcal{O}(q^6)`
- 错误类型:标签(下标)
- 证据:与行 113 的 a_2=4+5q²/12−763q⁴/13824 重复;scipy mathieu_a(4, 0.3)=16.003004 与该式一致 ✓。
- 修改理由:该展开式即标准 a_4(q)。

### 8. supplementary_formulas.tex 行 39-40 — 玻色/费米积分第二种形式的 Γ 因子【主要】
- 原公式:`g_{\nu}(z) = -\dfrac{1}{\Gamma(\nu)} \int_{0}^{\infty} x^{\nu-2} \ln(1 - z e^{-x}) \,\d x`、`f_{\nu}(z) = \dfrac{1}{\Gamma(\nu)} \int_{0}^{\infty} x^{\nu-2} \ln(1 + z e^{-x}) \,\d x`
- 改后:`\Gamma(\nu)` → `\Gamma(\nu-1)`(两处)
- 错误类型:系数
- 证据:ν=3, z=0.5:Li_3(0.5)=0.537213;原式=−I/Γ(3)=0.268607(差因子 2);改后 ✓。f_ν(z=2) 同理(1.66828 vs 0.83414)。
- 修改理由:分部积分 ∫x^{ν−1}·z e^{∓x}/(1∓ze^{−x})dx = ∓(ν−1)∫x^{ν−2}ln(1∓ze^{−x})dx,系数 (ν−1)/Γ(ν)=1/Γ(ν−1)。

### 9. supplementary_formulas.tex 行 84 — 修正 Helmholtz 方程符号不一致【主要】
- 原公式:`(\nabla^{2} + k^{2}) G(\vb{R}) = \delta^{(d)}(\vb{R})`,G = ∫e^{iq·R}/(q²+k²)dq/(2π)^d = (1/2π)(k/2πR)^{d/2−1}K_{d/2−1}(kR)
- 改后:`(k^{2} - \nabla^{2}) G(\vb{R}) = \delta^{(d)}(\vb{R})`
- 错误类型:符号
- 证据:(k²−∇²)e^{iq·R}=(k²+q²)e^{iq·R},故该 Fourier 表示满足 (k²−∇²)G=δ;(∇²+k²) 的解应为 Hankel 型振荡解。d=1 检验:G=e^{−kR}/(2k) 满足 (k²−∇²)G=δ,而 (∇²+k²)G=−δ。
- 修改理由:与 green_function.tex 行 436-438 的 (∇²−μ²)G=δ、G=−(1/2π)(μ/2πR)^{d/2−1}K 对照,文件此处方程与解矛盾(改动最小化:只改方程)。

### 10. supplementary_formulas.tex 行 161 — ∫e^{im(ξ−αcosξ)}sinξ dξ 恒等式【主要】
- 原公式:`\int_{0}^{2\pi} e^{i m (\xi - \alpha \cos\xi)} \sin\xi \, \d \xi = -2\pi \, i^{m} J_{m}(m \alpha)`
- 改后:`= -\frac{2\pi}{\alpha} \, (-i)^{m} J_{m}(m \alpha)`
- 错误类型:系数/符号
- 证据:数值 m=3,α=0.5:−0.76610i;m=4:−0.42720;m=2:1.44392。原式给出 0.38305i / −0.21360 / 0.72196(均差 1/α 且符号/奇偶因子错)。
- 修改理由:e^{−imαcosξ}=Σ_k(−i)^kJ_k(mα)e^{−ikξ},代入后精确求值得 −(2π/α)(−i)^mJ_m(mα)。

### 11. supplementary_formulas.tex 行 162 — ∫e^{im(ξ−αcosξ)}cosξ dξ 恒等式【主要】
- 原公式:`\int_{0}^{2\pi} e^{i m (\xi - \alpha \cos\xi)} \cos\xi \, \d \xi = 2\pi \, i^{m-1} J_{m}'(m \alpha)`
- 改后:`= 2\pi \, (-i)^{m-1} J_{m}'(m \alpha)`
- 错误类型:符号
- 证据:m=4, α=0.5:数值 +0.38297i;原式 −0.38297i;改后 ✓。m=3 时 (−i)²=i² 故原式恰好在 m 奇时碰对。
- 修改理由:同第 10 条的生成函数展开。

### 12. supplementary_formulas.tex 行 163 — φ 积分恒等式的 π 因子【主要】
- 原公式:`\frac{1}{4\pi} \int_{0}^{2\pi} \frac{1 - \sin^{2}\varphi \cos^{2}\theta + \beta^{2} \cos^{2}\theta - 2 \beta \cos\varphi \cos\theta}{(1 - \beta \cos\theta \cos\varphi)^{5}} \, \d \varphi = \frac{4(1 + \sin^{2}\theta) - \beta^{2} \cos^{4}\theta (1 + 3\beta^{2})}{4 (1 - \beta^{2} \cos^{2}\theta)^{7/2}}\pi`
- 改后:`= \frac{4(1 + \sin^{2}\theta) - \beta^{2} \cos^{4}\theta (1 + 3\beta^{2})}{16 (1 - \beta^{2} \cos^{2}\theta)^{7/2}}`
- 错误类型:系数(π 因子与分母)
- 证据:β=0.3, θ=0.5:LHS=0.389900;原 RHS=4.899628(=4π×LHS);改后 RHS=0.389900 ✓,且与行 135 求和恒等式(分母 16、无 π)完全一致。
- 修改理由:该式应是行 135 的 φ 平均,应为 A/(16B)。

### 13. supplementary_formulas.tex 行 191 — 离散余弦和恒等式【主要】
- 原公式:`\dfrac{1}{l} \sum_{k=0}^{l-1} \dfrac{\cos(2\pi k m/l)}{A - \cos(2\pi k/l)} = \dfrac{1}{\sqrt{A^2 - 1}} \cdot \dfrac{(A - \sqrt{A^2 - 1})^{|m|} - (A - \sqrt{A^2 - 1})^{l - |m|}}{1 - (A - \sqrt{A^2 - 1})^l}`
- 改后:`r^{|m|}` 与 `r^{l-|m|}` 之间减号 → 加号
- 错误类型:符号
- 证据:三组参数直接求和:(l,A,m)=(7,2.5,3):0.00479616,加号变体 0.00479616 ✓、减号变体 0.00313983 ✗;(4,3,1):0.0625 vs 0.062500/0.058926;(6,1.8,2):0.067188 vs 0.067188/0.055866;(5,2.2,3):0.036614 vs 0.036614/−0.022421。
- 修改理由:加号变体为标准恒等式。

### 14. vector_spherical_harmonics.tex 行 25 — Y_lm 缺 Condon-Shortley 相位【主要】
- 原公式:`Y_{lm}(\theta, \phi) = \sqrt{\frac{(2l+1)(l-m)!}{4\pi(l+m)!}} e^{im\phi} (\sin\theta)^m \, _2F_1(-l+m, l+m+1; m+1; \sin^2\frac{\theta}{2})`
- 改后:`e^{im\phi}` 前插入 `(-1)^m`
- 错误类型:符号
- 证据:文件自身表格采用含 CS 相位约定(如 (1,1) 行 Yûr z 分量=−√(3/8π)e^{iφ}cosθsinθ → Y_11=−√(3/8π)sinθe^{iφ},与 scipy sph_harm 一致);原超几何公式给出无 CS 版本(+√(3/8π)sinθe^{iφ}),m 奇时相差 (−1)^m。数值:sin^mθ·_2F_1 = (−1)^m·P_l^m(含 CS)。
- 修改理由:使行 25 与文件其余部分(表格、行 105-127 公式,均按含 CS 验证通过)一致。

### 15. vector_spherical_harmonics.tex 行 96-101 — 基矢转换矩阵前两行互换【主要】
- 原公式:矩阵第 1 行(ûr)ê± 分量为 cosθ/√2·e^{∓iφ},第 2 行(ûθ)为 sinθ/√2·e^{∓iφ}
- 改后:两行的 ê± 系数互换(ûr 行 sinθ,ûθ 行 cosθ),ẑ 列不变
- 错误类型:上下标/符号
- 证据:ûr=sinθcosφx̂+sinθsinφŷ+cosθẑ 的 ê+ 分量 = sinθe^{−iφ}/√2(ûθ 的为 cosθe^{−iφ}/√2);用修改后矩阵重构 ûr=(0.2922, 0.5741, 0.7648) 与直接值一致。
- 修改理由:原矩阵把 ûr、ûθ 的径向角度因子写反。

### 16. vector_spherical_harmonics.tex 行 105 — X_lm 分量公式两处错误【主要】
- 原公式:`\vb{X}_{lm} = -\frac{im}{\sqrt{l(l+1)} \sin\theta} Y_{lm} \uv{\theta} + \frac{i}{2} ( e^{-i\phi}\sqrt{\frac{(l-m)(l+m+1)}{l(l+1)}} Y_{l,m+1} - e^{i\phi}\sqrt{\frac{(l+m)(l-m+1)}{l(l+1)}} Y_{l,m-1} ) \uv{\phi}`
- 改后:`-\frac{m}{\sqrt{l(l+1)} \sin\theta} Y_{lm} \uv{\theta} - \frac{i}{2} ( ... ) \uv{\phi}`(θ 分量去掉 i;φ 分量整体加负号)
- 错误类型:符号
- 证据:X=−i r×∇Y/√(l(l+1)):X_θ=+i(1/sinθ)∂_φY/√(...)=−mY/(sinθ√(l(l+1)))(无 i);X_φ=−i∂_θY/√(...)=−(i/2)[e^{−iφ}√((l−m)(l+m+1))Y_{l,m+1}−e^{iφ}√((l+m)(l−m+1))Y_{l,m−1}]/√(l(l+1))(含 CS 约定下 ∂Y/∂θ=(1/2)[...],数值验证 (1,0) 处 ∂Y_10/∂θ=−√(3/4π)sinθ ✓)。修改后 8 个 (l,m) 全部与直接计算一致;原式 θ 分量 = i×正确、φ 分量 = −正确。
- 修改理由:与文件自身表格(第 163-217 行,数值验证全部正确)保持一致。

---

## 二、未修改的存疑项

### 17. supplementary_formulas.tex 行 137-138 — f_m(U)/g_m(W) 恒等式【存疑】
- 原文:
  `\frac{1}{U^2} \int_0^1 ( \frac{m^2}{U^2\xi^2} ( \frac{J_m(\xi U)}{J_m(U)} )^2 + ( \frac{J_m'(\xi U)}{J_m(U)} )^2 ) \xi d\xi = \frac{1}{U^2} \int_0^1 ( \frac{J_m(\xi U)}{J_m(U)} )^2 \xi d\xi + \frac{1}{U^2} f_m(U) = - \frac{f_m'(U)}{2U}`(g_m(W) 同理)
- 状态:文中未定义 f_m(U)/g_m(W);数值检验(m=2, U=3.5)表明:若 f_m(U)=−U·J_m'(U)/J_m(U) 则第二个等号不成立(−f_m'/(2U)=−0.3737 ≠ LHS=0.2960);对"存在某 f_m 使两条同时成立"的一致性条件 U²LHS'−I'=−4U·LHS 也以 1.026 vs −4.144 失败。但无法确定作者的 f_m 定义与正确形式,故不改,仅存疑。

---

## 三、未发现问题的文件与内容

- **infinite_integrals.tex**:全部正确(含参级数/积分的收敛域、Cauchy 差构造、C_p 常数、p=1 边界的 m_E/M_E 条件均核对无误)。
- **parameter_estimation.tex**:全部正确(M 投影、χ²_min 期望、t 分布、双参拟合公式、σ_k/σ_b/ρ_kb/σ_{y_0} 均核对无误)。
- **spectral_deconvolution.tex**:全部正确(变分驻点、偏差/协方差、约束解、SVD、零阶 Tikhonov、广义谱分解、G 矩阵示例均核对无误)。
- **green_function.tex 其余**:1D/2D/3D 内外部 Robin 与 Dirichlet/Neumann Green 函数(含级数系数、G_N 闭式、Wronskian W、k→0 展开、Graf/加法公式、波动与热核、Kirchhoff 公式、热核 Laplace 变换)全部数值验证正确。
- **ellipsoidal_coordinates.tex 其余**:椭圆积分延拓(除第 2-3 条外)、Λ/κ_a/κ_b/κ_c、旋转对称极限、度量/体积元/Laplacian、分离变量公式全部正确。
- **mathieu_functions.tex 其余**:递推、连分式、a_m/b_m 展开(与 scipy 一致)、ce/se 展开(代入 Mathieu 方程残差 ~10⁻³,即 O(q⁴) 量级)全部正确。
- **supplementary_formulas.tex 其余**:多对数展开、d 维立体角/傅里叶变换、K_ν 渐近与 Green 函数小/大 kR 行为、Hankel 变换积分(4 条)、K 积分(7π²/144、5π²/144)、K_ν(−ix) 恒等式、Airy 型渐近 J_m/J_m' 与大求和 (7/16)(2η)^{−5/2}(1+(5/7)θ²/(2η))、Bessel 函数表格(9 行全部)、对偶积分方程解、平面周期运动积分(除第 10-12 条)、电阻网离散和(除第 13 条)全部正确。
- **vector_spherical_harmonics.tex 其余**:行 111-127 直角坐标展开(ûrY、X、ûr×X)与两个长表格(表 1 直角坐标、表 2 球坐标)全部数值验证正确;正交归一化、散度/旋度公式亦正确。

---

## 四、叙述与体系问题(只记录建议,未修改文件)

按严重程度分组:【影响理解主线】为中等以上问题(缺动机/关键推导缺失/约定冲突);【小瑕疵】为表述或衔接问题。

### A. 影响理解主线

1. 【green_function.tex 行 1-4】缺引入:直接以"在区域 Ω 中求解 Laplace 型边值问题"开始,未说明 Green 函数是什么(点源响应)、为什么有用(把边值问题化为积分表示)。建议:加一段引言(如静电学/稳态热传导背景,点源响应叠加成解的物理解释)。
2. 【green_function.tex 行 270、308】3D G_N 闭式(含 ln 项与常数 2)从级数解到闭式的求和推导完全缺失;行 318-325 虽列出 Legendre 恒等式清单,但未指明每条如何用于哪一步。建议:补充求和过程,或注明"由恒等式(二)(三)逐项求和得到"。
3. 【green_function.tex 行 888-890】d 维推迟核统一形式 G_d=H(t)/(2cπ^{(d-1)/2})χ_+^{(1-d)/2}(c²t²−R²) 与前面 Fourier-Bessel 积分的等价性没有论证,读者无法自行验证(需分布恒等式)。建议:补一段说明(或注明出处),并展示 d=2,3 的对照。
4. 【spectral_deconvolution.tex 行 1-45】缺引入:直接从直方图记号开始,未说明解谱问题是什么(由观测谱反演真实谱)、为何病态;正则化项 μ^TGμ 在行 44 出现,但其动机(小奇异值噪声放大)直到行 382 才给出。建议:开头加引言,并把"病态/噪声放大"的动机提前到正则化首次出现处。
5. 【spectral_deconvolution.tex 行 44】Q 中正则化系数写成 2G(而非 G)的约定未说明(读者到行 429 的 2G=λI 才隐约明白)。建议:首次出现时注明"因子 2 仅为记号方便,使驻点方程系数整齐"。
6. 【ellipsoidal_coordinates.tex 行 1-4】缺引入:直接定义椭圆积分,未说明椭球坐标出现在哪些物理问题(椭球体引力势、椭球导体/磁体、椭球谐振腔)。建议:加引言并给出一个具体应用例子。
7. 【ellipsoidal_coordinates.tex 行 68-99】Λ(ξ)、κ_a、κ_b、κ_c 四个积分直接定义并给出闭式,但完全没有说明它们的几何/物理含义(Λ 为椭球坐标径向长度积分;κ 与椭球引力势的三个轴分量相关)与引入动机。建议:补一段物理解释。
8. 【ellipsoidal_coordinates.tex 行 254-265】分离变量公式突然出现(Ψ=f(ξ,η,ζ)g(ξ) 的 ∇² 公式),无动机、无推导、无用途说明。建议:说明用于椭球上 Laplace/Helmholtz 分离变量,并给出公式来源(由第 217-227 行 Laplacian 直接代入)。
9. 【mathieu_functions.tex 行 1-5】缺引入:直接给出 Mathieu 方程,未说明其来源(椭圆膜振动、四极质谱仪、周期摆/量子摆、周期介质中波传播)。建议:加引言与一个物理例子。
10. 【mathieu_functions.tex 行 28-48】全周期解按"c_{−n} 有限/为零"分两支(对应 ce_{2n} 与 se_{2n+2})的动机没有解释,读者不知道为什么分这两种情况。建议:补一句(两支对应 cos/sin 型周期解,由系数对称性 c_{−n−l}=±c_{−n+l} 决定)。
11. 【supplementary_formulas.tex 行 1-2】无总起:未说明本文件是哪些章节的补充、记号与正文的关系。且行 3-7 采用对称双边变换 (2π)^{-1/2},与 script.tex 辐射章的非对称约定(∫f e^{iωt}dt、1/2π 反变换)不一致;本文件内容(多对数→费米统计、Bessel 表/K_{2/3}→同步辐射)明显是辐射章的配套,约定冲突会造成读者混淆。建议:加总起说明,并统一或注明与正文约定的换算关系。
12. 【supplementary_formulas.tex 行 21-33】变换对表格实际使用单边余弦/正弦变换约定(如 √(2/π)∫_0^∞cos(ωτ)K_0(aω)dω=1/√(τ²+a²)),与行 3-7 声明的双边对称约定不一致,且表头未说明变换类型与正负号。建议:表头注明"单边 cos/sin 变换、∫_0^∞cos(ωτ)f(ω)dω"等约定。
13. 【vector_spherical_harmonics.tex 行 1-3】以"众所周知"开头直接进入标量 Helmholtz 方程,未说明动机(矢量 Helmholtz 解用于电磁波/弹性波的矢量场展开,如 Mie 散射)。建议:补一句应用背景与目标(构造矢量完备基)。
14. 【vector_spherical_harmonics.tex 行 64】"一般而言,当 ψ 描述的不是平面波或球面波时,基函数虽然完备,但不正交、不归一"——结论突然,无论证。建议:补一句(球面波时 L,M,N 的正交性来自 Y_lm 角向正交性与径向积分;一般情形无此结构)。
15. 【parameter_estimation.tex 行 1-22】缺引入:直接进入 GLS 数学框架,未说明参数估计问题的背景(实验拟合、加权最小二乘的直观意义:权重=误差精度倒数)。建议:加一段引言,并解释 Cov(ε)=σ_0²W^{-1} 中 W 的物理含义。
16. 【infinite_integrals.tex 行 195、515】两处"下面考虑一种典型的级数/积分形式"均未说明这些振荡级数/积分的研究动机与实际出处(如 Fourier 级数收敛、Dirichlet 核、物理中的振荡积分)。建议:各补一句来源与用途。

### B. 小瑕疵

17. 【green_function.tex 行 47-52】Neumann 情形"原先的 Green 函数发散"的根因(常数零模使 ∇²G=δ 不可解、兼容性条件)未说明,结论略显突然。建议:补一句零模说明。
18. 【green_function.tex 行 700-703】concomitant B_T 定义后正文并未使用(初值项随后改用 Laplace 变换推导),概念引入与后续脱节。建议:说明 B_T 与 Laplace 变换初值项推导的关系,或精简该段。
19. 【green_function.tex 行 440-449】d 维近源渐近展开直接罗列,未注明来源。建议:补一句"由 K_{d/2-1} 的小参数展开代入"。
20. 【green_function.tex 行 860-927】波动方程无界核一节中 χ_+^a 的记号(S_+^a/Γ(a+1))虽在行 883 定义,但 δ^{(m-1)} 表示 δ 的 m−1 阶导数未加说明(读者可能误解为上标)。建议:补注"δ^{(k)} 表示 k 阶分布导数"。
21. 【infinite_integrals.tex 行 272】"取 N_j 使 N_jη_j→1/4"的选择未解释(为保证 N_j≤n≤2N_j 时 nη_j∈[1/5,3/5],使 sin 项同号且有下界)。建议:补一句说明。
22. 【parameter_estimation.tex 行 179-182】σ_k=|k̂|√((r^{−2}−1)/(n−2)) 的等价形式突然出现,未说明与 σ_k=σ̂_0/√S_xx 的等价性(需用 r=S_xy/√(S_xxS_yy) 与 k̂=S_xy/S_xx 代入)。建议:补一句代数说明。
23. 【mathieu_functions.tex 行 32-33】行 32 是 n=1 的特例(λ−4−2q²/λ=...),与行 33 的一般公式并列且未注明,读者易混淆两者关系。建议:注明"n=1 时上式化为"。
24. 【mathieu_functions.tex 行 91】"显然,λ 可以展开成 q 的幂级数"的"显然"较随意(实为 Floquet 理论/解析依赖的结论)。建议:改为"由 Floquet 理论,λ(q) 在 q=0 邻域解析"。
25. 【supplementary_formulas.tex 行 17】∫F G dt=2∫_0^∞FG*dω 对实函数严格说应为 2∫_0^∞Re[F(ω)G*(ω)]dω(且与 (1/π) 因子的关系取决于单边谱定义),现表述省略了 Re 与推导。建议:补 Re 与一句推导或注明定义。
26. 【supplementary_formulas.tex 行 124-203】四节恒等式(Bessel 和、平面周期运动积分、Airy 型、立方电阻网、柱对称混合边界)全部纯公式罗列,无来源、无用途说明,且电阻网/混合边值两节与辐射主线无关联。建议:每节加一句用途(如"用于同步辐射角分布""用于圆柱波导本征值问题"),并注明出处。
27. 【ellipsoidal_coordinates.tex 行 15-49】6 条解析延拓公式直接罗列,无推导或出处(尤其 k²>1 分支的复杂公式,本次审核中即发现两处系数错误,足见读者难以自行验证)。建议:注明"由虚模数变换(DLMF 19.7.6-19.7.8)导出",或补一条示范推导。
28. 【ellipsoidal_coordinates.tex 行 194-227】度量、体积元、Laplacian 用"易知/易证"一笔带过,Laplacian 的推导(由 h_ξ 因子代入一般正交曲线坐标公式)被跳过。建议:至少补 Laplacian 的构造说明。
29. 【vector_spherical_harmonics.tex 行 77-82】正交性积分结果(尤其 ∫L·N* 的表面项)直接给出,未给推导线索。建议:补"由 ∫|∇Y|²dΩ=l(l+1) 与分部积分"一句。
30. 【vector_spherical_harmonics.tex 行 155-285】两个长表格无任何使用说明(如何得到、如何查用)。建议:加一句"由行 111-127 公式代入各 (l,m) 得到"。
31. 【green_function.tex 行 719-735】F_n(t)(模源项)与 f_n(t)(体源投影)两个相近记号易混淆,且 F_n 的定义分散在行 727-735。建议:统一改名或集中定义。

---

# 本轮二次核实结论（2026-08-04）

以下结论针对前文“未修改的存疑项”，以独立推导、极限检查和数值代入为准：

- 已修正 `radiation.tex` 椭圆轨道演化式：闭式右端必须除以 \(e_i^2\)，时间组合为 \(e_i^4t/(4\tau)\)。代入 \(t=0\) 得 1，代入相撞时间得 0；原式两项都不满足。
- 已修正 `rigid_body.tex` 心形刚体参数：由给定 \(a/R=6/5\)、\(g/(R\Omega^2)=1.2\) 必得 \(\alpha=7/10\)，并同步更新数值结果。情况三改为中间轴异宿轨道的准确表述。
- 已修正 `lorentz_transformation.tex` 的 \(S_\nu\) 计算，明确采用度规降指标 \(S_\nu=(-\boldsymbol{\beta}\cdot\boldsymbol S,\boldsymbol S)\)，后续 BMT 分量式保持不变。
- 已在 `inverse_square_motion.tex` 说明 \(\alpha=cL\) 分支：\(\phi=0\) 不在正半径物理解域，渐近线位于 \(\lvert\phi\rvert=\sqrt{E^2-m^2c^4}/E\)。
- 已统一 `nonlinear_oscillation.tex` 的 \(\zeta=O(\epsilon)\) 记账：物理阻尼项为 \(-\omega_0\zeta a\)，共振稳态中相应保留 \(\zeta/\epsilon\) 和 \(\zeta^2/\epsilon^2\)。原审核中删除这些因子的改法会把阻尼再次缩小一个 \(\epsilon\)，不采用。
- 已修正 `plasma.tex` 垂直传播横向耦合关系：两个横向因子之积等于耦合项的平方；第一条普通波关系本身保留。
- 已修正 `crystal_optics.tex` 的 \(r_L'\) 关系和 \(R_L'\) 标签；表中 \(t_L=0.82442\) 与正文公式一致，并非错误。
- 已修正 `scattering.tex` 的远场微分功率交叉项符号、无损高频介质球的相位项 \(2i\arctan(\cdots)\)，以及圆柱系数的实场共轭条件。
- 已将 `radiation.tex` 的一般四极矩定义改为 STF 形式；其 \(1/(720\pi\varepsilon_0c^5)\) 功率系数和实例公式随之自洽。
- 已在 `supplementary_formulas.tex` 定义 \(f_m(U)=J_m'(U)/(UJ_m(U))\)、\(g_m(W)=K_m'(W)/(WK_m(W))\)。用数值积分复核，恒等式误差约 \(10^{-12}\)。
- Cherenkov 场、运动磁矩场和穿越辐射磁矩项经过静止极限、远场 \( \boldsymbol E=-\beta c\,\hat{\boldsymbol z}\times\boldsymbol B \)、能流积分及 Maxwell 结构检查，未发现可确认的系数或符号错误，保留原式。
- Bose-Fermi 气体中 \(F(z)\) 的次领头系数与零温 \((7\ln2-1)\) 项在形式和维度上自洽；由于原三重级数在 \(z>1\) 不能直接逐项求和，未作未经充分证实的改动。
- STF 多极矩中的 \(1/42\)、\(1/60\)、\(1/1680\) 系数与通用 STF 展开式及低阶环形电偶极矩约定一致，未发现可确认错误。
- Ising 模型能量/热容项已通过数值微分关系复核，本轮不改。

---

# 叙述与体系问题的统一改造方案

前文记录的叙述建议不应逐条孤立修补，而应按统一的“物理动机 -> 模型假设 -> 基准解 -> 核心闭式推导 -> 近似台账 -> 极限检查 -> 实例解释 -> 章节总结”骨架重写。具体规范见 `docs/refactory.md`。

