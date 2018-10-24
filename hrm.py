import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
CONST_MAXVOLTAGE = 10000
CONST_MINVOLTAGE = -10000
CONST_MINBPS = 0.5
CONST_CUTOFF = 0.7
CONST_MINTIMEBETWEENBEATS = 0.2


def readCSV(filename):
    """
    Reads a time/voltage csv file and returns into arrays
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        timesarr = []
        voltagesarr = []
        for row in reader:
            if(len(row) != 2):
                continue
            if(row[0] == '' or row[1] == ''):
                continue
            timesarr.append(float(row[0]))
            voltagesarr.append(float(row[1]))
    return [timesarr, voltagesarr]


def getDuration(timesarr):
    """
    gets the duration of the input time array
    """
    dur = max(timesarr)-min(timesarr)
    return dur


def getBeats(timesarr, voltagesarr):
    """
    returns array of times of when there were beats
    """
    dur = getDuration(timesarr)
    numpointsforavg = int(np.ceil(CONST_MINBPS*dur))
    sortedvoltagesasc = sorted(voltagesarr, reverse=True)
    sortedvoltagesd = sorted(voltagesarr)
    cutoff = CONST_CUTOFF * np.average(sortedvoltagesasc[0:numpointsforavg])
    cutoff += np.average(sortedvoltagesd[0:numpointsforavg]) * (1-CONST_CUTOFF)
    length = len(timesarr)
    beats = []
    lastbeat = -1
    for x in range(0, length-2):
        if(voltagesarr[x+1] > cutoff and voltagesarr[x+1] > voltagesarr[x] and
                voltagesarr[x+1] > voltagesarr[x+2] and
                timesarr[x+1]-lastbeat > CONST_MINTIMEBETWEENBEATS):
            beats.append(timesarr[x+1])
            lastbeat = timesarr[x+1]
    return np.array(beats)


def getNumBeats(beatsarr):
    """
    given array of times at which beats occur, returns total number of beats
    """
    return len(beatsarr)


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
        [time, voltage] = readCSV('test_data11.csv')
        beattimes = getBeats(time, voltage)
        print(getNumBeats(beattimes))
        fig, ax = plt.subplots()
        ax.plot(time, voltage)
        plt.show()
