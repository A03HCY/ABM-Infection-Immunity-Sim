import numpy as np
import matplotlib.pyplot as plt

class Cell:
    """基础细胞类，管理每种细胞类型的数量和变化规则。"""
    def __init__(self, initial_value, target_value=0, growth_rate=0, decay_rate=0, response_delay=0, production_ratio=1.0):
        self.initial_value = initial_value
        self.value = initial_value             # 当前浓度
        self.target_value = target_value       # 平衡浓度
        self.growth_rate = growth_rate         # 增长速率
        self.decay_rate = decay_rate           # 衰减速率
        self.response_delay = response_delay   # 响应延迟，以时间步长为单位
        self.production_ratio = production_ratio  # 生成比例
        self.response_delay = response_delay   # 初始化延迟计数器
        if self.target_value == 0:
            self.target_value = initial_value if initial_value is not 0 else 1

    def update(self, delta_t):
        # 按生成比例增加细胞浓度
        self.value += self.production_ratio * self.growth_rate * (1 - self.value/self.target_value) * delta_t
        # 按衰减率减少细胞浓度
        self.value -= self.decay_rate * self.value * delta_t
