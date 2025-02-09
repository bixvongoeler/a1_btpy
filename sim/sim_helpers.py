import pygame as pg
import numpy as np

from .sim_config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, HOME_SIZE
from .sim_globals import *


def redraw_grid(cells: np.ndarray, divided: bool=False) -> pg.Surface:
    """
    Redraws the grid on the given surface updating to reflect the current state of the cells.

    Args:
        cells (np.ndarray): The current state of the cells.
        divided (bool, optional): Whether to add grid lines between cells. Defaults to False.
    Returns:
        pg.Surface: The updated grid surface.
    """

    # # Overwrite the home area
    # for x in range(GRID_DIM_X - HOME_SIZE, GRID_DIM_X):
    #     for y in range(GRID_DIM_Y - HOME_SIZE, GRID_DIM_Y):
    #             cells[x][y] = color_dict["DARK_GREEN"]

    # Create new surface
    new_surf = pg.Surface((GRID_DIM_X, GRID_DIM_Y))

    # Draw the grid onto surface
    pg.surfarray.blit_array(new_surf, cells)

    # Add small gaps between cells
    if divided:
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if y % CELL_SIZE == 0:
                    new_surf.set_at((x, y), (170, 140, 100))

    # Transform to screen size
    return pg.transform.scale(new_surf, (GRID_WIDTH, GRID_HEIGHT))

