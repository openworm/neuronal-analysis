import numpy as np
import os
import scipy.io as scio
import timeseries as ts

currdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_location = os.path.join(currdir, 'data/wbdata/')
print data_location
MAT_EXTENSION = '.mat'

# TODO: prevent "---" from getting into the list of neurons
def extract_nids_list(wormdata):
    nids = wormdata['NeuronIds'].transpose()
    total = []
    print wormdata['FlNm']
    for x in nids:
        for j in x:
            neuron_array = j[0]
            neurons = [ extract for n in neuron_array for extract in n if extract !='-'*3]
            total.append(neurons)

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
        data.dtype.names[i]: data[i].T
        for i in range(len(data.dtype.names))
    }
    keyed_data['NeuronIds']  = extract_nids_list(keyed_data)
    return keyed_data

def mat_dict_to_timeseries(mat_dict):
   """ Wraps all the timeseries in timeseries objects """
   neurons = mat_dict['NeuronIds']
   data = { key:ts.TimeSeries(series,nnames=neurons) \
   for key, series in mat_dict.iteritems() \
   if key != 'NeuronIds' and key != 'FlNm'}

   data['NeuronIds'] = np.array(mat_dict['NeuronIds'])
   data['FlNm'] = mat_dict['FlNm'][0]
   return data

def loadfiles(files):
   """ Puts scipy-io sourced matfiles into a cleaner, more structured form """
   datasets = [mat_dict_to_timeseries(load_matfile(filestr))
       for fname, filestr in files.iteritems()]

   return datasets


class KatoData:


    def __init__(self):

        files = {
            fname:readfile(os.path.join(data_location,fname))
            for fname in os.listdir(data_location)}
        print [(f) for f,k in files.iteritems()]
        self.wormData = loadfiles(files)
