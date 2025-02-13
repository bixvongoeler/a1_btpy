import bt_library as btl
from ..globals import *
import math
import random


class CleanSpot(btl.Task):
    """
    Implementation of the Task "Clean Spot" with improved circular movement.
    The robot moves in a circle around the spot with a specified radius.
    """
    @staticmethod
    def get_target_position(spot_pos, angle, current_radius, room_dimensions, robot_radius):
        """
        Calculate the target position on the circle based on the current angle.

        Args:
            spot_pos (list): Center position [x, y]
            angle (float): Current angle in radians
            current_radius (float): Current radius of the circle
            room_dimensions (list): Dimensions of the room [width, height]
            robot_radius (float): Radius of the robot

        Returns:
            list: Target position (x, y)
        """
        x = max(math.ceil(robot_radius), min((spot_pos[0] + round(current_radius * math.cos(angle))), room_dimensions[0] - 1 - math.ceil(robot_radius)))
        y = max(math.ceil(robot_radius), min((spot_pos[1] + round(current_radius * math.sin(angle))), room_dimensions[1] - 1 - math.ceil(robot_radius)))
        return [x, y]

    @staticmethod
    def get_next_move(current_pos, target_pos):
        """
        Determine the next move to reach the target position.

        Args:
            current_pos (list): Current position [x, y]
            target_pos (list): Target position [x, y]

        Returns:
            list: [dx, dy] representing the movement direction
        """
        dx = max(-3, min(3, target_pos[0] - current_pos[0]))
        dy = max(-3, min(3, target_pos[1] - current_pos[1]))
        print(f'Current Position: {current_pos}, Target Position: {target_pos}, dx: {dx}, dy: {dy}')
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
        room_dimensions = blackboard.get_in_environment(ROOM_DIMENSIONS, None)
        robot_radius = blackboard.get_in_environment(MY_RADIUS, None)
        # Get spot parameters
        spot_radius = blackboard.get_in_environment(SPOT_RADIUS, None)
        current_radius = blackboard.get_in_environment(SPOT_CURRENT_RADIUS, None)
        current_angle = blackboard.get_in_environment(SPOT_CURRENT_ANGLE, None)
        if current_angle is None:
            current_angle = 0

        # Calculate target position on circle
        target_pos = self.get_target_position(spot_pos, current_angle, current_radius, room_dimensions, robot_radius)

        # Calculate next move
        dx, dy = self.get_next_move(robot_pos, target_pos)

        # Check if we are at the target position and update angle and radius if so
        if dx == 0 and dy == 0:
            current_angle = (current_angle + math.pi / 16) % (2 * math.pi)
            blackboard.set_in_environment(SPOT_CURRENT_ANGLE, current_angle)
            if current_radius <= spot_radius + 1:
                # current_radius += blackboard.get_in_environment(SPOT_RADIUS, 3) / 80
                current_radius += 0.01 * spot_radius
                blackboard.set_in_environment(SPOT_CURRENT_RADIUS, current_radius)
            target_pos = self.get_target_position(spot_pos, current_angle, current_radius, room_dimensions, robot_radius)
            dx, dy = self.get_next_move(robot_pos, target_pos)

        blackboard.set_in_environment(ROBOT_DIRECTION, (dx, dy))
        # Update position
        blackboard.set_in_environment(ROBOT_POSITION, [robot_pos[0] + dx, robot_pos[1] + dy])
        if current_radius >= spot_radius * 0.8:
            return self.report_succeeded(blackboard)
        else:
            return self.report_running(blackboard)