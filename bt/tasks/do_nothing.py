#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl
from ..globals import *


class DoNothing(btl.Task):
    """
    Implementation of the Task "Do Nothing".
    """
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message('Do Nothing: Waiting For Next Task')

        return self.report_succeeded(blackboard)
