#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import SPOT_CLEANING_PATH, SPOT_CLEANING_POSITION, ROBOT_POSITION


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

        # Go To Spot
        if self.move_to_spot(blackboard):
            blackboard.set_in_environment(SPOT_CLEANING_PATH, None)
            return self.report_succeeded(blackboard)
        else:
            return self.report_running(blackboard)

    @staticmethod
    def move_to_spot(blackboard: btl.Blackboard) -> bool:
        path_to_spot = blackboard.get_in_environment(SPOT_CLEANING_PATH, None)
        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
        assert path_to_spot is not None
        assert robot_pos is not None
        if path_to_spot[0] > 0:
            print("Move Right")
            robot_pos[0] += 1
            path_to_spot[0] -= 1
            blackboard.set_in_environment(SPOT_CLEANING_PATH, path_to_spot)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_to_spot[0] < 0:
            print("Move Left")
            robot_pos[0] -= 1
            path_to_spot[0] += 1
            blackboard.set_in_environment(SPOT_CLEANING_PATH, path_to_spot)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_to_spot[1] > 0:
            print("Move Down")
            robot_pos[1] += 1
            path_to_spot[1] -= 1
            blackboard.set_in_environment(SPOT_CLEANING_PATH, path_to_spot)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_to_spot[1] < 0:
            print("Move Up")
            robot_pos[1] -= 1
            path_to_spot[1] += 1
            blackboard.set_in_environment(SPOT_CLEANING_PATH, path_to_spot)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        else:
            return True