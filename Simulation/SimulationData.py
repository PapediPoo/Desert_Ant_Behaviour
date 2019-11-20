import numpy as np


class SimulationResults:
	'''
	* Holds information about the paths created by the ant simulation
	* the field "self.paths" has n entries if n denotes #Ants.
	* Each Ant has two dedicated lists in "self.paths" which denote
	* Points on the x and the y axis.
	'''
	def __init__(self):
		self.paths = []

		self.foundFood = []
		self.foundBack = []
		self.stepsToFood = []
		self.stepsToNest = []

	def addPoint(self, path_index, x_pos, y_pos):
		# Adds a new point to the specified path		
		self.paths[path_index][0].append(x_pos)		
		self.paths[path_index][1].append(y_pos)		

	def addPath(self, color="r"):
		# Creates 2 list for x, y positions.
		# Color property used for debugging
		self.paths.append(([], [], color))
		self.foundFood.append(False)
		self.stepsToFood.append(0)
		self.stepsToNest.append(0)

	def getPath(self, path_index):
		# Returns single path as tuple		
		return self.paths[path_index]

	def getAll(self):
		return self.paths
