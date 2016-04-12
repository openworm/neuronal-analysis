import biodatamanager as dm

import katodata as kd
import os
manager = dm.BioDataManager()

katomat =  dm.BioDataset(
    name="The Kato Matlab  Dataset",
    filepath=kd.data_location,
    annotation='Created 2016: Just another set of 5 worms',
    tags=['katodata'],
    autoload=True,
    readfunc=kd.load,
    manager = manager)

"""
kato = dm.BioDataset(
    name="Kato Dataset",
    filepath='../data/katodata.sql',
    readfunc=
    writefunc=
    manager=manager)
"""
