import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def calculate_diffusion_coefficient(T, D0, Q, R):
    """diffusion coefficient for a given temperature"""
    return D0 * np.exp(-Q/(R*T))

def calculate_diffusion_flux(C, D, dx):
    """diffusion flux for a given concentration gradient"""
    flx = D * np.gradient(C,dx)
    return -1 * flx

def calculate_oxidation_rate(T, D0, Q, R, C, r, M):
    """oxidation rate for a given cell"""
    D = calculate_diffusion_coefficient(T, D0, Q, R)
    dx = 2 * r / 100
    J = calculate_diffusion_flux(C, D, dx)
    return int(1.33 * np.pi * r**3 * N_A * M) * J

# size of the grid and the initial state of each cell
grid_size = (100, 100)
grid = np.full(grid_size, "metallic")

# simulation parameters
temperature = 1000 # Celsius
time_step = 1 # seconds
duration = 3600 # seconds

# constants
k_B = 1.38e-23   # Boltzmann constant
N_A = 6.02e23    # Avogadro's number
M = 63.55       # molar mass of copper
r = 1e-7        # radius of cell (m)
T = 1000        # temperature (C)
D0 = 1e-4       # pre-exponential factor (m^2/s)
Q = 80e3        # activation energy for diffusion (J/mol)
R = 8.31        # gas constant (J/mol*K)
dt = 1          # time step (s)
duration = 3600 # duration of simulation (s)

# state mapping
state_map = {
    "metallic": 0,
    "oxide": 1,
    "void": 2
}

# simulate oxidation over time
for t in range(0, duration, time_step):
    # oxidation rate for each cell in the grid
    oxidation_rates = np.zeros(grid_size)
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            C = 1  # concentration of oxidizing species(arbitrary value)
            oxidation_rates[i][j] = calculate_oxidation_rate(T, D0, Q, R, C, r, M)

    # update cell states based on calculated oxidation rate
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if grid[i][j] == "metallic":
                # transition to oxide state based on oxidation rate
                if np.random.random() < oxidation_rates[i][j]:
                    grid[i][j] = "oxide"
            elif grid[i][j] == "oxide":
                # adjust oxide thickness based on oxidation rate
                thickness = 1 + oxidation_rates[i][j]
                if np.random.random() < 0.5:
                    thickness *= -1
                new_thickness = max(0, min(thickness, 5))
                if new_thickness == 0:
                    grid[i][j] = "void"
                else:
                    grid[i][j] = "oxide" * new_thickness

    # convert grid to numerical array
    grid_num = np.zeros(grid_size)
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            grid_num[i][j]


    # visualize the results
    if t % 3600 == 0:
        plt.imshow(grid_num, cmap="gray")
        plt.title(f"Time: {t // 3600} hours")
        plt.show()

