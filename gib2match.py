import pickle
import os
def gib2match(path):
    with open(path, 'r',encoding='utf-8') as file:
        data = file.read()
        data = data.split('\n\n[')
    if len(data[-1])<10:
        print(path)
    # data=['\n\n'.join([data[2*i],data[2*i+1]]) for i in range(int(len(data)/2))]
    data = [match for match in data if '완승' in match or '시간승' in match]
    data = [match for match in data if not  '. i' in match]
    data = [match for match in data if not '접장기' in match]
    data = [match for match in data if not '구기보' in match]
    data = [match for match in data if not '한수' in match] 
    
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






def match_str2dict(match_str):

    # discount_ratio=0.9
    # tot_input=[]
    # tot_score=[]
    # tot_action=[]
    match_lst=[]
    for idx, match in enumerate(match_str):

        match=match.replace(']\n[','\n\n')
        split=match.split('\n\n')

        match_info={}
        match_info['match_idx']=idx

        action_str=split[-1]
        split=split[:-1]

        for line in split:
            start_idx=line.find('"')
            title=line[:start_idx-1]
            content=line[start_idx+1:]
            end_idx=content.find('"')
            content=content[:end_idx]
            match_info[title]=content

            

        # cho_form_idx=match.find('초차림')
        # cho_form=match[cho_form_idx+5:cho_form_idx+9]
        # han_form_idx=match.find('한차림')
        # han_form=match[han_form_idx+5:han_form_idx+9]

        # match_info['cho_form']=cho_form
        # match_info['han_form']=han_form

        # end_turn_idx=match.find('총수 "')
        # win_idx=match.find('[대국결과')
        # end_turn=match[end_turn_idx+4:win_idx-3]
        # win=match[win_idx+7:win_idx+8]
        # match_info['end_turn']=int(end_turn)
        
        # match_info['who_win']=win

        action_lst=[]

        
        action_lst=action_str.split('. ')
       
        action_lst=action_lst[1:]
        action_lst=[action[:6] for action in action_lst]
        action_lst=[''.join(s for s in action if s.isdigit()) for action in action_lst]


        match_info['action_lst']=action_lst
    
        
        try:
            match_info['총수']=int(match_info['총수'])
        except:
            match_info['총수']=int(len(action_lst))
        
        try:
            match_info['대국결과']=match_info['대국결과'][0]
        except:
            continue

        try:
            del(match_info['대회명'])
            del(match_info['회전'])
            del(match_info['대국일자'])
            del(match_info['대국장소'])
            del(match_info['초대국자'])
            del(match_info['한대국자'])
            del(match_info['제한시간'])
        except:
            pass

        if '초포진' in match_info.keys():
            match_info['초차림']=match_info['초포진']
            match_info['한차림']=match_info['한포진']
        
        match_lst.append(match_info)
   
    pickle.dump(match_lst, open( "match_lst_len{}.p".format(len(match_lst)), "wb"))
    return match_lst


if __name__=='__main__':
    dir2match()
    match_str=tot_match('gib_str')
    match_str2dict(match_str)