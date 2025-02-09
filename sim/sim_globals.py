import numpy as np
import pygame as pg

import bt_library as btl
from sim.sim_colors import color_dict
from sim.sim_config import GRID_DIM_X, GRID_DIM_Y

grid_surf = pg.Surface((GRID_DIM_X, GRID_DIM_Y))
cells = np.ndarray((GRID_DIM_X, GRID_DIM_Y, 3), dtype=int)
cells[:, :, :] = color_dict["WOOD_COLOR"]

simulation_speed = [17]
is_playing = False
gui_objects = {}
game_objects = []
screen = None
font = None
big_font = None
symbol_font = None
current_blackboard = btl.Blackboard()
