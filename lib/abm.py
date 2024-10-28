import random
import string

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

class Agent(Base):
    def __init__(self, id: str = generate_random_string(4)):
        super().__init__(id)

class Environment(Base):
    def __init__(self, id: str = generate_random_string(4), generate_agents:tuple[Agent, int]=None):
        super().__init__(id)
        self._agents = []
        if generate_agents:
            agent_class, number = generate_agents
            if isinstance(agent_class, type) and issubclass(agent_class, Agent) and isinstance(number, int) and number > 0:
                self._generate(agent_class, number)
    
    def _generate(self, Agent: type[Agent], number: int):
        for i in range(number):
            self._agents.append(Agent(id=f'{self.id}_{i}'))