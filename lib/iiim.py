import numpy as np
from typing import Union, Callable, Tuple

class Base:
    def __init__(self):
        self.formulas = {}  # 存储公式的字典
        self.formula_id_counter = 0  # 用于分配唯一公式ID

    def register_formula(self, *args: Union[float, int, Callable, Tuple[Callable, ...]]) -> int:
        """
        注册一个公式并返回公式的唯一标识符。
        
        参数：
        *args：包含系数、函数或函数元组的参数。
        - float 或 int 类型将作为系数
        - callable 将直接作为公式中的函数
        - 元组形式 (callable, *args) 中，第一个元素是函数，剩下是函数参数

        返回：
        int：该公式的唯一标识符
        """
        formula_id = self.formula_id_counter  # 分配公式ID
        self.formulas[formula_id] = args  # 保存公式参数
        self.formula_id_counter += 1
        return formula_id  # 返回唯一标识符

    def evaluate_formula(self, formula_id: int) -> float:
        """
        根据公式ID计算公式结果。
        
        参数：
        formula_id：要计算的公式的标识符。
        
        返回：
        float：计算得到的结果
        """
        if formula_id not in self.formulas:
            raise ValueError(f"Formula ID {formula_id} not registered.")

        result = 1.0  # 初始结果设为1，便于后续乘法计算
        for element in self.formulas[formula_id]:
            if isinstance(element, (float, int)):
                # 如果是数字，直接作为系数
                result *= element
            elif callable(element):
                # 如果是函数且没有额外参数，直接调用
                result *= element()
            elif isinstance(element, tuple) and callable(element[0]):
                # 如果是元组且第一个是函数，则把元组的其余部分作为参数传入
                func, *params = element
                result *= func(*params)
            else:
                raise TypeError(f"Unsupported formula element type: {type(element)}")
        
        return result


class Living(Base):
    def __init__(self, initial_value, delta:float=0, balance_value=0):
        super().__init__()
        self.delta = delta
        self.initial_value = initial_value
        self.current_value = initial_value
        self.balance_value = balance_value
        self.natural_decay_info = {}
        self.history = []  # 用于记录每次 step 后的 current_value
        self.operation = {}
    
    def balance_ratio(self, time_diff: int = 0) -> float:
        """
        计算当前值与平衡值之间的比率。
        
        参数：
        - time_diff: 当前时刻到历史时刻的差值，默认为 0，表示使用当前值。
        
        返回：
        - float: 当前值与平衡值之间的比率。
        """
        # 如果 time_diff 为 0，则使用当前值
        if time_diff == 0:
            current_value = self.current_value
        else:
            # 否则使用历史值
            current_value = self.get_value(time_diff)

        if self.balance_value == 0:
            raise ValueError("balance_value 不能为零")

        # 计算平衡比率
        return 1 - current_value / self.balance_value

    def get_value(self, time_diff: int=1):
        """
        返回从当前时刻回溯 time_diff 个时间步的单一值。
        
        参数：
        - time_diff: 当前时刻到历史时刻的差值，必须为正整数。
        
        返回：
        - float: `history` 列表中的指定值。
        """
        if time_diff <= 0:
            return self.current_value
            # raise ValueError("time_diff 必须为正整数")
        if time_diff > len(self.history):
            return self.current_value
            # raise ValueError("time_diff 超出历史记录的范围")

        # 返回指定时间步的单一历史值
        return self.history[-time_diff]
    
    def cell_adjustment_formula(self, operation: str, *args) -> int:
        """
        注册一个用于更改 current_value 的公式，指定加或减。

        参数：
        operation: 指定公式结果对 current_value 的影响，加 "add" 或减 "sub"。
        *args: 传入的参数将与 register_formula 方式相同。

        返回：
        int：该公式的唯一标识符
        """
        # 检查加减操作参数是否有效
        if operation not in {"add", "sub"}:
            raise ValueError("Operation must be 'add' or 'sub'")
        
        # 注册公式并保存带有操作符的公式
        formula_id = self.register_formula(*args)
        self.operation[formula_id] = operation
        return formula_id

    def natural_decay(self, decay_rate: float) -> int:
        """
        定义自然死亡率公式，其中包含 decay_rate 和 current_value。
        
        参数：
        decay_rate: 自然死亡率，表示每个时间步减少的细胞比例。
        
        返回：
        int：该公式的唯一标识符
        """
        # 公式的参数包含衰减率和当前细胞数量（作为一个函数）
        formula_id = self.register_formula(decay_rate, lambda: self.current_value)
        self.natural_decay_info[formula_id] = decay_rate
        return formula_id
    
    def register_balance_function(self, coefficient: float) -> int:
        """
        注册数量平衡函数，计算系数与平衡差距率的积。
        
        参数：
        - coefficient: 用于计算的系数。
        
        返回：
        - int: 注册的公式的唯一标识符。
        """
        # 定义公式为系数乘以当前的平衡差距率
        formula = lambda: coefficient * self.balance_ratio() * self.get_value()

        # 注册公式并返回唯一标识符
        return self.register_formula(formula)
    
    def clear_natural_decay(self):
        """
        清除所有注册的自然衰减公式。
        """
        # 清除 natural_decay_formulas 中的条目
        for formula_id in list(self.natural_decay_info.keys()):
            if formula_id in self.formulas:
                del self.formulas[formula_id]  # 从 formulas 中移除公式
            del self.natural_decay_info[formula_id]
    
    def step(self):
        """
        执行一步操作，将当前值添加到历史记录中。
        可以在此处执行其他计算和更新操作。
        """
        # 将 current_value 添加到历史记录中
        self.history.append(self.current_value)
        for f in self.formulas:
            result = self.evaluate_formula(f) * self.delta
            if f in self.natural_decay_info:
                self.current_value -= result
                continue
            operation = self.operation.get(f, 'add')
            if operation == 'add':
                self.current_value += result
            if operation == 'sub':
                self.current_value -= result


class Cell(Living):
    def __init__(self, initial_value, delta:float=0, balance_value=0):
        super().__init__(initial_value, delta, balance_value)


import numpy as np
import matplotlib.pyplot as plt

# 创建 Cell 实例
cell = Cell(initial_value=10, delta=0.01, balance_value=50)


# 注册平衡函数，使用平衡系数 2
balance_coefficient = 23
cell.register_balance_function(balance_coefficient)

# 记录每一步的 current_value
data = []

# 循环 300 次
for _ in range(30):
    cell.step()
    data.append(cell.current_value)

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(data, label='Current Value', color='blue')
plt.title('Cell Growth Over Time')
plt.xlabel('Steps')
plt.ylabel('Current Value')
plt.grid(True)
plt.legend()
plt.show()