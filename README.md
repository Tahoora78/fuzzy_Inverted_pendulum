# Fuzzy Inverted Pendulum

Basically, this project consists of an inverted pendulum simulator and a fuzzy controller. The main goal was to develop a simple yet useful simulator to model the environment, so that you are enabled to easily create a fuzzy controller for the inverted pendulum problem.
It was implemented using **pygame** and **pyfuzzy** in *python2.7*.

We have 3 general functions for 3 main steps: fuzzification function 1 In this function the input is received and given by the given figures and the calculation of the line equation We each calculate the function of their belonging to the fuzzy set. pa: REAL; (* description = 'pendulum angle', min = 0, max = 360, unit = 'degrees' ) pv: REAL; ( description = 'pendulum angular velocity', min = - 200, max = 200, unit = 'degrees per second' *) The output of this function is 15 functions belonging to pa and pv. [up_more_right, up_right, up, up_left, up_more_left, down_more_left, do wn_left, down, down_right, down_more_right] [cw_fast_pv, cw_slow_pv, stop_pv, ccw_slow_pv, ccw_fast_pv] inference function 2 In this function, 15 outputs of the previous function are given as input. Using the 43 rules mentioned 5 lists of the output belonging function of these 43 rules as power We set the fuzzy belonging set to force and give it a maximum of 5 lists of belonging functions Return the output title. function 3 Using the 5 inputs of the center of mass function of the shape resulting from the collision of this maximum We get the inputs and the fuzzy force set by the integration method and get it We return in the form of output force

## Getting Started


### Install

    $ sudo pip install virtualenv
    $ virtualenv -p python2.7 venv
    $ source venv/bin/activate
    $ ./install-deps.sh

### Run

    $ ./main.py

Also, you can run the project using custom configurations located in the **configs** directory.

	$ ./main.py configs/full.ini


## Usage


### Physical parameters of simulator

> **M**: cart mass, *kg*
> 
> **m**: pendulum mass, *kg*
> 
> **l**: pendulum length, *m*
> 
> **x**: cart position, *m*
> 
> **v**: cart velocity, *m/s*
> 
> **a**: cart acceleration, *m/s^2*
> 
> **theta**: pendulum central angle, *radian*
> 
> **omega**: pendulum angular velocity, *m/s*
> 
> **alpha**: pendulum angular acceleration, *m/s^2*
> 
> **g**: gravity acceleration, *m/s^2*
> 
> **b**: cart coefficient of friction, *newton/m/s*
> 
> **I**: moment of inertia, *kg.m^2*
> 
> **min_x**: cart minimum x, *m*
> 
> **max_x**: cart maximum x, *m*
> 
> **force**: force applied on cart, *newton*

You can see all the parameters in **world.py** module.
Also these parameters can be modified using configuration files located in **configs** directory.

### Fuzzy Control Language (FCL)
The *FuzzyController* class in **controller.py** module, loads an *FCL* file to decide how much force needs to be applied to the cart in each cycle of simulation.
*FCL* files can be found in **controllers** directory. You can create your own controller by writing a new *FCL* file and specifying it in the *config* files by changing the *fcl_path* item.

**configs/default.ini**:

	[simulator]
	dt = 0.1
	fps = 60


	[controller]
	fcl_path = controllers/simple.fcl


	[world]
	theta = -90.0

### Simple FCL Controller

We have created a simple controller that works just fine and can be found in **controllers** directory. You can also checkout the fuzzy variables chart, available in the **images** directory.
