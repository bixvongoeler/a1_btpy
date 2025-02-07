#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#
from collections import namedtuple

from sockshandler import is_ip

import bt_library as btl

from bt.robot_behavior import robot_behavior
from bt.globals import *
from bt_library import Blackboard

import pygame as pg
import numpy as np
import random

# Main body of the assignment
current_blackboard = btl.Blackboard()
current_blackboard.set_in_environment(BATTERY_LEVEL, 80)
current_blackboard.set_in_environment(SPOT_CLEANING, False)
current_blackboard.set_in_environment(GENERAL_CLEANING, True)
current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
current_blackboard.set_in_environment(HOME_PATH, None)
current_blackboard.set_in_environment(CHARGING, False)
current_blackboard.set_in_environment(VACUUMING, False)
current_blackboard.set_in_environment(SPOT_CLEANING_POSITION, None)

GRID_DIM_X = 135
GRID_DIM_Y = 135
CELL_SIZE = 5

GRID_WIDTH = GRID_DIM_X * CELL_SIZE
GRID_HEIGHT = GRID_DIM_Y * CELL_SIZE

BATTERY_WIDTH = 30
TOP_BAR_HEIGHT = 40

SCREEN_WIDTH = BATTERY_WIDTH + GRID_WIDTH
SCREEN_HEIGHT = TOP_BAR_HEIGHT + GRID_HEIGHT

color_dict = {
    "WOOD_COLOR": (210, 180, 140),  # Constant floor color
    "DARK_WOOD_COLOR": (20, 50, 90),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DARK_GRAY": (100, 100, 100),
    "BLUE": (0, 0, 255),
    "GREEN": (76, 175, 80),
    "ORANGE": (255, 165, 0),
    "RED": (244, 67, 54),
    "BROWN": (139, 69, 19),
    "DARK_GREEN": (0, 100, 0),
}
current_blackboard.set_in_environment(HOME_POSITION, ((GRID_DIM_X // 2), 2))
current_blackboard.set_in_environment(ROBOT_POSITION, [(GRID_DIM_X // 2), (GRID_DIM_X // 2)])

# Create the external game state
cells = np.ndarray((GRID_DIM_X, GRID_DIM_Y, 3), dtype=int)
cells[:,:,:] = color_dict["WOOD_COLOR"]

# Init Window and Clock
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

# Font for text
font = pg.font.Font(None, 24)

# Creat Surface for Grid
home_pos = current_blackboard.get_in_environment(HOME_POSITION, ((GRID_DIM_X // 2), 2))
surf = pg.Surface((GRID_DIM_X, GRID_DIM_Y))
def redraw_grid():
    global surf
    for x in range(home_pos[0] - 2, home_pos[0] + 3):
        for y in range(home_pos[1] - 2, home_pos[1] + 3):
            if 0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y:
                cells[x][y] = color_dict["DARK_GREEN"]

    new_surf = pg.Surface((GRID_DIM_X, GRID_DIM_Y))
    # Draw the grid onto surface
    pg.surfarray.blit_array(new_surf, cells)
    # Transform to screen size
    surf = pg.transform.scale(new_surf, (GRID_WIDTH, GRID_HEIGHT))
    # Add small gaps between cells
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x % CELL_SIZE == 0 or y % CELL_SIZE == 0:
                surf.set_at((x, y), (170, 140, 100))
redraw_grid()


# Draw the top bar
simulation_speed = [1000]
is_playing = False
current_blackboard.set_in_environment(SPOT_CLEANING, False)
current_blackboard.set_in_environment(SPOT_CLEANING_POSITION, None)
current_blackboard.set_in_environment(GENERAL_CLEANING, False)

gui_objects = {}
game_objects = []

# Classes
class Button:
    def __init__(self, name, x, y, width, height, color=(200,200,200), button_text='Button', on_click_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False

        self.fillColors = {
            'normal': color,
            'hover': (max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25)),
            'pressed': (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        }

        self.button_surface = pg.Surface((self.width , self.height))
        # self.button_outline = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_text_surf = font.render(button_text, True, (20, 20, 20))
        gui_objects.update({name: self})

    def update_colors(self, color):
        self.fillColors = {
            'normal': color,
            'hover': (max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25)),
            'pressed': (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        }

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fillColors['normal'])

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fillColors['pressed'])
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_text_surf, [
            self.button_rect.width / 2 - self.button_text_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf.get_rect().height / 2
        ])

        screen.blit(self.button_surface, self.button_rect)

class Slider:
    def __init__(self, name, x, y, width, puck_width, height, value, v_min, v_max, color=(200,200,200), l_text='left', r_text='right'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.puck_width = puck_width
        self.value = value
        self.v_min = v_min
        self.v_max = v_max

        self.fillColors = {
            'normal': color,
            'puck': (255, 255, 255),
            'puck_hover': (200, 200, 200)
        }

        self.button_surface = pg.Surface((self.width, self.height))
        # self.button_outline = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.percent_value = 0
        self.refresh_percent_value()
        self.puck_rect = pg.Rect(self.x + ((self.percent_value ** (1/3)) * self.width) - (self.puck_width / 2), self.y, self.puck_width, self.height)
        self.puck_surface = pg.Surface((self.puck_width, self.height))
        self.button_text_surf_l = font.render(l_text, True, (20, 20, 20))
        self.button_text_surf_r = font.render(r_text, True, (20, 20, 20))
        gui_objects.update({name: self})

    def refresh_percent_value(self):
        self.percent_value = max(0, min(100, ((self.value[0] - self.v_min) / (self.v_max - self.v_min))))

    def update_colors(self, color):
        self.fillColors = {
            'normal': color,
            'puck': (255, 255, 255),
            'puck_hover': (200, 200, 200)
        }

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fillColors['normal'])
        self.puck_surface.fill(self.fillColors['puck'])

        if self.button_rect.collidepoint(mouse_pos):
            self.puck_surface.fill(self.fillColors['puck_hover'])

            if pg.mouse.get_pressed(num_buttons=3)[0]:
                # self.puck_surface.fill(self.fillColors['pressed'])
                mouse_percent = (mouse_pos[0] - self.x) / self.width
                value_percent = self.v_min + ((mouse_percent ** 3) * (self.v_max - self.v_min))
                self.value[0] = max(self.v_min, min(self.v_max, round(value_percent)))
                self.refresh_percent_value()
                self.puck_rect.x = self.x + ((self.percent_value ** (1/3)) * self.width) - (self.puck_width / 2)

        self.button_surface.blit(self.button_text_surf_l, [
            self.button_text_surf_l.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf_l.get_rect().height / 2
        ])
        self.button_surface.blit(self.button_text_surf_r, [
            self.button_rect.width - self.button_text_surf_r.get_rect().width - self.button_text_surf_r.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf_r.get_rect().height / 2
        ])
        screen.blit(self.button_surface, self.button_rect)
        screen.blit(self.puck_surface, self.puck_rect)

class SpotSelector:
    def __init__(self):
        self.radius = 2
        self.color = color_dict["BLUE"]
        self.active = True

    def process(self):
        if self.active:
            pg.draw.circle(screen, self.color, pg.mouse.get_pos(), self.radius * CELL_SIZE, 3)
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                x = (pg.mouse.get_pos()[0] - BATTERY_WIDTH) // CELL_SIZE
                y = (pg.mouse.get_pos()[1] - TOP_BAR_HEIGHT) // CELL_SIZE
                if 0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y:
                    global current_blackboard
                    current_blackboard.set_in_environment(SPOT_CLEANING_POSITION, (x, y))
                    current_blackboard.set_in_environment(SPOT_CLEANING, True)
                    add_dirt_at(x, y, self.radius)
                    print(f"Dusty Spot: x:{x}, y:{y}")
                    self.active = False
        else:
            if not current_blackboard.get_in_environment(SPOT_CLEANING, False):
                gui_objects["spot_cleaning_btn"].update_colors(color_dict["RED"])
                gui_objects["spot_cleaning_btn"].button_text_surf = font.render('Spot Clean: Off', True, (20, 20, 20))
                game_objects.remove(self)
                del self

class Roomba:
    def __init__(self):
        self.color = color_dict["BLACK"]
        self.head_color = (50, 50, 50)
        self.radius = 1.5
        self.head_radius = 1.0
        self.blackboard = current_blackboard
        self.x = self.blackboard.get_in_environment(ROBOT_POSITION, [-1, -1])[0]
        if self.x == -1:
            assert False, "Robot position not set"
        self.y = self.blackboard.get_in_environment(ROBOT_POSITION, [-1, -1])[1]
        if self.y == -1:
            assert False, "Robot position not set"
        game_objects.append(self)
    def process(self):
        pos = self.blackboard.get_in_environment(ROBOT_POSITION, [-1, -1])
        assert 0 <= pos[0] < GRID_DIM_X, "Robot x position out of bounds"
        assert 0 <= pos[1] < GRID_DIM_Y, "Robot y position out of bounds"
        self.x = pos[0]
        self.y = pos[1]

        pg.draw.circle(screen, self.color, (self.x * CELL_SIZE + BATTERY_WIDTH + CELL_SIZE // 2,
                                                   self.y * CELL_SIZE + TOP_BAR_HEIGHT + CELL_SIZE // 2),
                                                   self.radius * CELL_SIZE)
        pg.draw.circle(screen, self.head_color, (self.x * CELL_SIZE + BATTERY_WIDTH + CELL_SIZE // 2,
                                                        self.y * CELL_SIZE + TOP_BAR_HEIGHT + CELL_SIZE // 2),
                                                        self.head_radius * CELL_SIZE)

    def clean_check_dirt(self):
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if self.blackboard.get_in_environment(VACUUMING, False):
                    cells[x][y] = color_dict["WOOD_COLOR"]
                    redraw_grid()
                else:
                    found_dirt = False
                    if 0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y:
                        if not np.array_equal(cells[x][y], color_dict["WOOD_COLOR"]):
                            found_dirt = True
                    if found_dirt:
                        self.blackboard.set_in_environment(DUSTY_SPOT_SENSOR, True)
                    else:
                        self.blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
        redraw_grid()


# Helper FUnctions
def play_pause():
    global is_playing
    if is_playing:
        is_playing = False
        gui_objects["is_playing"].button_text_surf = font.render('Paused', True, (20, 20, 20))
        gui_objects["is_playing"].update_colors(color_dict["RED"])
    else:
        is_playing = True
        gui_objects["is_playing"].button_text_surf = font.render('Playing', True, (20, 20, 20))
        gui_objects["is_playing"].update_colors(color_dict["GREEN"])

def step_update():
    global is_playing
    if is_playing:
        play_pause()
    update_simulation()

def add_dirt():
    num_clusters = random.randint(8, 16)
    for _ in range(num_clusters):
        # Choose a random center point for the cluster
        center_x = random.randint(0, GRID_DIM_X - 1)
        center_y = random.randint(0, GRID_DIM_Y - 1)

        # Add dirt in a small radius around the center
        radius = random.randint(3, 8)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy > radius * radius:
                    continue
                # Add some randomness to the cluster shape
                if random.random() < 0.8:  # 70% chance to add dirt in radius
                    x = center_x + dx
                    y = center_y + dy
                    if 0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y:
                        dirt_color = random.randint(100, 200)
                        cells[x][y] = (dirt_color, dirt_color, dirt_color)
    redraw_grid()

def add_dirt_at(x, y, radius, is_spot=True):
    # Add dirt in a small radius around the center
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue
            # Add some randomness to the cluster shape
            if random.random() < 0.75:  # 70% chance to add dirt in radius
                i = x + dx
                j = y + dy
                if 0 <= i < GRID_DIM_X and 0 <= j < GRID_DIM_Y:
                    dirt_color = random.randint(50, 150)
                    if is_spot:
                        cells[i][j] = (255, dirt_color, dirt_color)
                    else:
                        cells[i][j] = (dirt_color, dirt_color, dirt_color)
    redraw_grid()

def spot_cleaning():
    global game_objects
    if not current_blackboard.get_in_environment(SPOT_CLEANING, False):
        game_objects.append(SpotSelector())
        gui_objects["spot_cleaning_btn"].update_colors(color_dict["GREEN"])
        gui_objects["spot_cleaning_btn"].button_text_surf = font.render('Spot Clean: On', True, (20, 20, 20))

def general_cleaning():
    if not current_blackboard.get_in_environment(GENERAL_CLEANING, False):
        current_blackboard.set_in_environment(GENERAL_CLEANING, True)
        gui_objects["general_cleaning_btn"].update_colors(color_dict["GREEN"])
        gui_objects["general_cleaning_btn"].button_text_surf = font.render('General Clean: On ', True, (20, 20, 20))
    else:
        current_blackboard.set_in_environment(GENERAL_CLEANING, False)
        gui_objects["general_cleaning_btn"].update_colors(color_dict["RED"])
        gui_objects["general_cleaning_btn"].button_text_surf = font.render('General Clean: Off', True, (20, 20, 20))

def draw_battery():
    # Battery container
    battery_rect = pg.Rect(0, TOP_BAR_HEIGHT, BATTERY_WIDTH, SCREEN_HEIGHT - TOP_BAR_HEIGHT)

    pg.draw.rect(screen, color_dict["DARK_GRAY"], battery_rect)

    # Battery level
    battery_level = current_blackboard.get_in_environment(BATTERY_LEVEL, 0)
    level_height = ((SCREEN_HEIGHT - TOP_BAR_HEIGHT) * (battery_level / 100))
    level_rect = pg.Rect(4, TOP_BAR_HEIGHT + (SCREEN_HEIGHT - TOP_BAR_HEIGHT - level_height), BATTERY_WIDTH - 8, level_height)

    # Color based on level
    if battery_level > 60:
        color = color_dict["GREEN"]
    elif battery_level > 30:
        color = color_dict["ORANGE"]
    else:
        color = color_dict["RED"]

    # Draw the battery
    pg.draw.rect(screen, color, level_rect)

    # Battery percentage
    text_surface = font.render(f"{int(battery_level)}%", True, color_dict["BLACK"])
    text_rect = text_surface.get_rect()
    # Rotate text
    text_surface = pg.transform.rotate(text_surface, 90)
    text_rect = text_surface.get_rect(center=(BATTERY_WIDTH // 2, SCREEN_HEIGHT - (level_height // 2)))
    screen.blit(text_surface, text_rect)

def fit_gui_elements():
    # SCREEN_WIDTH
    border_size = 4
    current_x = border_size
    for elem in gui_objects:
        if gui_objects[elem] == gui_objects["speed_slider"]:
            gui_objects[elem].x = SCREEN_WIDTH - gui_objects[elem].width - (border_size * 2)
        else:
            gui_objects[elem].x = current_x
            print(f"placing at {current_x}")
            current_x += gui_objects[elem].width + border_size
        gui_objects[elem].y = border_size
        gui_objects[elem].height = TOP_BAR_HEIGHT - (border_size * 2)

# GUI Elements
ELEM_HEIGHT = TOP_BAR_HEIGHT - (4 * 2)
play_btn = Button(name="is_playing", x=4, y=4, width=75, height=ELEM_HEIGHT,
                  color=color_dict["RED"], button_text='Paused', on_click_function=play_pause)
step_btn = Button(name="step_btn", x=83, y=4, width=30, height=ELEM_HEIGHT,
                  color=color_dict["BLUE"], button_text='>>', on_click_function=step_update)
add_dirt_btn = Button(name="add_dirt_btn", x=117, y=4, width=80, height=ELEM_HEIGHT,
                  color=color_dict["BROWN"], button_text='Add Dirt', on_click_function=add_dirt)
spot_cleaning_btn = Button(name="spot_cleaning_btn", x=201, y=4, width=130, height=ELEM_HEIGHT,
                  color=color_dict["RED"], button_text='Spot Clean: Off', on_click_function=spot_cleaning)
general_cleaning_btn = Button(name="general_cleaning_btn", x=335, y=4, width=170, height=ELEM_HEIGHT,
                  color=color_dict["RED"], button_text='General Clean: Off', on_click_function=general_cleaning)
speed_slider = Slider(name="speed_slider", x=509, y=4, width=SCREEN_WIDTH - 509 - 4, puck_width=20, height=ELEM_HEIGHT, value=simulation_speed,
                      v_min=5, v_max=2000, color=color_dict["BLUE"], l_text='Faster', r_text='Slower')
# fit_gui_elements()





def update_simulation():
    # Evaluate the behavior tree
    result = robot_behavior.evaluate(current_blackboard)
    print(result)

    # Rescan for Dirt and Vacuum
    robot.clean_check_dirt()

    # Update the battery level
    battery_level = current_blackboard.get_in_environment(BATTERY_LEVEL, 0)
    battery_level -= 0.1
    if current_blackboard.get_in_environment(VACUUMING, False):
        battery_level -= 0.3
    current_blackboard.set_in_environment(BATTERY_LEVEL, battery_level)


    # if random.random() < 0.05:
    #     # Add a random spot of dirt
    #     x = random.randint(0, GRID_DIM_X - 1)
    #     y = random.randint(0, GRID_DIM_Y - 1)
    #     color = random.randint(50, 150)
    #     cells[x][y] = (color, color, color)

robot = Roomba()

# Game Loop
running = True
time_elapsed_since_update = 0
while running:
    dt = clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if is_playing:
        time_elapsed_since_update += dt
        if time_elapsed_since_update > simulation_speed[0]:  # 17ms is roughly 60fps
            update_simulation()
            time_elapsed_since_update = 0


    screen.fill((0, 0, 0))

    # Draw Floor
    screen.blit(surf, (0 + BATTERY_WIDTH, 0 + TOP_BAR_HEIGHT))
    # Draw GUI
    for gui_object in gui_objects:
        gui_objects[gui_object].process()
    # Draw Game Objects
    for game_object in game_objects:
        game_object.process()

    draw_battery()


    pg.display.update()

pg.quit()

#
# done = False
# while not done:
#     # Each cycle in this while-loop is equivalent to 1 second time
#
#     # Step 1: Change the environment
#     #   - Change the battery level (charging or depleting)
#     #   - Simulate the response of the dusty spot sensor
#     #   - Simulate user input commands
#
#     # Step 2: Evaluating the behavior tree
#
#     # Print the state of the tree nodes before the evaluation
#     # print('BEFORE -------------------------------------------------------------------------')
#     # btl.print_states(current_blackboard)
#     # print('================================================================================')
#
#     result = robot_behavior.evaluate(current_blackboard)
#
#     # Print the state of the tree nodes before the evaluation
#     # print('AFTER --------------------------------------------------------------------------')
#     # btl.print_states(current_blackboard)
#     # print('================================================================================')
#
#     # Step 3: Determine if your solution must terminate
#     # done = True
#     user_input = input("Waiting: ")
#     if user_input == 'q':
#         done = True