import matplotlib.pyplot as plt
import numpy as np
import dataclasses

@dataclasses.dataclass
class ImmuneData:
    """
    Initializes the immune simulation model with default or custom parameters.
    
    Parameters:
        N (float): Maximum normal cell count.
        s (float): Virus growth rate.
        a (float): Infection cell increase coefficient.
        u (float): Virus loss coefficient.
        i (float): Immune cell increase coefficient.
        g1 (float): Impact coefficient of antibodies on virus reduction.
        g2 (float): Antibody decay rate.
        g3 (float): Antibody increase rate.
        m (float): Immune cell natural death coefficient.
    """
    N: float = 100
    s: float = 0.8
    a: float = 0.5
    u: float = 1e-3
    i: float = 0.1
    m: float = 0.02
    g1: float = 0.01
    g2: float = 0.01
    g3: float = 0.1



class Virus:
    def __init__(self, virus_id, initial_count, system:ImmuneData, native=1):
        self.id = virus_id
        self.count = initial_count
        self.system = system
        self.native = native


class ImmuneSimulation:
    def __init__(self, N: float = 500, virus: float = 0, s: float = 2, a: float = 0.5, u: float = 0.001, 
                 i: float = 0.1, g1: float = 0.01, g2: float = 1, g3:float = 0.1, m: float = 0.05, 
                 d: float = 5, dt: float = 0.01):
        """
        Initializes the immune simulation model with default or custom parameters.
        
        Parameters:
            N (float): Maximum normal cell count.
            virus (float): Init virus count.
            s (float): Virus growth rate.
            a (float): Infection cell increase coefficient.
            u (float): Virus loss coefficient.
            i (float): Immune cell increase coefficient.
            g1 (float): Impact coefficient of antibodies on virus reduction.
            g2 (float): Antibody decay rate.
            g3 (float): Antibody increase rate.
            m (float): Immune cell natural death coefficient.
            d (float): Immune cell response delay in days.
            dt (float): Time step size for simulation.
        """
        # Parameters
        self.N = N
        self.s = s
        self.a = a
        self.u = u
        self.i = i
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        self.m = m
        self.d = int(d / dt)
        self.dt = dt
        
        # Initial values
        self.virus = virus
        self.infected_cells = 0
        self.immune_cells = 0
        self.antibodies = 0
        
        # Lists to store time series data for each variable
        self.virus_values = []
        self.infected_values = []
        self.immune_values = []
        self.antibody_values = []
        self.healthy_values = []
        self.time_series = []
    
    def update_system(self, data: ImmuneData, virus: float=None):
        self.N = data.N
        self.s = data.s
        self.a = data.a
        self.u = data.u
        self.i = data.i
        self.g1 = data.g1
        self.g2 = data.g2
        self.g3 = data.g3
        self.m = data.m
        self.virus = virus if virus is not None else self.virus
        return self
    
    def req_system(self) -> ImmuneData:
        res = ImmuneData(
            N=self.N, s=self.s, a=self.a, u=self.u, i=self.i, g1=self.g1, g2=self.g2, g3=self.g3, m=self.m
        )
        return res
        
    def update(self):
        """Updates the values of virus, infected cells, immune cells, and antibodies."""
        # Calculate healthy cells
        H = self.N - self.infected_cells
        
        # Virus change rate
        dV_dt = self.s * (1 - self.infected_cells / self.N) * self.virus - self.u * self.virus * H \
                - self.g1 * self.antibodies * self.virus * (1 + self.infected_cells / self.N)
        
        # Immune cells change rate, with delay in immune response
        delayed_infected = self.infected_values[-self.d] if len(self.infected_values) > self.d else 0
        dM_dt = self.i * delayed_infected * self.virus - self.m * self.immune_cells

        # Infected cells change rate
        delayed_immune = self.immune_values[-self.d] if len(self.immune_values) > self.d else 0
        dI_dt = self.a * max(0, dV_dt) - self.m * delayed_infected
        
        # Antibodies change rate
        dA_dt = self.g3 * self.immune_cells - self.g2 * self.antibodies
        
        # Update current values
        self.virus += dV_dt * self.dt - 1e-4
        self.infected_cells += dI_dt * self.dt
        self.immune_cells += dM_dt * self.dt
        self.antibodies += dA_dt * self.dt
        
        self.virus = abs(self.virus)
        # Store results
        self.virus_values.append(self.virus)
        self.infected_values.append(max(0, self.infected_cells))
        self.immune_values.append(self.immune_cells)
        self.antibody_values.append(self.antibodies)
        self.healthy_values.append(H)
        return self
        
    def simulate(self, total_time: float):
        """Runs the simulation for a specified total time."""
        num_steps = int(total_time / self.dt)
        for _ in range(num_steps):
            self.update()
            self.time_series.append(len(self.time_series) * self.dt)
    
    @property
    def death_ratio(self):
        return self.infected_cells / self.native.N
    
    def add_virus(self, data:float):
        if not data: return
        self.virus += data * self.dt
            
    def req_results(self):
        """Returns the simulation results as a dictionary of time series data."""
        return {
            'time': self.time_series,
            'virus': self.virus_values,
            'infected_cells': self.infected_values,
            'immune_cells': self.immune_values,
            'antibodies': self.antibody_values,
            'healthy_cells': self.healthy_values
        }

class MultiList:
    def __init__(self, target=None):
        """
        Initializes the MultiList with a target value.
        
        Parameters:
            target: The target parameter to manage multiple lists.
        """
        self.target = target
        self.lists = {}  # 用于存储多个列表
        self.number = 0

    def _get_list(self):
        """获取当前 target 对应的列表，如果不存在，则创建一个新的列表。"""
        if self.target not in self.lists:
            self.lists[self.target] = [0] * (self.number - 1)
        return self.lists[self.target]
    
    def normalize(self):
        for lst in self.lists.values():
            lst += lst[-1] * (self.number - len(lst))

    def append(self, item):
        """像列表一样添加元素到当前 target 的列表中。"""
        self._get_list().append(item)
        self.number = self.number + 1

    def extend(self, items):
        """像列表一样扩展当前 target 的列表。"""
        self._get_list().extend(items)

    def __getitem__(self, index):
        """获取当前 target 列表的指定索引元素。"""
        if type(index) == int:
            return self._get_list()[index]
        if type(index) == str:
            lst = self._get_list(index)
            return lst[-1] if lst else None

    def __setitem__(self, index, value):
        """设置当前 target 列表的指定索引元素。"""
        self._get_list()[index] = value

    def __len__(self):
        """返回当前 target 列表的长度。"""
        return len(self._get_list())

    def __str__(self):
        """返回当前 target 列表的字符串表示。"""
        return str(self._get_list())

    def get_all_lists(self):
        """返回所有管理的列表。"""
        return self.lists
    
    @property
    def total(self) -> list:
        """返回一个 NumPy 数组，包含所有列表中元素的总和。"""
        # 使用列表生成器将所有列表转换为 NumPy 数组
        total_array = np.sum([np.array(lst) for lst in self.lists.values()], axis=0)
        return list(total_array)


class MultiSimulation:
    def __init__(self, native_immune: ImmuneData, dt: float):
        self.native = native_immune
        self.dt = dt
        self.d = 500

        self.virus_values = MultiList()
        self.antibody_values = MultiList()

        self.infected_virus = []
        
        # Initial values
        self.infected_cells = 0
        self.immune_cells = 0
        self.antibodies = 0
        
        # Lists to store time series data for each variable
        self.infected_values = [0]
        self.antibody_native_values = [0]
        self.immune_values = [0]
        self.healthy_values = [self.native.N]
        self.time_series = [0]
    
    def add_virus(self, virus:Virus):
        if virus.id in self.virus_values.lists:
            self.virus_values.lists[virus.id][-1] += virus.count * self.dt
        else:
            self.virus_values.target = virus.id
            self.antibody_values.target = virus.id
            self.antibody_values.append(0)
            self.virus_values.append(virus.count)
            self.infected_virus.append(virus)
    
    @property
    def total_virus(self) -> float:
        number = 0
        for i in self.virus_values.lists.values():
            number += i[-1]
        return number
    
    def update(self):
        H = min(self.native.N, self.native.N - self.infected_cells)
        for virus in self.infected_virus:
            immune = virus.system
            self.virus_values.target = virus.id
            self.antibody_values.target = virus.id

            virus_number = self.virus_values[-1]
            antibody_number = self.antibody_values[-1]
            # Virus change rate
            dV_dt = immune.s * (1 - self.infected_cells / self.native.N) * virus_number - immune.u * virus_number * H \
                - self.native.g1 * self.antibodies * virus_number * (1 + self.infected_cells / self.native.N) * virus.native \
                - immune.g1 * antibody_number * virus_number * (1 + self.infected_cells / self.native.N)
        
            # Immune cells change rate, with delay in immune response
            delayed_infected = self.infected_values[-self.d] if len(self.infected_values) > self.d else 0
            dM_dt = immune.i * delayed_infected * virus_number - immune.m * self.immune_cells

            # Infected cells change rate

            delayed_immune = self.immune_values[-self.d] if len(self.immune_values) > self.d else 0
            dI_dt = immune.a * max(0, virus_number) - self.native.m * delayed_immune
        
            # Antibodies change rate
            dA_dt_native = self.native.g3 * self.immune_cells - self.native.g2 * self.antibodies
            dA_dt_sys = immune.g3 * self.immune_cells - immune.g2 * antibody_number
        
            # Update current values
            virus_number += dV_dt * self.dt - 1e-4
            antibody_number += dA_dt_sys * self.dt
            self.virus_values.append(max(0, virus_number))
            self.antibody_values.append(antibody_number)

            self.antibodies += dA_dt_native * self.dt
            self.infected_cells += dI_dt * self.dt
            self.immune_cells += dM_dt * self.dt

        #self.antibody_values.normalize()
        #self.virus_values.normalize()
        
        self.infected_cells = min(self.native.N, max(0, self.infected_cells))

        self.infected_values.append(self.infected_cells)
        self.immune_values.append(self.immune_cells)
        self.healthy_values.append(self.native.N - self.infected_cells)
        self.antibody_native_values.append(self.antibodies)
    
    def simulate(self, total_time: float):
        """Runs the simulation for a specified total time."""
        num_steps = int(total_time / self.dt)
        for _ in range(num_steps):
            self.update()
            self.time_series.append(len(self.time_series) * self.dt)
    
    @property
    def death_ratio(self):
        return self.infected_cells / self.native.N
    
    def req_all_virus_history(self) -> list:
        return self.virus_values.total

    def req_virus_history(self, id) -> list:
        return self.virus_values.lists[id]
    
    def req_antibody_history(self, id) -> list:
        return self.antibody_values.lists[id]


# 测试类的功能
if __name__ == "__main__":
    time_duration = 42  # 总时间
    # immune_simulation = ImmuneSimulation(dt=0.01, virus=0.1)  # 创建仿真实例
    immune_simulation = MultiSimulation(native_immune=ImmuneData(), dt=0.01)
    immune_simulation.add_virus(Virus('cod', 0.1, ImmuneData()))
    immune_simulation.add_virus(Virus('cod5', 1.5, ImmuneData(s=2)))
    immune_simulation.simulate(total_time=time_duration)  # 运行仿真

    print(len(immune_simulation.antibody_native_values), len(immune_simulation.req_virus_history('cod5')))

    # 绘制结果
    plt.figure(figsize=(12, 12))

    # 绘制病毒数量
    plt.subplot(3, 2, 1)
    plt.plot(immune_simulation.time_series, immune_simulation.req_all_virus_history(), label='Virus Quantity (V)', color='blue')
    plt.title('Virus Quantity Over Time')
    plt.xlabel('Time')
    plt.ylabel('Virus Quantity (V)')
    plt.grid()
    plt.legend()

    # 绘制感染细胞数量
    plt.subplot(3, 2, 2)
    plt.plot(immune_simulation.time_series, immune_simulation.infected_values, label='Infected Cells (I)', color='green')
    plt.title('Infected Cells Over Time')
    plt.xlabel('Time')
    plt.ylabel('Infected Cells (I)')
    plt.axhline(y=0, color='blue', linestyle='--', label='Initial Infected Cells')
    plt.grid()
    plt.legend()

    # 绘制健康细胞数量
    plt.subplot(3, 2, 3)
    plt.plot(immune_simulation.time_series, immune_simulation.healthy_values, label='Healthy Cells (H)', color='orange')
    plt.title('Healthy Cells Over Time')
    plt.xlabel('Time')
    plt.ylabel('Healthy Cells (H)')
    plt.axhline(y=0, color='blue', linestyle='--', label='Healthy Cells Min')
    plt.grid()
    plt.legend()

    # 绘制免疫细胞数量
    plt.subplot(3, 2, 4)
    plt.plot(immune_simulation.time_series, immune_simulation.immune_values, label='Immune Cells (M)', color='purple')
    plt.title('Immune Cells Over Time')
    plt.xlabel('Time')
    plt.ylabel('Immune Cells (M)')
    plt.grid()
    plt.legend()

    # 绘制抗体数量
    plt.subplot(3, 2, 5)
    plt.plot(immune_simulation.time_series, immune_simulation.antibody_native_values, label='Antibodies (A)', color='cyan')
    plt.title('Antibodies Over Time')
    plt.xlabel('Time')
    plt.ylabel('Antibodies (A)')
    plt.grid()
    plt.legend()

    plt.tight_layout(pad=3.0)  # 增加子图之间的间距
    plt.show()