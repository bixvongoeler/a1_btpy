#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import ROBOT_POSITION, VACUUMING, SPOT_CLEANING_POSITION, SPOT_CLEANING


class DoneSpot(btl.Task):
    """
    Implementation of the Task "Done Spot".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Done with Spot')

        blackboard.set_in_environment(VACUUMING, False)
        blackboard.set_in_environment(SPOT_CLEANING, False)
        blackboard.set_in_environment(SPOT_CLEANING_POSITION, None)

        return self.report_succeeded(blackboard)
