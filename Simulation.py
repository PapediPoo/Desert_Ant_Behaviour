import Ant
import numpy as np


class Simulation:
	'''
	* Holds all information about simulation, runs simulation and returns results.
	'''
	def __init__(self, ant_count, environment):
		self.ants = []
		self.setAntCount(ant_count)
		self.environment = environment

		# TODO: Replace with success condition
		self.steps = 100

	def simulate(self):
		# TODO: should the SimulationResults object be reused?
		result = SimulationResults()
		for i, ant in enumerate(self.ants):
			result.addPath()
			result.addPoint(i, *ant.getPosition())

		# TODO: Replace with success condition
		for step in range(0, self.steps):
			for i, ant in enumerate(self.ants):
				ant.step()
				result.addPoint(i, *ant.getPosition())

		return result

	def setAntCount(self, ant_count):
		self.ants = [Ant.Ant() for i in range(0, ant_count)]

	def setSteps(self, steps):
		# TODO: Replace with success condition
		self.steps = steps


class SimulationParameters:
	'''
	* This class describes the parameters for the simulation.
	* It will be read by the Simulation class and read+written by the GUI.
	'''
	def __init__(self):
		pass

	# TODO: Use static fields (?)
	move_speed = 1
	turn_dev = np.pi/8
	vision_radius = 20

	dist_error = 0.1
	angle_error = 0.1

	ant_count = 5


class SimulationResults:
	'''
	* Holds information about the paths created by the ant simulation
	* the field "self.paths" has 2*n entries if n denotes #Ants.
	* Each Ant has two dedicated lists in "self.paths" which denote
	* Points on the x and the y axis.
	'''
	def __init__(self):
		self.paths = []

	def addPoint(self, path_index, x_pos, y_pos):
		# Adds a new point to the specified path
		real_index = path_index * 2
		self.paths[real_index].append(x_pos)
		self.paths[real_index+1].append(y_pos)

	def addPath(self):
		# Creates 2 list for x and y positions
		self.paths.append([])
		self.paths.append([])

	def getPath(self, path_index):
		# Returns single path as tuple
		real_index = path_index * 2
		return self.paths[real_index], self.paths[real_index+1]

	def getAll(self):
		return self.paths
