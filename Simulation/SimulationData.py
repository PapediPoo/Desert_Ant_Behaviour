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

	def addPath(self, color="r"):
		# Creates 2 list for x, y positions.
		# Color property used for debugging
		self.paths.append(([], [], color))
		self.foundFood.append(False)
		self.foundBack.append(False)
		self.stepsToFood.append(0)
		self.stepsToNest.append(0)

	def addPoint(self, path_index, x_pos, y_pos):
		# Adds a new point to the specified path		
		self.paths[path_index][0].append(x_pos)		
		self.paths[path_index][1].append(y_pos)	

	def foodFound(self, path_index):
		if not self.foundFood[path_index]:
			self.foundFood[path_index] = True
			self.stepsToFood[path_index] = len(self.paths[path_index][0])		

	def nestFound(self, path_index):
		self.foundBack[path_index] = True
		self.stepsToNest[path_index] = len(self.paths[path_index][0]) - self.stepsToFood[path_index]		

	def getPath(self, path_index):
		# Returns single path as tuple		
		return self.paths[path_index]

	def getAll(self):
		return self.paths
