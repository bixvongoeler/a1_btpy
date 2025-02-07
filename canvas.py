import tkinter as tk
from tkinter import ttk
import random

import bt_library as btl
from bt.globals import BATTERY_LEVEL, GENERAL_CLEANING, SPOT_CLEANING, DUSTY_SPOT_SENSOR, HOME_PATH, CHARGING, X_POS, \
    Y_POS
from bt.robot_behavior import robot_behavior
from bt_library import Blackboard


class SimulationCanvas:
    def __init__(self, root, robot_blackboard: btl.Blackboard()):
        self.root = root
        self.is_running = False
        self.cell_size = 15  # Size of each grid cell
        self.grid_size = 40  # 40x40 grid
        self.spot_selection_mode = False
        self.spot_preview_id = None
        self.battery_level = 100  # Battery level percentage
        self.battery_width = 30  # Width of battery bar
        self.is_dragging_battery = False
        self.robot_blackboard = robot_blackboard

        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create top control bar
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(0, 5))

        # Add play/pause button
        self.play_pause_btn = ttk.Button(self.control_frame, text="▶", width=3, command=self.toggle_simulation)
        self.play_pause_btn.pack(side=tk.LEFT, padx=2)

        # Add step button
        self.step_btn = ttk.Button(self.control_frame, text="→", width=3, command=self.step_simulation)
        self.step_btn.pack(side=tk.LEFT, padx=2)

        # Add dirt button
        self.add_dirt_btn = ttk.Button(self.control_frame, text="Add Dirt", command=self.add_random_dirt)
        self.add_dirt_btn.pack(side=tk.LEFT, padx=2)

        # Add speed slider
        ttk.Label(self.control_frame, text="Speed:").pack(side=tk.LEFT, padx=(10, 2))
        self.speed_slider = ttk.Scale(self.control_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                      command=self.update_speed)
        self.speed_slider.set(5)  # Default speed
        self.speed_slider.pack(side=tk.LEFT, padx=2)

        # Add cleaning mode buttons
        ttk.Separator(self.control_frame, orient='vertical').pack(side=tk.LEFT, padx=10, fill='y')
        self.general_clean_btn = ttk.Button(self.control_frame, text="General Clean", command=self.start_general_clean)
        self.general_clean_btn.pack(side=tk.LEFT, padx=2)

        self.spot_clean_btn = ttk.Button(self.control_frame, text="Spot Clean", command=self.start_spot_selection)
        self.spot_clean_btn.pack(side=tk.LEFT, padx=2)

        # Add status text
        self.status_text = ttk.Label(self.control_frame, text="Status: Paused")
        self.status_text.pack(side=tk.LEFT, padx=10)

        # Create canvas frame to hold both battery and grid
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(pady=5)

        # Create battery canvas
        canvas_height = self.cell_size * self.grid_size
        self.battery_canvas = tk.Canvas(self.canvas_frame, width=self.battery_width,
                                        height=canvas_height, bg='lightgray')
        self.battery_canvas.pack(side=tk.LEFT, padx=(0, 5))

        # Create canvas for grid
        canvas_size = self.cell_size * self.grid_size
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_size,
                                height=canvas_size, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Initialize grid data
        self.grid_data = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Draw initial grid
        self.draw_grid()

        # Bind mouse events for cell editing
        self.canvas.bind('<Button-1>', self.on_cell_click)
        self.canvas.bind('<Motion>', self.on_mouse_move)

        # Bind battery interaction events
        self.battery_canvas.bind('<Button-1>', self.start_battery_drag)
        self.battery_canvas.bind('<B1-Motion>', self.drag_battery)
        self.battery_canvas.bind('<ButtonRelease-1>', self.stop_battery_drag)

        # Draw initial battery
        self.draw_battery()

        # Draw inital Robot
        self.draw_robot()

        # Initialize simulation timer
        self.base_speed = 1000  # Base speed (1 second)
        self.simulation_speed = self.base_speed  # Current speed
        self.timer_id = None



    def draw_grid(self):
        """Draw the grid lines and fill cells based on grid_data"""
        self.canvas.delete('all')

        # Wood floor color (constant)
        wood_color = '#D2B48C'  # Tan/light brown

        # Draw cells
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Fill cell based on state
                if self.grid_data[row][col] == 1:  # Dirty cell
                    # Randomize dirt color for more natural look
                    dirt_r = random.randint(100, 120)
                    dirt_g = random.randint(90, 110)
                    dirt_b = random.randint(80, 100)
                    dirt_color = f'#{dirt_r:02x}{dirt_g:02x}{dirt_b:02x}'
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=dirt_color,
                                                 outline=wood_color)
                else:  # Clean cell
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=wood_color,
                                                 outline='#C4A484')

    def on_cell_click(self, event):
        """Handle mouse clicks on the grid"""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if not 0 <= row < self.grid_size or not 0 <= col < self.grid_size:
            return

        if self.spot_selection_mode:
            # End spot selection mode and print coordinates
            self.spot_selection_mode = False
            print(f"Spot clean selected at coordinates: ({col}, {row})")
            self.status_text.configure(text=f"Status: Spot selected at ({col}, {row})")
            self.spot_clean_btn.configure(state='normal')
            if self.spot_preview_id:
                self.canvas.delete(self.spot_preview_id)
                self.spot_preview_id = None

    def on_mouse_move(self, event):
        """Handle mouse movement for spot selection preview"""
        if self.spot_selection_mode:
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            self.update_spot_preview(row, col)

    def update_spot_preview(self, center_row, center_y):
        """Update the visual preview of the spot cleaning area"""
        if self.spot_preview_id:
            self.canvas.delete(self.spot_preview_id)

        # Calculate the center point in pixels
        center_x = (center_y + 0.5) * self.cell_size
        center_y = (center_row + 0.5) * self.cell_size

        # Draw a circle representing the spot cleaning area
        radius = 2.5 * self.cell_size  # 5x5 cells (2.5 cells radius)
        self.spot_preview_id = self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline='blue', width=2
        )

    def toggle_simulation(self):
        """Toggle between play and pause states"""
        self.is_running = not self.is_running
        if self.is_running:
            self.play_pause_btn.configure(text="⏸")
            self.status_text.configure(text="Status: Running")
            self.run_simulation()
        else:
            self.play_pause_btn.configure(text="▶")
            self.status_text.configure(text="Status: Paused")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

    def step_simulation(self):
        """Advance simulation by one step"""
        if not self.is_running:
            self.update_simulation()

    def run_simulation(self):
        """Run continuous simulation"""
        if self.is_running:
            self.update_simulation()
            self.timer_id = self.root.after(self.simulation_speed, self.run_simulation)

    def draw_battery(self):
        """Draw the battery level indicator"""
        self.battery_canvas.delete('all')
        height = self.battery_canvas.winfo_height()
        width = self.battery_width

        # Draw battery outline
        padding = 4
        self.battery_canvas.create_rectangle(
            padding, padding,
            width - padding, height - padding,
            outline='black', width=2
        )

        # Draw battery level
        level_height = (height - 2 * padding) * (self.battery_level / 100)
        if level_height > 0:
            # Choose color based on battery level
            if self.battery_level > 60:
                color = '#4CAF50'  # Green
            elif self.battery_level > 30:
                color = '#FFA500'  # Orange
            else:
                color = '#F44336'  # Red

            self.battery_canvas.create_rectangle(
                padding, height - padding - level_height,
                         width - padding, height - padding,
                fill=color, outline=color
            )

        # Draw battery percentage text
        text_y = height // 2
        self.battery_canvas.create_text(
            width // 2, text_y,
            text=f"{int(self.battery_level)}%",
            angle=90,
            font=('Arial', 10, 'bold'),
            fill='black'
        )

    def start_battery_drag(self, event):
        """Start dragging the battery level"""
        self.is_dragging_battery = True
        self.update_battery_level(event)

    def drag_battery(self, event):
        """Update battery level while dragging"""
        if self.is_dragging_battery:
            self.update_battery_level(event)

    def stop_battery_drag(self, event):
        """Stop dragging the battery level"""
        self.is_dragging_battery = False

    def update_battery_level(self, event):
        """Update battery level based on mouse position"""
        height = self.battery_canvas.winfo_height()
        padding = 4
        usable_height = height - 2 * padding

        # Calculate battery level from mouse position
        relative_y = height - event.y - padding
        new_level = (relative_y / usable_height) * 100

        # Clamp value between 0 and 100
        self.battery_level = max(0, min(100, new_level))

        # Update display
        self.draw_battery()

    def update_simulation(self):
        """Update the simulation state"""
        # Example update logic (replace with actual robot behavior)
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)
        self.grid_data[row][col] = 0  # Clean a random cell
        self.draw_grid()
        self.draw_robot()

    def start_general_clean(self):
        """Start general cleaning mode (dummy function)"""
        print("Starting general clean - functionality to be implemented")
        self.status_text.configure(text="Status: General cleaning initiated")

    def start_spot_selection(self):
        """Enter spot selection mode"""
        self.spot_selection_mode = True
        self.status_text.configure(text="Status: Select spot to clean")
        self.spot_clean_btn.configure(state='disabled')  # Disable button during selection

    def update_speed(self, value):
        """Update simulation speed based on slider value"""
        # Convert slider value (1-10) to speed
        # Slider value 1 = slowest (base_speed)
        # Slider value 10 = fastest (base_speed/10)
        speed_factor = float(value)
        self.simulation_speed = int(self.base_speed / speed_factor)

        # If simulation is running, restart it with new speed
        if self.is_running:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.run_simulation()

    def add_random_dirt(self):
        """Add dirt in a random pattern"""
        # Add dirt in random clusters
        num_clusters = random.randint(3, 8)
        for _ in range(num_clusters):
            # Choose a random center point for the cluster
            center_x = random.randint(0, self.grid_size - 1)
            center_y = random.randint(0, self.grid_size - 1)

            # Add dirt in a small radius around the center
            radius = random.randint(1, 3)
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    # Add some randomness to the cluster shape
                    if random.random() < 0.7:  # 70% chance to add dirt in radius
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                            self.grid_data[y][x] = 1

        self.draw_grid()

    def draw_robot(self):
        # Wood floor color (constant)
        wood_color = '#D2B48C'  # Tan/light brown

        # Draw Robot
        robot_x = self.robot_blackboard.get_in_environment(X_POS, 0)
        robot_y = self.robot_blackboard.get_in_environment(Y_POS, 0)
        print(f"Robot position: ({robot_x}, {robot_y})")
        x1 = (robot_x - 1) * self.cell_size
        x2 = (robot_x + 2) * self.cell_size
        y1 = (robot_y - 1) * self.cell_size
        y2 = (robot_y + 2) * self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                     fill='#252526',
                                     outline='#1E1E1E')


    @property
    def dirty_cells(self):
        """Return the number of dirty cells"""
        return sum(cell == 1 for row in self.grid_data for cell in row)


# Example usage
# if __name__ == "__main__":
#     tk_root = tk.Tk()
#     tk_root.title("Robot Vacuum Simulator")
#     app = SimulationCanvas(tk_root)
#     tk_root.mainloop()