from enum import Enum
import Simulation.SimulationParameters as PM
import numpy as np


class AntBehaviour(Enum):
	'''
	* Enum of possible ant behaviours
	'''
	search = 0
	to_nest = 1
	to_food = 2


class Ant:
	'''
	* Describes a single Ant (State&Behaviour).
	* An ant can either be searching, going back to the nest, or be on its way to the food (if its found)
	* Initially the ant will be randomly searching the food. Once food is found, it remembers which landmarks
	* it has seen in the past and how to get from each previous landmark to the next. That way the and will be
	* able to trace back the path it has taken from its nest to the food. This means that the ant associates
	* a single directional vector with each landmark which denotes the relative position of the next landmark
	* on the path from the nest to the food. If it sees multiple landmarks, it will take the sum of the
	* directional vectors.
	'''
	def __init__(self):
		self.x_pos = 0  # Assume that the nest is at location (0,0)
		self.y_pos = 0
		self.dir = np.random.random_sample() * np.pi * 2  # Random starting rotation between 0 and 2Pi
		self.behav = AntBehaviour.search
		self.food_found = False

	def step(self):
		# Does a single simulation step for this ant
		if self.behav is AntBehaviour.search:
			self.search()
		elif self.behav is AntBehaviour.to_nest:
			self.toNest()
		elif self.behav is AntBehaviour.to_food:
			self.toFood()

		# TODO: Implement behaviour transitions

	def search(self):
		# TODO: Implement Simulation boundaries
		# Calculate new position&direction as biased random walk
		self.dir = np.random.normal(self.dir, PM.move_angle)
		self.x_pos += np.cos(self.dir) * PM.move_speed
		self.y_pos += np.sin(self.dir) * PM.move_speed

	def toNest(self):
		# TODO: Implement return-to-nest behaviour
		pass

	def toFood(self):
		# TODO: Implement go-to-food behaviour
		pass

	def getPosition(self):
		return self.x_pos, self.y_pos
