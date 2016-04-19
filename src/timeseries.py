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
import sklearn.decomposition as deco

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
            raise(TypeError, 'Must use numpy array for timeseries')

        """Initializer"""
        self.timeseries = timeseries


        """
        NNames:
            A list of the names of all neurons whose indexes map
            to the indexes of datasets in timeseries(). Note: if
            a neuron's identity is not confirmed, the index will
            contain a None
        """
        self.nnames = nnames if not nnames is None else [None
                for i in xrange(timeseries.shape[0])]
        self.nname_to_index = {
                self.nnames[j]:j
                for j in range(len(self.nnames))
                if self.nnames[j]!=None
            }

    def series_on_neurons(self, neurons):
        raise(NotImplementedError)



