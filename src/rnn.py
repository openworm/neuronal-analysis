'''
### Recurrent Neural Network representation of C. elegans neural timeseries data
Script to model C. elegans neural timeseries data,
and generate similar data, using a Recurrent
Neural Network (specifically, a long short term memory or LSTM network)

Inspired by
http://karpathy.github.io/2015/05/21/rnn-effectiveness/

Based on code from
https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py
'''

from keras.models import Sequential
from keras.layers import Layer
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
from keras.optimizers import RMSprop

import numpy as np
import random
import sys
import os

import theano
from theano import tensor as T, function, printing

import biodatamanager as dm

os.environ["THEANO_FLAGS"] = "mode=FAST_RUN,device=gpu,floatX=float32"

# Layer implementing a Gaussian mixture model
# Implementation follows 
# https://github.com/jrieke/lstm-biology/blob/master/prediction_stateful_mixture.ipynb
# and
# https://github.com/fchollet/keras/issues/1061
# Thanks to @jrieke for providing code and guidance

class GMMActivation(Layer):
    """
    GMM-like activation function.
    Assumes that input has (D+2)*M dimensions, where D is the dimensionality of the 
    target data. The first M*D features are treated as means, the next M features as 
    standard devs and the last M features as mixture components of the GMM. 
    """
    def __init__(self, M, **kwargs):
        super(GMMActivation, self).__init__(**kwargs)
        self.M = M

    def get_output(self, train=False):
        X = self.get_input(train)
        D = T.shape(X)[1]/self.M - 2
        # leave mu values as they are since they're unconstrained
        # scale sigmas with exp, s.t. all values are non-negative 
        X = T.set_subtensor(X[:,D*self.M:(D+1)*self.M], T.exp(X[:,D*self.M:(D+1)*self.M]))
        # scale alphas with softmax, s.t. that all values are between [0,1] and sum up to 1
        X = T.set_subtensor(X[:,(D+1)*self.M:(D+2)*self.M], T.nnet.softmax(X[:,(D+1)*self.M:(D+2)*self.M]))
        return X

    def get_config(self):
        config = {"name": self.__class__.__name__,
                  "M": self.M}
        base_config = super(GMMActivation, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

def gmm_loss(y_true, y_pred):
    """
    GMM loss function.
    Assumes that y_pred has (D+2)*M dimensions and y_true has D dimensions. The first 
    M*D features are treated as means, the next M features as standard devs and the last 
    M features as mixture components of the GMM. 
    """
    def loss(m, M, D, y_true, y_pred):
        mu = y_pred[:,D*m:(m+1)*D]
        sigma = y_pred[:,D*M+m]
        alpha = y_pred[:,(D+1)*M+m]

        return (alpha/sigma/np.sqrt(2. * np.pi)) * T.exp(-T.sum(T.sqr(mu-y_true),-1)/(2*sigma**2))

    D = T.shape(y_true)[1]
    M = T.shape(y_pred)[1]/(D+2)
    seq = T.arange(M)
    result, _ = theano.scan(fn=loss, outputs_info=None, 
    sequences=seq, non_sequences=[M, D, y_true, y_pred])
    return -T.log(result.sum(0))

def generate(seq, maxlen=1, bs=3, ep=5, output_iterations=10, num_mixture_components=10):
    # seq is a single sample, in the format (timesteps, features) !
    # TODO: expand code to support multiple samples, fed into model together as a batch
    # Cut the timeseries data (variable name 'seq') into semi-redundant sequence chunks of maxlen

    X = []
    y = []

    for i in range(0, len(seq) - maxlen):
        X.append(seq[i:i+maxlen])
        y.append(seq[i+maxlen])

    dim = len((X[0][0]))

    print("sequence chunks:", len(X))
    print("chunk width:", len(X[0]))
    print("vector dimension:", dim)
    print("number of mixture components:", num_mixture_components)

    X = np.array(X)
    y = np.array(y)
    
    # build the model: 2 stacked LSTM
    print('Build model...')
    model = Sequential()
    model.reset_states()
    model.add(LSTM((dim+2) * num_mixture_components, return_sequences=False, input_shape=(maxlen, dim)))
    model.add(Dense((dim+2) * num_mixture_components))
    
    model.add(GMMActivation(num_mixture_components))

    model.compile(loss=gmm_loss, optimizer=RMSprop(lr=0.001))

    # Train the model
    model.fit(X, y, batch_size=bs, nb_epoch=ep)

    # Generate timeseries
    x_seed = X[len(X)-1] #choose final in-sample data point to initialize model
    x_array = []
    x_array.append(x_seed)
    x = np.array(x_array)

    predicted = []
    for i in range(output_iterations):
        pred_parameters = model.predict_on_batch(x)[0]

        means = pred_parameters[:num_mixture_components * dim]
        sds = pred_parameters[(num_mixture_components * dim):(num_mixture_components * (dim+1))]
        weights = pred_parameters[(num_mixture_components * (dim + 1)):]

        print(means)
        print(sds)
        print(weights)

        means = means.reshape(num_mixture_components, dim)
        sds = sds[:, np.newaxis]
        weights = weights[:, np.newaxis]
        
        pred = weights * np.random.normal(means, sds)
        pred = np.sum(pred, axis=0)
        predicted.append(pred)

    return predicted



