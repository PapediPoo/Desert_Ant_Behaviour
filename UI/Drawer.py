import tkinter
import matplotlib.pyplot as plt
import Environment.EnvironmentParameters as EP
from Environment.Environment import Environment

border_color = "gray"
path_color = "tomato"
nest_color = "green"
food_color = "blue"
landmark_color = "orange"


def drawEnvironment(canvas, environment, draw=False):
	h2 = EP.playround_height/2
	w2 = EP.playround_with/2
	plt.plot([-w2, w2, w2, -w2, -w2], [-h2, -h2, h2, h2, -h2], border_color)
	canvas.figure = plt.gcf()
	if draw:
		canvas.draw()


def drawPaths(canvas, paths, draw=False):
	for path in paths:
		plt.plot(path[0], path[1], path_color)
	canvas.figure = plt.gcf()
	if draw:
		canvas.draw()
