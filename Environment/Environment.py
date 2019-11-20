from Environment import EnvironmentParameters as EP
from Simulation import SimulationParameters as SP
from Environment.Landmarks import Landmark, FOOD, NEST
from random import randint, random


class Environment:
	"""
	Describes an environment containing landmarks and food on different places.
	The nest is assumed to be a landmark.
	The visual range describes the distance to landmarks which are seen, the
	action range the minimal distance of the food to eat it and to the nest to
	enter it.
	"""

	def __init__(self):
		self.landmarks = []
		self.food = []
		self.nests = []

	def generate_random_environment(self):
		"""
		Generates a random environment (i.e. landmarks, food and nests) according
		to the parameters in EnvironmentParamters.py.
		The first nest is placed at (0,0), all other points are placed randomly.
		"""

		# Generate the first nest at (0,0), the remaining at random points.
		self.nests = []
		self.nests.append(NEST(0, 0))

		for i in range(EP.nest_count - 1):
			x, y = self.get_random_coordinates()
			nest = NEST(x, y)
			self.nests.append(nest)

		# Generate landmarks
		self.landmarks = []
		num_landmarks = EP.landmark_count

		for i in range(num_landmarks):
			x, y = self.get_random_coordinates()
			landmark = Landmark(x, y)
			self.landmarks.append(landmark)

		# Generate food
		self.food = []
		num_food = EP.food_count

		for i in range(num_food):
			x, y = self.get_random_coordinates()
			food = FOOD(x, y)
			self.food.append(food)

		return self

	def get_random_coordinates(self):
		x = random() * EP.playround_with - EP.playround_with / 2
		y = random() * EP.playround_height - EP.playround_height / 2

		return x, y

	def get_visible_nests(self, x, y):
		""" Returns a list of nests within visual range."""

		return self.get_visible_POIs(x, y, self.nests)

	def get_visible_landmarks(self, x, y):
		""" Returns a list of landmarks within visual range."""

		return self.get_visible_POIs(x, y, self.landmarks)

	def get_visible_food(self, x, y):
		""" Returns a list of food within visual range."""

		return self.get_visible_POIs(x, y, self.food)

	def get_nearby_nest(self, x, y):
		""" Returns a Nest-Object if it is within action_range or None otherwise."""

		return self.get_nearby_POI(x, y, self.nests)

	def get_nearby_food(self, x, y):
		""" Returns a Food-Object if it is within action_range or None otherwise."""

		return self.get_nearby_POI(x, y, self.food)

	def get_visible_POIs(self, x, y, POIs):
		"""
		Returns a list of Points of Interest (objects of type Landmark or one of its subclasses)
		within visual range.
		POIs has to be a list of Points of Interest.
		"""

		is_visible = lambda _poi: self.get_distance((x, y), _poi.get_coordinates()) < SP.vision_range

		return filter(is_visible, POIs)

	def get_nearby_POI(self, x, y, POIs):
		"""
		Returns a Points of Interest (objects of type Landmark or one of its subclasses)
		within action range. If none is in action range, returns None.
		"""

		is_visible = lambda _poi: self.get_distance((x, y), _poi.get_coordinates()) < EP.action_range

		nearby_POIs = list(filter(is_visible, POIs))

		if len(nearby_POIs) == 0:
			return None
		else:
			return nearby_POIs[0]

	def get_distance(self, p1, p2):
		"""
		Returns the distance between p1 and p2.
		p1 and p2 have to be tuples of (x, y).
		"""

		x1, y1 = p1
		x2, y2 = p2
		return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)
