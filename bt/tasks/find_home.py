#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import HOME_PATH, HOME_POSITION


class FindHome(btl.Task):
    """
    Implementation of the Task "Find Home".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Looking for a home')

        home_pos = blackboard.get_in_environment(HOME_POSITION, None)
        if home_pos is None:
            self.print_message('Home position not found')
            return self.report_failed(blackboard)

        my_pos = blackboard.get_in_environment('ROBOT_POSITION', None)
        if my_pos is None:
            self.print_message('Robot position not found')
            return self.report_failed(blackboard)

        path_home = [home_pos[0] - my_pos[0], home_pos[1] - my_pos[1]]

        blackboard.set_in_environment(HOME_PATH, path_home)
        return self.report_succeeded(blackboard)
