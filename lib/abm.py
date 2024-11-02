import random
import string
import abc
from typing import Union


def generate_random_string(length: int) -> str:
    """生成指定长度的随机字符，包括大小写字母和数字"""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def clamp_value(value: float, min_value: float, max_value: float) -> float:
    """限制值在指定范围内"""
    return max(min(value, max_value), min_value)


class Base:
    def __init__(self, id: str = generate_random_string(4)):
        self.id = id


class Agent:...

class Environment:
    def size(self, deepth:int=0) -> int:...
    def add(self, object):...
    def random_agents(self, number:int, deepth:int=0) -> list[Agent]:...
    def get_agents(self, deepth:int=0):...
    def add_agent(self, agent:Agent):...

class Action:
    @abc.abstractmethod
    def schedule(self, agent:Agent, env:Environment):...

class Schedule(Base):
    def __init__(self, id: str = generate_random_string(4)):
        super().__init__(id)
        self._schedule = []
    
    def add(self, env:Environment, action:type[Action]):...

class Agent(Base):
    def __init__(self, id: str = generate_random_string(4), position:tuple=None):
        super().__init__(id)
        self.position = position if position is not None else (0, 0)
    
    def move(self, grid_size:tuple):
        # 随机选择上下左右移动
        direction = random.choice(["up", "down", "left", "right"])
        x, y = self.position  # 当前坐标
        if direction == "up" and y < grid_size[1] - 1:
            y += 1
        elif direction == "down" and y > 0:
            y -= 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < grid_size[0] - 1:
            x += 1
        self.position = (x, y)  # 更新位置

class Environment(Base):
    def __init__(self, id: str = generate_random_string(4), generate_agents:tuple[Agent, int]=None, agents:list[Agent]=None, sub_env:list[Environment]=None, parent_env:list[Environment]=None, map_size:tuple=None):
        super().__init__(id)
        self._agents = agents if agents is not None else []
        self._sub_env = sub_env if sub_env is not None else []
        self._parent_env = parent_env if parent_env is not None else []
        self.map_size = map_size if map_size is not None else (10, 10)
        if generate_agents:
            agent_class, number = generate_agents
            if isinstance(agent_class, type) and issubclass(agent_class, Agent) and isinstance(number, int) and number > 0:
                self._generate(agent_class, number)
    
    def _generate(self, Agent: type[Agent], number: int):
        print(number)
        for i in range(number):
            x = random.randint(0, self.map_size[0] - 1)
            y = random.randint(0, self.map_size[1] - 1)
            self._agents.append(Agent(id=f'{self.id}_{i}', position=(x, y)))
    
    def resize_map(self, x:int, y:int):
        self.map_size = (x, y)
    
    def replace_agents(self):
        for agent in self._agents:
            x = random.randint(0, self.map_size[0] - 1)
            y = random.randint(0, self.map_size[1] - 1)
            agent.position = (x, y)

    def size(self, deepth:int=0) -> int:
        size = len(self._agents)
        deepth -= 1
        if deepth == -1: return size
        for env in self._sub_env:
            size += env.size(deepth=deepth)
        return size
    
    def get_agents(self, deepth:int=0):
        agents = self._agents
        deepth -= 1
        if deepth == -1: return agents
        for env in self._sub_env:
            agents += env.get_agents(deepth=deepth)
        return agents
    
    def add(self, object):
        if type(object) == Agent:
            self.add_agent(object)
        if type(object) == Environment:
            self._sub_env.append(object)
        if type(object) == list:
            for obj in object:
                self.add(obj)
    
    def add_parent_env(self, env:Environment):
        self._parent_env.append(env)

    def transfer_agent_to(self, target_env:Environment, agent:Agent):
        """将个体从当前环境转移到目标环境"""
        if agent in self.agents:
            self._agents.remove(agent)
            target_env.add_agent(agent)
    
    def add_agent(self, agent:Agent):
        """在当前环境中随机放置个体"""
        agent.position = (random.randint(0, self.map_size[0] - 1),
                          random.randint(0, self.map_size[1] - 1))
        self._agents.append(agent)
    
    def random_agents(self, number:int, deepth:int=0) -> list[Agent]:
        agents = self.get_agents(deepth=deepth)
        sample_size = min(number, len(agents))
        return random.sample(agents, sample_size)
    
    def filter_agents(self, attribute:str, value, deepth:int=0) -> list[Agent]:
        return [agent for agent in self.get_agents(deepth=deepth) if getattr(agent, attribute, None) == value]
    