import transform as tf
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import PyOpenWorm as pow

from itertools import combinations
import timeseries 


class NeuronTimeSeriesIntegrator():
    """
    For integrating multiple time series and running
    cross-series analysis
    """
    def __init__(self,series):

        # Typechecking
        for ts in series:
            if not ts.__module__ == timeseries.__name__:
                raise(TypeError, 'Must use timeseries object for NeuronTimeSeriesComparator')
        self.series = series
        self.size = len(self.series) 
        self.neurons = [
            ts.nnames
            for ts in self.series]
        self.neuronmemberships = [ set(filter(lambda x: x!=None, series[i].nnames)) for i in range(5) ]
 
        self.global_neurons = self.global_shared()
        self.local_neurons = self.local_shared()
        
        groupings  = [ i for i in combinations(range(self.size), r=2)].extend(range(self.size))    
        self.neuron_pairings = groupings
        

    def global_shared(self):
        return sorted(set.intersection(*self.neuronmemberships))

    def local_shared(self):
        n = self.size
        similars = {
            (i,j): set.intersection(set(self.neurons[i]), set(self.neurons[j]))
            for j in range(n)
            for i in range(n)
        }
        return similars
    
    def datasintersect(self,i,j, global_ns=False):
        inbounds = i < self.size and j < self.size

        # TODO: check i and j are in bounds
        neurons = self.global_neurons if global_ns else self.local_neurons[(i,j)]

        indi = [self.series[i].nname_to_index[k] for k in neurons]
        indj = [self.series[i].nname_to_index[k] for k in neurons]

        mati = np.take(self.series[i], indi,axis=0)
        matj = np.take(self.series[j], indj,axis=0) 
        last = min(mati.shape[1], matj.shape[1])
        
        mati = mati[:,0:last]
        matj = matj[:,0:last]

        timeseriesi = NeuronTimeSeries(timeseries=mati, nnames=neurons)
        timeseriesj = NeuronTimeSeries(timeseries=matj, nnames=neurons)
        
        return timeseriesi, timeseriesj

import timeseries as ts
import data_config as dc
wd = dc.kato.data()
deltas = [ts.NeuronTimeSeries(timeseries=wd[i]['deltaFOverF_deriv'], nnames=wd[i]['NeuronIds'][0]) for i in range(5)]

print timeseries.__name__
integrator = NeuronTimeSeriesIntegrator(deltas)




"""    

wd = katodata.KatoData()

#sklearn_pca = PCA(wd['deltaFOverF_deriv'])
sklearn_pca = PCA(n_components=3)

transf = sklearn_pca.fit_transform(wd['deltaFOverF_deriv'])
#cov = sklearn_pca.get_covariance()
backtransformed = sklearn_pca.inverse_transform(transf)

components = sklearn_pca.components_

c302_loc = "."

# we are calculating
def crosscorrelate(value):
  return np.dot(value.T, value)

matrix1 = crosscorrelate(wd['deltaFOverF_deriv'])
print matrix1.shape

def neuronintersect(neuron1, wd):
  wd_neurons = set([ n[0] for n in wd['NeuronIds'] if n!=None])
  intersected = wd_neurons.intersection(set(c302_neurons))

# 303 elements, first is removed and saved as time steps (seconds)
# demo_data.dat is any proper c302 output .dat file
c302 = np.loadtxt(c302_loc + '/demo_data.dat')
c302_time = c302[:,0]
data = np.delete(c302, 0, 1)
c302_neurons = tf.c302_list(c302_loc + "/LEMS_c302_C_Full.xml")

#indexes_map =
wd_neurons = set([ n[0] for n in wd['NeuronIds'] if n!=None])


intersected = wd_neurons.intersection(set(c302_neurons))

print intersected

# PCA on simulation data
c302_pca, c302_trans = tf.scikit_pca(data, 3)



#plot simulation results
def plot_c302_result():
  fig = plt.figure(figsize=(10,20))
  gs  = gridspec.GridSpec(1,1)
  subplot1 = fig.add_subplot(gs[0,0])
  subplot1.set_title("c302 simulation")
  subplot1.pcolormesh(c302_deriv.T)
  subplot1.axis('tight')
#  subplot1.set_xticklabels(c302_time)
#  plt.pcolormesh(data.T);
#  plt.colorbar()
#  plt.show()
  fig.show()
  plt.savefig('simresult',dpi=300)


#plot_c302_result()
"""
