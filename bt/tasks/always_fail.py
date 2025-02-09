#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class AlwaysFail(btl.Task):
    """
    Implementation of the Task "Always Fail".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Always Fail After Dusty Spot')

        blackboard.set_in_environment(VACUUMING, False)
        blackboard.set_in_environment(DUSTY_SPOT_CLEANING_POSITION, None)
        blackboard.set_in_environment(DUSTY_SPOT_CURRENT_ANGLE, None)
        blackboard.set_in_environment(DUSTY_SPOT_RADIUS, None)
        blackboard.set_in_environment(DUSTY_SPOT_CURRENT_RADIUS, None)

        return self.report_failed(blackboard)
