import numpy as np
import logging
import config

from utils import setup_logger,action_to_message

class Node():

	def __init__(self, state):
		self.state = state
		self.playerTurn = state.playerTurn
		self.numTurn =state.num_turn
		self.id = state.id
		self.edges = []
		self.checked = False

	def isLeaf(self):
		if len(self.edges) > 0:
			return False
		else:
			return True

class Edge():

	def __init__(self, inNode, outNode, action):
		self.id = '{}|{}'.format(inNode.state.id, outNode.state.id)
		self.inNode = inNode
		self.outNode = outNode
		self.numTurn= inNode.state.num_turn
		self.playerTurn = inNode.state.playerTurn
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

	def __init__(self, root, cpuct):
		self.root = root
		self.tree = {}
		self.cpuct = cpuct
		self.addNode(root)
	
	def __len__(self):
		return len(self.tree)

	def moveToLeaf(self):

		# lg.logger_mcts.info('------MOVING TO LEAF------')

		breadcrumbs = []
		currentNode = self.root

		done = 0
		value = 0
		# window=Visualize(currentNode.state)
		while True:
			# maxQU = -99999

			# Nb = 0
			# for action, edge in currentNode.edges:
			# 	Nb = Nb + edge.stats['N']

			# print(currentNode.edges)
			# for idx, (action, edge) in enumerate(currentNode.edges):
			# 	#U : exploration term	
			# 	U = self.cpuct * np.sqrt(Nb) / (1 + edge.stats['N'])
					
			# 	Q = edge.stats['Q']
				
			# 	if Q + U > maxQU:
			# 		maxQU = Q + U
			# 		simulationAction = action
			# 		simulationEdge = edge
			(simulationAction,simulationEdge) = random.sample(currentNode.edges,1)[0]
			newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
			# window.show(newState)
			currentNode = simulationEdge.outNode
			breadcrumbs.append(simulationEdge)
			if not currentNode.checked:
				break
		
		currentNode.checked=True
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

		currentPlayer = leaf.state.playerTurn

		for edge in breadcrumbs:

			edge.stats['N'] = edge.stats['N'] + 1
			discount_value=discount**(leaf.numTurn-edge.numTurn)
			edge.stats['W'] = edge.stats['W'] + value*discount_value
			edge.stats['Q'] = edge.stats['W'] / edge.stats['N']

	def addNode(self, node):
		self.tree[node.id] = node



from game import Game, GameState
cpuct=1
discount=0.99
maxstage=1
lasttime=time.time()
if __name__=='__main__':
	state=Game().gameState
	root = Node(state)
	root.checked=True
	mcts = MCTS(root, cpuct)
	# if (mcts == None) or (state.id not in mcts.tree):
	# 	mcts=buildMCTS(state)
	# else:
	# 	changeRootMCTS(state)
	mcts.appendLeaf(root)
	for i in range(20000):
		
		leaf, value, done, breadcrumbs = mcts.moveToLeaf()
		if done==0:
			mcts.appendLeaf(leaf)
		mcts.backFill(leaf, value, breadcrumbs)
		
		if len(breadcrumbs)>maxstage:
			print('stage{} 돌파 {}'.format(maxstage, time.time()-lasttime))
			lasttime=time.time()
			maxstage+=1
		
    
	