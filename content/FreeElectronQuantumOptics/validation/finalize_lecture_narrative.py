"""Final continuity and terminology pass over the free-electron include graph."""
import re, zipfile
from lecture_edit_support import BASE, get, edit, region, finish
edit('ch07.tex',r'将 $(z-\hat H_{\rm full})|\Psi\rangle=|f\rangle$ 分别左乘 $P$、$Q$',r'取保留空间中的源 $P|f\rangle=|f\rangle$，将 $(z-\hat H_{\rm full})|\Psi\rangle=|f\rangle$ 分别左乘 $P$、$Q$')
edit('ch07.tex',r'此时固定的 $\hat\rho_X(t_i)$ 才定义一个作用在任意电子输入态上的状态无关完全正迹保持映射。初始电子--环境相关存在时，仍使用',r'''固定同一个 $\hat\rho_X(t_i)$ 后，所得电子演化是\emph{完全正保迹}（completely positive and trace preserving, CPTP）映射。保迹指归一化态演化后总概率仍为一；完全正指即使电子预先与另一个不参与相互作用的参考系统纠缠，只对电子施加此映射，联合态仍保持非负。它们来自联合幺正演化和环境偏迹。若初始电子--环境相关存在，仍使用''')
edit('ch07.tex','同一系统的推迟电场 Green 张量是 Maxwell 算符的因果逆。谱定理把这个逆直接展开到上述本征模上：',r'''回忆对角矩阵的求逆：每个本征值分别取倒数，本征向量保持不变。Maxwell 算符也可以在刚求得的模式基底中这样求逆，得到它的 Green 张量。取推迟边界条件时，频率写为 $\omega+\ii0^+$，表示先从复频率上半平面求响应，再令正虚部趋于零。由谱展开，''')
edit('ch07.tex',r'对 $\omega>0$ 取虚部后，推迟处方把每个极点变成在壳 $\delta$ 权重：',r'''外积 $\mathbf f_\lambda(\mathbf r)\otimes\mathbf f_\lambda^*(\mathbf r')$ 的 $ij$ 分量为 $f_{\lambda i}(\mathbf r)f_{\lambda j}^*(\mathbf r')$：它先把源投影到模式 $\lambda$，再给出观察点处该模式的场。分母在模式频率附近变小，表示共振增强。对 $\omega>0$ 取虚部，并使用 $\operatorname{Im}(x-\ii0^+)^{-1}=\pi\delta(x)$，得''')
edit('ch08.tex',r'$|\Delta_{\rm ms}|\lesssim O(T^{-1})$ 的通道有效地区分为近共振。',r'满足 $|\Delta_{\rm ms}|T\lesssim1$ 的通道位于共振主峰附近。')
edit('ch08.tex','这条约化链反复使用同一组电子中心量。入射中心动量、总能量、Lorentz 因子和群速度分别定义为','为计算实际电子的速度和反冲，沿用中心动量 $p_0$，相应总能量、Lorentz 因子与群速度为')
edit('ch08.tex',r'因此 $E_{\omega,z}$ 只表示角频率 $\omega$ 的纵向复场幅度，单位为 $\mathrm{V\,m^{-1}}$；$\mathcal E_\ell$ 则只表示第 $\ell$ 个真实电子通道的能量，两者不再共享同一种花体字形。只有对一般非单色时间信号真正执行全书固定的 Fourier 变换时才使用波浪号，不能把 $E_{\omega,z}$、$\mathbf E_\omega$ 与 Fourier 变换记号混写。',r'''$E_{\omega,z}$ 的单位为 $\mathrm{V\,m^{-1}}$。实场由正频分量及其共轭相加，所以纵向实场峰值为 $2|E_{\omega,z}|$。它与单位为能量的通道能量 $\mathcal E_\ell$ 是不同的量。对一般非单色信号，Fourier 变换仍按全书约定用波浪号表示。''')
edit('ch08.tex','这一传播子是相位调制、能量边带与程函约化共同继承的精确母对象。','给定入射态后，作用这个传播子就得到出射态；后面的相位调制公式将由它在窄波包条件下的近似求得。')
edit('ch09.tex','这里仍从 Sambe 母式而不是经验平均开始。取目标子空间为','为了计算时间平均以外的修正，在前面的 Sambe 矩阵中选取目标子空间为')
edit('ch10.tex','一般约化动力学同时包含系统--环境相关、有限环境记忆和不同 Bohr 频率之间的相干交叉项。Born 截断、Markov 局域化和久期平均分别控制这三类结构；只有三个独立尺度条件都成立，时间局域生成元才进一步化成 GKSL 形式。',r'''只知道当前电子态一般不足以预测下一时刻，因为环境可能还保存先前相互作用留下的信息。我们先像消去联立方程中的未知量一样，消去环境相关，得到含历史积分的系统方程；随后再检查什么时候历史积分可以简化为只依赖当前态的演化。''')
edit('ch10.tex',r'从精确记忆方程走到常见的 Lindblad 方程需要三次彼此独立的简化。Born 近似只限制耦合展开的阶数，所以经过 Born 截断以后，方程仍然记得过去的 $\rho_S(t-\tau)$；Markov 近似才把这段历史压缩成当前态，使方程变成时间局域；久期近似最后按照系统自身的 Bohr 频率把长期快速拍频的交叉块分开。把三步分开很重要：弱耦合不等于无记忆，无记忆也不自动保证完全正的 GKSL 结构。进入相互作用绘景，写',r'''下面进行常用的弱耦合推导。先按耦合强度保留二阶项，这一步称为 Born 近似，所得方程仍含历史态 $\rho_S(t-\tau)$。若环境相关衰减得足够快，再在记忆积分中用当前态替代缓慢变化的历史态，作 Markov 近似。最后比较不同 Bohr 频率的拍频与弛豫速度，舍去长期快速振荡的交叉项，作\emph{久期近似}。在相应条件下，将得到 Gorini--Kossakowski--Sudarshan--Lindblad（GKSL）方程，通常简称 Lindblad 方程。为逐步看出这些近似，进入相互作用绘景，写''')
edit('ch11.tex',r'其中 $\mathbf n=\mathbf r/r$，而 $\widetilde{\mathbf J}(\mathbf k,\omega)$ 是空间 Fourier 电流。这个式子说明辐射的母对象是任意源电流在真空横向质量壳 $|\mathbf k|=\omega/c$ 上的投影；具体的加速轨迹、端点跳变或界面诱导电流只决定 $\widetilde{\mathbf J}$ 的结构。对给定 Fourier convention，频谱角能量由该横向远场振幅的模平方和 Parseval 恒等式得到，因此不同辐射机制共享同一“源的在壳横向分量”判据。',r'''其中 $\mathbf n=\mathbf r/r$ 是观察方向，$\widetilde{\mathbf J}$ 是电流对空间坐标的 Fourier 变换。矩阵 $\mathbf I-\mathbf n\mathbf n^{\mathsf T}$ 去掉沿观察方向的分量，只留下横向电流；自变量 $k\mathbf n$ 则选出满足真空波色散 $k=\omega/c$ 的部分。因此，求某个过程的辐射，就是先求该过程的电流，再取它在传播波矢处的横向分量。对远场振幅取模平方并使用 Parseval 恒等式，即可求每单位频率和立体角的辐射能量。''')
edit('ch11.tex','为了把这一接口真正接到可计算 Green 张量，还需要显式求平面反射核。','为求界面反射产生的电场，接下来把反射系数代入 Green 张量。')
edit('ch11.tex','PINEM 的最小实验接口。','PINEM 的基本实验几何。')

# Audit the actual chapter include graph, including older inserted subsections.
visited=[]
def walk(name):
    if name in visited: return
    visited.append(name)
    for child in re.findall(r'\\input\{([^}]+)\}',get(name)):
        if not child.endswith('.tex'): child += '.tex'
        if (BASE/child).is_file(): walk(child)
for n in range(7,12): walk(f'ch{n:02}.tex')
backup=BASE/'validation/before-lecture-terminology.zip'
if not backup.exists():
    with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
        for name in visited: z.write(BASE/name,name)
terms={
 '块母方程':'分块演化方程', '母方程':'一般动力学方程',
 '母结构':'联合动力学结构', '母对象':'基本对象', '母接口':'概率关系',
 '母顶点':'耦合算符', '母 Hamiltonian':'完整 Hamiltonian',
 '母哈密顿量':'完整哈密顿量', '母式':'一般表达式',
 '可测人口':'可测占据概率', '能级人口':'能级占据概率',
}
for name in visited:
    s=get(name)
    for old,new in terms.items():
        if old in s:
            # Log one whole-file change per token to cover every reviewed occurrence.
            updated=s.replace(old,new); edit(name,s,updated); s=updated
finish('continuity')
