import numpy as np

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