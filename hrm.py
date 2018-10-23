import csv
CONST_MAXVOLTAGE = 10000
CONST_MINVOLTAGE = -10000


def readCSV(filename):
    """
    Reads a time/voltage csv file and returns into arrays
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        timesarr = []
        voltagesarr = []
        for row in reader:
            timesarr.append(float(row[0]))
            voltagesarr.append(float(row[1]))
    return [timesarr, voltagesarr]


def voltageExtremes(voltages):
    """
    Returns tuple of min,max of array of voltages
    """
    min = CONST_MAXVOLTAGE
    max = CONST_MINVOLTAGE
    for k in voltages:
        if k < min:
            min = k
        if k > max:
            max = k
    return (min, max)


if __name__ == "__main__":
        [time, voltage] = readCSV('lol')
