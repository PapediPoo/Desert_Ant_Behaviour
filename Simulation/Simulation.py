import time
from Ant import Ant
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
		self.result = None

	def simulate(self):
		# TODO: should the SimulationResults object be reused?
		start = time.time()
		result = SimulationResults()
		self.setAntCount(PM.ant_count)
		for i, ant in enumerate(self.ants):
			result.addPath()
			result.addPoint(i, *ant.getPosition())

		for i, ant in enumerate(self.ants):
			while ant.done is False:
				ant.step()
				result.addPoint(i, *ant.getPosition())
		print("Simulation time:", time.time()-start)
		return result

	def simulateStep(self):
		if self.result is None:
			self.result = SimulationResults()
			self.setAntCount(PM.ant_count)
			for i, ant in enumerate(self.ants):
				self.result.addPath()
				self.result.addPoint(i, *ant.getPosition())
		for i, ant in enumerate(self.ants):
			ant.step()
			self.result.addPoint(i, *ant.getPosition())
		return self.result

	def setAntCount(self, ant_count):
		self.ants = [Ant.Ant(self.environment, self.environment.nests[0]) for i in range(0, ant_count)]
