"""
KatoAnalyzer provides a comprehensive toolkit to make asking and answering
questions about the kato dataset much easier.
"""

import data_config as dc
import numpy as np
wormData = dc.kato.data()

# I hate the list comprehensions too. When we start doing serious analysis this wont happen
nname_to_index = [{wormData[i]['NeuronIds'][0][j]:j
                   for j in range(len(wormData[i]['NeuronIds'][0]))
                   if wormData[i]['NeuronIds'][0][j]!=None}
                  for i in range(5)]
neurons = [ set(filter(lambda x: x!=None, wormData[i]['NeuronIds'][0].values)) for i in range(5) ]

global_neurons = sorted(set.intersection(*neurons))

# Let's compute shared neurons in the dataset
from itertools import combinations
groupings  = [ i for i in combinations(range(5), r=2)]
local_neurons = {}
for i,j in groupings:
    ns_i = neurons[i]
    ns_j = neurons[j]
    local_neurons[(i,j)] = local_neurons[(j,i)] = set.intersection(set(ns_i), set(ns_j))

for i in range(5):
    groupings.append((i,i))
    local_neurons[(i,i)] = set.intersection(set(neurons[i]), set(neurons[i]))

def correlate(a,b):
  return np.dot(a, b.T)

def covariance(a,b):

def crosscorrelation(a,b):
    raise(NotImplementedError)
