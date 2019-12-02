import numpy as np
import threading


def angle(x, y):
	# calculates angle between (x,y) and the x-axis
	return np.arctan2(y, x)


def clip(val, min_val, max_val):
	# clips a value between a max and a min. numpy implementation is really slow
	if min_val < val < max_val:
		return val
	elif val < min_val:
		return min_val
	else:
		return max_val


class KillThread(threading.Thread):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.__kill_event = threading.Event()

	def kill(self):
		self.__kill_event.set()

	def killed(self):
		return self.__kill_event.is_set()

	def killJoin(self, time):
		self.join(time)
		if self.is_alive():
			self.kill()


def magnitude(x, y):
	return (x ** 2 + y **2) ** (1/2)
