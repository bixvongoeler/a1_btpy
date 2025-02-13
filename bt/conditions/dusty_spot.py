#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class DustySpot(btl.Condition):
    """
    Implementation of the condition "Dusty Spot".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Checking Dusty Spot')

        # Check if the Dusty Spot sensor is activated
        if blackboard.get_in_environment(DUSTY_SPOT_SENSOR, False):
            # if so, set the Dusty Spot position and radius
            self.print_message('Dusty Spot Detected')
            current_pos = blackboard.get_in_environment(ROBOT_POSITION, None)
            blackboard.set_in_environment(DUSTY_SPOT_CLEANING_POSITION, current_pos)
            blackboard.set_in_environment(DUSTY_SPOT_CURRENT_RADIUS, 8)
            blackboard.set_in_environment(DUSTY_SPOT_RADIUS, 24)
            blackboard.set_in_environment(DUSTY_SPOT_CURRENT_ANGLE, 0)
            return self.report_succeeded(blackboard)
        else:
            return self.report_failed(blackboard)
