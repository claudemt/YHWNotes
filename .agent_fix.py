#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mechanical fix:
  1. Rename Chinese labels -> fig:/eq:/sec:/tab: + english snake_case
  2. Sync-rename all \label/\ref/\eqref/\cref/\Cref/\autoref/\pageref targets
  3. Convert bare \eqref -> \cref, bare \ref -> \cref
  4. Strip handwritten 式/图/表/节 prefix immediately before \cref
Skips *_fig_code/ dirs. Protects first 20 lines of rigid_body.tex and ellipsoidal_coordinates.tex.
"""
import os, re, sys

ROOT = r"E:\OneDrive\Desktop\YHWNotes"
BODY_DIR = os.path.join(ROOT, "content", "YHWNotes", "sections")

# ---- label rename map: old Chinese name -> new name ----
RENAME = {
    # electrostatics.tex
    "立方电阻网对称化示意图": "fig:cubic_resistor_network_symmetry",
    "导体平面上的圆形孔": "sec:circular_hole_on_plane",
    "导体平面上的圆孔示意图": "fig:circular_hole_on_plane",
    "球域磁场扩散示意图": "fig:sphere_magnetic_diffusion",
    "球心磁场扩散示意图": "fig:sphere_center_magnetic_diffusion",
    "一维磁场扩散示意图": "fig:one_d_magnetic_diffusion",
    # plasma.tex
    "回旋运动示意图": "fig:gyromotion",
    "等离子体_横纵可分离变量": "eq:plasma_separable_xy",
    # radiation.tex
    "正弦天线的辐射-能量角分布": "fig:dipole_antenna_angular_power",
    "正弦天线的辐射-相对阻抗": "fig:dipole_antenna_impedance",
    "正弦天线的辐射": "fig:dipole_antenna_radiation",
    "电荷运动模式示意图-匀速运动": "fig:charge_motion_uniform",
    "匀速运动电荷的辐射示意图": "fig:uniform_motion_radiation",
    "电荷运动模式示意图-非匀速运动": "fig:charge_motion_nonuniform",
    "非匀速运动电荷的辐射示意图": "fig:nonuniform_motion_radiation",
    "电荷运动模式示意图-圆周运动": "fig:charge_motion_circular",
    "圆周运动电荷的辐射示意图": "fig:circular_motion_radiation",
    "电荷运动模式示意图-简谐运动": "fig:charge_motion_harmonic",
    "简谐运动电荷的辐射示意图": "fig:harmonic_motion_radiation",
    "电荷运动模式示意图": "fig:charge_motion_modes",
    "G(nu)图像": "fig:g_nu_plot",
    "G图像": "fig:g_plot",
    "电荷及磁矩辐射能量频谱": "fig:charge_magnet_radiation_spectrum",
    "点电荷周期运动辐射能量角分布-圆周运动": "fig:periodic_radiation_angular_circular",
    "点电荷周期运动辐射能量角分布-简谐运动": "fig:periodic_radiation_angular_harmonic",
    "点电荷周期运动辐射能量角分布": "fig:periodic_radiation_angular",
    "点电荷圆周运动辐射场示意图-E|_xy(beta=0.6)": "fig:circular_rad_field_e_xy_b06",
    "点电荷圆周运动辐射场示意图-E|_xy(beta=0.9)": "fig:circular_rad_field_e_xy_b09",
    "点电荷圆周运动辐射场示意图-E|_xz(beta=0.6)": "fig:circular_rad_field_e_xz_b06",
    "点电荷圆周运动辐射场示意图-E|_yz(beta=0.6)": "fig:circular_rad_field_e_yz_b06",
    "点电荷圆周运动辐射场示意图-B|_xy(beta=0.6)": "fig:circular_rad_field_b_xy_b06",
    "点电荷圆周运动辐射场示意图-B|_xy(beta=0.9)": "fig:circular_rad_field_b_xy_b09",
    "点电荷圆周运动辐射场示意图-B|_xz(beta=0.6)": "fig:circular_rad_field_b_xz_b06",
    "点电荷圆周运动辐射场示意图-B|_yz(beta=0.6)": "fig:circular_rad_field_b_yz_b06",
    "点电荷圆周运动辐射场示意图-E|_xy(beta=0.6)-2": "fig:circular_rad_field_e_xy_b06_b",
    "点电荷圆周运动辐射场示意图-E|_xy(beta=0.9)-2": "fig:circular_rad_field_e_xy_b09_b",
    "点电荷圆周运动辐射场示意图-E|_xz(beta=0.6)-2": "fig:circular_rad_field_e_xz_b06_b",
    "点电荷圆周运动辐射场示意图-E|_yz(beta=0.6)-2": "fig:circular_rad_field_e_yz_b06_b",
    "点电荷圆周运动辐射场示意图-S|_xy(beta=0.6)": "fig:circular_rad_field_s_xy_b06",
    "点电荷圆周运动辐射场示意图-S|_xy(beta=0.9)": "fig:circular_rad_field_s_xy_b09",
    "点电荷圆周运动辐射场示意图-S|_xz(beta=0.6)": "fig:circular_rad_field_s_xz_b06",
    "点电荷圆周运动辐射场示意图-S|_yz(beta=0.6)": "fig:circular_rad_field_s_yz_b06",
    "点电荷圆周运动辐射场示意图-tau|_xy(beta=0.6)": "fig:circular_rad_field_tau_xy_b06",
    "点电荷圆周运动辐射场示意图-tau|_xy(beta=0.9)": "fig:circular_rad_field_tau_xy_b09",
    "点电荷圆周运动辐射场示意图-tau|_xz(beta=0.6)": "fig:circular_rad_field_tau_xz_b06",
    "点电荷圆周运动辐射场示意图-tau|_yz(beta=0.6)": "fig:circular_rad_field_tau_yz_b06",
    "点电荷圆周运动辐射场示意图": "fig:circular_rad_field",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.6,eta=0)": "fig:harmonic_rad_field_e_yz_b06_e0",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.6,eta=0.25)": "fig:harmonic_rad_field_e_yz_b06_e25",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.9,eta=0)": "fig:harmonic_rad_field_e_yz_b09_e0",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.9,eta=0.25)": "fig:harmonic_rad_field_e_yz_b09_e25",
    "点电荷简谐运动辐射场示意图-B|_yz(beta=0.6,eta=0)": "fig:harmonic_rad_field_b_yz_b06_e0",
    "点电荷简谐运动辐射场示意图-B|_yz(beta=0.6,eta=0.25)": "fig:harmonic_rad_field_b_yz_b06_e25",
    "点电荷简谐运动辐射场示意图-B|_yz(beta=0.9,eta=0)": "fig:harmonic_rad_field_b_yz_b09_e0",
    "点电荷简谐运动辐射场示意图-B|_yz(beta=0.9,eta=0.25)": "fig:harmonic_rad_field_b_yz_b09_e25",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.6,eta=0)-2": "fig:harmonic_rad_field_e_yz_b06_e0_b",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.6,eta=0.25)-2": "fig:harmonic_rad_field_e_yz_b06_e25_b",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.9,eta=0)-2": "fig:harmonic_rad_field_e_yz_b09_e0_b",
    "点电荷简谐运动辐射场示意图-E|_yz(beta=0.9,eta=0.25)-2": "fig:harmonic_rad_field_e_yz_b09_e25_b",
    "点电荷简谐运动辐射场示意图-S|_yz(beta=0.6,eta=0)": "fig:harmonic_rad_field_s_yz_b06_e0",
    "点电荷简谐运动辐射场示意图-S|_yz(beta=0.6,eta=0.25)": "fig:harmonic_rad_field_s_yz_b06_e25",
    "点电荷简谐运动辐射场示意图-S|_yz(beta=0.9,eta=0)": "fig:harmonic_rad_field_s_yz_b09_e0",
    "点电荷简谐运动辐射场示意图-S|_yz(beta=0.9,eta=0.25)": "fig:harmonic_rad_field_s_yz_b09_e25",
    "点电荷简谐运动辐射场示意图-tau|_yz(beta=0.6,eta=0)": "fig:harmonic_rad_field_tau_yz_b06_e0",
    "点电荷简谐运动辐射场示意图-tau|_yz(beta=0.6,eta=0.25)": "fig:harmonic_rad_field_tau_yz_b06_e25",
    "点电荷简谐运动辐射场示意图-tau|_yz(beta=0.9,eta=0)": "fig:harmonic_rad_field_tau_yz_b09_e0",
    "点电荷简谐运动辐射场示意图-tau|_yz(beta=0.9,eta=0.25)": "fig:harmonic_rad_field_tau_yz_b09_e25",
    "点电荷简谐运动辐射场示意图": "fig:harmonic_rad_field",
    # scattering.tex
    "电磁场按球坐标展开": "sec:em_field_spherical_expansion",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损小球,x方向实部": "fig:sphere_scat_small_lossy_x",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损小球,y方向实部": "fig:sphere_scat_small_lossy_y",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损小球,z方向实部": "fig:sphere_scat_small_lossy_z",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损小球,振幅大小": "fig:sphere_scat_small_lossy_amp",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损大球,x方向实部": "fig:sphere_scat_large_lossy_x",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损大球,y方向实部": "fig:sphere_scat_large_lossy_y",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损大球,z方向实部": "fig:sphere_scat_large_lossy_z",
    "球体散射振幅比较图(对比有无损耗及不同半径)-有损大球,振幅大小": "fig:sphere_scat_large_lossy_amp",
    "球体散射振幅比较图(对比有无损耗及不同半径)-无损大球,x方向实部": "fig:sphere_scat_large_lossless_x",
    "球体散射振幅比较图(对比有无损耗及不同半径)-无损大球,y方向实部": "fig:sphere_scat_large_lossless_y",
    "球体散射振幅比较图(对比有无损耗及不同半径)-无损大球,z方向实部": "fig:sphere_scat_large_lossless_z",
    "球体散射振幅比较图(对比有无损耗及不同半径)-无损大球,振幅大小": "fig:sphere_scat_large_lossless_amp",
    "球体散射振幅比较图(对比有无损耗及不同半径)": "fig:sphere_scat_comparison",
    "球体总场振幅比较图(对比有无损耗及不同半径)-有损小球": "fig:sphere_total_small_lossy",
    "球体总场振幅比较图(对比有无损耗及不同半径)-有损大球": "fig:sphere_total_large_lossy",
    "球体总场振幅比较图(对比有无损耗及不同半径)-无损大球": "fig:sphere_total_large_lossless",
    "球体总场振幅比较图(对比有无损耗及不同半径)": "fig:sphere_total_comparison",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损小柱,x方向实部": "fig:cyl_scat_small_lossy_x",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损小柱,y方向实部": "fig:cyl_scat_small_lossy_y",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损小柱,z方向实部": "fig:cyl_scat_small_lossy_z",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损小柱,振幅大小": "fig:cyl_scat_small_lossy_amp",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损大柱,x方向实部": "fig:cyl_scat_large_lossy_x",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损大柱,y方向实部": "fig:cyl_scat_large_lossy_y",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损大柱,z方向实部": "fig:cyl_scat_large_lossy_z",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-有损大柱,振幅大小": "fig:cyl_scat_large_lossy_amp",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-无损大柱,x方向实部": "fig:cyl_scat_large_lossless_x",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-无损大柱,y方向实部": "fig:cyl_scat_large_lossless_y",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-无损大柱,z方向实部": "fig:cyl_scat_large_lossless_z",
    "柱体散射振幅比较图(对比有无损耗及不同半径)-无损大柱,振幅大小": "fig:cyl_scat_large_lossless_amp",
    "柱体散射振幅比较图(对比有无损耗及不同半径)": "fig:cyl_scat_comparison",
    "柱体总场振幅比较图(对比有无损耗及不同半径)-有损小柱": "fig:cyl_total_small_lossy",
    "柱体总场振幅比较图(对比有无损耗及不同半径)-有损大柱": "fig:cyl_total_large_lossy",
    "柱体总场振幅比较图(对比有无损耗及不同半径)-无损大柱": "fig:cyl_total_large_lossless",
    "柱体总场振幅比较图(对比有无损耗及不同半径)": "fig:cyl_total_comparison",
    # stf_multipole_expansion.tex
    "环形偶极矩示意图-环形电偶极矩": "fig:toroidal_electric_dipole",
    "环形偶极矩示意图-环形磁偶极矩": "fig:toroidal_magnetic_dipole",
    "环形偶极矩示意图": "fig:toroidal_dipole",
    # thin_film.tex
    "介质膜示意图-光学介质膜": "fig:thin_film_optical",
    "光学介质膜": "fig:optical_film",
    "介质膜示意图-弹性介质膜": "fig:thin_film_elastic",
    "弹性介质膜": "fig:elastic_film",
    "介质膜示意图": "fig:thin_film",
    # waveguide.tex
    "平面介质波导传播参量关系图(n_1=2.5,n_2=1.5)-角频率关系图": "fig:planar_wg_dispersion_omega",
    "平面介质波导传播参量关系图(n_1=2.5,n_2=1.5)-群速度关系图": "fig:planar_wg_dispersion_vg",
    "平面介质波导传播参量关系图(n_1=2.5,n_2=1.5)-特征位移关系图": "fig:planar_wg_dispersion_field",
    "传播模式示意图(n_1=2.5,n_2=1.5)": "fig:waveguide_propagation_modes",
    "圆柱波导传输模式图": "fig:cylindrical_waveguide_modes",
    "传输效率关系图(n_1=2.5,n_2=1.5)": "fig:waveguide_transmission_efficiency",
    "圆柱波导传输效率图": "fig:cylindrical_waveguide_efficiency",
    "mu_mn数值表": "tab:mu_mn_table",
    "kappa_mn数值表(n_1=2.5,n_2=1.5)": "tab:kappa_mn_table",
    "截止处纵向波数、传输比率表(n_1=2.5,n_2=1.5)": "tab:cutoff_wavenumber_table",
    "无限长波导示意图": "fig:infinite_waveguide",
    "平板波导示意图": "fig:planar_waveguide",
    "圆形波导振幅分布图-TE,m=3,n=2": "fig:circular_wg_amp_te_3_2",
    "圆形波导振幅分布图-TE,m=3,n=5": "fig:circular_wg_amp_te_3_5",
    "圆形波导振幅分布图-TE,m=5,n=5": "fig:circular_wg_amp_te_5_5",
    "圆形波导振幅分布图-TM,m=3,n=2": "fig:circular_wg_amp_tm_3_2",
    "圆形波导振幅分布图-TM,m=3,n=5": "fig:circular_wg_amp_tm_3_5",
    "圆形波导振幅分布图-TM,m=5,n=5": "fig:circular_wg_amp_tm_5_5",
    "圆形波导振幅分布图": "fig:circular_wg_amp",
    "矩形波导振幅分布图-TE,m=3,n=2": "fig:rectangular_wg_amp_te_3_2",
    "矩形波导振幅分布图-TE,m=3,n=5": "fig:rectangular_wg_amp_te_3_5",
    "矩形波导振幅分布图-TE,m=5,n=5": "fig:rectangular_wg_amp_te_5_5",
    "矩形波导振幅分布图-TM,m=3,n=2": "fig:rectangular_wg_amp_tm_3_2",
    "矩形波导振幅分布图-TM,m=3,n=5": "fig:rectangular_wg_amp_tm_3_5",
    "矩形波导振幅分布图-TM,m=5,n=5": "fig:rectangular_wg_amp_tm_5_5",
    "矩形波导振幅分布图": "fig:rectangular_wg_amp",
    "平板波导振幅分布图-TE,m=4,f=4.00GHz": "fig:planar_wg_amp_te_4_4ghz",
    "平板波导振幅分布图-TE,m=4,f=8.00GHz": "fig:planar_wg_amp_te_4_8ghz",
    "平板波导振幅分布图-TE,m=5,f=8.00GHz": "fig:planar_wg_amp_te_5_8ghz",
    "平板波导振幅分布图-TM,m=4,f=4.00GHz": "fig:planar_wg_amp_tm_4_4ghz",
    "平板波导振幅分布图-TM,m=4,f=8.00GHz": "fig:planar_wg_amp_tm_4_8ghz",
    "平板波导振幅分布图-TM,m=5,f=8.00GHz": "fig:planar_wg_amp_tm_5_8ghz",
    "平板波导振幅分布图": "fig:planar_wg_amp",
    # ellipsoidal_coordinates.tex
    "椭球坐标系小节": "sec:ellipsoidal_coordinates",
    "椭球坐标示意图": "fig:ellipsoidal_coordinates",
    # mathieu_functions.tex
    "Mathieu方程解的示意图-本征值曲线(阴影区稳定)": "fig:mathieu_eigenvalue_curve",
    "Mathieu方程解的示意图-Mathieu函数": "fig:mathieu_functions",
    "Mathieu方程解的示意图": "fig:mathieu_equation_solutions",
    # supplementary_formulas.tex
    "多对数函数": "fig:polylog",
    "高维空间Helmholtz方程的格林函数": "fig:higher_dim_helmholtz_green",
    "Airy型函数渐近式比较": "fig:airy_asymptotics_comparison",
    # vector_spherical_harmonics.tex
    "矢量球谐函数直角坐标展开式": "fig:vsh_cartesian_expansion",
    "矢量球谐函数球坐标展开式": "fig:vsh_spherical_expansion",
    # inverse_square_motion.tex
    "吸引场中不同参数下的运动实例-r(phi)图": "fig:attractive_motion_r_phi",
    "吸引场中不同参数下的运动实例-t(r)图": "fig:attractive_motion_t_r",
    "吸引场中不同参数下的运动实例": "fig:attractive_motion_examples",
    # nonlinear_oscillation.tex
    "达芬系统固有频率附近驱动响应相图-epsilon>0": "fig:duffing_phase_eps_pos",
    "达芬系统固有频率附近驱动响应相图-epsilon<0": "fig:duffing_phase_eps_neg",
    "达芬系统固有频率附近驱动响应相图": "fig:duffing_phase_near_natural",
    "达芬系统超谐波共振幅频响应图-改变驱动力": "fig:duffing_superharmonic_force",
    "达芬系统超谐波共振幅频响应图-改变阻尼": "fig:duffing_superharmonic_damping",
    "达芬系统超谐波共振幅频响应图": "fig:duffing_superharmonic_response",
    "达芬系统亚谐波共振响应图": "fig:duffing_subharmonic_response",
    # rigid_body.tex
    "欧拉角示意图": "fig:euler_angles",
    "刚体定点转动例题示意图": "fig:rigid_body_fixed_rotation_example",
    # crystal_optics.tex
    "晶体内的电磁场矢量": "fig:em_field_vectors_in_crystal",
    "锥形折射示意图": "fig:conical_refraction",
    "干涉装置示意图": "fig:crystal_interference_setup",
    "单轴晶体干涉装置示意图": "fig:uniaxial_crystal_interference",
    "算例的四种出射入射方式": "fig:four_incident_exit_configs",
    "第一类消光情形": "fig:extinction_type_i",
    "第二类消光情形": "fig:extinction_type_ii",
    # fourier_optics_4f.tex
    "方孔圆孔频谱比较图": "fig:square_vs_circular_aperture_spectrum",
    "4f系统示意图": "fig:four_f_system",
    "物面及频谱面模拟图-单长方孔": "fig:object_spectrum_rect_single",
    "单长方孔": "fig:rect_single",
    "物面及频谱面模拟图-双长方孔": "fig:object_spectrum_rect_double",
    "双长方孔": "fig:rect_double",
    "物面及频谱面模拟图-五角星孔": "fig:object_spectrum_star",
    "五角星孔": "fig:star_aperture",
    "物面及频谱面模拟图-等腰三角形孔": "fig:object_spectrum_triangle",
    "等腰三角形孔": "fig:isosceles_triangle_aperture",
    "物面及频谱面模拟图-单圆孔": "fig:object_spectrum_circle_single",
    "单圆孔": "fig:circle_single",
    "物面及频谱面模拟图-双圆孔": "fig:object_spectrum_circle_double",
    "双圆孔": "fig:circle_double",
    "物面及频谱面模拟图-五缝": "fig:object_spectrum_five_slits",
    "五缝": "fig:five_slits",
    "物面及频谱面模拟图-三缝": "fig:object_spectrum_three_slits",
    "三缝": "fig:three_slits",
    "物面及频谱面模拟图-立方密排方孔": "fig:object_spectrum_cubic_square",
    "立方密排方孔": "fig:cubic_square_aperture",
    "物面及频谱面模拟图-六角密排方孔": "fig:object_spectrum_hex_square",
    "六角密排方孔": "fig:hex_square_aperture",
    "物面及频谱面模拟图-立方密排圆孔": "fig:object_spectrum_cubic_circle",
    "物面及频谱面模拟图-六角密排圆孔": "fig:object_spectrum_hex_circle",
    "物面及频谱面模拟图-“十”字孔": "fig:object_spectrum_cross",
    "物面及频谱面模拟图-二维光栅": "fig:object_spectrum_2d_grating",
    "物面及频谱面模拟图": "fig:object_and_spectrum_plane",
    "滤波后像面理论模拟-“十”字挡零级": "fig:filtered_image_cross_block_zero",
    "滤波后像面理论模拟-单长方孔挡零级": "fig:filtered_image_rect_block_zero",
    "滤波后像面理论模拟-二维光栅过正狭缝": "fig:filtered_image_grating_vertical_slit",
    "滤波后像面理论模拟-二维光栅过斜狭缝": "fig:filtered_image_grating_tilted_slit",
    "滤波后像面理论模拟": "fig:filtered_image_theory",
    # matrix_optics.tex
    "主面节点焦点图": "fig:principal_plane_nodes_foci",
    "高斯光束通过透镜组": "fig:gaussian_beam_lens_system",
    # ising_model.tex
    "各统计量随温度变化图-状态概率": "fig:ising_state_probability_vs_T",
    "各统计量随温度变化图-磁化率": "fig:ising_susceptibility_vs_T",
    "各统计量随温度变化图-序参量": "fig:ising_order_parameter_vs_T",
    "各统计量随温度变化图-热容": "fig:ising_heat_capacity_vs_T",
    "各统计量随温度变化图": "fig:ising_observables_vs_T",
}

# files whose first 20 lines must be left untouched
PROTECTED_HEADS = {
    os.path.normpath("content/YHWNotes/sections/Mechanics/RigidBody/rigid_body.tex"),
    os.path.normpath("content/YHWNotes/sections/MathTool/SpecialFunctions/ellipsoidal_coordinates.tex"),
}
PROTECTED_HEAD_LINES = 20

def iter_body_files():
    for dirpath, dirnames, filenames in os.walk(BODY_DIR):
        base = os.path.basename(dirpath)
        if base.endswith("_fig_code"):
            continue
        for fn in filenames:
            if fn.endswith(".tex"):
                yield os.path.join(dirpath, fn)

def main():
    # sort old names by length desc so longer names are replaced first
    # (avoids partial-match issues, though we use exact \label{...} style)
    old_names_sorted = sorted(RENAME.keys(), key=len, reverse=True)

    # Build regex to match any ref command wrapping a known old label.
    # Commands: \label, \ref, \eqref, \cref, \Cref, \autoref, \pageref
    # We match: (\\(?:label|ref|eqref|cref|Cref|autoref|pageref)\{) (OLD) (\})
    # and replace the OLD with NEW.
    ref_cmd_re = re.compile(
        r"(\\(?:label|eqref|cref|Cref|autoref|pageref|ref)\{)("
        + "|".join(re.escape(k) for k in old_names_sorted)
        + r")(\})"
    )

    # bare \eqref -> \cref  (after renaming)
    bare_eqref_re = re.compile(r"\\eqref\{")
    # bare \ref -> \cref  (won't match \cref/\Cref/\eqref/\autoref/\pageref because those have extra letters)
    bare_ref_re = re.compile(r"(?<![a-zA-Z\\])\\ref\{")
    # handwritten prefix strip: 式/图/表/节 + optional ws immediately before \cref{
    hand_prefix_re = re.compile(r"(式|图|表|节)\s*\\cref\{")

    stats = {
        "files_touched": 0,
        "label_renames": 0,
        "eqref_to_cref": 0,
        "ref_to_cref": 0,
        "hand_prefix_stripped": 0,
    }
    renamed_pairs = []  # (old, new)

    for f in iter_body_files():
        rel = os.path.relpath(f, ROOT)
        with open(f, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8")
        # split keeping line endings so we can apply per-line protection
        lines = text.splitlines(keepends=True)

        protected = os.path.normpath(rel) in PROTECTED_HEADS
        changed = False

        for idx, line in enumerate(lines):
            if protected and idx < PROTECTED_HEAD_LINES:
                continue  # leave head untouched

            orig = line

            # 1) rename labels/refs
            def _rename_sub(m):
                stats["label_renames"] += 1
                old = m.group(2)
                new = RENAME[old]
                renamed_pairs.append((old, new))
                return m.group(1) + new + m.group(3)

            line = ref_cmd_re.sub(_rename_sub, line)

            # 2) bare \eqref -> \cref
            n = len(bare_eqref_re.findall(line))
            if n:
                stats["eqref_to_cref"] += n
                line = bare_eqref_re.sub(r"\\cref{", line)

            # 3) bare \ref -> \cref
            n = len(bare_ref_re.findall(line))
            if n:
                stats["ref_to_cref"] += n
                line = bare_ref_re.sub(r"\\cref{", line)

            # 4) strip handwritten 式/图/表/节 prefix before \cref{
            n = len(hand_prefix_re.findall(line))
            if n:
                stats["hand_prefix_stripped"] += n
                line = hand_prefix_re.sub(r"\\cref{", line)

            if line != orig:
                lines[idx] = line
                changed = True

        if changed:
            out = "".join(lines)
            with open(f, "wb") as fh:
                fh.write(out.encode("utf-8"))
            stats["files_touched"] += 1

    print("=== STATS ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  total distinct labels renamed: {len(RENAME)}")
    # verify all rename keys were used
    used = set(p[0] for p in renamed_pairs)
    missing = set(RENAME.keys()) - used
    if missing:
        print(f"  WARNING: {len(missing)} rename keys not found in source:")
        for m in sorted(missing):
            print(f"    - {m!r}")
    else:
        print("  all rename keys were applied at least once")

if __name__ == "__main__":
    main()
