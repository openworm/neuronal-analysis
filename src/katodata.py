import numpy as np
import os
import scipy.io as scio
import pandas as pd
import biodatamanager as dm

currdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_location = os.path.join(currdir, 'data/wbdata/')
MAT_EXTENSION = '.mat'

def extract_nids_list(wormdata):
    nids = wormdata['NeuronIds'][0][0].transpose()
    total = []
    for x in nids:
        for j in x:
            neuron_array = j[0]
            neurons = [ extract 
                for n in neuron_array 
                for extract in n if extract !='-'*3]
            if len(neurons)==0: neurons=None

            total.append(neurons)
    
    return total

def readfile(fname):
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

    data=matfile['wbData']

    keyed_data = {
        data.dtype.names[i]: data[data.dtype.names[i]].T
        for i in range(len(data.dtype.names))
    }
    final = {}
    final['NeuronIds']  = extract_nids_list(data)
    final['deltaFOverF'] = keyed_data['deltaFOverF'][0][0]
    final['deltaFOverF_deriv'] = keyed_data['deltaFOverF_deriv'][0][0]
    final['deltaFOverF_bc'] = keyed_data['deltaFOverF_bc'][0][0]
    final['tv'] = np.array(keyed_data['tv'][0][0]).flatten()

    
    return final

def loadfiles(files):
   """ Puts scipy-io sourced matfiles into a cleaner, more structured form """
   datasets = [
       load_matfile(filestr)
       for fname, filestr in files.iteritems()]

   return datasets

def load(path):
    files = {
        fname:readfile(os.path.join(data_location,fname))
        for fname in os.listdir(path)
    }
    return pd.DataFrame(loadfiles(files)).T


filenames = os.listdir(data_location)

if __name__ =='__main__':
  mat = readfile(os.path.join(data_location, filenames[0]))
  data = mat['wbData']
  neurons = extract_nids_list(data)
  print neurons
