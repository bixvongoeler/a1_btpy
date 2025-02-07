#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

from bt_library.blackboard import Blackboard
from bt_library.common import ResultEnum
from bt_library.decorator import Decorator
from bt_library.tree_node import TreeNode


class UntilFails(Decorator):
    """
    Specific implementation of the UntilFails decorator.
    """

    def __init__(self, child: TreeNode):
        """
        Default constructor.

        :param child: Child associated to the decorator
        """
        super().__init__(child)

    def run(self, blackboard: Blackboard) -> ResultEnum:
        """
        Execute the behavior of the node.

        :param blackboard: Blackboard with the current state of the problem
        :return: The result of the execution
        """

        result_child = self.child.run(blackboard)

        # Return running until child returns failure
        if result_child == ResultEnum.FAILED:
            return self.report_failed(blackboard)
        else:
            return self.report_running(blackboard)
