import matplotlib.pyplot as plt
import tkinter
import numpy as np
from Simulation.Simulation import Simulation
from Simulation.SimulationData import SimulationParameters
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


if __name__ == '__main__':
	# TODO: Unuglify
	root = tkinter.Tk()
	control_panel = tkinter.Frame(root)
	graph_panel = tkinter.Frame(root)

	def _quit():
		root.quit()
		root.destroy()

	def _simulate():
		SimulationParameters.move_speed = speed_scale.get() / 100
		SimulationParameters.turn_dev = angle_scale.get() / 180 * np.pi

		plt.clf()
		s = Simulation(100, None)
		s.setSteps(250)
		result = s.simulate().getAll()
		for i in range(0, (int)(len(result) / 2)):
			plt.plot(result[i], result[i + 1])

		canvas.figure = plt.gcf()
		canvas.draw()

	# Setup graph canvas and toolbar
	canvas = FigureCanvasTkAgg(plt.gcf(), graph_panel)
	canvas.draw()

	canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

	toolbar = NavigationToolbar2Tk(canvas, graph_panel)
	toolbar.update()

	canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

	# Setup control panel
	control_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
	graph_panel.pack(side=tkinter.RIGHT)

	speed_scale = tkinter.Scale(control_panel, from_=25, to=400, orient=tkinter.HORIZONTAL, label="Ant speed")
	speed_scale.pack(side=tkinter.TOP)

	angle_scale = tkinter.Scale(control_panel, from_=1, to=90, orient=tkinter.HORIZONTAL, label="Ant angle")
	angle_scale.pack(side=tkinter.TOP)

	simulate_button = tkinter.Button(control_panel, text="Simulate", command=_simulate)
	simulate_button.pack(side=tkinter.TOP)

	quit_button = tkinter.Button(control_panel, text="Quit", command=_quit)
	quit_button.pack(side=tkinter.BOTTOM)
	root.protocol("WM_DELETE_WINDOW", _quit)

	tkinter.mainloop()
