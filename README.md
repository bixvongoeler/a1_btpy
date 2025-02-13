# CS131 A1 Behavior Trees
This project implements the provided behavior tree, adding to it by providing a simple GUI and visualization of the simulation state. It uses a hierarchical behavior tree to control the robot in a simulated discrete grid environment, and perform user requested actions such as spot cleaning or general room cleaning.

## Requirements
- Tested using `Python 3.11`
- Install: `pygame` for GUI and visualization
- Install: `numpy` for numerical operations and grid representation
- Or run: `pip install -r requirements.txt` inside project directory

## Running The Project
1. Run the project using `python main.py`
2. The GUI will open, displaying the grid and the robot's current state. 

[![GUI](imgs/window_ss.png)](imgs/window_ss.png)

3. Use the buttons to control the robot's actions:
   - `Play/Pause`: Start or pause the simulation.
   - `>>`: Step through the simulation one step at a time. 
   - `Add Dirt`: Adds small _dusty spots_ around the grid which when hit activate the dusty spot sensor. 
   - `Spot Clean`: Allows the user to select a spot on the grid for special spot cleaning.
   - `General Clean`: The robot will clean the entire room.
   - `Speed Slider`: Controls how frequently the behavior tree is evaluated.
4. When finished exit the program by closing the window or with `^C` in the terminal.

## Structure and Assumptions
### Environment and Simulation
I have designed the simulation to emulate the real world interactions of a vacuum robot with its environment. As such, the robots internal behavior tree only knows the information stored within the blackboard. The robot class in the simulation acts as the shell: it activates relevant sensors on the blackboard such as spot cleaning requested or dirty spot sensor activated. The environmental simulation is purely for visualization, sensor activation, and user interaction. While the robot is not performing a task, or charging, the simulation fast forwards. The dust accumulation rate increases and the robots battery drains at an increased rate to simulate the dormant time. The simulation takes place on a discrete grid, with each cell holding the cells dust state. The robot also moves through this grid in a discrete matter, although the robots renderer attempts to smooth the visualization of this motion and rotation by creating "fake" intermediate locations to render at between behavior tree updates.

### Node Structure
The behavior tree uses a hierarchy of node types that inherit from a base TreeNode class. Key node types include Task (action nodes like "GoHome"), Condition (decision nodes like "BatteryLessThan30"), and Composite nodes (Sequence, Selection, and Priority) that manage multiple children. Decorator nodes like Timer modify child behaviors.
The tree evaluates from root to leaves each cycle. When a node returns RUNNING (like during timed operations), the evaluation pauses until the next cycle. The robot prioritizes charging when battery is below 30%, executing a FindHome → GoHome → Charge sequence until reaching 100% before resuming other tasks.
All nodes share state through a blackboard system that tracks battery, position, and cleaning status.

### Assumptions
![bt_figure.png](imgs/bt_figure.png)
My implementation of the tree maintains the required node structure, although adds a significant number of interactions with the blackboard in order to facilitate robot movement or coordinate positions of spots/home. Additionally, the timer tasks have expiration times multiplied by a factor of five. This was necessary to facilitate the small grid size and discrete movement style. The clean spot tasks also include code allowing for their implementation to be replaced with Until Succeed nodes (rather than the current timer implementation). In this version the task runs until the entire spot has been cleaned rather than being dictated by a timer. Additionally, my implementation of the Priority nodes includes no internal representation of sub node priority's beyond the order in which they have been added to the Priority node in its constructor.

### Potential Future Improvements
- Obstacle detection/avoidance
- More nuanced pathfinding and floor cleaning paths.
- Continuous representation of position, rotation, using velocity and acceleration.
- Better textures/gui and more cleaning modes.

### Feature ScreenShots
#### Dynamic Dust Simulation
![dust_path.png](imgs/dust_path.png)
#### Spot Cleaning Indicators
![Spot_cleaning.png](imgs/Spot_cleaning.png)
