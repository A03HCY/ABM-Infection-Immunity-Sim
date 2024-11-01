import numpy as np
import matplotlib.pyplot as plt

# 参数设置
N = 100      # 正常细胞数量（最大感染细胞数量）
s = 0.5       # 病毒增长速率
a = 0.5       # 感染细胞增加的系数
u = 0.001      # 病毒损耗系数
i = 0.1       # 免疫细胞增加的系数
d = 500         # 延迟时间步数
dt = 0.01     # 时间步长
time = np.arange(0, 100, dt)  # 时间范围

# 初始化病毒数量、感染细胞数量和免疫细胞数量
virus = 0.1   # 初始病毒数量
infected_cells = 0  # 初始感染细胞数量
immune_cells = 0     # 初始免疫细胞数量

# 存储结果
virus_values = []
infected_values = []
healthy_values = []
immune_values = []

# 存储过去的感染细胞数量以计算免疫细胞
past_infected_cells = []

healthy_cells = N

# 模拟过程
for t in time:
    # 计算病毒数量变化
    dV = (s * (1 - infected_cells / N) * virus - u * virus * healthy_cells) * dt
    virus += dV
    
    # 计算感染细胞数量变化
    dI = a * dV
    infected_cells += dI
    # 限制感染细胞数量在 [0, N] 之间
    infected_cells = min(infected_cells, N)
    
    # 计算健康细胞数量
    healthy_cells = N - infected_cells

    # 计算免疫细胞数量，考虑延迟和感染细胞比例
    if len(past_infected_cells) >= d:
        immune_cells += i * past_infected_cells[-d] * (1 - past_infected_cells[-d] / N) * dt
    
    # 存储当前值
    virus_values.append(virus)
    infected_values.append(infected_cells)
    healthy_values.append(healthy_cells)
    immune_values.append(immune_cells)

    # 存储当前感染细胞数量以供延迟使用
    past_infected_cells.append(infected_cells)

# 绘制结果
plt.figure(figsize=(12, 10))

# 绘制病毒数量
plt.subplot(2, 2, 1)
plt.plot(time, virus_values, label='Virus Quantity (V)', color='blue')
plt.title('Virus Quantity Over Time')
plt.xlabel('Time')
plt.ylabel('Virus Quantity (V)')
plt.axhline(y=max(virus_values), color='red', linestyle='--', label='Max Virus')
plt.grid()
plt.legend()

# 绘制感染细胞数量
plt.subplot(2, 2, 2)
plt.plot(time, infected_values, label='Infected Cells (I)', color='green')
plt.title('Infected Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Infected Cells (I)')
plt.axhline(y=N, color='red', linestyle='--', label='Max Infected Cells (N)')
plt.axhline(y=0, color='blue', linestyle='--', label='Initial Infected Cells')
plt.grid()
plt.legend()

# 绘制健康细胞数量
plt.subplot(2, 2, 3)
plt.plot(time, healthy_values, label='Healthy Cells (N)', color='orange')
plt.title('Healthy Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Healthy Cells (N)')
plt.axhline(y=N, color='red', linestyle='--', label='Initial Healthy Cells (N)')
plt.axhline(y=0, color='blue', linestyle='--', label='Healthy Cells Min')
plt.grid()
plt.legend()

# 绘制免疫细胞数量
plt.subplot(2, 2, 4)
plt.plot(time, immune_values, label='Immune Cells (M)', color='purple')
plt.title('Immune Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Immune Cells (M)')
plt.axhline(y=max(immune_values), color='red', linestyle='--', label='Max Immune Cells')
plt.grid()
plt.legend()

plt.tight_layout(pad=3.0)  # 增加子图之间的间距
plt.show()