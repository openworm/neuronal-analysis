import biodatamanager as dm

import katodata as kd

manager = dm.BioDataManager()

kato =  dm.BioDataset(
    name="The Kato Dataset",
    filepath=kd.data_location,
    annotation='Created 2016: Just another set of 5 worms',
    tags=['katodata'],
    autoload=True,
    readfunc=kd.load)
manager.new(kato)




