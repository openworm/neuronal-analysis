Here the structure and details of the neuronal-analysis source code will be enumerated. 

Dependencies:

- scipy
- pandas
- pyopenworm
- libneuroml
- c302/simulator

This needs to be a module, not a program. It should expose an interface such that it can be used as an engine that can be run anywhere. Eventually this could integrate with Geppeto, etc. 

Components: this library should be modelled with sklearn's design patterns in consideration. 

- **Data Management**: this set of classes deal with management of data. I hope this class can eventually become a standalone library to help scientists manage their datasets. Having a robust interface for managing data will be very important for this project because it is all about analysis and creation of large datasets - it will be used as a module and hence to ease people in we need a unified interface for dealing with data. 
    - Loading data and keeping track of all data relevant to a project
    - Annotating, labelling, sorting, classifying data
    - Saving data, using artificial filesystems to organize data
- **Data Analysis**: this set of classes should expose methods for the range of commonly used procedures for neural data analysis. Preferably using a method-chaining interface, the library should be very modular.
    - Tie together different analytical methods. 

- **Data Comparison**: 
    - Implement novel techniques for comparison of neural time series in relation to graph structure. 
    - Harnessing **`Data Analysis`**, **`Data Comparison`** will provide an interface for conducting arbitrary statistical 
      tests on data. 
- **Plotting**: 
    - The library should implement novel plotting capabilities
    - Make it very easy to compare across arbitrary axes in a dataset.
- **Experiment Management**: an interface for documenting an experiment in the code itself
    - Underneath it would just be a dictionary building class. 
    - Lots of potential use cases for this.
- **Connectome**: for accessing, clustering, getting data from the static OpenWorm connectome
