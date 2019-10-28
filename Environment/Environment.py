from Environment import EnvironmentParameters as EP
from random import randint, random


class Environment:
	"""
	* Describes an environment containing landmarks and food on different places.
	* The nest is assumed to be a landmark.
	* The visual range describes the distance to landmarks which are seen, the
	* action range the minimal distance of the food to eat it and to the nest to
	* enter it.
	* Food only gets noticed in the action range, whereas landmarks and the nest
	* get noticed in the visual range. Is this the expected behaviour?
	"""	

	# TODO: Now, landmarks and the nest get treated in the same way, but food is not. Maybe create classes for them anyway? (What about the algorithm?)
	__id = 0

	def __init__(self):
		self.id = Environment.__id
		Environment.__id += 1

		self.nest_x = 0
		self.nest_y = 0

		self.landmarks = [(self.nest_x, self.nest_y)]
		self.food = []
		
	def generate_random_environment(self):
		# Generate landmarks
		self.landmarks = [(self.nest_x, self.nest_y)]
		num_landmarks = randint(1, EP.max_landmark_count)
		
		for i in range(num_landmarks):
			x = random() * EP.playround_with - EP.playround_with / 2
			y = random() * EP.playround_height - EP.playround_height / 2

			self.landmarks.append(x, y)

		# Generate food
		self.food = []
		num_food = randint(1, EP.max_food_count)
		
		for i in range(num_food):
			x = random() * EP.playround_with - EP.playround_with / 2
			y = random() * EP.playround_height - EP.playround_height / 2

			self.food.append((x, y))

	def get_visible_landmarks(self, x, y):
		is_visible = lambda x_l, y_l: self.get_distance(x_l, y_l, x, y) < EP.visual_range
		
		nearby_landmarks = filter(is_visible, self.landmarks)

		# TODO: Maybe return nearby landmarks sorted by its distance to the ant?

		return nearby_landmarks

	def is_near_food(self, x, y):
		is_visible = lambda x_f, y_f: self.get_distance(x_f, y_f, x, y) < EP.action_range

		return any([is_visible(x_f, y_f) for x_f, y_f in self.food])

	def is_near_nest(self, x, y):
		distance_to_nest = self.get_distance(self.nest_x, self.nest_y, x, y)
		return distance_to_nest < EP.action_range

	def get_distance(self, x1, y1, x2, y2):
		return (x1 - x2) ** 2 + (y1 - y2) ** 2
