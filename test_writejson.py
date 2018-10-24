from hrm import writeJson
import pytest
import numpy
import json


@pytest.mark.parametrize("testinput", [
    ({"voltage_extremes": (1.0, 1.0), "duration": 1.0,
      "beats": numpy.array([1.0, 1.0]), "num_beats": 1.0, "mean_hr_bpm": 1.0}),
    ("blahblahblah"),
    ([])
])
def test(testinput):
    if isinstance(testinput, type("abc")):
        assert writeJson(testinput, {"beats": numpy.array([])}) == -1
    elif isinstance(testinput, type([])):
        assert writeJson("throwaway.csv", testinput) == -1
    else:
        writeJson("testwritejson.csv", testinput)
        jsonfile = open("testwritejson.json")
        jsonstr = jsonfile.read()
        exp = json.loads(jsonstr)
        print(type(exp["voltage_extremes"]))
        print(type(testinput["voltage_extremes"]))
        assert exp["voltage_extremes"][0] == testinput["voltage_extremes"][0]
        assert exp["duration"] == testinput["duration"]
        assert exp["beats"][0] == testinput["beats"][0]
        assert exp["num_beats"] == testinput["num_beats"]
        assert exp["mean_hr_bpm"] == testinput["mean_hr_bpm"]
