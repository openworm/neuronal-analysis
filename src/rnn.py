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
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import os

import biodatamanager as dm

os.environ["THEANO_FLAGS"] = "mode=FAST_RUN,device=gpu,floatX=float32"

def generate(seq, maxlen=10, bs=128, ep=5, output_iterations=10):
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

	X = np.array(X)
	y = np.array(y)
	
	# build the model: 2 stacked LSTM
	print('Build model...')
	model = Sequential()
	model.add(LSTM(512, return_sequences=True, input_shape=(maxlen, dim)))
	model.add(Dropout(0.2))
	model.add(LSTM(512, return_sequences=False))
	model.add(Dropout(0.2))
	model.add(Dense(dim))
	model.add(Activation('softmax'))

	model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

	# Train the model
	model.fit(X, y, batch_size=bs, nb_epoch=ep)

	# Generate timeseries
	x_seed = X[len(X)-1] #choose final in-sample data point to initialize model
	x_array = []
	x_array.append(x_seed)
	x = np.array(x_array)

	generated = []
	for i in range(output_iterations):
	    pred = model.predict(x, verbose=0)[0].tolist()

	    #drop oldest data in x, and append predicted data for feedforward into model
	    j = []
	    x = []
	    for i in range(1, len(x_seed)):    
	        j.append(x_seed[i])
	    j.append(pred)
	    x = []
	    x.append(j)
	    x = np.array(x)
	    generated.append(pred)

	return np.array(generated)