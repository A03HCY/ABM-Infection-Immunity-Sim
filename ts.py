import random
import math

class Agent:
    def __init__(self, position):
        self.position = position  # 位置坐标 (x, y)
        self.status = "healthy"  # 示例状态：'healthy', 'infected', 'immune'
    
    def move(self, env):
        # 随机选择本地移动或尝试跨环境移动
        if random.random() < 0.8:  # 80% 概率在当前环境内移动
            self._local_move(env.grid_size)
        else:  # 20% 概率尝试跨环境移动
            self._cross_environment_move(env)

    def _local_move(self, grid_size):
        # 随机选择上下左右移动
        direction = random.choice(["up", "down", "left", "right"])
        x, y = self.position
        if direction == "up" and y < grid_size - 1:
            y += 1
        elif direction == "down" and y > 0:
            y -= 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < grid_size - 1:
            x += 1
        self.position = (x, y)  # 更新位置

    def _cross_environment_move(self, env):
        # 若有父环境，可能进入父环境；若有子环境，可能进入子环境
        if env.parent and random.random() < 0.5:
            # 50% 概率尝试进入父环境
            env.transfer_agent_to(env.parent, self)
        elif env.sub_environments:
            # 随机选择一个子环境并尝试转移
            target_env = random.choice(env.sub_environments)
            env.transfer_agent_to(target_env, self)

# 环境类，支持嵌套和跨环境移动
class Environment:
    def __init__(self, grid_size, num_agents=0, infection_radius=1.5, parent=None):
        self.grid_size = grid_size
        self.infection_radius = infection_radius
        self.agents = self._generate_agents(num_agents)
        self.sub_environments = []  # 存储子环境
        self.parent = parent  # 可选的父环境引用

    def add_sub_environment(self, sub_env):
        """添加子环境"""
        self.sub_environments.append(sub_env)

    def _generate_agents(self, num_agents):
        """随机生成个体在地图上"""
        agents = []
        for _ in range(num_agents):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            agent = Agent(position=(x, y))
            agents.append(agent)
        return agents

    def transfer_agent_to(self, target_env, agent):
        """将个体从当前环境转移到目标环境"""
        # 移除个体并在目标环境中重新定位
        if agent in self.agents:
            self.agents.remove(agent)
            target_env.add_agent(agent)

    def add_agent(self, agent):
        """在当前环境中随机放置个体"""
        agent.position = (random.randint(0, self.grid_size - 1),
                          random.randint(0, self.grid_size - 1))
        self.agents.append(agent)

    def step(self):
        # 每个时间步个体移动并检查交互
        for agent in list(self.agents):  # 使用 list 避免在迭代中修改 self.agents
            agent.move(self)
            self.check_interactions(agent)

        # 更新每个子环境
        for sub_env in self.sub_environments:
            sub_env.step()
    
    def check_interactions(self, agent):
        # 检查是否有其他个体在交互范围内
        for other_agent in self.agents:
            if other_agent is not agent:
                distance = math.sqrt(
                    (agent.position[0] - other_agent.position[0])**2 +
                    (agent.position[1] - other_agent.position[1])**2
                )
                if distance <= self.infection_radius:
                    self.interact(agent, other_agent)
    
    def interact(self, agent1, agent2):
        # 示例交互逻辑：若 agent1 是感染者，则可能感染 agent2
        if agent1.status == "infected" and agent2.status == "healthy":
            infection_probability = 0.2  # 例如 20% 的感染概率
            if random.random() < infection_probability:
                agent2.status = "infected"

# 创建环境和子环境
main_env = Environment(grid_size=20, num_agents=20, infection_radius=5)
sub_env1 = Environment(grid_size=10, num_agents=10, infection_radius=5, parent=main_env)
sub_env2 = Environment(grid_size=10, num_agents=10, infection_radius=4, parent=main_env)

a = Agent((0, 0))
a.status = 'infected'

sub_env1.add_agent(a)

main_env.add_sub_environment(sub_env1)
main_env.add_sub_environment(sub_env2)

# 运行模拟
for _ in range(10):  # 模拟 10 个时间步
    main_env.step()
    # 统计或打印感染人数等信息
    infected_count_main = sum(1 for agent in main_env.agents if agent.status == "infected")
    infected_count_sub1 = sum(1 for agent in sub_env1.agents if agent.status == "infected")
    infected_count_sub2 = sum(1 for agent in sub_env2.agents if agent.status == "infected")
    print(f"主环境感染人数：{infected_count_main}")
    print(f"子环境 1 感染人数：{infected_count_sub1}")
    print(f"子环境 2 感染人数：{infected_count_sub2}")
