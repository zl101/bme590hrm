from hrm import readCSV, getBeats, getMeanHR, getDuration
import pytest


@pytest.mark.parametrize("testinput,expected", [
    ('test_data31.csv', 81.42),
    ('test_data1.csv', 75),
    ('test_data11.csv', 68.57)
])
def test(testinput, expected):
    [t, v] = readCSV(testinput)
    beattimes = getBeats(t, v)
    exp = getMeanHR(beattimes, duration=getDuration(t))
    assert abs(expected-exp) < 0.2*expected
