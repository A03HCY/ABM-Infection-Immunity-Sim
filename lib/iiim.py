import numpy as np
import matplotlib.pyplot as plt

# 初始化参数
delta_t = 1e-4  # 时间步长
total_time = 1   # 总时间（单位：天）
time_steps = int(total_time / delta_t)  # 计算的时间步数

# 初始化数组
V = np.zeros(time_steps)  # 病毒浓度数组
A = np.zeros(time_steps)  # 抗体浓度数组
CV = np.zeros(time_steps)  # 感染细胞数量数组
MSV = np.zeros(time_steps)  # 刺激的巨噬细胞数量数组
TH1 = np.zeros(time_steps)  # 类1辅助T淋巴细胞数量数组
TH2 = np.zeros(time_steps)  # 类2辅助T淋巴细胞数量数组

# 初始条件
V[0] = 1e-15   # 初始病毒量
A[0] = 8.5e-16 # 初始抗体量
CV[0] = 0      # 初始感染细胞数量
TH1[0] = 0     # 初始TH1细胞数量
TH2[0] = 0     # 初始TH2细胞数量
CT = 1.7e-14   # 总细胞数量
MT = 1e-18     # 初始巨噬细胞数量（未使用）
TH1_T = 1e-18  # TH1细胞的目标浓度
TH2_T = 1e-18  # TH2细胞的目标浓度

# 参数设置
v = 970.9      # 病毒生成速率
s = 3.43e13    # 健康细胞感染速率
a_m = 3.3      # 巨噬细胞的自然死亡率
g_vc = 5.39e13 # 感染损耗率
g_va = 3.56e8  # 抗体中和率
g_av = 7.77e7  # 抗体对病毒的抑制率
g_vm = 1.7     # 巨噬细胞对病毒的清除率

# TH1和TH2细胞的生成参数
b_hMv = 1e28   # TH1细胞生成率
p_hMv = 4      # TH1细胞生成的比例
t_H1 = 6       # TH1细胞响应的延迟
a_h = 1        # TH1细胞的自然死亡率

b_hB = 3.15e28 # TH2细胞生成率
p_hB = 4       # TH2细胞生成的比例
t_H2 = 6       # TH2细胞响应的延迟
a_hB = 1       # TH2细胞的自然死亡率

# 主循环
for t in range(1, time_steps):
    Chiv = CT - CV[t-1]  # 当前健康细胞数量

    # 更新病毒量
    V[t] = V[t-1] + (v * CV[t-1] * (1 - CV[t-1] / CT)) * delta_t  # 病毒自然增长
    V[t] -= (g_vc * Chiv * V[t-1]) * delta_t  # 由于感染导致的病毒损耗
    V[t] -= (g_va * A[t-1] * V[t-1] * (1 + 1e6 * (CV[t-1] / CT))) * delta_t  # 抗体中和导致的损耗
    V[t] -= (g_vm * MSV[t-1] * V[t-1]) * delta_t  # 巨噬细胞对病毒的清除

    # 更新感染细胞数量
    CV[t] = CV[t-1] + s * V[t] * Chiv * delta_t  # 新增感染细胞

    # 更新抗体量
    A[t] = A[t-1] - (g_av * A[t-1] * V[t-1]) * delta_t  # 抗体因中和病毒而减少

    # 更新刺激的巨噬细胞数量
    MSV[t] = MSV[t-1] + (g_vm * MT * V[t-1]) * delta_t  # 巨噬细胞数量增加
    MSV[t] -= (a_m * MSV[t-1]) * delta_t  # 巨噬细胞自然死亡

    # 更新TH1细胞数量
    TH1[t] = TH1[t-1] + (b_hMv * (p_hMv * MSV[t-t_H1] * TH1[t-t_H1] - MSV[t-1] * TH1[t-1])) * delta_t  # TH1细胞生成
    TH1[t] += a_h * (TH1_T - TH1[t-1]) * delta_t  # 调整TH1细胞数量接近目标浓度

    # 更新TH2细胞数量
    TH2[t] = TH2[t-1] + (b_hB * (p_hB * MSV[t-t_H2] * TH2[t-t_H2] - MSV[t-1] * TH2[t-1])) * delta_t  # TH2细胞生成
    TH2[t] += a_hB * (TH2_T - TH2[t-1]) * delta_t  # 调整TH2细胞数量接近目标浓度

# 创建时间数组
time = np.arange(0, total_time, delta_t)  # 时间数组

# 创建图形
plt.figure(figsize=(12, 12))

# 绘制病毒浓度图
plt.subplot(4, 1, 1)  # 4行1列的第1个图
plt.plot(time, V, label='Virus Concentration (V)', color='blue')
plt.xlabel('Time (days)')
plt.ylabel('Concentration')
plt.title('Virus Concentration Over Time')
plt.legend()
plt.grid()

# 绘制感染细胞数量图
plt.subplot(4, 1, 2)  # 4行1列的第2个图
plt.plot(time, CV, label='Infected Cells (CV)', color='red')
plt.xlabel('Time (days)')
plt.ylabel('Concentration')
plt.title('Infected Cells Over Time')
plt.legend()
plt.grid()

# 绘制抗体浓度图
plt.subplot(4, 1, 3)  # 4行1列的第3个图
plt.plot(time, A, label='Antibody Concentration (A)', color='green')
plt.xlabel('Time (days)')
plt.ylabel('Concentration')
plt.title('Antibody Concentration Over Time')
plt.legend()
plt.grid()

# 绘制TH1细胞数量图
plt.subplot(4, 1, 4)  # 4行1列的第4个图
plt.plot(time, TH1, label='TH1 Cells Concentration', color='purple')
plt.xlabel('Time (days)')
plt.ylabel('Concentration')
plt.title('TH1 Cells Over Time')
plt.legend()
plt.grid()

# 调整布局并显示图形
plt.tight_layout()
plt.show()