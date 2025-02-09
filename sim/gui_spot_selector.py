import pygame as pg

from bt import SPOT_CLEANING_POSITION, SPOT_CLEANING, SPOT_RADIUS, SPOT_CURRENT_RADIUS
from .sim_config import GRID_DIM_X, GRID_DIM_Y, CELL_SIZE, BATTERY_WIDTH, TOP_BAR_HEIGHT, ROBOT_RADIUS
from .sim_colors import color_dict


class SpotSelector:
    def __init__(self, screen, robot_radius, font, current_blackboard, game_objects, gui_objects, on_click_function=None):
        self.radius = ROBOT_RADIUS * 2.5
        self.color = color_dict["BLUE"]
        self.active = True
        self.screen = screen
        self.font = font
        self.robot_radius = robot_radius
        self.on_click_function = on_click_function
        self.current_blackboard = current_blackboard
        self.gui_objects = gui_objects
        self.game_objects = game_objects

    def process(self):
        global current_blackboard
        if self.active:
            pg.draw.circle(self.screen, self.color, pg.mouse.get_pos(), self.radius * CELL_SIZE, 3)
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                x = (pg.mouse.get_pos()[0] - BATTERY_WIDTH) // CELL_SIZE
                y = (pg.mouse.get_pos()[1] - TOP_BAR_HEIGHT) // CELL_SIZE
                if 0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y:
                    self.current_blackboard.set_in_environment(SPOT_CLEANING_POSITION, (x, y))
                    self.current_blackboard.set_in_environment(SPOT_CLEANING, True)
                    self.current_blackboard.set_in_environment(SPOT_RADIUS, self.radius)
                    self.current_blackboard.set_in_environment(SPOT_CURRENT_RADIUS, self.robot_radius)
                    self.on_click_function(x, y, self.radius)
                    print(f"Dusty Spot: x:{x}, y:{y}")
                    self.active = False
        else:
            if not self.current_blackboard.get_in_environment(SPOT_CLEANING, False):
                self.gui_objects["spot_cleaning_btn"].update_colors(color_dict["RED"])
                self.gui_objects["spot_cleaning_btn"].button_text_surf = self.font.render('Spot Clean: Off', True, (20, 20, 20))
                self.game_objects.remove(self)
                del self
