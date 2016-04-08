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
        self.__dataset_metadata={}
        self.__tags = set()
        self.__datasets_in_memory={}

    def information(self):
        """
        Provides an overview of datasets, dates created, annotations, etc.
        """
        return self.__dataset_metadata

    def new_dataset(self
        , name
        , location
        , loader
        , annotation='No annotation given'
        , tags=[]):

        """
        Makes BioDataManager aware of this dataset.
        Won't throw an error if the file for the dataset doesn't exist.
        """

        if(self.__dataset_exists(name)):
            warnings.warn('Cannot add existing dataset', RuntimeWarning)
            return

        assert hasattr(loader, '__call__')
        assert isinstance(name, types.StringType) or isinstance(name, types.IntType)
        assert isinstance(location, types.StringType)
        assert isinstance(annotation, types.StringType)
        assert isinstance(tags, types.ListType)

        tagset = set(tags)

        metadata = {
            'name': name,
            'annotation': annotation,
            'tags': tagset,
            'location': location,
            'loaderfunction': loader
        }
        self.__dataset_metadata[name] = metadata
        self.__tags.update(tagset)
        return self

    def metadata(self, dataset):
        """
        Returns metadata for "dataset"
        """
        self.__assert_dset(dataset)
        # assert metadata in self.__dataset_metadata[dataset]
        return dict(self.__dataset_metadata[dataset])

    def retrieve(self, dataset):
        """ Returns the dataset in memory """
        self.__load_dataset(dataset)
        return self.__datasets_in_memory[dataset]

    def __load_dataset(self, dataset, forcereload=False):
        """
        1. check if "dataset" belongs in config
          if it doesn't, crash and ask the user to setup
          their config first
        2. check if the dataset file exists
          if it doesn't, report this to the user.
          Alternatively it would be cool to implement some Make like
          facility for scientists. Where you can define dependencies among
          scripts and let the code run them for you.
        3. If the dataset is in config, then:
            - Load the dataset into memory
            - Use the loader function to turn it into
              a data structure.
            - Add that datastructure to self.datasets
        """


        # Confirming the dataset does in fact exist
        self.__assert_dset(dataset)

        # Confirming the file for the dataset exists
        # If no path exists, assume dataset cannot be
        dataset_path = self.__dataset_metadata[dataset]['location']
        if not os.path.exists(dataset_path):
            raise(OSError, 'File for dataset {0} does not exist'.format(dataset))

        loaderfunc = self.__dataset_metadata[dataset]['loaderfunction']

        # Don't do anything if we've already loaded this dataset
        if forcereload == False and dataset in self.__datasets_in_memory:
            return


        self.__datasets_in_memory[dataset] = loaderfunc(dataset_path)

        return

    def __nonexistent_datasets(self, ):
        """ Returns a list of datasets whos files do not exist """

    def __dataset_exists(self, dataset):
        return dataset in self.__dataset_metadata

    def __assert_dset(self, dataset, warning='Requested dataset does not exist'):
        exists = self.__dataset_exists(dataset)
        if not exists:
            raise(IndexError, warning)
