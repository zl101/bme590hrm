from hrm import readCSV, getBeats, getMeanHR, getDuration, hrd
import pytest
import numpy


@pytest.mark.parametrize("testinput,expected", [
    ('test_data31.csv', {"voltage_extremes": (1.0, 1.0), "duration": 1.0,
                         "beats": numpy.array([]),
                         "num_beats": 1.0, "mean_hr_bpm": 1.0}),
    ('test_data1.csv', {"voltage_extremes": (1.0, 1.0), "duration": 1.0,
                        "beats": numpy.array([]),
                        "num_beats": 1.0, "mean_hr_bpm": 1.0}),
    ('test_data10.csv', {"voltage_extremes": (1.0, 1.0), "duration": 1.0,
                         "beats": numpy.array([]),
                         "num_beats": 1.0, "mean_hr_bpm": 1.0})

])
def test(testinput, expected):
    [t, v] = readCSV(testinput)
    exp = hrd(t, v, duration=getDuration(t))
    assert isinstance(exp["voltage_extremes"],
                      type(expected["voltage_extremes"]))
    assert isinstance(exp["duration"],
                      type(expected["duration"]))
    assert isinstance(exp["beats"],
                      type(expected["beats"]))
    assert isinstance(exp["duration"],
                      type(expected["num_beats"]))
    assert isinstance(exp["duration"],
                      type(expected["mean_hr_bpm"]))
