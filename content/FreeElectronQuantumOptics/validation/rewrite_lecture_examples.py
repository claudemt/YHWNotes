"""Reader-facing explanations accompanying the analytic examples. Run once."""
from lecture_edit_support import edit, region, lead, finish
S='sections/'
def opening(stem,new):
    name=S+stem+'.tex'
    # Keep semantic labels; replace the opening before its first display.
    from lecture_edit_support import get
    text=get(name); start=text.index('\n\n')+2
    stops=[text.find(t,start) for t in ['\n\n',r'\begin{']]
    end=min(x for x in stops if x>=0)
    edit(name,text[start:end],new.rstrip()+'\n' if text[end]=='\\' else new.rstrip())

opening('electron-channel-coherence-worked',r'''在离散基底中，态 $\sum_r c_r|r\rangle$ 的归一化通常写成 $\sum_r|c_r|^2=1$。这一写法用到了基矢正交性。电子的实际输入是有宽度的波包，平移后的两个包可能重叠，因此在把它们称为两个通道以前，需要先计算内积。下面固定自旋，只保留纵向动量。取 $\langle p|p'\rangle=\delta(p-p')$，入射态写成''')
edit(S+'electron-channel-coherence-worked.tex',r'$f_p$ 是动量概率振幅密度，单位为动量的负二分之一次方；$|f_p|^2\dd p$ 才是落在一个动量区间的概率。广义态 $|p\rangle$ 本身不具有有限范数，所以不能把某一点的 $|f_p(p)|^2$ 当作离散通道概率。',r'''其中 $f_p(p)$ 是连续动量振幅。电子落在小区间 $[p,p+\dd p]$ 的概率为 $|f_p(p)|^2\dd p$，所以 $|f_p|^2$ 是概率密度，$f_p$ 的单位为动量的负二分之一次方。这与离散系数 $c_r$ 的无量纲性质不同。$|p\rangle$ 的 $\delta$ 归一化保证积分叠加后的波包具有有限范数。''')
edit(S+'electron-channel-coherence-worked.tex',r'这是量子波包的条件，不是仪器分辨率；若控制的是重叠模平方，分母中的 $8$ 改为 $4$。保留误差符号能直接用于任意电子能量、交换步长和所需精度。',r'''这里限制的是两个波包本身的内积。仪器是否能把两个峰分开，还要另外计算探测响应。若误差要求施加在重叠的模平方上，同样取对数，分母中的 $8$ 改为 $4$。''')
edit(S+'electron-channel-coherence-worked.tex',r'在已选定的正交通道基 $\{|r\rangle_e\}$ 中，任意联合纯态都可展开为',r'''选好正交通道基以后，还要处理电子与环境的相关。设 $\{|r\rangle_e\}$ 和 $\{|\mu\rangle_X\}$ 分别是电子与环境的正交基。先将联合振幅写为 $C_{r\mu}$，再把同一电子通道对应的所有环境振幅合成一个向量，便有''')
opening('electron-finite-window-worked',r'''上一节的矩形脉冲给出 $\sinc^2$ 跃迁谱。它来自不同时刻发生的跃迁振幅相加：共振时相位相同，失谐时相位随时间转动。为了比较不同脉冲形状，把这一积分保留下来。设初态到末态通道 $j$ 的相互作用绘景矩阵元为 $\hbar\mathcal G_jw(t)\ee^{\ii\Delta_jt}$，其中 $\mathcal G_j$ 是耦合率，$\Delta_j$ 是失谐，两者单位均为 ${\rm s^{-1}}$；无量纲函数 $w(t)$ 描述耦合何时打开、何时关闭以及怎样变化。由一阶含时微扰论，''')
edit(S+'electron-finite-window-worked.tex','为什么连续末态的总概率可以正比于 $T$？定义所选初态的跃迁谱密度',r'''单个共振末态的概率随 $T^2$ 增长，而黄金律给出的总概率随 $T$ 增长。要看清这一变化，需要把连续末态在不同失谐处的贡献积分起来。将末态数目与耦合权重合并，定义所选初态的\emph{跃迁谱密度}''')
opening('electron-pinem-field-calibration',r'''前面已把电子的调制写成沿轨迹的场积分 $\beta$。现在用一个给定近场求可测的边带概率。代入场幅之前，先把实场峰值与复振幅的关系写清楚：本书的 $E_{\omega,z}$ 表示正频分量，因此单频实场为''')
opening('electron-quantum-exchange-coherence',r'''经典 PINEM 给出一个纯电子态。若把同一束相干光完全量子化，电子输出是否仍等于这个纯态，需要对光场求偏迹才能判断。相干态满足 $\hat a|\alpha_{\rm coh}\rangle=\alpha_{\rm coh}|\alpha_{\rm coh}\rangle$，吸收项因此产生熟悉的经典振幅；发射项含有 $\hat a^\dagger$，还会产生不能用这个数代替的分量。下面保留两项，计算电子的密度矩阵、能谱和纯度。光子统计在电子谱中的表现由同一联合态描述。\cite{Dahan2021Science}''')
edit(S+'electron-quantum-exchange-coherence.tex',r'这里 $m$ 是真空交换部分中电子损失的量子数；在移去相干位移的光场表象中，它与环境的 Fock 记录一一对应。对这些未观测记录求和就产生混态，而不是给每个电子振幅随意附加一个衰减因子。',r'''每个 $\hat b^m|\psi_\beta\rangle$ 都是把经典输出向能量损失方向移动 $m$ 阶后的归一态，$w_m$ 是它的概率权重。局部推导中会把光的平均相干幅度移去，余下的不同光子数对应这些不同的电子平移。只观测电子时，对正交的光子末态求和，便得到上式的混合。''')
edit(S+'electron-quantum-exchange-coherence.tex',r'这些被平移的态彼此正交，因为 $S_{\rm tr}$ 与 $\hat b$ 对易，且 $\langle0|\hat b^{m-n}|0\rangle=\delta_{mn}$。所以 $w_m$ 就是约化电子态的本征值，纯度为',r'''为了量化混合程度，使用\emph{纯度} $\operatorname{Tr}\rho^2$。若归一化密度矩阵的本征值为 $w_m$，纯度就是 $\sum_mw_m^2$；只有一个本征值等于一时为纯态，几个非零权重共同存在时纯度小于一。这里的平移态彼此正交：$S_{\rm tr}$ 与 $\hat b$ 对易，而 $\langle0|\hat b^{m-n}|0\rangle=\delta_{mn}$。因此已经找到了本征值 $w_m$，无需另求矩阵对角化，得到''')
edit(S+'electron-quantum-exchange-coherence.tex','两个条件的差异由解析式直接可见。','在这个极限中，经典调制保持不变，而真空交换权重趋于零。')
opening('electron-thermal-exchange-analytic',r'''相干光的平均光子数确定以后，仍有许多不同光态具有同样的平均能量。热光就是其中一种。它没有固定光学相位，光子数也遵循与相干态不同的分布。为了求这些差别怎样传给电子，保持上一节的单模低反冲交换算符 $S_Q$ 不变，仍取电子初态 $|0\rangle_e$，只把光场输入换为热态''')
edit(S+'electron-thermal-exchange-analytic.tex',r'与其逐个计算无限多个 $P_\ell$，先定义它们的\emph{特征函数}',r'''出射电子可以占据许多边带。求这组概率时，可以利用 Fourier 级数把所有 $P_\ell$ 合成一个函数，称为概率分布的\emph{特征函数}：''')
edit(S+'electron-thermal-exchange-analytic.tex',r'这里 $\vartheta$ 是用于生成统计矩的无量纲辅助变量，不是某个电子的到达相位。概率是它的 Fourier 系数，矩可由原点导数得到；$\ln\chi_e$ 的导数则直接给累积量。热输入的闭式为',r'''其中 $\hat\Lambda_e$ 是阶数算符，$\vartheta$ 是无量纲 Fourier 变量。它只是用来整理概率，不代表额外的电子动力学。因为 $\partial_\vartheta\ee^{\ii\ell\vartheta}=\ii\ell\ee^{\ii\ell\vartheta}$，在原点求导便有
\[
\langle\ell\rangle=-\ii\chi_e'(0),\qquad
\langle\ell^2\rangle=-\chi_e''(0),\qquad \chi_e(0)=1.
\]
对数的导数则自动去掉低阶矩的乘积：
\[
-\ii(\ln\chi_e)'(0)=\langle\ell\rangle,\qquad
-(\ln\chi_e)''(0)=\langle\ell^2\rangle-\langle\ell\rangle^2.
\]
这些对数导数称为\emph{累积量}，前两阶就是均值和方差。用本节末尾的算符代数求热态平均，得到''')
opening('electron-recoil-bragg-calculation',r'''前面给出了从完整反冲格选出两个共振态的条件。现在计算一次脉冲中的转移概率，并将两态解与完整格的演化比较。我们仍限制自旋保持、单一纵向动量步长和二阶色散，先写出所有电子通道的方程：''')
opening('electron-temporal-bunching-worked',r'''在能谱上看到一串边带以后，还不能仅凭各峰的高度确定电子的时间分布；不同边带的相位决定它们在何时相长干涉。下面把上一节的密度矩阵传播式用于 PINEM 输出，求出周期密度及其 Fourier 谐波。令 $\theta_\zeta=\kappa_z\zeta$ 表示一个空间周期内的位置，$s_{\rm d}=\omega_{\rm r}t\simeq\omega_{\rm r}L/v_0$ 表示传播中积累的反冲相位；两者均无量纲。相对周期密度为''')
edit(S+'electron-temporal-bunching-worked.tex','对这种纯输入，前面副对角线求和还可化成一个闭式：',r'''将周期密度写为 $\mathfrak n_e=\sum_d B_d\ee^{\ii d\theta_\zeta}$，其 Fourier 系数为
\[
B_d=\frac1{2\pi}\int_0^{2\pi}\dd\theta_\zeta\,
\mathfrak n_e(\theta_\zeta,s_{\rm d})\ee^{-\ii d\theta_\zeta}.
\]
把密度的双重求和代入，角积分只留下 $\ell-m=d$ 的项。这解释了为什么第 $d$ 阶密度谐波需要所有相隔 $d$ 条边带的相干共同贡献。对上述纯 PINEM 输入，Bessel 和式进一步给出''')
opening('electron-gaussian-lens-analytic',r'''时间透镜的聚焦也可以直接从一个有限波包的波函数计算。取已建立的纵向二阶色散，在随中心电子运动的坐标 $\zeta=z-v_0t$ 中，包络满足含时 Schrödinger 方程（time-dependent Schrödinger equation, TDSE）''')
edit(S+'electron-gaussian-lens-analytic.tex',r'$m_\parallel=\gamma_0^3\me$ 是纵向色散曲率质量；使用它并不把实际电子换成非相对论电子。被消去的是中心能量和匀速载波相位，剩下的包络仍须满足实际占据动量范围内的高阶色散误差很小。',r'''这个方程与自由非相对论粒子的 Schrödinger 方程形式相同，但系数 $m_\parallel=\gamma_0^3\me$ 来自相对论能量的二次展开。中心能量和匀速运动已被移入载波相位，$\psi$ 只描述相对于中心电子的包络变化。它的适用条件仍是实际动量范围内高阶色散积累的相位可以忽略。''')
edit(S+'electron-gaussian-lens-analytic.tex',r'$C_\zeta$ 描述位置表象中的二次相位，不与前面动量表象的 $C_p$ 混用。代入一般解，$d=1+(C_\zeta+\ii)u_t$。利用',r'''这里 $C_\zeta$ 是无量纲实数，控制位置表象中的二次相位；前面用 $C_p$ 表示的是动量表象中的二次相位。$t_{\rm dif}$ 具有时间单位，它是无啁啾高斯包络因自由传播而明显展宽的时间尺度，$u_t$ 则以这个时间为单位。代入一般解，有 $d=1+(C_\zeta+\ii)u_t$。利用''')
edit(S+'electron-gaussian-lens-analytic.tex','聚焦没有违反不确定关系。对上述初态，直接计算动量导数给',r'''为了理解压缩过程中动量分布怎样变化，再计算位置与动量的协方差。记 $\Delta\zeta=\hat\zeta-\langle\hat\zeta\rangle$、$\Delta p=\hat p-\langle\hat p\rangle$；由于两个算符不对易，用对称乘积定义实协方差。对上述初态，在位置表象使用 $\hat p=-\ii\hbar\partial_\zeta$，得''')
edit(S+'electron-gaussian-lens-analytic.tex','这将波函数解、相空间剪切和不确定关系接到同一个可手算的结果上。','因此焦点处位置与动量不再相关，宽度乘积恰好达到最小不确定值。')
edit(S+'electron-gaussian-lens-analytic.tex','这样核积分、微分方程和概率守恒三个检查彼此独立，读者无需运行时间网格也能验证完整解。','所以传播后的函数同时满足初始条件、运动方程和归一化条件。')
opening('electron-reference-tomography-worked',r'''上一节说明可以在能谱测量前加入参考操作，将相干信息变为概率变化。现在具体计算：未知电子态只占据两个通道时，扫描四个参考相位能确定哪些矩阵元。先保留一般的参考幺正算符 $U_R(\varphi_R)$，其中 $\varphi_R$ 是可控相位；将探测结果 $m$ 的效应算符记为 $E_m^{\rm det}$。测得概率为''')
edit(S+'electron-reference-tomography-worked.tex',r'$p$ 可由不加参考场的能谱测量得到；$c_{01}=x_{01}+\ii y_{01}$ 的实部和虚部是剩下两个未知实参数。正性约束给出它们的允许圆盘，不能在重建后忽略。',r'''按 $|0\rangle,|1\rangle$ 的顺序排列基矢，$p$ 是通道 $0$ 的占据概率，可以直接测得。厄米性要求两个非对角元互为共轭，所以只剩 $c_{01}=x_{01}+\ii y_{01}$ 的实部和虚部未知。由 $\det\rho_e=p(1-p)-|c_{01}|^2\ge0$，它们必须位于半径为 $\sqrt{p(1-p)}$ 的圆盘内；这个条件保证重建结果仍是合法量子态。''')
opening('electron-detector-inversion-worked',r'''能谱仪记录的是每个能量区间内的电子数。要由理想 PINEM 边带计算这些计数，需要先加入入射能宽和仪器误差，再对各区间积分。以\eqnrefs{eq:pinem-spatial-detector-forward-dp19}为起点，设入射能量偏差与仪器加性误差为彼此独立的零均值高斯变量，标准差分别是 $\sigma_{E,\rm in}$、$\sigma_{E,\rm inst}$。记 $\varepsilon_d=E_d-E_0$ 为相对于源中心能量的读出偏差，并假设整个建模能区中的探测效率为常数 $\mathcal Q_E^{\rm det}$。在已经探测到电子这一条件下，读出能量的概率密度为''')
opening('electron-colored-noise-applications',r'''如果环境的随机频率偏移在一段时间内仍彼此相关，电子先后积累的相位也会相关。这时用一个常数衰减率描述全部演化，可能低估或高估相干。下面从一般相位噪声的关联函数出发，计算自由积累与理想回波，并用一个可解析的相关函数比较它们。''')
region(S+'electron-colored-noise-applications.tex',r'\begin{Example}[同一噪声对不同边带相干的影响]',r'\end{Example}',r'''\begin{Example}[不同阶相干对记忆误差的敏感性]
设相邻边带的相干衰减因子为 $v(t)=\exp[-\chi_{\rm free}(t)]$。求相隔 $d$ 阶的相干，以及常数率近似误差不超过 $0<\varepsilon<1$ 时允许的阶差。

由\eqnrefs{eq:electron-noise-filter-time}，相隔 $d$ 阶的因子为 $v(t)^{d^2}$。因此，即使相邻边带的相干只略有减小，更远的非对角元也可能明显衰减。记无量纲时间 $x=t/\tau_\varphi>0$、噪声强度 $a_\varphi=\sigma_\varphi\tau_\varphi>0$，则常数率近似相对于精确结果的比值为
\[
R_d=\exp[-d^2a_\varphi^2(1-\ee^{-x})].
\]
要求 $1-R_d\le\varepsilon$，对两边取对数，得到
\[
|d|\le\frac{\sqrt{-\ln(1-\varepsilon)}}
{a_\varphi\sqrt{1-\ee^{-x}}}.
\]
长时间 $x\gg1$ 时，右边趋于有限值 $\sqrt{-\ln(1-\varepsilon)}/a_\varphi$。因此延长观测时间虽使瞬时衰减率接近常数，却不会消除最初记忆阶段积累的相对幅值误差。

对理想回波，直接相减两个指数得
\[
\chi_{\rm free}-\chi_{\rm echo}
=2a_\varphi^2(1-\ee^{-x/2})^2,
\qquad
\frac{\mathcal V_d^{\rm echo}}{\mathcal V_d^{\rm free}}
=\exp[2d^2a_\varphi^2(1-\ee^{-x/2})^2].
\]
回波提高保留下来的相干，但两者在长时间仍共同衰减。若另有独立的到达时间抖动，还需乘上\eqnrefs{eq:arrival_jitter_dephasing}的衰减因子；若两种噪声相关，则必须保留交叉协方差。
''')
finish('examples')
