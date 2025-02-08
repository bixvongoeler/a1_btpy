#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt as bt
import bt_library as btl
from bt_library.common import ResultEnum as RE

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
# tree_root = bt.Selection(
#     [
#         bt.BatteryLessThan30(),
#         bt.Timer(10, bt.FindHome())
#     ]
# )

# Battery Path
battery_path = bt.Sequence(
    [
        bt.BatteryLessThan30(),
        bt.FindHome(),
        bt.GoHome(),
        bt.Charge()
    ]
)

# Cleaning Sub Paths
spot_cleaning_path = bt.Sequence(
    [
        bt.SpotCleaning(),
        bt.FindSpot(),
        bt.GoToSpot(),
        bt.UntilSucceeds(bt.CleanSpot()),
        bt.DoneSpot()
    ]
)

general_cleaning_path = bt.Sequence(
    [
        bt.GeneralCleaning(),
        bt.Sequence(
            [
                bt.Priority(
                    [
                        bt.Sequence(
                            [
                                bt.DustySpot(),
                                bt.UntilSucceeds(
                                    bt.CleanSpot()
                                ),
                                bt.AlwaysFail()
                            ]
                        ),
                        bt.UntilFails(
                            bt.CleanFloor()
                        )
                    ]
                ),
                bt.DoneGeneral()
            ]
        )
    ]
)

# Cleaning Path
cleaning_path = bt.Selection(
    [
        spot_cleaning_path,
        general_cleaning_path
    ]
)

tree_root = bt.Priority(
    [
        battery_path,
        cleaning_path,
        bt.DoNothing()
    ]
)

# Store the root node in a behavior tree instance
robot_behavior = btl.BehaviorTree(tree_root)
