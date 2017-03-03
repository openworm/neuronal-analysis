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

def spring_layout(y,t,w,k,n,d,T):                                         
  """                                                                 
  y: an (n*2,d) dimensional matrix where y[:n]_i                      
     is the position of the ith node in d dimensions                  
     and y[n:]_i is the velocity of the ith node                      
  w: (n,n) matrix of edge weights                                     
  """                                                                 
  print "ITERATION {}/{}".format(t,T)
  
  y = np.copy(y.reshape((n*2,d)))                                     
                                                                      
  # rj across, ri down                                                
  rs_from = np.tile(y[:n], (n,1,1))                                   
  # ri across, rj down                                                
  rs_to = np.transpose(rs_from, axes=(1,0,2))                         
  # directional distance between each r_i and r_j                     
  # dr_ij is the force from j onto i, i.e. r_i - r_j                  
  dr = rs_to - rs_from                                                
  # Used as a mask                                                    
  nd_identity = np.eye(n).reshape((n,n,1))                            
  # Physical distances between nodes                                  
  R = ma.array(                                                       
        np.sqrt(np.sum(np.power(dr, 2.), axis=2, keepdims=True)),     
        mask=nd_identity                                              
      )                                                               
  # Computing forces using the spring equation                        
  # this force equation is designed                                   
  # so that there is no potential                                     
  # energy when R = w                                                 
  F = -k*(R-w)                                                         
  Fnet = np.sum(F, axis=1)                                            
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

def simulate():

  kato = dc.kato.data()
  data = kato[0]["deltaFOverF_bc"].T

  mean = np.mean(data, axis=1, keepdims=True)
  standardized = (data-mean)
  correlation = data.dot(data.T)
  connectome = dc.connectome_networkx.data().to_directed()
  adjacency = nx.to_numpy_matrix(connectome)

  t = 10                         
  t_f = t*10                     
  t = np.linspace(0, t, num=t_f) 
  print t.shape
  N = adjacency.shape[0]
  w = adjacency*np.random.rand(N,N)*10
    
  r0 = np.random.rand(N,3)*10
  d = r0.shape[-1]                                 
  n = r0.shape[0] 
  v0 = r0*0.
  k=1.

  y0 = np.zeros((n*2,d))                          
  y0[:n] = r0                                      
  y0[n:] = v0 

  return sim_particles(t, r0,v0,w)

alreadysimulated = os.path.isfile("../data/spaceembedding1.npy")
                                                                 
if False:#alreadysimulated:
  rf = np.load("../data/spaceembedding1.npy")
else:
  rf = simulate()
  np.save(rf,"../data/spaceembedding.npy")

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#x = rf[:,:n,:]
#y = rf[:,:n,1]
#z = rf[:,:n,2]
#ax.scatter(x,y,z)

n = rf.shape[1]/2
pos = rf[-1,:n,:]
center = np.mean(pos, axis=0, keepdims=True)

dr = pos-center

R = np.sqrt(np.sum(dr**2, axis=1))
u = np.mean(R) 
#sigma = np.std(R)
#conds = R-u >= 0.7*sigma
#pos = pos[conds]
#R = R[conds]

colors = cm.viridis(R) 

import matplotlib.pyplot as plt

plt.plot(rf[0])
plt.plot(rf[1])
plt.plot(rf[2])
plt.show()

def visualize():
  from vispy import app, visuals, scene

  # build your visuals                                                
  Scatter3D = scene.visuals.create_visual_node(visuals.MarkersVisual) 
                                                                      
  # The real-things : plot using scene                                
  # build canvas                                                      
  canvas = scene.SceneCanvas(keys='interactive', show=True)           
                                                                      
  # Add a ViewBox to let the user zoom/rotate                         
  view = canvas.central_widget.add_view()                             
  view.camera = 'turntable'                                           
  view.camera.fov = 45                                                
  view.camera.distance = 10


  # plot
  p1 = Scatter3D(parent=view.scene)
  p1.set_gl_state('translucent', blend=False, depth_test=True)
  p1.set_data(pos, face_color=colors)
  p1.symbol = visuals.marker_types[10]

  # run
  app.run()

