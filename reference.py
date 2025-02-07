import pygame
import random
import sys


class VacuumSimulation:
    def __init__(self):
        pygame.init()

        # Constants
        self.CELL_SIZE = 15
        self.GRID_SIZE = 40
        self.BATTERY_WIDTH = 30
        self.TOP_BAR_HEIGHT = 40

        # Calculate window dimensions
        self.window_width = self.BATTERY_WIDTH + (self.CELL_SIZE * self.GRID_SIZE)
        self.window_height = self.TOP_BAR_HEIGHT + (self.CELL_SIZE * self.GRID_SIZE)

        # Initialize window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Robot Vacuum Simulator")

        # Colors
        self.WOOD_COLOR = (210, 180, 140)  # Constant floor color
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (76, 175, 80)
        self.ORANGE = (255, 165, 0)
        self.RED = (244, 67, 54)

        # Initialize simulation state
        self.grid_data = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.battery_level = 100
        self.is_running = False
        self.is_dragging_battery = False
        self.spot_selection_mode = False
        self.simulation_speed = 5  # 1-10 scale
        self.clock = pygame.time.Clock()

        # Button rectangles
        self.play_btn = pygame.Rect(10, 10, 60, 20)
        self.step_btn = pygame.Rect(80, 10, 60, 20)
        self.add_dirt_btn = pygame.Rect(150, 10, 60, 20)
        self.spot_clean_btn = pygame.Rect(220, 10, 70, 20)
        self.speed_slider_rect = pygame.Rect(300, 15, 100, 10)
        self.speed_handle = pygame.Rect(345, 12, 10, 16)

        # Font
        self.font = pygame.font.Font(None, 24)

    def draw_button(self, rect, text, color=(200, 200, 200)):
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_battery(self):
        # Battery container
        battery_rect = pygame.Rect(0, self.TOP_BAR_HEIGHT, self.BATTERY_WIDTH,
                                   self.window_height - self.TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, (200, 200, 200), battery_rect)

        # Battery level
        level_height = ((self.window_height - self.TOP_BAR_HEIGHT) * (self.battery_level / 100))
        level_rect = pygame.Rect(4, self.TOP_BAR_HEIGHT + (self.window_height - self.TOP_BAR_HEIGHT - level_height),
                                 self.BATTERY_WIDTH - 8, level_height)

        # Color based on level
        if self.battery_level > 60:
            color = self.GREEN
        elif self.battery_level > 30:
            color = self.ORANGE
        else:
            color = self.RED

        pygame.draw.rect(self.screen, color, level_rect)

        # Battery percentage
        text_surface = self.font.render(f"{int(self.battery_level)}%", True, self.BLACK)
        text_rect = text_surface.get_rect()
        # Rotate text
        text_surface = pygame.transform.rotate(text_surface, 90)
        text_rect = text_surface.get_rect(center=(self.BATTERY_WIDTH // 2,
                                                  self.window_height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = self.BATTERY_WIDTH + (col * self.CELL_SIZE)
                y = self.TOP_BAR_HEIGHT + (row * self.CELL_SIZE)
                rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)

                if self.grid_data[row][col] == 1:  # Dirty cell
                    # Randomize dirt color
                    dirt_r = random.randint(100, 120)
                    dirt_g = random.randint(90, 110)
                    dirt_b = random.randint(80, 100)
                    pygame.draw.rect(self.screen, (dirt_r, dirt_g, dirt_b), rect)
                else:  # Clean cell
                    pygame.draw.rect(self.screen, self.WOOD_COLOR, rect)

                pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)

    def add_random_dirt(self):
        num_clusters = random.randint(3, 8)
        for _ in range(num_clusters):
            center_x = random.randint(0, self.GRID_SIZE - 1)
            center_y = random.randint(0, self.GRID_SIZE - 1)

            radius = random.randint(1, 3)
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if random.random() < 0.7:
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
                            self.grid_data[y][x] = 1

    def draw_spot_preview(self, pos):
        if pos:
            grid_x = (pos[0] - self.BATTERY_WIDTH) // self.CELL_SIZE
            grid_y = (pos[1] - self.TOP_BAR_HEIGHT) // self.CELL_SIZE

            if 0 <= grid_x < self.GRID_SIZE and 0 <= grid_y < self.GRID_SIZE:
                center_x = self.BATTERY_WIDTH + (grid_x * self.CELL_SIZE) + (self.CELL_SIZE // 2)
                center_y = self.TOP_BAR_HEIGHT + (grid_y * self.CELL_SIZE) + (self.CELL_SIZE // 2)
                radius = int(2.5 * self.CELL_SIZE)
                pygame.draw.circle(self.screen, self.BLUE, (center_x, center_y), radius, 2)

    def update_simulation(self):
        if self.is_running:
            # Example: clean a random cell
            row = random.randint(0, self.GRID_SIZE - 1)
            col = random.randint(0, self.GRID_SIZE - 1)
            self.grid_data[row][col] = 0

    def run(self):
        last_update = pygame.time.get_ticks()
        update_interval = 1000 // self.simulation_speed

        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check button clicks
                    if self.play_btn.collidepoint(mouse_pos):
                        self.is_running = not self.is_running
                    elif self.step_btn.collidepoint(mouse_pos) and not self.is_running:
                        self.update_simulation()
                    elif self.add_dirt_btn.collidepoint(mouse_pos):
                        self.add_random_dirt()
                    elif self.spot_clean_btn.collidepoint(mouse_pos):
                        self.spot_selection_mode = not self.spot_selection_mode

                    # Check battery click
                    battery_rect = pygame.Rect(0, self.TOP_BAR_HEIGHT, self.BATTERY_WIDTH,
                                               self.window_height - self.TOP_BAR_HEIGHT)
                    if battery_rect.collidepoint(mouse_pos):
                        self.is_dragging_battery = True

                    # Speed slider
                    if self.speed_slider_rect.collidepoint(mouse_pos):
                        self.simulation_speed = (mouse_pos[0] - self.speed_slider_rect.x) // 10
                        self.simulation_speed = max(1, min(10, self.simulation_speed))
                        update_interval = 1000 // self.simulation_speed

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging_battery = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.is_dragging_battery:
                        mouse_y = pygame.mouse.get_pos()[1]
                        total_height = self.window_height - self.TOP_BAR_HEIGHT
                        rel_y = mouse_y - self.TOP_BAR_HEIGHT
                        self.battery_level = 100 - (rel_y / total_height * 100)
                        self.battery_level = max(0, min(100, self.battery_level))

            # Update simulation based on speed
            if self.is_running and current_time - last_update >= update_interval:
                self.update_simulation()
                last_update = current_time

            # Draw everything
            self.screen.fill(self.WHITE)

            # Draw buttons
            self.draw_button(self.play_btn, "▶ Play" if not self.is_running else "⏸ Pause")
            self.draw_button(self.step_btn, "Step")
            self.draw_button(self.add_dirt_btn, "Add Dirt")
            self.draw_button(self.spot_clean_btn, "Spot Clean",
                             (150, 150, 255) if self.spot_selection_mode else (200, 200, 200))

            # Draw speed slider
            pygame.draw.rect(self.screen, (200, 200, 200), self.speed_slider_rect)
            handle_x = self.speed_slider_rect.x + (self.simulation_speed - 1) * 10
            self.speed_handle.x = handle_x
            pygame.draw.rect(self.screen, (100, 100, 100), self.speed_handle)

            # Draw simulation elements
            self.draw_battery()
            self.draw_grid()

            # Draw spot preview if in spot selection mode
            if self.spot_selection_mode:
                self.draw_spot_preview(pygame.mouse.get_pos())

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    simulation = VacuumSimulation()
    simulation.run()