import pygame
import random
import time

pygame.init()

MAX_X = 700
MAX_Y = 650

gameDisplay = pygame.display.set_mode((MAX_X,MAX_Y))
pygame.display.set_caption('Gravris')
pygame.display.update()

gameExit = False;

clock = pygame.time.Clock()

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
violet = (238,130,238)
cyan = (0,255,255)
blue = (0,0,255)
orange = (255,165,0)
yellow = (255,255,0)
green = (0,100,0)

#Player controls
#0: shift1
#1: shift2
#2: rotate
#3: accelerate
PLAYER_CONTROLS = []

PLAYER_CONTROLS.append([])
PLAYER_CONTROLS.append([])
PLAYER_CONTROLS.append([])
PLAYER_CONTROLS.append([])

PLAYER_CONTROLS[0].append(pygame.K_a)
PLAYER_CONTROLS[0].append(pygame.K_d)
PLAYER_CONTROLS[0].append(pygame.K_w)
PLAYER_CONTROLS[0].append(pygame.K_s)
PLAYER_CONTROLS[0].append(pygame.K_x)

PLAYER_CONTROLS[1].append(pygame.K_h)
PLAYER_CONTROLS[1].append(pygame.K_n)
PLAYER_CONTROLS[1].append(pygame.K_m)
PLAYER_CONTROLS[1].append(pygame.K_b)
PLAYER_CONTROLS[1].append(pygame.K_SPACE)

PLAYER_CONTROLS[2].append(pygame.K_RIGHT)
PLAYER_CONTROLS[2].append(pygame.K_LEFT)
PLAYER_CONTROLS[2].append(pygame.K_DOWN)
PLAYER_CONTROLS[2].append(pygame.K_UP)
PLAYER_CONTROLS[2].append(pygame.K_RCTRL)

PLAYER_CONTROLS[3].append(pygame.K_KP3)
PLAYER_CONTROLS[3].append(pygame.K_KP9)
PLAYER_CONTROLS[3].append(pygame.K_KP5)
PLAYER_CONTROLS[3].append(pygame.K_KP6)
PLAYER_CONTROLS[3].append(pygame.K_KP0)

#board bounds
SPACING = 20

X_START = 80
Y_START = 50
X_END = 620
Y_END = 590
X_LENGTH = X_END-X_START
Y_LENGTH = Y_END-Y_START
B_DEPTH = 2

RX_START = 280
RY_START = 250
RX_END = 420
RY_END = 390
RX_LENGTH = RX_END-RX_START
RY_LENGTH = RY_END-RY_START
R_DEPTH = 2

#board mino
minoPieces = []
minoColor = []

for i in range((X_END-X_START)*(Y_END-Y_START)/(SPACING*SPACING)):
    minoPieces.append(False)
    minoColor.append(white)

def pileDisplay(): #empty param, displays stacked minos on gameBoard
    global minoPieces
    global minoColor

    i = 0

    while i<((X_LENGTH)*(Y_LENGTH)/(SPACING*SPACING)):

        if minoPieces[i]:
            pygame.draw.rect(gameDisplay,minoColor[i],[(i%(X_LENGTH/SPACING))*SPACING+X_START,(i/(Y_LENGTH/SPACING))*SPACING+Y_START,SPACING,SPACING])

        else:
            pygame.draw.rect(gameDisplay,white,[(i%(X_LENGTH/SPACING))*SPACING+X_START,(i/(Y_LENGTH/SPACING))*SPACING+Y_START,SPACING,SPACING])
            
        i+=1

#################################

#Mino Properties and modifiers

#block properties:
#pos: 0:facing above
#     1:facing to the right
#     2:facing below
#     3:facing to the left
#shape:0:T-mino
#      1:Z-mino
#      2:l-mino
#      3:J-mino
#      4:L-mino
#      5:O-mino
#      6:S-mino
pivot = []
pos = []
shape = []

pivot.append([0,0])
pivot.append([0,0])
pivot.append([0,0])
pivot.append([0,0])

pos.append(0)
pos.append(1)
pos.append(2)
pos.append(3)

shape.append(0)
shape.append(0)
shape.append(0)
shape.append(0)

def minoInitialize(player, mark): #player(int), mark(int), initializes a player's mino
    global pivot
    global pos
    global shape

    displace = 0
    shift = 0

    pos[player] = player
    shape[player] = mark%7

    if shape[player]==5 or shape[player]==2:
        shift = SPACING

    if shape[player] == 1 or shape[player] == 5 or shape[player] == 6:
        displace = SPACING
    
    if player==0:
        pivot[0] = [RX_START+3*SPACING-shift, RY_END]
        
    elif player==1:
        pivot[1] = [RX_START-SPACING, RY_START+3*SPACING]
        
    elif player==2:
        pivot[2] = [RX_START+3*SPACING, RY_START-SPACING+displace]

    elif player==3:
        pivot[3] = [RX_END-displace, RY_START+3*SPACING+shift]

def MINO_FShift(player): #player(int), shifts mino in one direction (clockwise)
    global pivot

    if player==0:
        pivot[0][0]-=SPACING

    elif player==1:
        pivot[1][1]-=SPACING

    elif player==2:
        pivot[2][0]+=SPACING

    else:
        pivot[3][1]+=SPACING

def MINO_RShift(player): #player(int),shifts mino in one direction(counter clockwise)
    global pivot

    if player==0:
        pivot[0][0]+=SPACING

    elif player==1:
        pivot[1][1]+=SPACING

    elif player==2:
        pivot[2][0]-=SPACING

    else:
        pivot[3][1]-=SPACING

def MINO_gravity(player): #player(int), drops mino towards respective player's side
    global pivot

    if player==0:
        pivot[0][1]+=SPACING

    elif player==1:
        pivot[1][0]-=SPACING

    elif player==2:
        pivot[2][1]-=SPACING

    else:
        pivot[3][0]+=SPACING

def MINO_rotate(player): #player(int), rotates given mino
    global pos
    pos[player]=(pos[player]+1)%4

def MINO_future(op,player,cor): #op(string),player(int),cor(list(int,int)), predicts mino's future position
                                #                                           based upon given operation
    if op == "FShift":
        if player == 1:
            return [cor[0]-SPACING,cor[1]]
        
        elif player == 2:
            return [cor[0],cor[1]-SPACING]

        elif player == 3:
            return [cor[0]+SPACING,cor[1]]

        elif player == 4:
            return [cor[0],cor[1]+SPACING]
            
    elif op == "RShift":
        if player == 1:
            return [cor[0]+SPACING,cor[1]]
        
        elif player == 2:
            return [cor[0],cor[1]+SPACING]

        elif player == 3:
            return [cor[0]-SPACING,cor[1]]

        elif player == 4:
            return [cor[0],cor[1]-SPACING]
            
    elif op == "gravity":
        if player == 1:
            return [cor[0],cor[1]+SPACING]

        elif player == 2:
            return [cor[0]-SPACING,cor[1]]

        elif player == 3:
            return [cor[0],cor[1]-SPACING]

        elif player == 4:
            return [cor[0]+SPACING,cor[1]]

################################

#Frames Per Second
FPS = 30
pygame.time.Clock()

######################################################
######################################################
###########     Game Mechanics        ################
######################################################
######################################################

def tMinoCreate(cor,direction,real): # cor(list(int,int)),direction(int),real(bool),prints t shape mino on board

    r1 = 0
    r2 = 0
    r3 = 0
    
    if(direction == 1):
        r1 = SPACING

    elif(direction == 2):
        r2 = 2*SPACING

    elif(direction == 3):
        r3 = SPACING

    if real:
        visual = violet

    else:
        visual = white
    
        
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+r1,cor[1]+r1,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1]-SPACING+r2,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING-r3,cor[1]+r3,SPACING,SPACING])


def tMinoInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    t mino's 4 pieces

    design = []
    r1 = 0
    r2 = 0
    r3 = 0
    
    if(direction == 1):
        r1 = SPACING

    elif(direction == 2):
        r2 = 2*SPACING

    elif(direction == 3):
        r3 = SPACING

    design.append([cor[0],cor[1]])
    design.append([cor[0]-SPACING+r1,cor[1]+r1])
    design.append([cor[0],cor[1]-SPACING+r2])
    design.append([cor[0]+SPACING-r3,cor[1]+r3])

    return design

################################################################################

def zMinoCreate(cor,direction,real):  # cor(list(int,int)),direction(int),real(bool),prints z shape mino on board

    addend = 0

    if real:
        visual = red

    else:
        visual = white

    if direction%2 == 1:
        addend = 2*SPACING

    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+addend,cor[1]-SPACING,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1]-SPACING+addend,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING,cor[1],SPACING,SPACING])

def zMinoInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    z mino's 4 pieces

    design = []
    addend = 0

    if direction%2 == 1:
        addend = 2*SPACING

    design.append([cor[0],cor[1]])
    design.append([cor[0]-SPACING+addend,cor[1]-SPACING])
    design.append([cor[0],cor[1]-SPACING+addend])
    design.append([cor[0]+SPACING,cor[1]])

    return design

###############################################################################

def longlCreate(cor,direction,real): # cor(list(int,int)),direction(int),real(bool),prints l shape mino on board

    xAdd = 0
    yAdd = 0

    if real:
        visual = cyan

    else:
        visual = white

    if direction%2 == 0:
        xAdd = SPACING
    
    elif direction%2 == 1:
        yAdd = SPACING

    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+xAdd,cor[1]-yAdd,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+2*xAdd,cor[1]-2*yAdd,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+3*xAdd,cor[1]-3*yAdd,SPACING,SPACING])

def longlInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    l mino's 4 pieces
    design = []
    xAdd = 0
    yAdd = 0

    if direction%2 == 0:
        xAdd = SPACING
    
    elif direction%2 == 1:
        yAdd = SPACING

    design.append([cor[0],cor[1]])
    design.append([cor[0]+xAdd,cor[1]-yAdd])
    design.append([cor[0]+2*xAdd,cor[1]-2*yAdd])
    design.append([cor[0]+3*xAdd,cor[1]-3*yAdd])

    return design


###############################################################################
def jMinoCreate(cor,direction,real):  # cor(list(int,int)),direction(int),real(bool),prints j shape mino on board

    r1 = 0
    r2 = 0
    r3 = 0

    if real:
        visual = blue

    else:
        visual = white

    if direction == 1:
        r1 = SPACING
    
    elif direction == 2:
        r2 = 2*SPACING

    elif direction == 3:
        r1 = SPACING
        r3 = 2*SPACING

    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING-r3,cor[1]-r1+r3,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+r1,cor[1]+r1,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+r1+r2,cor[1]-SPACING+r2,SPACING,SPACING])

def jMinoInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    j mino's 4 pieces
    design = []
    r1 = 0
    r2 = 0
    r3 = 0

    if direction == 1:
        r1 = SPACING
    
    elif direction == 2:
        r2 = 2*SPACING

    elif direction == 3:
        r3 = 2*SPACING
        r1 = SPACING

    design.append([cor[0],cor[1]])
    design.append([cor[0]+SPACING-r3,cor[1]-r1+r3])
    design.append([cor[0]-SPACING+r1,cor[1]+r1])
    design.append([cor[0]-SPACING+r1+r2,cor[1]-SPACING+r2])   

    return design

##################################################################################

def bootLCreate(cor,direction,real):  # cor(list(int,int)),direction(int),real(bool),prints L shape mino on board
    r1 = 0
    r2 = 0
    r3 = 0

    if real:
        visual = orange

    else:
        visual = white

    if direction == 1:
        r1 = SPACING
    
    elif direction == 2:
        r2 = 2*SPACING

    elif direction == 3:
        r1 = SPACING
        r3 = 2*SPACING

    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+r1,cor[1]+r1,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING-r3,cor[1]+r1-r3,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING-r1-r2,cor[1]-SPACING+r2,SPACING,SPACING])

def bootLInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    L mino's 4 pieces
    design = []
    r1 = 0
    r2 = 0
    r3 = 0

    if direction == 1:
        r1 = SPACING
    
    elif direction == 2:
        r2 = 2*SPACING

    elif direction == 3:
        r1 = SPACING
        r3 = 2*SPACING

    design.append([cor[0]-SPACING+r1,cor[1]+r1])
    design.append([cor[0],cor[1]])
    design.append([cor[0]+SPACING-r3,cor[1]+r1-r3])
    design.append([cor[0]+SPACING-r1-r2,cor[1]-SPACING+r2])

    return design

####################################################################################
def oMinoCreate(cor,real): # cor(list(int,int)),real(bool),prints o shape mino on board
    if real:
        visual = yellow

    else:
        visual = white

    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING,cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING,cor[1]-SPACING,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1]-SPACING,SPACING,SPACING])

def oMinoInfo(cor): # cor(list(int,int)), provides coordinates of t mino's 4 pieces
    design = []
    
    design.append([cor[0],cor[1]])
    design.append([cor[0]+SPACING,cor[1]])
    design.append([cor[0]+SPACING,cor[1]-SPACING])
    design.append([cor[0],cor[1]-SPACING])

    return design

#####################################################################################
def sMinoCreate(cor,direction,real):  # cor(list(int,int)),direction(int),real(bool),prints s shape mino on board

    addend = 0

    if real:
        visual = green

    else:
        visual = white

    if direction%2 == 1:
        addend = 2*SPACING

    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]-SPACING+addend,cor[1],SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0],cor[1]-SPACING,SPACING,SPACING])
    pygame.draw.rect(gameDisplay,visual,[cor[0]+SPACING,cor[1]-SPACING+addend,SPACING,SPACING])

def sMinoInfo(cor,direction): # cor(list(int,int)), direction(int), provides coordinates of
                              #                                    s mino's 4 pieces

    design = []
    addend = 0

    if direction%2 == 1:
        addend = 2*SPACING

    design.append([cor[0],cor[1]])
    design.append([cor[0]-SPACING+addend,cor[1]])
    design.append([cor[0],cor[1]-SPACING])
    design.append([cor[0]+SPACING,cor[1]-SPACING+addend])

    return design
######################################################

def printMino(cor,blockType,direction,real): #cor(list(int,int)), blockType(int), direction(int), real(bool)
                                             #prints the proper mino on the gameBoard, based upon blockType
    if(blockType==0):
        tMinoCreate(cor,direction,real)

    elif(blockType==1):
        zMinoCreate(cor,direction,real)

    elif(blockType==2):
        longlCreate(cor,direction,real)

    elif(blockType==3):
        jMinoCreate(cor,direction,real)

    elif(blockType==4):
        bootLCreate(cor,direction,real)

    elif(blockType==5):
        oMinoCreate(cor,real)

    elif(blockType==6):
        sMinoCreate(cor,direction,real)
        
###############################################
        
def selectMino(cor,blockType,direction): #cor(list(int,int)), blockType(int), direction(int)
                                         #returns the coordinates of a mino's 4 blocks
    if(blockType==0):
        return tMinoInfo(cor,direction)

    elif(blockType==1):
        return zMinoInfo(cor,direction)

    elif(blockType==2):
        return longlInfo(cor,direction)

    elif(blockType==3):
        return jMinoInfo(cor,direction)

    elif(blockType==4):
        return bootLInfo(cor,direction)

    elif(blockType==5):
        return oMinoInfo(cor)

    elif(blockType==6):
        return sMinoInfo(cor,direction)
###############################################
    
def selectColor(blockType): #blockType(int), returns the color of a given mino, given the type of mino used
    if(blockType==0):
        return violet

    elif(blockType==1):
        return red

    elif(blockType==2):
        return cyan

    elif(blockType==3):
        return blue

    elif(blockType==4):
        return orange

    elif(blockType==5):
        return yellow

    elif(blockType==6):
        return green
    
########################################################################################################################################
def gameBoard(): #prints board used for game
    x = X_START
    y = Y_START
    rX = RX_START
    rY = RY_START

    while x<=(X_END):
        pygame.draw.rect(gameDisplay,black,[x,Y_START,B_DEPTH,Y_LENGTH])
        x+=SPACING
    while y<=(Y_END):
        pygame.draw.rect(gameDisplay,black,[X_START,y,X_LENGTH,B_DEPTH])
        y+=SPACING
    while rX<=(RX_END):
        pygame.draw.rect(gameDisplay,red,[rX,RY_START,R_DEPTH,RY_LENGTH])
        rX+=SPACING
    while rY<=(RY_END):
        pygame.draw.rect(gameDisplay,red,[RX_START,rY, RX_LENGTH, R_DEPTH])
        rY+=SPACING

######################################################
def safeMove(cor,blockType,direction,player,pSize): # cor(list(int,int)), blockType(int), direction(int),player(int) determines whether a given move is allowed

    global minoPieces

    for each in selectMino(cor,blockType,direction):

        if each[0] < X_START or each[0]>= X_END or each[1] < Y_START or each[1] >=Y_END:
            return False

        blc = (each[1]-Y_START)/SPACING
        blc *= (Y_LENGTH)/SPACING
        blc += (each[0]-X_START)/SPACING
        
        if blc>=((X_END-X_START)*(Y_END-Y_START)/(SPACING*SPACING)) or blc<0:
            return False

        elif minoPieces[blc]:
            return False

        for x in range(0,pSize):
            if player!=x:
                for other in selectMino(pivot[x],shape[x],pos[x]):
                    if other[0]==each[0] and other[1]==each[1]:
                        return False
    return True    

    
######################################################
def boardIntegration(cor,blockType,direction): #cor(list(int,int)),blockType(int),direction(int), makes the player's mino a part of the gameBoard                                                                                        
    global minoPieces
    global minoColor

    for each in selectMino(cor,blockType,direction):
        blc = (each[1]-Y_START)/SPACING
        blc *= (X_LENGTH)/SPACING
        blc+= (each[0]-X_START)/SPACING
        minoPieces[blc] = True
        minoColor[blc] = selectColor(blockType)

######################################################

def lineClearCheck(priority):

    global minoPieces
    global minoColor

    lines = 0

    startY = 0
    startX = 0

    endY = 0
    endX = 0
    
    if priority == 0:
        startY = (RY_END-Y_START)/SPACING
        
        endY = (Y_LENGTH)/SPACING
        endX = (X_LENGTH)/SPACING

        clearCount = endX

    elif priority == 1:
        startX = 0

        endY = (Y_LENGTH)/SPACING
        endX = (RX_START-X_START)/SPACING

    elif priority == 2:
        startY = 0


        endY = (RY_START-Y_START)/SPACING
        endX = (X_LENGTH)/SPACING

    else:
         startX = (RX_END-X_START)/SPACING

         endY = (Y_LENGTH)/SPACING
         endX = (X_LENGTH)/SPACING


    if priority%2==0:
        i = startY
        while i<endY:
            count = 0
            j=0
            while j<endX:
                if minoPieces[i*(X_LENGTH/SPACING)+j]:
                    count+=1
                else:
                    j=endX
                j+=1

            if count == endX:
                lines+=(100+lines)
                j=i
                i-=1

                while (priority==0 and j>startY) or (priority==2 and j<endY):
                    k=0                
                    while k<endX:
                        temp = j-1

                        if priority == 2:
                            temp = j+1
                        
                        minoPieces[j*(X_LENGTH/SPACING)+k]=minoPieces[(temp)*(X_LENGTH/SPACING)+k]

                        if minoPieces[j*(X_LENGTH/SPACING)+k]:
                            minoColor[j*(X_LENGTH/SPACING)+k]=minoColor[(temp)*(X_LENGTH/SPACING)+k]

                        else:
                            minoColor[j*(X_LENGTH/SPACING)+k] = white
                            
                        k+=1

                    if priority == 0:
                        j-=1

                    else:
                        j+=1
                    
            i+=1
            
    else:
        i=startX
        while i<endX:
            count = 0
            j=0
            while j<endY:
                if minoPieces[j*(X_LENGTH/SPACING)+i]:
                    count+=1
                else:
                    j=endY
                j+=1
            if i == (X_LENGTH-SPACING)/SPACING:
                print count
                print "over"
                print endY

            if count == endY:
                lines+=(100+lines)
                j=i
                i-=1
                while (priority == 1 and j<endX) or (priority == 3 and j>startX):
                    k=0
                    while k<endY:
                        temp = j+1

                        if priority == 3:
                            temp = j-1
                            
                        minoPieces[k*(X_LENGTH/SPACING)+j]=minoPieces[k*(X_LENGTH/SPACING)+temp]

                        if minoPieces[k*(X_LENGTH/SPACING)+j]:
                            minoColor[k*(X_LENGTH/SPACING)+j]=minoColor[k*(X_LENGTH/SPACING)+temp]

                        else:
                            minoColor[k*(X_LENGTH/SPACING)+j]=white

                        

                        k+=1
                    if priority == 1:
                        j+=1

                    else:
                        j-=1

            i+=1
           
    return lines
 

######################################################
######################################################
###########     Menu Mechanics        ################
######################################################
######################################################

def placeMessage(msg,color,size,xLevel,yLevel):
    font = pygame.font.SysFont('Arial',size,True,True)
    titleSurf = font.render(msg,True,color)
    
    gameDisplay.blit(titleSurf,[xLevel,yLevel])   

def gameTitle():


    gameDisplay.fill(white)
    font = pygame.font.SysFont('Arial',100,True,True)
    titleSurf = font.render("Gravris",True,orange)
    titleRect = titleSurf.get_rect()
    titleRect.center = MAX_X/2,MAX_Y/4

    gameDisplay.blit(titleSurf,titleRect)

    placeMessage("Press p to start",black,30,MAX_X/8,300)
    placeMessage("Press c to change controls",black,30,MAX_X/8,350)
    
    pygame.display.update()

    while True:        #event module
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                return event

            elif event.type==pygame.QUIT:
                return event
########################################################
################################################################################
################################################################################
################################################################################

def controlEdit(repeat):

    global PLAYER_CONTROLS

    gameDisplay.fill(white)

    placeMessage("Player Controls", black, 75,0,0)
    placeMessage("Pause Game: ESCAPE Key(cannot be changed)",black, 25,50,500)
    placeMessage("Enter the key of an assigned command to change its key", black, 20, 50, 600)
    placeMessage("Bracket numbers like [2] represent keypad numbers", black, 20, 50, 625)
    i=0

    displace = [] #used for message displacement and color

    while i<4:
        displace.append([])
        i+=1
    i=0
    
    displace[0].append(0)
    displace[0].append(0)
    displace[0].append(green)
    displace[1].append(0)
    displace[1].append(200)
    displace[1].append(violet)
    displace[2].append(350)
    displace[2].append(0)
    displace[2].append(blue)
    displace[3].append(350)
    displace[3].append(200)
    displace[3].append(orange)

    while i<4:  #display info
        placeMessage("".join(["Player  ",str(i+1),": "]),displace[i][2],25,0+displace[i][0],100+displace[i][1])

        placeMessage("Shift1 key: ", black, 20, 20+displace[i][0], 125+displace[i][1])
        placeMessage(pygame.key.name(PLAYER_CONTROLS[i][0]),red,20, 130+displace[i][0],125+displace[i][1])

        placeMessage("Shift2 key: ", black, 20, 20+displace[i][0], 150+displace[i][1])
        placeMessage(pygame.key.name(PLAYER_CONTROLS[i][1]),red,20, 130+displace[i][0],150+displace[i][1])

        placeMessage("Rotate key: ", black, 20, 20+displace[i][0], 175+displace[i][1])
        placeMessage(pygame.key.name(PLAYER_CONTROLS[i][2]),red,20, 130+displace[i][0],175+displace[i][1])

        placeMessage("Soft Drop key: ", black, 20, 20+displace[i][0], 200+displace[i][1])
        placeMessage(pygame.key.name(PLAYER_CONTROLS[i][3]),red,20, 170+displace[i][0],200+displace[i][1])

        placeMessage("Hard Drop key: ", black, 20, 20+displace[i][0], 225+displace[i][1])
        placeMessage(pygame.key.name(PLAYER_CONTROLS[i][4]),red,20, 170+displace[i][0],225+displace[i][1])

        i+=1


    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_ESCAPE:
                    return event
                
                match = False
                control = [-1,-1]

                for player in PLAYER_CONTROLS:  #confirm whether key is currently used
                    for command in player:
                        if command == event.key:
                            match = True
                            control = [PLAYER_CONTROLS.index(player),player.index(command)]
                            
                if match:
                    pygame.draw.rect(gameDisplay,white,[50,625, 550, 25])
                    placeMessage("Enter replacement key(ESC cannot be used)", black, 20, 50, 625)
                    pygame.display.update()

                    complete = False

                    while not complete:        #repeat until replacement is made            
                        replaceFound = False
                        replacement = event

                        while not replaceFound:     #collect replacement key
                            for command in pygame.event.get():
                                if command.type == pygame.QUIT:
                                    return command
                                if command.type == pygame.KEYDOWN:
                                    replacement = command
                                    replaceFound = True
                                    
                        match = False 
                        for player in PLAYER_CONTROLS:  #ensure replacement key isn't being used
                            for command in player:
                                if replacement.key==command:
                                    match=True
                                    
                        if replacement.key==event.key:
                            pass
                            complete = True

                        elif match:
                            pygame.draw.rect(gameDisplay,white,[50,625, 550, 25])
                            placeMessage("Key is currently being used. Try Again", black, 20, 50, 625)
                            pygame.display.update()

                        elif replacement.key!=pygame.K_ESCAPE:
                            PLAYER_CONTROLS[control[0]][control[1]] = replacement.key
                            complete = True
                    
                    return repeat
            
            if event.type==pygame.QUIT:
                return event
        
################################################################################
################################################################################
################################################################################
################################################################################
def playerNum():
    
    gameDisplay.fill(white)
    placeMessage("Select Number of Players",black,20,0,125)

    i=1
    while i<=4:
        pygame.draw.rect(gameDisplay, black,[-75+i*100,200,20,20])
        placeMessage(str(i),white,20,-75+i*100,200)
        i+=1

    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return event,0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                i=1
                while i<=4:
                    if x>=(i*100-75) and x<=(i*100-55) and y>=200 and y<=220:
                        return event,i
                    i+=1
    
def gameLoop(option,players):

    if not players>=1 and players<=4:
        return option
    
    tCountM = 2
    tCountS = 1
    tCountT = FPS-1

    duration = []
    counter = []
    
    for x in range(0,players):
        counter.append(1)
        duration.append(25)

    default = 25

    gameDisplay.fill(white)

    shiftCount = []
    shiftRate = []
    key_press = []

    score = []
    
    finished = []
    gameExit = 0

    for x in range(0,players):
        shiftCount.append(0)     
        shiftRate.append(1)
        key_press.append(pygame.QUIT)

        score.append([x,0])
        
        finished.append(False)
        minoInitialize(x,random.randint(0,6))
        printMino(pivot[x],shape[x],pos[x], True)
        
    while gameExit<players and (tCountM>0 or tCountS>0):

        gameExit = 0
        
        for x in range(0,players):
            if not finished[x]:
                printMino(pivot[x],shape[x],pos[x], False)     
                if(counter[x]==0): #gravity module for tetris mino

                    if safeMove(MINO_future("gravity",x+1,pivot[x]),shape[x],pos[x],x,players):
                        MINO_gravity(x)

                    else:
                        boardIntegration(pivot[x],shape[x],pos[x])
                        minoInitialize(x,((shape[x]+random.randint(1,6))%7) )

                        if not safeMove(pivot[x],shape[x],pos[x],x,players):
                            finished[x] = True
                            
                        indx = 0

                        while x!=score[indx][0]:
                            indx+=1

                        score[indx][1]+=lineClearCheck(x)

                        indx2 = 0

                        if indx>0:
                            indx2 = indx-1

                        while score[indx][1] > score[indx2][1]:
                            temp = score[indx2]
                            score[indx2] = score[indx]
                            score[indx]=temp
                            
                            indx-=1

                            if indx==0:
                                indx2=0

                            else:
                                indx2=indx-1

        pileDisplay()
        for x in range(0,players):
            if not finished[x]:
                printMino(pivot[x],shape[x],pos[x], True)
            pygame.draw.rect(gameDisplay,white,[X_END,x*10,MAX_X-X_END,10])
            placeMessage("".join(["Player ",str(score[x][0]+1), ": ",str(score[x][1])]),black,10,X_END,x*10)

        gameBoard()
        pygame.display.update()

        for x in range(0,players):
            if not finished[x]:
                if shiftRate[x]>1 and shiftCount[x]==0:   #module that continues shift1 and shift2 while key is still pressed

                    printMino(pivot[x],shape[x],pos[x], False)
                    
                    if key_press[x] == PLAYER_CONTROLS[x][0]:
                        if safeMove(MINO_future("FShift",x+1,pivot[x]), shape[x],pos[x],x,players):
                            MINO_FShift(x)

                    elif key_press[x] ==PLAYER_CONTROLS[x][1]:
                        if safeMove(MINO_future("RShift",x+1,pivot[x]),shape[x],pos[x],x,players):
                            MINO_RShift(x)

                    printMino(pivot[x],shape[x],pos[x], True)
                    gameBoard()
        pygame.display.update()

        for event in pygame.event.get(): #event module 
            for x in range(0,players):
                if not finished[x]:
                    if event.type == pygame.QUIT:
                        return event
                    if event.type != pygame.KEYDOWN:
                        key_press[x] = pygame.QUIT
                        duration[x] = default
                        shiftRate[x] = 1
                    if event.type == pygame.KEYDOWN:
                        printMino(pivot[x],shape[x],pos[x],False)
                        if event.key == PLAYER_CONTROLS[x][0]:
                            if safeMove(MINO_future("FShift",x+1,pivot[x]), shape[x],pos[x],x,players):
                                MINO_FShift(x)
                                shiftRate[x] = 5
                                key_press[x] = event.key
                        elif event.key == PLAYER_CONTROLS[x][1]:
                            if safeMove(MINO_future("RShift",x+1,pivot[x]),shape[x],pos[x],x,players):
                                MINO_RShift(x)
                                shiftRate[x] = 5
                                key_press[x] = event.key
                        elif event.key == PLAYER_CONTROLS[x][2]:
                            if safeMove(pivot[x],shape[x],(pos[x]+1)%4,x,players):
                                MINO_rotate(x)
                        elif event.key == PLAYER_CONTROLS[x][3]:
                            key_press[x] = event.key
                            duration[x] = 5
                        elif event.key == PLAYER_CONTROLS[x][4]:
                            while safeMove(MINO_future("gravity",x+1,pivot[x]),shape[x],pos[x],x,players):
                                MINO_gravity(x)
                            counter[x] = duration[x]-1
                        printMino(pivot[x],shape[x],pos[x], True)
                        gameBoard()
                        if event.key == pygame.K_ESCAPE:
                            placeMessage("Paused(press escape to return to game)", black, 15, 100,0)
                            pygame.display.update()
                            pause = True
                            while pause:
                                for event in pygame.event.get():
                                    if event.type==pygame.KEYDOWN:
                                        if event.key==pygame.K_ESCAPE:
                                            pygame.draw.rect(gameDisplay,white,[100,0,400,20])
                                            pause = False
        
        for x in range(0,players):
            if not finished[x]:
                counter[x]=(counter[x]+1)%duration[x]
                shiftCount[x]=(shiftCount[x]+1)%shiftRate[x]

            else:
                gameExit+=1

        tCountT+=1

        if tCountT==FPS:
            tCountT = 0

            if tCountS==0:
                tCountM-=1
                tCountS=59
                
            else:
                tCountS-=1

            gameTime = []
            gameTime.append(str(tCountM))
            gameTime.append(':')
            if tCountS<10:
                gameTime.append('0')
            gameTime.append(str(tCountS))

            pygame.draw.rect(gameDisplay,white,[500,630,100,20])
            placeMessage( ''.join(gameTime),black,20,500,630)
                
        pygame.display.update()
        clock.tick(FPS)

    #reinitialize pile for next run
    del minoPieces[:]
    del minoColor[:]
    for i in range((X_END-X_START)*(Y_END-Y_START)/(SPACING*SPACING)): 
        minoPieces.append(False)
        minoColor.append(white)

    placeMessage("Game Over",black,40,100,300)
    placeMessage("Press ESC to return to the menu", black,30, 150, 340)

    placement = 1

    for x in range(0,players):
        placeMessage("".join(["#  ",str(placement),":   Player ",str(score[x][0]+1), ": ",str(score[x][1])]),black,20,100,430+x*20)

        if x!=(players-1):
            if score[x][1]!=score[x+1][1]:
                placement+=1
            
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return event
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return event

############################################################################################################################################

            
#MAIN PROGRAM
option = gameTitle()
while option.type != pygame.QUIT:
    while option.type == pygame.KEYDOWN:
        if option.key == pygame.K_c:
            option = controlEdit(option)
        elif option.key == pygame.K_p:
            option,participants = playerNum()
            option = gameLoop(option,participants)    
        else:
            option = gameTitle()

pygame.quit()
quit()
