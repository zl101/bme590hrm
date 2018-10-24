from hrm import readCSV, getBeats, getNumBeats
import pytest


@pytest.mark.parametrize("testinput,expected", [
    ('test_data31.csv', 19),
    ('test_data1.csv', 35),
    ('test_data11.csv', 32)
])
def test(testinput, expected):
    [t, v] = readCSV(testinput)
    beattimes = getBeats(t, v)
    numbeats = getNumBeats(beattimes)
    assert abs(expected-numbeats) < 0.2*expected
