from lib.abm import Agent, Environment, generate_random_string
from .abm import *
from .iiim_model import *
from typing import Union, List, Tuple
import math

class ImmuneAgent(Agent):
    def __init__(self, id: str = generate_random_string(4), position: Tuple[int, int] = None, v=0, dt=0.01, data:ImmuneData=None):
        super().__init__(id, position)
        self.virus_simulation = ImmuneSimulation(virus=v, dt=dt)
        self.immunity_level = 0.0
        self.virus_level = 0.0
        self.add_virus = self.virus_simulation.add_virus
        if data:
            self.virus_simulation.update_system(data=data)

    def update_immunity(self, day=0.1):
        """更新免疫水平和病毒模拟"""
        self.virus_simulation.simulate(total_time=day)  # 每个时间步进行一次模拟
        self.immunity_level = self.virus_simulation.immune_cells  # 更新免疫水平
        self.virus_level = self.virus_simulation.virus  # 更新病毒水平

    def spread_virus(self, other_agents: List[Agent]):
        """尝试感染周围的代理，并按距离计算感染比例"""
        for other in other_agents:
            if other.id == self.id: continue
            if self.position != other.position:  # 仅在不同位置的代理之间传播
                distance = self.calculate_distance(other)
                infection_ratio = self.calculate_infection_ratio(distance)
                other.add_virus(self.virus_level * infection_ratio)
                print(f'Agent {self.id} increased Agent {other.id}\'s virus level by {self.virus_level * infection_ratio:.2f} (Distance: {distance:.2f})')
            else:
                infection_ratio = 0.9
                other.add_virus(self.virus_level * infection_ratio)
                print(f'Agent {self.id} increased Agent {other.id}\'s virus level by {self.virus_level * infection_ratio:.2f} (Distance: 0)')

    def calculate_distance(self, other: Agent) -> float:
        """计算当前代理与其他代理之间的距离"""
        return math.sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)

    def calculate_infection_ratio(self, distance: float) -> float:
        """根据距离计算感染比例"""
        max_distance = 5.0  # 最大影响距离
        if distance <= max_distance:
            return 1 - (distance / max_distance)  # 距离越近，比例越高
        return 0.0  # 超过最大距离，不感染

class ImmuneEnvironment(Environment):
    def __init__(self, id: str = ..., generate_agents: Tuple[Agent | int] = None, agents: List[Agent] = None, sub_env: List[Environment] = None, parent_env: List[Environment] = None, map_size: Tuple = None):
        super().__init__(id, generate_agents, agents, sub_env, parent_env, map_size)
        self.agent_count_history = []  # 记录代理数量变化
        self.infected_count_history = []  # 记录感染人数变化

    def step(self):
        """执行环境中的一个时间步"""
        for agent in self._agents:
            agent.move(self.map_size)  # 移动代理
            if isinstance(agent, ImmuneAgent):
                agent.update_immunity()  # 更新免疫代理的免疫水平
                agent.spread_virus(self.get_agents())

        # 记录当前代理数量和感染人数
        self.agent_count_history.append(len(self._agents))
        self.infected_count_history.append(self.count_infected())

    def count_infected(self, level:float = 10) -> int:
        """返回感染代理的数量"""
        return sum(1 for agent in self._agents if agent.virus_level >= level)


