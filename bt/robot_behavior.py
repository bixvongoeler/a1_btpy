#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 3.0.0 - copyright (c) 2023-2024 Santini Fabrizio. All rights reserved.
#

import bt as bt
import bt_library as btl

# Grid size is quite small, so we need to increase the timer length by a multiplier
TIMER_MULTIPLIER = 5

# Battery Path
battery_path = bt.Sequence(
    [
        bt.BatteryLessThan30(),
        bt.FindHome(),
        bt.GoHome(),
        bt.Charge()
    ]
)

# Spot Cleaning Sub Paths
spot_cleaning_path = bt.Sequence(
    [
        bt.SpotCleaning(),
        bt.FindSpot(),
        bt.GoToSpot(),
        bt.Timer(20 * TIMER_MULTIPLIER, bt.CleanSpot()), # Needs to be higher than 20 as the grid size is quite small
        bt.DoneSpot()
    ]
)

# General Cleaning
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
                                bt.Timer(
                                    35 * TIMER_MULTIPLIER,
                                    bt.DustyCleanSpot()
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


# Create Root Node from our Sub Trees
tree_root = bt.Priority(
    [
        battery_path,
        cleaning_path,
        bt.DoNothing()
    ]
)

# Store the root node in a behavior tree instance
robot_behavior = btl.BehaviorTree(tree_root)
