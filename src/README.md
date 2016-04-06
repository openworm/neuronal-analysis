Here the structure and details of the neuronal-analysis source code will be enumerated. 

Dependencies:

- scipy
- pandas
- pyopenworm
- libneuroml
- c302/simulator

This needs to be a module, not a program. It should expose an interface such that it can be used as an engine that can be run anywhere. Eventually this could integrate with Geppeto, etc. 

Components: 

- **Data Management**: this set of classes deal with management of data. I hope this class can eventually become a standalone library to help scientists manage their datasets. Having a robust interface for managing data will be very important for this project because it is all about analysis and creation of large datasets - it will be used as a module and hence to ease people in we need a unified interface for dealing with data. 
    - Loading data and keeping track of all data relevant to a project
    - Annotating, labelling, sorting, classifying data
    - Saving data, using artificial filesystems to organize data

- **Data Analysis**: this set of classes should expose methods for the range of commonly used procedures for neural data analysis. Preferably using a method-chaining interface, the library should be very modular. 

- **Data Comparison**: 
