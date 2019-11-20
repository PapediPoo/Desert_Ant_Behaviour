import time
import threading
import queue
import Ant.Util as util
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
		self.threads = {}

	def simulateAll(self):
		self.result = SimulationResults()
		start = time.time()

		self.setAntCount(PM.ant_count)
		for ant in self.ants:
			self.result.addPath()
			self.result.addPoint(ant.id, *ant.getPosition())

		for ant in self.ants:
			t = util.KillThread(target=self.simulate, args=[ant,])
			t.start()
			self.threads[t.ident] = t
			t.killJoin(2)


		print("Simulation time:", time.time() - start)

		return self.result

	def simulate(self, ant):
		while not ant.done and not (threading.get_ident() in self.threads and self.threads[threading.get_ident()].killed()):
			ant.step()
			self.result.addPoint(ant.id, *ant.getPosition())

			if ant.food_found:
				self.result.foodFound(ant.id)

		if ant.done:
			self.result.nestFound(ant.id)

	def setAntCount(self, ant_count):
		self.ants = [Ant.Ant(i, self.environment, self.environment.nests[0]) for i in range(0, ant_count)]
