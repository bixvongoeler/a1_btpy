import math
import random
import numpy as np

from sim import sim_globals
from sim.sim_config import GRID_DIM_X, GRID_DIM_Y
from sim.sim_globals import cells
from sim.sim_helpers import redraw_grid

def add_dirt(num_min=5, num_max=8, radius_min=8, radius_max=16):
    num_clusters = random.randint(num_min, num_max)
    for _ in range(num_clusters):
        # Choose a random center point for the cluster
        center_x = random.randint(0, GRID_DIM_X - 1)
        center_y = random.randint(0, GRID_DIM_Y - 1)

        # Add dirt in a small radius around the center
        radius = random.randint(radius_min, radius_max)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x = center_x + dx
                y = center_y + dy
                if not (0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y):
                    continue
                distance = dx ** 2 + dy ** 2
                radius_sqr = radius ** 2
                distance_scaled = distance ** 1.1
                # Add some randomness to the cluster shape
                if (random.random() * 2) < distance_scaled / radius_sqr:
                    continue
                # Otherwise continue
                if random.random() < 0.8:  # 70% chance to add dirt in radius
                    offset_color = random.randint(180, 230)
                    dirt_color = (offset_color, offset_color, offset_color)
                    cells[x][y] = dirt_color
    sim_globals.grid_surf = redraw_grid(cells)


def add_uniform_dirt(grey_intensity=0.05):
    random_mask = np.random.random(cells.shape[:-1]) < 0.01  # Adjust 0.5 to control density
    random_mask = np.stack([random_mask] * 3, axis=-1)  # Expand to match RGB channels

    # Create base grey mask
    grey = np.ones_like(cells)
    grey[:, :, :] = (176, 171, 164)

    # Apply grey effect only where random_mask is True
    cells[:] = np.where(random_mask,
                        (1 - grey_intensity) * cells + grey_intensity * grey,
                        cells)

    # Ensure values stay within valid RGB range (0-255)
    np.clip(cells, 0, 255, out=cells)

    # Convert back to integer type if needed
    cells[:] = cells.astype(np.uint8)
    sim_globals.grid_surf = redraw_grid(cells)


def add_dirt_at(i, j, radius, is_spot=True):
    # Add dirt in a small radius around the center
    radius = math.floor(radius)
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            x = i + dx
            y = j + dy
            if not (0 <= x < GRID_DIM_X and 0 <= y < GRID_DIM_Y):
                continue
            distance = (dx ** 2 + dy ** 2) ** (1 / 2)

            # Add some randomness to the cluster shape
            if distance != 0 and (random.random() * 1.2 * radius) < distance ** 1.1:
                continue
            # Otherwise continue
            if random.random() < 0.9:  # 70% chance to add dirt in radius
                offset_color = random.randint(150, 180)
                dirt_color = (255, offset_color, offset_color)
                cells[x][y] = dirt_color
    sim_globals.grid_surf = redraw_grid(cells)
