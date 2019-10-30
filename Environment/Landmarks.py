from enum import Enum


class LandmarkTypes(Enum):
    LANDMARK = 0
    FOOD = 1
    NEST = 2


class Landmark:
    """
    * Describes a landmark with its x and y coordinates.
    * Each Landmark has a unique ID.
    """
    last_id = 0

    def __init__(self, x, y):
        self.__id = Landmark.last_id
        Landmark.last_id += 1

        self.__x = x
        self.__y = y

    def get_id(self):
        return self.__id

    def get_coordinates(self):
        return self.__x, self.__y

    def get_type(self):
        return LandmarkTypes.LANDMARK

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class FOOD(Landmark):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_type(self):
        return LandmarkTypes.FOOD


class NEST(Landmark):
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_type(self):
        return LandmarkTypes.NEST
