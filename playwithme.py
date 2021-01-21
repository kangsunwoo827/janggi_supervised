from game import Game, GameState
from visualize import Visualize
from value_model import Residual_CNN
import config
import numpy as np
import random

def playwithme(model,turn):
    env=Game()
    window=Visualize(env.gameState)
    window.show(env.gameState)
    while True:
        if turn==env.gameState.playerTurn:
            while True:
                action=window.wait_click()
                if action != None:
                    break
            env.step(action)

        else:
            
            maxQ=-9999
            
            for idx, action in enumerate(env.gameState.allowedActions()):
                x=env.gameState.newInput()
                Q = model.predict(np.reshape(x,(1,29,10,9)))[0]

                if Q > maxQ:
                    maxQ = Q 
                    selectAction = action
            env.step(selectAction)

        window.show(env.gameState)





if __name__=='__main__':
    model = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (29,10,9), 1,config.HIDDEN_CNN_LAYERS)
    path='value_model_version9876.h5'
    m_tmp = model.read(path)
    model.model.set_weights(m_tmp.get_weights())
    playwithme(model,1)