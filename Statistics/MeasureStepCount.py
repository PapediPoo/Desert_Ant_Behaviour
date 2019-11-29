import numpy as np
from Simulation.Simulation import Simulation
from Simulation.SimulationData import SimulationResults
import Simulation.SimulationParameters as SimulationParameters
import Environment.EnvironmentParameters as EnvironmentParameters
from Environment.Environment import Environment
import matplotlib.pyplot as plt

from multiprocessing import Pool

NUM_CORES = 4


def run(index):
    EnvironmentParameters.playround_with = 600
    EnvironmentParameters.playround_height = 600
    EnvironmentParameters.food_count = 1
    EnvironmentParameters.landmark_count = 0

    SimulationParameters.ant_count = 25
    SimulationParameters.move_speed = 1
    SimulationParameters.move_angle = 15 / 180 * np.pi
    SimulationParameters.traceback_angle = index / 180 * np.pi
    SimulationParameters.vision_range = 25

    e = Environment().generate_environment(
        [],
        [(250, 0)],
        [(100, 0), (-100, 0), (0, 100), (0, -100), (200, 200), (200, -200), (-200, -200), (-200, 200)])
    s = Simulation(e)

    return s.simulateAll()


def run_simulations(index, num_simulations=10):
    pool = Pool(NUM_CORES)
        
    results = pool.map(run, [index] * num_simulations)

    return results


def measure_steps(index):
    results = run_simulations(index, 4)

    allResults = SimulationResults()

    allResults.foundFood = [x for result in results for x in result.foundFood]
    allResults.foundBack = [x for result in results for x in result.foundBack]
    allResults.stepsToFood = [x for result in results for x in result.stepsToFood]
    allResults.stepsToNest = [x for result in results for x in result.stepsToNest]

    return allResults


if __name__ == '__main__':
    x_axis = []
    y_axis1 = []
    y_axis2 = []
    y_axis3 = []
    y_axis4 = []

    for i in range(0, 35, 1):
        results = measure_steps(i)

        num_ants = len(results.foundFood)
        percentage_food_found = sum(results.foundFood) / num_ants * 100
        percentage_nest_found = sum(results.foundBack) / num_ants * 100

        avg_steps_to_food = sum(results.stepsToFood) / num_ants
        avg_steps_to_nest = sum(results.stepsToNest) / num_ants

        # print(list(zip(results.foundFood, results.stepsToFood)))
        # print(list(zip(results.foundBack, results.stepsToNest)))

        print(num_ants, 'ants simulated.')

        print('Percentage of ants that found food:', percentage_food_found)
        print('Percentage of ants that found back:', percentage_nest_found)

        print('Average steps:', avg_steps_to_food + avg_steps_to_nest)
        print('Average steps to food:', avg_steps_to_food)
        print('Average steps to nest:', avg_steps_to_nest)

        x_axis.append(i)
        y_axis1.append(avg_steps_to_food)
        y_axis2.append(avg_steps_to_nest)

        y_axis3.append(percentage_food_found)
        y_axis4.append(percentage_nest_found)

    line1, = plt.plot(x_axis, y_axis1, label="steps to food")
    line2, = plt.plot(x_axis, y_axis2, label="steps to nest")
    plt.xlabel("average traceback angle error")
    plt.ylabel("average steps")
    plt.legend(handles=[line1, line2], loc="upper right")
    plt.figure()

    line3, = plt.plot(x_axis, y_axis3, label="avg food found")
    line4, = plt.plot(x_axis, y_axis4, label="avg nest found")
    plt.xlabel("average traceback angle error")
    plt.ylabel("average ants found back [%]")
    plt.legend(handles=[line3, line4], loc="upper right")
    plt.show()
