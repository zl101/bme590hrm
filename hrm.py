import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import sys
import logging
CONST_MAXVOLTAGE = 10000
CONST_MINVOLTAGE = -10000
CONST_MINBPS = 0.5
CONST_CUTOFF = 0.7
CONST_MINTIMEBETWEENBEATS = 0.2
CONST_MINTIME = -10000
CONST_MAXTIME = 10000
CONST_MINPOINTSFORECG = 1000


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
            try:
                timesarr.append(float(row[0]))
                voltagesarr.append(float(row[1]))
            except:
                logging.error("Found invalid values in file")
                raise TypeError("Invalid values encountered in file")
    if(max(voltagesarr) > 300):
        logging.error("Found value above 300")
        raise ValueError("Voltages Exceed Range")
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


def getMeanHR(beatsarr, lower=CONST_MINTIME, upper=CONST_MAXTIME, duration=-1):
    """
    use upper and lower to pass in user specified time interval
    if no user duration, must pass in duration used to get the beats arr
    """
    length = len(beatsarr)
    lowerindex = 0
    upperindex = length-1
    for i in range(0, length):
        if beatsarr[i] > lower:
            lowerindex = i
            break
    for j in range(0, length):
        if beatsarr[length-j-1] < upper:
            upperindex = length-j
            break
    nbeats = beatsarr[lowerindex:upperindex]
    if(duration == -1):
        return len(nbeats)/((upper-lower)/60)
    else:
        return len(nbeats)*60/duration


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


def hrd(time, voltage, lower=CONST_MINTIME, upper=CONST_MAXTIME, duration=-1):
    """
    Wrapper function used to call other functions giving metrics
    Metrics used to construct dictionary
    Returns dictionary
    """
    dict = {}
    dict["voltage_extremes"] = voltageExtremes(voltage)
    dict["duration"] = getDuration(time)
    beats = getBeats(time, voltage)
    dict["beats"] = beats
    dict["num_beats"] = getNumBeats(beats)
    if duration == -1:
        dict["mean_hr_bpm"] = getMeanHR(beats, lower, upper)
    else:
        if(duration == 0):
            raise ValueError("Invalid Duration")
        dict["mean_hr_bpm"] = getMeanHR(beats, duration=duration)
    return dict


def writeJson(filename, dict):
    """
    given a filename and dictionary writes dictionary to filename.json
    """
    if(not isinstance(dict, type({}))):
        return -1
    ndict = dict.copy()
    ndict["beats"] = ndict["beats"].tolist()
    ind = filename.find('.')
    if ind == -1:
        return -1
    jsonname = filename[0:ind] + ".json"
    with open(jsonname, 'w') as file:
        json.dump(ndict, file, ensure_ascii=False)

if __name__ == "__main__":
        """
        Main gets user inputs and uses those inputs to perform task
        """
        logging.basicConfig(filename='hrm.log', level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("Starting New Log...")
        try:
            fname = input("Enter CSV File Name: ")
            [time, voltage] = readCSV(fname)
        except:
            logging.error("Unable to Read File")
            sys.exit("Invalid File")
        logging.info("filename: " + fname)
        if(len(time) < CONST_MINPOINTSFORECG):
            sys.exit("Not enough data to perform analysis")
        k = input("Select custom interval for Mean HR y/n?")
        if k == "y":
            print("Signal ranged from ")
            print(str(min(time)) + " seconds to ")
            print(str(max(time)) + " seconds")
            lower = input("Enter lower in seconds:")
            upper = input("Enter upper in seconds:")
            logging.info("User Input Lower: " + lower)
            logging.info("User Input Upper: " + upper)
            try:
                lower = float(lower)
                upper = float(upper)
            except:
                logging.error("Check User Input")
                sys.exit("User Input Non numeric")
            if(lower < min(time)):
                logging.error("Check User Input")
                sys.exit("User Input Below Valid Range")
            if(upper > max(time)):
                logging.error("Check User Input")
                sys.exit("User Input Above Valid Range")
            hrdict = hrd(time, voltage, lower, upper)
        else:
            hrdict = hrd(time, voltage, duration=getDuration(time))
        writeJson(fname, hrdict)
        print("Wrote Stats to File")
