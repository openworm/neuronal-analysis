import transform as tf
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import PyOpenWorm as pow

import katodata

class CompareBatch():
    """
    For organizing an arbitrary number of time series for comparison
    This will become useful for comparing multiple C302 runs, as well
    as comparing the five kato datasets
    """

class TimeSeriesComparator():
    """Implementing functionality to compare two time series"""
    def __init__(seriesA, seriesB):
        

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
