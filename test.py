from tensorflow.keras.models import Sequential, load_model, Model
import numpy as np
from game import Game,GameState
from utils import make_action_space
env=Game()
state=env.gameState
print(state.board)

import time
import os
path='short-btq'
tot_data=[]
for file in os.listdir(path):
    filepath='{}/{}'.format(path,file)
    print('--')
    print(file)
    print ("last modified: %s" % time.ctime(os.path.getmtime(filepath)))
    # print ("created: %s" % time.ctime(os.path.getctime(filepath)))