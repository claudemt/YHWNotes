# Poincaré 对称性、Noether 定理与曲率时空中的场论  
## ——从 Lie 群、表示论到经典场论、量子场论与协变推广

---

## 目录

1. [记号与约定](#1-记号与约定)  
2. [Poincaré 群及其 Lie 代数](#2-poincaré-群及其-lie-代数)  
3. [Poincaré 代数的统一推导](#3-poincaré-代数的统一推导)  
4. [Poincaré 群在场上的表示](#4-poincaré-群在场上的表示)  
5. [任意阶张量与旋量的 Lorentz 生成元](#5-任意阶张量与旋量的-lorentz-生成元)  
6. [Wigner 分类：场表示与粒子自旋](#6-wigner-分类场表示与粒子自旋)  
7. [最小作用量原理与 Euler–Lagrange 方程](#7-最小作用量原理与-eulerlagrange-方程)  
8. [Noether 第一定理的一般形式](#8-noether-第一定理的一般形式)  
9. [Poincaré 对称性与能动量守恒](#9-poincaré-对称性与能动量守恒)  
10. [Lorentz 对称性与 \(L+S\) 守恒](#10-lorentz-对称性与-ls-守恒)  
11. [Belinfante–Rosenfeld 改进](#11-belinfanterosenfeld-改进)  
12. [常见平直时空场论](#12-常见平直时空场论)  
13. [从 \(\Sigma_{ab}\) 到曲率时空协变导数](#13-从-sigma_ab-到曲率时空协变导数)  
14. [曲率时空中的作用量、EL 方程与 Noether 结构](#14-曲率时空中的作用量el-方程与-noether-结构)  
15. [曲率时空中的标量、矢量、张量与旋量](#15-曲率时空中的标量矢量张量与旋量)  
16. [高自旋场与受限背景](#16-高自旋场与受限背景)  
17. [动态几何：Einstein–Hilbert + matter](#17-动态几何einsteinhilbert--matter)  
18. [总结：从群论到守恒律的统一链条](#18-总结从群论到守恒律的统一链条)

---

# 1. 记号与约定

本文先在 \(d\) 维 Minkowski 时空中建立完整的 Poincaré 场论，再推广到一般 Lorentzian 曲率时空。

平直时空采用

\[
\eta_{\mu\nu}
=
\operatorname{diag}(-,+,\ldots,+),
\]

指标范围为

\[
\mu,\nu,\rho,\sigma=0,\ldots,d-1.
\]

升降指标均由 \(\eta_{\mu\nu}\) 完成。

自然单位：

\[
\hbar=c=1.
\]

Poincaré 无穷小酉表示约定为

\[
\boxed{
U(1+\omega,\epsilon)
=
I
+i\epsilon_\mu P^\mu
-\frac{i}{2}\omega_{\mu\nu}M^{\mu\nu}
+O(\epsilon^2,\omega^2,\epsilon\omega).
}
\]

其中

\[
M^{\mu\nu}=-M^{\nu\mu}.
\]

---

# 2. Poincaré 群及其 Lie 代数

## 2.1 Minkowski 时空的等距变换

Poincaré 变换定义为

\[
\boxed{
x'^\mu
=
\Lambda^\mu{}_\nu x^\nu+a^\mu,
}
\]

其中 Lorentz 矩阵满足

\[
\boxed{
\Lambda^T\eta\Lambda=\eta.
}
\]

也就是说

\[
\eta_{\rho\sigma}
\Lambda^\rho{}_\mu
\Lambda^\sigma{}_\nu
=
\eta_{\mu\nu}.
\]

因此 Minkowski 间隔

\[
ds^2=\eta_{\mu\nu}dx^\mu dx^\nu
\]

保持不变。

---

## 2.2 群乘法

设

\[
g_1=(\Lambda_1,a_1),
\qquad
g_2=(\Lambda_2,a_2).
\]

先做 \(g_1\)：

\[
x'=\Lambda_1x+a_1,
\]

再做 \(g_2\)：

\[
x''
=
\Lambda_2x'+a_2.
\]

代入：

\[
x''
=
\Lambda_2\Lambda_1x
+
\Lambda_2a_1+a_2.
\]

因此

\[
\boxed{
(\Lambda_2,a_2)(\Lambda_1,a_1)
=
(\Lambda_2\Lambda_1,\Lambda_2a_1+a_2).
}
\]

这表明

\[
\boxed{
ISO(1,d-1)
=
SO(1,d-1)\ltimes\mathbb R^{1,d-1}.
}
\]

不是直积，而是半直积。

---

## 2.3 逆元

令

\[
(\Lambda,a)^{-1}
=
(\Lambda',a').
\]

要求

\[
(\Lambda',a')(\Lambda,a)
=
(I,0).
\]

由群乘法：

\[
(\Lambda'\Lambda,\Lambda'a+a')
=
(I,0).
\]

因此

\[
\Lambda'=\Lambda^{-1},
\]

并且

\[
a'=-\Lambda^{-1}a.
\]

所以

\[
\boxed{
(\Lambda,a)^{-1}
=
(\Lambda^{-1},-\Lambda^{-1}a).
}
\]

---

# 3. Poincaré 代数的统一推导

本节不直接给出 \([P,P]\)、\([M,P]\)、\([M,M]\) 三组公式，而是从群结构和 Lie 代数定义逐步推导。

---

## 3.1 Lorentz Lie 代数

取恒等元附近

\[
\Lambda=I+\omega+O(\omega^2).
\]

Lorentz 条件

\[
\Lambda^T\eta\Lambda=\eta
\]

给出

\[
(I+\omega)^T\eta(I+\omega)
=
\eta.
\]

保留一阶：

\[
\omega^T\eta+\eta\omega=0.
\]

定义

\[
\omega_{\mu\nu}
=
\eta_{\mu\rho}\omega^\rho{}_\nu,
\]

则

\[
\boxed{
\omega_{\mu\nu}
=
-\omega_{\nu\mu}.
}
\]

所以 Lorentz 群在 \(d\) 维有

\[
\frac{d(d-1)}2
\]

个独立生成元。

---

## 3.2 半直积 Lie bracket

Poincaré Lie 代数元素写成

\[
X=(\omega,a),
\]

其中

\[
\omega\in\mathfrak{so}(1,d-1),
\qquad
a\in\mathbb R^{1,d-1}.
\]

考虑两条一参数群：

\[
g_1(t)
=
(e^{t\omega_1},ta_1)+O(t^2),
\]

\[
g_2(s)
=
(e^{s\omega_2},sa_2)+O(s^2).
\]

Lie bracket 可以由群交换子定义：

\[
g_1(t)g_2(s)g_1(t)^{-1}g_2(s)^{-1}
=
I+ts[X_1,X_2]+O(t^2,s^2,t^2s,ts^2).
\]

利用群乘法

\[
(\Lambda_2,a_2)(\Lambda_1,a_1)
=
(\Lambda_2\Lambda_1,\Lambda_2a_1+a_2)
\]

逐阶展开。

Lorentz 部分：

\[
e^{t\omega_1}
e^{s\omega_2}
e^{-t\omega_1}
e^{-s\omega_2}
=
I+ts[\omega_1,\omega_2]+\cdots.
\]

平移部分在 \(ts\) 阶给出

\[
ts(\omega_1a_2-\omega_2a_1).
\]

因此：

\[
\boxed{
[(\omega_1,a_1),(\omega_2,a_2)]
=
\left(
[\omega_1,\omega_2],
\omega_1a_2-\omega_2a_1
\right).
}
\]

这是一条式子给出全部 Poincaré Lie 代数。

---

## 3.3 由统一 bracket 推出 \([P,P]=0\)

纯平移对应

\[
X_1=(0,a_1),
\qquad
X_2=(0,a_2).
\]

代入：

\[
[(0,a_1),(0,a_2)]
=
(0,0).
\]

因此

\[
\boxed{
[P_\mu,P_\nu]=0.
}
\]

这反映平移子群

\[
\mathbb R^{1,d-1}
\]

是 Abel 群。

---

## 3.4 由统一 bracket 推出 \([M,P]\)

取

\[
X_1=(\omega,0),
\qquad
X_2=(0,a).
\]

则

\[
[(\omega,0),(0,a)]
=
(0,\omega a).
\]

所以 Lorentz 生成元对平移生成元的伴随作用正是矢量表示。

设

\[
\omega^\mu{}_\nu
=
\frac12
\omega_{\rho\sigma}
(J^{\rho\sigma}_{V})^\mu{}_\nu,
\]

其中矢量表示的 Lorentz 生成元必须满足

\[
(\omega a)^\mu
=
\omega^\mu{}_\nu a^\nu.
\]

定义

\[
\boxed{
(J_V^{\rho\sigma})^\mu{}_\nu
=
i
\left(
\eta^{\rho\mu}\delta^\sigma{}_\nu
-
\eta^{\sigma\mu}\delta^\rho{}_\nu
\right).
}
\]

于是

\[
[M^{\rho\sigma},P^\mu]
\]

必须按照同一矢量表示作用，即

\[
\boxed{
[M^{\rho\sigma},P^\mu]
=
i
\left(
\eta^{\rho\mu}P^\sigma
-
\eta^{\sigma\mu}P^\rho
\right).
}
\]

等价地，降指标后

\[
\boxed{
[M_{\rho\sigma},P_\mu]
=
i
\left(
\eta_{\rho\mu}P_\sigma
-
\eta_{\sigma\mu}P_\rho
\right).
}
\]

---

## 3.5 由 Lorentz 矩阵表示推导 \([M,M]\)

在矢量表示中定义

\[
\boxed{
(J^{\mu\nu})^\rho{}_\sigma
=
i
\left(
\eta^{\mu\rho}\delta^\nu{}_\sigma
-
\eta^{\nu\rho}\delta^\mu{}_\sigma
\right).
}
\]

直接计算矩阵乘积：

\[
(J^{\mu\nu}J^{\rho\sigma})^\alpha{}_\beta
=
(J^{\mu\nu})^\alpha{}_\gamma
(J^{\rho\sigma})^\gamma{}_\beta.
\]

代入定义：

\[
(J^{\mu\nu}J^{\rho\sigma})^\alpha{}_\beta
=
-
\left(
\eta^{\mu\alpha}\delta^\nu{}_\gamma
-
\eta^{\nu\alpha}\delta^\mu{}_\gamma
\right)
\left(
\eta^{\rho\gamma}\delta^\sigma{}_\beta
-
\eta^{\sigma\gamma}\delta^\rho{}_\beta
\right).
\]

展开：

\[
\begin{aligned}
(J^{\mu\nu}J^{\rho\sigma})^\alpha{}_\beta
=
-&
\eta^{\mu\alpha}\eta^{\rho\nu}\delta^\sigma{}_\beta
+
\eta^{\mu\alpha}\eta^{\sigma\nu}\delta^\rho{}_\beta
\\
+&
\eta^{\nu\alpha}\eta^{\rho\mu}\delta^\sigma{}_\beta
-
\eta^{\nu\alpha}\eta^{\sigma\mu}\delta^\rho{}_\beta.
\end{aligned}
\]

再交换

\[
(\mu,\nu)\leftrightarrow(\rho,\sigma)
\]

并相减，最终得到

\[
\boxed{
\begin{aligned}
[J^{\mu\nu},J^{\rho\sigma}]
=
i\Big(
&
\eta^{\mu\rho}J^{\nu\sigma}
-\eta^{\mu\sigma}J^{\nu\rho}
\\
&
-\eta^{\nu\rho}J^{\mu\sigma}
+\eta^{\nu\sigma}J^{\mu\rho}
\Big).
\end{aligned}
}
\]

由于 Lie 代数的结构常数与具体忠实表示无关，所以一般 Lorentz 生成元 \(M^{\mu\nu}\) 满足

\[
\boxed{
\begin{aligned}
[M^{\mu\nu},M^{\rho\sigma}]
=
i\Big(
&
\eta^{\mu\rho}M^{\nu\sigma}
-\eta^{\mu\sigma}M^{\nu\rho}
\\
&
-\eta^{\nu\rho}M^{\mu\sigma}
+\eta^{\nu\sigma}M^{\mu\rho}
\Big).
\end{aligned}
}
\]

---

## 3.6 Poincaré Lie 代数总结

因此

\[
\boxed{
[P^\mu,P^\nu]=0,
}
\]

\[
\boxed{
[M^{\mu\nu},P^\rho]
=
i(
\eta^{\mu\rho}P^\nu
-
\eta^{\nu\rho}P^\mu
),
}
\]

\[
\boxed{
\begin{aligned}
[M^{\mu\nu},M^{\rho\sigma}]
=
i\Big(
&
\eta^{\mu\rho}M^{\nu\sigma}
-\eta^{\mu\sigma}M^{\nu\rho}
\\
&
-\eta^{\nu\rho}M^{\mu\sigma}
+\eta^{\nu\sigma}M^{\mu\rho}
\Big).
\end{aligned}
}
\]

---

## 3.7 单一扩展指标公式

若希望把以上三个关系压缩成一条指标公式，可定义

\[
J_{AB}=-J_{BA},
\qquad
A,B=0,\ldots,d,
\]

并规定

\[
J_{\mu\nu}=M_{\mu\nu},
\qquad
J_{\mu d}=P_\mu.
\]

再引入退化双线性形式

\[
\boxed{
\widehat\eta_{AB}
=
\begin{pmatrix}
\eta_{\mu\nu}&0\\
0&0
\end{pmatrix}.
}
\]

则

\[
\boxed{
[J_{AB},J_{CD}]
=
i\left(
\widehat\eta_{AC}J_{BD}
-\widehat\eta_{AD}J_{BC}
-\widehat\eta_{BC}J_{AD}
+\widehat\eta_{BD}J_{AC}
\right).
}
\]

这条式子不是把 Poincaré 群误认为普通 \(SO(p,q)\)，而只是利用退化双线性形式编码半直积结构。

---

# 4. Poincaré 群在场上的表示

## 4.1 有限变换

设场为

\[
\Phi^A(x),
\]

其中 \(A\) 代表某个有限维 Lorentz 表示。

采用如下约定：

\[
\boxed{
U(\Lambda,a)
\Phi^A(x)
U^{-1}(\Lambda,a)
=
D(\Lambda^{-1})^A{}_B
\Phi^B(\Lambda x+a).
}
\]

其中

\[
D(\Lambda_2\Lambda_1)
=
D(\Lambda_2)D(\Lambda_1).
\]

---

## 4.2 为什么 \(D(\Lambda)\) 必须是表示

连续做两次 Lorentz 变换：

\[
\Phi'
=
D(\Lambda_1)\Phi,
\]

\[
\Phi''
=
D(\Lambda_2)\Phi'.
\]

所以

\[
\Phi''
=
D(\Lambda_2)D(\Lambda_1)\Phi.
\]

另一方面两次变换合并为

\[
\Lambda_2\Lambda_1,
\]

因此必须有

\[
D(\Lambda_2\Lambda_1)
=
D(\Lambda_2)D(\Lambda_1).
\]

---

## 4.3 场表示的无穷小生成元

写

\[
\Lambda=I+\omega.
\]

因为

\[
\omega_{\mu\nu}=-\omega_{\nu\mu},
\]

一般有限维表示可写为

\[
\boxed{
D(I+\omega)
=
I
-\frac{i}{2}
\omega_{\mu\nu}\Sigma^{\mu\nu}.
}
\]

于是

\[
\boxed{
\Sigma^{\mu\nu}
=
-\Sigma^{\nu\mu}.
}
\]

这些 \(\Sigma^{\mu\nu}\) 满足与 \(M^{\mu\nu}\) 相同的 Lorentz Lie 代数。

---

## 4.4 无穷小场变换

定义

\[
\xi^\mu
=
\epsilon^\mu+\omega^\mu{}_\nu x^\nu.
\]

由

\[
\Phi(\Lambda x+a)
=
\Phi(x)
+
\xi^\rho\partial_\rho\Phi(x)
+O(\xi^2),
\]

以及

\[
D(\Lambda^{-1})
=
I+\frac{i}{2}\omega_{\mu\nu}\Sigma^{\mu\nu},
\]

得到

\[
\boxed{
\delta\Phi^A
=
\xi^\rho\partial_\rho\Phi^A
+
\frac{i}{2}
\omega_{\mu\nu}
(\Sigma^{\mu\nu})^A{}_B\Phi^B.
}
\]

---

## 4.5 总 Lorentz 生成元

Lorentz 部分：

\[
\delta_\omega\Phi
=
\omega^\mu{}_\nu x^\nu\partial_\mu\Phi
+
\frac{i}{2}
\omega_{\mu\nu}\Sigma^{\mu\nu}\Phi.
\]

利用 \(\omega_{\mu\nu}\) 的反对称性：

\[
\omega^\mu{}_\nu x^\nu\partial_\mu
=
-\frac{i}{2}
\omega_{\mu\nu}
\,i(x^\mu\partial^\nu-x^\nu\partial^\mu).
\]

定义

\[
\boxed{
L^{\mu\nu}
=
i(x^\mu\partial^\nu-x^\nu\partial^\mu).
}
\]

于是

\[
\boxed{
M^{\mu\nu}_{\rm field}
=
L^{\mu\nu}+\Sigma^{\mu\nu}.
}
\]

也就是说 Lorentz 生成元天然分为：

\[
\boxed{
\text{orbital}+\text{intrinsic}.
}
\]

---

# 5. 任意阶张量与旋量的 Lorentz 生成元

## 5.1 标量

若

\[
\phi'(x')=\phi(x),
\]

则

\[
D(\Lambda)=1.
\]

所以

\[
\boxed{
\Sigma^{\mu\nu}=0.
}
\]

---

## 5.2 矢量

四矢量满足

\[
V'^\rho
=
\Lambda^\rho{}_\sigma V^\sigma.
\]

无穷小：

\[
\delta V^\rho
=
\omega^\rho{}_\sigma V^\sigma.
\]

另一方面

\[
\delta V^\rho
=
-\frac{i}{2}
\omega_{\mu\nu}
(\Sigma^{\mu\nu})^\rho{}_\sigma
V^\sigma.
\]

比较系数得到

\[
\boxed{
(\Sigma^{\mu\nu})^\rho{}_\sigma
=
i(
\eta^{\mu\rho}\delta^\nu{}_\sigma
-
\eta^{\nu\rho}\delta^\mu{}_\sigma
).
}
\]

---

## 5.3 协变矢量

由

\[
V_\rho
=
\eta_{\rho\sigma}V^\sigma
\]

可得

\[
\boxed{
(\Sigma^{\mu\nu}V)_\rho
=
i(
\delta^\mu{}_\rho V^\nu
-
\delta^\nu{}_\rho V^\mu
).
}
\]

---

## 5.4 任意 \((r,s)\) 张量

考虑

\[
T^{\alpha_1\cdots\alpha_r}
{}_{\beta_1\cdots\beta_s}.
\]

Lorentz 变换对每一个指标独立作用，因此总生成元是各指标生成元之和：

\[
\boxed{
\Sigma^{\mu\nu}_{(r,s)}
=
\sum_{k=1}^{r}
\Sigma^{\mu\nu}_{(V,k)}
+
\sum_{\ell=1}^{s}
\Sigma^{\mu\nu}_{(V^\ast,\ell)}.
}
\]

显式地：

\[
\begin{aligned}
(\Sigma^{\mu\nu}T)^{\alpha_1\cdots\alpha_r}
{}_{\beta_1\cdots\beta_s}
=
i\sum_{k=1}^{r}
\Big(
&
\eta^{\mu\alpha_k}
T^{\alpha_1\cdots\nu\cdots\alpha_r}
{}_{\beta_1\cdots\beta_s}
\\
-&
\eta^{\nu\alpha_k}
T^{\alpha_1\cdots\mu\cdots\alpha_r}
{}_{\beta_1\cdots\beta_s}
\Big)
\\
+i\sum_{\ell=1}^{s}
\Big(
&
\delta^\mu{}_{\beta_\ell}
T^{\alpha_1\cdots\alpha_r}
{}_{\beta_1\cdots\nu\cdots\beta_s}
\\
-&
\delta^\nu{}_{\beta_\ell}
T^{\alpha_1\cdots\alpha_r}
{}_{\beta_1\cdots\mu\cdots\beta_s}
\Big).
\end{aligned}
\]

这就是任意阶普通 Lorentz 张量的统一公式。

---

## 5.5 二阶张量

对于

\[
T^{\rho\sigma},
\]

有

\[
\boxed{
\Sigma_{(2)}^{\mu\nu}
=
\Sigma_{(1)}^{\mu\nu}\otimes I
+
I\otimes\Sigma_{(1)}^{\mu\nu}.
}
\]

显式地：

\[
\boxed{
\begin{aligned}
(\Sigma^{\mu\nu}T)^{\rho\sigma}
=
i\Big[
&
\eta^{\mu\rho}T^{\nu\sigma}
-
\eta^{\nu\rho}T^{\mu\sigma}
\\
&
+
\eta^{\mu\sigma}T^{\rho\nu}
-
\eta^{\nu\sigma}T^{\rho\mu}
\Big].
\end{aligned}
}
\]

---

## 5.6 \(p\)-form

完全反对称张量

\[
A_{\mu_1\cdots\mu_p}
=
A_{[\mu_1\cdots\mu_p]}
\]

仍然使用 \((0,p)\) 张量生成元。

场强定义：

\[
\boxed{
F_{\mu_0\cdots\mu_p}
=
(p+1)
\partial_{[\mu_0}
A_{\mu_1\cdots\mu_p]}.
}
\]

---

## 5.7 Dirac 旋量

Clifford algebra：

\[
\boxed{
\{\gamma^\mu,\gamma^\nu\}
=
2\eta^{\mu\nu}.
}
\]

要求旋量表示满足

\[
D(\Lambda)\gamma^\rho D^{-1}(\Lambda)
=
\Lambda^\rho{}_\sigma\gamma^\sigma.
\]

无穷小展开：

\[
D(\Lambda)
=
I-\frac{i}{2}\omega_{\mu\nu}\Sigma^{\mu\nu}.
\]

比较一阶项可得

\[
\boxed{
\Sigma^{\mu\nu}
=
\frac{i}{4}
[\gamma^\mu,\gamma^\nu].
}
\]

因此 Dirac 场上的总 Lorentz 生成元

\[
\boxed{
M^{\mu\nu}
=
i(x^\mu\partial^\nu-x^\nu\partial^\mu)
+
\frac{i}{4}
[\gamma^\mu,\gamma^\nu].
}
\]

---

## 5.8 四维 Weyl 表示

在 \(d=4\)，

\[
Spin(1,3)\simeq SL(2,\mathbb C).
\]

有限维不可约表示由

\[
(j_L,j_R)
\]

标记。

常见表示：

| 场 | Lorentz 表示 |
|---|---|
| 标量 | \((0,0)\) |
| 左手 Weyl | \((\frac12,0)\) |
| 右手 Weyl | \((0,\frac12)\) |
| Dirac | \((\frac12,0)\oplus(0,\frac12)\) |
| 四矢量 | \((\frac12,\frac12)\) |
| 自对偶二形式 | \((1,0)\) |
| 反自对偶二形式 | \((0,1)\) |
| 一般二形式 | \((1,0)\oplus(0,1)\) |
| 对称无迹 rank-2 | \((1,1)\) |

---

## 5.9 张量-旋量

若场同时有张量指标和 spinor 指标，则总生成元是张量积表示的和：

\[
\boxed{
\Sigma^{\mu\nu}_{\rm total}
=
\Sigma^{\mu\nu}_{\rm tensor}\otimes I
+
I\otimes\Sigma^{\mu\nu}_{\rm spinor}.
}
\]

例如 vector-spinor

\[
\psi_\rho
\]

属于

\[
\left(\frac12,\frac12\right)
\otimes
\left[
\left(\frac12,0\right)
\oplus
\left(0,\frac12\right)
\right].
\]

---

# 6. Wigner 分类：场表示与粒子自旋

必须区分：

\[
\boxed{
\text{Lorentz 场表示}
\neq
\text{Poincaré 单粒子不可约表示}.
}
\]

单粒子态按照 Poincaré 群不可约酉表示分类。

---

## 6.1 第一 Casimir

\[
\boxed{
P^2=P_\mu P^\mu.
}
\]

对于 massive particle：

\[
\boxed{
P^2=-m^2.
}
\]

---

## 6.2 Pauli–Lubanski 向量

四维定义

\[
\boxed{
W^\mu
=
\frac12
\epsilon^{\mu\nu\rho\sigma}
P_\nu M_{\rho\sigma}.
}
\]

第二 Casimir：

\[
\boxed{
W^2=W_\mu W^\mu.
}
\]

massive spin-\(s\)：

\[
\boxed{
W^2
=
m^2s(s+1).
}
\]

无质量粒子则由 little group 分类。

---

# 7. 最小作用量原理与 Euler–Lagrange 方程

## 7.1 一阶局域场论

考虑

\[
S[\Phi]
=
\int d^dx\,
\mathcal L(\Phi^A,\partial_\mu\Phi^A).
\]

作任意变分：

\[
\Phi^A
\to
\Phi^A+\delta\Phi^A.
\]

有

\[
\delta S
=
\int d^dx
\left[
\frac{\partial\mathcal L}{\partial\Phi^A}\delta\Phi^A
+
\frac{\partial\mathcal L}
{\partial(\partial_\mu\Phi^A)}
\partial_\mu\delta\Phi^A
\right].
\]

定义

\[
\boxed{
\Pi_A^\mu
=
\frac{\partial\mathcal L}
{\partial(\partial_\mu\Phi^A)}.
}
\]

分部积分：

\[
\Pi_A^\mu\partial_\mu\delta\Phi^A
=
\partial_\mu(\Pi_A^\mu\delta\Phi^A)
-
(\partial_\mu\Pi_A^\mu)\delta\Phi^A.
\]

因此

\[
\delta S
=
\int d^dx
\left[
\left(
\frac{\partial\mathcal L}{\partial\Phi^A}
-
\partial_\mu\Pi_A^\mu
\right)\delta\Phi^A
+
\partial_\mu(\Pi_A^\mu\delta\Phi^A)
\right].
\]

若变分在边界消失，则边界项不贡献。

由于 \(\delta\Phi^A\) 任意：

\[
\boxed{
\frac{\partial\mathcal L}{\partial\Phi^A}
-
\partial_\mu
\frac{\partial\mathcal L}
{\partial(\partial_\mu\Phi^A)}
=
0.
}
\]

---

## 7.2 一般高阶导数 EL 方程

若

\[
\mathcal L
=
\mathcal L
(
\Phi,
\partial\Phi,
\ldots,
\partial^N\Phi
),
\]

反复分部积分得到

\[
\boxed{
\sum_{k=0}^{N}
(-1)^k
\partial_{\mu_1}\cdots\partial_{\mu_k}
\left[
\frac{
\partial\mathcal L
}{
\partial(
\partial_{\mu_1}\cdots
\partial_{\mu_k}\Phi^A
)
}
\right]
=
0.
}
\]

---

# 8. Noether 第一定理的一般形式

## 8.1 变分恒等式

任何局域场论的变分都可以写成

\[
\boxed{
\delta\mathcal L
=
E_A\delta\Phi^A
+
\partial_\mu\Theta^\mu(\Phi,\delta\Phi).
}
\]

其中

\[
E_A=0
\]

就是 Euler–Lagrange 方程。

对一阶理论，

\[
\boxed{
\Theta^\mu
=
\Pi_A^\mu\delta\Phi^A.
}
\]

---

## 8.2 连续对称

若某一参数连续变换使

\[
\boxed{
\delta\mathcal L
=
\partial_\mu K^\mu,
}
\]

则

\[
E_A\delta\Phi^A
+
\partial_\mu
\left(
\Theta^\mu-K^\mu
\right)
=
0.
\]

定义 Noether 流

\[
\boxed{
J^\mu
=
\Theta^\mu-K^\mu.
}
\]

因此有 off-shell 恒等式

\[
\boxed{
\partial_\mu J^\mu
=
-E_A\delta\Phi^A.
}
\]

在运动方程成立时：

\[
\boxed{
\partial_\mu J^\mu=0.
}
\]

---

# 9. Poincaré 对称性与能动量守恒

## 9.1 平移变换

纯平移：

\[
x^\mu\to x^\mu+\epsilon^\mu.
\]

场变化：

\[
\boxed{
\delta\Phi^A
=
\epsilon^\nu\partial_\nu\Phi^A.
}
\]

若理论不显含 \(x\)，则

\[
\delta\mathcal L
=
\epsilon^\nu\partial_\nu\mathcal L.
\]

因为 \(\epsilon^\nu\) 为常数：

\[
\delta\mathcal L
=
\partial_\mu
(
\epsilon^\mu\mathcal L
).
\]

所以

\[
\boxed{
K^\mu
=
\epsilon^\mu\mathcal L.
}
\]

---

## 9.2 Noether 流

一阶理论中

\[
\Theta^\mu
=
\Pi_A^\mu
\epsilon^\nu\partial_\nu\Phi^A.
\]

因此

\[
J^\mu
=
\epsilon^\nu
\Pi_A^\mu\partial_\nu\Phi^A
-
\epsilon^\mu\mathcal L.
\]

写成

\[
J^\mu
=
\epsilon^\nu
\left[
\Pi_A^\mu\partial_\nu\Phi^A
-
\delta^\mu{}_\nu\mathcal L
\right].
\]

定义 canonical energy-momentum tensor：

\[
\boxed{
T^\mu{}_\nu
=
\Pi_A^\mu\partial_\nu\Phi^A
-
\delta^\mu{}_\nu\mathcal L.
}
\]

所以

\[
\boxed{
J^\mu_{\rm trans}
=
\epsilon^\nu T^\mu{}_\nu.
}
\]

因为 \(\epsilon^\nu\) 任意：

\[
\boxed{
\partial_\mu T^\mu{}_\nu=0.
}
\]

---

## 9.3 守恒荷

由连续性方程

\[
\partial_0T^{0\nu}
+
\partial_iT^{i\nu}
=
0
\]

对空间积分：

\[
\frac{d}{dt}
\int d^{d-1}x\,T^{0\nu}
=
-
\int d^{d-1}x\,
\partial_iT^{i\nu}.
\]

若空间无穷远表面通量消失，则

\[
\boxed{
P^\nu
=
\int d^{d-1}x\,T^{0\nu}
}
\]

守恒。

---

# 10. Lorentz 对称性与 \(L+S\) 守恒

## 10.1 场的 Lorentz 变化

纯 Lorentz 变换：

\[
\epsilon^\mu=0.
\]

于是

\[
\xi^\mu
=
\omega^\mu{}_\nu x^\nu.
\]

场变分：

\[
\delta\Phi^A
=
\omega^\rho{}_\sigma
x^\sigma\partial_\rho\Phi^A
+
\frac{i}{2}
\omega_{\mu\nu}
(\Sigma^{\mu\nu})^A{}_B\Phi^B.
\]

---

## 10.2 拉氏量的变化

因为 \(\mathcal L\) 是 Lorentz scalar，

\[
\delta\mathcal L
=
\xi^\rho\partial_\rho\mathcal L.
\]

又由于

\[
\partial_\rho\xi^\rho
=
\omega^\rho{}_\rho
=
0,
\]

所以

\[
\delta\mathcal L
=
\partial_\rho
(
\xi^\rho\mathcal L
).
\]

因此

\[
\boxed{
K^\lambda
=
\xi^\lambda\mathcal L.
}
\]

---

## 10.3 Noether 流

\[
J^\lambda
=
\Pi_A^\lambda\delta\Phi^A
-
\xi^\lambda\mathcal L.
\]

代入：

\[
\begin{aligned}
J^\lambda
=
&
\omega^\rho{}_\sigma
x^\sigma
\left(
\Pi_A^\lambda\partial_\rho\Phi^A
-
\delta^\lambda{}_\rho\mathcal L
\right)
\\
&
+
\frac{i}{2}
\omega_{\mu\nu}
\Pi_A^\lambda
(\Sigma^{\mu\nu})^A{}_B
\Phi^B.
\end{aligned}
\]

第一括号就是

\[
T^\lambda{}_\rho.
\]

利用 \(\omega_{\mu\nu}\) 反对称性：

\[
\omega^\rho{}_\sigma
x^\sigma T^\lambda{}_\rho
=
-\frac12
\omega_{\mu\nu}
\left(
x^\mu T^{\lambda\nu}
-
x^\nu T^{\lambda\mu}
\right).
\]

定义轨道角动量流

\[
\boxed{
L^{\lambda\mu\nu}
=
x^\mu T^{\lambda\nu}
-
x^\nu T^{\lambda\mu}.
}
\]

再定义 spin current

\[
\boxed{
S^{\lambda\mu\nu}
=
-i
\Pi_A^\lambda
(\Sigma^{\mu\nu})^A{}_B
\Phi^B.
}
\]

于是

\[
\boxed{
J^\lambda_{\rm Lorentz}
=
-\frac12
\omega_{\mu\nu}
\left(
L^{\lambda\mu\nu}
+
S^{\lambda\mu\nu}
\right).
}
\]

定义

\[
\boxed{
J^{\lambda\mu\nu}
=
L^{\lambda\mu\nu}
+
S^{\lambda\mu\nu}.
}
\]

因此

\[
\boxed{
\partial_\lambda J^{\lambda\mu\nu}=0.
}
\]

---

## 10.4 Lorentz 守恒荷

\[
\boxed{
M^{\mu\nu}
=
\int d^{d-1}x\,
J^{0\mu\nu}.
}
\]

即

\[
\boxed{
M^{\mu\nu}
=
\int d^{d-1}x
\left[
x^\mu T^{0\nu}
-
x^\nu T^{0\mu}
+
S^{0\mu\nu}
\right].
}
\]

于是完整 Poincaré charge

\[
\boxed{
Q[\epsilon,\omega]
=
\epsilon_\mu P^\mu
-
\frac12
\omega_{\mu\nu}M^{\mu\nu}.
}
\]

从而

\[
\boxed{
U=1+iQ.
}
\]

---

## 10.5 canonical \(T^{\mu\nu}\) 的反对称部分

由

\[
\partial_\lambda
J^{\lambda\mu\nu}=0
\]

展开：

\[
0
=
\partial_\lambda
(
x^\mu T^{\lambda\nu}
-
x^\nu T^{\lambda\mu}
+
S^{\lambda\mu\nu}
).
\]

利用

\[
\partial_\lambda T^{\lambda\nu}=0,
\]

得到

\[
\boxed{
T^{\mu\nu}
-
T^{\nu\mu}
+
\partial_\lambda S^{\lambda\mu\nu}
=
0.
}
\]

即

\[
\boxed{
2T^{[\mu\nu]}
=
-\partial_\lambda
S^{\lambda\mu\nu}.
}
\]

---

# 11. Belinfante–Rosenfeld 改进

定义

\[
\boxed{
B^{\lambda\mu\nu}
=
\frac12
\left(
S^{\lambda\mu\nu}
+
S^{\mu\nu\lambda}
+
S^{\nu\mu\lambda}
\right).
}
\]

令

\[
\boxed{
T_B^{\mu\nu}
=
T_{\rm can}^{\mu\nu}
+
\partial_\lambda
B^{\lambda\mu\nu}.
}
\]

利用上一节关系可以证明：

\[
\boxed{
T_B^{\mu\nu}=T_B^{\nu\mu}.
}
\]

另一方面，

\[
B^{\lambda\mu\nu}
=
-B^{\mu\lambda\nu},
\]

所以

\[
\partial_\mu\partial_\lambda
B^{\lambda\mu\nu}
=
0.
\]

因此

\[
\boxed{
\partial_\mu T_B^{\mu\nu}=0.
}
\]

总角动量流可以改写成

\[
\boxed{
J_B^{\lambda\mu\nu}
=
x^\mu T_B^{\lambda\nu}
-
x^\nu T_B^{\lambda\mu}.
}
\]

也就是说自旋信息被重新吸收到对称的能动量张量中。

---

# 12. 常见平直时空场论

## 12.1 实标量场

\[
\boxed{
\mathcal L
=
-\frac12
\partial_\mu\phi
\partial^\mu\phi
-
\frac12
m^2\phi^2.
}
\]

变分：

\[
\delta\mathcal L
=
-\partial_\mu\phi\,
\partial^\mu\delta\phi
-
m^2\phi\delta\phi.
\]

分部积分：

\[
\delta S
=
\int d^dx
\left(
\Box\phi-m^2\phi
\right)\delta\phi.
\]

所以

\[
\boxed{
(\Box-m^2)\phi=0.
}
\]

由于

\[
\Sigma^{\mu\nu}=0,
\]

因此

\[
\boxed{
S^{\lambda\mu\nu}=0.
}
\]

---

## 12.2 复标量场

\[
\boxed{
\mathcal L
=
-\partial_\mu\phi^\ast
\partial^\mu\phi
-
m^2\phi^\ast\phi.
}
\]

分别对 \(\phi\)、\(\phi^\ast\) 变分：

\[
\boxed{
(\Box-m^2)\phi=0,
}
\]

\[
\boxed{
(\Box-m^2)\phi^\ast=0.
}
\]

全局 \(U(1)\)：

\[
\phi\to e^{i\alpha}\phi.
\]

无穷小

\[
\delta\phi=i\alpha\phi,
\qquad
\delta\phi^\ast=-i\alpha\phi^\ast.
\]

Noether 流：

\[
\boxed{
j^\mu
=
i
\left(
\phi^\ast\partial^\mu\phi
-
\phi\partial^\mu\phi^\ast
\right).
}
\]

---

## 12.3 Maxwell 场

\[
\boxed{
F_{\mu\nu}
=
\partial_\mu A_\nu
-
\partial_\nu A_\mu.
}
\]

作用量

\[
\boxed{
S
=
-\frac14
\int d^dx\,
F_{\mu\nu}F^{\mu\nu}.
}
\]

变分：

\[
\delta F_{\mu\nu}
=
\partial_\mu\delta A_\nu
-
\partial_\nu\delta A_\mu.
\]

因此

\[
\delta S
=
-\frac12
\int d^dx\,
F^{\mu\nu}
(
\partial_\mu\delta A_\nu
-
\partial_\nu\delta A_\mu
).
\]

利用 \(F^{\mu\nu}=-F^{\nu\mu}\)：

\[
\delta S
=
-\int d^dx\,
F^{\mu\nu}
\partial_\mu\delta A_\nu.
\]

分部积分：

\[
\delta S
=
\int d^dx\,
(\partial_\mu F^{\mu\nu})
\delta A_\nu.
\]

所以

\[
\boxed{
\partial_\mu F^{\mu\nu}=0.
}
\]

Bianchi 恒等式：

\[
\boxed{
\partial_{[\lambda}F_{\mu\nu]}=0.
}
\]

对称 gauge-invariant 能动量张量：

\[
\boxed{
T_{\mu\nu}
=
F_{\mu\rho}F_\nu{}^\rho
-
\frac14
\eta_{\mu\nu}
F_{\rho\sigma}F^{\rho\sigma}.
}
\]

---

## 12.4 Proca 场

\[
\boxed{
\mathcal L
=
-\frac14F_{\mu\nu}F^{\mu\nu}
-\frac12m^2A_\mu A^\mu.
}
\]

变分得到

\[
\boxed{
\partial_\mu F^{\mu\nu}
-
m^2A^\nu=0.
}
\]

取 \(\partial_\nu\)：

\[
-m^2\partial_\nu A^\nu=0.
\]

故 \(m\neq0\) 时

\[
\boxed{
\partial_\mu A^\mu=0.
}
\]

---

## 12.5 任意 \(p\)-form

令

\[
A_p
=
\frac1{p!}
A_{\mu_1\cdots\mu_p}
dx^{\mu_1}\wedge\cdots\wedge dx^{\mu_p}.
\]

定义

\[
\boxed{
F_{p+1}=dA_p.
}
\]

作用量

\[
\boxed{
S
=
-\frac12
\int F_{p+1}\wedge\star F_{p+1}.
}
\]

变分：

\[
\delta F=d(\delta A).
\]

所以

\[
\delta S
=
-\int d(\delta A)\wedge\star F.
\]

分部积分：

\[
\delta S
=
(-1)^p
\int
\delta A\wedge d\star F
\]

忽略边界项。

故

\[
\boxed{
d\star F=0.
}
\]

再加定义恒等式

\[
\boxed{
dF=0.
}
\]

---

## 12.6 Dirac 场

\[
\boxed{
\mathcal L_D
=
\bar\psi
(i\gamma^\mu\partial_\mu-m)\psi.
}
\]

对 \(\bar\psi\) 变分：

\[
\boxed{
(i\gamma^\mu\partial_\mu-m)\psi=0.
}
\]

对 \(\psi\) 变分：

\[
\boxed{
i(\partial_\mu\bar\psi)\gamma^\mu
+
m\bar\psi=0.
}
\]

常用对称能动量张量：

\[
\boxed{
T^{\mu\nu}
=
\frac{i}{4}
\left[
\bar\psi\gamma^\mu
\overleftrightarrow{\partial^\nu}\psi
+
\bar\psi\gamma^\nu
\overleftrightarrow{\partial^\mu}\psi
\right].
}
\]

---

## 12.7 Weyl 场

四维左手 Weyl 场：

\[
\chi_\alpha
\in
\left(\frac12,0\right).
\]

作用量

\[
\boxed{
S
=
\int d^4x\,
i\chi^\dagger
\bar\sigma^\mu
\partial_\mu\chi.
}
\]

场方程

\[
\boxed{
i\bar\sigma^\mu\partial_\mu\chi=0.
}
\]

---

## 12.8 Rarita–Schwinger 场

vector-spinor：

\[
\psi_\mu.
\]

自由质量零作用量：

\[
\boxed{
S_{\rm RS}
=
-\int d^4x\,
\bar\psi_\mu
\gamma^{\mu\nu\rho}
\partial_\nu\psi_\rho.
}
\]

场方程：

\[
\boxed{
\gamma^{\mu\nu\rho}
\partial_\nu\psi_\rho=0.
}
\]

gauge symmetry：

\[
\boxed{
\delta\psi_\mu
=
\partial_\mu\epsilon.
}
\]

---

## 12.9 Fierz–Pauli spin-2

令

\[
h_{\mu\nu}=h_{\nu\mu},
\qquad
h=\eta^{\mu\nu}h_{\mu\nu}.
\]

作用量

\[
\boxed{
\begin{aligned}
\mathcal L_{\rm FP}
=
&
-\frac12
\partial_\lambda h_{\mu\nu}
\partial^\lambda h^{\mu\nu}
+
\partial_\mu h^{\mu\nu}
\partial^\lambda h_{\lambda\nu}
\\
&
-
\partial_\mu h^{\mu\nu}
\partial_\nu h
+
\frac12
\partial_\lambda h
\partial^\lambda h
\\
&
-
\frac12m^2
(
h_{\mu\nu}h^{\mu\nu}-h^2
).
\end{aligned}
}
\]

特殊质量组合

\[
\boxed{
h_{\mu\nu}h^{\mu\nu}-h^2
}
\]

保证线性理论中不引入额外标量 ghost。

---

# 13. 从 \(\Sigma_{ab}\) 到曲率时空协变导数

这是从平直到曲率最关键的桥梁。

---

## 13.1 vielbein

一般曲率时空中不能在全局使用同一个 Minkowski frame。

引入 vielbein：

\[
\boxed{
g_{\mu\nu}
=
e^a{}_\mu
e^b{}_\nu
\eta_{ab}.
}
\]

逆 vielbein 满足

\[
e^\mu{}_a e^a{}_\nu
=
\delta^\mu{}_\nu,
\]

\[
e^\mu{}_a e^b{}_\mu
=
\delta_a{}^b.
\]

---

## 13.2 为什么需要 spin connection

在每个点的 tangent space 中仍有局域 Lorentz 变换：

\[
e^a{}_\mu
\to
\Lambda^a{}_b(x)e^b{}_\mu.
\]

场若处于某个 Lorentz 表示 \(\Sigma^{ab}\)，则

\[
\Phi
\to
D(\Lambda(x))\Phi.
\]

由于 \(\Lambda\) 依赖于 \(x\)，

\[
\partial_\mu\Phi
\]

不再按同一表示协变。

确实，

\[
\partial_\mu(D\Phi)
=
D\partial_\mu\Phi
+
(\partial_\mu D)\Phi.
\]

第二项破坏协变性。

因此必须引入 connection。

---

## 13.3 一般表示上的协变导数

定义

\[
\boxed{
D_\mu
=
\partial_\mu
-
\frac{i}{2}
\omega_{\mu ab}\Sigma^{ab}.
}
\]

要求

\[
D'_\mu\Phi'
=
D(\Lambda)
D_\mu\Phi.
\]

由此可以推导 spin connection 的变换律：

\[
\boxed{
\omega'_\mu
=
\Lambda\omega_\mu\Lambda^{-1}
-
(\partial_\mu\Lambda)\Lambda^{-1}.
}
\]

这里把

\[
\omega_\mu
=
-\frac{i}{2}
\omega_{\mu ab}\Sigma^{ab}
\]

视作 Lie algebra-valued connection。

---

## 13.4 不同表示只是 \(\Sigma^{ab}\) 不同

这是统一性的关键：

### 标量

\[
\Sigma^{ab}=0
\]

所以

\[
\boxed{
D_\mu\phi=\partial_\mu\phi.
}
\]

### Lorentz 矢量

\[
(\Sigma^{ab})^c{}_d
=
i(
\eta^{ac}\delta^b{}_d
-
\eta^{bc}\delta^a{}_d
).
\]

于是

\[
D_\mu V^a
=
\partial_\mu V^a
+
\omega_\mu{}^a{}_bV^b.
\]

### Dirac spinor

\[
\Sigma^{ab}
=
\frac{i}{4}
[\gamma^a,\gamma^b].
\]

所以

\[
\boxed{
D_\mu\psi
=
\left(
\partial_\mu
-
\frac{i}{2}
\omega_{\mu ab}\Sigma^{ab}
\right)\psi.
}
\]

### 任意 tensor-spinor

只需取

\[
\boxed{
\Sigma^{ab}_{\rm total}
=
\Sigma^{ab}_{\rm tensor}
+
\Sigma^{ab}_{\rm spinor}.
}
\]

同一个

\[
D_\mu
=
\partial_\mu-\frac{i}{2}\omega_{\mu ab}\Sigma^{ab}
\]

统一适用。

---

## 13.5 与坐标协变导数的关系

若将 Lorentz 指标转为坐标指标：

\[
V^\mu
=
e^\mu{}_aV^a,
\]

要求

\[
D_\mu e^a{}_\nu=0.
\]

即 tetrad postulate：

\[
\boxed{
\partial_\mu e^a{}_\nu
+
\omega_\mu{}^a{}_b e^b{}_\nu
-
\Gamma^\rho_{\mu\nu}e^a{}_\rho
=
0.
}
\]

它把 spin connection 与 affine connection 联系起来。

---

# 14. 曲率时空中的作用量、EL 方程与 Noether 结构

## 14.1 强假设

为了得到受控而自洽的曲率时空场论，作以下假设：

1. \(M\) 是光滑 Lorentzian manifold；
2. 存在 Levi–Civita connection；
3. 作用量局域且 diffeomorphism covariant；
4. 若存在 spinor，则 \(M\) admits a spin structure；
5. 高自旋场在需要时限制到 Einstein 或 maximally symmetric background；
6. 若讨论 QFT，则背景几何先视为经典给定。

---

## 14.2 作用量

一般形式：

\[
\boxed{
S[\Phi;g]
=
\int d^dx
\sqrt{|g|}
\,
\mathcal L
(
\Phi,
D\Phi,
g,
R,
R_{\mu\nu},
R_{\mu\nu\rho\sigma},
\ldots
).
}
\]

minimal coupling 是最简单选择：

\[
\eta_{\mu\nu}\to g_{\mu\nu},
\]

\[
\partial_\mu\to\nabla_\mu
\quad\text{或}\quad
D_\mu,
\]

\[
d^dx
\to
d^dx\sqrt{|g|}.
\]

但一般还允许非最小曲率耦合。

---

## 14.3 曲率时空 EL 方程

最简单的一阶情形：

\[
S
=
\int d^dx\sqrt{|g|}
\mathcal L(
\Phi^A,D_\mu\Phi^A
).
\]

变分：

\[
\delta S
=
\int d^dx\sqrt{|g|}
\left[
\frac{\partial\mathcal L}{\partial\Phi^A}
\delta\Phi^A
+
\frac{\partial\mathcal L}
{\partial(D_\mu\Phi^A)}
D_\mu\delta\Phi^A
\right].
\]

定义

\[
\Pi_A^\mu
=
\frac{\partial\mathcal L}
{\partial(D_\mu\Phi^A)}.
\]

利用协变分部积分：

\[
\int d^dx\sqrt{|g|}
\Pi_A^\mu D_\mu\delta\Phi^A
=
-
\int d^dx\sqrt{|g|}
(D_\mu\Pi_A^\mu)\delta\Phi^A
\]

忽略边界项。

所以

\[
\boxed{
\frac{\partial\mathcal L}{\partial\Phi^A}
-
D_\mu
\frac{\partial\mathcal L}
{\partial(D_\mu\Phi^A)}
=
0.
}
\]

---

## 14.4 Hilbert 能动量张量

定义

\[
\boxed{
T_{\mu\nu}
=
-\frac2{\sqrt{|g|}}
\frac{\delta S_m}{\delta g^{\mu\nu}}.
}
\]

于是

\[
\delta_gS_m
=
-\frac12
\int d^dx\sqrt{|g|}
T_{\mu\nu}\delta g^{\mu\nu}.
\]

因为

\[
\delta g^{\mu\nu}
=
\delta g^{\nu\mu},
\]

所以

\[
\boxed{
T_{\mu\nu}=T_{\nu\mu}.
}
\]

---

## 14.5 diffeomorphism invariance 推出协变守恒

无穷小 diffeomorphism 由 \(\xi^\mu\) 生成。

度规 Lie 导数：

\[
\boxed{
\delta_\xi g_{\mu\nu}
=
\nabla_\mu\xi_\nu
+
\nabla_\nu\xi_\mu.
}
\]

在物质场方程成立时：

\[
0
=
\delta_\xi S_m
=
\frac12
\int d^dx\sqrt{|g|}
T^{\mu\nu}
(
\nabla_\mu\xi_\nu+\nabla_\nu\xi_\mu
).
\]

由于 \(T^{\mu\nu}\) 对称：

\[
0
=
\int d^dx\sqrt{|g|}
T^{\mu\nu}
\nabla_\mu\xi_\nu.
\]

协变分部积分：

\[
0
=
-
\int d^dx\sqrt{|g|}
(\nabla_\mu T^{\mu\nu})\xi_\nu.
\]

因 \(\xi^\nu\) 任意：

\[
\boxed{
\nabla_\mu T^{\mu\nu}=0.
}
\]

---

## 14.6 Killing vector 与守恒流

若

\[
\xi^\mu
\]

满足 Killing 方程：

\[
\boxed{
\nabla_{(\mu}\xi_{\nu)}=0,
}
\]

定义

\[
\boxed{
J^\mu_\xi
=
T^\mu{}_\nu\xi^\nu.
}
\]

则

\[
\nabla_\mu J^\mu_\xi
=
(\nabla_\mu T^{\mu\nu})\xi_\nu
+
T^{\mu\nu}\nabla_\mu\xi_\nu.
\]

第一项为零。

第二项：

\[
T^{\mu\nu}\nabla_\mu\xi_\nu
=
\frac12
T^{\mu\nu}
(
\nabla_\mu\xi_\nu+\nabla_\nu\xi_\mu
)
=
0.
\]

因此

\[
\boxed{
\nabla_\mu J^\mu_\xi=0.
}
\]

守恒荷：

\[
\boxed{
Q_\xi
=
\int_\Sigma
d\Sigma_\mu
\,T^\mu{}_\nu\xi^\nu.
}
\]

---

# 15. 曲率时空中的标量、矢量、张量与旋量

## 15.1 标量场

作用量：

\[
\boxed{
S_\phi
=
-\frac12
\int d^dx\sqrt{|g|}
\left[
\nabla_\mu\phi\nabla^\mu\phi
+
m^2\phi^2
+
\xi R\phi^2
\right].
}
\]

变分：

\[
\delta S_\phi
=
-\int d^dx\sqrt{|g|}
\left[
\nabla_\mu\phi\nabla^\mu\delta\phi
+
(m^2+\xi R)\phi\delta\phi
\right].
\]

分部积分：

\[
\delta S_\phi
=
\int d^dx\sqrt{|g|}
\left[
\Box_g\phi
-
m^2\phi
-
\xi R\phi
\right]
\delta\phi.
\]

所以

\[
\boxed{
(\Box_g-m^2-\xi R)\phi=0.
}
\]

---

## 15.2 Maxwell 场

定义

\[
F_{\mu\nu}
=
\nabla_\mu A_\nu
-
\nabla_\nu A_\mu.
\]

Levi–Civita connection 对称，因此

\[
F_{\mu\nu}
=
\partial_\mu A_\nu-\partial_\nu A_\mu.
\]

作用量：

\[
\boxed{
S_A
=
-\frac14
\int d^dx\sqrt{|g|}
F_{\mu\nu}F^{\mu\nu}.
}
\]

变分得到

\[
\boxed{
\nabla_\mu F^{\mu\nu}=0.
}
\]

Hilbert tensor：

\[
\boxed{
T_{\mu\nu}
=
F_{\mu\rho}F_\nu{}^\rho
-
\frac14
g_{\mu\nu}
F_{\rho\sigma}F^{\rho\sigma}.
}
\]

---

## 15.3 Proca 场

\[
\boxed{
S
=
\int d^dx\sqrt{|g|}
\left[
-\frac14F_{\mu\nu}F^{\mu\nu}
-\frac12m^2A_\mu A^\mu
\right].
}
\]

EL：

\[
\boxed{
\nabla_\mu F^{\mu\nu}
-
m^2A^\nu=0.
}
\]

取协变散度：

\[
\nabla_\nu\nabla_\mu F^{\mu\nu}
-
m^2\nabla_\nu A^\nu=0.
\]

第一项因反对称张量与曲率恒等式消失，因此

\[
\boxed{
\nabla_\mu A^\mu=0
\qquad(m\neq0).
}
\]

---

## 15.4 一般 \(p\)-form

\[
F_{p+1}=dA_p.
\]

作用量：

\[
\boxed{
S
=
-\frac12
\int
F_{p+1}\wedge\star F_{p+1}.
}
\]

场方程：

\[
\boxed{
d\star F=0,
}
\]

Bianchi：

\[
\boxed{
dF=0.
}
\]

---

## 15.5 一般张量场

压缩全部张量指标为 \(A\)。

可考虑二次作用量：

\[
\boxed{
S_T
=
-\frac12
\int d^dx\sqrt{|g|}
\left[
(D_\rho T_A)(D^\rho T^A)
+
m^2T_AT^A
+
\sum_i
c_i
\mathcal R_i{}_{AB}
T^AT^B
\right].
}
\]

其中

\[
\mathcal R_i
\]

代表允许的

\[
R,\quad
R_{\mu\nu},\quad
R_{\mu\nu\rho\sigma}
\]

与场指标的各种 contraction。

变分得到一般形式：

\[
\boxed{
(-D^2+m^2)T_A
+
\sum_i
c_i
\mathcal R_i{}_A{}^BT_B
=
0.
}
\]

若要求只传播某个不可约 spin，还必须附加 trace、divergence 或 gauge constraints。

---

## 15.6 Dirac 场

定义 curved gamma matrices：

\[
\boxed{
\gamma^\mu
=
e^\mu{}_a\gamma^a.
}
\]

它们满足

\[
\boxed{
\{\gamma^\mu,\gamma^\nu\}
=
2g^{\mu\nu}.
}
\]

spinor covariant derivative：

\[
\boxed{
D_\mu\psi
=
\left(
\partial_\mu
-
\frac{i}{2}
\omega_{\mu ab}\Sigma^{ab}
\right)\psi.
}
\]

其中

\[
\Sigma^{ab}
=
\frac{i}{4}
[\gamma^a,\gamma^b].
\]

Hermitian Dirac action：

\[
\boxed{
S_D
=
\int d^dx\,e
\left[
\frac{i}{2}
\left(
\bar\psi\gamma^\mu D_\mu\psi
-
(D_\mu\bar\psi)\gamma^\mu\psi
\right)
-
m\bar\psi\psi
\right].
}
\]

对 \(\bar\psi\) 变分：

\[
\boxed{
(i\gamma^\mu D_\mu-m)\psi=0.
}
\]

---

## 15.7 Dirac 能动量张量

\[
\boxed{
\begin{aligned}
T_{\mu\nu}
=
\frac{i}{4}
\Big[
&
\bar\psi\gamma_\mu D_\nu\psi
+
\bar\psi\gamma_\nu D_\mu\psi
\\
&
-
(D_\nu\bar\psi)\gamma_\mu\psi
-
(D_\mu\bar\psi)\gamma_\nu\psi
\Big].
\end{aligned}
}
\]

on-shell：

\[
\boxed{
\nabla_\mu T^{\mu\nu}=0.
}
\]

---

## 15.8 局域 Lorentz spin current

若把

\[
e^a{}_\mu,
\qquad
\omega_\mu{}^{ab}
\]

作为独立背景变量，则定义

\[
\boxed{
\tau^\mu{}_a
=
\frac1e
\frac{\delta S_m}{\delta e^a{}_\mu},
}
\]

\[
\boxed{
s^\mu{}_{ab}
=
\frac2e
\frac{\delta S_m}
{\delta\omega_\mu{}^{ab}}.
}
\]

局域 Lorentz 变换

\[
\delta e^a{}_\mu
=
\lambda^a{}_b e^b{}_\mu,
\]

\[
\delta\omega_\mu{}^{ab}
=
-D_\mu\lambda^{ab}.
\]

作用量不变给出

\[
\boxed{
\tau_{[ab]}
+
\frac12
D_\mu s^\mu{}_{ab}
=
0.
}
\]

这正是平直时空

\[
T^{[\mu\nu]}
+
\frac12
\partial_\lambda S^{\lambda\mu\nu}
=
0
\]

的曲率时空版本。

---

# 16. 高自旋场与受限背景

## 16.1 为什么简单 \(\partial\to\nabla\) 不总成立

在平直时空：

\[
[\partial_\mu,\partial_\nu]=0.
\]

在曲率时空：

\[
\boxed{
[\nabla_\mu,\nabla_\nu]T
\sim
R_{\mu\nu}\cdot T.
}
\]

因此高自旋场原本依赖导数交换的 gauge identity 会产生额外曲率项。

所以

\[
\boxed{
\text{高自旋理论通常不能只靠 }
\partial_\mu\to\nabla_\mu
\text{ 完成。}
}
\]

---

## 16.2 Rarita–Schwinger 场

作强假设：

\[
R_{\mu\nu}=0.
\]

取

\[
\boxed{
S_{\rm RS}
=
-\int d^4x\,e\,
\bar\psi_\mu
\gamma^{\mu\nu\rho}
D_\nu\psi_\rho.
}
\]

EL 方程：

\[
\boxed{
\gamma^{\mu\nu\rho}
D_\nu\psi_\rho=0.
}
\]

质量零 gauge transformation：

\[
\boxed{
\delta\psi_\mu
=
D_\mu\epsilon.
}
\]

在一般背景上该 gauge symmetry 会受到 curvature obstruction。

---

## 16.3 spin-2：从 Einstein–Hilbert 展开

不要机械地将 Fierz–Pauli 中的

\[
\partial
\]

换成

\[
\nabla.
\]

更可靠的方法是从

\[
\boxed{
S_{\rm EH}
=
\frac1{2\kappa}
\int d^dx\sqrt{|g|}
(R-2\Lambda)
}
\]

出发。

取背景

\[
\bar g_{\mu\nu}
\]

满足背景 Einstein 方程，并展开：

\[
\boxed{
g_{\mu\nu}
=
\bar g_{\mu\nu}
+
\kappa h_{\mu\nu}.
}
\]

把作用量展开到二阶：

\[
S_{\rm EH}
=
S[\bar g]
+
S^{(1)}[h]
+
S^{(2)}[h]
+\cdots.
\]

背景满足方程时

\[
S^{(1)}=0.
\]

所以

\[
S^{(2)}[h]
\]

就是一致的 linear spin-2 action。

线性场方程：

\[
\boxed{
\delta G_{\mu\nu}[h]
+
\Lambda h_{\mu\nu}
=
\kappa\,\delta T_{\mu\nu}.
}
\]

---

## 16.4 一般高自旋

若背景 maximally symmetric：

\[
\boxed{
R_{\mu\nu\rho\sigma}
=
K
(
g_{\mu\rho}g_{\nu\sigma}
-
g_{\mu\sigma}g_{\nu\rho}
),
}
\]

高自旋场可以通过加入曲率相关项恢复 gauge consistency。

形式上：

\[
\boxed{
\mathcal F_g[\phi]
+
K\,\mathcal A[\phi]
=
0.
}
\]

---

# 17. 动态几何：Einstein–Hilbert + matter

若 \(g_{\mu\nu}\) 也作为动力学变量：

\[
\boxed{
S[g,\Phi]
=
\frac1{2\kappa}
\int d^dx\sqrt{|g|}
(R-2\Lambda)
+
S_m[g,\Phi].
}
\]

对 \(g^{\mu\nu}\) 变分：

\[
\boxed{
G_{\mu\nu}
+
\Lambda g_{\mu\nu}
=
\kappa T_{\mu\nu}.
}
\]

对物质场：

\[
\boxed{
E_A[\Phi,g]=0.
}
\]

Bianchi identity：

\[
\boxed{
\nabla_\mu G^{\mu\nu}=0.
}
\]

因此

\[
\boxed{
\nabla_\mu T^{\mu\nu}=0.
}
\]

---

## 17.1 半经典重力

若物质量子化、几何仍经典：

\[
\boxed{
G_{\mu\nu}
+
\Lambda g_{\mu\nu}
=
\kappa
\langle
\widehat T_{\mu\nu}
\rangle_{\rm ren}.
}
\]

这是 semiclassical gravity。

它不是完整 quantum gravity。

---

# 18. 总结：从群论到守恒律的统一链条

整个结构可以压缩为以下几步。

---

## 18.1 群结构

\[
\boxed{
ISO(1,d-1)
=
SO(1,d-1)\ltimes\mathbb R^{1,d-1}.
}
\]

---

## 18.2 Lie bracket

\[
\boxed{
[(\omega_1,a_1),(\omega_2,a_2)]
=
(
[\omega_1,\omega_2],
\omega_1a_2-\omega_2a_1
).
}
\]

它一次性给出

\[
[P,P]=0,
\]

\[
[M,P]\sim P,
\]

\[
[M,M]\sim M.
\]

---

## 18.3 场表示

\[
\boxed{
M^{\mu\nu}
=
L^{\mu\nu}
+
\Sigma^{\mu\nu}.
}
\]

任意张量、旋量、张量-旋量都只是在选择不同的

\[
\Sigma^{\mu\nu}.
\]

---

## 18.4 作用量原理

\[
\boxed{
\delta S=0
}
\]

推出

\[
\boxed{
E_A=0.
}
\]

---

## 18.5 Noether 恒等式

\[
\boxed{
\delta\mathcal L
=
E_A\delta\Phi^A
+
\partial_\mu\Theta^\mu.
}
\]

若

\[
\delta\mathcal L
=
\partial_\mu K^\mu,
\]

则

\[
\boxed{
J^\mu
=
\Theta^\mu-K^\mu,
}
\]

并有

\[
\boxed{
\partial_\mu J^\mu
=
-E_A\delta\Phi^A.
}
\]

---

## 18.6 Poincaré 守恒流

平移：

\[
\boxed{
\partial_\mu T^{\mu\nu}=0.
}
\]

Lorentz：

\[
\boxed{
\partial_\lambda
\left(
x^\mu T^{\lambda\nu}
-
x^\nu T^{\lambda\mu}
+
S^{\lambda\mu\nu}
\right)
=
0.
}
\]

---

## 18.7 曲率时空统一桥梁

对任意 Lorentz 表示：

\[
\boxed{
D_\mu
=
\partial_\mu
-
\frac{i}{2}
\omega_{\mu ab}\Sigma^{ab}.
}
\]

这一个公式统一了：

- scalar；
- vector；
- arbitrary tensor；
- spinor；
- tensor-spinor。

---

## 18.8 曲率时空守恒律

\[
\boxed{
\nabla_\mu T^{\mu\nu}=0.
}
\]

若存在 Killing vector：

\[
\boxed{
J^\mu_\xi
=
T^\mu{}_\nu\xi^\nu,
\qquad
\nabla_\mu J^\mu_\xi=0.
}
\]

于是

\[
\boxed{
Q_\xi
=
\int_\Sigma
d\Sigma_\mu\,
T^\mu{}_\nu\xi^\nu.
}
\]

---

## 18.9 最终逻辑

\[
\boxed{
\text{Lie group}
\to
\text{Lie algebra}
\to
\text{representation}
\to
\text{field transformation}
\to
\text{action}
\to
\text{Euler--Lagrange}
\to
\text{Noether current}
\to
\text{conserved charge}.
}
\]

平直时空中：

\[
\boxed{
P^\mu,\quad M^{\mu\nu}
}
\]

是 Poincaré 生成元。

曲率时空中，全局 Poincaré 对称一般消失，而被

\[
\boxed{
\text{diffeomorphism covariance}
+
\text{local Lorentz symmetry}
}
\]

所取代。



---

# 19. 一般自旋与螺旋度：量子场论中的表示、自由度与常见应用

这一节把前面的 Lorentz 场表示

\[
\Sigma^{\mu\nu}
\]

与真正的单粒子自旋/螺旋度联系起来。

最重要的原则是

\[
\boxed{
\text{场所处的 Lorentz 表示}
\neq
\text{物理单粒子的 Poincaré 不可约表示}.
}
\]

例如：

- \(A_\mu\) 是 Lorentz 四矢量，但无质量 photon 只有 \(h=\pm1\) 两个物理 helicity；
- \(h_{\mu\nu}\) 是二阶对称张量，但无质量 graviton 只有 \(h=\pm2\)；
- vector-spinor \(\psi_\mu\) 包含多个 Lorentz 分量，但 Rarita–Schwinger 约束只留下 spin-\(\frac32\) 的物理部分。

---

## 19.1 Massive particle：little group \(SO(3)\)

四维 massive particle 满足

\[
P^2=-m^2,
\qquad
m>0.
\]

可以进入静止系：

\[
p^\mu=(m,\mathbf 0).
\]

保持该四动量不变的 Lorentz 变换组成 little group

\[
\boxed{
SO(3)
}
\]

或其双覆盖

\[
\boxed{
SU(2).
}
\]

因此 massive 单粒子态由普通角动量表示分类：

\[
\boxed{
s=0,\frac12,1,\frac32,\ldots
}
\]

并具有

\[
\boxed{
2s+1
}
\]

个自旋极化态。

Pauli–Lubanski Casimir 满足

\[
\boxed{
W^2
=
m^2s(s+1).
}
\]

因此 massive spin 是真正的 Lorentz invariant representation label。

---

## 19.2 Massless particle：little group \(ISO(2)\)

无质量粒子满足

\[
P^2=0.
\]

取标准动量

\[
k^\mu=(E,0,0,E).
\]

保持它不变的 little group 是

\[
\boxed{
ISO(2).
}
\]

普通局域 QFT 中最常见的是其平移子群平凡作用的有限 helicity 表示。

此时 Pauli–Lubanski 向量满足

\[
\boxed{
W^\mu
=
hP^\mu,
}
\]

其中

\[
\boxed{
h
}
\]

就是 helicity。

对 proper orthochronous Lorentz group，massless helicity 是 Lorentz invariant。

一个 parity-invariant 的实无质量 bosonic field 通常同时含有

\[
\boxed{
h=+s,\qquad h=-s.
}
\]

但 chiral theory 可以只保留一侧。

---

## 19.3 Massive spin 与 massless helicity 的自由度计数

在四维：

### massive spin-\(s\)

\[
\boxed{
N_{\rm dof}=2s+1.
}
\]

### massless finite-helicity spin-\(s\)

通常

\[
\boxed{
N_{\rm dof}=2
}
\]

对应

\[
h=\pm s.
\]

对 chiral field 可以只有一个 helicity sector。

这就是为什么

\[
m\neq0
\]

与

\[
m=0
\]

的同一“spin”场在自由度结构上存在本质差别。

---

# 20. spin-0：标量与赝标量

## 20.1 自由场

Lorentz 表示：

\[
\boxed{
(0,0).
}
\]

粒子自旋：

\[
\boxed{
s=0.
}
\]

作用量：

\[
\boxed{
\mathcal L
=
-\frac12
(\partial\phi)^2
-
\frac12m^2\phi^2.
}
\]

物理自由度：

\[
\boxed{
1.
}
\]

---

## 20.2 QFT 中常见应用

### Higgs-like scalar

标准的重整化势：

\[
\boxed{
V(\phi)
=
\frac12m^2\phi^2
+
\frac{\lambda}{4!}\phi^4.
}
\]

### Yukawa coupling

标量与 fermion 最常见的局域耦合：

\[
\boxed{
\mathcal L_Y
=
-y\phi\bar\psi\psi.
}
\]

若 \(\phi\) 是 pseudoscalar，则常见形式为

\[
\boxed{
\mathcal L_{\rm ps}
=
-iy_5
\phi
\bar\psi\gamma^5\psi.
}
\]

### 有效场论中的 Goldstone boson

Goldstone 场通常表现为 derivatively coupled scalar：

\[
\boxed{
\mathcal L_{\rm EFT}
=
\frac12
(\partial\pi)^2
+
\frac{c_4}{\Lambda^4}
(\partial\pi)^4
+\cdots.
}
\]

常见应用包括：

- Higgs sector；
- pion/chiral perturbation theory；
- inflaton；
- axion/axion-like particle；
- order parameter field。

---

# 21. spin-\(\frac12\)：Weyl、Dirac 与 Majorana

## 21.1 Massive Dirac particle

Dirac field：

\[
\boxed{
\psi
\in
\left(\frac12,0\right)
\oplus
\left(0,\frac12\right).
}
\]

满足

\[
\boxed{
(i\slashed\partial-m)\psi=0.
}
\]

单个 massive particle 有

\[
\boxed{
2s+1=2
}
\]

个 spin states。

量子场还同时包含 antiparticle 模式，因此 Dirac field 的 mode expansion 包含：

- 两个 particle spin states；
- 两个 antiparticle spin states。

---

## 21.2 Massless Weyl fermion 与 helicity

左手 Weyl field：

\[
\boxed{
\chi_\alpha
\in
\left(\frac12,0\right).
}
\]

右手 Weyl field：

\[
\boxed{
\bar\eta^{\dot\alpha}
\in
\left(0,\frac12\right).
}
\]

massless limit 中 chirality 与 helicity 紧密对应。

在常用 convention 下：

\[
\boxed{
\text{left-handed particle}
\;\Longleftrightarrow\;
h=-\frac12,
}
\]

\[
\boxed{
\text{right-handed particle}
\;\Longleftrightarrow\;
h=+\frac12.
}
\]

相应 antiparticle helicity 相反。

---

## 21.3 QFT 应用

最典型应用：

- quarks；
- charged leptons；
- neutrinos；
- chiral gauge theory；
- supersymmetry 中的 gaugino/higgsino；
- Majorana dark matter。

---

## 21.4 Vector current 与 gauge coupling

Dirac current：

\[
\boxed{
j^\mu
=
\bar\psi\gamma^\mu\psi.
}
\]

与 spin-1 gauge field 的最基本耦合：

\[
\boxed{
\mathcal L_{\rm int}
=
-gA_\mu j^\mu.
}
\]

即

\[
\boxed{
\mathcal L_{\rm int}
=
-g
A_\mu
\bar\psi\gamma^\mu\psi.
}
\]

写成协变导数：

\[
\boxed{
D_\mu
=
\partial_\mu+igA_\mu.
}
\]

于是

\[
\boxed{
\mathcal L
=
\bar\psi(i\gamma^\mu D_\mu-m)\psi.
}
\]

---

# 22. spin-1：photon、gluon、\(W/Z\) 与 Proca 场

## 22.1 Lorentz field 与物理态的区别

四矢量场：

\[
\boxed{
A_\mu
\in
\left(\frac12,\frac12\right).
}
\]

它有四个 Lorentz components。

但这不代表一个 photon 有四个 physical polarizations。

---

## 22.2 Massive spin-1

Proca 方程：

\[
\boxed{
\partial_\mu F^{\mu\nu}
-
m^2A^\nu=0.
}
\]

由此推出

\[
\boxed{
\partial_\mu A^\mu=0.
}
\]

四个场分量减去一个约束，留下

\[
\boxed{
3
}
\]

个极化：

\[
\boxed{
\lambda=-1,0,+1.
}
\]

这正是

\[
2s+1=3.
\]

---

## 22.3 Massive vector polarization sum

取

\[
p^2=-m^2.
\]

物理极化满足

\[
p^\mu\epsilon_\mu^{(\lambda)}=0.
\]

在本文 signature 下 completeness relation 为

\[
\boxed{
\sum_{\lambda=-1}^{1}
\epsilon_\mu^{(\lambda)}(p)
\epsilon_\nu^{(\lambda)\ast}(p)
=
g_{\mu\nu}
+
\frac{p_\mu p_\nu}{m^2}.
}
\]

---

## 22.4 Massless spin-1

Maxwell theory：

\[
\boxed{
\mathcal L
=
-\frac14F_{\mu\nu}F^{\mu\nu}.
}
\]

gauge redundancy：

\[
\boxed{
A_\mu
\to
A_\mu+\partial_\mu\alpha.
}
\]

最终只剩

\[
\boxed{
h=\pm1.
}
\]

也就是说 photon 只有两个 transverse helicities。

---

## 22.5 QFT 应用

### photon

\[
\boxed{
U(1)
}
\]

gauge boson。

### gluon

\[
\boxed{
SU(3)_c
}
\]

adjoint gauge boson，仍然是 massless helicity

\[
\boxed{
h=\pm1.
}
\]

额外的 color index 与 Lorentz helicity 是独立的内部自由度。

### \(W^\pm,Z\)

电弱对称破缺后成为 massive spin-1：

\[
\boxed{
\lambda=-1,0,+1.
}
\]

纵向极化

\[
\lambda=0
\]

与 Higgs/Goldstone sector 密切相关。

高能极限下 Goldstone equivalence theorem 将 longitudinal \(W/Z\) 与相应 Goldstone mode 联系起来。

---

# 23. spin-\(\frac32\)：Rarita–Schwinger 与 gravitino

## 23.1 vector-spinor 的冗余分量

\[
\psi_\mu
\]

同时具有 vector 与 spinor 指标。

所以 Lorentz 表示中不仅包含 spin-\(\frac32\)，还包含 spin-\(\frac12\) 成分。

因此必须通过方程与约束去除不需要的低自旋部分。

---

## 23.2 Massive spin-\(\frac32\)

一般需要条件

\[
\boxed{
(\slashed p-m)\psi_\mu=0,
}
\]

\[
\boxed{
p^\mu\psi_\mu=0,
}
\]

\[
\boxed{
\gamma^\mu\psi_\mu=0.
}
\]

这些约束共同留下

\[
\boxed{
2s+1=4
}
\]

个物理态：

\[
\boxed{
\lambda=
-\frac32,
-\frac12,
+\frac12,
+\frac32.
}
\]

---

## 23.3 Massless spin-\(\frac32\)

Rarita–Schwinger gauge symmetry：

\[
\boxed{
\delta\psi_\mu
=
\partial_\mu\epsilon.
}
\]

gauge redundancy 去除低 helicity 成分，最终保留

\[
\boxed{
h=\pm\frac32.
}
\]

---

## 23.4 QFT 中常见应用

### gravitino

超引力中 graviton 的 supersymmetric partner：

\[
\boxed{
s=\frac32.
}
\]

在 local supersymmetry 破缺后，gravitino 可以获得质量。

这对应 super-Higgs mechanism。

### hadronic EFT

spin-\(\frac32\) baryon resonance，例如 \(\Delta\)-type resonance，可用 Rarita–Schwinger field 作为有效描述。

---

# 24. spin-2：graviton 与 massive spin-2

## 24.1 对称二阶张量

\[
\boxed{
h_{\mu\nu}=h_{\nu\mu}.
}
\]

在四维一开始有

\[
10
\]

个 components。

---

## 24.2 Massless spin-2

线性化 diffeomorphism：

\[
\boxed{
\delta h_{\mu\nu}
=
\partial_\mu\xi_\nu
+
\partial_\nu\xi_\mu.
}
\]

规范冗余与 constraint 最终只留下

\[
\boxed{
h=\pm2.
}
\]

因此 massless graviton 有两个物理 helicity。

---

## 24.3 spin-2 与能动量张量的普适耦合

线性化引力最重要的耦合：

\[
\boxed{
\mathcal L_{\rm int}
=
-\frac{\kappa}{2}
h_{\mu\nu}T^{\mu\nu}.
}
\]

因此：

\[
\boxed{
\text{spin-1 gauge boson couples to }J^\mu,
}
\]

而

\[
\boxed{
\text{spin-2 graviton couples to }T^{\mu\nu}.
}
\]

这是 QFT 中非常重要的结构类比。

---

## 24.4 Massive spin-2

Fierz–Pauli theory 中 massive spin-2 有

\[
\boxed{
2s+1=5
}
\]

个极化：

\[
\boxed{
\lambda=-2,-1,0,+1,+2.
}
\]

可以用 massive spin-1 polarization vector 构造 polarization tensors。

例如

\[
\boxed{
\epsilon_{\mu\nu}^{(\pm2)}
=
\epsilon_\mu^{(\pm)}
\epsilon_\nu^{(\pm)}.
}
\]

\[
\boxed{
\epsilon_{\mu\nu}^{(\pm1)}
=
\frac1{\sqrt2}
\left(
\epsilon_\mu^{(\pm)}
\epsilon_\nu^{(0)}
+
\epsilon_\mu^{(0)}
\epsilon_\nu^{(\pm)}
\right).
}
\]

helicity-0 tensor 可取为适当的 traceless combination。

---

## 24.5 QFT 应用

- linearized gravity；
- gravitational waves；
- graviton scattering；
- massive gravity；
- Kaluza–Klein spin-2 modes；
- composite spin-2 resonance；
- stress-tensor exchange；
- AdS/CFT 中与 boundary stress tensor 对偶的 bulk graviton。

---

# 25. 一般整数 spin-\(s\)：massive field

在四维，对于 massive integer spin-\(s\)，可以用 totally symmetric tensor

\[
\boxed{
\phi_{\mu_1\cdots\mu_s}
=
\phi_{(\mu_1\cdots\mu_s)}
}
\]

描述。

为了只留下纯 spin-\(s\)，自由场满足典型的 Fierz–Pauli 型条件：

\[
\boxed{
(\Box-m^2)
\phi_{\mu_1\cdots\mu_s}=0,
}
\]

\[
\boxed{
\partial^{\mu_1}
\phi_{\mu_1\mu_2\cdots\mu_s}=0,
}
\]

\[
\boxed{
\phi^\rho{}_{\rho\mu_3\cdots\mu_s}=0.
}
\]

即：

- Klein–Gordon equation；
- transverse；
- traceless。

这些条件将 Lorentz tensor 中多余的低 spin 成分投影掉，留下

\[
\boxed{
2s+1
}
\]

个 massive spin states。

---

# 26. 一般整数 massless spin-\(s\)：Fronsdal field

取 totally symmetric field

\[
\phi_{\mu_1\cdots\mu_s}.
\]

Fronsdal gauge transformation：

\[
\boxed{
\delta
\phi_{\mu_1\cdots\mu_s}
=
s\,
\partial_{(\mu_1}
\epsilon_{\mu_2\cdots\mu_s)}.
}
\]

gauge parameter 要求 traceless：

\[
\boxed{
\epsilon^\rho{}_{\rho\mu_3\cdots}=0.
}
\]

对 \(s\ge4\)，Fronsdal field 通常要求 double-traceless：

\[
\boxed{
\phi^{\rho\sigma}{}_{\rho\sigma\mu_5\cdots}=0.
}
\]

Fronsdal operator：

\[
\boxed{
\begin{aligned}
\mathcal F_{\mu_1\cdots\mu_s}
=
&
\Box\phi_{\mu_1\cdots\mu_s}
\\
&
-
s\,
\partial_{(\mu_1}
(\partial\cdot\phi)_{\mu_2\cdots\mu_s)}
\\
&
+
\frac{s(s-1)}2
\partial_{(\mu_1}
\partial_{\mu_2}
\phi'_{\mu_3\cdots\mu_s)}.
\end{aligned}
}
\]

自由方程

\[
\boxed{
\mathcal F_{\mu_1\cdots\mu_s}=0.
}
\]

在四维最终传播

\[
\boxed{
h=\pm s.
}
\]

---

# 27. 一般半整数 spin-\(s=n+\frac12\)

可用 symmetric tensor-spinor

\[
\boxed{
\psi_{\mu_1\cdots\mu_n}
}
\]

描述。

其总 Lorentz generator 是

\[
\boxed{
\Sigma^{ab}_{\rm total}
=
\Sigma^{ab}_{\rm tensor}
+
\Sigma^{ab}_{\rm spinor}.
}
\]

massless Fang–Fronsdal 型理论具有 gauge transformation

\[
\boxed{
\delta
\psi_{\mu_1\cdots\mu_n}
=
n\,
\partial_{(\mu_1}
\epsilon_{\mu_2\cdots\mu_n)}.
}
\]

并伴随适当的 gamma-trace constraints。

在四维，物理态最终为

\[
\boxed{
h=\pm\left(n+\frac12\right).
}
\]

---

# 28. 为什么 gauge symmetry 与 helicity 直接相关

一个高 rank Lorentz field 往往包含多个 spin/helicity sector。

例如：

\[
A_\mu
\]

作为四矢量包含多于两个 component；

\[
h_{\mu\nu}
\]

包含远多于两个 component；

\[
\psi_\mu
\]

也包含 spin-\(\frac12\) 部分。

对于 massless field，gauge symmetry 的核心作用就是消除非物理 polarizations。

因此：

\[
\boxed{
\text{massless gauge symmetry}
\Longrightarrow
\text{physical helicity projection}.
}
\]

具体地：

\[
A_\mu
\quad\Rightarrow\quad
h=\pm1,
\]

\[
\psi_\mu
\quad\Rightarrow\quad
h=\pm\frac32,
\]

\[
h_{\mu\nu}
\quad\Rightarrow\quad
h=\pm2.
\]

---

# 29. 常见耦合按 spin 的统一模式

QFT 中几个最典型的局域耦合可以按 spin 排列。

## spin-0

\[
\boxed{
\phi\,\bar\psi\psi
}
\]

或

\[
\boxed{
\phi F_{\mu\nu}F^{\mu\nu}.
}
\]

## spin-1

\[
\boxed{
A_\mu J^\mu.
}
\]

要求电流守恒：

\[
\boxed{
\partial_\mu J^\mu=0.
}
\]

## spin-2

\[
\boxed{
h_{\mu\nu}T^{\mu\nu}.
}
\]

要求

\[
\boxed{
\partial_\mu T^{\mu\nu}=0.
}
\]

这个序列说明：

\[
\boxed{
\text{场的 spin 越高，对其源的张量结构要求越高。}
}
\]

---

# 30. helicity amplitude：现代 QFT 中最直接的应用

对于 massless particle，直接使用 helicity basis 往往比使用 Lorentz tensor components 更高效。

四维无质量动量可以写为

\[
\boxed{
p_{\alpha\dot\alpha}
=
\lambda_\alpha
\tilde\lambda_{\dot\alpha}.
}
\]

little-group scaling：

\[
\boxed{
\lambda
\to
t\lambda,
\qquad
\tilde\lambda
\to
t^{-1}\tilde\lambda.
}
\]

helicity-\(h\) 的外线态要求振幅满足

\[
\boxed{
\mathcal A_n
\to
t_i^{-2h_i}
\mathcal A_n
}
\]

对每一条外线分别成立。

这实际上把 helicity 表示论直接转化为 scattering amplitude 的齐次性条件。

---

## 30.1 Yang–Mills 三点振幅

在复动量或适当解析延拓下：

\[
\boxed{
A_3(1^-,2^-,3^+)
=
g
\frac{
\langle12\rangle^3
}{
\langle23\rangle
\langle31\rangle
}.
}
\]

其 little-group scaling 正好对应

\[
(-1,-1,+1).
\]

---

## 30.2 Gravity 三点振幅

对应的 graviton 三点振幅：

\[
\boxed{
M_3(1^{-2},2^{-2},3^{+2})
=
\kappa
\frac{
\langle12\rangle^6
}{
\langle23\rangle^2
\langle31\rangle^2
}.
}
\]

可以看到 gravity amplitude 在结构上近似是 Yang–Mills amplitude 的“平方”。

这也是 double-copy 结构的最简单信号之一。

---

# 31. chirality、helicity 与 mass 的关系

对于 massless fermion，

\[
\boxed{
[\gamma^5,\slashed p]=0
\quad
(p^2=0)
}
\]

使左右 chirality sector 解耦。

因此可以独立使用 Weyl field。

对于 massive fermion：

\[
\boxed{
m\bar\psi\psi
}
\]

把

\[
\left(\frac12,0\right)
\]

和

\[
\left(0,\frac12\right)
\]

耦合起来。

因此 massive Dirac particle 不再是单一 helicity eigenstate。

换言之：

\[
\boxed{
m=0:
\text{ chirality 与 helicity 紧密绑定},
}
\]

而

\[
\boxed{
m\neq0:
\text{ helicity 不是完整 Lorentz invariant spin label}.
}
\]

---

# 32. massive spin-2 的 helicity decomposition

massive spin-2 有五个 helicity：

\[
\boxed{
\pm2,\quad
\pm1,\quad
0.
}
\]

而 massless spin-2 只有

\[
\boxed{
\pm2.
}
\]

因此

\[
m\to0
\]

极限在相互作用理论中可能并不平凡。

helicity-0 mode 尤其重要。

这在 massive gravity 中导致著名的：

- helicity decomposition；
- strong coupling scale；
- Vainshtein mechanism；
- massive 与 massless gravity 极限的非平凡性。

---

# 33. 高自旋场在 QFT 中的常见应用

一般 spin \(s>2\) 场并非没有应用，而是其一致相互作用受到强限制。

常见场景包括：

### 1. Hadron resonance

强相互作用谱中存在高自旋 resonance，可在 EFT 中使用高 rank tensor 或 tensor-spinor 描述。

### 2. Regge trajectory

强子与 string excitation 往往形成

\[
J
\sim
\alpha' m^2+\alpha_0
\]

型 Regge trajectory。

### 3. String theory

string spectrum 自然包含无限塔：

\[
s=0,1,2,\ldots
\]

以及相应 massive higher-spin excitations。

### 4. AdS/CFT

boundary CFT 中的高自旋算符对应 bulk 中的高自旋场。

### 5. Higher-spin gravity

在 AdS 背景中，可以构造包含无限塔高自旋 gauge fields 的一致理论。

---

# 34. 为什么平直时空中的 massless higher-spin interaction 很难

对 massless spin \(s>2\)，同时要求：

- Lorentz invariance；
- locality；
- unitary；
- finite number of fields；
- conventional S-matrix；
- long-range interaction；

会受到非常强的约束。

因此一般规律是：

\[
\boxed{
\text{flat-space interacting massless higher spin}
}
\]

远比

\[
\boxed{
s\le2
}
\]

困难。

常见绕开方式包括：

- AdS background；
- infinite tower of states；
- nonlocality；
- string theory；
- 放松标准 S-matrix 假设。

---

# 35. 从 Lorentz 表示到物理态：几个典型投影

这一节把“表示”与“物理自由度”并列起来。

| 场 | Lorentz 表示/类型 | 约束或 gauge | 物理态 |
|---|---|---|---|
| \(\phi\) | scalar | 无 | \(s=0\) |
| \(\psi\) massive | Dirac | Dirac equation | \(s=\frac12\), 2 spin states |
| \(\chi\) massless | Weyl | Weyl equation | 单 chirality helicity |
| \(A_\mu\) massive | vector | \(p\cdot A=0\) | \(s=1\), 3 states |
| \(A_\mu\) massless | vector gauge field | \(A\sim A+\partial\alpha\) | \(h=\pm1\) |
| \(\psi_\mu\) massive | vector-spinor | \(p\cdot\psi=0,\gamma\cdot\psi=0\) | \(s=\frac32\), 4 states |
| \(\psi_\mu\) massless | gauge vector-spinor | \(\psi_\mu\sim\psi_\mu+\partial_\mu\epsilon\) | \(h=\pm\frac32\) |
| \(h_{\mu\nu}\) massive | symmetric tensor | transverse + traceless | \(s=2\), 5 states |
| \(h_{\mu\nu}\) massless | gauge symmetric tensor | linear diffeomorphism | \(h=\pm2\) |
| \(\phi_{\mu_1\cdots\mu_s}\) massless | symmetric rank-\(s\) | Fronsdal gauge symmetry | \(h=\pm s\) |

---

# 36. 最常见的 QFT 对应关系

从应用角度，可以把常见粒子/场归纳为：

\[
\boxed{
s=0
\quad\Rightarrow\quad
\text{Higgs, Goldstone, axion, inflaton}
}
\]

\[
\boxed{
s=\frac12
\quad\Rightarrow\quad
\text{quark, lepton, neutrino, gaugino}
}
\]

\[
\boxed{
s=1
\quad\Rightarrow\quad
\text{photon, gluon, }W,Z
}
\]

\[
\boxed{
s=\frac32
\quad\Rightarrow\quad
\text{gravitino, spin-}\frac32\text{ hadron resonance}
}
\]

\[
\boxed{
s=2
\quad\Rightarrow\quad
\text{graviton, massive spin-2 resonance, KK graviton}
}
\]

\[
\boxed{
s>2
\quad\Rightarrow\quad
\text{higher-spin EFT, string states, Regge states, AdS higher-spin fields}.
}
\]

---

# 37. 本节最核心的统一认识

对于任意场，第一层是 Lorentz transformation：

\[
\boxed{
M^{\mu\nu}
=
L^{\mu\nu}
+
\Sigma^{\mu\nu}.
}
\]

第二层是 Poincaré 单粒子表示：

\[
\boxed{
P^2,\quad W^2
}
\]

决定 mass 与 spin/helicity。

第三层是 dynamical constraints：

\[
\boxed{
\text{equations of motion}
+
\text{constraints}
+
\text{gauge redundancy}
}
\]

把一个大的 Lorentz field representation 投影到真正的物理单粒子 Hilbert space。

因此真正的逻辑不是

\[
\text{rank of tensor}
=
\text{spin},
\]

而是

\[
\boxed{
\text{Lorentz representation}
+
\text{field equation}
+
\text{constraints/gauge}
\Longrightarrow
\text{physical Poincaré spin/helicity}.
}
\]

这也是理解 scalar、photon、Dirac fermion、graviton 与 higher-spin field 的统一框架。
