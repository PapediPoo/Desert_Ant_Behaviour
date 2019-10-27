import Ant
import Simulation.SimulationParameters as PM
from Simulation.SimulationData import SimulationResults


class Simulation:
	'''
	* Holds all information about simulation, runs simulation and returns results.
	'''
	def __init__(self, environment):
		self.ants = []
		self.setAntCount(PM.ant_count)
		self.environment = environment

		# TODO: Replace with success condition
		self.steps = 100

	def simulate(self):
		# TODO: should the SimulationResults object be reused?
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

		return result

	def setAntCount(self, ant_count):
		self.ants = [Ant.Ant() for i in range(0, ant_count)]

	def setSteps(self, steps):
		# TODO: Replace with success condition
		self.steps = steps
