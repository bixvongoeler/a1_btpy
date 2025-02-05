#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt as bt
import bt_library as btl

# Instantiate the tree according to the assignment. The following are just examples.

# Example 1:
# tree_root = bt.Timer(5, bt.FindHome())

# Example 2:
# tree_root = bt.Selection(
#     [
#         BatteryLessThan30(),
#         FindHome()
#     ]
# )

# Example 3:
tree_root = bt.Selection(
    [
        bt.BatteryLessThan30(),
        bt.Timer(10, bt.FindHome())
    ]
)

# Store the root node in a behavior tree instance
robot_behavior = btl.BehaviorTree(tree_root)
