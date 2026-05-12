import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import scienceplots  # 必须导入

# ======================
# 🔥 启用 SciencePlots 样式（论文最常用组合）
# ======================
plt.style.use(['science', 'ieee', 'no-latex'])
# 如需 LaTeX 渲染公式更美观（需装TeX）：去掉 'no-latex'
# plt.style.use(['science', 'ieee'])

# 全局微调（保持学术感）
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "lines.linewidth": 1.5,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05
})

# ======================
# 物理函数定义（完全复刻你Mathematica）
# ======================

def gammaC(q):
    return 0.5 * np.log(q / (q - 2))

def eqn(a, gamma, q):
    return np.exp(2*a/(q-1)) * np.cosh(a-gamma) - np.cosh(a+gamma)

def a_func(gamma, q):
    if q <= 2:
        return np.nan
    gc = gammaC(q)
    if gamma <= gc:
        return 0.0
    # 多初始值找根
    a0 = max(0.1, gamma - gc)
    guesses = [a0, 2*a0, 0.5, 1.0, 2.0, 5.0]
    for s in guesses:
        try:
            sol = root_scalar(eqn, args=(gamma, q), bracket=[s*0.1, s*10], method='brentq')
            if sol.converged and abs(sol.root) > 1e-8:
                return sol.root
        except:
            continue
    return np.nan

# --- 概率 ---
def Pmp(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    den = 2*(np.cosh(2*av)+np.exp(-2*gamma))
    return np.exp(-2*gamma)/den if den!=0 else np.nan

def Ppp(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    den = 2*(np.cosh(2*av)+np.exp(-2*gamma))
    return np.exp(2*av)/den if den!=0 else np.nan

def Pp(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    den = 2*(np.cosh(2*av)+np.exp(-2*gamma))
    return (np.exp(-2*gamma)+np.exp(2*av))/den if den!=0 else np.nan

# --- 磁化率 chi ---
def chi(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    log_term = np.log(q/(q-2))
    if log_term == 0: return np.nan
    numer = 8*gamma*(1 + np.exp(-2*gamma)*np.cosh(2*av))
    denom = (np.cosh(2*av)+np.exp(-2*gamma))**2 * log_term
    tanh_term = np.tanh(av+gamma) - np.tanh(av-gamma)
    return (numer/denom) * (2 - (q-1)*tanh_term)

# --- 比热 CH (Bethe) ---
def CH(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    expg = np.exp(-2*gamma)
    c2a = np.cosh(2*av)
    s2a = np.sinh(2*av)
    c2g = np.cosh(2*gamma)
    s2g = np.sinh(2*gamma)
    den = (c2a + expg)**2
    bracket = c2a + ((q-1)*s2a**2) / (c2a + c2g - (q-1)*s2g)
    return gamma**2 * 2*q * expg / den * bracket

# --- 磁化 m (Bethe) ---
def m_func(gamma, q):
    av = a_func(gamma, q)
    if np.isnan(av): return np.nan
    den = np.cosh(2*av) + np.exp(-2*gamma)
    return np.sinh(2*av)/den if den!=0 else np.nan

# --- B-W 近似 mp, CHp ---
def gammaCp(q):
    return 1.0 / q

def mp_eqn(m, gamma, q):
    return m - np.tanh(q * gamma * m)

def mp_func(gamma, q):
    if q <= 0:
        return np.nan
    gc = gammaCp(q)
    if gamma <= gc:
        return 0.0
    m0 = min(0.9, max(0.05, np.sqrt(max(1e-8, q*gamma-1))))
    try:
        sol = root_scalar(mp_eqn, args=(gamma, q), bracket=[1e-4, 1-1e-4], method='brentq')
        return sol.root if sol.converged else np.nan
    except:
        return np.nan

def CHp(gamma, q):
    gc = gammaCp(q)
    if gamma <= gc:
        return 0.0
    mv = mp_func(gamma, q)
    if np.isnan(mv): return np.nan
    den = 1 - q*gamma*(1 - mv**2)
    if den == 0: return np.nan
    return gamma**2 * q**2 * mv**2 * (1 - mv**2) / den

# ======================
# 绘图：4张图（SciencePlots风格）
# ======================

q_list = [3, 4, 5]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
linestyles = ['-', '--', '-.']

# ------------------------------------------------------------------------------
# 图1：CH 比热（Bethe vs B-W）
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.6))  # IEEE双栏标准尺寸
gamma = np.linspace(0.4, 5.5, 400)
for i, q in enumerate(q_list):
    ch_bethe = np.array([CH(g, q) for g in gamma])
    ch_bw   = np.array([CHp(g, q) for g in gamma])
    ax.plot(1/gamma, ch_bethe, c=colors[i], ls=linestyles[0], lw=1.5, label=f'Bethe $q={q}$')
    ax.plot(1/gamma, ch_bw,   c=colors[i], ls=linestyles[1], lw=1.5, label=f'B-W $q={q}$')
ax.set_xlabel(r'$kT/J$')
ax.set_ylabel(r'$C/Nk$')
ax.legend(ncol=2, frameon=False)
ax.grid(alpha=0.2)
plt.savefig('CH_vs_T.pdf', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 图2：磁化强度 |m|（Bethe vs B-W）
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.6))
for i, q in enumerate(q_list):
    m_bethe = np.array([abs(m_func(g, q)) for g in gamma])
    m_bw    = np.array([abs(mp_func(g, q)) for g in gamma])
    ax.plot(1/gamma, m_bethe, c=colors[i], ls=linestyles[0], lw=1.5, label=f'Bethe $q={q}$')
    ax.plot(1/gamma, m_bw,    c=colors[i], ls=linestyles[1], lw=1.5, label=f'B-W $q={q}$')
ax.set_xlabel(r'$kT/J$')
ax.set_ylabel(r'$|m|$')
ax.legend(ncol=2, frameon=False)
ax.grid(alpha=0.2)
plt.savefig('m_vs_T.pdf', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 图3：概率 Pmp, Ppp, Pp（q=3为例）
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.6))
gamma_p = np.linspace(0.5, 4.0, 400)
q_p = 3
pmp = np.array([Pmp(g, q_p) for g in gamma_p])
ppp = np.array([Ppp(g, q_p) for g in gamma_p])
pp  = np.array([Pp(g, q_p)  for g in gamma_p])
ax.plot(1/gamma_p, pmp, c=colors[0], lw=1.5, label=r'$p_{+-}$')
ax.plot(1/gamma_p, ppp, c=colors[1], lw=1.5, label=r'$p_{++}$')
ax.plot(1/gamma_p, pp,  c=colors[2], lw=1.5, label=r'$p_{+}$')
ax.set_xlabel(r'$kT/J$')
ax.set_ylabel(r'Probability')
ax.legend(frameon=False)
ax.grid(alpha=0.2)
plt.savefig('Prob_vs_T.pdf', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 图4：磁化率 chi
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.6))
gamma_c = np.linspace(0.5, 8.0, 400)
for i, q in enumerate(q_list):
    chi_vals = np.array([chi(g, q) for g in gamma_c])
    ax.plot(1/gamma_c, chi_vals, c=colors[i], lw=1.5, label=f'$q={q}$')
ax.set_xlabel(r'$kT/J$')
ax.set_ylabel(r'$\chi$')
ax.legend(frameon=False)
ax.grid(alpha=0.2)
plt.savefig('Chi_vs_T.pdf', dpi=300)
plt.close()

print("✅ 四张图已保存为 PDF（SciencePlots 论文样式）")