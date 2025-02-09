import math

import pygame as pg
import numpy as np

import sim.sim_globals
from bt import ROBOT_POSITION, VACUUMING, DUSTY_SPOT_SENSOR, ROBOT_DIRECTION
from .sim_config import GRID_DIM_X, GRID_DIM_Y, CELL_SIZE, BATTERY_WIDTH, TOP_BAR_HEIGHT, ROBOT_RADIUS
from .sim_colors import color_dict
from .sim_helpers import redraw_grid

class Roomba:
    def __init__(self, current_blackboard, game_objects, screen, cells):
        self.color = color_dict["BLACK"]
        self.head_color = (50, 50, 50)
        self.radius = ROBOT_RADIUS
        self.head_radius = ROBOT_RADIUS * 0.8
        self.blackboard = current_blackboard
        self.x = self.blackboard.get_in_environment(ROBOT_POSITION, None)[0]
        self.y = self.blackboard.get_in_environment(ROBOT_POSITION, None)[1]
        self.rendered_x = None
        self.rendered_y = None
        self.screen = screen
        self.cells = cells
        self.image = pg.image.load("sim/assets/roomba_clean_96.png")
        self.angle = 0
        # self.image = pg.transform.scale(self.image, (96, 96))

        assert (self.x is not None and self.y is not None), "Robot position not found"
        game_objects.append(self)

    @staticmethod
    def average_angles(prev_angle, new_angle):
        """
        Average two angles, handling the wrap-around at 360 degrees correctly.
        """
        # Convert angles to radians
        a1 = math.radians(prev_angle)
        a2 = math.radians(new_angle)

        # Apply non-linear scaling (can adjust power to change curve)
        # Using power of 2 for quadratic scaling

        factor = round(1 + 15 * ((sim.sim_globals.simulation_speed[0] + 1) / 100))

        # Convert to vectors and average
        x = ((math.cos(a1) * factor) + math.cos(a2)) / (factor + 1)
        y = ((math.sin(a1) * factor) + math.sin(a2)) / (factor + 1)

        # Convert back to angle
        avg_angle = math.degrees(math.atan2(y, x))

        # Normalize to 0-360
        return (avg_angle + 360) % 360
    @staticmethod
    def get_smooth_position(current_grid_pos, prev_rendered_pos, cell_size, is_x, max_lag_pixels=8):
        """
        Smoothly interpolate between grid positions while limiting maximum lag.

        Args:
            current_grid_pos: Current integer grid position
            prev_rendered_pos: Previous rendered pixel position
            cell_size: Size of each grid cell in pixels
            is_x: Boolean indicating if the position is on the x-axis
            max_lag_pixels: Maximum allowed lag in pixels
        """
        # Convert grid position to target pixel position (center of cell)
        if is_x:
            target_pixels = current_grid_pos * cell_size + BATTERY_WIDTH + cell_size // 2
        else:
            target_pixels = current_grid_pos * cell_size + TOP_BAR_HEIGHT + cell_size // 2

        if prev_rendered_pos is None:
            return target_pixels

        # Calculate difference between current target and previous position
        diff = target_pixels - prev_rendered_pos

        # If difference is within max lag, do smooth interpolation
        if abs(diff) <= max_lag_pixels:
            # Use 0.2 as interpolation factor (can adjust for different smoothing)
            return prev_rendered_pos + (diff * 0.25)
        else:
            # If lag is too high, snap to maximum allowed lag position
            return target_pixels - (max_lag_pixels * (1 if diff > 0 else -1))

    def get_smooth_rotation_45(self, new_angle_vec, prev_angle):
        """
        Convert dx and dy to rotation angle in 45-degree increments,
        smoothly transitioning from the previous angle.
        """
        # Calculate the base angle
        new_angle = math.degrees(math.atan2(-new_angle_vec[0], -new_angle_vec[1]))
        new_angle = (new_angle + 360) % 360

        # new_angle = round(new_angle / 15) * 15

        # Average with previous angle
        return self.average_angles(prev_angle, new_angle)

    def process(self):
        grid_x = self.blackboard.get_in_environment(ROBOT_POSITION, None)[0]
        grid_y = self.blackboard.get_in_environment(ROBOT_POSITION, None)[1]
        assert (self.x is not None and self.y is not None), "Robot position not found"
        rotation = self.blackboard.get_in_environment(ROBOT_DIRECTION, None)
        self.angle = self.get_smooth_rotation_45(rotation, self.angle)
        self.rendered_x = self.get_smooth_position(grid_x, self.rendered_x, CELL_SIZE, True)
        self.rendered_y = self.get_smooth_position(grid_y, self.rendered_y, CELL_SIZE, False)

        rotated_img = pg.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_img.get_rect()
        rotated_rect.center = (
            self.rendered_x,  # Already in pixels
            self.rendered_y  # Already in pixels
        )
        self.screen.blit(rotated_img, rotated_rect)
        # pg.draw.circle(self.screen, self.color, (self.x * CELL_SIZE + BATTERY_WIDTH + CELL_SIZE // 2,
        #                                     self.y * CELL_SIZE + TOP_BAR_HEIGHT + CELL_SIZE // 2),
        #                self.radius * CELL_SIZE)
        # pg.draw.circle(self.screen, self.head_color, (self.x * CELL_SIZE + BATTERY_WIDTH + CELL_SIZE // 2,
        #                                          self.y * CELL_SIZE + TOP_BAR_HEIGHT + CELL_SIZE // 2),
        #                self.head_radius * CELL_SIZE)

    def clean_check_dirt(self):
        self.x = self.blackboard.get_in_environment(ROBOT_POSITION, None)[0]
        self.y = self.blackboard.get_in_environment(ROBOT_POSITION, None)[1]
        assert (self.x is not None and self.y is not None), "Robot position not found"

        # Create a grid of coordinates
        x_coords, y_coords = np.ogrid[0:GRID_DIM_X, 0:GRID_DIM_Y]

        # Calculate distances from robot position using broadcasting
        distances = np.sqrt((x_coords - self.x) ** 2 + (y_coords - self.y) ** 2)

        # Create mask for cells within robot's radius
        radius_mask = distances <= self.radius

        # Sum RGB values for each cell (axis 2 is the RGB dimension)
        color_sums = np.sum(self.cells, axis=2)

        # Count dirt within radius
        dirt_mask = (color_sums > 540) & radius_mask
        found_dirt = np.sum(dirt_mask)

        # Update cells if vacuuming
        if self.blackboard.get_in_environment(VACUUMING, False):
            # Only update cells within radius
            wood_color = np.array(color_dict["WOOD_COLOR"])
            self.cells[radius_mask] = wood_color
            sim.sim_globals.grid_surf = redraw_grid(self.cells)

        # Update dusty spot sensor
        self.blackboard.set_in_environment(DUSTY_SPOT_SENSOR, found_dirt >= 8)
