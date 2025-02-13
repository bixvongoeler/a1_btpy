#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import SPOT_CLEANING_PATH, SPOT_CLEANING_POSITION, ROBOT_POSITION, ROBOT_DIRECTION


class GoToSpot(btl.Task):
    """
    Implementation of the Task "Go Home".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Going To Spot')

        # Recall Spot Path
        path_to_spot = blackboard.get_in_environment(SPOT_CLEANING_PATH, None)
        if path_to_spot is None:
            self.print_message('Spot path not found')
            return self.report_failed(blackboard)

        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)

        # Go To Spot
        dx, dy = self.get_next_move(robot_pos, path_to_spot)

        # Check if we are at the spot
        if dx == 0 and dy == 0:
            blackboard.set_in_environment(SPOT_CLEANING_PATH, None)
            return self.report_succeeded(blackboard)

        # Update position
        if dx != 0:
            robot_pos[0] += dx
        if dy != 0:
            robot_pos[1] += dy

        blackboard.set_in_environment(ROBOT_DIRECTION, (dx, dy))

        # Update Blackboard
        blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
        blackboard.set_in_environment(SPOT_CLEANING_PATH, (path_to_spot[0] - dx, path_to_spot[1] - dy))
        return self.report_running(blackboard)

    @staticmethod
    def get_next_move(current_pos, path_to_spot):
        """
        Determine the next move to reach the target position.
        Args:
            current_pos (list): Current position [x, y]
            path_to_spot (list): Path to target [x, y]
        Returns:
            list: [dx, dy] representing the movement direction
        """
        dx = max(-1, min(1, path_to_spot[0]))
        dy = max(-1, min(1, path_to_spot[1]))
        return [dx, dy]