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

class TimeSeries: 
    
    
    """
    As of now, TimeSeries is meant to be subclassed. 
    Until we make new design decisions, TimeSeries 
    will provide a blank interface which subclasses 
    will need to implement. 

    Nothing complicated enough is going on behind 
    the scenes yet to warrant setting up some abstr-
    act WormData interface
    """
    def __init__(self,timeseries,nnames=None,descriptor=None): 
        """Initializer"""
        self.description = descriptor if descriptor else 'No description provided'
        self.timeseries = timeseries
        self.nnames = nnames if nnames else [None 
                for i in xrange(timeseries.shape[0])]
    
    def neuron_names(self):
        """
        Returns:
            A list of the names of all neurons whose indexes map
            to the indexes of datasets in timeseries(). Note: if 
            a neuron's identity is not confirmed, the index will
            contain a None
        """
        #raise NotImplementedError("Subclasses should implement this!")
        return self.nnames

    def timeseries(self):
        """
        Returns: 
            A numpy matrix arranged neurons*time-series containing
            time series data for each neuron. 
        """
        #raise NotImplementedError("Subclasses should implement this!")
        return self.timeseries

    def metadata(self):
        """
        Returns:
            dictionary: keyed metadata for this time series
            dataset. 
        """
        #raise NotImplementedError("Subclasses should implement this!")
        return {'description': self.description}




 
    

