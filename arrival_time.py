#!/usr/bin/env python
"""
Parses the logs from the Mixed example.
"""

import argparse
from collections import defaultdict
import re
import uuid

import dateutil.parser
from matplotlib import pyplot
import numpy
import pandas

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logfile', type=argparse.FileType())
    args = parser.parse_args()

    regex = re.compile(r'(.*) INFO .* calling updateLoss from thread (.*) with loss (.*)')

    # Map from job ID to map from timestamp to loss value
    loss_events = defaultdict(dict)
    for line in args.logfile:
        match = regex.match(line)
        if match:
            try:
                (time_str, thread_id_str, loss_str) = match.groups()
                thread_id = uuid.UUID(thread_id_str)
                timestamp = dateutil.parser.parse(time_str)
                loss = float(loss_str)
                loss_events[thread_id][timestamp] = loss
            except:
                print(line)
                continue
    #print(type(loss_events))
#    print(loss_events)

    # list of pandas series
    dataframes = [pandas.Series(list(trace.values()), index=list(trace.keys()))
        for trace in loss_events.values()]
    #print(dataframes[0])

    resampled = [df.asfreq('1S', method='pad') for df in dataframes]
    #print(resampled[0])
    centered = [df - df[-1] for df in resampled]
    normalized = [df / df[0] for df in centered]

    summed = pandas.Series()
    for series in normalized:
        summed = summed.add(series, fill_value=0)
    #print(summed)
    summed = summed.resample('2S').mean()
    #print(summed)

    #print(type(summed.index))
    #print(summed.index)
    #print(summed.index[0])
    #print(summed.index - summed.index[0])
    #print(len(summed.index))


    lrange = summed[0] - summed[-1]
    print("\n")
    print("First loss: {}. Last loss: {}".format(summed[0], summed[-1]))
    print("total loss range is {}".format(lrange))
    #print("lrange type: {}".format(type(lrange)))

    p90 = summed[0] - 0.9*lrange
    p95 = summed[0] - 0.95*lrange
    print("total length of series {}".format(len(summed)))
    print("90% loss: {}. 95% loss: {}".format(p90, p95))
    for i in reversed(range(len(summed))):
        if summed[i] >= p90:
            print("90% loss. the {}th element. {}".format(i, summed[i]))
            et = (summed.index[i] - summed.index[0]).total_seconds()
            print("total elapsed time {}".format(et))
            print("Average elapsed time {}".format(et/160))
            break

    for i in reversed(range(len(summed))):
        if summed[i] >= p95:
            print("95% loss. the {}th element. {}".format(i, summed[i]))
            et = (summed.index[i] - summed.index[0]).total_seconds()
            print("total elapsed time {}".format(et))
            print("Average elapsed time {}".format(et/160))
            break

    print("\n")

    #pyplot.figure()
    #pyplot.plot([i*5 for i in range(len(summed.index))] , summed)
    #pyplot.show()

if __name__ == '__main__':
    main()
