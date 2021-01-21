from MCTS import MCTS as mcts
from MCTS import Node, Edge

from game import Game, GameState
from visualize import Visualize
from value_model import Residual_CNN
import config
import numpy as np
import random




def simple_run(model):
    env=Game()
    root = Node(env.gameState)
    mc = mcts(root, 1)
    currentNode = mc.root

    done = 0
    value = 0
    window=Visualize(currentNode.state)
    while True:
        maxQ=-9999
        mc.appendLeaf(currentNode)
        for idx, (action, edge) in enumerate(currentNode.edges):
            #U : exploration term
            x=edge.outNode.state.newInput()
            Q = model.predict(np.reshape(x,(1,29,10,9)))[0]
        

            if Q > maxQ:
                maxQ = Q 
                simulationAction = action
                simulationEdge = edge
        print(maxQ)
        # (simulationAction,simulationEdge) = random.sample(currentNode.edges,1)[0]
        newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
        if newState.id not in mc.tree:
            node = Node(newState)
            mc.addNode(node)
        else:
            node = mc.tree[newState.id]
        window.show(newState)
        currentNode = simulationEdge.outNode
        if done:
            break

import time
def simulate_run(model,sim):
    env=Game()
    root = Node(env.gameState)
    mc = mcts(root, 1)
    window=Visualize(root.state)
    simulateCount=sim
    while True:
        currentNode = mc.root
        mc.appendLeaf(currentNode)
        l=time.time()
        for sim in range(simulateCount):
            breadcrumbs = []
            done = 0
            value = 0
            
            currentNode = mc.root
            while not currentNode.isLeaf():
                # print(currentNode.numTurn)
                maxQU=-9999
                
                tot_N = len(currentNode.edges)
                for action, edge in currentNode.edges:
                    tot_N = tot_N + edge.stats['N'] 

                for idx, (action, edge) in enumerate(currentNode.edges):
                   
                    Q = edge.stats['Q']
                    U = 0.1*np.sqrt(np.log(tot_N)/(1+edge.stats['N']))
                    if Q+U> maxQU:
                        maxQU = Q+U 
                        simulationAction = action
                        simulationEdge = edge
                    # print('action{}-Q={} U={} Q+U={}'.format(action,np.round(Q,2),np.round(U,2),np.round(Q+U,2)))
                    
                # print(maxQU)
                # print('===================================')
                newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn
                # window.show(newState)
                currentNode = simulationEdge.outNode
                breadcrumbs.append(simulationEdge)
            mc.appendLeaf(currentNode)
            x=currentNode.state.newInput()
            value=float(model.predict(np.reshape(x,(1,29,10,9))))
            for edge in breadcrumbs:
                edge.stats['N'] = edge.stats['N'] +1
                edge.stats['W'] += value
                edge.stats['Q'] = edge.stats['W'] / edge.stats['N']
        print(time.time()-l)

        #simulation이 끝난 후
        currentNode=mc.root
        maxn=-1
        Nlist=[edge[1].stats['N'] for edge in currentNode.edges]
        maxNlist=list(filter(lambda x : x[1].stats['N']==max(Nlist), currentNode.edges))
        print(Nlist)
        simulationAction,simulationEdge=random.choice(maxNlist)
        newState, value, done = currentNode.state.takeAction(simulationAction)
        window.show(newState)
        mc.root = mc.tree[newState.id]

































if __name__=='__main__':
    model = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (29,10,9), 1,config.HIDDEN_CNN_LAYERS)
    path='on9876_value_model_version0121.h5'
    m_tmp = model.read(path)
    model.model.set_weights(m_tmp.get_weights())
    simulate_run(model,600)