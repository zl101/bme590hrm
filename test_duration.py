from hrm import getDuration
import pytest

CONST_ALLOWEDERROR = 0.0000001


@pytest.mark.parametrize("testinput,expected", [
    ([0.001, 0.5, 0.02, 0.3], 0.499),
    ([0.13, 0.135, 0.139], 0.009)
])
def test(testinput, expected):
    res = getDuration(testinput)
    assert abs(res-expected) < CONST_ALLOWEDERROR
