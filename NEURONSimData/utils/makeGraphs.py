from pylab import *
from os import walk

neuronNames = [
  "I1L",
  "M1"
]
segments = [0]

def getData(fname):
  vec = []
  with open('../data/'+fname, 'r') as f:
    for line in f:
      if len(line) > 1:
        vec.append(float(line))
  f.closed
  
  return vec
  
_,_,allfiles = walk('../data').next()

for seg in range(0,99):
  fileset = []
  for fname in allfiles:
    if fname[-5:] == str(seg)+'.dat':
      fileset.append(fname)
      
  if len(fileset) < 1:
    break

  for fname in fileset:
    vData = getData(fname)
    plot(vData)
  title(str(len(fileset)) + " neurons, segment " + str(seg))
  ylabel('mV')
  xlabel('steps')
  savefig('../graphs/allNeurons_seg'+str(seg)+'.png')
  clf()
  