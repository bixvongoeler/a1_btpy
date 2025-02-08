import bt_library as btl
from ..globals import *
import math
import random


class CleanFloor(btl.Task):
    """
    Implementation of the Task "Clean Spot" with improved circular movement.
    """
    @staticmethod
    def calc_new_cleaning_route(room_dimensions, robot_radius):
        need_to_clean = []
        for i in range(round(robot_radius), math.ceil(room_dimensions[0] - 1 - robot_radius), round(robot_radius * 4)):
            for j in range(math.ceil(robot_radius), math.floor(room_dimensions[1] - 1 - robot_radius), round(robot_radius)):
                need_to_clean.append([i, j])
            for j in range(math.floor(room_dimensions[1] - 1 - robot_radius), math.ceil(robot_radius), -round(robot_radius)):
                if (i + round(3 * robot_radius)) < room_dimensions[0]:
                    need_to_clean.append([i + round(2 * robot_radius), j])
                else:
                    need_to_clean.append([math.floor(room_dimensions[0] - 1 - robot_radius), j])
        need_to_clean.append([room_dimensions[0] // 2, room_dimensions[1] // 2])
        return need_to_clean

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
        dx = max(-1, min(1, target_pos[0] - current_pos[0]))
        dy = max(-1, min(1, target_pos[1] - current_pos[1]))
        return [dx, dy]

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        """
        Systematically clean the floor.
        """
        self.print_message('Cleaning Floor')
        blackboard.set_in_environment(VACUUMING, True)

        # Get current positions
        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
        robot_radius = blackboard.get_in_environment(MY_RADIUS, None)
        room_dimensions = blackboard.get_in_environment(ROOM_DIMENSIONS, None)
        need_to_clean = blackboard.get_in_environment(NEED_TO_CLEAN, None)
        if need_to_clean is None:
            need_to_clean = self.calc_new_cleaning_route(room_dimensions, robot_radius)

        # Get Next Position in the cleaning route
        target_pos = need_to_clean[0]

        # Calculate next move
        dx, dy = self.get_next_move(robot_pos, target_pos)

        if dx == 0 and dy == 0:
            need_to_clean.pop(0)
            dx, dy = self.get_next_move(robot_pos, target_pos)

        robot_pos[0] += dx
        robot_pos[1] += dy
        blackboard.set_in_environment(ROBOT_POSITION, robot_pos)

        # End Task if no more cleaning to do
        if len(need_to_clean) == 0:
            blackboard.set_in_environment(NEED_TO_CLEAN, None)
            return self.report_failed(blackboard)
        else:
            blackboard.set_in_environment(NEED_TO_CLEAN, need_to_clean)
            return self.report_running(blackboard)
