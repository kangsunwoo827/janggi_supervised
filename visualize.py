# -*- coding: utf-8 -*- 
#장기
#이 파일에서 정의된 것
#1) Pieces 클래스 . 장기 알을 의미
#2) Can_go 클래스. 장기 알이 이동가능한지 표시하는 걸 의미
#3) Gamestate 클래스. 게임을 총 관리하는 클래스
import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

from visual_param import *

# from game import GameState,Game

wait_time = 1
Pieces_list = [None,'jol','sa','sang','ma','po','cha','wang']

import os
os.environ['DISPLAY']


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
            
        self.image = pygame.image.load("piece_img/"+self.team+name+'.png').convert_alpha()

        self.scale_image=pygame.transform.scale(self.image, (sizex,sizey))
    
    def draw(self):
        DISPLAYSURF.blit(self.scale_image, (self.x, self.y))
        
class Can_go(pygame.sprite.Sprite):
    #Cho's turn : +1 , Han's turn : -1 
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
            go_list=[
                    [before[0]-self.turn, before[1]],
                    [before[0], before[1]-1],
                    [before[0], before[1]+1]
                    ]

            #궁안에 있으면 대각선 추가 (졸)
            if self.in_gung:
                go_list.append([before[0]-self.turn, before[1]-1])
                go_list.append([before[0]-self.turn, before[1]+1])
         
        if marker ==2:
             go_list=[
                    [before[0]+1, before[1]],
                    [before[0]-1, before[1]],
                    [before[0], before[1]-1],
                    [before[0], before[1]+1],
                    [before[0]+1, before[1]+1],
                    [before[0]-1, before[1]-1],
                    [before[0]+1, before[1]-1],
                    [before[0]-1, before[1]+1]
                    ]
                
        if marker ==3:
            go_list=[[before[0]+3, before[1]+2]
                        ,[before[0]+2, before[1]+3]
                        ,[before[0]+3, before[1]-2]
                        ,[before[0]+2, before[1]-3]
                        ,[before[0]-3, before[1]+2]
                        ,[before[0]-2, before[1]+3]
                        ,[before[0]-3, before[1]-2]
                        ,[before[0]-2, before[1]-3]]
            
        if marker ==4:
            go_list=[[before[0]+1, before[1]+2]
                    ,[before[0]+2, before[1]+1]
                    ,[before[0]+1, before[1]-2]
                    ,[before[0]+2, before[1]-1]
                    ,[before[0]-1, before[1]+2]
                    ,[before[0]-2, before[1]+1]
                    ,[before[0]-1, before[1]-2]
                    ,[before[0]-2, before[1]-1]]
         
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
            if self.turn * gameboard[l[0],l[1]]>0:
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
            king_index=[x[0] for x in np.where(expect_gameboard==(7*self.turn))]
            king_die=False
            
            for i in range(expect_gameboard.shape[0]):
                for j in range(expect_gameboard.shape[1]):
                    mark=expect_gameboard[i,j]
                    before=(i,j)
                    if (mark*self.turn)<0:
                        self.turn*=(-1)
                            
                        mark=abs(mark)
                        expect_can_list=self.can_go(mark,before,expect_gameboard)
                        if king_index in expect_can_list:
                            king_die=True
                            
                        self.turn*=(-1)
                
            if king_die:
                dangerous.append(can)
        
        return dangerous
    
    def janggoon(self,gameboard):
        expect_gameboard=gameboard
        king_index=[x[0] for x in np.where(expect_gameboard==7*(-self.turn))]
        king_die=False
        for i in range(expect_gameboard.shape[0]):
                for j in range(expect_gameboard.shape[1]):
                    mark=expect_gameboard[i,j]
                    before=(i,j)
                    if (mark*self.turn)>0:
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
                    
                    if (self.mark*self.turn)>0:
                   
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


class Visualize:
    def __init__(self,GameState,cho_form='mssm',han_form='mssm'):
        #cho_form 의 형태는 'mssm'과 같은 형식 m는 마 s는 상
        global FPS_CLOCK, DISPLAYSURF, BASIC_FONT,NUM_FONT, TITLE_FONT, GAMEOVER_FONT

        pygame.init()

        FPS_CLOCK = pygame.time.Clock()

        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('장기')

        BASIC_FONT = pygame.font.Font('/usr/share/fonts/NanumGothic.ttf', 16)
        NUM_FONT= pygame.font.Font('/usr/share/fonts/NanumPen.ttf', 20)
        TITLE_FONT = pygame.font.Font('/usr/share/fonts/NanumGothicBold.ttf', 24)
        GAMEOVER_FONT = pygame.font.Font('/usr/share/fonts/NanumGothicExtraBold.ttf', 48)

        # BASIC_FONT = pygame.font.Font('/Windows/Fonts/nanumgothic.ttf', 16)
        # NUM_FONT= pygame.font.Font('/Windows/Fonts/nanumpen.ttf', 20)
        # TITLE_FONT = pygame.font.Font('/Windows/Fonts/nanumgothicbold.ttf', 24)
        # GAMEOVER_FONT = pygame.font.Font('/Windows/Fonts/nanumgothicextrabold.ttf', 48)

        # Set initial parameters
        self.init = False
        self.gameState=GameState
        self.num_turn = self.gameState.num_turn
        # Cho turn: +1, Han turn: -1
        self.turn = self.gameState.playerTurn

        if self.turn>0:
            self.cho_score=self.gameState.playerScore
            self.han_score=self.gameState.oppoScore
        else:
            self.cho_score=self.gameState.oppoScore
            self.han_score=self.gameState.playerScore

        self.cho_formation, self.han_formation=cho_form, han_form
    
        # No mark: 0, Cho mark: Plus, Han mark = minus
        # 병 1 사 2 상 3 마 4 포 5 차 6 왕7
    
        self.gameboard=self.gameState.board

        # Cho wins: +1, Han wins: -1, playing: 0
        self.win_index = self.gameState.who_win

        self.janggoon=False
        self.mate=False
        self.can_go=None
        self.wait_move=False
        self.marker=0
        
        # List of X coordinates and Y coordinates
        self.X_coord = []
        self.Y_coord = []

        for i in range(POINT_WIDTH):
            self.X_coord.append(
                MARGIN + i * int(GRID_SIZE / (POINT_WIDTH-1)))
            
        for i in range(POINT_HEIGHT):   
            self.Y_coord.append(
                TOP_MARGIN + i *int(GRID_SIZE / (POINT_HEIGHT-1)))

        # Fill background color
        DISPLAYSURF.fill(BACK)

        # Draw board
        self.draw_main_board(self.X_coord,self.Y_coord)
        
        
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                self.terminate()


        # Display Information
        self.title_msg()
        self.num_msg()
        self.form_msg()
        self.score_msg()
        self.jang_msg()

        # Display who's turn
        self.turn_msg()

        # Check_win 0: playing, 1: cho win, 2: han win
        self.display_win(self.win_index)
            
#   Game loop
    def show(self,newState):
        self.__init__(newState)
        pygame.display.update()
    
    # Exit the game
    def terminate(self):
        pygame.quit()
        sys.exit()

    # Draw main board
    def draw_main_board(self,X_coord,Y_coord):
        #판 색만들기 
        pygame.draw.rect(DISPLAYSURF, JANG, [0,TOP_MARGIN-40,440,440])

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
        
        #=================================================#
        #==================Draw marks=====================#
        #=================================================#

        # No mark: 0, Cho mark: Plus, Han mark = minus
        # 병 1 사 2 상 3 마 4 포 5 차 6 왕7
        
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
                    
                    jol=Pieces(Team,1,*Mini)
                    jol.draw()
                        
                elif abs(self.gameboard[i, j]) == 2:
                   
                    sa=Pieces(Team,2,*Mini)
                    sa.draw()
                        
                elif abs(self.gameboard[i, j]) == 3:
                    
              
                    sang=Pieces(Team,3,*Middle)
                    sang.draw()
                        
                    
                elif abs(self.gameboard[i, j]) == 4:
                   
                        
                    ma=Pieces(Team,4,*Middle)
                    ma.draw()
                        
                elif abs(self.gameboard[i, j]) == 5:
                   
                    po=Pieces(Team,5,*Middle)
                    po.draw()
                        
                
                elif abs(self.gameboard[i, j]) == 6:
                    
                    cha=Pieces(Team,6,*Middle)
                    cha.draw()
                        
                    
                elif abs(self.gameboard[i, j]) == 7:
                        
                    wang=Pieces(Team,7,*Big)
                    wang.draw()
                        

    # Display title
    def title_msg(self):
        titleSurf = TITLE_FONT.render('Janggi', True, BLACK)
        titleRect = titleSurf.get_rect()
        titleRect.center = (HALF_WINDOW_WIDTH, 25)
        DISPLAYSURF.blit(titleSurf, titleRect)

    def num_msg(self):
        #세로 줄에 대한 숫자 표시
        for i in range(9):
            num1Surf = NUM_FONT.render(str(i+1), True, BLACK)
            num1Rect = num1Surf.get_rect()
            num1Rect.center = (self.X_coord[i],TOP_MARGIN-30)
            DISPLAYSURF.blit(num1Surf, num1Rect)

            num2Surf = NUM_FONT.render(str(i+1), True, BLACK)
            num2Rect = num2Surf.get_rect()
            num2Rect.center = (self.X_coord[i],TOP_MARGIN+ GRID_SIZE+30)
            DISPLAYSURF.blit(num2Surf, num2Rect)

        #가로 줄에 대한 숫자 표시
        for i in range(10):
            num=(i+1)%10
            num1Surf = NUM_FONT.render(str(num), True, BLACK)
            num1Rect = num1Surf.get_rect()
            num1Rect.center = (MARGIN-30,self.Y_coord[i])
            DISPLAYSURF.blit(num1Surf, num1Rect)

            num2Surf = NUM_FONT.render(str(num), True, BLACK)
            num2Rect = num2Surf.get_rect()
            num2Rect.center = (MARGIN+GRID_SIZE+30,self.Y_coord[i])
            DISPLAYSURF.blit(num2Surf, num2Rect)





    
    def jang_msg(self):            
        if self.janggoon:
            if self.turn:
                color=BLUE
            else:
                color=RED
            if self.mate:
                mateSurf = TITLE_FONT.render('Mate!', True, color)
                mateRect = mateSurf.get_rect()
                mateRect.center = (HALF_WINDOW_WIDTH,140)
                DISPLAYSURF.blit(mateSurf, mateRect)
            else:
                jangSurf = TITLE_FONT.render('Janggoon!', True, color)
                jangRect = jangSurf.get_rect()
                jangRect.center = (HALF_WINDOW_WIDTH,140)
                DISPLAYSURF.blit(jangSurf, jangRect)


    # Display formation
    def form_msg(self):
        formSurf1 = BASIC_FONT.render('cho :'+''.join(self.cho_formation),
                                      True, BLACK)
        formRect1 = formSurf1.get_rect()
        formRect1.topleft = (WINDOW_WIDTH-120, 80)
        DISPLAYSURF.blit(formSurf1, formRect1)

        formSurf2 = BASIC_FONT.render('han :'+''.join(self.han_formation), True,
                                      BLACK)
        formRect2 = formSurf1.get_rect()
        formRect2.topleft = (WINDOW_WIDTH-120, 105)
        DISPLAYSURF.blit(formSurf2, formRect2)

    # Display scores
    def score_msg(self):

        scoreSurf1 = BASIC_FONT.render('Cho Vs Han',
                                       True, BLACK)
        scoreRect1 = scoreSurf1.get_rect()
        scoreRect1.topleft = (MARGIN, 80)
        DISPLAYSURF.blit(scoreSurf1, scoreRect1)

        scoreSurf2 = BASIC_FONT.render(str(self.cho_score) + 'pt      '+str(self.han_score)+'pt',
                                       True, BLACK)
        scoreRect2 = scoreSurf2.get_rect()
        scoreRect2.topleft = (MARGIN, 105)
        DISPLAYSURF.blit(scoreSurf2, scoreRect2)


    # Display turn
    def turn_msg(self):
        num_turnSurf = BASIC_FONT.render(str(self.num_turn), True, BLACK)
        num_turnRect = num_turnSurf.get_rect()
        num_turnRect.center = (HALF_WINDOW_WIDTH, 135)
        DISPLAYSURF.blit(num_turnSurf, num_turnRect)
        if self.turn >0:
            turnSurf = BASIC_FONT.render("Cho's Turn!", True, BLACK)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (MARGIN, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)
        else:
            turnSurf = BASIC_FONT.render("Han's Turn!", True, BLACK)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (WINDOW_WIDTH - 120, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)
      
        

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
                

            # han Win
            if win_index == -1:
                # Fill background color
                DISPLAYSURF.fill(RED)
                winSurf = GAMEOVER_FONT.render("han Win!", True, BLACK)
                winRect = winSurf.get_rect()
                winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
                DISPLAYSURF.blit(winSurf, winRect)
              


           

            time.sleep(wait_time)
            self.init = True
            # self.__init__()


if __name__ == "__main__":
    game=Game('mssm','mssm')
    window=Visualize(game)
    while True:
        window.show()
        
