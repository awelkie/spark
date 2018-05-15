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

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logfile', type=argparse.FileType())
    args = parser.parse_args()

    regex = re.compile(r'(.*) INFO .* calling updateLoss from thread (.*) with loss (.*)')

    # Map from job ID to map from timestamp to loss value
    loss_events = defaultdict(dict)
    per_iter_loss = defaultdict(list)
    for line in args.logfile:
        match = regex.match(line)
        if match:
            try:
                (time_str, thread_id_str, loss_str) = match.groups()
                thread_id = uuid.UUID(thread_id_str)
                timestamp = dateutil.parser.parse(time_str)
                loss = float(loss_str)
                loss_events[thread_id][timestamp] = loss
                per_iter_loss[thread_id].append(loss)
            except:
                #print(line)
                continue

    pyplot.figure()
    for loss_trace in loss_events.values():
        losses = numpy.array(list(loss_trace.values()))
        losses -= losses[-1]
        losses /= losses[0]
        pyplot.plot_date(list(loss_trace.keys()), losses)
    pyplot.show()

    pyplot.figure()
    for loss_trace in per_iter_loss.values():
        iterations = [i for i in range(len(loss_trace))]
        pyplot.plot(iterations, loss_trace)
        pyplot.grid(True)
        pyplot.xlabel("Iteration")
        pyplot.ylabel("Loss value")
        pyplot.title("LogisticRegression Loss without SLAQ")
    pyplot.show()

    pyplot.figure()
    for loss_trace in loss_events.values():
        timestamps = list(loss_trace.keys())
        losses = list(loss_trace.values())
        #print(timestamps)
        #print(losses)
        loss_reductions = [losses[-1] / l for l in losses]
        elapsed_time = [(t - timestamps[0]).total_seconds() for t in timestamps]
        pyplot.plot(loss_reductions, elapsed_time)
#        pyplot.xlim(0.8, 1)
#        pyplot.ylim(0, 0.1)
        pyplot.grid(True)
    pyplot.show()

if __name__ == '__main__':
    main()
