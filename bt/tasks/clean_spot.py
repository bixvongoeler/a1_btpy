import bt_library as btl
from ..globals import ROBOT_POSITION, VACUUMING, SPOT_CLEANING_POSITION
import math


class CleanSpot(btl.Task):
    """
    Implementation of the Task "Clean Spot" with improved circular movement.
    The robot moves in a circle around the spot with a specified radius.
    """

    def __init__(self, radius=3):
        """
        Initialize the CleanSpot task.

        Args:
            radius (int): Radius of the circular cleaning pattern (default: 1)
        """
        super().__init__()
        self.radius = radius
        self.current_angle = 0  # Track the current angle for circular movement

    def get_target_position(self, spot_pos, angle):
        """
        Calculate the target position on the circle based on the current angle.

        Args:
            spot_pos (list): Center position [x, y]
            angle (float): Current angle in radians

        Returns:
            list: Target position (x, y)
        """
        x = spot_pos[0] + round(self.radius * math.cos(angle))
        y = spot_pos[1] + round(self.radius * math.sin(angle))
        return [x, y]

    @staticmethod
    def get_next_move(current_pos, target_pos):
        """
        Determine the next move to reach the target position.

        Args:
            current_pos (list): Current position [x, y]
            target_pos (list): Target position [x, y]

        Returns:
            tuple: (dx, dy) representing the movement direction
        """
        dx = 0
        dy = 0

        if current_pos[0] < target_pos[0]:
            dx = 1
        elif current_pos[0] > target_pos[0]:
            dx = -1

        if current_pos[1] < target_pos[1]:
            dy = 1
        elif current_pos[1] > target_pos[1]:
            dy = -1

        return [dx, dy]

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        """
        Execute the circular cleaning pattern around the spot.
        """
        self.print_message('Cleaning Spot')
        blackboard.set_in_environment(VACUUMING, True)

        # Get current positions
        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
        spot_pos = blackboard.get_in_environment(SPOT_CLEANING_POSITION, None)

        if robot_pos is None or spot_pos is None:
            return self.report_failed(blackboard)

        # If at spot center, move to start of circle
        if robot_pos[0] == spot_pos[0] and robot_pos[1] == spot_pos[1]:
            robot_pos[1] -= self.radius  # Move up to start position
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            self.current_angle = -math.pi / 2  # Start at top of circle
            return self.report_succeeded(blackboard)

        # Calculate target position on circle
        target_pos = self.get_target_position(spot_pos, self.current_angle)

        # If at target position, update angle for next position
        if robot_pos[0] == target_pos[0] and robot_pos[1] == target_pos[1]:
            self.current_angle = (self.current_angle + math.pi / 4) % (2 * math.pi)
            target_pos = self.get_target_position(spot_pos, self.current_angle)

        # Get next move direction
        dx, dy = self.get_next_move(robot_pos, target_pos)

        # Update position
        if dx != 0:
            robot_pos[0] += dx
            print("Move", "Right" if dx > 0 else "Left")
        elif dy != 0:
            robot_pos[1] += dy
            print("Move", "Down" if dy > 0 else "Up")

        blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
        return self.report_succeeded(blackboard)