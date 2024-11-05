from lib.abm_model import *
import matplotlib.pyplot as plt

# 创建环境
environment = ImmuneEnvironment(map_size=[50,50])

print(environment.map_size)

# 创建免疫代理并添加到环境中
for d in range(50):
    environment.add_agent(ImmuneAgent(id=d))

i = ImmuneAgent()
i.add_virus(Virus('cod', 0.1, ImmuneData()))

environment.add_agent(i)

# 运行仿真
for t in range(365):
    environment.step()

# 输出代理的病毒水平
for agent in environment._agents:
    print(f'Agent ID: {agent.id}, Virus Level: {agent.virus_simulation.total_virus:.2f}')


# 绘制图形
plt.figure(figsize=(10, 6))

for agent in environment.get_agents():
    plt.plot(agent.virus_simulation.virus_values, label=f'Agent {agent.id}')


# 添加标题和标签
plt.title('Virus Levels Over Time for Each Agent')
plt.xlabel('Time Steps')
plt.ylabel('Virus Level')
plt.legend()  # 显示图例
plt.grid()    # 显示网格
plt.tight_layout()  # 自动调整布局

# 显示图形
plt.show()

# 绘制感染人数变化
plt.figure(figsize=(12, 6))
plt.plot(environment.infected_count_history, label='Infected Count', color='red', linestyle='--', linewidth=2)

plt.title('Infected Count Over Time')
plt.xlabel('Time Steps')
plt.ylabel('Number of Infected Agents')
plt.legend()  # 显示图例
plt.grid()    # 显示网格
plt.tight_layout()  # 自动调整布局
plt.show()

# 绘制结果
plt.figure(figsize=(12, 12))

# 绘制病毒数量
plt.subplot(3, 2, 1)
plt.plot(i.virus_simulation.time_series, i.virus_simulation.req_all_virus_history(), label='Virus Quantity (V)', color='blue')
plt.title('Virus Quantity Over Time')
plt.xlabel('Time')
plt.ylabel('Virus Quantity (V)')
plt.grid()
plt.legend()

# 绘制感染细胞数量
plt.subplot(3, 2, 2)
plt.plot(i.virus_simulation.time_series, i.virus_simulation.infected_values, label='Infected Cells (I)', color='green')
plt.title('Infected Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Infected Cells (I)')
plt.axhline(y=0, color='blue', linestyle='--', label='Initial Infected Cells')
plt.grid()
plt.legend()

# 绘制健康细胞数量
plt.subplot(3, 2, 3)
plt.plot(i.virus_simulation.time_series, i.virus_simulation.healthy_values, label='Healthy Cells (H)', color='orange')
plt.title('Healthy Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Healthy Cells (H)')
plt.axhline(y=0, color='blue', linestyle='--', label='Healthy Cells Min')
plt.grid()
plt.legend()

# 绘制免疫细胞数量
plt.subplot(3, 2, 4)
plt.plot(i.virus_simulation.time_series, i.virus_simulation.immune_values, label='Immune Cells (M)', color='purple')
plt.title('Immune Cells Over Time')
plt.xlabel('Time')
plt.ylabel('Immune Cells (M)')
plt.grid()
plt.legend()

# 绘制抗体数量
plt.subplot(3, 2, 5)
plt.plot(i.virus_simulation.time_series, i.virus_simulation.antibody_native_values, label='Antibodies (A)', color='cyan')
plt.title('Antibodies Over Time')
plt.xlabel('Time')
plt.ylabel('Antibodies (A)')
plt.grid()
plt.legend()

plt.tight_layout(pad=3.0)  # 增加子图之间的间距
plt.show()