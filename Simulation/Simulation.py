import time
import Ant
from Environment.Environment import Environment
import Simulation.SimulationParameters as PM
from Simulation.SimulationData import SimulationResults


class Simulation:
	'''
	* Holds all information about simulation, runs simulation and returns results.
	'''
	def __init__(self, environment):
		self.environment = environment
		self.ants = []
		self.setAntCount(PM.ant_count)

		# TODO: Replace with success condition
		self.steps = 100

	def simulate(self):
		# TODO: should the SimulationResults object be reused?
		start = time.time()
		result = SimulationResults()
		self.setAntCount(PM.ant_count)
		for i, ant in enumerate(self.ants):
			result.addPath()
			result.addPoint(i, *ant.getPosition())

		# TODO: Replace with success condition
		for step in range(0, self.steps):
			for i, ant in enumerate(self.ants):
				ant.step()
				result.addPoint(i, *ant.getPosition())
		print("Simulation time:", time.time()-start)
		for ant in self.ants:
			print("Ant found landmarks:", ant.landmarks)
		return result

	def setAntCount(self, ant_count):
		self.ants = [Ant.Ant(self.environment, self.environment.nests[0]) for i in range(0, ant_count)]

	def setSteps(self, steps):
		# TODO: Replace with success condition
		self.steps = steps
