import numpy as np
import matplotlib.pyplot as plt
from lib.iiim import Cell

# 初始条件
CT = 1.7e-14   # 总细胞数量
AT = 8.5e-16   # 初始抗体量
MT = 1e-18     # 初始巨噬细胞数量
TH1_T = 1e-18  # TH1细胞的目标浓度
TH2_T = 1e-18  # TH2细胞的目标浓度
TE_T = 1e-18   # TE细胞的目标浓度
B_T = 1e-21    # B细胞的目标浓度
VT = 1e-16

# 参数设置

# 健康细胞感染和病毒相关参数
s = 3.43e13    # 健康细胞感染速率
v = 970.9      # 病毒生成速率
g_vc = 5.39e13 # 病毒感染细胞的损耗率
g_va = 3.56e8  # 病毒受到抗体的中和率
b_ce = 1.9e8   # 破坏细胞常数
n = 0

# 抗体相关参数
g_av = 7.77e7  # 抗体对病毒的抑制率
b_a = 0.39     # 抗体生成率
t_a = 0        # 抗体生成延迟

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
p_e = 2        # TE细胞生成的比例
t_C = 3        # TE细胞响应的延迟
b_ec = 1.2e13  # TE细胞因感染细胞而死亡的损耗率
a_e = 0.4002   # TE细胞的自然死亡率

# B细胞的生成参数
b_pB = 5.4e46  # B细胞生成率
p_b = 1        # B细胞生成的比例
t_B = 1        # B细胞响应的延迟
a_b = 0.1      # B细胞的自然死亡率



# 初始化参数
delta_t = 1e-4  # 时间步长
total_time = 1   # 总时间（单位：天）
time_steps = int(total_time / delta_t)  # 计算的时间步数

V = Cell(VT, delta=delta_t, balance_value=CT * v)
A = Cell(AT, delta=delta_t, balance_value=AT)

A.cell_adjustment_formula('add', 4 * v, A.get_value, A.balance_ratio)
V.cell_adjustment_formula('add', v, V.get_value, V.balance_ratio)

V.cell_adjustment_formula('sub', g_va, V.get_value(), A.get_value)

# 循环 300 次
for _ in range(300):
    V.step()

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(V.history, label='Current Value', color='blue')
plt.title('Cell Growth Over Time')
plt.xlabel('Steps')
plt.ylabel('Current Value')
plt.grid(True)
plt.legend()
plt.show()