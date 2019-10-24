import matplotlib.pyplot as plt
import tkinter
import numpy as np
from Simulation.Simulation import Simulation
import Simulation.SimulationParameters as SimulationParameters
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


if __name__ == '__main__':
	# TODO: Add visual representation of environment
	# Setup window
	root = tkinter.Tk()
	root.title("Desert Ant Behaviour Simulation")
	control_panel = tkinter.Frame(root)
	graph_panel = tkinter.Frame(root)

	def _quit():
		root.quit()
		root.destroy()

	def _simulate():
		# Read control panel values
		SimulationParameters.ant_count = count_scale.get()
		SimulationParameters.move_speed = speed_scale.get() / 100
		SimulationParameters.turn_dev = angle_scale.get() / 180 * np.pi
		SimulationParameters.vision_radius = vision_scale.get()
		SimulationParameters.dist_error = speed_error_scale.get()
		SimulationParameters.angle_error = angle_error_scale.get()

		plt.clf()
		s = Simulation(SimulationParameters.ant_count, None)
		s.setSteps(250)
		result = s.simulate().getAll()
		for i in range(0, (int)(len(result) / 2)):
			plt.plot(result[i], result[i + 1])

		canvas.figure = plt.gcf()
		canvas.draw()

	# Setup graph canvas and toolbar
	canvas = FigureCanvasTkAgg(plt.gcf(), graph_panel)
	canvas.draw()

	toolbar = NavigationToolbar2Tk(canvas, graph_panel)
	toolbar.update()

	canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

	# Position control panel
	control_panel.grid(row=0, column=0, sticky="ns")
	graph_panel.grid(row=0, column=1, sticky="nwes")

	# Set weight
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=0)
	root.columnconfigure(1, weight=1)

	# Setup control panel
	count_scale = tkinter.Scale(control_panel, from_=1, to=250, orient=tkinter.HORIZONTAL, label="Ant count")
	count_scale.pack(side=tkinter.TOP)

	speed_scale = tkinter.Scale(control_panel, from_=25, to=400, orient=tkinter.HORIZONTAL, label="Ant speed")
	speed_scale.pack(side=tkinter.TOP)

	angle_scale = tkinter.Scale(control_panel, from_=1, to=90, orient=tkinter.HORIZONTAL, label="Ant angle")
	angle_scale.pack(side=tkinter.TOP)

	vision_scale = tkinter.Scale(control_panel, from_=1, to=100, orient=tkinter.HORIZONTAL, label="Ant vision radius")
	vision_scale.pack(side=tkinter.TOP)

	speed_error_scale = tkinter.Scale(control_panel, from_=0, to=100, orient=tkinter.HORIZONTAL, label="Ant speed error")
	speed_error_scale.pack(side=tkinter.TOP)

	angle_error_scale = tkinter.Scale(control_panel, from_=0, to=100, orient=tkinter.HORIZONTAL, label="Ant angle error")
	angle_error_scale.pack(side=tkinter.TOP)

	simulate_button = tkinter.Button(control_panel, text="Simulate", command=_simulate)
	simulate_button.pack(side=tkinter.TOP)

	quit_button = tkinter.Button(control_panel, text="Quit", command=_quit)
	quit_button.pack(side=tkinter.BOTTOM)
	root.protocol("WM_DELETE_WINDOW", _quit)

	tkinter.mainloop()
