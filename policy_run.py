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


             # for num_turn in range(end_turn):    
        #     action=action_lst[num_turn]
        #     action=action[:5]
            
        #     num_turn+=1
        #     if win=='초':
        #         win_constant=1
        #     else:
        #         win_constant=0
        #     if '한수쉼' in action:
        #         action=None
        #         continue
        #     else:
        #         before=[int(i) for i in action[0:2]]
        #         after=[int(i) for i in action[3:5]]
        #         action=[before,after]
        #     next_action.append(action)
        #     new_state, value, done, _=env.step(action)
        #     # window.show(new_state)
        #     input=new_state.BoardToInput
        #     score=discount_ratio**(end_turn-num_turn)
        #     score*=(-1)**(num_turn+win_constant)
        #     input_lst.append(input)
        #     score_lst.append(score)

        # tot_input.append(input_lst)
        # tot_score.append(score_lst)
        # tot_action.append(next_action)
        # if num%50==0:
        #     print('총 {}중 iter {}'.format(len(data),num))



# for i in range(15):
#     data = pickle.load( open( 'gib_match_lst/match_lst_ver{}.p'.format(i),   "rb" ) )
#     tot_x,tot_y=actions2policy(data)
#     pickle.dump(tot_x, open( "gib_policy/policy_input_ver{}_len{}.p".format(i, len(tot_x)), "wb"))
#     pickle.dump(tot_y, open( "gib_policy/policy_output_ver{}_len{}.p".format(i, len(tot_y)), "wb"))
#     print('end ver{}'.format(i))
# #
# data = pickle.load( open( 'match_lst_len14797.p',   "rb" ) )
# tot_x,tot_y=actions2policy(data)
# pickle.dump(tot_x, open( "policy_input_len{}.p".format(len(tot_x)), "wb"))
# pickle.dump(tot_y, open( "policy_output_len{}.p".format(len(tot_y)), "wb"))
# for i in range(15):
#     pickle.dump(data[i*1000:(i+1)*1000], open( "match_lst_ver{}.p".format(i), "wb"))
#     print('iter',i)


# 




import config
from policy_model import Policy_Residual_CNN
import random
import numpy as np
import time
from utils import make_action_space

tot_x = pickle.load( open( "gib_policy\policy_input_ver0_len117658.p",   "rb" ) )
tot_y = pickle.load( open( "gib_policy\policy_output_ver0_len117658.p",   "rb" ) )
action_space=make_action_space()
eyes=np.eye(len(action_space))
tot_y = [eyes[action_idx] for action_idx in tot_y]
train_overall_loss=[]
train_policy_loss=[]
total_data=list(zip(tot_x,tot_y))

policy_NN =Policy_Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (15,10,9), 2451, config.HIDDEN_CNN_LAYERS)
model=policy_NN


for i in range(300):
    minibatch = random.sample(total_data, 4096)
    training_states = np.array([row[0] for row in minibatch],dtype=float)
    training_targets = {'policy_head': np.array([row[1] for row in minibatch],dtype=float)} 

    fit = model.fit(training_states, training_targets, epochs=config.EPOCHS, verbose=1, validation_split=0, batch_size = 32)
    print('NEW LOSS %s'% fit.history)

    train_overall_loss.append(round(fit.history['loss'][config.EPOCHS - 1],4))
    train_policy_loss.append(round(fit.history['policy_head_loss'][config.EPOCHS - 1],4)) 

    # plt.plot(self.train_overall_loss, 'k')
    # plt.plot(self.train_value_loss, 'k:')
    # plt.plot(self.train_policy_loss, 'k--')

    # plt.legend(['train_overall_loss', 'train_value_loss', 'train_policy_loss'], loc='lower left')

    # display.clear_output(wait=True)
    # display.display(pl.gcf())
    # pl.gcf().clear()
    # time.sleep(1.0)

    model.printWeightAverages()
    