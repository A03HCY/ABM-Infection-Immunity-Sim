from lib.abm_model import *
import matplotlib.pyplot as plt

# 创建环境
environment = ImmuneEnvironment(map_size=[50,50])

print(environment.map_size)

# 创建免疫代理并添加到环境中
for d in range(50):
    environment.add_agent(ImmuneAgent(id=d))

environment.add_agent(ImmuneAgent(v=0.1))

# 运行仿真
for _ in range(300):
    environment.step()

# 输出代理的病毒水平
for agent in environment._agents:
    print(f'Agent ID: {agent.id}, Virus Level: {agent.virus_simulation.virus:.2f}')


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
