# Desert Ant Behaviour

## Overview

This code is part of our project in Agent Based Modelling and Social Simulations. Our paper with detailed explanations can be found in Paper.pdf.

We simulated the food-gathering behaviour of desert ants. Our environment is represented by a two-dimensional plane and contains the nest, (possibly) multiple food-sources and landmarks which are used by the ants for orientation. An ant performs the following actions:

- The ant starts at the nest (with coordinates (0, 0)) and performs a biased random walk (biased toward the current direction vector) until it stumbles upon food. For each discovered landmark, the ant remembers the directional vector to the previous landmark (or to the nest for the first landmark). Once the ant has found a food source, it uses these vectors to walk back to the nest.
- Because the walking-back-to-the-nest is also a biased random walk (though with a stronger bias towards the visited landmarks than in food-search behaviour), a probability exists that the ants loses its track. It then switches back to search behaviour until it finds another known landmark.
- Once the ant found back to the nest, its journey has ended.

## Adjustable Parameters

The environment can be controlled by the following parameters (found in Environment/EnvironmentParameters.py):

- the number of nests,
- the number of landmarks,
- the number of food sources,
- the width and the height of the playground and
- the action range which describes the minimal distances in which an ant has "found" the nest or a food source.

The simulation itself can be controlled by the following parameters (found in Simulation/SimulationParameters.py):

- the move-speed which describes the distance traveled during a timestep,
- the standard deviation of the move angle in food-search behaviour,
- the standard deviation of the move angle in nest-search behaviour,
- the vision range which describes the minimal distance in which an ant "sees" a landmark and
- the number of ants.

There are two ways to run a simulation:

## Graphical Interface

With the graphical interface, one can play with the various simulation parameters and visualize the paths taken by the ants. To start the graphical interface, one can use the following command:

    python -m UI.SimulationWindow

## Batch Simulation

To gather statistics of the typical behaviour with respect to different parameters, a batch simulation can be performed by executing 

    python -m Statistics.CollectStatistics

In MeasureStepCount.py, mutiple simulations are executed simultaniously on multiple cores. The simulations on each process are parameterized by the thread index and can thus simulate differents parameters.

However: to change the parameters tested, one has to directly change the code in MeasureStepCount.py. Thus, do not run it unless you understand the code. Furthermore, one has to consider that simulating even one degree of freedom takes quite some time depending on the processor and memory.

Instead of runnig simulations on your own, we recommend you to take a look at the graphs produced by us. They are located in the folder "Desert Ant Behaviour Graphics".

## Notes Regarding Reproducability

The code is written for Python 3.74. We used the following libraries:

- numpy
- matplotlib

If you do not have Python nor the libraries installed on your system:

1.  Install Python 3.7.4 using the excecutables on https://www.python.org/downloads/release/python-374/.
2.  Install numyp and matplotlib using the following command:

        pip install numpy matplotlib

3.  In the command line, navigate to this folder and run

        python -m UI.SimulationWindow