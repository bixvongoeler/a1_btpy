#################################################################################
# Behavior Tree framework for A1 Behavior trees assignment.                     #
# CS 131 - Artificial Intelligence                                              #
#                                                                               #
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.#
#################################################################################
# Solution Author: William Bix von Goeler (wvongo01)                            #
#            Date: 02/08/2025                                                   #
#     Description: This is the main file for the Roomba simulation. It inits    #
#                  the simulation, creates the GUI, and runs the main loop.     #
#                                                                               #
#################################################################################

import pygame as pg
from sim import *
import random
from bt.robot_behavior import robot_behavior
from bt.globals import *
import bt_library as btl

# Initialize the blackboard
current_blackboard.set_in_environment(BATTERY_LEVEL, 80)
current_blackboard.set_in_environment(SPOT_CLEANING, False)
current_blackboard.set_in_environment(GENERAL_CLEANING, False)
current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
current_blackboard.set_in_environment(HOME_PATH, None)
current_blackboard.set_in_environment(CHARGING, False)
current_blackboard.set_in_environment(VACUUMING, False)
current_blackboard.set_in_environment(SPOT_CLEANING_POSITION, None)
current_blackboard.set_in_environment(NEED_TO_CLEAN, None)
current_blackboard.set_in_environment(ROOM_DIMENSIONS, (GRID_DIM_X, GRID_DIM_Y))
current_blackboard.set_in_environment(MY_RADIUS, ROBOT_RADIUS)
current_blackboard.set_in_environment(HOME_POSITION,
                                      ((GRID_DIM_X - (HOME_SIZE // 2)), (GRID_DIM_Y - (HOME_SIZE // 2))))
current_blackboard.set_in_environment(ROBOT_POSITION,
                                      [round(GRID_DIM_X - (HOME_SIZE // 2)), round(GRID_DIM_Y - (HOME_SIZE // 2))])
current_blackboard.set_in_environment(ROBOT_DIRECTION, (-1, 0))

# Init Window and Clock
pg.init()
clock = pg.time.Clock()
sim_globals.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Init Font for text
sim_globals.font = pg.font.Font("sim/assets/SF-Pro-Rounded-Semibold.otf", 18)
sim_globals.big_font = pg.font.Font("sim/assets/SF-Pro-Rounded-Semibold.otf", 30)
sim_globals.symbol_font = pg.font.Font("sim/assets/PFRB.ttf", 70)

# Creat Surface for Grid
sim_globals.grid_surf = redraw_grid(cells)

# GUI Elements
create_gui_elements()
pause_symbol = sim_globals.symbol_font.render(" ", True, (255, 150, 150))
fast_symbol = sim_globals.symbol_font.render(" ", True, (255, 150, 150))
home_text = sim_globals.font.render('Home', True, (255, 255, 255))

# Step Button (Simulates the robot for a set number of iterations rather than running the simulation in real time)
STEP_SIZE = 1
def step_update():
    """
    Runs the Behavioral Tree STEP_SIZE iterations.
    """
    if sim_globals.is_playing:
        play_pause()
    for i in range(0, STEP_SIZE):
        update_simulation()
    if random.random() < 0.01:
        add_uniform_dirt()
step_btn = Button(name="step_btn", x=83, y=4, width=30, height=TOP_BAR_HEIGHT - (4 * 2),
                  font=sim_globals.font, screen=sim_globals.screen, container=sim_globals.gui_objects,
                  color=color_dict["BLUE"], button_text='>>', on_click_function=step_update, one_press=False)

# Main Logic Loop
PRINT_FULL_STATE = True # Print the state of the tree nodes before and after the evaluation
TOTAL_EVALS = 0 # Track number of evaluations
def update_simulation():
    """
    Updates the simulation by evaluating and triggering the robots sensors, and updating the world state
    by removing dust under the vacuum. evaluating the behavior tree and updating the environment.
    """
    global TOTAL_EVALS

    # Scan Dusty Spot Sensor and Vacuum
    robot.clean_check_dirt()

    # Print the state of the tree nodes before the evaluation
    if PRINT_FULL_STATE:
        print(f'BEFORE [{TOTAL_EVALS}] ---------------------------------------------------------------------')
        btl.print_states(current_blackboard)
        print('================================================================================')
        print(f'RUN [{TOTAL_EVALS}] ---------------------------------------------------------------------')

    # Evaluate the behavior tree
    result = robot_behavior.evaluate(current_blackboard)
    print(result)

    # Print the state of the tree nodes after the evaluation
    if PRINT_FULL_STATE:
        print('================================================================================')
        print(f'AFTER [{TOTAL_EVALS}] ----------------------------------------------------------------------')
        btl.print_states(current_blackboard)
        print('================================================================================')
        TOTAL_EVALS += 1

    # Update the battery level (based on the current task) and add dust
    battery_level = current_blackboard.get_in_environment(BATTERY_LEVEL, 0)

    # If charging, don't deplete battery and timelapse (fastest dust accumulation)
    if current_blackboard.get_in_environment(CHARGING, False):
        sim_config.DUST_FREQUENCY = 5
        sim_config.DIRT_SPOT_FREQUENCY = 0.0001
    # If not cleaning, deplete battery and timelapse (fast dust accumulation)
    elif (not current_blackboard.get_in_environment(SPOT_CLEANING, False) and
          not current_blackboard.get_in_environment(GENERAL_CLEANING, False)):
        sim_config.DUST_FREQUENCY = 20
        sim_config.DIRT_SPOT_FREQUENCY = 0.0005
        battery_level -= 0.005
    # Otherwise, deplete battery (normal dust accumulation)
    else:
        sim_config.DUST_FREQUENCY = 3000
        sim_config.DIRT_SPOT_FREQUENCY = 0.0001
        battery_level -= 0.002
        # If Vacuum is on, deplete battery faster
        if current_blackboard.get_in_environment(VACUUMING, False):
            battery_level -= 0.002
    # Update the battery level on the blackboard
    current_blackboard.set_in_environment(BATTERY_LEVEL, battery_level)

    # Add random dust spots to the grid
    if random.random() < sim_config.DIRT_SPOT_FREQUENCY:
        add_dirt(1, 1, 7, 24)

# Initialize the Robot Object (ONLY RESPONSIBLE for drawing the robot and updating its sensors based on position)
# ALL ROBOT BEHAVIOR IS HANDLED BY THE BEHAVIOR TREE EVALUATED IN update_simulation()
robot = Roomba(current_blackboard=current_blackboard, game_objects=game_objects, screen=sim_globals.screen, cells=cells)

# Add some Initial Dust
for _ in range(0, 80):
    add_uniform_dirt()

# Used to track frame time and update times based on the simulation speed
time_elapsed_since_update = 0
time_elapsed_since_last_draw = 0
time_elapsed_since_last_dust = 0

# MAIN LOOP
running = True
while running:
    # Get the time since the last loop
    dt = clock.tick()

    # Check for Window Close
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update the simulation based on the simulation speed
    if sim_globals.is_playing:
        time_elapsed_since_update += dt
        if time_elapsed_since_update > simulation_speed[0]:  # 17ms is roughly 60fps
            update_simulation()
            time_elapsed_since_update = 0

    # Add Dust based on the simulation speed
    if sim_globals.is_playing:
        time_elapsed_since_last_dust += dt
        if time_elapsed_since_last_dust > (
                simulation_speed[0] + 1) * sim_config.DUST_FREQUENCY:  # 17ms is roughly 60fps
            add_uniform_dirt()
            time_elapsed_since_last_dust = 0

    # Draw the screen at a targeted 60fps
    time_elapsed_since_last_draw += dt
    if time_elapsed_since_last_draw > FRAMETIME:
        # Draw Blank Background
        sim_globals.screen.fill((0, 0, 0))
        # Draw Simulated Grid
        sim_globals.screen.blit(sim_globals.grid_surf, (0 + BATTERY_WIDTH, 0 + TOP_BAR_HEIGHT))
        # Draw Home Text
        sim_globals.screen.blit(home_text, (SCREEN_WIDTH - home_text.get_width(), SCREEN_HEIGHT - home_text.get_height()))
        # Draw GUI
        for gui_object in gui_objects:
            gui_objects[gui_object].process()
        # Draw Game Objects (Robot, and Spot Selector)
        for game_object in game_objects:
            game_object.process()
        # Draw Dock
        draw_dock()
        # Draw Battery Meter
        draw_battery()
        # Update General Button (checks for when robot edits the blackboard)
        update_general_cleaning()
        # Draw FPS Counter
        fps = f"{round(1000 / time_elapsed_since_last_draw)}"
        fps_text = sim_globals.font.render(fps, True, (255, 200, 200))
        sim_globals.screen.blit(fps_text, (
            SCREEN_WIDTH - fps_text.get_width(), SCREEN_HEIGHT - home_text.get_height() - fps_text.get_height()))
        # Draw FastForward/Pause Symbol
        if sim_globals.is_playing:
            if current_blackboard.get_in_environment(CHARGING, False) or not current_blackboard.get_in_environment(
                    SPOT_CLEANING, False) and not current_blackboard.get_in_environment(GENERAL_CLEANING, False):
                sim_globals.screen.blit(fast_symbol, (SCREEN_WIDTH - fast_symbol.get_width(), TOP_BAR_HEIGHT))
        else:
            sim_globals.screen.blit(pause_symbol, (SCREEN_WIDTH - pause_symbol.get_width() * 0.8, TOP_BAR_HEIGHT))
        # Update the screen
        pg.display.update()
        time_elapsed_since_last_draw = 0

pg.quit()
