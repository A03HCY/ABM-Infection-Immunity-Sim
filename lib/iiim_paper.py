import numpy as np
import matplotlib.pyplot as plt

# 初始化参数
delta_t = 1e-2  # 时间步长
total_time = 1.5   # 总时间（单位：week）
time_steps = int(total_time / delta_t)  # 计算的时间步数

# 初始化数组
V = np.zeros(time_steps)  # 病毒浓度数组
A = np.zeros(time_steps)  # 抗体浓度数组
CV = np.zeros(time_steps)  # 感染细胞数量数组
MSV = np.zeros(time_steps)  # 刺激的巨噬细胞数量数组
TH1 = np.zeros(time_steps)  # 类1辅助T淋巴细胞数量数组
TH2 = np.zeros(time_steps)  # 类2辅助T淋巴细胞数量数组
TE = np.zeros(time_steps)   # 细胞毒性T淋巴细胞数量数组
B = np.zeros(time_steps)    # B淋巴细胞数量数组

# 初始条件
CT = 1.7e-14   # 总细胞数量
AT = 8.5e12    # 最大抗体量
MT = 1e-18     # 初始巨噬细胞数量
TH1_T = 1e-18  # TH1细胞的目标浓度
TH2_T = 1e-18  # TH2细胞的目标浓度
TE_T = 1e-18   # TE细胞的目标浓度
B_T = 1e-21    # B细胞的目标浓度

# 变量设置
V[0] = 1e-15   # 初始病毒量
A[0] = 8.5e-16      # 初始抗体量
CV[0] = 0      # 初始感染细胞数量
TH1[0] = TH1_T # 初始TH1细胞数量
TH2[0] = TH2_T # 初始TH2细胞数量
TE[0] = TE_T   # 初始细胞毒性T淋巴细胞数量
B[0] = B_T     # 初始B细胞数量

# 参数设置

# 健康细胞感染和病毒相关参数
s = 3.43e13    # 健康细胞感染速率
v = 970.9      # 病毒生成速率
g_vc = 5.39e13 # 病毒感染细胞的损耗率
g_va = 3.56e15  # 病毒受到抗体的中和率
b_ce = 1.9e8   # 破坏细胞常数
bm = 12.92
n = 0

# 抗体相关参数
g_av = 7.77e7  # 抗体对病毒的抑制率
b_a = 0.4     # 抗体生成率
t_a = 1        # 抗体生成延迟

# 巨噬细胞相关参数
g_vm = 1.7     # 巨噬细胞对病毒的清除率
a_m = 3.3      # 巨噬细胞的自然死亡率

# TH1细胞的生成参数
b_hMv = 1e28   # TH1细胞生成率
p_hMv = 4      # TH1细胞生成的比例
t_H1 = 6       # TH1细胞响应的延迟
a_h = 1        # TH1细胞的自然死亡率

# TH2细胞的生成参数
b_hB = 3.15e28 # TH2细胞生成率
p_hB = 4       # TH2细胞生成的比例
t_H2 = 6       # TH2细胞响应的延迟
a_hB = 1       # TH2细胞的自然死亡率

# TE细胞的生成参数
b_p = 5.5e45   # TE细胞生成率
p_e = 14        # TE细胞生成的比例
t_C = 3        # TE细胞响应的延迟
b_ec = 1.2e13  # TE细胞因感染细胞而死亡的损耗率
a_e = 0.4002   # TE细胞的自然死亡率

# B细胞的生成参数
b_pB = 5.4e46  # B细胞生成率
p_b = 1        # B细胞生成的比例
t_B = 1        # B细胞响应的延迟
a_b = 0.3      # B细胞的自然死亡率

# 主循环
for t in range(1, time_steps):

    Chiv = CT - CV[t-1]  # 当前健康细胞数量

    # 更新病毒量
    V[t] = V[t-1] + (v * CV[t-1] * (1 - CV[t-1] / CT)) * delta_t  # 病毒自然增长
    V[t] -= (g_va * A[t-1] * V[t-1] * (1 + (CV[t-1] / CT))) * delta_t  # 抗体中和导致的损耗
    V[t] -= (g_vm * MSV[t-1] * V[t-1]) * delta_t  # 巨噬细胞对病毒的清除
    V[t] -= (g_vc * Chiv * V[t-1]) * delta_t  # 由于感染导致的病毒损耗

    # 更新刺激的巨噬细胞数量
    MSV[t] = MSV[t-1] + (g_vm * MT * V[t-1]) * delta_t  # 巨噬细胞数量增加
    MSV[t] -= (a_m * MSV[t-1]) * delta_t  # 巨噬细胞自然死亡

    # 更新TH1细胞数量
    TH1[t] = TH1[t-1] + (b_hMv * (p_hMv * MSV[t-t_H1] * TH1[t-t_H1] - MSV[t-1] * TH1[t-1])) * delta_t  # TH1细胞生成
    TH1[t] += a_h * (TH1_T - TH1[t-1]) * delta_t  # 调整TH1细胞数量接近目标浓度

    # 更新TH2细胞数量
    TH2[t] = TH2[t-1] + (b_hB * (p_hB * MSV[t-t_H2] * TH2[t-t_H2] - MSV[t-1] * TH2[t-1])) * delta_t  # TH2细胞生成
    TH2[t] += a_hB * (TH2_T - TH2[t-1]) * delta_t  # 调整TH2细胞数量接近目标浓度

    # 更新细胞毒性T淋巴细胞数量
    TE[t] = TE[t-1] + b_p * (p_e * MSV[t - t_C] * TH1[t-t_C] * TH2[t-t_C]) * delta_t  # TE细胞生成
    TE[t] += b_ec * CV[t-1] * TE[t-1] * delta_t  # TE细胞因感染细胞而死亡
    TE[t] += a_e * (TE_T - TE[t-1]) * delta_t  # 调整TE细胞数量接近目标浓度
    
    # 更新B细胞数量
    B[t] = B[t-1] + b_pB * (p_b * TH2[t-1] * MSV[t-t_B] * B[t-t_B]) * delta_t  # B细胞生成
    B[t] += a_b * (B_T - B[t-1]) * delta_t  # 调整B细胞数量接近目标浓度

    # 更新抗体量
    A[t] = A[t-1] + b_a * A[t-t_a] * (1 - A[t-t_a]/AT) * delta_t  # 抗体生成
    A[t] -= (g_av * A[t-1] * V[t-1]) * delta_t  # 抗体因中和病毒而减少

    # 更新感染细胞数量
    CV[t] = CV[t-1] + s * V[t] * Chiv * delta_t  # 新增感染细胞
    CV[t] -= b_ce * CV[t-1] * TE[t-1] * delta_t  # 杀死的感染细胞


time = np.linspace(0, 14, time_steps)

# 绘图
plt.figure(figsize=(14, 12))

# 绘制病毒浓度
plt.subplot(4, 2, 1)
plt.plot(time, V, label='Virus Concentration (V)', color='red')
plt.title('Virus Concentration Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Concentration (mol/L)')
plt.grid(True)

# 绘制抗体浓度
plt.subplot(4, 2, 2)
plt.plot(time, A, label='Antibody Concentration (A)', color='blue')
plt.title('Antibody Concentration Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Concentration (mol/L)')
plt.grid(True)

# 绘制感染细胞数量
plt.subplot(4, 2, 3)
plt.plot(time, CV, label='Infected Cells (CV)', color='green')
plt.title('Infected Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

# 绘制刺激的巨噬细胞数量
plt.subplot(4, 2, 4)
plt.plot(time, MSV, label='Stimulated Macrophages (MSV)', color='orange')
plt.title('Stimulated Macrophages Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

# 绘制 TH1 细胞数量
plt.subplot(4, 2, 5)
plt.plot(time, TH1, label='TH1 Cells', color='purple')
plt.title('TH1 Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

# 绘制 TH2 细胞数量
plt.subplot(4, 2, 6)
plt.plot(time, TH2, label='TH2 Cells', color='brown')
plt.title('TH2 Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

# 绘制细胞毒性T淋巴细胞数量
plt.subplot(4, 2, 7)
plt.plot(time, TE, label='Cytotoxic T Cells (TE)', color='cyan')
plt.title('Cytotoxic T Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

# 绘制 B 细胞数量
plt.subplot(4, 2, 8)
plt.plot(time, B, label='B Cells', color='magenta')
plt.title('B Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Number of Cells')
plt.grid(True)

plt.tight_layout()
plt.show()