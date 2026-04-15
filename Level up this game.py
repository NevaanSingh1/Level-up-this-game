import math
import random
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 1
ENEMY_SPEED_Y = 3
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('background.png')

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0

#Enemy
enemyImg = []
enemyX= []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for _i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, SCREEN_WIDTH -64))#64 is the size of the enemy
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = PLAYER_START_Y
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready"



# Score
score_value = 0
# Use system font for better compatibility
font = pygame.font.SysFont("arial", 32)
textX = 10
textY = 10

#Game Over Text
# Use system font for game over as well
over_font = pygame.font.SysFont("arial", 64)

def show_score(x,y):
    score = font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))


def game_over_text():
    # Display the game over text
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,250))

def player(x,y):
    #Draw the player on the screen
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    #Draw an enemy on the screen
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    #Fire a bullet from the player's postion
    global bullet_state
    bullet_state ="fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
#Check if there is a collision between the enemy and a bullet  
   distance = math.sqrt((enemyX-bulletX)**2+(enemyY-bulletY)**2)
   return distance < COLLISION_DISTANCE

# Game Loop
running = True
bullet_state = "ready"
game_over = False
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                bullet_state = "fire"
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
            playerX_change = 0
    
    #Player Movement
    playerX += playerX_change
    playerX = max(0, min(playerX, SCREEN_WIDTH - 64)) # 64 is the size of the player

    if not game_over:
        #Enemy Movement
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j]= 2000
                game_over = True
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]  # Move enemies down only when hitting the edge
            enemy(enemyX[i], enemyY[i], i)
            #Collision Check
            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = PLAYER_START_Y
                bullet_state = "ready"
                score_value += 1
                enemyX[i]= random.randint(0, SCREEN_WIDTH -64)
                enemyY[i]= random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
                # Level up logic
                if score_value >= 20:
                    ENEMY_SPEED_X += 1
                    ENEMY_SPEED_Y += 1
                    BULLET_SPEED_Y += 1
                    score_value = 0  # Reset score after leveling up
                    print("Congratulations! You've progressed to the next level of this game!")
        # Bullet Movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = PLAYER_START_Y
                bullet_state = "ready"
    else:
        game_over_text()

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()