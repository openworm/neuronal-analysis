import biodatamanager as dm

import katodata as kd
import os
import pandas as pd
manager = dm.BioDataManager()

kato_matlab =  dm.BioDataset(
    name="Kato Matlab  Dataset",
    filepath=kd.data_location,
    annotation='Deprecated. Use Kato Dataset instead',
    tags=['katodata'],
    readfunc=kd.load,
    manager = manager)

flnm = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/data/katodata.pickle'
kato = dm.BioDataset(
    name="Kato Dataset",
    filepath=flnm,
    readfunc=pd.read_pickle,
    writefunc=lambda flnm, data: data.to_pickle(flnm),
    annotation='Straight from the heads of five worms to your table',
    manager=manager)
