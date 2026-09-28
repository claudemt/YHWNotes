# AdvancedPhysics 数值图

本目录中的数值图脚本统一调用仓库根目录 `preamble.py`，共享字体、颜色表、参考线、坐标轴、图例和 PDF/PNG 保存规则。脚本在仓库根目录执行 `python main.py build AdvancedPhysics --figures` 时运行，图像写入 `content/AdvancedPhysics/figures/generated/`。需安装 `numpy`、`scipy` 和 `matplotlib`；脚本使用固定参数或随机种子，以便复算。

- `biharmonic_square_code.py`：对 Navier 方板连续求解两次离散 Poisson 方程，与解析正弦解比较；断言最大误差随网格加密递减且接近二阶。
- `biharmonic_disk_boundary_code.py`：绘制圆盘上由边界位移与法向斜率确定的双调和解，并直接核验两项边界数据。
- `integral_equations_code.py`：复合梯形公式求 Volterra 方程，Gauss--Legendre 求积离散秩一 Fredholm 方程；显示收敛与 $\lambda=3$ 的共振。
- `inverse_integral_regularization_code.py`：在固定种子的含噪积分数据上比较直接差分与零阶 Tikhonov 恢复，并输出二者的 $L^2$ 误差。
- `plate_modal_response_code.py`：用 $m,n\le9$ 的奇数模态计算简支方板；分别生成单幅频响图 `plate_modal_response` 与双幅模态位形图 `plate_modal_shapes`，避免把不同量纲挤入三栏小图。
- `ising_random_cluster_code.py`：分别穷举自旋构型和随机簇边集，断言相关函数与连通概率的最大差异小于 $2\times10^{-14}$。

双调和方板、积分方程、逆问题、模态响应和有限图模型分别由各自脚本计算。有限图的结构示意另由 `figures/tikz/five-edge-graph.tex` 绘制，并沿用根 `preamble.tex` 的 `tikzfig`、`wfA` 和 `lecturelabel` 公共样式。
