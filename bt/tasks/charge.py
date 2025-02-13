#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import CHARGING, BATTERY_LEVEL

class Charge(btl.Task):
    """
    Implementation of the Task "Charge".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Charging')

        # Set Charging to True
        blackboard.set_in_environment(CHARGING, True)

        # Recall Battery Level
        battery_level = blackboard.get_in_environment(BATTERY_LEVEL, None)
        if battery_level is None:
            self.print_message('Battery level not found')
            return self.report_failed(blackboard)

        # Charging logic
        if battery_level < 100:
            # Run while battery level is less than 100
            blackboard.set_in_environment(BATTERY_LEVEL, battery_level + 0.1)
            return self.report_running(blackboard)
        else:
            # Battery is fully charged exit
            self.print_message('Battery fully charged')
            blackboard.set_in_environment(CHARGING, False)
            return self.report_succeeded(blackboard)