import numpy as np
import logging
import config
import tensorflow as tf
from utils import setup_logger,action_to_message, make_action_space, action_to_coord

class Node():

	def __init__(self, state):
		self.state = state
		self.numTurn =state.num_turn
		self.id = state.id
		self.edges = []

	def isLeaf(self):
		if len(self.edges) > 0:
			return False
		else:
			return True

class Edge():

	def __init__(self, inNode, outNode, action):
		# self.id = '{}|{}'.format(inNode.state.id, action)
		self.inNode = inNode
		self.outNode = outNode
		self.numTurn= inNode.state.num_turn
		self.action = action

		self.stats =  {
					'N': 0,
					'W': 0,
					'Q': 0
				}

from visualize import Visualize		
import time
import random
class MCTS():

	def __init__(self, root, cpuct, tree={}):
		self.root = root
		self.tree = tree
		self.cpuct = cpuct
		self.addNode(root)	
	
	def __len__(self):
		return len(self.tree)

	

	def newmoveToLeaf(self):

		# lg.logger_mcts.info('------MOVING TO LEAF------')

		breadcrumbs = []
		currentNode = self.root

		done = 0
		value = 0
		action_space=make_action_space()
		# window=Visualize(currentNode.state)
		
		# from collections import deque
		# history_que=deque( range(6), maxlen=6 )
		while True:
			allowedActions=currentNode.state.allowedActions()
			allowed_idx=[action_space.index(action) for action in allowedActions]
			
			mask=np.zeros(len(action_space))
			mask[allowed_idx]=1
			x=currentNode.state.BoardToInput
			action_pred = model.predict(np.reshape(x,(1,15,10,9)))
			# print(history_que)
			# if history_que[0]==history_que[4] and history_que[1]==history_que[5]:
			# 	ban_idx=history_que[2]
			# 	mask[ban_idx]=0
			
			action_pred += np.random.normal(0,1/10,len(action_space))
			action_pred=action_pred*mask
			pred_idx=np.argmax(action_pred)
			for action in allowedActions:
				after=action_to_coord(action)[1]
				if currentNode.state.board[after[0],after[1]]==(-7)*currentNode.state.playerTurn:
					kill_idx=action_space.index(action)
					pred_idx=kill_idx
			simulationAction = action_space[pred_idx]
			# history_que.append(pred_idx)
			# (simulationAction,simulationEdge) = random.sample(currentNode.edges,1)[0]
			newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
			if newState.id not in self.tree:
				node = Node(newState)
				self.addNode(node)
			else:
				node = self.tree[newState.id]
			newEdge = Edge(currentNode, node, simulationAction)
			currentNode.edges.append((simulationAction, newEdge))
			# window.show(newState)
			
			currentNode = newEdge.outNode
			breadcrumbs.append(newEdge)
			if done:
				break
			# if not currentNode.checked:
			# 	break
		
		# currentNode.checked=True
		return currentNode, value, done, breadcrumbs

	def moveToLeaf(self):

		# lg.logger_mcts.info('------MOVING TO LEAF------')

		breadcrumbs = []
		currentNode = self.root

		done = 0
		value = 0
		# window=Visualize(currentNode.state)
		while True:
			allowedActions=currentNode.state.allowedActions() 
			simulationAction=random.choice(allowedActions)

			# (simulationAction,simulationEdge) = random.sample(currentNode.edges,1)[0]
			newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
			if newState.id not in self.tree:
				node = Node(newState)
				self.addNode(node)
			else:
				node = self.tree[newState.id]

			newEdge = Edge(currentNode, node, simulationAction)
			currentNode.edges.append((simulationAction, newEdge))
			# window.show(newState)
			
			currentNode = newEdge.outNode
			breadcrumbs.append(newEdge)
			if currentNode.numTurn>100:
				for edge in breadcrumbs:
					if edge.stats['N']==0:
						try:
							del(self.tree[edge.outNode.id])
						except:
							pass

				breadcrumbs = []
				currentNode = self.root
				done = 0
				value = 0
				
			if done:
				
				break
			
		
		# currentNode.checked=True
		return currentNode, value, done, breadcrumbs

	def appendLeaf(self, leaf):
		allowedActions=leaf.state.allowedActions() 
		for idx, action in enumerate(allowedActions):
			newState, _, _ = leaf.state.takeAction(action)
			
			if newState.id not in self.tree:
				node = Node(newState)
				self.addNode(node)
			else:
				node = self.tree[newState.id]
			newEdge = Edge(leaf, node, action)
			leaf.edges.append((action, newEdge))



	def backFill(self, leaf, value, breadcrumbs):
		# lg.logger_mcts.info('------DOING BACKFILL------')

		for edge in breadcrumbs:

			edge.stats['N'] = edge.stats['N'] + 1
			discount_value=(-discount)**(leaf.numTurn-edge.numTurn-1)
			#value는 그 상황에 대한 그 턴의 플레이어가 느끼는 가치 (이겼으면 1)
			edge.stats['W'] = edge.stats['W'] - value*discount_value
			edge.stats['Q'] = edge.stats['W'] / edge.stats['N']

	def addNode(self, node):
		self.tree[node.id] = node



from game import Game, GameState
import pickle
from visualize import Visualize
from multiprocessing import Process, Manager
cpuct=1
discount=0.99
maxstage=1
import dill


def loop_simulate(mcts_arg):
		print('start simulate')
		mcts=mcts_arg
		i=1
		l=time.time()
		
		while True:
			leaf, value, done, breadcrumbs = mcts.newmoveToLeaf()
			mcts.backFill(leaf, value, breadcrumbs)
			i+=1
			print(i)
			if i%500==0:
				print('iteration{}-tree:{}'.format(i, len(mcts.tree)))
				
				print(time.time()-l)
				l=time.time()
				if len(mcts.tree)>800000:
					print('save mcts_tree')
					new_tree=[]
					for key in mcts.tree:
						for edge in mcts.tree[key].edges:
							edge=edge[1]
							new_tree.append([edge.outNode.state.board, edge.outNode.numTurn, edge.stats['Q']])
					with open('gibo_policy_len{}.pickle'.format(len(new_tree)), 'wb') as f:
						pickle.dump(new_tree, f)
					break


			
			
			# if len(breadcrumbs)>maxstage:
			# 	print('stage{} 돌파 {}'.format(maxstage, time.time()-lasttime))
			# 	lasttime=time.time()
			# 	maxstage+=1

def loop_test(mcts_arg):
	mcts=mcts_arg
	currentNode = root

	done = 0
	value = 0
	window=Visualize(currentNode.state)
	while True:
		
		mcts.appendLeaf(currentNode)
		# maxQ = -99999
		Qlist=[edge.stats['Q'] for (action, edge) in currentNode.edges]
		maxQlst=list(filter(lambda x : x[1].stats['Q']==max(Qlist), currentNode.edges))
		print(max(Qlist))
		simulationAction,simulationEdge=random.choice(maxQlst)
		# for idx, (action, edge) in enumerate(currentNode.edges):
		# # 	#U : exploration term	
		# # 	U = self.cpuct * np.sqrt(Nb) / (1 + edge.stats['N'])
				
		# 	Q = edge.stats['Q']

		# 	if Q > maxQ:
		# 		maxQ = Q 
		# 		simulationAction = action
		# 		simulationEdge = edge

		newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
		
		window.show(newState)
		
		currentNode = simulationEdge.outNode
		if done:
			break
# from value_model import Residual_CNN
# model = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (29,10,9), 1,config.HIDDEN_CNN_LAYERS)
# path='value_model_version9876.h5'
# m_tmp = model.read(path)
# model.model.set_weights(m_tmp.get_weights())

from policy_model import Policy_Residual_CNN
model =Policy_Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (15,10,9), 2450, config.HIDDEN_CNN_LAYERS)
path='gibo_policy0127.h5'
m_tmp = model.read(path)
model.model.set_weights(m_tmp.get_weights())


if __name__=='__main__':
	
	# if (mcts == None) or (state.id not in mcts.tree):
	# 	mcts=buildMCTS(state)
	# else:
	# 	changeRootMCTS(state)
	while True:
		# try:
		state=Game().gameState
		root = Node(state)
		mcts = MCTS(root, cpuct)
		# mcts.appendLeaf(root)
		loop_simulate(mcts)
		mcts=''
		# except:
		# 	continue

