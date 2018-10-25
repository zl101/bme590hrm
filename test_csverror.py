from hrm import readCSV
import pytest


def test():
    with pytest.raises(TypeError):
        readCSV("test_data30.csv")
    with pytest.raises(ValueError):
        readCSV("test_data32.csv")
