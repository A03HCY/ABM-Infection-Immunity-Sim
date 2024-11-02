import matplotlib.pyplot as plt

class ImmuneSimulation:
    def __init__(self, N: float = 100, virus:float = 0, s: float = 0.8, a: float = 0.5, u: float = 0.001, 
                 i: float = 0.1, g1: float = 0.1, g2: float = 0.01, m: float = 0.02, 
                 d: float = 500, dt: float = 0.01):
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
            m (float): Immune cell natural death coefficient.
            d (float): Immune cell response delay in time steps.
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
        self.m = m
        self.d = d
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
        
    def update(self):
        """Updates the values of virus, infected cells, immune cells, and antibodies."""
        # Calculate healthy cells
        H = self.N - self.infected_cells
        
        # Virus change rate
        dV_dt = self.s * (1 - self.infected_cells / self.N) * self.virus - self.u * self.virus * H \
                - self.g1 * self.antibodies * self.virus * (1 + self.infected_cells / self.N)
        
        # Infected cells change rate
        dI_dt = self.a * dV_dt
        
        # Immune cells change rate, with delay in immune response
        delayed_infected = self.infected_values[-self.d] if len(self.infected_values) > self.d else 0
        dM_dt = self.i * delayed_infected * self.virus - self.m * self.immune_cells
        
        # Antibodies change rate
        dA_dt = self.immune_cells - self.g2 * self.antibodies
        
        # Update current values
        self.virus += dV_dt * self.dt
        self.infected_cells += dI_dt * self.dt
        self.immune_cells += dM_dt * self.dt
        self.antibodies += dA_dt * self.dt
        
        # Store results
        self.virus_values.append(self.virus)
        self.infected_values.append(self.infected_cells)
        self.immune_values.append(self.immune_cells)
        self.antibody_values.append(self.antibodies)
        self.healthy_values.append(H)
        
    def simulate(self, total_time: float):
        """Runs the simulation for a specified total time."""
        num_steps = int(total_time / self.dt)
        for _ in range(num_steps):
            self.update()
            self.time_series.append(len(self.time_series) * self.dt)
    
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

# 测试类的功能
if __name__ == "__main__":
    time_duration = 14  # 总时间
    immune_simulation = ImmuneSimulation(dt=0.01, virus=0.1)  # 创建仿真实例
    immune_simulation.simulate(total_time=time_duration)  # 运行仿真

    # 绘制结果
    plt.figure(figsize=(12, 12))

    # 绘制病毒数量
    plt.subplot(3, 2, 1)
    plt.plot(immune_simulation.time_series, immune_simulation.virus_values, label='Virus Quantity (V)', color='blue')
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
    plt.plot(immune_simulation.time_series, immune_simulation.antibody_values, label='Antibodies (A)', color='cyan')
    plt.title('Antibodies Over Time')
    plt.xlabel('Time')
    plt.ylabel('Antibodies (A)')
    plt.grid()
    plt.legend()

    plt.tight_layout(pad=3.0)  # 增加子图之间的间距
    plt.show()