#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class GoHome(btl.Task):
    """
    Implementation of the Task "Go Home".
    """

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Going Home')

        blackboard.set_in_environment(VACUUMING, False)

        # Recall Spot Path
        path_home = blackboard.get_in_environment(HOME_PATH, None)
        if path_home is None:
            self.print_message('Home path not found')
            return self.report_failed(blackboard)

        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)

        # Go To Spot
        dx, dy = self.get_next_move(robot_pos, path_home)

        # Check if we are at the spot
        if dx == 0 and dy == 0:
            blackboard.set_in_environment(HOME_PATH, None)
            return self.report_succeeded(blackboard)

        # Update position
        if dx != 0:
            robot_pos[0] += dx
        if dy != 0:
            robot_pos[1] += dy

        blackboard.set_in_environment(ROBOT_DIRECTION, (dx, dy))

        # Update Blackboard
        blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
        blackboard.set_in_environment(HOME_PATH, (path_home[0] - dx, path_home[1] - dy))
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