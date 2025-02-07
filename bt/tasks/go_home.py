#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import HOME_PATH, HOME_POSITION, ROBOT_POSITION


class GoHome(btl.Task):
    """
    Implementation of the Task "Go Home".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Going Home')

        # Recall Home Path
        path_home = blackboard.get_in_environment(HOME_PATH, None)
        if path_home is None:
            self.print_message('Home path not found')
            return self.report_failed(blackboard)

        # Go Home
        if self.move_home(blackboard):
            return self.report_succeeded(blackboard)
        else:
            return self.report_running(blackboard)

    @staticmethod
    def move_home(blackboard: btl.Blackboard) -> bool:
        path_home = blackboard.get_in_environment(HOME_PATH, None)
        robot_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
        assert path_home is not None
        assert robot_pos is not None
        if path_home[0] > 0:
            print("Move Right")
            robot_pos[0] += 1
            path_home[0] -= 1
            blackboard.set_in_environment(HOME_PATH, path_home)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_home[0] < 0:
            print("Move Left")
            robot_pos[0] -= 1
            path_home[0] += 1
            blackboard.set_in_environment(HOME_PATH, path_home)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_home[1] > 0:
            print("Move Down")
            robot_pos[1] += 1
            path_home[1] -= 1
            blackboard.set_in_environment(HOME_PATH, path_home)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        elif path_home[1] < 0:
            print("Move Up")
            robot_pos[1] -= 1
            path_home[1] += 1
            blackboard.set_in_environment(HOME_PATH, path_home)
            blackboard.set_in_environment(ROBOT_POSITION, robot_pos)
            return False
        else:
            return True