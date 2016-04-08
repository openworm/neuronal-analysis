def load(configfile):
    # check if it will fit in memory?
    # x <- read(file)
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

    def __init__(self.configfile):
        # @private
        self.config = load(configfile)

        # self.loaded_datasets = ?

    def information():
        """
        Provides an overview of datasets, dates created, annotations, etc.
        """
        raise NotImplementedError


    def load_dataset(dataset, loader):
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

        raise NotImplementedError

    def metadata(dataset):
        """
        Returns metadata for "dataset"
        """
        raise NotImplementedError


    def annotate(dataset, annotation):
        """
        Adds to a list of annotations for "dataset"
        """
        raise NotImplementedError

    def tag(dataset, tag):
        """ Tag a data for easy grouping """
        raise NotImplementedError
