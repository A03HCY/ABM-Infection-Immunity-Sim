import numpy as np
import matplotlib.pyplot as plt

# 参数设置
nu = 0.1  # 病毒复制率
g_va = 0.01  # 抗体中和病毒的速率
g_vm = 0.1  # 巨噬细胞清除病毒的速率
g_ec = 0.05  # CTL清除感染细胞的速率
A_T = 1e6  # 抗体的最大浓度
C_T = 1e6  # 最大感染细胞数
tau_H1 = 1  # TH1细胞时间延迟
delta_t = 0.1  # 时间步长
total_time = 30  # 总时间

# 初始化变量
time_steps = int(total_time / delta_t)
V = np.zeros(time_steps)  # 自由病毒浓度
M_v = np.zeros(time_steps)  # 巨噬细胞浓度
TH1 = np.zeros(time_steps)  # TH1细胞浓度
TH2 = np.zeros(time_steps)  # TH2细胞浓度
T_e = np.zeros(time_steps)  # 细胞毒性T细胞浓度
B = np.zeros(time_steps)  # B细胞浓度
A = np.zeros(time_steps)  # 抗体浓度
C_v = np.zeros(time_steps)  # 感染细胞浓度
m = np.zeros(time_steps)  # 损伤细胞浓度

# 初始条件
V[0] = 1e-15  # 初始病毒浓度
M_v[0] = 0  # 初始巨噬细胞浓度
TH1[0] = 1e2  # 初始TH1细胞浓度
TH2[0] = 1e2  # 初始TH2细胞浓度
T_e[0] = 0  # 初始CTL浓度
B[0] = 0  # 初始B细胞浓度
A[0] = 0  # 初始抗体浓度
C_v[0] = 0  # 初始感染细胞浓度
m[0] = 0  # 初始损伤细胞浓度

# 时间迭代
for t in range(1, time_steps):
    # 更新病毒浓度
    V[t] = V[t-1] + (nu * C_v[t-1] * (1 - C_v[t-1] / C_T) - g_va * A[t-1] * V[t-1] - g_vm * M_v[t-1] * V[t-1]) * delta_t
    
    # 更新巨噬细胞浓度
    M_v[t] = M_v[t-1] + (0.1 * V[t-1] - 0.05 * M_v[t-1]) * delta_t  # 示例公式
    
    # 更新TH1细胞浓度
    TH1[t] = TH1[t-1] + (0.01 * M_v[t-1] * (1 - TH1[t-1] / 100) - 0.01 * TH1[t-1]) * delta_t
    
    # 更新TH2细胞浓度
    TH2[t] = TH2[t-1] + (0.01 * M_v[t-1] * (1 - TH2[t-1] / 100) - 0.01 * TH2[t-1]) * delta_t
    
    # 更新细胞毒性T细胞浓度
    T_e[t] = T_e[t-1] + (0.01 * M_v[t-1] * TH1[t-1] - g_ec * T_e[t-1]) * delta_t
    
    # 更新B细胞浓度
    B[t] = B[t-1] + (0.01 * M_v[t-1] * TH2[t-1] - 0.01 * B[t-1]) * delta_t
    
    # 更新抗体浓度
    A[t] = A[t-1] + (0.1 * A[t-1] * (1 - A[t-1] / A_T) - g_va * V[t-1] * A[t-1]) * delta_t
    
    # 更新感染细胞浓度
    C_v[t] = C_v[t-1] + (nu * V[t-1] - g_ec * T_e[t-1] * C_v[t-1]) * delta_t
    
    # 更新损伤细胞浓度
    m[t] = m[t-1] + (g_ec * T_e[t-1] * C_v[t-1] - 0.01 * m[t-1]) * delta_t

# 绘制结果
plt.figure(figsize=(12, 10))

plt.subplot(4, 2, 1)
plt.plot(np.arange(0, total_time, delta_t), V, label='Virus Load (V)')
plt.title('Virus Load Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Virus Concentration')

plt.subplot(4, 2, 2)
plt.plot(np.arange(0, total_time, delta_t), M_v, label='Macrophages (M_v)', color='orange')
plt.title('Macrophages Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Macrophage Concentration')

plt.subplot(4, 2, 3)
plt.plot(np.arange(0, total_time, delta_t), TH1, label='Helper T Cells (TH1)', color='green')
plt.title('TH1 Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('TH1 Concentration')

plt.subplot(4, 2, 4)
plt.plot(np.arange(0, total_time, delta_t), T_e, label='Cytotoxic T Cells (T_e)', color='red')
plt.title('Cytotoxic T Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('T_e Concentration')

plt.subplot(4, 2, 5)
plt.plot(np.arange(0, total_time, delta_t), B, label='B Cells (B)', color='purple')
plt.title('B Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('B Cell Concentration')

plt.subplot(4, 2, 6)
plt.plot(np.arange(0, total_time, delta_t), A, label='Antibodies (A)', color='brown')
plt.title('Antibody Concentration Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Antibody Concentration')

plt.subplot(4, 2, 7)
plt.plot(np.arange(0, total_time, delta_t), C_v, label='Infected Cells (C_v)', color='blue')
plt.title('Infected Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Infected Cell Concentration')

plt.subplot(4, 2, 8)
plt.plot(np.arange(0, total_time, delta_t), m, label='Damaged Cells (m)', color='gray')
plt.title('Damaged Cells Over Time')
plt.xlabel('Time (days)')
plt.ylabel('Damaged Cell Concentration')

plt.tight_layout()
plt.show()