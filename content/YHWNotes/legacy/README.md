# Legacy 归档

本目录存放从 `sections/` 移出的历史残留文件——数值验算脚本、未被主文引用的临时产物与旧版草稿。
这些文件不再参与整书 build，仅作留档，请勿在 `.tex` 中 `\input` / `\subimport` / `\includegraphics` 引用。

归档日期：2026-09-21

## 归档清单

| 归档位置 | 原始路径 | 内容 | 归档原因 |
|---|---|---|---|
| `Statistics/BoseFermiGas/bose_fermi_gas_mma/` | `sections/Statistics/BoseFermiGas/bose_fermi_gas_mma/` | `bose_fermi_gas_mma_01.nb`、`bose_fermi_gas_mma_02.nb`（Mathematica notebook，合计约 414 KB） | 历史数值验算脚本，未被主文引用 |
| `Statistics/BoseFermiGas/bose_fermi_plot_py/` | `sections/Statistics/BoseFermiGas/bose_fermi_plot_py/` | `bose_fermi_plot.py` 及 5 张 PNG（`all_panels.png`、`Cv_T.png`、`gamma_T.png`、`mu_T.png`、`P_T.png`） | 历史绘图脚本与中间产物；`bose_fermi_gas.tex` 未通过 `\includegraphics` 引用 |
| `Electrodynamics/STFMultipoleExpansion/english_version/` | `sections/Electrodynamics/STFMultipoleExpansion/english_version/` | `Multipole Expansion of Electromagnetic Field in Cartesian Coordinates.tex`（约 36 KB） | 未被主文引用的英文旧版草稿 |
| `MathTool/SpecialFunctions/supplement_material/` | `sections/MathTool/SpecialFunctions/supplement_material/` | `prove_spherical_harmonics_gradient.tex`（约 6 KB） | 未被主文引用的补充证明草稿 |

## 备注

- 移动前已对 `sections/**/*.tex` 全文检索 `bose_fermi_gas_mma` / `bose_fermi_plot_py` / `english_version` / `prove_spherical_harmonics_gradient`，零命中，确认无引用。
- `_fig_code/` 下活跃的 `.py` / `.tex` 不在本次归档范围。
- 如需恢复某项，按上表"原始路径"复制回 `sections/` 对应位置即可。
