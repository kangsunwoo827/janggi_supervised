#!/usr/bin/env python
# coding: utf-8

#장기
import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy
# Colors
#				 R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (200,  72,  72)
LIGHT_ORANGE = (198, 108,  58)
ORANGE       = (180, 122,  48)
GREEN        = ( 72, 160,  72)
BLUE         = ( 66,  72, 200)
YELLOW       = (162, 162,  42)
NAVY         = ( 75,   0, 130)
PURPLE       = (143,   0, 255)
JANG         = (220, 179,  92)
BACK         = (245, 225, 195)

# 화면에 대한 하이퍼 파라미터

FPS = 30
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 640
TOP_MARGIN = 200
MARGIN = 40
POINT_WIDTH = 9
POINT_HEIGHT= 10

GRID_SIZE = WINDOW_WIDTH - 2 * (MARGIN)

HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)

CELL_SIZE = int(GRID_SIZE/(POINT_WIDTH-1)) 



Pieces_list=[None,'jol','sa','sang','ma','po','cha','wang']

wait_time = 1


class Pieces(pygame.sprite.Sprite):
    def __init__(self,team,name_num,x,y,sizex,sizey):
        #team 0 = cho and 1 = han
        if team==0:
            self.team='cho'
            self.color=GREEN
        else:
            self.team='han'
            self.color=RED

        name=Pieces_list[name_num]

        self.x, self.y=x,y
        self.sizex=sizex
        self.sizey=sizey

        self.image = pygame.image.load("C:/Users/Sunny.LAPTOP-L010FOP1/Desktop/piece_img/"+self.team+name+'.png').convert_alpha()

        self.scale_image=pygame.transform.scale(self.image, (sizex,sizey))

    def draw(self):
        DISPLAYSURF.blit(self.scale_image, (self.x, self.y))


class Can_go(pygame.sprite.Sprite):
    def __init__(self,mark,before_y,before_x,gameboard,turn):
        self.marker=mark
        self.before=(before_y,before_x)
        self.gameboard=gameboard
        self.turn=turn
        self.in_gung=False

    #갈 수 있는 모든 위치 얻기
    def get_go(self,marker,before,gameboard):
        go_list=[]
        self.in_gung=False

        if marker==2 or marker==7:
            self.in_gung=True

        if(before[0]>=7 and 3<=before[1] and before[1] <=5) or(before[0]<=2 and 3<=before[1] and before[1] <=5):
            self.in_gung=True

        if marker==1:
            go_list=[[before[0]+(-1)**(self.turn+1),before[1]]
                        ,[before[0],before[1]-1]
                        ,[before[0],before[1]+1]]
            #궁안에 있으면 대각선 추가 (졸)
            if self.in_gung:
                go_list.append([before[0]+(-1)**(self.turn+1),before[1]-1])
                go_list.append([before[0]+(-1)**(self.turn+1),before[1]+1])

        if marker ==2:
             go_list= [[before[0]+1,before[1]]
                        ,[before[0]-1,before[1]]
                        ,[before[0],before[1]-1]
                        ,[before[0],before[1]+1]
                        ,[before[0]+1,before[1]+1]
                        ,[before[0]-1,before[1]-1]
                        ,[before[0]+1,before[1]-1]
                        ,[before[0]-1,before[1]+1]]

        if marker ==3:
            go_list=[[before[0]+3,before[1]+2]
                        ,[before[0]+2,before[1]+3]
                        ,[before[0]+3,before[1]-2]
                        ,[before[0]+2,before[1]-3]
                        ,[before[0]-3,before[1]+2]
                        ,[before[0]-2,before[1]+3]
                        ,[before[0]-3,before[1]-2]
                        ,[before[0]-2,before[1]-3]]

        if marker ==4:
            go_list=[[before[0]+1,before[1]+2]
                    ,[before[0]+2,before[1]+1]
                    ,[before[0]+1,before[1]-2]
                    ,[before[0]+2,before[1]-1]
                    ,[before[0]-1,before[1]+2]
                    ,[before[0]-2,before[1]+1]
                    ,[before[0]-1,before[1]-2]
                    ,[before[0]-2,before[1]-1]]

        if marker ==5:
            go_list.append([9,before[1]])
            for i in range(9):
                go_list.append([before[0],i])
                go_list.append([i,before[1]])

            #궁안에 있으면 대각선 추가 (포)  
            if self.in_gung:
                #아래쪽 궁에 있을 때
                if (before[0]>=7 and 3<=before[1] and before[1] <=5) :
                    if before[0]%2==1 and before[1]%2==1:
                        if gameboard[8,4]!=0 and abs(gameboard[8,4])!=5:
                            go_list.append([16-before[0],8-before[1]])
                else:
                    if (before[1]%2)!=(before[0]%2):
                        if gameboard[1,4]!=0 and abs(gameboard[1,4])!=5:
                                go_list.append([2-before[0],8-before[1]])



        #궁안에 있으면 대각선 추가 (차)          
        if marker == 6:
            for i in range(9):
                go_list.append([before[0],i])
                go_list.append([i,before[1]])
            go_list.append([9,before[1]])

            if self.in_gung:
                #아래쪽에 있을 때
                if (before[0]>=7 and 3<=before[1] and before[1] <=5):
                    if before[1]==4 and before[0]==8:
                        go_list.append([before[0]+1,before[1]+1])
                        go_list.append([before[0]+1,before[1]-1])
                        go_list.append([before[0]-1,before[1]+1])
                        go_list.append([before[0]-1,before[1]-1])

                    elif before[0]%2==1 and before[1]%2==1:
                        go_list.append([8,4])
                        if gameboard[8,4]==0:
                            go_list.append([16-before[0],8-before[1]])

                #위쪽 궁에 있을 때
                else:

                    if (before[1]%2)!=(before[0]%2):
                        if before[1]==4:
                            go_list.append([before[0]+1,before[1]+1])
                            go_list.append([before[0]+1,before[1]-1])
                            go_list.append([before[0]-1,before[1]+1])
                            go_list.append([before[0]-1,before[1]-1])

                        else:
                            go_list.append([1,4])
                            if gameboard[1,4]==0:
                                go_list.append([2-before[0],8-before[1]])


        if marker ==7:
             go_list=[[before[0]+1,before[1]]
                        ,[before[0]-1,before[1]]
                        ,[before[0],before[1]-1]
                        ,[before[0],before[1]+1]
                        ,[before[0]+1,before[1]+1]
                        ,[before[0]-1,before[1]-1]
                        ,[before[0]+1,before[1]-1]
                        ,[before[0]-1,before[1]+1]]

        return go_list

    #규칙 상 갈 수 있는 곳 남기기

    def can_go(self,marker,before,gameboard):

        go_list=self.get_go(marker,before,gameboard)
        can_list=[]
        for l in go_list:
            #판 밖으로 나가는 것 제외
            if l[0]<0 or l[0]>9 or l[1]<0 or l[1]>8:
                continue
            #같은 팀 말 위로 나가는 거 제외
            if gameboard[l[0],l[1]]*((-1)**self.turn)>0:
                continue

            #궁밖으로 못나감, 대각선으로 이동할 수 없는 곳이 있음
            if self.in_gung:
                if(before[0]>=7 and 3<=before[1] and before[1] <=5):

                    if (l[0]<7 or l[1]<3 or l[1]>5)  and (marker==2 or marker==7):
                        continue

                    if before[0]==8 or before[1]==4:
                        if before[0]==8 and before[1]==4:
                            pass
                        else:
                            if l[0]-before[0]!=0 and l[1]-before[1]!=0:
                                continue


                else:
                    if (l[0]>2 or l[1]<3 or l[1]>5) and (marker==2 or marker==7):
                        continue

                    if before[0]==1 or before[1]==4:
                        if before[0]==1 and before[1]==4:
                            pass
                        else:
                            if l[0]-before[0]!=0 and l[1]-before[1]!=0:
                                continue



            #가는 길에 막히면 못움직임 (상)
            if marker==3 :
                move_y=np.sign(l[0]-before[0])
                move_x=np.sign(l[1]-before[1])
                if  gameboard[l[0]+1*(-move_y),l[1]+1*(-move_x)]==0 and gameboard[l[0]+2*(-move_y),l[1]+2*(-move_x)]==0:
                    pass
                else:
                    continue


            #가는 길에 막히면 못움직임 (마)      
            if marker==4 :

                move_y=np.sign(l[0]-before[0])
                move_x=np.sign(l[1]-before[1])
                if  gameboard[l[0]+1*(-move_y),l[1]+1*(-move_x)]==0:
                    pass
                else:
                    continue

            #포 사이에 하나 있어야 함 이 때 포면 안됨

            if marker==5:

                count=0
                jump_po=False

                if l[0]-before[0]!=0 and l[1]-before[1]!=0:
                    count=1
                elif l[0]-before[0]==0 and l[1]-before[1]==0:
                    continue

                elif l[0]-before[0]==0:
                    d=l[1]-before[1]
                    if d>0:
                        for i in range(1,d):
                            if gameboard[l[0],before[1]+i]!=0:
                                if abs(gameboard[l[0],before[1]+i])==5:
                                    jump_po=True
                                count+=1

                    else:
                        for i in range(-1,d,-1):
                            if gameboard[l[0],before[1]+i]!=0:

                                if abs(gameboard[l[0],before[1]+i])==5:
                                    jump_po=True
                                count+=1

                elif l[1]-before[1]==0:
                    d=l[0]-before[0]
                    if d>0:
                        for i in range(1,d):
                            if gameboard[before[0]+i,l[1]]!=0:
                                if abs(gameboard[before[0]+i,l[1]])==5:
                                    jump_po=True
                                count+=1
                    else:
                        for i in range(-1,d,-1):
                            if gameboard[before[0]+i,l[1]]!=0:
                                if abs(gameboard[before[0]+i,l[1]])==5:
                                    jump_po=True
                                count+=1


                if count!=1:
                    continue

                if jump_po or abs(gameboard[l[0],l[1]])==5:
                    continue


            #차 막히면 못감
            if marker==6:
                block=False
                if l[0]-before[0]!=0 and l[1]-before[1]!=0:
                    pass
                elif l[0]-before[0]==0 and l[1]-before[1]==0:
                    continue
                elif l[0]-before[0]==0:
                    d=l[1]-before[1]
                    if d>0:
                        for i in range(1,d):
                            if gameboard[l[0],before[1]+i]!=0:
                                block=True

                    else:
                        for i in range(-1,d,-1):
                            if gameboard[l[0],before[1]+i]!=0:
                                block=True

                elif l[1]-before[1]==0:
                    d=l[0]-before[0]
                    if d>0:
                        for i in range(1,d):
                            if gameboard[before[0]+i,l[1]]!=0:
                                block=True
                    else:
                        for i in range(-1,d,-1):
                            if gameboard[before[0]+i,l[1]]!=0:
                                block=True
                else:
                    continue

                if block:
                    continue



            can_list.append(l)

        return can_list

    #움직였는데 죽는 자리면 위험목록에 넣기
    def move_check(self,can_list):
        dangerous=[]
        for can in can_list:
            expect_gameboard=copy.copy(self.gameboard)
            expect_gameboard[can[0],can[1]]=expect_gameboard[self.before[0],self.before[1]]
            expect_gameboard[self.before[0],self.before[1]]=0
            king_index=[x[0] for x in np.where(expect_gameboard==(7*((-1)**self.turn)))]
            king_die=False

            for i in range(expect_gameboard.shape[0]):
                for j in range(expect_gameboard.shape[1]):
                    mark=expect_gameboard[i,j]
                    before=(i,j)
                    if (mark*((-1)**self.turn))<0:
                        if self.turn:
                            self.turn=0
                        else:
                            self.turn=1

                        mark=abs(mark)
                        expect_can_list=self.can_go(mark,before,expect_gameboard)
                        if king_index in expect_can_list:
                            king_die=True

                        if self.turn:
                            self.turn=0
                        else:
                            self.turn=1

            if king_die:
                dangerous.append(can)

        return dangerous

    def janggoon(self,gameboard):
        expect_gameboard=gameboard
        king_index=[x[0] for x in np.where(expect_gameboard==(7*((-1)**(self.turn+1))))]
        king_die=False
        for i in range(expect_gameboard.shape[0]):
                for j in range(expect_gameboard.shape[1]):
                    mark=expect_gameboard[i,j]
                    before=(i,j)
                    if (mark*((-1)**self.turn))>0:
                        mark=abs(mark)
                        expect_can_list=self.can_go(mark,before,expect_gameboard)
                        if king_index in expect_can_list:
                            king_die=True


        return king_die

    def mate(self):
        mate=True
        for i in range(self.gameboard.shape[0]):
                for j in range(self.gameboard.shape[1]):
                    self.mark=self.gameboard[i,j]
                    self.before=(i,j)

                    if (self.mark*((-1)**self.turn))>0:

                        mark=abs(self.mark)
                        real=self.real_go(mark,self.before,self.gameboard)

                        if real != []:
                            mate=False


        return mate

    def draw(self,X_coord,Y_coord):
        can_list=self.can_go(self.marker,self.before,self.gameboard)
        dangerous=self.move_check(can_list)
        for pos in can_list:
            x=X_coord[pos[1]]
            y=Y_coord[pos[0]]
            if pos in dangerous:
                pygame.draw.circle(DISPLAYSURF,GREEN,(x,y),7)
                pygame.draw.line(DISPLAYSURF, RED, (x-7,y-7),(x+7,y+7),3)
                pygame.draw.line(DISPLAYSURF, RED, (x-7,y+7),(x+7,y-7),3)
            elif self.gameboard[pos[0],pos[1]]==0:
                pygame.draw.circle(DISPLAYSURF,GREEN,(x,y),7)
            else:
                pygame.draw.circle(DISPLAYSURF,RED,(x,y),7)
        pygame.display.update()

    def real_go(self,marker,before,gameboard):
        real_can_go=[]
        can_list=self.can_go(marker,before,gameboard)
        danger=self.move_check(can_list)

        for l in can_list:
            if l in danger:
                continue
            else:
                real_can_go.append(l)
        return real_can_go






def ReturnName():
    return '장기'


def Return_Num_Action():
    return 9 * 8


def Return_BoardParams():
    return GAMEBOARD_SIZE, WIN_MARK




class GameState:
    def __init__(self,cho_form='mssm',han_form='mssm'):
        #cho_form 의 형태는 'mssm'가 같은 형식 m는 마 s는 상
        global FPS_CLOCK, DISPLAYSURF, BASIC_FONT, TITLE_FONT, GAMEOVER_FONT

        pygame.init()
        FPS_CLOCK = pygame.time.Clock()

        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('장기')

        BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)
        TITLE_FONT = pygame.font.Font('freesansbold.ttf', 24)
        GAMEOVER_FONT = pygame.font.Font('freesansbold.ttf', 48)

        # Set initial parameters
        self.init = False
        self.num_turn = 0
        self.cho_score=72
        self.han_score=72
        self.cho_formation,self.han_formation=cho_form,han_form
        self.cho_form,self.han_form=[],[]
        for c in self.cho_formation:
            if c=='m':
                self.cho_form.append(4)
            else:
                self.cho_form.append(3)

        for h in self.han_formation:
            if h=='m':
                self.han_form.append(4)
            else:
                self.han_form.append(3)


        self.janggoon=False
        self.mate=False
        self.can_go=None
        self.wait_move=False
        self.marker=0

        # No stone: 0, Cho stone: Plus, Han stone = minus
        # 병 1 사 2 상 3 마 4 포 5 차 6 왕7


        a=self.cho_form[0]
        b=self.cho_form[1]
        c=self.cho_form[2]
        d=self.cho_form[3]
        formation_cho=np.array([[0,0,0,0,0,0,0,0,0],
                                [1,0,1,0,1,0,1,0,1],
                                [0,5,0,0,0,0,0,5,0],
                                [0,0,0,0,7,0,0,0,0],
                                [6,a,b,2,0,2,c,d,6]])

        a=self.han_form[0]
        b=self.han_form[1]
        c=self.han_form[2]
        d=self.han_form[3]
        formation_han=np.array([[0,0,0,0,0,0,0,0,0],
                                [1,0,1,0,1,0,1,0,1],
                                [0,5,0,0,0,0,0,5,0],
                                [0,0,0,0,7,0,0,0,0],
                                [6,a,b,2,0,2,c,d,6]])


        self.base_gameboard=np.concatenate([np.flip(formation_han*(-1), axis=0),formation_cho])
        self.gameboard=self.base_gameboard

        self.cho_win = 0
        self.han_win = 0

        # Cho turn: 0, Han turn: 1
        self.turn = 0

        # Cho wins: 1, Han wins: 2, playing: 0
        self.win_index = 0

        # List of X coordinates and Y coordinates
        self.X_coord = []
        self.Y_coord = []

        for i in range(POINT_WIDTH):
            self.X_coord.append(
                MARGIN + i * int(GRID_SIZE / (POINT_WIDTH-1)))

        for i in range(POINT_HEIGHT):   
            self.Y_coord.append(
                TOP_MARGIN + i *int(GRID_SIZE / (POINT_HEIGHT-1)))


#     def step(self, input_):  # Game loop
    def step(self):
              # Initial settings
        if self.init == True:
            self.num_turn = 0

            # No mark: 0, o: 1, x = -1
            self.gameboard = self.base_gameboard

            # Reset init
            self.init = False

        # Fill background color
        DISPLAYSURF.fill(BACK)

        # Draw board
        self.draw_main_board(self.X_coord,self.Y_coord)

        #check the mate
        check=Can_go(self.marker,0,0,self.gameboard,self.turn)
        self.mate=check.mate()

        # Key settings
        mouse_pos = 0

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                self.terminate()

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()

        # Check mouse position and count
        check_valid_pos = False
        x_index = -1
        y_index = -1

        #mouse_pos 받기

        if mouse_pos != 0 :
            for i in range(len(self.X_coord)):
                for j in range(len(self.Y_coord)):
                    if (self.X_coord[i] - 15 < mouse_pos[0] < self.X_coord[
                        i] + 15) and (self.Y_coord[j] - 15 < mouse_pos[1] <
                                              self.Y_coord[j] + 15):
                        check_valid_pos = True
                        x_index = i
                        y_index = j

                        # If selected spot is 아무것도 없으면, it is not valid move!
                        # 같은 팀 말이 아니여도 안됨!

                        if self.gameboard[j, i]*((-1)**self.turn) >0:
                            self.wait_move=True
                            global before_y_index,before_x_index
                            before_y_index=y_index
                            before_x_index=x_index


            # board 움직이기

        if self.wait_move: 
            if check_valid_pos:
                if ((-1)**self.turn)*self.gameboard[y_index, x_index]>0:
                    self.marker=((-1)**self.turn)*self.gameboard[y_index, x_index]

            can=Can_go(self.marker,before_y_index,before_x_index,self.gameboard,self.turn)
            can.draw(self.X_coord,self.Y_coord)

            #이동과정
            if  self.gameboard[y_index,x_index]*((-1)**self.turn) <=0:
                before=(before_y_index,before_x_index)

                for can_lst in can.real_go(self.marker,before,self.gameboard):
                    if can_lst==[y_index,x_index]:
                        self.gameboard[y_index,x_index]=self.gameboard[before_y_index,before_x_index]
                        self.gameboard[before_y_index,before_x_index]=0
                        self.janggoon=can.janggoon(self.gameboard)
                        self.wait_move=False
                        if self.turn:
                            self.turn=0
                        else:
                            self.turn=1   
                        break


#         # If vs mode and MCTS works
#         if np.any(input_) != 0:
#             action_index = np.argmax(input_)
#             y_index = int(action_index / 3)
#             x_index = action_index % 3
#             check_valid_pos = True

        # Change the gameboard according to the stone's index
#         if check_valid_pos:
#             if self.turn == 0:
#                 self.gameboard[y_index, x_index] = 1
#                 self.turn = 1
#                 self.num_mark += 1
#             else:
#                 self.gameboard[y_index, x_index] = -1
#                 self.turn = 0
#                 self.num_mark += 1


        # Display Information
        self.title_msg()
        self.rule_msg()
        self.score_msg()
        self.jang_msg()

        # Display who's turn
        self.turn_msg()
        pygame.display.update()

        # Check_win 0: playing, 1: cho win, 2: han win
        self.win_index = self.check_win()
        self.display_win(self.win_index)

        return self.gameboard, check_valid_pos, self.win_index, self.turn

    # Exit the game
    def terminate(self):
        pygame.quit()
        sys.exit()

    # Draw main board
    def draw_main_board(self,X_coord,Y_coord):
        #판 색만들기 
        pygame.draw.rect(DISPLAYSURF, JANG, [20,TOP_MARGIN-20,400,400])

        # Horizontal Lines
        for i in (X_coord):
            pygame.draw.line(DISPLAYSURF, BLACK, (
            i, TOP_MARGIN), (i,TOP_MARGIN + GRID_SIZE), 1)

        # Vertical Lines
        for j in (Y_coord):
            pygame.draw.line(DISPLAYSURF, BLACK, (
            MARGIN , j), (WINDOW_WIDTH -MARGIN,j), 1)

        # 궁 안에 대각선 그리기
        for l in [[3,0,5,2],[3,2,5,0],[3,7,5,9],[3,9,5,7]]:
            pygame.draw.line(DISPLAYSURF, BLACK, (X_coord[l[0]],Y_coord[l[1]]), (X_coord[l[2]],Y_coord[l[3]]), 2)


#         # Draw center circle
#         pygame.draw.circle(DISPLAYSURF, WHITE, (
#         MARGIN + 4 * int(GRID_SIZE / (GAMEBOARD_SIZE)),
#         TOP_MARGIN + 4 * int(GRID_SIZE / (GAMEBOARD_SIZE))), 5, 0)

        # Draw marks
        # No stone: 0, Cho stone: Plus, Han stone = minus
        # 병 1 사 2 상 3 마 4 포 5 차 6 왕7
        self.cho_score,self.han_score=0,0

        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if self.gameboard[i, j] > 0:
                    Team=0
                elif self.gameboard[i, j] < 0:
                    Team=1

                Mini=(X_coord[j]-CELL_SIZE*0.5,Y_coord[i]-CELL_SIZE*0.5
                      ,CELL_SIZE,CELL_SIZE)
                Middle=(int(X_coord[j]-CELL_SIZE*0.55),int(Y_coord[i]-CELL_SIZE*0.55)
                      ,int(CELL_SIZE*1.1),int(CELL_SIZE*1.1))
                Big=(int(X_coord[j]-0.6*CELL_SIZE),int(Y_coord[i]-0.6*CELL_SIZE)
                      ,int(1.2*CELL_SIZE),int(1.2*CELL_SIZE))

                if abs(self.gameboard[i, j]) == 1:
                    if Team==0:
                        self.cho_score+=2
                    else:
                        self.han_score+=2
                    jol=Pieces(Team,1,*Mini)
                    jol.draw()

#                     pygame.draw.rect(DISPLAYSURF, Mark_Color,
#                                        [self.X_coord[j]-5, self.Y_coord[i]-10,10,20],
#                                        0)

                elif abs(self.gameboard[i, j]) == 2:
                    if Team==0:
                        self.cho_score+=3
                    else:
                        self.han_score+=3

                    sa=Pieces(Team,2,*Mini)
                    sa.draw()

                elif abs(self.gameboard[i, j]) == 3:
                    if Team==0:
                        self.cho_score+=3
                    else:
                        self.han_score+=3

                    sang=Pieces(Team,3,*Middle)
                    sang.draw()


                elif abs(self.gameboard[i, j]) == 4:
                    if Team==0:
                        self.cho_score+=5
                    else:
                        self.han_score+=5

                    ma=Pieces(Team,4,*Middle)
                    ma.draw()

                elif abs(self.gameboard[i, j]) == 5:
                    if Team==0:
                        self.cho_score+=7
                    else:
                        self.han_score+=7

                    po=Pieces(Team,5,*Middle)
                    po.draw()


                elif abs(self.gameboard[i, j]) == 6:
                    if Team==0:
                        self.cho_score+=13
                    else:
                        self.han_score+=13

                    cha=Pieces(Team,6,*Middle)
                    cha.draw()


                elif abs(self.gameboard[i, j]) == 7:

                    wang=Pieces(Team,7,*Big)
                    wang.draw()


    # Display title
    def title_msg(self):
        titleSurf = TITLE_FONT.render('Janggi', True, BLACK)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (MARGIN, 10)
        DISPLAYSURF.blit(titleSurf, titleRect)

    def jang_msg(self):            
        if self.janggoon:
            if self.mate:
                mateSurf = TITLE_FONT.render('Mate!', True, BLACK)
                mateRect = mateSurf.get_rect()
                mateRect.topright = (WINDOW_WIDTH-MARGIN-10,50)
                DISPLAYSURF.blit(mateSurf, mateRect)
            else:
                jangSurf = TITLE_FONT.render('Janggoon!', True, BLACK)
                jangRect = jangSurf.get_rect()
                jangRect.topright = (WINDOW_WIDTH-MARGIN-10,50)
                DISPLAYSURF.blit(jangSurf, jangRect)


    # Display rule
    def rule_msg(self):
        ruleSurf1 = BASIC_FONT.render('cho :'+''.join(self.cho_formation),
                                      True, BLACK)
        ruleRect1 = ruleSurf1.get_rect()
        ruleRect1.topleft = (MARGIN, 50)
        DISPLAYSURF.blit(ruleSurf1, ruleRect1)

        ruleSurf2 = BASIC_FONT.render('han :'+''.join(self.han_formation), True,
                                      BLACK)
        ruleRect2 = ruleSurf1.get_rect()
        ruleRect2.topleft = (MARGIN, 70)
        DISPLAYSURF.blit(ruleSurf2, ruleRect2)

    # Display scores
    def score_msg(self):
        scoreSurf1 = BASIC_FONT.render('Score: ', True, BLACK)
        scoreRect1 = scoreSurf1.get_rect()
        scoreRect1.topleft = (MARGIN, 105)
        DISPLAYSURF.blit(scoreSurf1, scoreRect1)

        scoreSurf2 = BASIC_FONT.render('Cho =' + str(self.cho_score) + 'pt       ',
                                       True, BLACK)
        scoreRect2 = scoreSurf2.get_rect()
        scoreRect2.topleft = (scoreRect1.midright[0], 105)
        DISPLAYSURF.blit(scoreSurf2, scoreRect2)

        scoreSurf3 = BASIC_FONT.render('Han = ' + str(self.han_score) +'pt',
                                       True, BLACK)
        scoreRect3 = scoreSurf3.get_rect()
        scoreRect3.topleft = (scoreRect2.midright[0], 105)
        DISPLAYSURF.blit(scoreSurf3, scoreRect3)


    # Display turn
    def turn_msg(self):
        if self.turn == 0:
            turnSurf = BASIC_FONT.render("Cho's Turn!", True, BLACK)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (MARGIN, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)
        else:
            turnSurf = BASIC_FONT.render("Han's Turn!", True, BLACK)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (WINDOW_WIDTH - 100, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)

    # Check win
    def check_win(self):
        # 왕이 있나 확인
        global win_reason
        win_reason=''
        cho_alive=True
        han_alive=True

        if self.cho_score<10:
            cho_alive=False
            win_reason='Score Loss'
        if self.han_score<10:
            han_alive=False
            win_reason='Score Loss'

        #외통수 확인
        if self.mate:
            time.sleep(wait_time)
            if self.turn:
                han_alive=False
                win_reason='Mate'
            else:
                cho_alive=False
                win_reason='Mate'

        if cho_alive and han_alive:
            return 0
        elif not cho_alive:
            return 2
        elif not han_alive:
            return 1



    # Display Win
    def display_win(self, win_index):

        self.init = False
        if win_index==0:
            pass
        else:
            # Cho Win
            if win_index == 1:
                # Fill background color
                DISPLAYSURF.fill(BLUE)

                winSurf = GAMEOVER_FONT.render("Cho Win!", True, BLACK)
                winRect = winSurf.get_rect()
                winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
                DISPLAYSURF.blit(winSurf, winRect)
                self.cho_win += 1


            # han Win
            if win_index == 2:
                # Fill background color
                DISPLAYSURF.fill(RED)
                winSurf = GAMEOVER_FONT.render("han Win!", True, BLACK)
                winRect = winSurf.get_rect()
                winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
                DISPLAYSURF.blit(winSurf, winRect)
                self.han_win += 1



            reasonSurf = TITLE_FONT.render(win_reason, True, BLACK)
            reasonRect = reasonSurf.get_rect()
            reasonRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            DISPLAYSURF.blit(reasonSurf, reasonRect)
            pygame.display.update()

            time.sleep(wait_time)
            self.init = True
            self.__init__()

if __name__ == "__main__":
    game=GameState('mssm','mssm')

    while True:
        game.step()

# pygame.quit() 