import pygame
import random
from pygame.locals import *
import sys
pygame.init()
SCREENHEIGHT = 500
SCREENWIDTH = 280
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pipe = pygame.transform.scale(pygame.image.load('game//pipe.png').convert_alpha(),(50,100))

sky = pygame.transform.scale(pygame.image.load('game//sky.jpg').convert_alpha(),(280,500))
rabbit = pygame.transform.scale(pygame.image.load('game//rabbit.png').convert_alpha(),(50,50))
base = pygame.transform.scale(pygame.image.load('game//base.jpg').convert_alpha(),(280,100))
cloud = pygame.transform.scale(pygame.image.load('game//cloud.png').convert_alpha(),(50,50))
pygame.display.set_caption('RABBIT RUN')
FPSCLOCK = pygame.time.Clock()
GAME_SOUNDS = {}
GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

GAME_SPRITES = {
    '0' : pygame.image.load('gallery//sprites//0.png'),
    '1' : pygame.image.load('gallery//sprites//1.png'),
    '2' : pygame.image.load('gallery//sprites//2.png'),
    '3' : pygame.image.load('gallery//sprites//3.png'),
    '4' : pygame.image.load('gallery//sprites//4.png'),
    '5' : pygame.image.load('gallery//sprites//5.png'),
    '6' : pygame.image.load('gallery//sprites//6.png'),
    '7' : pygame.image.load('gallery//sprites//7.png'),
    '8' : pygame.image.load('gallery//sprites//8.png'),
    '9' : pygame.image.load('gallery//sprites//9.png')
}


def getRandomPipe(score) :
    global playerVelY,playerY,playerAcc,obstacle_speed,cloudX,pipes,playerY,newPipe,baseY,playerX,playerJumped,pipeX_init,pipeY,score_down
    score_down = False
    maxPipeY = SCREENHEIGHT - int(pipe.get_height()/2) - base.get_height() + int(score/400)
    minPipeY = SCREENHEIGHT - int(pipe.get_height()) - base.get_height() + int(score/400)
    pipeY = random.randint(minPipeY,maxPipeY)
    return {'x' : pipeX_init , 'y' : pipeY}


player_vel_init = -20
score = 0
playerY = SCREENHEIGHT - base.get_height() - rabbit.get_height()
baseY = SCREENHEIGHT - base.get_height()
playerX = SCREENWIDTH * 0.13
score_down = False
playerVelY = 0
playerMaxVelY = 10
playerMinVelY = -8
playerAcc = 1
pipeX_init = 300
FPS=32
cloudX = 350
pipes=[]
newPipe = getRandomPipe(score)
pipes.append(newPipe)
pipeY = pipes[0]['y']
cloud_on_screen = []
clouds =[
    [SCREENWIDTH + cloud.get_width()*2,cloud.get_height()*3],
    [SCREENWIDTH + cloud.get_width()*6,cloud.get_height()*7],
    [SCREENWIDTH + cloud.get_width()*4,cloud.get_height()*1],
    [SCREENWIDTH + cloud.get_width()*1,cloud.get_height()*5],
    [SCREENWIDTH + cloud.get_width()*0,cloud.get_height()*8]
]
cloud_pos = []
obstacle_speed = -5
playerYList = [SCREENHEIGHT - base.get_height() - rabbit.get_height()]
playerVelY = -20
playerJumped = [False,False]


def welcomeScreen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN  and event.key == K_SPACE:
                
                return 
                
            else:
                screen.blit(pygame.image.load('game//message.jpg').convert_alpha(),(0,0))
                pygame.display.update()

def reset():
    global pipes,score,playerX,playerY,player_vel_init,score_down,playerVelY,pipeX_init
    
    player_vel_init = -20
    score = 0
    playerY = SCREENHEIGHT - base.get_height() - rabbit.get_height()
    baseY = SCREENHEIGHT - base.get_height()
    playerX = SCREENWIDTH * 0.13
    score_down = False
    playerVelY = 0
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAcc = 1
    pipeX_init = 300
    FPS=32
    cloudX = 350
    pipes=[]
    newPipe = getRandomPipe(score)
    pipes.append(newPipe)
    pipeY = pipes[0]['y']
    cloud_on_screen = []
    clouds =[
        [SCREENWIDTH + cloud.get_width()*2,cloud.get_height()*3],
        [SCREENWIDTH + cloud.get_width()*6,cloud.get_height()*7],
        [SCREENWIDTH + cloud.get_width()*4,cloud.get_height()*1],
        [SCREENWIDTH + cloud.get_width()*1,cloud.get_height()*5],
        [SCREENWIDTH + cloud.get_width()*0,cloud.get_height()*8]
    ]
      
    obstacle_speed = -5
    playerYList = [SCREENHEIGHT - base.get_height() - rabbit.get_height()]
    playerVelY = -20
    playerJumped = [False,False]


def blit_rabbit() :
    global playerVelY,playerY,playerAcc,obstacle_speed,cloudX,pipes,playerY,newPipe,baseY,playerX
    if playerJumped[0]  or playerY < baseY - rabbit.get_height() :
        playerY += playerVelY
        playerVelY += playerAcc
        
    else:
        playerVelY = 0

    return playerY
    

for i in range(5) :
    cloud_pos.append(clouds[i][0])

def blit_cloud() :
    global clouds,cloudX,cloud_on_screen

    cloud_list=[]
    for i in range(5) : 
        if cloud_pos[i] < -(cloud.get_width()):
            cloud_pos[i] = clouds[i][0]
        cloud_pos[i] += obstacle_speed
        cloud_list.append({'cloudX' : cloud_pos[i],'cloudY' : clouds[i][1]})
    return cloud_list


def crash_test() :
    global pipes,pipeY,playerX,playerY
    playerMidPosX = playerX + (rabbit.get_width()/2)
    pipeMidPosX = pipes[0]['x'] + (pipe.get_width()/2)
    if playerX + rabbit.get_width() >= pipes[0]['x'] and playerY + rabbit.get_height() >pipeY :
        if -((rabbit.get_width() + pipe.get_width())/2) <= (playerMidPosX-pipeMidPosX) <= ((rabbit.get_width() + pipe.get_width())/2):
            return [True,playerMidPosX,pipeMidPosX]    # [collision, playerMidPosX,pipeMidPosX]
        else:
            return [False,playerMidPosX,pipeMidPosX]
    else:
        return [False,playerMidPosX,pipeMidPosX]

def blit_pipe(pipeX,score) :
    global playerVelY,playerY,playerAcc,obstacle_speed,pipeY,cloudX,pipes,playerY,newPipe,baseY,playerX,playerJumped,pipeX_init
    pipeX += obstacle_speed
    if pipes[0]['x'] < -(pipe.get_width()):
        pipes.pop(0)
        newPipe = getRandomPipe(score)
        pipes.append(newPipe)
        pipeX_init = 300
    else:
        pipes.pop(0)
        pipes.append({'x' : pipeX, 'y' : pipeY})
    
    return pipes

def endScreen(score) :
    endMessage = pygame.image.load("game//endMessage.jpg").convert_alpha()
    score_list = list(str(score))
    GAME_SOUNDS['die'].play()
    while True :
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_SPACE:
                return
    
        number_width = GAME_SPRITES['0'].get_width()
        screen.blit(endMessage,(0,0))
        for i in range(len(score_list)) :
            screen.blit(GAME_SPRITES[score_list[i]],(((SCREENWIDTH-number_width*len(score_list))/2) + GAME_SPRITES['0'].get_width()*i , (SCREENHEIGHT-GAME_SPRITES['0'].get_height())/2))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    

def mainGame():
    global playerY,playerVelY,playerJumped,pipeX_init,newPipe,pipeY,score,obstacle_speed,player_vel_init,score_down
    
    while True:
        if playerJumped == [True,True] and baseY - 5 <= playerY + rabbit.get_height() <= baseY + 5 :
            playerJumped = [False,False]
        for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if playerJumped[1] == False :
                    playerVelY = player_vel_init
                if playerJumped[0] :
                    playerJumped[1] = True
                playerJumped[0] = True
                GAME_SOUNDS['wing'].play()

        collide = crash_test()

        playerY = blit_rabbit()
        
        if collide[0]:
            GAME_SOUNDS['hit'].play()
            return
            

        elif -((rabbit.get_width() + pipe.get_width())/2) <= (collide[1] - collide[2]) <= ((rabbit.get_width() + pipe.get_width())/2):
            if not score_down :
                score += 1
                GAME_SOUNDS['point'].play()
                score_down = True
                
        if pipes[0]['y'] - playerVelY <= playerY + rabbit.get_height() <= pipes[0]['y'] + playerVelY and -((rabbit.get_width() + pipe.get_width())/2) <= (collide[2]-collide[1]) <= ((rabbit.get_width() + pipe.get_width())/2) :
            playerVelY = 0
            playerY = pipes[0]['y'] - rabbit.get_height()

        if playerY + rabbit.get_height() <= 0:
            return

        if playerY + rabbit.get_height() > baseY :
            playerY = baseY - rabbit.get_height()

        player_vel_init += (score/8000)
        pipeX_init += (score/10)
        obstacle_speed -= (score/7000)

        pipe_data = blit_pipe(pipes[0]['x'],score)
        cloud_data = blit_cloud()

        screen.blit(sky,(0,0))
        for i in range(5):
            screen.blit(cloud,(cloud_data[i]['cloudX'],cloud_data[i]['cloudY']))
        
        screen.blit(pipe,(pipe_data[0]['x'],pipe_data[0]['y']))
        screen.blit(base,(0,baseY))
        screen.blit(rabbit,((int(playerX)),(int(playerY))))

        score_list = list(str(score))
        number_width = GAME_SPRITES['0'].get_width()

        for i in range(len(score_list)) :
            screen.blit(GAME_SPRITES[(score_list[i])],(((SCREENWIDTH-number_width*len(score_list))/2) + GAME_SPRITES['0'].get_width()*i,SCREENHEIGHT*0.13))
        pygame.display.update()
        FPSCLOCK.tick(FPS)



while True:
    reset()
    welcomeScreen()
    mainGame()
    endScreen(score)