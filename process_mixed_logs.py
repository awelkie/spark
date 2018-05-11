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
    parser.add_argument('slaq_logfile', type=argparse.FileType())
    parser.add_argument('noslaq_logfile', type=argparse.FileType())
    args = parser.parse_args()

    regex = re.compile(r'(.*) INFO .* calling updateLoss from thread (.*) with loss (.*)')

    # Map from job ID to map from timestamp to loss value
    slaq_loss_events = defaultdict(dict)
    for line in args.slaq_logfile:
        match = regex.match(line)
        if match:
            try:
                (time_str, thread_id_str, loss_str) = match.groups()
                thread_id = uuid.UUID(thread_id_str)
                timestamp = dateutil.parser.parse(time_str)
                loss = float(loss_str)
                slaq_loss_events[thread_id][timestamp] = loss
            except:
                print(line)
                continue

    # Map from job ID to map from timestamp to loss value
    noslaq_loss_events = defaultdict(dict)
    for line in args.noslaq_logfile:
        match = regex.match(line)
        if match:
            try:
                (time_str, thread_id_str, loss_str) = match.groups()
                thread_id = uuid.UUID(thread_id_str)
                timestamp = dateutil.parser.parse(time_str)
                loss = float(loss_str)
                noslaq_loss_events[thread_id][timestamp] = loss
            except:
                print(line)
                continue

    slaq_dataframes = [pandas.Series(list(trace.values()), index=list(trace.keys()))
        for trace in slaq_loss_events.values()]

    noslaq_dataframes = [pandas.Series(list(trace.values()), index=list(trace.keys()))
        for trace in noslaq_loss_events.values()]

    slaq_resampled = [df.asfreq('5S', method='pad') for df in slaq_dataframes]
    slaq_centered = [df - df[-1] for df in slaq_resampled]
    slaq_normalized = [df / df[0] for df in slaq_centered]

    noslaq_resampled = [df.asfreq('5S', method='pad') for df in noslaq_dataframes]
    noslaq_centered = [df - df[-1] for df in noslaq_resampled]
    noslaq_normalized = [df / df[0] for df in noslaq_centered]

    slaq_summed = pandas.Series()
    for series in slaq_normalized:
        slaq_summed = slaq_summed.add(series, fill_value=0)
    slaq_summed = slaq_summed.resample('5S').mean()

    noslaq_summed = pandas.Series()
    for series in noslaq_normalized:
        noslaq_summed = noslaq_summed.add(series, fill_value=0)
    noslaq_summed = noslaq_summed.resample('5S').mean()

    pyplot.figure()
    pyplot.plot(5 * numpy.arange(len(slaq_summed)), slaq_summed, '-', label='SLAQ')
    pyplot.plot(5 * numpy.arange(len(noslaq_summed)), noslaq_summed, '--', label='Fair Resource')
    # pyplot.xlim(0, 400)
    # pyplot.ylim(0, 0.5)
    pyplot.title("Average normalized loss")
    pyplot.ylabel("Normalized loss")
    pyplot.xlabel("Elapsed time (seconds)")
    pyplot.legend()
    pyplot.show()

if __name__ == '__main__':
    main()
