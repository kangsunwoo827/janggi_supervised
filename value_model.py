# %matplotlib inline

import logging
import config
import numpy as np
import keras
# import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import regularizers

# from loss import softmax_cross_entropy_with_logits

# import loggers as lg

import keras.backend as K

# from settings import run_folder, run_archive_folder

class Gen_Model():
	def __init__(self, reg_const, learning_rate, input_dim, output_dim):
		self.reg_const = reg_const
		self.learning_rate = learning_rate
		self.input_dim = input_dim
		self.output_dim = output_dim

	def predict(self, x):
		return self.model.predict(x)

	def fit(self, states, targets, epochs, verbose, validation_split, batch_size):
		return self.model.fit(states, targets, epochs=epochs, verbose=verbose, validation_split = validation_split, batch_size = batch_size)

	def write(self, sentense, version):
		self.model.save('{}value_model_version'.format(sentense) + "{0:0>4}".format(version) + '.h5')

	def read(self,path):
		return load_model(path)

	def printWeightAverages(self):
		layers = self.model.layers
		for i, l in enumerate(layers):
			try:
				x = l.get_weights()[0]
				# lg.logger_model.info('WEIGHT LAYER %d: ABSAV = %f, SD =%f, ABSMAX =%f, ABSMIN =%f', i, np.mean(np.abs(x)), np.std(x), np.max(np.abs(x)), np.min(np.abs(x)))
			except:
				pass
		# lg.logger_model.info('------------------')
		for i, l in enumerate(layers):
			try:
				x = l.get_weights()[1]
				# lg.logger_model.info('BIAS LAYER %d: ABSAV = %f, SD =%f, ABSMAX =%f, ABSMIN =%f', i, np.mean(np.abs(x)), np.std(x), np.max(np.abs(x)), np.min(np.abs(x)))
			except:
				pass
		# lg.logger_model.info('******************')


	def viewLayers(self):
		layers = self.model.layers
		for i, l in enumerate(layers):
			x = l.get_weights()
			print('LAYER ' + str(i))

			try:
				weights = x[0]
				s = weights.shape

				fig = plt.figure(figsize=(s[2], s[3]))  # width, height in inches
				channel = 0
				filter = 0
				for i in range(s[2] * s[3]):

					sub = fig.add_subplot(s[3], s[2], i + 1)
					sub.imshow(weights[:,:,channel,filter], cmap='coolwarm', clim=(-1, 1),aspect="auto")
					channel = (channel + 1) % s[2]
					filter = (filter + 1) % s[3]

			except:
	
				try:
					fig = plt.figure(figsize=(3, len(x)))  # width, height in inches
					for i in range(len(x)):
						sub = fig.add_subplot(len(x), 1, i + 1)
						if i == 0:
							clim = (0,2)
						else:
							clim = (0, 2)
						sub.imshow([x[i]], cmap='coolwarm', clim=clim,aspect="auto")
						
					plt.show()

				except:
					try:
						fig = plt.figure(figsize=(3, 3))  # width, height in inches
						sub = fig.add_subplot(1, 1, 1)
						sub.imshow(x[0], cmap='coolwarm', clim=(-1, 1),aspect="auto")
						
						plt.show()

					except:
						pass

			plt.show()
				
		# lg.logger_model.info('------------------')


class Residual_CNN(Gen_Model):
	def __init__(self, reg_const, learning_rate, input_dim,  output_dim, hidden_layers):
		Gen_Model.__init__(self, reg_const, learning_rate, input_dim, output_dim)
		self.hidden_layers = hidden_layers
		self.num_layers = len(hidden_layers)
		self.model = self._build_model()

	def residual_layer(self, input_block, filters, kernel_size):

		x = self.conv_layer(input_block, filters, kernel_size)

		x = Conv2D(
		filters = filters
		, kernel_size = kernel_size
		, data_format="channels_first"
		, padding = 'same'
		, use_bias=False
		, activation='linear'
		, kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)

		x = BatchNormalization(axis=1)(x)

		x = add([input_block, x])

		x = LeakyReLU()(x)

		return (x)

	def conv_layer(self, x, filters, kernel_size):

		x = Conv2D(
		filters = filters
		, kernel_size = kernel_size
		, data_format="channels_first"
		, padding = 'same'
		, use_bias=False
		, activation='linear'
		, kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)

		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)

		return (x)

	def value_head(self, x):

		x = Conv2D(
		filters = 1
		, kernel_size = (1,1)
		, data_format="channels_first"
		, padding = 'same'
		, use_bias=False
		, activation='linear'
		, kernel_regularizer = regularizers.l2(self.reg_const)
		)(x)


		x = BatchNormalization(axis=1)(x)
		x = LeakyReLU()(x)

		x = Flatten()(x)

		x = Dense(
			20
			, use_bias=False
			, activation='linear'
			, kernel_regularizer=regularizers.l2(self.reg_const)
			)(x)

		x = LeakyReLU()(x)

		x = Dense(
			1
			, use_bias=False
			, activation='tanh'
			, kernel_regularizer=regularizers.l2(self.reg_const)
			, name = 'value_head'
			)(x)



		return (x)

	def _build_model(self):

		main_input = Input(shape = self.input_dim, name = 'main_input')

		x = self.conv_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

		if len(self.hidden_layers) > 1:
			for h in self.hidden_layers[1:]:
				x = self.residual_layer(x, h['filters'], h['kernel_size'])

		vh = self.value_head(x)

		model = Model(inputs=[main_input], outputs=[vh])
		sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
		adam=keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
		model.compile(loss='mean_squared_error',
			optimizer=adam
			)

		return model

	def convertToModelInput(self, state):
		inputToModel =  state.BoardToInput #np.append(state.binary, [(state.playerTurn + 1)/2] * self.input_dim[1] * self.input_dim[2])
		inputToModel = np.reshape(inputToModel, self.input_dim) 
		return (inputToModel)






from game import Game, GameState
# from visualize import Visualize
from time import sleep
from gib2match import gib2match,dir2match,tot_match, match_str2dict
import pickle
from utils import make_action_space
import numpy as np
# dir2match('gib_raw')
# match_str=tot_match('gib_str')
# print(len(match_str))
# match_lst=match_str2dict(match_str)
# match_lst

def actions2policy(match_lst):
    tot_x=[]
    tot_y=[]
    action_space=make_action_space()
    eye=np.eye(len(action_space))
    for iter, match_info in enumerate(match_lst):
        action_lst=match_info['action_lst']
        if iter%500==0:
            print(iter)
        env=Game(match_info['초차림'], match_info['한차림'])
        state=env.gameState
        #input : 현 state에 대한 설명  output : action
        for i, action in enumerate(action_lst):
            num_turn=i+1
            tot_x.append(state.BoardToInput)
            action=''.join(s for s in action if s.isdigit())
            
            if len(action)!=4:
                action=None
            # else:
            #     if action[1]=='0':
            #         print(iter)

            tot_y.append(action_space.index(action))
            state, value, done, info=env.step(action)
        

    return tot_x, tot_y      





import config
import random
import numpy as np
import time
from utils import make_action_space
from keras.callbacks import ModelCheckpoint
import dill
import MCTS
import tensorflow as tf
import os
def value_learning(data):
	print('start_value_learning')
	tot_x=[]
	tot_y=[]
	for state in data:
		s=GameState(state[0],state[1])
		tot_x.append(s.newnewInput())
		tot_y.append(state[2])

	total_data=list(zip(tot_x,tot_y))
	
	training_states = np.array([row[0] for row in total_data],dtype=float)
	training_targets = np.array([row[1] for row in total_data],dtype=float)

	fit = model.fit(training_states, training_targets, epochs=1, verbose=1, validation_split=0.03, batch_size =256)

	print('NEW LOSS %s'% fit.history)

	model.printWeightAverages()

if __name__=='__main__':

	value_NN =Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (33,10,9), 1, config.HIDDEN_CNN_LAYERS)
	model=value_NN
	path = 'board-numTurn-Q-len1366975.pickle'
	with open(path, 'rb') as f:
		data=pickle.load(f)
	random.shuffle(data)
	# for iter in range(3):
	for i in range(14):
		# print('iter',iter)
		data_split=data[100000*i:100000*(i+1)]
		with tf.device("/gpu:0"):
			value_learning(data_split)
	model.write('newnewinput_', 1111)

	# model = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (29,10,9), 1,config.HIDDEN_CNN_LAYERS)
	# path='value_model_version9876.h5'
	# m_tmp = model.read(path)
	# model.model.set_weights(m_tmp.get_weights())
	# for i in range(10):
	# 	# print('iter',iter)
	# 	data_split=data[100000*i:100000*(i+1)]
	# 	with tf.device("/gpu:0"):
	# 		value_learning(data_split)
	# model.write('on9876_', 121)




	# path='board-numTurn-Q-len1366975.pickle'
	
	# path='short-btq'


	# tot_data=[]
	# for file in os.listdir(path):
	# 	print(file)
	# 	filepath='{}/{}'.format(path,file)
	# 	with open(filepath, 'rb') as f:
	# 		data = pickle.load(f)
	# 		tot_data.extend(data)
	
	# print(len(tot_data))
	
	# with open('total-short-btq-len{}'.format(len(tot_data)), 'wb') as f:
	# 	pickle.dump(tot_data, f)


	