#!/usr/bin/env python
""" Creates artifical k-means data. """

import numpy

CLUSTER_DIMS = 100
NUM_CLUSTERS = 10
NUM_POINTS_PER_CLUSTER = 1_000

def main():
    clusters = [[i] * CLUSTER_DIMS for i in range(NUM_CLUSTERS)]
    points = numpy.concatenate([
        numpy.random.normal(loc=cluster, scale=100, size=(NUM_POINTS_PER_CLUSTER, len(cluster)))
        for cluster in clusters])
    numpy.savetxt('kmeans_data.txt', points)

if __name__ == '__main__':
    main()
