import tkinter
import matplotlib.pyplot as plt
import Environment.EnvironmentParameters as EP
import Simulation.SimulationParameters as SP
from Environment.Environment import Environment
from Environment.Landmarks import Landmark

border_color = "gray"
path_color = "tomato"
nest_color = "green"
food_color = "blue"
landmark_color = "orange"
vision_color = "turquoise"

'''
* Draws Environment boundaries, landmarks, nests and food on a given canvas
'''
def drawEnvironment(canvas, environment, draw=False):
    h2 = EP.playround_height / 2
    w2 = EP.playround_with / 2
    plt.plot([-w2, w2, w2, -w2, -w2], [-h2, -h2, h2, h2, -h2], border_color)
    for nest in environment.nests:
        plt.scatter(nest.x, nest.y, c=nest_color)
    for food in environment.food:
        plt.scatter(food.x, food.y, c=food_color)
    for landmark in environment.landmarks:
        plt.scatter(landmark.x, landmark.y, c=landmark_color)
        # plt.annotate(landmark.id, (landmark.x, landmark.y))
    canvas.figure = plt.gcf()
    if draw:
        canvas.draw()

'''
* Draws ant paths on a given canvas
'''
def drawPaths(canvas, paths, draw=False):
    for path in paths:
        plt.plot(path[0], path[1], path_color)
    canvas.figure = plt.gcf()
    if draw:
        canvas.draw()
