#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# Version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt_library as btl


class Priority(btl.Composite):
    """
    Specific implementation of the priority composite.
    Always starts with the highest priority (first) child.
    """

    def __init__(self, children: btl.NodeListType):
        """!
        Default constructor.

        :param children: List of children for this node
        """
        super().__init__(children)

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        """
        Execute the behavior of the node. Priority nodes check children in order
        until one succeeds or all fail.

        :param blackboard: Blackboard with the current state of the problem
        :return: The result of the execution
        """
        # Always start from first (highest priority) child
        for child in self.children:
            result = child.run(blackboard)

            if result == btl.ResultEnum.SUCCEEDED:
                return btl.ResultEnum.SUCCEEDED

            if result == btl.ResultEnum.RUNNING:
                return btl.ResultEnum.RUNNING
            # If child failed, continue to next child

        # All children failed
        return btl.ResultEnum.FAILED