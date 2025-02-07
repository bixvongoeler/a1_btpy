#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl

class DebugMessage(btl.TreeNode):
    """
    Implementation of the Debug Task "Debug Message".
    """
    def __init__(self, message: str, result: btl.ResultEnum):
        """!
        Default constructor.

        :param message: Debug message to print
        :param result: Result to return ( FAILED, RUNNING, SUCCEEDED )
        """
        super().__init__()
        self.message = message
        self.result = result

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message(self.message)
        # print(self.message)

        if self.result == btl.ResultEnum.FAILED:
            return self.report_failed(blackboard)
        elif self.result == btl.ResultEnum.RUNNING:
            return self.report_running(blackboard)
        if self.result == btl.ResultEnum.SUCCEEDED:
            return self.report_succeeded(blackboard)
        else:
            return self.report_failed(blackboard)