import numpy as np
from Simulation.Simulation import Simulation
from Simulation.SimulationData import SimulationResults
import Simulation.SimulationParameters as SimulationParameters
from Environment.Environment import Environment

from multiprocessing import Pool

NUM_CORES = 4

def run(index):
    SimulationParameters.ant_count = 2
    SimulationParameters.move_speed = 1
    SimulationParameters.move_angle = 15 / 180 * np.pi
    SimulationParameters.traceback_angle = 5 / 180 * np.pi
    SimulationParameters.vision_range = 15

    e = Environment().generate_random_environment()
    s = Simulation(e)

    return s.simulateAll()

def run_simulations(num_simulations = 10):    
    pool = Pool(NUM_CORES)
        
    results = pool.map(run, range(num_simulations))

    return results

def measure_steps():
    results = run_simulations(10)

    allResults = SimulationResults()

    allResults.foundFood = [x for result in results for x in result.foundFood]
    allResults.foundBack = [x for result in results for x in result.foundBack]
    allResults.stepsToFood = [x for result in results for x in result.stepsToFood]
    allResults.stepsToNest = [x for result in results for x in result.stepsToNest]

    return allResults    

if __name__  == '__main__':
    results = measure_steps()

    num_ants = len(results.foundFood)
    percentage_food_found = sum(results.foundFood) / num_ants
    percentage_nest_found = sum(results.foundBack) / num_ants

    avg_steps_to_food = sum(results.stepsToFood) / num_ants
    avg_steps_to_nest = sum(results.stepsToNest) / num_ants

    print(num_ants, 'ants simulated.')

    print('Percentage of ants that found food:', percentage_food_found)
    print('Percentage of ants that found back:', percentage_nest_found)

    print('Average steps:', avg_steps_to_food + avg_steps_to_nest)
    print('Average steps to food:', avg_steps_to_food)
    print('Average steps to nest:', avg_steps_to_nest)
