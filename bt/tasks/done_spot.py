#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class DoneSpot(btl.Task):
    """
    Implementation of the Task "Done Spot".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Done with Spot')

        # Reset the environment variables related to spot cleaning
        blackboard.set_in_environment(VACUUMING, False)
        blackboard.set_in_environment(SPOT_CLEANING, False)
        blackboard.set_in_environment(SPOT_CLEANING_POSITION, None)
        blackboard.set_in_environment(SPOT_CLEANING_PATH, None)
        blackboard.set_in_environment(SPOT_CURRENT_ANGLE, None)
        blackboard.set_in_environment(SPOT_RADIUS, None)
        blackboard.set_in_environment(SPOT_CURRENT_RADIUS, None)

        return self.report_succeeded(blackboard)
