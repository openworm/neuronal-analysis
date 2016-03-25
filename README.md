# neuronal-analysis
Tools to produce, analyse and compare both simulated and recorded neuronal datasets

This repository is intended to capture the results of both performing analysis on the dynamics of c. elegans neurons that have been recorded, as well as analyzing the results of simulations of c. elegans neurons, and making the two comparable to each other.  While our current simulations of c. elegans neurons still leave out many important details and tuning, there is a lot to be learned from even making coarse grained comparisons between real dynamics and dynamics that can come from imprecise models.

## Analysis

In a separate repo, [progress was reported](https://github.com/openworm/CElegansNeuroML/issues/56#issuecomment-193942933) by @lukeczapla and @theideasmith in reproducing analysis via python code on existing data sets recorded from real c. elegans neurons:

**Sample fluorescence heatmap for 107 neurons**
![zimmer-scaled](https://cloud.githubusercontent.com/assets/6181116/13614157/1b8fc986-e53d-11e5-8ece-cb91fe4bce0c.jpg).

**PCA on Derivatives**
![derivative-manifolds](https://cloud.githubusercontent.com/assets/6181116/13614440/7cba4780-e53e-11e5-961f-9692897c908c.png)

They wrote:

>We also have some [code](https://gist.github.com/de0351c46c8e8ee9fe21) to deal with the[ Kato data](https://github.com/theideasmith/network/tree/master/Zimmer-Data-Analysis), which you can access at the link provided, in the folder _wbdata_. In that directory, if you `import transform.py as tf`, you can access a dictionary containing all of Katos data with `tf.wormData`. The dictionary contains calcium imaging data for five worms and is keyed by the original matlab file names as they were sent by Kato himself :). Each worm's data's contains timevector ‘tv’, neural activity traces uncorrected (‘deltaFOverF') and corrected for bleaching (‘deltaFOverF_bc’) as well as derivatives (‘deltaFOverF_deriv'). The identity of neurons is in the same order in the cell array ‘NeuronIds'. 

## Simulation

The same approach taken for recordings of real neurons can be applied to simulations.  While the real neurons were reporting a fluorescence change over time, and the simulations are outputting membrane potential (voltage), at the level of gross dynamics, because those [two variables are known to be related](https://en.wikipedia.org/wiki/Action_potential), they are comparable.

### Bottom-up
The OpenWorm project has been following a bottom-up approach to modeling the nervous system for some time.  The [c302 project](https://github.com/openworm/CElegansNeuroML/tree/master/CElegans/pythonScripts/c302) has been a rallying point for this.  

![c302 structure](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/images/c302.png)

Using the [LibNeuroML library](https://github.com/NeuralEnsemble/libNeuroML), combined with information about the name and connectivity of c. elegans neurons, we have built up a data structure that represents the nervous system of th ec. elegans, with details like the kinds of synapses, neurotransmitters, gap junction relationships it may have.  Then we can run the network as a simulation and see how the membrane potential might change over time.


![Simulation in jNeuroML](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/images/LEMS.png)


The project of identifying and modeling the dynamics of all the ion channels has been the work of the [ChannelWorm project](https://github.com/openworm/channelworm).  From there, the [Muscle model](https://github.com/openworm/muscle_model) has been our rallying point for a highly detailed single cell model that would use our detailed ion channel models first.  Beyond this, we have begun doing some work to improve the motor neurons and get the dynamics of the synapse between motor neurons and muscles corect.  At each level, we have endeavored to constrain the model with data.  Thus ion channel models [are constrained by and tuned with I/V curve information mined from the literature](https://channelworm.readthedocs.org/en/latest/optimization/).  The same can begin to be done with the muscle model.  While this is important infrastructure, there are still many gaps that are remaining.

### Top-down

With the advent of new experimental techniques to image hundreds of neurons at the same time, we now have another important kind of data to use to constrain the nervous system model.  We can begin to explore what are the minimum dynamical conditions that are necessary to produce, in broad strokes, the same kinds of high-level dynamics.  Even simplistic models of neurons hooked together with the c. elegans connectome will likely produce interesting investigations.

### Merging the Bottom-up with the Top-down

It is critical that the work of improving the nervous system model use all approaches, and result in a single unified model rather than a disconnected collection of models.  While it is acceptable to have different versions of the models temporarily, eventually these must all converge on a single picture of the nervous system.  To facilitate this, we have begun with modeling and computational infrastructure that is capable both of representing high-level and low-level aspects of the biophysics of neurons.  

# The future

Next steps for this exciting endeavor will be described in the issues on this repo.  As we collect scripts and code that are relevant to putting these pieces together, we will incorporate them here and make sure the community can execute them.
