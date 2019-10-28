from enum import Enum
import Simulation.SimulationParameters as SP
import Environment.EnvironmentParameters as EP
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
	def __init__(self, environment=None):
		self.x_pos = 0  # Assume that the nest is at location (0,0)
		self.y_pos = 0
		self.dir = np.random.random_sample() * np.pi * 2  # Random starting rotation between 0 and 2Pi
		self.behav = AntBehaviour.search

		self.env = environment
		self.food_found = False

	def step(self):
		# Does a single simulation step for this ant
		if self.behav is AntBehaviour.search:
			self.search()
		elif self.behav is AntBehaviour.to_nest:
			self.toNest()
		elif self.behav is AntBehaviour.to_food:
			self.toFood()

		if self.env is not None and self.env.is_near_food(self.x_pos, self.y_pos):
			self.food_found = True

		# TODO: Implement behaviour transitions

	def search(self):
		# TODO: Implement Simulation boundaries
		# Calculate new position&direction as biased random walk
		self.dir = np.random.normal(self.dir, SP.move_angle)
		self.x_pos += np.cos(self.dir) * SP.move_speed
		self.y_pos += np.sin(self.dir) * SP.move_speed

		h2 = EP.playround_height/2
		w2 = EP.playround_with/2
		# np.clip would make the simulation ~5x slower
		self.x_pos = Ant.__clip(self.x_pos, -w2, w2)
		self.y_pos = Ant.__clip(self.y_pos, -h2, h2)

	def toNest(self):
		# TODO: Implement return-to-nest behaviour
		pass

	def toFood(self):
		# TODO: Implement go-to-food behaviour
		pass

	def getPosition(self):
		return self.x_pos, self.y_pos

	@staticmethod
	def __clip(val, min_val, max_val):
		if min_val < val < max_val:
			return val
		elif val < min_val:
			return min_val
		else:
			return max_val
