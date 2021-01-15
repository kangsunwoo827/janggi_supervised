# from game import Game, GameState
# from visualize import Visualize
from time import sleep
import pickle
import os
def gib2match(path):
    with open(path, 'r',encoding='utf-8') as file:
        data = file.read()
        data = data.split('\n\n')
    data = data[:-1]
    data=['\n\n'.join([data[2*i],data[2*i+1]]) for i in range(int(len(data)/2))]
    data = [match for match in data if  '완승' in match]
    data = [match for match in data if not  '. i' in match]
    
    pickle.dump(data, open( "gib_str/{}len{}.p".format(path[8:],len(data)), "wb" ) )
    return len(data)


def dir2match(dir='gib_raw'):
    num=0
    for file_name in os.listdir(dir):
        num+=gib2match('{}\{}'.format(dir,file_name))
    print(num)

def tot_match(dir='gib_str'):
    tot_match=[]
    for file_name in os.listdir(dir):
        matches = pickle.load( open( '{}\{}'.format(dir,file_name),   "rb" ) )
        for match in matches:
            if match in tot_match:
                continue
            tot_match.append(match)

    return tot_match

dir2match('gib_raw')
match_str=tot_match('gib_str')
print(len(match_str))



def gib_to_data(path='gibo2020.txt'):

    with open(path, 'r',encoding='utf-8') as file:
        data = file.read()
        data = data.split('\n\n')
        
    data = data[:-1]

    data=['\n\n'.join([data[2*i],data[2*i+1]]) for i in range(1163)]
    data = [match for match in data if  '완승' in match]
    data = [match for match in data if not  '. i' in match]
    num=0
    discount_ratio=0.9
    tot_input=[]
    tot_score=[]
    tot_action=[]
    for match in data:
        num+=1
        cho_form_idx=match.find('초차림')
        cho_form=match[cho_form_idx+5:cho_form_idx+9]
        han_form_idx=match.find('한차림')
        han_form=match[han_form_idx+5:han_form_idx+9]
        end_turn_idx=match.find('총수 "')
        win_idx=match.find('[대국결과')
        end_turn=match[end_turn_idx+4:win_idx-3]
        win=match[win_idx+7:win_idx+8]
        cho_form=''.join(['m' if i=='마' else 's' for i in cho_form])
        han_form=''.join(['m' if i=='마' else 's' for i in han_form])
        pan_lst=[]
        strend_idx=match.find('\n\n')
        action_str=match[strend_idx+2:]
        # print(action_str)
        env=Game(cho_form,han_form)
        # window=Visualize(env.gameState)
        action_lst=action_str.split('. ')
        action_lst=action_lst[1:]
        # action_lst=[action for action in action_lst]
        # print(action_lst)
        end_turn=int(end_turn)
        input_lst=[]
        score_lst=[]
        next_action=[]
        for num_turn in range(end_turn):
            action=action_lst[num_turn]
            action=action[:5]
            
            num_turn+=1
            if win=='초':
                win_constant=1
            else:
                win_constant=0
            if '한수쉼' in action:
                action=None
                continue
            else:
                before=[int(i) for i in action[0:2]]
                after=[int(i) for i in action[3:5]]
                action=[before,after]
            next_action.append(action)
            new_state, value, done, _=env.step(action)
            # window.show(new_state)
            input=new_state.BoardToInput
            score=discount_ratio**(end_turn-num_turn)
            score*=(-1)**(num_turn+win_constant)
            input_lst.append(input)
            score_lst.append(score)

        tot_input.append(input_lst)
        tot_score.append(score_lst)
        tot_action.append(next_action)
        if num%50==0:
            print('총 {}중 iter {}'.format(len(data),num))

    return [tot_input,tot_score,tot_action]

# import pickle
# import config
# from model import Residual_CNN
# import random
# import numpy as np
# import time
# from utils import make_action_space
# gib_2020_data=gib_to_data()

# # pickle.dump(gib_2020_data, open( "gib2020.p", "wb" ) )
# action_space=make_action_space()
# data = pickle.load( open( "gib2020.p",   "rb" ) )
# input_data=[d[:-1] for d in data[0]]
# input_data=[y for x in input_data for y in x]
# value_data=[d[:-1] for d in data[1]]
# value_data=[y for x in value_data for y in x]
# policy_data=[d[1:] for d in data[2]]
# policy_data=[action_space.index(y) for x in policy_data for y in x]
# policy_onehot=[]
# for index in policy_data:
#     onehot=np.zeros(2451)
#     onehot[index]=1
#     policy_onehot.append(onehot)

# total_data=list(zip(input_data,value_data,policy_onehot))

# train_overall_loss=[]
# train_value_loss=[]
# train_policy_loss=[]

# supervised_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, (15,10,9), 2451, config.HIDDEN_CNN_LAYERS)
# model=supervised_NN


# for i in range(200):
#     minibatch = random.sample(total_data, 2048)
#     training_states = np.array([row[0] for row in minibatch],dtype=float)
#     training_targets = {'value_head': np.array([row[1] for row in minibatch],dtype=float)
#                         , 'policy_head': np.array([row[2] for row in minibatch],dtype=float)} 

#     fit = model.fit(training_states, training_targets, epochs=config.EPOCHS, verbose=1, validation_split=0, batch_size = 32)
#     print('NEW LOSS %s'% fit.history)

#     train_overall_loss.append(round(fit.history['loss'][config.EPOCHS - 1],4))
#     train_value_loss.append(round(fit.history['value_head_loss'][config.EPOCHS - 1],4)) 
#     train_policy_loss.append(round(fit.history['policy_head_loss'][config.EPOCHS - 1],4)) 

#     # plt.plot(self.train_overall_loss, 'k')
#     # plt.plot(self.train_value_loss, 'k:')
#     # plt.plot(self.train_policy_loss, 'k--')

#     # plt.legend(['train_overall_loss', 'train_value_loss', 'train_policy_loss'], loc='lower left')

#     # display.clear_output(wait=True)
#     # display.display(pl.gcf())
#     # pl.gcf().clear()
#     # time.sleep(1.0)

#     model.printWeightAverages()
    
# supervised_NN.write('janggi', 9999)