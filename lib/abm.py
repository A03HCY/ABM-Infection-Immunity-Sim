import random
import string
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


class Agent(Base):
    def __init__(self, id: str = generate_random_string(4)):
        super().__init__(id)

class Environment(Base):
    def __init__(self, id: str = generate_random_string(4), generate_agents:tuple[Agent, int]=None, agents:list[Agent]=None, sub_env:list[Environment]=None):
        super().__init__(id)
        self._agents = agents if agents is not None else []
        self._subenv = sub_env if sub_env is not None else []
        if generate_agents:
            agent_class, number = generate_agents
            if isinstance(agent_class, type) and issubclass(agent_class, Agent) and isinstance(number, int) and number > 0:
                self._generate(agent_class, number)
    
    def _generate(self, Agent: type[Agent], number: int):
        print(number)
        for i in range(number):
            self._agents.append(Agent(id=f'{self.id}_{i}'))
    
    def size(self, deepth:int=0) -> int:
        size = len(self._agents)
        deepth -= 1
        if deepth == -1: return size
        for env in self._subenv:
            size += env.size(deepth=deepth)
        return size
    
    def get_agents(self, deepth:int=0):
        agents = self._agents
        deepth -= 1
        if deepth == -1: return agents
        for env in self._subenv:
            agents += env.get_agents(deepth=deepth)
        return agents
    
    def add(self, object):
        if type(object) == Agent:
            self._agents.append(object)
        if type(object) == Environment:
            self._subenv.append(object)
        if type(object) == list:
            for obj in object:
                self.add(obj)
    
    def random_agents(self, number:int, deepth:int=0) -> list[Agent]:
        agents = self.get_agents(deepth=deepth)
        sample_size = min(number, len(agents))
        return random.sample(agents, sample_size)