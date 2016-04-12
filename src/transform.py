import matplotlib.pyplot as plt
from matplotlib import gridspec
import scipy.io as scio
import os
import sklearn.decomposition as deco
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import numpy as np

def graph_worm_overview(wormdata):
    """
    Wormdata as a dictionary
    """

    fields = ['deltaFOverF_deriv',
              'deltaFOverF_bc',
              'tv',
              'NeuronIds',
              'FlNm',
              'deltaFOverF']

    if wormdata.keys() != fields:
        raise TypeError("Passed wormdata lacks necessary fields")

    fig = plt.figure(figsize=(10,20))

    gs  = gridspec.GridSpec(3,1)

    deriv_ax = fig.add_subplot(gs[0,0])
    deriv_ax.set_title("Fluorescence Derivative")
    deriv_ax.pcolormesh(wormdata['deltaFOverF_deriv'].T)
    deriv_ax.axis('tight')

    bc_ax = fig.add_subplot(gs[1,0])
    bc_ax.set_title("Fluorescence Bleach Cancelled")
    bc_ax.pcolormesh(wormdata['deltaFOverF_bc'].T)
    bc_ax.axis('tight')

    f_over_f = fig.add_subplot(gs[2,0])
    f_over_f.set_title("Fluorescence Raw")
    f_over_f.pcolormesh(wormdata['deltaFOverF'].T)
    f_over_f.axis('tight')

    fig.tight_layout()

    return fig

def draw_worm_overview_graphs(data):
    for flnm,worm in data.iteritems():
        file = os.path.splitext(flnm)[0] + '.png'
        graph_worm_overview(worm).savefig(file, bbox_inches="tight")

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def scikit_pca(X, n_components=3):
        # PCA
        sklearn_pca = PCA(n_components=n_components)
        X_transf = sklearn_pca.fit_transform(X)
        return (sklearn_pca, X_transf)

def plot_manifolds():
    import dimensions_kit as dk
    dims = dk.dimensions(5)
    fig = plt.figure(figsize=(20,10))
    gs  = gridspec.GridSpec(3,2)
    i = 0
    for k,v in wormData.iteritems():
        x,y = dk.transform(dims, i)
        _, pca = scikit_pca(v['deltaFOverF_deriv'])

        ax = fig.add_subplot(gs[x,y], projection="3d")
        print "-"*30
        print pca
        ax.plot(pca[:,0], pca[:,1], pca[:,2])
        ax.set_title('PCA on fluorescence derivative')

        i+=1

    return fig

def c302_list(file):
    from lxml import etree
    xml = etree.parse(file)
    columns = xml.findall('.//OutputColumn')
    return map(lambda c: c.values()[0], columns)

