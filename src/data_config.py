import biodatamanager as dm
import katodata as kd
import os
import pandas as pd
import networkx as nx

projdir=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

manager = dm.BioDataManager()

kato_matlab =  dm.BioDataset(
    name="Kato Matlab",
    filepath=kd.data_location,
    annotation='Deprecated. Use Kato Dataset instead',
    tags=['katodata'],
    readfunc=kd.load,
    manager = manager)

kato = dm.BioDataset(
    name="Kato Pandas",
    filepath=projdir+'/data/katodata.pickle',
    readfunc=pd.read_pickle,
    writefunc=lambda flnm, data: data.to_pickle(flnm),
    annotation='Straight from the heads of five worms to your table',
    manager=manager,
    autoload=True)


connectome_excel=dm.BioDataset(                                
    name='Connectome Excel',                                   
    filepath=projdir+'/data/CElegansNeuronTables.xls',         
    readfunc=lambda flnm: pd.read_excel(flnm, sheetname=None), 
    writefunc=lambda flnm, data: data.write_excel(flnm),       
    annotation='The CElegans Connectome Excel',                
    manager=manager)                                           

def gen_connectome_graph():                                          
    __connectome = connectome_excel.data()                           
    interneurons = __connectome['Connectome']                        
    muscle = __connectome['NeuronsToMuscle']                         
    sensory = __connectome['Sensory']                                
                                                                     
    __connectome_network = nx.Graph()                              
                                                                     
    for row in xrange(interneurons.shape[0]):                        
        n_a = interneurons['Origin'][row]                            
        n_b = interneurons['Target'][row]                            
        num_connections = interneurons['Number of Connections'][row] 
        neurotransmitter = interneurons['Neurotransmitter'][row]     
        type_of_connection = interneurons['Type'][row]               
        __connectome_network.add_edge(n_a, n_b,                      
             type_of_connection = type_of_connection,                
             weight=num_connections,                                 
             neurotransmitter=neurotransmitter)                      
        #__connectome_network[n_a]['Type'] = 'InterNeuron'
        #__connectome_network[n_b]['Type'] = 'InterNeuron'
                                                 
#    for row in xrange(muscle.shape[0]):                              
#        n_a = muscle['Neuron'][row]                                  
#        n_b = muscle['Muscle'][row]                                  
#        num_connections = muscle['Number of Connections'][row]       
#        neurotransmitter = muscle['Neurotransmitter'][row]           
#                                                                     
#        __connectome_network.add_edge(n_a, n_b,                      
#             weight=num_connections,                                 
#             neurotransmitter=neurotransmitter)                      
#        #__connectome_network[n_b]['Type'] = 'Muscle'

    """for row in xrange(sensory.shape[0]):                             
        n_a = sensory['Neuron'][row]                                 
        __connectome_network[n_a]['Type'] = sensory['Landmark'][row] 
    """
    return __connectome_network                                      

connectome_networkx = dm.BioDataset(
    name='Connectome Networkx',
    filepath=projdir+'/data/connectome.pickle',
    genfunc=gen_connectome_graph,
    readfunc=nx.read_gpickle,
    writefunc=nx.write_gpickle,
    annotation='Networkx Connectome',
    manager=manager)
