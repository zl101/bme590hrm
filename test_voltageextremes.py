from hrm import voltageExtremes
import pytest


@pytest.mark.parametrize("testinput,expected", [
    ([0, 1, 2], (0, 2)),
    ([-5.5, -10, -2, 6], (-10, 6)),
    ([9, -8, -8, 11, 0.005], (-8, 11))
])
def test(testinput, expected):
    res = voltageExtremes(testinput)
    assert res == expected
