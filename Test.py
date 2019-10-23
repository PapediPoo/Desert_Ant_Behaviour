# Write any test code here so that the rest of the code remains clean

import Ant
import Environment
import GUI
import Simulation
import matplotlib.pyplot as plt

if __name__ == '__main__':
	s = Simulation.Simulation(100, None)
	s.setSteps(250)
	result = s.simulate().getAll()
	for i in range(0, (int)(len(result)/2)):
		plt.plot(result[i], result[i+1])
	plt.axes([0, 50, 0, 50])
	plt.show()
