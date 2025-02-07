import pytest
from bt.debug_nodes.debug_message import DebugMessage
import bt_library as btl

@pytest.mark.parametrize(
    "test_input_msg,expected_out",
    [("pass", "pass\n"),
     ("fail", "fail\n"),
     ("running", "running\n")]
)
def test_run(test_input_msg, expected_out, capsys):
    msg_node = DebugMessage(test_input_msg, btl.ResultEnum.SUCCEEDED)
    msg_node.run(btl.Blackboard())
    captured = capsys.readouterr()
    assert captured.out.count(expected_out) == 1

