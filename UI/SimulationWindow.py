"""
Run this to graphically simulate ants.
"""

from UI.Drawer import drawEnvironment, drawPaths
from Simulation.Simulation import Simulation
import Simulation.SimulationParameters as SimulationParameters
from Environment.Environment import Environment

import matplotlib.pyplot as plt
import tkinter
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

if __name__ == '__main__':
    # Setup window
    root = tkinter.Tk()
    root.title("Desert Ant Behaviour Simulation")
    control_panel = tkinter.Frame(root)
    graph_panel = tkinter.Frame(root)


    def _quit():
        root.quit()
        root.destroy()


    def _simulate(args=None):
        # Read control panel values
        SimulationParameters.ant_count = count_scale.get()
        SimulationParameters.move_speed = speed_scale.get() / 100
        SimulationParameters.move_angle = angle_scale.get() / 180 * np.pi
        SimulationParameters.traceback_angle = traceback_angle_scale.get() / 180 * np.pi
        SimulationParameters.vision_range = vision_scale.get()

        plt.clf()  # clears previous graph
        plt.axis("off")
        plt.tight_layout(0)

        e = Environment().generate_random_environment()
        s = Simulation(e)
        result = s.simulateAll()

        if result is None:
            return

        drawPaths(canvas, result.getAll())
        drawEnvironment(canvas, e)
        canvas.draw()


    # Setup graph canvas and toolbar
    canvas = FigureCanvasTkAgg(plt.gcf(), graph_panel)

    toolbar = NavigationToolbar2Tk(canvas, graph_panel)
    toolbar.update()

    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    # Position control panel
    control_panel.grid(row=0, column=0, sticky="ns")
    graph_panel.grid(row=0, column=1, sticky="nwes")

    # Set weight
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)

    # Setup control panel
    count_scale = tkinter.Scale(control_panel, from_=1, to=30, orient=tkinter.HORIZONTAL, label="Ant count")
    count_scale.set(1)
    count_scale.pack(side=tkinter.TOP)

    speed_scale = tkinter.Scale(control_panel, from_=25, to=400, orient=tkinter.HORIZONTAL, label="Ant move speed")
    speed_scale.set(400)
    speed_scale.pack(side=tkinter.TOP)

    angle_scale = tkinter.Scale(control_panel, from_=1, to=90, orient=tkinter.HORIZONTAL, label="Ant move angle")
    angle_scale.set(15)
    angle_scale.pack(side=tkinter.TOP)

    traceback_angle_scale = tkinter.Scale(control_panel, from_=1, to=90, orient=tkinter.HORIZONTAL, label="Ant traceback angle")
    traceback_angle_scale.set(5)
    traceback_angle_scale.pack(side=tkinter.TOP)

    vision_scale = tkinter.Scale(control_panel, from_=1, to=100, orient=tkinter.HORIZONTAL, label="Ant vision radius")
    vision_scale.set(50)
    vision_scale.pack(side=tkinter.TOP)

    simulate_button = tkinter.Button(control_panel, text="Simulate", command=_simulate)
    simulate_button.pack(side=tkinter.TOP)
    root.bind("s", _simulate)

    quit_button = tkinter.Button(control_panel, text="Quit", command=_quit)
    quit_button.pack(side=tkinter.BOTTOM)
    root.protocol("WM_DELETE_WINDOW", _quit)

    tkinter.mainloop()
