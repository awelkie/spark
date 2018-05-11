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

    dataframes = [pandas.Series(list(trace.values()), index=list(trace.keys()))
        for trace in loss_events.values()]

    resampled = [df.asfreq('5S', method='pad') for df in dataframes]
    centered = [df - df[-1] for df in resampled]
    normalized = [df / df[0] for df in centered]

    summed = pandas.Series()
    for series in normalized:
        summed = summed.add(series, fill_value=0)
    summed = summed.resample('5S').mean()

    pyplot.figure()
    pyplot.plot_date(summed.index, summed)
    pyplot.show()

if __name__ == '__main__':
    main()
