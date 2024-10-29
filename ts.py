import numpy as np
import matplotlib.pyplot as plt

# 参数设置
N = 1000      # 总细胞数
I0 = 1        # 初始感染细胞
C0 = 50       # 初始免疫细胞
S0 = N - I0   # 初始易感细胞
beta = 0.3    # 感染率
delta = 0.1   # 免疫细胞对感染细胞的清除率
timesteps = 160  # 迭代时间步

# 初始化数组
S = np.zeros(timesteps)
I = np.zeros(timesteps)
C = np.zeros(timesteps)

S[0] = S0
I[0] = I0
C[0] = C0

# 模拟过程
for t in range(1, timesteps):
    new_infections = beta * S[t-1] * I[t-1] / N
    new_clearances = delta * C[t-1] * I[t-1] / N
    
    S[t] = S[t-1] - new_infections
    I[t] = I[t-1] + new_infections - new_clearances
    C[t] = C[t-1] + new_clearances  # 免疫细胞数量增加

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(S, label='易感细胞 (S)', color='blue')
plt.plot(I, label='感染细胞 (I)', color='red')
plt.plot(C, label='免疫细胞 (C)', color='green')
plt.title('病毒与免疫细胞动态模拟')
plt.xlabel('时间 (天)')
plt.ylabel('细胞数')
plt.legend()
plt.grid()
plt.show()