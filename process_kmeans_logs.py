#!/usr/bin/env python
"""
Parses the logs from the KMeans example.
"""

import argparse
from collections import defaultdict
import re
import uuid

import dateutil.parser
from matplotlib import pyplot
import numpy

def calculate_mean_time_to_reduction(loss_events):
    loss_reductions = numpy.linspace(0.8, 1, 30)
    for loss_trace in loss_events.values():
        loss_values = list(loss_trace.values())
        starting_loss = loss_values[0]
        target_losses = loss_reductions * starting_loss

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
            (time_str, thread_id_str, loss_str) = match.groups()
            thread_id = uuid.UUID(thread_id_str)
            timestamp = dateutil.parser.parse(time_str)
            loss = float(loss_str)
            loss_events[thread_id][timestamp] = loss

    # pyplot.figure()
    # for loss_trace in loss_events.values():
        # pyplot.plot_date(list(loss_trace.keys()), list(loss_trace.values()))
    # pyplot.show()

    # pyplot.figure()
    # for loss_trace in loss_events.values():
        # pyplot.plot_date(list(loss_trace.keys()), list(loss_trace.values()))
    # pyplot.show()

    pyplot.figure()
    for loss_trace in loss_events.values():
        timestamps = list(loss_trace.keys())
        losses = list(loss_trace.values())
        loss_reductions = [losses[-1] / l for l in losses]
        elapsed_time = [(t - timestamps[0]).total_seconds() for t in timestamps]
        pyplot.plot(loss_reductions, elapsed_time)
        pyplot.xlim(0.8, 1)
        pyplot.ylim(0, 0.1)
        pyplot.grid(True)
    pyplot.show()

if __name__ == '__main__':
    main()
