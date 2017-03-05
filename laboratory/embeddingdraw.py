import sys
import numpy as np
import scipy.cluster.hierarchy as sch
import pylab
import scipy
import matplotlib.pyplot as plt
import networkx as nx
import numpy.ma as ma
from scipy.integrate import odeint
from mayavi import mlab

import matplotlib.cm as cm

import os
import sys
import numpy as np
import scipy.stats

sys.path.append('../src/')
import data_config  as dc

kato = dc.kato.data()
data = kato[0]["deltaFOverF_bc"].T

mean = np.mean(data, axis=1, keepdims=True)
standardized = (data-mean)
correlation = data.dot(data.T)
connectome = dc.connectome_networkx.data().to_directed()
adjacency = nx.to_numpy_matrix(connectome)


H=connectome
# reorder nodes from 0,len(G)-1
G=nx.convert_node_labels_to_integers(H)
# 3d spring layout
pos=nx.spring_layout(G,dim=3)
# numpy array of x,y,z positions in sorted node order
xyz=np.array([pos[v] for v in sorted(G)])
# scalar colors
scalars=np.array(G.nodes())+5

mlab.figure(1, bgcolor=(0, 0, 0))
mlab.clf()

pts = mlab.mesh(xyz[:,0], xyz[:,1], xyz[:,2])

pts.mlab_source.dataset.lines = np.array(G.edges())
tube = mlab.pipeline.tube(pts, tube_radius=0.01)
mlab.pipeline.surface(tube, color=(0.8, 0.8, 0.8))
mlab.show()
mlab.savefig('mayavi2_spring.png')
# mlab.show() # interactive window
