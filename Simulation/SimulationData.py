import numpy as np


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
		self.paths[path_index][0].append(x_pos)		
		self.paths[path_index][1].append(y_pos)		

	def addPath(self):
		# Creates 2 list for x and y positions
		self.paths.append(([], []))
		self.paths.append(([], []))

	def getPath(self, path_index):
		# Returns single path as tuple		
		return self.paths[path_index]

	def getAll(self):
		return self.paths
