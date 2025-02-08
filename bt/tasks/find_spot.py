#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import SPOT_CLEANING_PATH, SPOT_CLEANING_POSITION, ROBOT_POSITION, SPOT_RADIUS


class FindSpot(btl.Task):
    """
    Implementation of the Task "Find Home".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Looking for Spot')

        spot_pos = blackboard.get_in_environment(SPOT_CLEANING_POSITION, None)
        if spot_pos is None:
            self.print_message('Spot position not found')
            return self.report_failed(blackboard)

        my_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
        if my_pos is None:
            self.print_message('Robot position not found')
            return self.report_failed(blackboard)

        path_to_spot = [spot_pos[0] - my_pos[0], spot_pos[1] - my_pos[1]]

        blackboard.set_in_environment(SPOT_CLEANING_POSITION, spot_pos)
        blackboard.set_in_environment(SPOT_CLEANING_PATH, path_to_spot)
        return self.report_succeeded(blackboard)
