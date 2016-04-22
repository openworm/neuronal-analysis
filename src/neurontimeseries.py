"""
We are going to start by providing a unified inter
face for transporting and dealing with C-Elegans i
maging data

Data_load is used for retrieving either Kato or C3
02 simulation run data. There will also be an inte
rface for annotating and labelling data.

TimeSeries is the base class for handling neuronal a
ctivity data. (Note: there will be another set of
interfaces for analyzing data. You'll have to plug
a WormData interface into them
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

from itertools import combinations, product
import neurontimeseries

import scipy.cluster.hierarchy as sch

class NeuronTimeSeries:


    """
    As of now, TimeSeries is meant to be subclassed.
    Until we make new design decisions, TimeSeries
    will provide a blank interface which subclasses
    will need to implement.

    Nothing complicated enough is going on behind
    the scenes yet to warrant setting up some abstr-
    act WormData interface
    """
    def __init__(self,timeseries=None,nnames=None):
        if not type(timeseries).__module__ == np.__name__ :
            raise TypeError('Must use numpy array for timeseries')

        """Initializer"""
        self.timeseries = timeseries


        """
        NNames: A list of the names of all neurons
        whose indexes map to the indexes of datasets in
        timeseries(). Note: if a neuron's identity is not
        confirmed, the index will contain a None
        """
        self.nnames = nnames if not nnames is None else [None
                for i in xrange(timeseries.shape[0])]
        self.nname_to_index = {
                self.nnames[j]:j
                for j in range(len(self.nnames))
                if self.nnames[j]!=None
            }


    def dims_match(self, other):
        return self.timeseries.shape == other.timeseries.shape and set(self.nnames) == set(other.nnames)

    def neuron_intersect(self, other):
        intersection=set(self.nnames).intersection(other.nnames)
        return intersection

    def select_neurons(self,neurons):
        # TODO: check i and j are in bounds
        indexes = [self.nname_to_index[k] for k in neurons if k in self.nname_to_index]
        mat = self.timeseries[indexes]
        return NeuronTimeSeries(timeseries=mat, nnames=neurons)

    def cross_correlate(self, other):
        a = self
        b = other
        if not self.dims_match(other):
            nintersect = self.neuron_intersect(other)
            a = self.select_neurons(nintersect)
            b = other.select_neurons(nintersect)

        min_ind = min(a.timeseries.shape[1], b.timeseries.shape[1])
        # Let numpy catch any errors
        return np.dot(a.timeseries[:,0:min_ind], b.timeseries[:,0:min_ind].T)


class NeuronTimeSeriesIntegrator():
    """
    For integrating multiple time series and running
    cross-series analysis
    """
    def __init__(self,series):

        # Typechecking
        for ts in series:
            if not ts.__module__ == neurontimeseries.__name__:
                raise(TypeError, """
                    Must use timeseries object
                    for NeuronTimeSeriesComparator""")

        self.series = series
        self.size = len(self.series)
        self.neurons = [
            ts.nnames
            for ts in self.series]

        self.neuronmemberships = [
            set(
                filter(lambda x: x!=None, series[i].nnames))
            for i in range(5) ]

        self.global_neurons = self.global_shared()
        self.local_neurons = self.local_shared()

        groupings  = [
            i for i in product(
                range(self.size),
                range(self.size)
            )]

        self.neuron_pairings = groupings


    def global_shared(self):
        return sorted(
            set.intersection(*self.neuronmemberships))

    def local_shared(self):
        n = self.size
        similars = {
            (i,j): set.intersection(
                set(self.neurons[i]),
                set(self.neurons[j]))
            for j in range(n)
            for i in range(n)
        }
        return similars

    def global_timeseries(self):
        ns = self.global_neurons
        return map(
            lambda series: series.select_neurons(ns),
            self.series
        )

    def cross_correlations(self, global_ns=False, clustered=False):
        CC = {}
        for k,i in self.neuron_pairings:
            neuron_list = self.global_neurons \
                if global_ns else self.local_neurons[(k,i)]

            a = self.series[i].select_neurons(neuron_list)
            b = self.series[k].select_neurons(neuron_list)

            correl = a.cross_correlate(b)

            CC[(k,i)] = correl

        return CC
