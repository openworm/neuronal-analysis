"""
Analyzer is for creating data analysis pipelines. 
It integrates with experiment_management so each step in the analysis
of data can be annotated, etc. 

If the routines implemented by Analyzer aren't suitable enough
for what you are doing, Analyzer also allows for the creation of 
custom pipelines with the same annotation capabilities as native ones. 

Data analysis pipelines should be easily composable,
modularizable, and shareable. Analyzer makes this standardized for
everything OpenWorm. 

Additionally, once pipelines are composable they become machine-composable. 
Such capabilities will be invaluable if we want to develop complex auto-experimentation
software. 

"""

import sys
import os
import numpy as np

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

from tvregdiff import TVRegDiff

class Analyzer:

    def __init__(self, timeseries):
        self.timeseries = timeseries

    def tvd(self, iters=10, alpha=1e-1, diff=None): #iter specifies number of iterations, alpha specifies 'regularization parameter'
    	
    	deriv = []
    	count = 0

    	for t, vector in enumerate(self.timeseries.T): #differentiate neuron-by-neuron

    		u = TVRegDiff(vector, iters, alpha, dx=diff, plotflag=0, diagflag=0)
    		deriv.append(u)

    		if count % 10 == 0:
    			print("Completed:", count)
    		count += 1

    	return np.array(deriv).T

    def timeseries_plot(self, ax):
    	subplot = ax.pcolor(self.timeseries.T)
    	return subplot

    def pca_plot3d(self, ax):

    	# Example:
    	# a = Analyzer(wormData)
    	# fig = plt.figure(figsize=(20,10))
    	# ax = fig.add_subplot(1, 2, 1, projection='3d')
    	# a.pca_plot3d(ax)
    	# ax.set_title(("PCA results"))
    	# plt.show()

		pca = PCA(n_components=3)
		pca.fit(self.timeseries)
		out = pca.transform(self.timeseries)

		col = (out.T[0] + out.T[1] + out.T[2])

		cmhot = plt.get_cmap("jet")

		subplot = ax.scatter(out.T[0], out.T[1], out.T[2], depthshade='False', c=col, cmap=cmhot, marker='o')

		return subplot

