from enum import Enum


class LandmarkTypes(Enum):
    LANDMARK = 0
    FOOD = 1
    NEST = 2


class Landmark():
    """
	* Describes a landmark with its x and y coordinates.
    * Each Landmark has a unique ID.
	"""	

    last_id = 0

    def __init__(self, x, y):
        self.id = Landmark.last_id
        Landmark.last_id += 1

        self.x = x
        self.y = y

    def get_id(self):
        return self.id

    def get_coordinates(self):
        return self.x, self.y

    def get_type(self):
        return LandmarkTypes.LANDMARK

    @property
    def id(self):
        return self.id

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y


class FOOD(Landmark):
    def __init__(self, x, y):
        Landmark.__init__(self, x, y)

    def get_type(self):
        return LandmarkTypes.FOOD


class NEST(Landmark):
    def __init__(self, x, y):
        Landmark.__init__(self, x, y)

    def get_type(self):
        return LandmarkTypes.NEST
