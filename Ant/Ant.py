from enum import Enum
import Simulation.SimulationParameters as SP
import Environment.EnvironmentParameters as EP
import Ant.Util as util
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
	def __init__(self, id, environment=None, home=None):
		self.id = id

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

		self.certainty = 0
		# The ant expects a known landmark after walking some distance. If it does not find any known landmarks,
		# it's certainty drops and it goes back to searching

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

		if self.env.get_nearby_food(self.x_pos, self.y_pos) is not None and not self.food_found:
			self.behav = AntBehaviour.to_nest
			self.food_found = True
			# print("landmarks to", self.landmarks_to_food)
			# print("landmarks from", self.landmarks_to_nest)

		if self.behav is AntBehaviour.to_nest and self.food_found and self.certainty < 0:
			# Executed when the and found food but got lost on the way back
			# print("uncertain! back to search")
			self.behav = AntBehaviour.search

		if self.behav is AntBehaviour.search and self.food_found and not self.__readLandmarks(self.__visible_landmarks + self.__visible_food, False) == (0, 0):
			# Executed when the ant already found food but got lost on its way back and gets back on track
			# print("regained certainty")
			self.behav = AntBehaviour.to_nest

		if self.env.get_nearby_nest(self.x_pos, self.y_pos) is not None and self.food_found:
			self.done = True

	def search(self):
		# Calculate new position&direction as biased random walk
		self.__move(np.random.normal(self.dir, SP.move_angle))

	def toNest(self):
		if len(self.__visible_nests) > 0:
			# If nest in sight, move to nest
			self.__move(util.angle(self.__visible_nests[0].x - self.x_pos, self.__visible_nests[0].y - self.y_pos))
		else:
			# Move in direction indicated by nearby landmarks
			x, y = self.__readLandmarks(self.__visible_landmarks + self.__visible_food, False)
			if x is 0 and y is 0:
				# Move mostly straight if no landmarks in vision
				# self.__move(self.dir)
				self.__move(np.random.normal(self.dir, SP.traceback_angle))
				self.certainty -= SP.move_speed
			else:
				self.__move(util.angle(x, y))
				self.certainty = util.magnitude(x, y)

	def toFood(self):
		if len(self.__visible_food) > 0:
			# If food visible, move to food
			self.__move(util.angle(self.__visible_food[0].x - self.x_pos, self.__visible_food[0].y - self.y_pos))
		else:
			# Move in direction indicated by nearby landmarks
			x, y = self.__readLandmarks(self.__visible_landmarks + self.__visible_nests, True)
			if x is 0 and y is 0:
				# Move mostly straight if no landmarks in vision
				# self.__move(self.dir)
				self.__move(np.random.normal(self.dir, SP.traceback_angle))
			else:
				self.__move(util.angle(x, y))

	def getPosition(self):
		return self.x_pos, self.y_pos

	def __move(self, dir):
		self.dir = dir
		self.x_pos += np.cos(self.dir) * SP.move_speed
		self.y_pos += np.sin(self.dir) * SP.move_speed

		h2 = EP.playround_height/2
		w2 = EP.playround_with/2
		# np.clip would make the simulation ~5x slower
		self.x_pos = util.clip(self.x_pos, -w2, w2)
		self.y_pos = util.clip(self.y_pos, -h2, h2)

	def __writeLandmarks(self, landmarks):
		# Reads landmark directions from ant memory and sums them up
		for landmark in landmarks:
			if landmark is not self.cur_landmark:
				self.landmarks_to_food[self.cur_landmark.id] = (landmark.x - self.cur_landmark.x, landmark.y - self.cur_landmark.y)
				if landmark.id not in self.landmarks_to_nest:
					self.landmarks_to_nest[landmark.id] = (self.cur_landmark.x - landmark.x, self.cur_landmark.y - landmark.y)
				self.cur_landmark = landmark

	def __readLandmarks(self, landmarks, to_food=True):
		# Writes landmarks into memory of ant
		tot_x, tot_y = 0, 0
		for landmark in landmarks:
			l = (self.landmarks_to_food if to_food else self.landmarks_to_nest)
			if landmark.id not in l: continue
			x, y = l[landmark.id]
			tot_x += x
			tot_y += y
		return tot_x, tot_y
