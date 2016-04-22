import warnings
import os
import types
import weakref

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
    , readfunc=None
    , writefunc=None
    , filepath=''
    , genfunc=None
    , name = None
    , dataset=None
    , annotation='No annotation given'
    , tags=[]
    , autoload=False
    , dependencies=[]
    , manager = None):
        """
        Creates a BioDataset instance
        I want this to eventually become a make-like utility
        for scientific data-management.

        To do that, we'll need a dependency resolver.
        Dependency resolver:
        http://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/
        """

        if not name:
            raise TypeError('Cannot create anonymous dataset')

        self.__cache = dataset

        # We should really do dependency
        self.__reader = readfunc
        self.__writer = writefunc
        self.__generator = genfunc

        self.filepath = filepath
        self.tags = set(tags)
        self.annotation = annotation
        self.name = name
        self.dependencies = dependencies
        if autoload == True:
           self.data()


        if isinstance(manager,BioDataManager):
            manager.new(self)
            self.__manager = weakref.ref(manager)

    def data(self):
        assert hasattr(self.__reader, '__call__')

        """ Retrieve the dataset.
        If it's already in memory, nothing happens.
        If it is not in memory, it will be loaded into memory
        """
        if not self.__cache is None: return self.__cache

        dataset_path = self.filepath
        path_exists = os.path.exists(dataset_path)
        # If the file doesn't exist and we have
        # no generator, then quit
        if not path_exists and self.__generator==None:
            raise OSError('No file or path to retrieve {0}'.format(dataset_path))
        # If file doesn't exist and we do have a generator
        # then generate
        elif not path_exists and self.__generator!=None:
            cache = self.__generator()
            self.__cache = cache
        # If file does exist, then generate it
        else:
            self.__cache = self.__reader(self.filepath)
        return  self.__cache

    def write(self):

        """
        Writes the dataset if it is in the cache
        and a writefunc was supplied
        """
        assert hasattr(self.__writer)
        # We can't write if the dataset hasn't been loaded
        if self.__cache == None: return

        self.__writer(self.filepath,self.__cache)

    def flush(self):
        # Flushes the cache. Maybe the file has changed
        # and we need to reload
        self.__cache = None
        return self

    def loaded(self):
        return  not self.__cache is None

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
    def __repr__(self):
        keys = self.datasets.keys()
        annotations = [ds.annotation for k, ds in self.datasets.iteritems()]

        string = '::BioDataManager Instance::\n'

        for i in range(len(keys)):
            string += '{0}: {1}\n'.format(keys[i], annotations[i])
        return string

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

    def request(dataset):
        if not  __dataset_exists(dataset):
            raise IndexError('Dataset {0} doesn\'t exist'.format(dataset))

        return self.datasets[dataset]


    def __dataset_exists(self, dataset):
        return dataset in self.datasets

    def __assert_dset(self, dataset, warning='Requested dataset does not exist'):
        exists = self.__dataset_exists(dataset)
        if not exists:
            raise IndexError(warning)
