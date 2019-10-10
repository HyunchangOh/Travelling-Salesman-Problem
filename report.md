# Travelling Salesman Problem

20170410 Hyunchang Oh. October 10th.

Travelling salesman problem, or TSP in short, seeks the shortest path to visit all given locations on a map and is a foundational problem of optimisation with many direct applicabilities in real life. While there exists a deterministic algorithm, named *Held-Karp Algorithm*, its high time complexity of *O(n<sup>2</sup>2<sup>n</sup>)*  makes the problem unsolvable with large number of locations. Therefore, several heuristic approaches have been proposed based on stochasticity. This document is to explain how to use and understand *solver.py* a python program to solve TSP with heuristic approach. 

The entirety of *solver.py* is developed solely by Hyunchang Oh without making reference to any external sources other than the lectures provided by Prof. Yoo Shin of KAIST CS.



## 0. Environment Setup

### Install Python

The program requires python to run, as it is a python program. Download and install python for your OS at the link below. The program was built and tested with Python 3.7.4 for Windows. 

For Windows, make sure you add python to the PATH variable during installation. There will be a checkbox for that when installer starts. If you forgot to do so during installation, you follow this document by substituting 'python' with 'py' for commands in cmd.

https://www.python.org/downloads/



### Install NumPy

NumPy is a python package that supports various scientific calculations. In this program, NumPy was used to calculate weighted random for Ant Colony Optimisation.

#### Mac

Go to the page below and download the package called numpy-1.6.1-py2.7-python.org-macosx10.6.dmg.

https://sourceforge.net/projects/numpy/files/NumPy/

#### Windows

If you have pip, type the following command on cmd.

```
pip install numpy
```

If you do not have pip, you can use the *get-pip.py* program attached with this document. Type the following command on cmd.

```
python get-pip.py
```

#### Linux

Type the following command on terminal.

```
sudo apt install python-numpy
```



## 1. How to Run the Program

### Organisation

The following is the files required to/generated by the solver program are stored in the tsp/ directory.

- solver.py

  The main python solver program. 

- rl11849.tsp

  Example tsp file with 11849 points. Running the solver program with this file will require a lot of time and space, which some computers may not be able to support.

- a280.tsp

  Example tsp file with 280 points. The solver program was mainly tested with this size of input, and thus is guaranteed to perform well.

- solution.csv

  This file is not given at the first time, but the solver program will save any intermediate optimal state it encounters to this file. If you run the solver program for the same tsp file, the solver program will start from the existing solution.csv file. If you run the solver program for another tsp file, this file will be overwritten with the solution for that tsp file, so be sure to save the file to other safe directory.

- get-pip.py

  This file is to install pip for windows. If you are on other OS, or have pip installed already, you do not need to care about this file at all.

- burma14.tsp

  Example tsp file with 14 points. As this problem has very small number of points, it is the best choice to explore various features of the solver quickly. 

  

### The Basic Command

The solver program can be used for any tsp files under the format of those posted at http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html

The solver program also supports passing specific parameters for optimisation under specific flags. See below for what they are. For now, you can try running the program with default parameter values, which are automatically loaded if you do not specify.

The below is the command-line code for executing the program for burma14.tsp. Substitute this to the file of your interest, that is saved at the same directory as solver.py. Also, be sure to run the command at the directory where solver.py lies.

```
python solver.py burma14.tsp
```



### The Parameters

The solver has three parts: (1) modified ant colony optimisation step(ACO) (2) two point random swap (2PRS) (3) three point random swap(3PRS). Here, let's give our attention to the parameters for each step and how to use flags to change them. Exact mechanics of, and heuristics behind each step will be discussed at the next section. All parameters may only take positive integers, except *"Message Toggle"* (flag: -m).

##### Overall
**-f:**  *"Total generation number"* The solver iterates through ACO, 2PRS, 3PRS. This number specifies the number of this big cycle. For example, when this number is 2, the solver will proceed as the following: ACO-2PRS-3PRS-ACO-2PRS-3PRS. 
**-m**: *"Message Toggle"* The solver will print out certain messages at end of each step, and also let the user know when an improvement has been made. If this value is 0 (default), no message will be printed. If this is value is set to be nonzero, messages will be printed.

##### Modified Ant Colony Optimisation

**-ag:** *"Ant Generation"* Specifies the number of generations the solver will process for the ACO step.
**-an:** *"Ants"* Specifies the number of ants used for each ant generation.

**-phbf**: *"Pheromone from beforelife"* Specifies the multiplication constant to the pheromones on the edge of saved solution.

##### Two Point random Swap
**-p2:** *"children number"* specifies the number of children solutions that will be generated from each selected solution of each generation.
**-s2:** *"selection number"* specifies the number of solutions that will be selected and passed to the next generation
**-g2:** *"generations"* specifies the number of generations
**-r2:** *"range"* During 2PRS, the first point will be chosen randomly. The second point will be chosen from the points whose order of visit differs less than 'range' to the first point. 

##### Three Point Random Swap

**-p3:** *"children number"* specifies the number of children solutions that will be generated from each selected solution of each generation.
**-s3:** *"selection number"* specifies the number of solutions that will be selected and passed to the next generation
**-g3:** *"generations"* specifies the number of generations
**-r3:** *"range"* During 2PRS, the first point will be chosen randomly. The second point and the third point will be chosen from the points whose order of visit differs less than 'range' to the first point. 

##### Changing Both Random Swap Parameters at Once

**-p, -s, -g, -r**: Changes the corresponding parameters of 2PRS and 3PRS together. If this and 2PRS-specific/3PRS-specific flag were used together, 2PRS/3PRS-specific flag will have a higher priority.



### Default Values

You can only specify few of the parameters listed above. Those that have not been specified by the user will have the default value. The default values are also useful in a sense that they provide one decent heuristic, and that you may develop your own heuristics based on that.

**-f:**  *"Total generation number"* 10 
**-m**: *"Message Toggle"* 0
**-ag:** *"Ant Generation"*  3
**-an:** *"Ants"* 3
**-p2:** *"children number"* 5
**-s2:** *"selection number"* 3
**-g2:** *"generations"* 4000
**-r2:** *"range"* 5
**-p3:** *"children number"* 5
**-s3:** *"selection number"* 3
**-g3:** *"generations"* 4000
**-r3:** *"range"* 5



## 2. How the Program works

### 2-1. The starting point

The solver will first look for *solution.csv* file. If such a file exists at the same directory with the solver, the solver will then check its length. If the length complies with the number of points for the given tsp file, solver will begin from *solution.csv*. 

If there is no *solution.csv*, or the number of values in *solution.csv* do not comply with the tsp file, solver will create a brand-new *solution.csv* and a new starting solution will be generated at the first modified ant colony optimisation step.



### 2-2 Modified Ant Colony Optimisation Step

The first algorithm to be applied by the solver is the modified ant colony optimisation step. It is derived from the ant colony optimisation algorithm introduced in class, but some heuristics have been applied to modify the algorithm.

#### Generation of Pheromone List

Solver will first generate a 2-D list (implemented with dictionary data structure), that specifies the amount of pheromone on each edge. (1) Initially, the amount of pheromone on each edge is not uniform, but is inversely proportional to the length of the edge. (2) If there is a saved file, extra pheromone will be spread on the edges present on the saved solution; the amount of pheromone spread on step 1 will be multiplied by a special parameter named *pheromone from beforelife*. 

Note that all edges are 'bidirectional', meaning that any given pair of points is connected with two edges, (For example for point A and B, the two edges will be A -->B and B-->A) and may have distinct pheromone values. Mathematically, this may seem useless as the order of visit does not affect the fitness function at all. However, having bidirectional edges is beneficial when there can only be a few ants due to low computing power. With just a few ants and few generations, it is necessary to distinguish their order of visit and let the solution follow that accordingly.

#### Tour of the Ants

For each generation, ants will be placed at random point, with their number specified under the flag *-an*. The probability of a point to be selected for the next point is proportional to the amount of pheromone present on corresponding edge (direction sensitive). When an edge has been traveled by an ant, the pheromone value on that edge will be increased by a certain value. Note that this change is not visible to other ants of the same generation. This is made possible by keeping two separate pheromone-edge list, and updating only one of them during each generation.

Points that have been already visited by an ant will not be visible to that ant. The tour of the ant finishes when the ant has visited all points, or equivalently when there is no visible point left for an ant. Then, the tour for another ant will begin with the pheromone-edge list that has been saved at the end of the previous generation (or initialisation). When a generation finishes, the updated pheromone list will be copied to the un-updated pheromone list. This will continue for *generations* (flag: -ag) number of generations.

#### Retrieving the Solution

It is impossible to get an immediate solution from the pheromone list as it is not a 1D order of points, but a 2D list. Therefore, a special method has been prepared to retrieve a 1D order of points from the 2D pheromone list.

First, a point will be randomly chosen. Let's call this point A. Then, the point connected with A by the edge with the most pheromone will be chosen as the next point (again, edges are direction sensitive). Visited point will be 'popped' from the pheromone list and thus will not be visited again. The retrieval ends when there is no point left. The total distance for the retrieved solution will be calculated.

If the total distance for the retrieved solution is shorter than that of the saved solution (if any), the new solution will be saved, overwriting the old *solution.csv* file. Else, the retrieved solution will be discarded and later steps will take the old solution as the starting point. If a better solution 



### 2-3 Two Point Random Swap

Two point random swap is extremely easy, if the population control mechanic was ignored for now. Solver will first pick a random point in the list. Then, it will choose a second random point within the range (not in distance, but in order of visit) of *ran* (flag: -r2), so that the maximum difference in order of visit is *ran*. Solver will swap two points, calculate the total distance, and save the new order if the total distance is decreased. One method, named **'the population control'**, was employed to avoid falling straightly into local optimum and another method, named  **'swapping distance calculation'**, to shorten the resource usage on calculation of total distance.

#### Population Control

At each generation, solver will not only keep one best solution, but a list of multiple best solutions. The best *selection number* (flag: -s2) of members from the list will be passed to the next generation. Then, at the next generation, *children number* (flag: -p2) of new solutions will be generated from each of the solutions that has been passed from the previous generation. Therefore, each generation will have a total of *children number* * *selection number* of new solutions in addition to the list of solutions passed from the previous generation. 

 At the first generation, there is only one solution passed from the previous step, not a *selection number* of solutions. To compensate this, *children number* * *selection number* of solutions is generated from one single solution at the first generation.

At the last generation, one best solution is saved to *solution.csv* and all other is discarded. 

#### Swapping Distance Calculation Method

Only two points are swapped at each instance, and maximum of four edges have been changed. It will be a waste of time if solver has to calculate the total distance without making use of this information. Therefore, a very efficient distance calculation method has been employed.

If two selected points are adjacent to each other, total of three edges have been destroyed and newly formed. So, the lengths of the three edges will be subtracted from total distance, and the lengths of the newly formed edges will be added to the total distance. Now we have the up-to-date total distance.

If two selected points are not adjacent to each other, total of four edges have been destroyed and newly formed. Similar operations will be conducted for the four edges, and we can get the up-to-date total distance.



### 2.4 Three Point Random Swap

Population control and  swapping distance calculation method have also been employed to this step. The only difference with the Two Point Random Swap is that the solver now takes three randomly chosen points and shuffles them. One point will be randomly selected. The second and third point will be selected within the range of *ran3* (in order of visit, not distance) from the first point. First point (A) and second point (B) are swapped first. Then the first point, now at the position of the second point, will be swapped with the third point (C). See below illustration to un-confuse yourself.

Initial state: -----------A-------- B---------C --------

After first swap: -----------------B-------------A----------C-------------

After second swap: -----------------B-----------C----------A------------



### 2.5 The Grand Iteration

Solver will apply the methods in the following order: Modified Ant Colony Optimisation --> Two Point Random Swap -->  Three Point Random Swap. This iteration will be repeated *total generation number* (flag: -f) of times. Modified Ant Colony Optimisation (MACO) step will only begin from a saved solution, which is the best solution acquired so far. Two Point Random Swap(2PRS) will begin from one best solution returned by MACO, even if that solution is actually 'worse' than the solution saved in *solution.csv* file. At the end of 2PRS, its best solution will be compared to *solution.csv*, and the better one will assume the position of *solution.csv*. Three Point Random Swap will begin from one best solution returned by 2PRS, even if that is actually worse than *solution.csv*. 3PRS, similar to 2PRS, will write to *solution.csv* file if its final best is better than previous *solution.csv*. If the solution returned by 3PRS is worse than *solution.csv* this solution will be discarded forever, and MACO step of next generation will begin from *solution.csv*. 

#### Why is the grand iteration arranged in this order?

2PRS, and 3PRS are much faster than MACO, and thus can find a reasonable local optimum quickly. However, they lack the power to jump from a local optimum to another, even with the population control feature. MACO provides more randomness, so that solver may 'jump' to spots further away in the fitness landscape, where it may a better local optimum, or even the global optimum. 
