from hrm import readCSV
import pytest


@pytest.mark.parametrize("testinput,expected", [
    ('csv1.csv', [[1, 3, 5], [2, 4, 6]]),
    ('csv2.csv', [[-3, 4, 10, -1], [4, 4, 10, -1]])
])
def test(testinput, expected):
    res = readCSV(testinput)
    assert res == expected
