"""
Topics to be explored:
- Lattice Approximations of Continuous Space Manifolds
- Finding an embedding of a neural network in R^3
- Neural Field Models for particle dynamics and stochastic
  dynamics on neural manifolds
- Intrinsic Dimensionality of a Graph

An idea that occurred to me yesterday relates to the
"*planar dimensionality of a graph*" which means the
minimal number of dimensions necessary in which to
project the graph such that no edges intersect with
eachother. For example, the intrinsic dimensionality
of a planar graph is $2$. A graph for which intersections
only exist between one single node $n_i$ and any number
of other nodes $n_j, j\ne i$, embedding this graph in
3 dimensional will remove any line intersections simply
by the definition of a line emanating from a point
(because the only place the line segments representing
edges intersect is at the node itself and therefore
they intersect nowhere else).

Once you can find the dimensionality of a graph as well
as an appropriate embedding of the graph in those
dimensions (using someforce based spring layout model) then things get interesting.

If the graph has intrinsic dimensionality $n$, by
projecting the graph into dimensions $n+1$ and
force laying out the graph in these dimensions
you obtain LATTICE APPROXIMATION OF A CONTINUOUS SPACE CURVE.
The position of a node along dimension $n+1$
converges such that the euclidean distance between
any two nodes in this $n+1$ space is exactly equal to
their edges distance.

**Now we have found the most perfect intrinsic spatial
embedding of a graph** because:
1. The distance between all the nodes in this space is
   exactly equal to the weight of their edges
2. The space approximation created by the graph lattice is continuous.

*NOW* we can start playing with the physics of this high
dimensional graph manifold, for example, by fitting
a field function to the data
"""

import sys
import numpy as np
import scipy.cluster.hierarchy as sch
import pylab
import scipy
import matplotlib.pyplot as plt
import networkx as nx
import numpy.ma as ma
from scipy.integrate import odeint


import matplotlib.cm as cm

import os
import sys
import numpy as np
import scipy.stats

sys.path.append('../src/')
import data_config  as dc

"""
By embedding a graph in 3+1 dimensions
we can find a continuous surface on which the
network lives

This is enabled by a theorem in network science
that the probability of edge collisions
for a graph embedded in three dimensions is
zero
"""

import numpy as np
import numpy.ma as ma
from scipy.integrate import odeint
import cv2

def get_dr(y):
    n = y.shape[0]
    # rj across, ri down
    rs_from = np.tile(y, (n,1,1))
    # ri across, rj down
    rs_to = np.transpose(rs_from, axes=(1,0,2))
    # directional distance between each r_i and r_j
    # dr_ij is the force from j onto i, i.e. r_i - r_j
    dr = rs_to - rs_from
    dr = dr.astype(np.float32)
    return dr
def get_radii(y):

    dR = get_dr(y)
    R = np.array(
      np.power(
        np.sum(np.power(dR, 2.), axis=2),
        1./2.
      )
    ).astype(np.float32)
    return R

def spring_layout(y,t,w,k,n,d,T):
  """
  y: an (n*2,d) dimensional matrix where y[:n]_i
     is the position of the ith node in d dimensions
     and y[n:]_i is the velocity of the ith node
  w: (n,n) matrix of edge weights
  """
  y = np.copy(y.reshape((n*2,d)))
  x = y[:n]
  v = y[n:]
  dR = get_dr(x)

  # F=0 <=> R=w
  # we also add a damping term
  F = -k*(dR-w*dR/(np.linalg.norm(dR)))
  Fnet = np.sum(F, axis=1) - v
  a = Fnet #nodes have unit mass
  # Setting velocities
  y[:n] = np.copy(y[n:])
  # Entering the acceleration into the velocity slot
  y[n:] = np.copy(a)
  # Flattening it out for scipy.odeint to work
  return np.array(y).reshape(n*2*d)

def sim_particles(t, r, v, w, k=1.):

    d = r.shape[-1]
    n = r.shape[0]

    y0 = np.zeros((n*2,d))
    y0[:n] = r
    y0[n:] = v
    y0 = y0.reshape(n*2*d)

    w = np.array([w]).reshape( (w.shape[0], w.shape[1], 1) )
    yf = odeint(
        spring_layout,
        y0,
        t,
        args=(w,k,n,d, t.shape[0])).reshape(t.shape[0],n*2,d)

    return yf

def get_data():
    kato = dc.kato.data()
    data = kato[0]["deltaFOverF_bc"].T

    mean = np.mean(data, axis=1, keepdims=True)
    standardized = (data-mean)
    correlation = data.T.dot(data)
    connectome = dc.connectome_networkx.data().to_directed()
    adjacency = nx.to_numpy_matrix(connectome)
    return {
        "data": data,
        "correletion": correlation,
        "adjacency": adjacency,
        "network":connectome
    }

def simulate():
  data = get_data()

  adjacency = data["adjacency"]
  t = 10
  t_f = 100
  t = np.linspace(0, t, num=t_f).astype(np.float32)

  # a = 0.
  # b = 100.
  # r = np.array([
  #     [a, 0.],
  #     [a+2.,0.],
  # ])
  # v = np.array([
  #     [0.,10.],
  #     [0., -10.],
  # ])
  #
  # w = np.array([
  #   [0,1],
  #   [1,0]
  # ]).astype(np.float32)

  n = 5
  G = nx.grid_2d_graph(n,n)
  N = 25
  w = nx.to_numpy_matrix(G)*10
  r = np.random.rand(N,3)
  d = r.shape[-1]
  v = r*0.
  k=1.
  return sim_particles(t,r,v,w)

if __name__=="__main__":
    alreadysimulated = os.path.isfile("../data/spaceembedding.npy")

    if False:#alreadysimulated:
      rf = np.load("../data/spaceembedding.npy")
    else:
      rf = simulate()
      np.save("../data/spaceembedding.npy",rf)

    data = get_data()

    H = nx.grid_2d_graph(5,5)
    pos = np.array(nx.spring_layout(H, dim=3).values())#
    pos = rf[-1,:25]

    from mayavi import mlab

    # reorder nodes from 0,len(G)-1
    G=nx.convert_node_labels_to_integers(H)

    scalars=np.array(G.nodes())+5

    mlab.figure(1, bgcolor=(0, 0, 0))
    mlab.clf()

    pts = mlab.points3d(pos[:,0], pos[:,1], pos[:,2],
                        scalars,
                        scale_factor=0.01,
                        scale_mode='none',
                        colormap='Blues',
                        resolution=20)

    pts.mlab_source.dataset.lines = np.array(G.edges())
    tube = mlab.pipeline.tube(pts, tube_radius=0.01)
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0.8))

    mlab.savefig('mayavi2_spring.png')
    mlab.show() # interactive window
