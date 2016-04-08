import warnings
import os
import types

def load(configfile):
    # check if file exists
    # check if it will fit in memory?
    # x <- read(file)
    # Throw that error
    # return x
    raise NotImplementedError


class BioDataset():
    """
    This is an abstract class for implementing
    """
    def __init__(
      self
    ,  readfunc=None
    , writefunc=None
    , name ='Anonymous Dataset'
    , filepath=None
    , dataset=None
    , annotation='No annotation given'
    , tags=[]
    , autoload=False):

        self.__cache = dataset
        self.__reader = readfunc
        self.__writer = writefunc
        
        self.filepath = filepath
        self.tags = set(tags)
        self.annotation = annotation
        self.name = name

        if autoload == True: 
           self.retrieve()
        
    
    def retrieve(self):
        assert hasattr(self.__reader, '__call__') 
        
        """ Retrieve the dataset. 
        If it's already in memory, nothing happens. 
        If it is not in memory, it will be loaded into memory
        """
        if self.__cache != None: return self.__cache
        
        dataset_path = self.filepath
        if not os.path.exists(dataset_path):
            raise(OSError, 'File for dataset {0} does not exist'.format(dataset))

        self.__cache = self.__reader(self.filepath)
        return self

    def write(self):
        assert hasattr(self.__writer)
        # We can't write if the dataset hasn't been loaded
        if self.__cache == None: return

        self.__writer(self.__cache)
        return self

    def flush(self):
        # Flushes the cache. Maybe the file has changed
        # and we need to reload
        self.__cache = None
        return self

    def data(self):
        # Allow user to retrieve the cache
        return self.__cache

class BioDataManager():
    """
    (Inspired by BioParameter from c302)
    BioDataManager is the interface for all project related
    fileIO. Because we'll be dealing with lots of data which would
    otherwise be scattered about the project, BioDataManager
    creates a central data management authority where all the
    different datasets are tracked.
    It is meant to simplify managing, annotating, dating,
    reading and writing all project related data.

    At this point, a BioDataManager has two primary variables:

    config: containing dataset metadata
    loaded_datasets: structured datasets loaded into memory
                for computational use.

    Methods:
        information(dataset1, ..., datasetn): If nothing passed will return
            global dataset overview. Otherwise return an array containing
            information specific to the datasets of interest
        load_dataset(name, loader): loads dataset "name" into memory
            and builds a structured representation of it using
            loaderfunc.

    """
    def __init__(self):
        self.datasets = {}
        self.tags = set()

    def new(self, biodataset):

        assert isinstance(biodataset, BioDataset)   

        """
        Makes BioDataManager aware of this dataset.
        Won't throw an error if the file for the dataset doesn't exist.
        """

        if(self.__dataset_exists(biodataset.name)):
            warnings.warn('Cannot add existing dataset', RuntimeWarning)
            return
        
        self.datasets[biodataset.name] = biodataset
        self.tags.update(biodataset.tags)
        return self

    def __dataset_exists(self, dataset):
        return dataset in self.datasets

    def __assert_dset(self, dataset, warning='Requested dataset does not exist'):
        exists = self.__dataset_exists(dataset)
        if not exists:
            raise(IndexError, warning)
