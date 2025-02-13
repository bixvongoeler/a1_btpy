#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class DoneGeneral(btl.Task):
    """
    Implementation of the Task "Done General".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Done with General Clean')

        # Set relevant blackboard variables to False
        blackboard.set_in_environment(VACUUMING, False)
        blackboard.set_in_environment(GENERAL_CLEANING, False)
        blackboard.set_in_environment(NEED_TO_CLEAN, None)

        return self.report_succeeded(blackboard)
