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
	def __init__(self, environment=None, home=None):
		self.x_pos = home.x
		self.y_pos = home.y
		self.dir = np.random.random_sample() * np.pi * 2  # Random starting rotation between 0 and 2Pi
		self.behav = AntBehaviour.search

		self.env = environment
		self.food_found = False
		self.done = False

		self.landmarks_to_food = {}
		self.landmarks_to_nest = {}
		self.home = home
		self.cur_landmark = home

		self.__visible_landmarks = []
		self.__visible_food = []
		self.__visible_nests = []

	def step(self):
		# Get all relevant information in vision
		self.__visible_nests = list(self.env.get_visible_nests(self.x_pos, self.y_pos))
		self.__visible_food = list(self.env.get_visible_food(self.x_pos, self.y_pos))
		self.__visible_landmarks = list(self.env.get_visible_landmarks(self.x_pos, self.y_pos))

		# Do a single simulation step
		if self.behav is AntBehaviour.search:
			self.search()
		elif self.behav is AntBehaviour.to_nest:
			self.toNest()
		elif self.behav is AntBehaviour.to_food:
			self.toFood()
		elif self.behav is AntBehaviour.search_food:
			self.search()
		elif self.behav is AntBehaviour.search_nest:
			self.search()

		# Do state transitions
		if self.food_found is False:
			self.__writeLandmarks(self.__visible_landmarks)
			if len(self.__visible_food) > 0:
				self.__writeLandmarks(self.__visible_food)
				self.behav = AntBehaviour.to_food

		if self.env.get_nearby_food(self.x_pos, self.y_pos) is not None:
			self.behav = AntBehaviour.to_nest
			self.food_found = True
			print("landmarks to", self.landmarks_to_food)
			print("landmarks from", self.landmarks_to_nest)

		if self.env.get_nearby_nest(self.x_pos, self.y_pos) is not None and self.food_found:
			self.done = True
		# TODO: Implement behaviour transitions

	def search(self):
		# Calculate new position&direction as biased random walk
		self.__move(np.random.normal(self.dir, SP.move_angle))

	def toNest(self):
		if len(self.__visible_nests) > 0:
			# If nest in sight, move to nest
			self.__move(self.getAngle(self.__visible_nests[0].x, self.__visible_nests[0].y))
		else:
			# Move in direction indicated by nearby landmarks
			x, y = self.__readLandmarks(self.__visible_landmarks + self.__visible_food, False)
			if x is 0 and y is 0:
				self.__move(self.dir)
			else:
				self.__move(self.getAngle(x+self.x_pos, y+self.y_pos))

	def toFood(self):
		if len(self.__visible_food) > 0:
			self.__move(self.getAngle(self.__visible_food[0].x, self.__visible_food[0].y))
		else:
			x, y = self.__readLandmarks(self.__visible_landmarks + self.__visible_nests, True)
			if x is 0 and y is 0:
				self.__move(self.dir)
			else:
				self.__move(self.getAngle(x, y))

	def getPosition(self):
		return self.x_pos, self.y_pos

	def getAngle(self, x, y):
		return np.arctan2(y-self.y_pos, x-self.x_pos)

	@staticmethod
	def __clip(val, min_val, max_val):
		if min_val < val < max_val:
			return val
		elif val < min_val:
			return min_val
		else:
			return max_val

	@staticmethod
	def __magnitude(x, y):
		return ((x **2) + (y **2)) **(1/2)

	def __move(self, dir):
		self.dir = dir
		self.x_pos += np.cos(self.dir) * SP.move_speed
		self.y_pos += np.sin(self.dir) * SP.move_speed

		h2 = EP.playround_height/2
		w2 = EP.playround_with/2
		# np.clip would make the simulation ~5x slower
		self.x_pos = Ant.__clip(self.x_pos, -w2, w2)
		self.y_pos = Ant.__clip(self.y_pos, -h2, h2)

	def __writeLandmarks(self, landmarks):
		for landmark in landmarks:
			if landmark is not self.cur_landmark:
				self.landmarks_to_food[self.cur_landmark.id] = (landmark.x - self.cur_landmark.x, landmark.y - self.cur_landmark.y)
				if landmark.id not in self.landmarks_to_nest:
					self.landmarks_to_nest[landmark.id] = (self.cur_landmark.x - landmark.x, self.cur_landmark.y - landmark.y)
				self.cur_landmark = landmark

	def __readLandmarks(self, landmarks, to_food=True):
		tot_x, tot_y = 0, 0
		for landmark in landmarks:
			l = (self.landmarks_to_food if to_food else self.landmarks_to_nest)
			if landmark.id not in l: continue
			x, y = l[landmark.id]
			tot_x += x
			tot_y += y
		return tot_x, tot_y
