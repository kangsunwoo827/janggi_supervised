from tensorflow.keras.models import Sequential, load_model, Model
import numpy as np
from game import Game,GameState
from utils import make_action_space
model=load_model('checkpoint-version-2-iter-164.h5')
env=Game()
state=env.gameState
print(state.board)
a=np.reshape(state.BoardToInput, (1,15,10,9)) 
pred=model.predict(a)
idx=np.argmax(pred)
action_space=make_action_space()
print(action_space[idx])
# for idx, value in enumerate(pred[0]):
#     print('action {} value is {}'.format(action_space[idx],value))


