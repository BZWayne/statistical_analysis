Research Track II - Assignment
==================================

This is the assignment of the course Research Track 2, Robotics Engineering, University of Genoa, Italy.

The assignment is divided into four parts, which are: 
1) Research Track II Documentation was added using Sphinx from the Research Track I task.
2) Jupyter notebook was added to interact with the simulation on the third assignment:
   * To experiment some modalities
   * To plot the graphs for the laser scanner data, odometry data and reached / not-reached targets.
  
3) Perform a statistical analysis on the first assignment. To compare two code for statistics: 
   * [My code](https://github.com/BZWayne/rt_exercises/tree/main/robot_simulation_python)
   * [Professor's code](https://github.com/CarmineD8/python_simulator.git)
   
4) [Report of research theme](https://github.com/BZWayne/rt2_exercises/blob/main/RT2_report.pdf) 


Sphinx Documentation
-------------------

This is part of the Research Track 2 Documentation which is inside in folder *rt2_exercises/docs/html*

* [Documentation](https://github.com/BZWayne/rt2_exercises/tree/main/docs/html/index.html)


Jupyter Notebook
-------------------

This is part of the Research Track 2 [Jupyter](https://github.com/BZWayne/rt2_exercises/blob/main/jupyter/final_assignment.ipynb)

* To launch the Jupyter notebook, type these in two terminals:
```bash
$ jupyter notebook --allow-root --ip 0.0.0.0
```
```bash
$ roslaunch rt2_exercises jupyter.launch
```

Improvements
------------------

There are three main improvements that I came up with, which are:

* Provide better interface for sequentially setting the goal
* Develop more structured code 
