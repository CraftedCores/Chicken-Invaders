import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen with a resolution of 800x600 pixels
screen = pygame.display.set_mode((800, 600))

# Load the background image
background = pygame.image.load('ChickenInvaderBackground.png')

# Load and play background music on a loop
mixer.music.load('8_Bit_Adventure.mp3')
mixer.music.play(-1)  # -1 makes the music loop indefinitely
mixer.music.set_volume(0.3)  # Set the volume to 30%

# Set the game title and window icon
pygame.display.set_caption("Chicken Invaders")
icon = pygame.image.load('Chicken Icon.png')
pygame.display.set_icon(icon)

# Initialize player properties
playerImg = pygame.image.load('Cat.png')  # Player sprite
playerX = 370  # Initial X position of the player
playerY = 480  # Fixed Y position of the player
playerX_change = 0  # Horizontal movement speed

# Initialize enemy properties
enemyImg = []  # List to store enemy sprites
enemyX = []  # List to store enemy X positions
enemyY = []  # List to store enemy Y positions
enemyX_change = []  # List to store enemy horizontal speed
enemyY_change = []  # List to store enemy vertical speed
numEnemies = 6  # Number of enemies in the game

# Create multiple enemies with random positions
for i in range(numEnemies):
    enemyImg.append(pygame.image.load('Chicken.png'))  # Load enemy sprite
    enemyX.append(random.randint(0, 736))  # Random starting X position
    enemyY.append(random.randint(50, 150))  # Random starting Y position
    enemyX_change.append(4)  # Horizontal speed of enemies
    enemyY_change.append(40)  # Distance enemies move down when they hit the screen edge

# Initialize bullet properties
bulletImg = pygame.image.load('Bullet.png')  # Bullet sprite
bulletX = 0  # Bullet's X position
bulletY = 480  # Bullet's initial Y position
bulletY_change = 10  # Speed of the bullet
bullet_state = "ready"  # Bullet state: "ready" (not fired) or "fire" (in motion)

# Initialize score properties
score_value = 0  # Player's score
font = pygame.font.Font('freesansbold.ttf', 32)  # Font for score display
textX = 10  # X position for the score display
textY = 10  # Y position for the score display

# Font for the "Game Over" text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Function to display the score on the screen
def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to display the "Game Over" text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Function to draw the player sprite
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw an enemy sprite
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Position the bullet slightly above the player

# Function to detect a collision between an enemy and the bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Simplified collision check using a distance threshold
    return abs(enemyX - bulletX) < 27 and abs(enemyY - bulletY) < 27

# Main game loop
running = True
while running:
    clock.tick(60)  # Limit the frame rate to 60 frames per second
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(background, (0, 0))  # Draw the background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            running = False
        if event.type == pygame.KEYDOWN:  # Handle key press events
            if event.key == pygame.K_LEFT:  # Move left
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # Move right
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # Fire bullet
                mixer.Sound('laser.wav').play()
                bulletX = playerX  # Set bullet's X position to player's X
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # Stop movement when key is released
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    # Update player position and ensure it stays within screen bounds
    playerX += playerX_change
    playerX = max(0, min(playerX, 736))  # Keep player within screen width

    # Update enemy positions
    for i in range(numEnemies):
        # Check if any enemy reaches the player
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000  # Move all enemies off screen
            game_over_text()
            # running = False  # Uncomment to stop the game loop
            break

        # Move the enemy and bounce it off the edges
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]  # Move enemy down when it hits the screen edge

        # Check for collision with the bullet
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            mixer.Sound('ChickenSound.wav').play()
            bulletY = 480  # Reset bullet position
            bullet_state = "ready"
            score_value += 1  # Increment score
            # Reset enemy position
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # Draw the enemy

    # Move the bullet if it has been fired
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:  # Reset bullet if it moves off screen
            bulletY = 480
            bullet_state = "ready"

    # Draw the player and score
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # Update the display


