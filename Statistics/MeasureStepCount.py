import numpy as np
from Simulation.Simulation import Simulation
import Simulation.SimulationParameters as SimulationParameters
from Environment.Environment import Environment

from multiprocessing import Pool

NUM_CORES = 4

def run(index):
    e = Environment().generate_random_environment()
    s = Simulation(e)

    return s.simulateAll()

def run_simulations(num_simulations = 10):    
    pool = Pool(NUM_CORES)
        
    results = pool.map(run, range(num_simulations))

    return results

def measure_steps():
    SimulationParameters.ant_count = 2
    SimulationParameters.move_speed = 1
    SimulationParameters.move_angle = 15 / 180 * np.pi
    SimulationParameters.traceback_angle = 5 / 180 * np.pi
    SimulationParameters.vision_range = 50

    results = run_simulations(10)
    print(results)

if __name__  == '__main__':
    measure_steps()
