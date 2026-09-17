"""One-time conversion of the eight new teaching modules to analytic exercises."""
from pathlib import Path
import re

BOOK=Path(__file__).resolve().parents[1]
SECTIONS=BOOK/'sections'

def examples(name, replacements):
    p=SECTIONS/name
    text=p.read_text(encoding='utf-8')
    pattern=r'\\begin\{Example\}.*?\\end\{Example\}'
    assert len(re.findall(pattern,text,re.S))==len(replacements),name
    iterator=iter(replacements)
    text=re.sub(pattern,lambda m:next(iterator),text,flags=re.S)
    p.write_text(text,encoding='utf-8')

examples('electron-channel-coherence-worked.tex',[
r'''\begin{Example}[解析求出高斯通道的重叠与正交条件]
设入射动量概率分布的标准差为 $\sigma_p$，振幅取为
\begin{equation*}
 f_p(p)=(2\pi\sigma_p^2)^{-1/4}
 \exp[-(p-p_0)^2/(4\sigma_p^2)].
\end{equation*}
求平移 $\ell$ 阶与 $m$ 阶后的重叠，并将允许误差写成对谱宽的条件。

令 $a=p_0+\ell\hbar\kappa_z$、$b=p_0+m\hbar\kappa_z$。关键是先配方：
\begin{equation*}
 (p-a)^2+(p-b)^2=2[p-(a+b)/2]^2+(a-b)^2/2.
\end{equation*}
第一项的高斯积分恰好抵消归一化因子，第二项与积分变量无关，故
\begin{equation}
 S_{\ell m}^{\rm pkt}
 =\exp\!\left[-\frac{(\ell-m)^2\hbar^2\kappa_z^2}{8\sigma_p^2}\right].
 \label{eq:electron-channel-gaussian-overlap}
\end{equation}
若允许相邻通道的振幅重叠至多为 $0<\epsilon_{\rm ov}<1$，取对数即可得到
\begin{equation*}
 \sigma_p\le\frac{\hbar|\kappa_z|}{\sqrt{8\ln(1/\epsilon_{\rm ov})}}.
\end{equation*}
在同步、窄带条件下，$v_0\kappa_z=\omega$、$\sigma_E\simeq v_0\sigma_p$，故同一条件为
$\sigma_E\lesssim\hbar\omega/\sqrt{8\ln(1/\epsilon_{\rm ov})}$。
这是量子波包的条件，不是仪器分辨率；若控制的是重叠模平方，分母中的 $8$ 改为 $4$。保留误差符号能直接用于任意电子能量、交换步长和所需精度。
\end{Example}''',
r'''\begin{Example}[不等权两通道的纯度与干涉可见度]
取归一化联合态
\begin{equation*}
 |\Psi\rangle=\sqrt{w}\,|0\rangle|\chi_0\rangle
 +\sqrt{1-w}\,\ee^{\ii\varphi}|1\rangle|\chi_1\rangle,
 \quad 0\le w\le1,\quad \mu_X=\langle\chi_1|\chi_0\rangle.
\end{equation*}
不指定环境的具体模型，求电子纯度和参考干涉可见度。

由偏迹规则，非对角元等于两振幅乘积乘环境重叠：
\begin{equation*}
 \rho_e=\begin{pmatrix}
 w&\sqrt{w(1-w)}\,\ee^{-\ii\varphi}\mu_X\\
 \sqrt{w(1-w)}\,\ee^{\ii\varphi}\mu_X^*&1-w
 \end{pmatrix}.
\end{equation*}
\emph{纯度}是密度矩阵平方的迹。对这个二阶矩阵，不必求本征值，直接平方对角项并加两份非对角模平方：
\begin{equation*}
 \operatorname{Tr}\rho_e^2
 =w^2+(1-w)^2+2w(1-w)|\mu_X|^2
 =1-2w(1-w)(1-|\mu_X|^2).
\end{equation*}
再投影到 $|+_\vartheta\rangle=(|0\rangle+\ee^{\ii\vartheta}|1\rangle)/\sqrt2$，得到
\begin{equation*}
 P_+(\vartheta)=\frac12+\sqrt{w(1-w)}
 \Re[\ee^{\ii(\vartheta-\varphi)}\mu_X],\qquad
 \mathcal V=\frac{P_{\max}-P_{\min}}{P_{\max}+P_{\min}}
 =2\sqrt{w(1-w)}|\mu_X|.
\end{equation*}
因此可见度下降可能来自两种独立原因：路径权重不等，或环境记录可区分。即使 $|\mu_X|=1$、电子完全纯，只要 $w\ne1/2$，该参考投影的可见度仍小于一；等权时才有 $\mathcal V=|\mu_X|$。

若环境记录是两种相干态，则
$|\mu_X|=\exp[-|\alpha_1-\alpha_0|^2/2]$，代入即可得到纯度和可见度随记录间距的闭式。记录相同给纯态，正交记录给纯度 $w^2+(1-w)^2$；两者的普通能谱始终都是 $(w,1-w)$。
\end{Example}'''])

examples('electron-finite-window-worked.tex',[
r'''\begin{Example}[高斯作用窗的线宽与等面积比较]
把矩形开关换成 $w(t)=\exp[-t^2/(2\tau_w^2)]$，求弱跃迁谱，并与具有相同积分面积的矩形窗比较。这里 $\tau_w$ 是振幅包络的时间尺度。

对指数配方，或直接使用高斯 Fourier 积分，有
\begin{equation*}
 \int_{-\infty}^{\infty}\dd t\,
 \ee^{-t^2/(2\tau_w^2)+\ii\Delta t}
 =\sqrt{2\pi}\tau_w\ee^{-\Delta^2\tau_w^2/2}.
\end{equation*}
因此
\begin{equation*}
 A_j^{(1)}=-\ii\mathcal G_j\sqrt{2\pi}\tau_w
 \ee^{-\Delta_j^2\tau_w^2/2},\qquad
 P_j^{(2)}=2\pi|\mathcal G_j|^2\tau_w^2
 \ee^{-\Delta_j^2\tau_w^2}.
\end{equation*}
令谱值降到共振峰的一半，取对数得 $|\Delta_j|\tau_w=\sqrt{\ln2}$，故角频率全宽半高为 $2\sqrt{\ln2}/\tau_w$。它来自\emph{概率}包络，不能直接使用振幅包络的半高宽。

若矩形窗长度取 $T=\sqrt{2\pi}\tau_w$，两窗具有相同积分面积和相同共振概率 $|\mathcal G_j|^2T^2$。高斯窗的谱全宽为 $2\sqrt{2\pi\ln2}/T$；矩形窗则为 $4x_{1/2}/T$，其中 $x_{1/2}$ 是 $\sinc^2x=1/2$ 的首个正根。两者都按 $T^{-1}$ 缩窄，但高斯谱没有旁瓣，矩形谱有代数衰减的旁瓣。延长窗口时，弱跃迁条件仍须独立检查，不能只比较线宽。
\end{Example}''',
r'''\begin{Example}[黄金律的适用时间窗是否存在]
对上述 Lorentz 跃迁谱，给定允许的有限时间相对误差 $\eta$ 和最大耗尽概率 $p_*$，求一组便于手算的充分条件。

先无量纲化，令 $x=T/\tau_c$、$\epsilon_c=\Gamma_0\tau_c$。精确二阶结果与黄金律之比为
\begin{equation*}
 R(x)=\frac{P^{(2)}(T)}{\Gamma_0T}
 =1-\frac{1-\ee^{-x}}{x},\qquad
 1-R(x)=\frac{1-\ee^{-x}}{x}<\frac1x.
\end{equation*}
这里把相对误差定义为相对于黄金律预测的偏差。求导得
\begin{equation*}
 R'(x)=\frac{1-(1+x)\ee^{-x}}{x^2}>0,
\end{equation*}
因为 $\ee^x>1+x$。因此增加作用时间会单调改善黄金律的有限窗误差，却同时增加耗尽。

由上界，$T\ge\tau_c/\eta$ 足以使相对误差不超过 $\eta$；又因 $P^{(2)}<\Gamma_0T$，取 $T\le p_*/\Gamma_0$ 足以控制耗尽。两条件能够同时满足，只需
\begin{equation*}
 \frac{\tau_c}{\eta}\le T\le\frac{p_*}{\Gamma_0},\qquad
 \Gamma_0\tau_c\le\eta p_*.
\end{equation*}
这是一组充分条件，未必是最宽的时间窗。它直接说明：只有环境去相位时间显著短于初态耗尽时间，才存在可用的恒定速率区。若区间为空，应回到有限时间概率或完整动力学，而不是强行定义一个黄金律速率。
\end{Example}'''])

examples('electron-pinem-field-calibration.tex',[
r'''\begin{Example}[由实场峰值解析求边带与能宽]
给定实场峰值 $E_{\rm pk}^{\rm(real)}$、作用长度 $L_{\rm int}$ 和失配 $\Delta\kappa$，求弱边带权重，并用完整能谱宽度反求场幅。令
\begin{equation*}
 b=|\beta|=\frac{eE_{\rm pk}^{\rm(real)}L_{\rm int}}{2\hbar\omega}
 \left|\sinc\!\left(\frac{\Delta\kappa L_{\rm int}}2\right)\right|.
\end{equation*}
用 Bessel 幂级数而不逐阶数值求值：
\begin{equation*}
 J_0(2b)=1-b^2+\frac{b^4}{4}+O(b^6),\quad
 J_1(2b)=b-\frac{b^3}{2}+O(b^5),\quad
 J_2(2b)=\frac{b^2}{2}+O(b^4).
\end{equation*}
平方后得到
\begin{equation*}
 P_0=1-2b^2+\frac32b^4+O(b^6),\quad
 P_{\pm1}=b^2-b^4+O(b^6),\quad
 P_{\pm2}=\frac{b^4}{4}+O(b^6).
\end{equation*}
检查归一化时必须把正负阶都算入：$P_0+2P_1+2P_2=1+O(b^6)$。四阶项恰好抵消，是检查展开是否遗漏系数的简便方法。

若不要求 $b\ll1$，仍可使用完整 Bessel 分布的矩恒等式 $\operatorname{Var}\ell=2b^2$。于是交换导致的能量标准差为
\begin{equation*}
 \sigma_{E,\rm ex}=\sqrt2\hbar\omega b
 =\frac{eE_{\rm pk}^{\rm(real)}L_{\rm int}}{\sqrt2}
 \left|\sinc\!\left(\frac{\Delta\kappa L_{\rm int}}2\right)\right|.
\end{equation*}
已知失配时可直接反解 $E_{\rm pk}^{\rm(real)}$。同步处展宽与场强、长度线性相关；接近 $\sinc$ 零点时反演分母很小，场幅误差被放大。这里使用的是相互作用增加的完整能谱方差；源能宽、仪器展宽与有限窗口的处理见\secref{sec:electron-detector-inversion-worked}。
\end{Example}'''])

examples('electron-quantum-exchange-coherence.tex',[
r'''\begin{Example}[经典纯态近似的误差怎样随耦合缩小]
以 $|\psi_\beta\rangle$ 为经典参考态，求量子电子态偏离它的大小，并比较“能谱接近”与“量子态接近”两种判据。

前面已证明各平移态彼此正交；未平移项的本征值为 $w_0=\ee^{-r_Q}$。因此与参考纯态的重叠概率为
\begin{equation*}
 F_\beta\equiv\langle\psi_\beta|\rho_e^{\rm out}|\psi_\beta\rangle
 =\ee^{-r_Q}.
\end{equation*}
采用\emph{迹距离} $\mathcal D_{\rm tr}(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1$，其中迹范数是奇异值之和；对厄米差矩阵，就是本征值绝对值之和。这里差矩阵的本征值是 $w_0-1,w_1,w_2,\ldots$，故无需做无限维对角化：
\begin{equation*}
 \mathcal D_{\rm tr}
 =\frac12\bigl[(1-w_0)+\sum_{m\ge1}w_m\bigr]
 =1-\ee^{-r_Q}.
\end{equation*}
迹距离控制任意一个测量事件的概率偏差。要求该误差不超过 $0<\varepsilon<1$，等价于
\begin{equation*}
 r_Q\le-\ln(1-\varepsilon).
\end{equation*}
小耦合时，$\mathcal D_{\rm tr}=r_Q+O(r_Q^2)$，纯度则为
$\operatorname{Tr}[(\rho_e^{\rm out})^2]=1-2r_Q+3r_Q^2+O(r_Q^3)$。

相反，量子方差相对于经典方差的增量在 $\beta\ne0$ 时为
\begin{equation*}
 \frac{\operatorname{Var}\ell-2|\beta|^2}{2|\beta|^2}
 =\frac{r_Q}{2|\beta|^2}
 =\frac1{2|\alpha_{\rm coh}|^2}.
\end{equation*}
增大平均光子数会让这个\emph{相对方差误差}缩小，却不改变固定 $r_Q$ 下的迹距离。要同时恢复完整的经典电子纯态，应取 $\gq\to0$、$|\alpha_{\rm coh}|\to\infty$ 且 $\beta$ 固定。两个条件的差异由解析式直接可见。
\end{Example}'''])

examples('electron-recoil-bragg-calculation.tex',[
r'''\begin{Example}[有失谐的两态转移及其容差]
在外部通道已被受控消去的前提下，设两保留态仍有残余失谐 $\Delta_B$。去掉公共在位能后，按 $|0\rangle,|1\rangle$ 排列的 Hamiltonian 为
\begin{equation*}
 H_2=\frac\hbar2
 \begin{pmatrix}-\Delta_B&\Omega^*\\\Omega&\Delta_B\end{pmatrix}.
\end{equation*}
求从 $|0\rangle$ 出发的转移概率，以及达到 $1-\eta$ 最大转移率所允许的失谐。

不必先求本征矢。直接平方得 $H_2^2=\hbar^2\Omega_B^2I/4$，其中
$\Omega_B=\sqrt{|\Omega|^2+\Delta_B^2}$。指数的偶数幂与奇数幂分别求和，得到
\begin{equation*}
 U_2(T)=I\cos\frac{\Omega_BT}{2}
 -\frac{2\ii H_2}{\hbar\Omega_B}\sin\frac{\Omega_BT}{2},\qquad
 P_1(T)=\frac{|\Omega|^2}{|\Omega|^2+\Delta_B^2}
 \sin^2\frac{\Omega_BT}{2}.
\end{equation*}
首个极大值位于 $T=\pi/\Omega_B$，但其高度一般小于一：
\begin{equation*}
 P_{1,\max}=\frac1{1+(\Delta_B/|\Omega|)^2},\qquad
 P_{1,\max}\ge1-\eta
 \ \Longleftrightarrow\ 
 \frac{|\Delta_B|}{|\Omega|}\le\sqrt{\frac{\eta}{1-\eta}}.
\end{equation*}
当 $\Delta_B=0$ 时恢复 $\pi$ 脉冲公式；当失谐远大于耦合时，转移上限按 $|\Omega/\Delta_B|^2$ 衰减。增加耦合能提高容差，却同时破坏外部反冲通道的谱隔离，所以还必须保留 $|\Omega|/(2\omega_{\rm r})\ll1$。两态解析解本身不能检验后一条件，完整格点的 TDSE 演化用于做这项检验。
\end{Example}'''])

examples('electron-temporal-bunching-worked.tex',[
r'''\begin{Example}[第一谐波最强的距离：弱调制与强调制]
给定 $b=|\beta|>0$，求第一谐波首次达到最大值的漂移距离。由闭式，问题化为在 $0\le s_{\rm d}\le\pi/2$ 内最大化
$|B_1|=|J_1(4b\sin s_{\rm d})|$。

令 $x_*$ 为 $J_1'(x)=0$ 的第一个正根。递推关系给
$J_1'(x)=[J_0(x)-J_2(x)]/2$，所以该常数也由 $J_0(x_*)=J_2(x_*)$ 定义；$x_*\simeq1.84118$。$J_1$ 的首个正极大值也是其绝对最大值。现在只需检查驱动能否达到这个参数：
\begin{equation*}
 s_{\rm d,*}=\begin{cases}
 \pi/2,&4b<x_*,\\
 \arcsin[x_*/(4b)],&4b\ge x_*,
 \end{cases}\qquad
 L_* =\frac{v_0s_{\rm d,*}}{\omega_{\rm r}}.
\end{equation*}
弱调制时可用 $J_1(x)\simeq x/2$，故 $|B_1|\simeq2b|\sin s_{\rm d}|$，首个最优位置是 $L_T/4$。强调制时展开 $\arcsin x\simeq x$，得
$L_*\simeq v_0x_*/(4b\omega_{\rm r})$，最优距离随场幅近似反比缩短。

达到 $x_*$ 后，第一谐波上限为 $|B_1|=J_1(x_*)\simeq0.581865$；对应 $\mathcal M_1=2|B_1|>1$。这不违反密度正性，因为 $\mathcal M_1$ 是 Fourier 调制幅度。若只保留 $1+2\Re(B_1\ee^{\ii\theta_\zeta})$，反而会出现负值，说明必须保留更高谐波。第一谐波最大、完整脉冲最窄和 Talbot 复现是三个不同条件。
\end{Example}''',
r'''\begin{Example}[从所需谐波反推时间抖动容差]
要求第 $d\ne0$ 阶谐波至少保留理想幅度的比例 $0<\eta_d<1$。由高斯衰减因子取对数，直接得到
\begin{equation*}
 \exp[-d^2\omega^2\sigma_{t,\rm jit}^2/2]\ge\eta_d
 \ \Longleftrightarrow\ 
 \sigma_{t,\rm jit}\le\frac{\sqrt{2\ln(1/\eta_d)}}{|d|\omega}.
\end{equation*}
因此分辨越高的谐波，允许的抖动按 $1/|d|$ 缩小。若给定同一保留阈值 $\eta$，可用谐波阶数的上限为
\begin{equation*}
 d_{\max}=\left\lfloor
 \frac{\sqrt{2\ln(1/\eta)}}{\omega\sigma_{t,\rm jit}}
 \right\rfloor,
\end{equation*}
其中向下取整表示取不超过括号内实数的最大整数。

若探测器另有独立高斯时间响应宽度 $\sigma_{t,\rm det}$，两个特征函数相乘，测得谐波为
\begin{equation*}
 B_d^{\rm obs}=B_d\exp\!\left[-\frac{d^2\omega^2}{2}
 (\sigma_{t,\rm jit}^2+\sigma_{t,\rm det}^2)\right].
\end{equation*}
因此仅凭谐波衰减，不能区分束流到达抖动与探测时间模糊。若 $B_d\ne0$，不同 $d$ 的 $-\ln|B_d^{\rm obs}/B_d|/d^2$ 应为同一常数；偏离这个关系说明单一高斯模糊模型不充分。这给出不依赖某组特定时间数值的实验检查。
\end{Example}'''])

examples('electron-reference-tomography-worked.tex',[
r'''\begin{Example}[四相位数据的解析重建与正性检查]
将四相位测得概率记为 $p_0,p_{\pi/2},p_\pi,p_{3\pi/2}$，已知输入占据 $p$ 和参考系数 $u_0,u_1$。求相干，并给出无需对角化的物理一致性条件。

先把条纹写成三个实系数：
\begin{equation*}
 P_0(\varphi_R)=A_R-C_R\cos\varphi_R+S_R\sin\varphi_R,
 \quad C_R=2u_0u_1x_{01},\quad S_R=2u_0u_1y_{01}.
\end{equation*}
四个设置依次读出 $A_R-C_R,A_R+S_R,A_R+C_R,A_R-S_R$。两两作差与作和即可解出
\begin{equation*}
 C_R=\frac{p_\pi-p_0}{2},\qquad
 S_R=\frac{p_{\pi/2}-p_{3\pi/2}}2,\qquad
 c_{01}=\frac{C_R+\ii S_R}{2u_0u_1}.
\end{equation*}
同一模型还要求
\begin{equation*}
 p_0+p_\pi=p_{\pi/2}+p_{3\pi/2}=2A_R,
 \qquad A_R=u_0^2p+u_1^2(1-p).
\end{equation*}
这是独立于未知相干的背景检查。正半定条件 $\det\rho_e\ge0$ 进一步给
\begin{equation*}
 C_R^2+S_R^2\le4u_0^2u_1^2p(1-p).
\end{equation*}
最后，由矩阵平方直接得到纯度
\begin{equation*}
 \operatorname{Tr}\rho_e^2=p^2+(1-p)^2
 +\frac{C_R^2+S_R^2}{2u_0^2u_1^2}.
\end{equation*}
等号边界对应纯态；$C_R=S_R=0$ 对应具有同样普通能谱的非相干混合。有限计数会使一致性关系近似成立，统计检验必须结合下述计数误差，不能把一次偏离直接当成模型失效。
\end{Example}'''])

examples('electron-detector-inversion-worked.tex',[
r'''\begin{Example}[由允许误分率解析确定分辨率要求]
设相邻边带间隔为 $\hbar\omega$、有效高斯标准差为 $\sigma_E$，以两中心的中点划分窗口。求给定真实边带的电子被分到其他窗口的概率。

将中心平移到零，正确窗口为 $[-\hbar\omega/2,\hbar\omega/2]$。左右高斯尾相等，所以
\begin{equation*}
 P_{\rm mis}=2\Phi_N\!\left(-\frac{\hbar\omega}{2\sigma_E}\right).
\end{equation*}
给定容许值 $0<\varepsilon<1$，利用 $\Phi_N$ 单调递增并反解，得到
\begin{equation*}
 P_{\rm mis}\le\varepsilon
 \ \Longleftrightarrow\ 
 \sigma_E\le\frac{\hbar\omega}{2\Phi_N^{-1}(1-\varepsilon/2)}.
\end{equation*}
这里 $\Phi_N^{-1}(y)$ 是满足 $\Phi_N(x)=y$ 的分位点。若希望避免求反函数，还可由正态尾上界
$\Phi_N(-x)<\ee^{-x^2/2}/(\sqrt{2\pi}x)$（$x>0$）得到
\begin{equation*}
 P_{\rm mis}<\sqrt{\frac8\pi}\frac{\sigma_E}{\hbar\omega}
 \exp\!\left[-\frac{(\hbar\omega)^2}{8\sigma_E^2}\right].
\end{equation*}
尾上界来自在积分中用 $u/x\ge1$ 替代一，再积分 $u\ee^{-u^2/2}$。它显示良好分辨区的误分率随间隔宽度比呈指数下降。$P_{\rm mis}$ 是给定真实边带的条件误差；实际某个窗口的占据还须叠加所有边带的输入权重。
\end{Example}''',
r'''\begin{Example}[复近场反演的闭式自检与误差传播]
令 $q_0,q_{\pi/2},q_\pi,q_{3\pi/2}$ 为四相位方差数据，参考幅度 $\beta_R>0$ 已知，求复耦合并检查四组数据能否来自同一个稳定场。

写 $\beta_s=x_s+\ii y_s$，令 $A_s=x_s^2+y_s^2+\beta_R^2$，则四组理想数据依次为
\begin{equation*}
 A_s+2\beta_Rx_s,\quad A_s+2\beta_Ry_s,\quad
 A_s-2\beta_Rx_s,\quad A_s-2\beta_Ry_s.
\end{equation*}
作差给出\eqnrefs{eq:electron-nearfield-four-phase-field}，作和则提供两类自检：
\begin{align*}
 q_0+q_\pi&=q_{\pi/2}+q_{3\pi/2},\\
 \frac{(q_0-q_\pi)^2+(q_{\pi/2}-q_{3\pi/2})^2}{16\beta_R^2}
 &=\frac{q_0+q_{\pi/2}+q_\pi+q_{3\pi/2}}4-\beta_R^2.
\end{align*}
第一式检查相位无关背景是否稳定，第二式检查由干涉差值恢复的 $|\beta_s|^2$ 是否与平均强度一致。其成立条件包括稳定相位、正确基线方差及有效的完整能窗。

若四组 $q$ 的估计误差独立且同方差 $\sigma_q^2$，参考本身视为已知，则线性作差给
\begin{equation*}
 \operatorname{Var}\widehat x_s=\operatorname{Var}\widehat y_s
 =\frac{\sigma_q^2}{8\beta_R^2},\qquad
 \operatorname{Cov}(\widehat x_s,\widehat y_s)=0.
\end{equation*}
这里固定的是 $q$ 的误差，不能据此认为参考越强越好：真实计数下 $\sigma_q$、可收集能窗和参考标定误差都可能随参考幅度变化。参考相位的共同偏移只旋转重建的复平面坐标，所确定的是相对相位。
\end{Example}'''])

# Keep numerical propagation as explicit validation of analytic models, outside exercises.
p=SECTIONS/'electron-recoil-bragg-calculation.tex'
t=p.read_text(encoding='utf-8')
marker=r'\figref{fig:electron-bragg-convergence}'
addition=r'''用于检验近似的 TDSE 计算采用相同的初态 $d_\ell(0)=\delta_{\ell0}$ 和名义脉冲面积 $|\Omega|T=\pi$，以 $r_\Omega=|\Omega|/\omega_{\rm r}$ 为唯一驱动参数。完整格点在 $r_\Omega=0.20,1,5$ 时分别给出 $P_1\simeq0.9951,0.9076,0.1167$，对应泄漏约为 $0.00490,0.0741,0.7715$；两态模型在三种情况下都预测完全转移。这里的数值是对解析约化的误差检查，求解的是\eqnrefs{eq:electron-bragg-full-lattice} 的含时 Schrödinger 方程（TDSE），常脉冲时可直接用矩阵指数传播。

'''
t=t.replace(marker,addition+marker,1)
p.write_text(t,encoding='utf-8')

p=SECTIONS/'electron-reference-tomography-worked.tex'
t=p.read_text(encoding='utf-8')
t=t.replace('上例若每相位 $N=10^4$，两分量的统计标准差约为 $0.00548$ 和 $0.00556$；总剂量是四组共 $4\\times10^4$ 个电子，另需用于确定 $p$ 和标定参考的计数。',r'''用例题中的条纹系数，上式分子还可写成 $2A_R(1-A_R)-2C_R^2$；虚部分子把 $C_R$ 换成 $S_R$。若要求两个分量的标准差均不超过 $\varepsilon_c$，充分的每相位计数为
\begin{equation*}
 N\ge\frac{\max\{2A_R(1-A_R)-2C_R^2,\,
 2A_R(1-A_R)-2S_R^2\}}{16u_0^2u_1^2\varepsilon_c^2}.
\end{equation*}
总剂量为四组共 $4N$，另需用于确定 $p$ 和标定参考的计数。实际设计时可用 $P(1-P)\le1/4$ 给出与未知态无关的保守上界。''')
t=t.replace('两通道电子态的参考读出。实线使用', '两通道电子态的参考读出。数值图取 $p=0.65$、$b_R=0.40$；实线使用')
p.write_text(t,encoding='utf-8')

p=SECTIONS/'electron-pinem-field-calibration.tex'
t=p.read_text(encoding='utf-8').replace('右图取同步情况下的 $|\\beta|=0.6452$',r'右图取 $\SI{200}{\kilo\electronvolt}$ 电子、$\SI{800}{\nano\metre}$ 光、$\SI{2}{\micro\metre}$ 同步作用区和 $\SI{1}{\mega\volt\per\metre}$ 实场峰值，此时 $|\beta|=0.6452$')
p.write_text(t,encoding='utf-8')

p=SECTIONS/'electron-temporal-bunching-worked.tex'
t=p.read_text(encoding='utf-8').replace('左图用相同的 PINEM 占据',r'数值图取 $|\beta|=1.20$、$\SI{200}{\kilo\electronvolt}$ 电子及 $\SI{800}{\nano\metre}$ 同步光学步长。左图用相同的 PINEM 占据')
p.write_text(t,encoding='utf-8')

p=BOOK/'ch11.tex'
t=p.read_text(encoding='utf-8').replace('长度为整整数个调制周期','长度为整数个调制周期')
p.write_text(t,encoding='utf-8')
print('Reworked 12 examples as symbolic analytic exercises; retained numerical figures as validation.')
