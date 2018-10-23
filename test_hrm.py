from hrm import readCSV,voltageExtremes
import pytest
@pytest.mark.parametrize("teststr,expected",[
    ([0,1,2],(0,2)),
    ([-5.5,-10,-2,6], (-10,6))
])
def test(teststr,expected):
    res = voltageExtremes(teststr)
    assert res == expected
