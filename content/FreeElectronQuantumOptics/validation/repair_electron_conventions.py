"""One-time, bounded repairs for the reviewed electron-optics conventions."""
from pathlib import Path
BOOK=Path(__file__).resolve().parents[1]
def once(s,a,b):
    assert s.count(a)==1,(a,s.count(a))
    return s.replace(a,b)
def write(name,s): (BOOK/name).write_text(s,encoding='utf-8')

p=BOOK/'ch08.tex'; s=p.read_text(encoding='utf-8')
start=s.index(r'\begin{Derivation}[从\eqnrefs{eq:universal_free_electron_boson_hamiltonian}到\eqnrefs{eq:qpinem-single-mode-hamiltonian-dp68}]')
end=s.index(r'\end{Derivation}',start)+len(r'\end{Derivation}')
b=s[start:end]
b=once(b,"\\ee^{+\\ii[E(p')-E(p)]t/\\hbar}","\\ee^{+\\ii\\{[E(p')-E(p)]/\\hbar-\\omega_\\lambda\\}t}")
b=once(b,'这里 $\\hat{\\mathcal G}_{\\lambda,I}$ 仍作用在完整正能电子连续谱上。',r'这里将光模自由演化的 $\ee^{-\ii\omega_\lambda t}$ 也吸收到 $\hat{\mathcal G}_{\lambda,I}$ 中；$\hat a_\lambda$ 为固定的相互作用绘景模算符，不能再重复附加该相位。$\hat{\mathcal G}_{\lambda,I}$ 仍作用在完整正能电子连续谱上。')
i=b.index('最后把一个固定整体相位'); head,tail=b[:i],b[i:]
for old,new in [(r'\upsilon_\ell',r'\mathcal G_\ell'),(r'\upsilon_0',r'\mathcal G_0'),(r'\upsilon(t)',r'\mathcal G(t)'),(r'\upsilon^*(t)',r'\mathcal G^*(t)'),(r'|\upsilon|',r'|\mathcal G|'),(r'\epsilon_\upsilon',r'\epsilon_{\mathcal G}'),(r'\epsilon_\delta',r'\epsilon_\Delta'),(r'\delta_\ell',r'\Delta_\ell'),(r'\delta_0',r'\Delta_0')]: head=head.replace(old,new)
head=head.replace(r'O(\epsilon_{\mathcal G},\epsilon_\Delta)',r'O\!\left(|\mathcal G_0|(\epsilon_{\mathcal G}+\epsilon_\Delta)\right)')
tail=once(tail,'最后把一个固定整体相位吸收到 $\\upsilon(t)$ 的定义，使交换项采用反厄米生成元的常用写法，',r'保留真实矩阵元的记号 $\mathcal G(t)$，并另定义 $\upsilon(t)=-\ii\mathcal G(t)$，即 $\mathcal G(t)=\ii\upsilon(t)$。这样 $\gq=\int\upsilon(t)\dd t$ 与经典 $\beta$ 的相位对应是显式的。代入上式，')
s=s[:start]+head+tail+s[end:]
write('ch08.tex',s)

p=BOOK/'ch09.tex'; s=p.read_text(encoding='utf-8')
start=s.index(r'\subsection{Bloch--Floquet 纤维}'); end=s.index(r'\section{周期驱动与时间尺度}',start)
b=s[start:end].replace(r'\mathbf p_0',r'\mathbf p_{\rm B}').replace(r'\dd^3 p_0',r'\dd^3 p_{\rm B}')
intro=r'''“纤维”表示一组只能彼此相差倒格动量的通道。以一维周期 $a$ 为例，令 $G_1=2\pi/a$：$0.3\hbar G_1$、$1.3\hbar G_1$ 和 $2.3\hbar G_1$ 属于同组，$0.4\hbar G_1$ 属于另一组。每组保留一个连续余数，再用整数记录加了多少个倒格动量，便能重新编排整个动量轴。用 $\mathbf p_{\rm B}$ 表示第一 Brillouin 区内的准动量代表，区别于入射束的物理中心动量 $\mathbf p_0$；后者可以远在第一 Brillouin 区之外。

不同纤维“不耦合”只描述哈密顿量的分块结构，并不自动把初态变成纤维间的非相干混合。初态跨越多个准动量并保留相干时，重建空间波函数仍须叠加各纤维振幅。

'''
b=once(b,r'\subsection{Bloch--Floquet 纤维}'+'\n',r'\subsection{Bloch--Floquet 纤维}'+'\n\n'+intro)
s=s[:start]+b+s[end:]; write('ch09.tex',s)

p=BOOK/'ch10.tex'; s=p.read_text(encoding='utf-8')
start=s.index(r'\subsection{能量格相干到时间密度的定量映射}');end=s.index(r'\input{sections/electron-temporal-bunching-worked}',start)
b=s[start:end].replace('n_e',r'\mathfrak n_e').replace(r'\mathcal V_1(t)',r'\mathcal M_1(t)')
b=once(b,'最简单的相干可见度定义为','可先定义第一谐波的相对调制幅度')
b=once(b,'其中该定义适用于高阶谐波对密度极值修正较小时；完整密度对比度应直接由',r'它一般不等于限制在 $[0,1]$ 的 Michelson 可见度；只有高阶谐波可忽略时二者才一致。完整密度对比度应直接由')
s=s[:start]+b+s[end:]
s=once(s,'参考操作改变的是测量基，而不是未知态本身；','实验中参考操作先改变待测电子态，再测量能量；数学上也可把这一过程等价地写成原始未知态上的旋转测量算符。')
start=s.index(r'\subsection{时间透镜与 Talbot 传播}');end=s.index(r'\section{开放系统动力学}',start)
b=s[start:end]
b=b.replace(r'\omega\tau+\varphi_\beta',r'\varphi_\beta-\omega\tau').replace(r'\omega\tau_0+\varphi_\beta',r'\varphi_\beta-\omega\tau_0')
b=once(b,'用随电子中心运动的延迟 $\\tau$ 表示',r'用到达延迟 $\tau=t-z/v_0=-\zeta/v_0$ 表示，能量阶数 $\ell$ 的 Fourier 因子固定为 $\ee^{-\ii\ell\omega\tau}$，因此')
b=once(b,r'\delta E(\theta)=-2\hbar\omega|\beta|\cos\theta.',r'\delta E(\theta)=2\hbar\omega|\beta|\cos\theta.')
b=once(b,r'\frac{2L_z\hbar\omega|\beta|}{m_\parallel v_0^3}\cos\theta',r'-\frac{2L_z\hbar\omega|\beta|}{m_\parallel v_0^3}\cos\theta')
b=once(b,r'\delta\theta=\omega\delta\tau.',r'\delta\theta=-\omega\delta\tau.')
s=s[:start]+b+s[end:]; write('ch10.tex',s)

p=BOOK/'sections/04pinem-gaussian-worked-dp65.tex';s=p.read_text(encoding='utf-8')
s=s.replace(r'E_{\rm pk}',r'E_{\omega,0}').replace('是正频电场复振幅的峰值','是正频电场复振幅的峰值（实场余弦峰值为其模长的两倍）')
write('sections/04pinem-gaussian-worked-dp65.tex',s)
p=BOOK/'sections/04pinem-quantum-statistics-worked-dp65.tex';s=p.read_text(encoding='utf-8')
s=once(s,'量子交换传播子~\\eqnrefs{eq:qpinem_S} 在 $|\\gq|\\ll1$ 时展开为',r'量子交换传播子~\eqnrefs{eq:qpinem_S} 对 Fock 输入的弱交换条件为 $|\gq|^2(n+1)\ll1$。在实际占据范围内满足该条件后，展开为')
s=once(s,'当 $n\\gg1$ 时，两者相对差异只有 $1/n$，经典 PINEM 的近似增益--损失对称由此恢复。',r'只有同时维持 $|\gq|^2(n+1)\ll1$ 时，增大 $n$ 才使这两条弱交换率的相对差异按 $1/n$ 减小。这只检验增益--损失对称，不能据此把 Fock 输入的电子约化态视为经典相干调制后的纯态。')
write('sections/04pinem-quantum-statistics-worked-dp65.tex',s)
print('Conventions repaired in chapters 8–10 and the existing examples.')
