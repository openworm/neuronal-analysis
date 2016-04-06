import numpy as np
import os
import scipy.io as scio

currdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_location = os.path.join(currdir, 'data/wbdata/')
print data_location
MAT_EXTENSION = '.mat'

def extract_nids_list(wormdata):
    nids = wormdata['NeuronIds'].transpose()
    total = []
    for x in nids:
        for j in x:
            for y in j:
                d = []
                if len(y)==0: total.append(None)
                else:
                    for n in y:
                        listed = n.tolist()
                        if len(listed)>0: d.append(listed[0] )
                    total.append(d)
    # I'm too lazy to figure out why
    # the lists come out with neuronids
    # nested, so I'm just going to
    # flatten it and hope the interpreter
    # will optimize for me
    
    return total

def readfile(fname):
    print(fname)
    _, ext = os.path.splitext(fname)
    if(ext!= MAT_EXTENSION):
        # We'll need better errorchecking and raising
        # I don't know the idiomatic way of doing this in 
        # python
        print("Error: Must pass Matfile")
        raise


    """
    Reads a matfile and throws an error if the file doesn't exist
    """
    try:
        matfile = scio.loadmat(fname)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        raise
    return matfile

def load_matfile(matfile):
    """Builds a dictionary from a matfile string"""

    data=matfile['wbData'][0][0]

    keyed_data = { 
        data.dtype.names[i]: data[i] 
        for i in range(len(data.dtype.names))
    }
    keyed_data['NeuronIds']  = extract_nids_list(keyed_data)
    return keyed_data

def loadfiles(files):
    
    datasets = { 
        fname: load_matfile(filestr) 
        for fname, filestr in files.iteritems()
    }
    
    return datasets


class KatoData:
          
    def __init__(self):
        
        files = {
            fname:readfile(os.path.join(data_location,fname))
            for fname in os.listdir(data_location)}
        print [(f) for f,k in files.iteritems()] 
        self.filedata = loadfiles(files)
        
    
    
        
        

        

