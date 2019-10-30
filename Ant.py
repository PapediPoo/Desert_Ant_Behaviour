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
	search_food = 3
	search_nest = 4


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
		self.x_pos = home.x  # Assume that the nest is at location (0,0)
		self.y_pos = home.y
		self.dir = np.random.random_sample() * np.pi * 2  # Random starting rotation between 0 and 2Pi
		self.behav = AntBehaviour.search

		self.next_x = 0
		self.next_y = 0

		self.env = environment
		self.food_found = False
		self.to_food = True
		self.has_path = True
		self.done = False

		self.landmarks = {}
		self.home = home
		self.cur_landmark = home

	def simulate(self):
		while self.food_found is False:
			self.step()

	def step(self):
		# Does a single simulation step for this ant
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

		'''if self.env is not None and self.env.is_near_food(self.x_pos, self.y_pos):
			self.food_found = True'''

		nests = self.env.get_visible_nests(self.x_pos, self.y_pos)
		food = self.env.get_visible_food(self.x_pos, self.y_pos)
		landmarks = self.env.get_visible_landmarks(self.x_pos, self.y_pos)
		if self.food_found is False:
			self.__writeLandmarks(landmarks)
			if len(list(food)) > 0:
				print("food found")
				self.food_found = True
				self.__writeLandmarks(list(food))
				self.behav = AntBehaviour.to_food

		if self.env.get_nearby_food(self.x_pos, self.y_pos) is not None:
			self.done = True
		# TODO: Implement behaviour transitions

	def search(self):
		# Calculate new position&direction as biased random walk
		self.__move(np.random.normal(self.dir, SP.move_angle))

		h2 = EP.playround_height/2
		w2 = EP.playround_with/2
		# np.clip would make the simulation ~5x slower
		self.x_pos = Ant.__clip(self.x_pos, -w2, w2)
		self.y_pos = Ant.__clip(self.y_pos, -h2, h2)

	def toNest(self):
		# TODO: Implement return-to-nest behaviour
		pass

	def toFood(self):
		# TODO: Reuse landmark filter from transition code
		food = list(self.env.get_visible_food(self.x_pos, self.y_pos))
		if len(food) > 0:
			self.__move(self.getAngle(food[0].x, food[0].y))
		else:
			landmarks = self.env.get_visible_landmarks(self.x_pos, self.y_pos)
			new_dir, new_dist = self.__readLandmarks(landmarks)
			self.__move(new_dir)

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

	def __move(self, dir):
		self.dir = dir
		self.x_pos += np.cos(self.dir) * SP.move_speed
		self.y_pos += np.sin(self.dir) * SP.move_speed

		self.next_x += np.cos(self.dir) * SP.move_speed
		self.next_y += np.sin(self.dir) * SP.move_speed

	def __writeLandmarks(self, landmarks):
		for landmark in landmarks:
			if landmark is not self.cur_landmark:
				self.landmarks[self.cur_landmark.id] = (self.next_x, self.next_y)
				self.next_x = 0
				self.next_y = 0
				self.cur_landmark = landmark

	def __readLandmarks(self, landmarks):
		tot_x, tot_y = 0, 0
		for landmark in landmarks:
			if not landmark.id in self.landmarks:
				continue
			x, y = self.landmarks[landmark.id]
			tot_x += x
			tot_y += y
		return tot_x, tot_y
