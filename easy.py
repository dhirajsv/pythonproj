import pygame
import random
import math

from pygame import mixer

pygame.init()


#Create screen
screen = pygame.display.set_mode((800,600))


#Background
background=pygame.image.load("background.png")

#Background Sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("Asteroids")
icon=pygame.image.load("meteor.png")
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load("jet.png")
playerX=370
playerY=530
playerX_change=0


#Missile
missileImg = pygame.image.load("missile.png")
missileX=0
missileY=530
missileX_change=0
missileY_change=10
missile_state = "ready"

#Multiple Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = 0.4
num_enemies = 4

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("asteroid.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(20,150))

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 642
textY = 10

#Gameover
gameover_font = pygame.font.Font("freesansbold.ttf", 90)

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(0,255,0))
    screen.blit(score, (x,y))

def game_over():
    over_text = font.render("GAME OVER !!!  FINAL Score :" + str(score_value),True,(0,255,0))
    screen.blit(over_text, (170,250))

def player(x,y):
    screen.blit(playerImg, (x,y))
    
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
    
def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x+16,y+10))
    
def isCollision(enemyX,enemyY,missileX,missileY):
    dist=math.sqrt(math.pow((enemyX-missileX),2)+(math.pow((enemyY-missileY),2))) 
    if dist < 30:
        return True
    else:
        return False
    
    
#Game loop
running = True
while running: 
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False
             
             
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-4
            if event.key == pygame.K_RIGHT:
                playerX_change=4
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missile_Sound = mixer.Sound("laser.wav")
                    missile_Sound.play()
                    missileX = playerX
                    fire_missile (missileX,missileY)
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
    #Player Movement            
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    #Enemy Movement
    for i in range(num_enemies):
        
        #Gameover
        if enemyY[i] > 500:
            for j in range(num_enemies):
                enemyY[j] = 3000
            game_over()
            break
        enemyY[i] += enemyY_change
        
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],missileX,missileY)
        if collision:
            collision_Sound = mixer.Sound("explosion.wav")
            collision_Sound.play()
            missileY=530
            missile_state = "ready"
            score_value += 1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(25,150)
        enemy(enemyX[i],enemyY[i],i)
    
    
   
        
        
    #Missile Movement
    if missileY <= -10:
        missileY = 530
        missile_state = "ready"
    if missile_state == "fire":
        fire_missile(missileX,missileY)
        missileY -= missileY_change
   
        
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
    
         
            
